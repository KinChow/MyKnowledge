"""Keyframe extraction and confirmation for video Sources."""

from __future__ import annotations

import math
import shutil
import subprocess
import time
import uuid
from pathlib import Path

from ..common import atomic_write, canonical_json, read_stable, sha256_bytes
from ..front_matter import FrontMatter
from ..operation_store import OperationStore
from ..paths import RepoPaths


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
    """Preview/apply derived keyframes onto an existing video Source."""

    def __init__(self, root: Path) -> None:
        self.root = Path(root)
        self.paths = RepoPaths(self.root)
        self.store = OperationStore(self.root)

    def preview(
        self,
        source_path: Path,
        media_path: Path,
        timestamps: list[float],
        *,
        executable: str = "ffmpeg",
    ) -> dict:
        try:
            metadata, _body = FrontMatter.parse(source_path.read_text(encoding="utf-8"))
            if metadata.get("source_type") != "video":
                return {"state": "blocked", "error_code": "source_not_video"}
            media_data, stat = read_stable(media_path)
            operation_id = "frame-" + uuid.uuid4().hex
            staging = self.paths.frame_staging(operation_id)
            frames, extractor = extract_keyframes(
                media_path, staging, timestamps, executable=executable
            )
            payload = {
                "operation_type": "video_frames",
                "target_vault": "public",
                "source_path": str(source_path.relative_to(self.root)),
                "source_id": metadata["id"],
                "media_path": str(media_path),
                "media_hash": sha256_bytes(media_data),
                "media_stat": {
                    "dev": stat.st_dev,
                    "ino": stat.st_ino,
                    "size": stat.st_size,
                    "mtime_ns": stat.st_mtime_ns,
                },
                "staging": str(staging.relative_to(self.root)),
                "frames": frames,
                "extractor": extractor,
            }
            record = self.store.new(payload)
            return {
                "state": "previewed",
                "operation_id": record["operation_id"],
                "source_id": metadata["id"],
                "media_hash": payload["media_hash"],
                "frame_count": len(frames),
            }
        except (OSError, RuntimeError, ValueError) as exc:
            return {"state": "blocked", "error_code": str(exc)}

    def apply(self, operation_id: str, confirmed: bool = False) -> dict:
        record, error = self.store.apply_preflight(
            operation_id, "video_frames", confirmed
        )
        if error is not None:
            return error

        def expire(error_code: str) -> dict:
            shutil.rmtree(self.root / record["staging"], ignore_errors=True)
            self.store.update(record, "expired", error_code=error_code)
            return {
                "state": "expired",
                "operation_id": operation_id,
                "error_code": error_code,
            }

        try:
            media = Path(record["media_path"])
            data, stat = read_stable(media)
        except OSError:
            return expire("frame_media_missing")
        if sha256_bytes(data) != record["media_hash"] or (
            stat.st_dev,
            stat.st_ino,
            stat.st_size,
            stat.st_mtime_ns,
        ) != tuple(
            record["media_stat"][key] for key in ("dev", "ino", "size", "mtime_ns")
        ):
            return expire("hash_mismatch")
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
            self.store.update(
                record,
                "applied",
                confirmation={
                    "actor_type": "human",
                    "actor_id": "local-user",
                    "scope": "apply",
                    "confirmed_at": time.time(),
                },
                applied_files=applied_files
                + [str(manifest_path.relative_to(self.root))],
            )
            shutil.rmtree(staging, ignore_errors=True)
            return {
                "state": "applied",
                "operation_id": operation_id,
                "source_id": record["source_id"],
                "frame_count": len(record["frames"]),
            }
        except (OSError, ValueError, KeyError):
            return expire("frame_apply_failed")


def main(argv: list[str] | None = None) -> int:
    """CLI for keyframe preview/apply."""
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Preview/apply video keyframes")
    parser.add_argument("mode", choices=("preview", "apply"))
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--source", type=Path)
    parser.add_argument("--media", type=Path)
    parser.add_argument("--timestamps", help="comma-separated seconds")
    parser.add_argument("--ffmpeg-path", default="ffmpeg")
    parser.add_argument("--operation")
    parser.add_argument("--confirm", action="store_true")
    args = parser.parse_args(argv)
    service = VideoFrameService(args.root)
    if args.mode == "preview":
        if not args.source or not args.media or not args.timestamps:
            parser.error("preview requires --source, --media and --timestamps")
        try:
            timestamps = [float(value.strip()) for value in args.timestamps.split(",")]
        except ValueError:
            parser.error("--timestamps must be comma-separated seconds")
        result = service.preview(
            args.source,
            args.media,
            timestamps,
            executable=args.ffmpeg_path,
        )
    else:
        if not args.operation:
            parser.error("apply requires --operation")
        result = service.apply(args.operation, confirmed=args.confirm)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("state") != "blocked" else 2
