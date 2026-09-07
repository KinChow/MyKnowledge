"""yt-dlp subtitle adapter tests without network or media downloads."""

from pathlib import Path

import pytest

from tools.ingest import source_ingestor, video_subtitles
from tools.ingest.source_ingestor import SourceIngestor


def test_acquire_subtitles_prefers_manual_track(monkeypatch):
    calls = []

    def fake_version(*args, **kwargs):  # noqa: ARG001
        class Result:
            stdout = "2026.08.19\n"

        return Result()

    def fake_download(url, output_dir, *, executable, languages, automatic):
        calls.append(automatic)
        (output_dir / "video.zh-Hans.vtt").write_text(
            "WEBVTT\n\n00:00:01.000 --> 00:00:02.000\n人工字幕\n",
            encoding="utf-8",
        )

    monkeypatch.setattr(video_subtitles.subprocess, "run", fake_version)
    monkeypatch.setattr(video_subtitles, "_run_subtitles", fake_download)
    result = video_subtitles.acquire_subtitles(
        "https://www.bilibili.com/video/BV-test", allow_automatic=True
    )
    assert result.kind == "manual"
    assert result.language == "zh-hans"
    assert calls == [False]
    assert result.extractor == "yt-dlp/2026.08.19"


def test_acquire_subtitles_can_fallback_to_automatic(monkeypatch):
    calls = []

    def fake_version(*args, **kwargs):  # noqa: ARG001
        class Result:
            stdout = "test-version"

        return Result()

    def fake_download(url, output_dir, *, executable, languages, automatic):
        calls.append(automatic)
        if automatic:
            (output_dir / "video.zh-CN.vtt").write_text(
                "WEBVTT\n\n00:00:01.000 --> 00:00:02.000\n自动字幕\n",
                encoding="utf-8",
            )

    monkeypatch.setattr(video_subtitles.subprocess, "run", fake_version)
    monkeypatch.setattr(video_subtitles, "_run_subtitles", fake_download)
    result = video_subtitles.acquire_subtitles(
        "https://www.youtube.com/watch?v=test", allow_automatic=True
    )
    assert result.kind == "automatic"
    assert result.language == "zh-cn"
    assert calls == [False, True]


def test_acquire_subtitles_blocks_when_no_track(monkeypatch):
    class Result:
        stdout = "test-version"

    monkeypatch.setattr(video_subtitles.subprocess, "run", lambda *a, **k: Result())
    monkeypatch.setattr(video_subtitles, "_run_subtitles", lambda *a, **k: None)
    with pytest.raises(RuntimeError, match="video_subtitles_missing"):
        video_subtitles.acquire_subtitles("https://www.youtube.com/watch?v=test")


def test_remote_video_preview_records_subtitle_provenance(monkeypatch, tmp_path: Path):
    class Remote:
        data = b"WEBVTT\n\n00:00:01.000 --> 00:00:02.000\nremote\n"
        kind = "automatic"
        language = "zh"
        format = "vtt"
        extractor = "yt-dlp/test"

    monkeypatch.setattr(source_ingestor, "acquire_subtitles", lambda *a, **k: Remote())
    root = tmp_path / "vault"
    preview = SourceIngestor(root).preview(
        {
            "source_type": "video",
            "domain": "tools",
            "source_id": "remote-video",
            "url": "https://www.youtube.com/watch?v=test",
            "allow_automatic": True,
        }
    )
    assert preview["state"] == "previewed"
    applied = SourceIngestor(root).apply(preview["operation_id"], confirmed=True)
    assert applied["state"] == "applied"
    source = root / "content/sources/tools/remote-video/remote-video.md"
    text = source.read_text(encoding="utf-8")
    assert "automatic" in text
    assert "yt-dlp/test" in text
