"""Keyframe extraction and confirmation for video Sources."""

from __future__ import annotations

import math
import shutil
import subprocess
import uuid
from pathlib import Path

from .. import contract
from ..common import atomic_write, canonical_json, read_stable, sha256_bytes
from ..front_matter import FrontMatter
from ..paths import RepoPaths

_FRAMES_SCHEMA = "video-frames/v1"


def _frame_result(domain: dict) -> dict:
    """把 VideoFrameService 的遗留 state dict 归一为 contract 信封（加法式）。

    ``state == "applied"`` → ``ok`` + ``changed=True``；其余（blocked）→ ``blocked``，
    顶层 error_code 取已登记的具体码，动态/未预期码归伞码 ``video_frame_failed``
    并把原始码放进 ``errors[]``。领域字段（source_id/frame_count…）保留；顶层操作态
    ``state`` 收敛进 ``status``，不保留（避免双状态轴）。
    """
    fields = dict(domain)
    # 操作态 state(applied) 只表达成败，收敛到 status，不在顶层与 status 并列成双轴。
    applied = fields.pop("state", None) == "applied"
    if applied:
        return contract.ok(_FRAMES_SCHEMA, changed=True, **fields)
    raw = str(fields.pop("error_code", "video_frame_failed"))
    if raw in contract.ERROR_CODES:
        code = raw
    else:
        code = "video_frame_failed"
        fields.setdefault("errors", [{"code": raw}])
    return contract.blocked(_FRAMES_SCHEMA, code, **fields)


def _timestamp(value: float) -> str:
    if not math.isfinite(value) or value < 0:
        raise ValueError("frame_timestamp_invalid")
    millis = round(value * 1000)
    return f"{millis // 3_600_000:02d}:{(millis // 60_000) % 60:02d}:{(millis // 1000) % 60:02d}.{millis % 1000:03d}"


def _version(executable: str) -> str:
    try:
        result = subprocess.run(
            [executable, "-version"],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
        )
    except FileNotFoundError as exc:
        raise RuntimeError("extractor_unavailable:ffmpeg") from exc
    return (result.stdout or result.stderr).splitlines()[0].strip() or "unknown"


def extract_keyframes(
    media_path: Path,
    output_dir: Path,
    timestamps: list[float],
    *,
    executable: str = "ffmpeg",
) -> tuple[list[dict], dict]:
    """Extract one PNG per requested timestamp into a staging directory."""
    if not media_path.is_file():
        raise RuntimeError("frame_media_missing")
    if not timestamps:
        raise ValueError("frame_timestamps_missing")
    normalized = sorted(set(round(float(value), 3) for value in timestamps))
    labels = [_timestamp(value) for value in normalized]
    output_dir.mkdir(parents=True, exist_ok=True)
    version = _version(executable)
    frames = []
    for index, (seconds, label) in enumerate(zip(normalized, labels, strict=True), 1):
        filename = f"frame-{index:04d}-{label.replace(':', '')}.png"
        target = output_dir / filename
        command = [
            executable,
            "-hide_banner",
            "-loglevel",
            "error",
            "-ss",
            str(seconds),
            "-i",
            str(media_path),
            "-frames:v",
            "1",
            "-c:v",
            "png",
            "-y",
            str(target),
        ]
        try:
            result = subprocess.run(
                command,
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=300,
            )
        except FileNotFoundError as exc:
            raise RuntimeError("extractor_unavailable:ffmpeg") from exc
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError("frame_extraction_timeout") from exc
        if result.returncode != 0 or not target.is_file():
            raise RuntimeError("frame_extraction_failed")
        data = target.read_bytes()
        frames.append(
            {
                "index": index,
                "timestamp_seconds": seconds,
                "timestamp": label,
                "filename": filename,
                "sha256": sha256_bytes(data),
                "byte_length": len(data),
            }
        )
    return frames, {
        "extractor": "ffmpeg",
        "extractor_version": version,
        "options": {"format": "png", "timestamps_seconds": normalized},
    }


