"""Mature-platform subtitle acquisition through yt-dlp.

Only subtitle files are requested. The media stream is never downloaded and
the returned bytes stay in the preview operation until canonicalized.
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

from .video_inventory import validate_video_url


@dataclass(frozen=True)
class SubtitleResult:
    data: bytes
    language: str
    kind: str
    format: str
    extractor: str


def _run_subtitles(
    url: str,
    output_dir: Path,
    *,
    executable: str,
    languages: str,
    automatic: bool,
) -> None:
    command = [
        executable,
        "--ignore-config",
        "--no-warnings",
        "--no-playlist",
        "--skip-download",
        "--write-auto-subs" if automatic else "--write-subs",
        "--sub-langs",
        languages,
        "--sub-format",
        "vtt",
        "--output",
        str(output_dir / "%(id)s.%(ext)s"),
        url,
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
        raise RuntimeError("extractor_unavailable:yt-dlp") from exc
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("video_subtitles_timeout") from exc
    if result.returncode != 0 and not list(output_dir.glob("*.vtt")):
        raise RuntimeError("video_subtitles_failed")


def _select_file(output_dir: Path, languages: str) -> tuple[Path, str] | None:
    candidates = sorted(output_dir.glob("*.vtt"))
    if not candidates:
        return None
    preferred = [item.strip().lower() for item in languages.split(",") if item.strip()]
    for language in preferred:
        for candidate in candidates:
            if f".{language}." in candidate.name.lower():
                return candidate, language
    candidate = candidates[0]
    parts = candidate.name.rsplit(".", 2)
    return candidate, parts[-2] if len(parts) == 3 else "unknown"


def acquire_subtitles(
    url: str,
    *,
    languages: str = "zh-Hans,zh-CN,zh,cmn,en",
    allow_automatic: bool = False,
    executable: str = "yt-dlp",
) -> SubtitleResult:
    """Fetch one VTT subtitle track, preferring human subtitles."""
    validate_video_url(url)
    try:
        version = (
            subprocess.run(
                [executable, "--version"],
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=30,
            ).stdout.strip()
            or "unknown"
        )
    except FileNotFoundError as exc:
        raise RuntimeError("extractor_unavailable:yt-dlp") from exc
    with tempfile.TemporaryDirectory(prefix="myknowledge-video-subs-") as directory:
        output_dir = Path(directory)
        _run_subtitles(
            url,
            output_dir,
            executable=executable,
            languages=languages,
            automatic=False,
        )
        selected = _select_file(output_dir, languages)
        kind = "manual"
        if selected is None and allow_automatic:
            _run_subtitles(
                url,
                output_dir,
                executable=executable,
                languages=languages,
                automatic=True,
            )
            selected = _select_file(output_dir, languages)
            kind = "automatic"
        if selected is None:
            raise RuntimeError("video_subtitles_missing")
        path, language = selected
        data = path.read_bytes()
    return SubtitleResult(
        data=data,
        language=language,
        kind=kind,
        format="vtt",
        extractor=f"yt-dlp/{version}",
    )


def executable_available(executable: str = "yt-dlp") -> bool:
    """Small diagnostic helper used by callers before offering remote mode."""
    return shutil.which(executable) is not None
