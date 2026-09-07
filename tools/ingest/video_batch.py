"""Resumable per-item video archive orchestration.

The runner composes mature yt-dlp, ffmpeg and ASR CLIs. It owns only task
state and retry boundaries; canonical Source writes still go through the
existing Preview/Apply services.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import uuid
from pathlib import Path

from ..common import atomic_write, canonical_json
from .source_ingestor import SourceIngestor
from .video_asr import transcribe_openai_whisper, transcribe_whisper_cpp
from .video_frames import VideoFrameService


class VideoBatchRunner:
    def __init__(
        self,
        root: Path,
        task_dir: Path,
        *,
        ytdlp_path: str = "yt-dlp",
        asr_path: str = "whisper",
        ffmpeg_path: str = "ffmpeg",
        asr_model_sha256: str | None = None,
        asr_engine: str = "openai-whisper",
        asr_model_path: str | None = None,
    ) -> None:
        self.root = Path(root)
        self.task_dir = Path(task_dir)
        self.ytdlp_path = ytdlp_path
        self.asr_path = asr_path
        self.ffmpeg_path = ffmpeg_path
        self.asr_model_sha256 = asr_model_sha256
        self.asr_engine = asr_engine
        self.asr_model_path = asr_model_path
        self.ingestor = SourceIngestor(self.root)
        self.frames = VideoFrameService(self.root)
        self.report_path = self.task_dir / "video-batch-report.json"

    def run(
        self,
        inventory_path: Path,
        *,
        mode: str = "sample",
        limit: int | None = None,
        retry_failed: bool = False,
    ) -> dict:
        if mode not in {"sample", "full"}:
            raise ValueError("video_batch_mode_invalid")
        inventory = json.loads(Path(inventory_path).read_text(encoding="utf-8"))
        selected = [
            item
            for item in inventory.get("items", [])
            if item.get("selection") == "selected"
        ]
        if limit is not None:
            selected = selected[:limit]
        report = self._load_report(inventory, mode)
        for item in selected:
            key = str(item["playlist_index"])
            previous = report["items"].get(key) or {}
            if previous.get("state") == "applied":
                continue
            if previous.get("state") == "blocked" and not retry_failed:
                continue
            try:
                result = self._process_item(item, mode)
                report["items"][key] = {"state": "applied", **result}
            except (
                OSError,
                RuntimeError,
                ValueError,
                subprocess.SubprocessError,
            ) as exc:
                report["items"][key] = {
                    "state": "blocked",
                    "error_code": str(exc),
                    "next_action": "retry this playlist item after fixing the recorded dependency",
                }
            self._refresh_counts(report, len(selected))
            self._save_report(report)
        self._refresh_counts(report, len(selected))
        self._save_report(report)
        return report

    @staticmethod
    def _refresh_counts(report: dict, selected_count: int) -> None:
        report["selected_count"] = selected_count
        report["applied_count"] = sum(
            item.get("state") == "applied" for item in report["items"].values()
        )
        report["blocked_count"] = sum(
            item.get("state") == "blocked" for item in report["items"].values()
        )
        report["state"] = (
            "complete" if report["applied_count"] == selected_count else "partial"
        )

    def _process_item(self, item: dict, mode: str) -> dict:
        position = int(item["playlist_index"])
        stem = f"cs336-p{position:02d}"
        media_dir = self.task_dir / "media"
        transcript_dir = self.task_dir / "transcript" / stem
        media_dir.mkdir(parents=True, exist_ok=True)
        transcript_dir.mkdir(parents=True, exist_ok=True)
        media = media_dir / f"{stem}.{'mp4' if mode == 'sample' else 'wav'}"
        self._download(item["url"], media, mode)
        if self.asr_engine == "whisper.cpp":
            if not self.asr_model_path:
                raise ValueError("asr_model_path_required")
            asr = transcribe_whisper_cpp(
                media,
                Path(self.asr_model_path),
                executable=self.asr_path,
                language="zh",
                threads=8,
            )
        else:
            asr = transcribe_openai_whisper(
                media,
                model="turbo",
                executable=self.asr_path,
                language="zh",
            )
        if self.asr_model_sha256:
            asr.provenance["model_sha256"] = self.asr_model_sha256
        transcript = transcript_dir / f"{stem}.srt"
        atomic_write(transcript, asr.data)
        source_id = f"cs336-p{position:02d}"
        preview = self.ingestor.preview(
            {
                "source_type": "video",
                "domain": "computer-science",
                "source_id": source_id,
                "url": item["url"],
                "input_path": str(transcript),
                "archive_policy": "transcript-only",
                "transcript_provenance": asr.provenance,
            }
        )
        if preview.get("state") != "previewed":
            raise RuntimeError(str(preview.get("errors") or preview))
        applied = self.ingestor.apply(preview["operation_id"], confirmed=True)
        if applied.get("state") != "applied":
            raise RuntimeError(str(applied))
        frame_count = 0
        if mode == "sample":
            source_path = (
                self.root
                / "content"
                / "sources"
                / "computer-science"
                / source_id
                / f"{source_id}.md"
            )
            frame_preview = self.frames.preview(
                source_path, media, [3.0, 10.0, 20.0], executable=self.ffmpeg_path
            )
            if frame_preview.get("state") != "previewed":
                raise RuntimeError(str(frame_preview))
            frame_applied = self.frames.apply(
                frame_preview["operation_id"], confirmed=True
            )
            if frame_applied.get("state") != "applied":
                raise RuntimeError(str(frame_applied))
            frame_count = frame_applied["frame_count"]
        return {
            "source_id": source_id,
            "snapshot_sha256": applied["snapshot_sha256"],
            "media_path": str(media.relative_to(self.task_dir)),
            "transcript_path": str(transcript.relative_to(self.task_dir)),
            "frame_count": frame_count,
            "extractor": asr.provenance,
        }

    def _download(self, url: str, output: Path, mode: str) -> None:
        if output.is_file() and output.stat().st_size > 0:
            return
        command = [
            self.ytdlp_path,
            "--ignore-config",
            "--no-warnings",
            "--no-playlist",
        ]
        if mode == "sample":
            command.extend(
                [
                    "-f",
                    "bv*+ba/b",
                    "--merge-output-format",
                    "mp4",
                ]
            )
            command.extend(
                [
                    "--download-sections",
                    "*00:00-00:30",
                    "--force-keyframes-at-cuts",
                ]
            )
        else:
            command.extend(["-f", "ba/b", "--extract-audio", "--audio-format", "wav"])
        command.extend(["-o", str(output)])
        command.append(url)
        result = subprocess.run(
            command, check=False, capture_output=True, text=True, timeout=3600
        )
        if result.returncode != 0 or not output.is_file():
            raise RuntimeError("video_download_failed")

    def _load_report(self, inventory: dict, mode: str) -> dict:
        if self.report_path.exists():
            current = json.loads(self.report_path.read_text(encoding="utf-8"))
            if (
                current.get("inventory_sha256") == inventory.get("inventory_sha256")
                and current.get("mode") == mode
            ):
                return current
        return {
            "schema_version": "video-batch-report/v1",
            "run_id": "run_" + uuid.uuid4().hex,
            "inventory_sha256": inventory.get("inventory_sha256"),
            "mode": mode,
            "items": {},
        }

    def _save_report(self, report: dict) -> None:
        self.task_dir.mkdir(parents=True, exist_ok=True)
        atomic_write(self.report_path, canonical_json(report) + b"\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run resumable video Source batch archive"
    )
    parser.add_argument("inventory", type=Path)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--task-dir", type=Path, required=True)
    parser.add_argument("--mode", choices=("sample", "full"), default="sample")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--retry-failed", action="store_true")
    parser.add_argument("--ytdlp-path", default="yt-dlp")
    parser.add_argument("--asr-path", default="whisper")
    parser.add_argument("--asr-model-sha256")
    parser.add_argument(
        "--asr-engine",
        choices=("openai-whisper", "whisper.cpp"),
        default="openai-whisper",
    )
    parser.add_argument("--asr-model-path")
    parser.add_argument("--ffmpeg-path", default="ffmpeg")
    args = parser.parse_args(argv)
    result = VideoBatchRunner(
        args.root,
        args.task_dir,
        ytdlp_path=args.ytdlp_path,
        asr_path=args.asr_path,
        ffmpeg_path=args.ffmpeg_path,
        asr_model_sha256=args.asr_model_sha256,
        asr_engine=args.asr_engine,
        asr_model_path=args.asr_model_path,
    ).run(
        args.inventory, mode=args.mode, limit=args.limit, retry_failed=args.retry_failed
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("state") != "partial" else 2
