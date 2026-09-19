"""video ingest 模块公共返回归一到 tools.contract 的契约测试。"""

from __future__ import annotations

from pathlib import Path

from tools import contract
from tools.ingest import video_inventory
from tools.ingest.video_frames import VideoFrameService


def _metadata() -> dict:
    return {
        "_type": "playlist",
        "id": "BV-test",
        "title": "CS336",
        "entries": [
            {
                "id": "BV-test_p1",
                "title": "p01 [中文] Lecture",
                "playlist_index": 1,
                "webpage_url": "https://www.bilibili.com/video/BV-test?p=1",
            }
        ],
    }


def test_build_inventory_is_ok_envelope(monkeypatch):
    monkeypatch.setattr(video_inventory, "_run_ytdlp", lambda *a, **k: _metadata())
    result = video_inventory.build_inventory(
        "https://www.bilibili.com/video/BV-test/", language="zh"
    )
    assert result["status"] == "ok"
    assert result["schema_version"] == "video-inventory/v1"
    # 领域字段加法保留 + 自哈希覆盖信封仍自洽。
    assert result["inventory_item_count"] == 1
    assert result["inventory_sha256"].startswith("sha256:")


def test_frame_extract_on_non_video_source_is_blocked_envelope(tmp_path: Path):
    source = tmp_path / "doc.md"
    source.write_text("---\nid: doc-1\nsource_type: doc\n---\n正文\n", encoding="utf-8")
    result = VideoFrameService(tmp_path).extract(source, tmp_path / "media.mp4", [1.0])
    assert result["status"] == "blocked"
    assert result["schema_version"] == "video-frames/v1"
    assert result["error_code"] == "source_not_video"
    assert result["error_code"] in contract.ERROR_CODES
