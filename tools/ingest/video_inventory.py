"""Bilibili/YouTube 视频 metadata inventory（F014）。

该模块只调用成熟的 yt-dlp 获取 metadata，不下载媒体，也不写 canonical Source。
输出的 inventory 可作为后续 Preview/Apply 的 hash-bound 输入。
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import urlparse

from ..common import atomic_write, canonical_json, safe_id, sha256_bytes

INVENTORY_SCHEMA = "video-inventory/v1"
SUPPORTED_HOSTS = {
    "bilibili.com",
    "www.bilibili.com",
    "b23.tv",
    "youtube.com",
    "www.youtube.com",
    "youtu.be",
    "m.youtube.com",
}
LANGUAGE_MARKER = re.compile(r"\[(?P<language>中文|英文|zh|en)\]", re.IGNORECASE)
CJK_RE = re.compile(r"[\u3400-\u9fff]")


def validate_video_url(url: str) -> str:
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower().rstrip(".")
    if parsed.scheme not in {"http", "https"} or not host:
        raise ValueError("video_url_invalid")
    if host not in SUPPORTED_HOSTS and not any(
        host.endswith("." + suffix) for suffix in ("bilibili.com", "youtube.com")
    ):
        raise ValueError("video_host_unsupported")
    return url


def _platform(url: str) -> str:
    host = (urlparse(url).hostname or "").lower()
    return "bilibili" if "bilibili" in host or host == "b23.tv" else "youtube"


def classify_language(title: str) -> str:
    """Prefer explicit platform title markers; otherwise remain conservative."""
    marker = LANGUAGE_MARKER.search(title or "")
    if marker:
        return {"中文": "zh", "zh": "zh", "英文": "en", "en": "en"}[
            marker.group("language").lower()
        ]
    if CJK_RE.search(title or "") and not re.search(
        r"\b(lecture|guest lecture)\b", title, re.I
    ):
        return "zh"
    return "unknown"


def _run_ytdlp(url: str, executable: str = "yt-dlp") -> dict:
    command = [
        executable,
        "--ignore-config",
        "--skip-download",
        "--no-warnings",
        "--dump-single-json",
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
            timeout=180,
        )
    except FileNotFoundError as exc:
        raise RuntimeError("extractor_unavailable:yt-dlp") from exc
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("video_inventory_timeout") from exc
    if result.returncode != 0:
        raise RuntimeError("video_inventory_failed")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError("video_inventory_invalid_json") from exc


def _entry_url(entry: dict, source_url: str, index: int) -> str:
    url = entry.get("webpage_url") or entry.get("original_url")
    if url:
        return str(url)
    platform_id = entry.get("id")
    if platform_id and "bilibili" in source_url:
        return f"https://www.bilibili.com/video/{platform_id}"
    if platform_id:
        return f"https://www.youtube.com/watch?v={platform_id}"
    return f"{source_url}#item={index}"


def _normalise_entry(entry: dict, source_url: str, index: int) -> dict:
    title = str(entry.get("title") or "")
    platform_id = str(entry.get("id") or "")
    stable_id = re.sub(r"[^a-z0-9]+", "-", platform_id.lower()).strip("-") or "item"
    p = entry.get("playlist_index") or index
    try:
        p = int(p)
    except (TypeError, ValueError):
        p = index
    return {
        "item_id": safe_id(f"video-{stable_id}-p{p}"),
        "platform_id": platform_id or None,
        "playlist_index": p,
        "title": title or None,
        "language": classify_language(title),
        "url": _entry_url(entry, source_url, p),
        "duration_seconds": entry.get("duration"),
        "upload_date": entry.get("upload_date"),
        "uploader": entry.get("uploader"),
    }


def build_inventory(
    url: str, *, language: str | None = None, executable: str = "yt-dlp"
) -> dict:
    source_url = validate_video_url(url)
    metadata = _run_ytdlp(source_url, executable)
    raw_entries = (
        metadata.get("entries") if metadata.get("_type") == "playlist" else None
    )
    entries = [item for item in (raw_entries or [metadata]) if isinstance(item, dict)]
    items = [
        _normalise_entry(item, source_url, index)
        for index, item in enumerate(entries, 1)
    ]
    selected = [item for item in items if not language or item["language"] == language]
    selected_ids = {item["item_id"] for item in selected}
    for item in items:
        item["selection"] = (
            "selected" if item["item_id"] in selected_ids else "excluded"
        )
        if item["selection"] == "excluded":
            item["excluded_reason"] = (
                f"language_not_selected:{language}" if language else "not_selected"
            )
    payload = {
        "schema_version": INVENTORY_SCHEMA,
        "source_url": source_url,
        "platform": _platform(source_url),
        "source_id": metadata.get("id"),
        "title": metadata.get("title"),
        "captured_at": metadata.get("timestamp"),
        "inventory_item_count": len(items),
        "selected_item_count": len(selected),
        "selection_language": language,
        "items": items,
    }
    payload["inventory_sha256"] = sha256_bytes(canonical_json(payload))
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Inventory Bilibili/YouTube video metadata"
    )
    parser.add_argument("url")
    parser.add_argument("--language", choices=["zh", "en"])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--ytdlp-path", default="yt-dlp")
    args = parser.parse_args(argv)
    try:
        result = build_inventory(
            args.url, language=args.language, executable=args.ytdlp_path
        )
    except (RuntimeError, ValueError) as exc:
        print(
            json.dumps({"state": "blocked", "error_code": str(exc)}, ensure_ascii=False)
        )
        return 2
    data = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        atomic_write(args.output, data.encode("utf-8"))
    print(data, end="")
    return 0
