import json
from pathlib import Path

import pytest

from tools.ingest import video_inventory


def _metadata() -> dict:
    return {
        "_type": "playlist",
        "id": "BV-test",
        "title": "CS336",
        "entries": [
            {
                "id": "BV-test_p1",
                "title": "CS336 p01 [中文] 从零构建大语言模型",
                "playlist_index": 1,
                "webpage_url": "https://www.bilibili.com/video/BV-test?p=1",
                "duration": 60,
            },
            {
                "id": "BV-test_p2",
                "title": "CS336 p02 [英文] Lecture 1",
                "playlist_index": 2,
                "webpage_url": "https://www.bilibili.com/video/BV-test?p=2",
            },
        ],
    }


def test_classify_language_prefers_explicit_title_marker():
    assert video_inventory.classify_language("p01 [中文] Lecture") == "zh"
    assert video_inventory.classify_language("p02 [英文] Lecture") == "en"
    assert video_inventory.classify_language("Lecture 1: Overview") == "unknown"


def test_build_inventory_selects_language_without_download(monkeypatch):
    calls = []

    def fake_run(url: str, executable: str = "yt-dlp"):
        calls.append((url, executable))
        return _metadata()

    monkeypatch.setattr(video_inventory, "_run_ytdlp", fake_run)
    result = video_inventory.build_inventory(
        "https://www.bilibili.com/video/BV-test/",
        language="zh",
        executable="fake-yt-dlp",
    )

    assert len(calls) == 1
    assert calls[0][1] == "fake-yt-dlp"
    assert result["inventory_item_count"] == 2
    assert result["selected_item_count"] == 1
    assert result["items"][0]["selection"] == "selected"
    assert result["items"][1]["excluded_reason"] == "language_not_selected:zh"
    assert result["inventory_sha256"].startswith("sha256:")


def test_inventory_rejects_unsupported_host():
    with pytest.raises(ValueError, match="video_host_unsupported"):
        video_inventory.build_inventory("https://example.com/video")


def test_cli_writes_inventory_to_explicit_output(monkeypatch, tmp_path: Path, capsys):
    monkeypatch.setattr(video_inventory, "_run_ytdlp", lambda *_args: _metadata())
    output = tmp_path / "inventory.json"
    assert (
        video_inventory.main(
            [
                "https://www.bilibili.com/video/BV-test/",
                "--language",
                "zh",
                "--output",
                str(output),
            ]
        )
        == 0
    )
    captured = json.loads(capsys.readouterr().out)
    persisted = json.loads(output.read_text(encoding="utf-8"))
    assert captured["inventory_sha256"] == persisted["inventory_sha256"]