class VideoFrameService:
    """把派生关键帧抽取并附加到一个已存在的 video Source（直接写，ADR-0019）。"""

    def __init__(self, root: Path) -> None:
        self.root = Path(root)
        self.paths = RepoPaths(self.root)

    def _prepare(
        self,
        source_path: Path,
        media_path: Path,
        timestamps: list[float],
        *,
        executable: str = "ffmpeg",
    ) -> dict:
        """校验 source 类型并抽取关键帧到 staging；异常统一转结构化 blocked。"""
        try:
            metadata, _body = FrontMatter.parse(source_path.read_text(encoding="utf-8"))
            if metadata.get("source_type") != "video":
                return {"state": "blocked", "error_code": "source_not_video"}
            media_data, _stat = read_stable(media_path)
            staging = self.paths.frame_staging("frame-" + uuid.uuid4().hex)
            frames, extractor = extract_keyframes(
                media_path, staging, timestamps, executable=executable
            )
            payload = {
                "source_path": str(source_path.relative_to(self.root)),
                "source_id": metadata["id"],
                "media_hash": sha256_bytes(media_data),
                "staging": str(staging.relative_to(self.root)),
                "frames": frames,
                "extractor": extractor,
            }
            return {"state": "ready", "payload": payload}
        except (OSError, RuntimeError, ValueError) as exc:
            return {"state": "blocked", "error_code": str(exc)}

    def extract(
        self,
        source_path: Path,
        media_path: Path,
        timestamps: list[float],
        *,
        executable: str = "ffmpeg",
    ) -> dict:
        """抽取关键帧并附加到 source（ADR-0019：直接写，无 operation/锁/确认）。"""
        prepared = self._prepare(
            source_path, media_path, timestamps, executable=executable
        )
        if prepared["state"] != "ready":
            return _frame_result(prepared)
        return _frame_result(self._commit(prepared["payload"]))

    def _commit(self, record: dict) -> dict:
        """落盘：写关键帧与 manifest、更新 source front matter；失败清理 staging。"""

        def expire(error_code: str) -> dict:
            shutil.rmtree(self.root / record["staging"], ignore_errors=True)
            return {"state": "blocked", "error_code": error_code}

        source = self.root / record["source_path"]
        try:
            metadata, body = FrontMatter.parse(source.read_text(encoding="utf-8"))
            staging = self.root / record["staging"]
            if any(
                not (staging / frame["filename"]).is_file()
                for frame in record["frames"]
            ):
                return expire("frame_staging_missing")
            frame_dir = source.parent / "media" / "frames"
            frame_dir.mkdir(parents=True, exist_ok=True)
            attachments = metadata.setdefault("attachments", [])
            applied_files = []
            for frame in record["frames"]:
                source_frame = staging / frame["filename"]
                target_frame = frame_dir / frame["filename"]
                shutil.copyfile(source_frame, target_frame)
                attachments.append(
                    {
                        "filename": str(target_frame.relative_to(source.parent)),
                        "media_type": "image/png",
                        "sha256": frame["sha256"],
                        "role": "derived",
                        "kind": "frame",
                        "timestamp_seconds": frame["timestamp_seconds"],
                    }
                )
                applied_files.append(str(target_frame.relative_to(self.root)))
            manifest = {
                "schema_version": "video-frames/v1",
                "source_id": record["source_id"],
                "media_sha256": record["media_hash"],
                "extractor": record["extractor"],
                "frames": record["frames"],
            }
            manifest_path = frame_dir / "manifest.json"
            atomic_write(manifest_path, canonical_json(manifest) + b"\n")
            metadata["frame_manifest"] = {
                "path": str(manifest_path.relative_to(self.root)),
                "sha256": sha256_bytes(canonical_json(manifest) + b"\n"),
            }
            atomic_write(source, FrontMatter.render(metadata, body).encode("utf-8"))
            shutil.rmtree(staging, ignore_errors=True)
            return {
                "state": "applied",
                "source_id": record["source_id"],
                "frame_count": len(record["frames"]),
                "applied_files": applied_files
                + [str(manifest_path.relative_to(self.root))],
            }
        except (OSError, ValueError, KeyError):
            return expire("frame_apply_failed")


def main(argv: list[str] | None = None) -> int:
    """CLI for keyframe extraction onto an existing video Source."""
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Extract video keyframes")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--media", type=Path, required=True)
    parser.add_argument("--timestamps", required=True, help="comma-separated seconds")
    parser.add_argument("--ffmpeg-path", default="ffmpeg")
    args = parser.parse_args(argv)
    try:
        timestamps = [float(value.strip()) for value in args.timestamps.split(",")]
    except ValueError:
        parser.error("--timestamps must be comma-separated seconds")
    result = VideoFrameService(args.root).extract(
        args.source, args.media, timestamps, executable=args.ffmpeg_path
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("status") == "ok" else 2
