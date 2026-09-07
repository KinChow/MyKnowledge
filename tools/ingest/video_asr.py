"""Whisper-compatible local ASR adapter.

The adapter delegates decoding to the mature whisper.cpp executable and only
normalizes its SRT output. Model weights remain outside the repository; their
path and SHA-256 are recorded in provenance.
"""

from __future__ import annotations

import hashlib
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AsrResult:
    data: bytes
    provenance: dict


def transcribe_openai_whisper(
    media_path: Path,
    *,
    model: str = "turbo",
    executable: str = "whisper",
    language: str = "zh",
) -> AsrResult:
    """Run the mature openai-whisper CLI and return its SRT output."""
    if not media_path.is_file():
        raise RuntimeError("asr_media_missing")
    with tempfile.TemporaryDirectory(prefix="myknowledge-whisper-openai-") as directory:
        command = [
            executable,
            str(media_path),
            "--model",
            model,
            "--language",
            language,
            "--task",
            "transcribe",
            "--output_format",
            "srt",
            "--output_dir",
            directory,
            "--fp16",
            "False",
        ]
        try:
            result = subprocess.run(
                command,
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=3600,
            )
        except FileNotFoundError as exc:
            raise RuntimeError("extractor_unavailable:openai-whisper") from exc
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError("asr_timeout") from exc
        srt_path = Path(directory) / f"{media_path.stem}.srt"
        if result.returncode != 0 or not srt_path.exists():
            raise RuntimeError("asr_failed")
        data = srt_path.read_bytes()
    return AsrResult(
        data=data,
        provenance={
            "kind": "asr",
            "engine": "openai-whisper",
            "engine_version": "external-cli",
            "model_name": model,
            "model_sha256": None,
            "language": language,
            "format": "srt",
        },
    )


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def _version(executable: str) -> str:
    try:
        result = subprocess.run(
            [executable, "--version"],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
        )
    except FileNotFoundError as exc:
        raise RuntimeError("extractor_unavailable:whisper.cpp") from exc
    return result.stdout.strip() or result.stderr.strip() or "unknown"


def transcribe_whisper_cpp(
    media_path: Path,
    model_path: Path,
    *,
    executable: str = "whisper-cli",
    language: str = "auto",
    threads: int | None = None,
) -> AsrResult:
    """Run whisper.cpp and return its generated SRT bytes plus provenance."""
    if not media_path.is_file():
        raise RuntimeError("asr_media_missing")
    if not model_path.is_file():
        raise RuntimeError("asr_model_missing")
    with tempfile.TemporaryDirectory(prefix="myknowledge-whisper-") as directory:
        output_base = Path(directory) / "transcript"
        command = [
            executable,
            "-m",
            str(model_path),
            "-f",
            str(media_path),
            "-osrt",
            "-of",
            str(output_base),
        ]
        if language != "auto":
            command.extend(("-l", language))
        if threads is not None:
            command.extend(("-t", str(threads)))
        try:
            result = subprocess.run(
                command,
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=3600,
            )
        except FileNotFoundError as exc:
            raise RuntimeError("extractor_unavailable:whisper.cpp") from exc
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError("asr_timeout") from exc
        srt_path = output_base.with_suffix(".srt")
        if result.returncode != 0 or not srt_path.exists():
            raise RuntimeError("asr_failed")
        data = srt_path.read_bytes()
    return AsrResult(
        data=data,
        provenance={
            "kind": "asr",
            "engine": "whisper.cpp",
            "engine_version": _version(executable),
            "model_name": model_path.name,
            "model_sha256": _file_sha256(model_path),
            "language": language,
            "threads": threads,
            "format": "srt",
        },
    )
