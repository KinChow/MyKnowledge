"""Resumable batch runner tests with external media tools mocked."""

import json
from pathlib import Path

from tools.ingest import video_batch
from tools.ingest.video_asr import AsrResult


class FakeIngestor:
    def preview(self, request: dict) -> dict:
        assert request["source_type"] == "video"
        assert request["transcript_provenance"]["kind"] == "asr"
        return {
            "state": "previewed",
            "operation_id": "op_source",
            "snapshot_sha256": "sha256:snapshot",
        }

    def apply(self, operation_id: str, confirmed: bool = False) -> dict:
        assert operation_id == "op_source" and confirmed
        return {"state": "applied", "snapshot_sha256": "sha256:snapshot"}


class FakeFrames:
    def preview(self, source, media, timestamps, *, executable):  # noqa: ARG002
        assert timestamps == [3.0, 10.0, 20.0]
        return {"state": "previewed", "operation_id": "op_frames"}

    def apply(self, operation_id: str, confirmed: bool = False) -> dict:
        assert operation_id == "op_frames" and confirmed
        return {"state": "applied", "frame_count": 3}


def test_batch_runner_is_resumable_and_records_per_item(monkeypatch, tmp_path: Path):
    inventory = tmp_path / "inventory.json"
    inventory.write_text(
        json.dumps(
            {
                "inventory_sha256": "sha256:inventory",
                "items": [
                    {
                        "playlist_index": 1,
                        "selection": "selected",
                        "url": "https://www.bilibili.com/video/BV-test?p=1",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    def fake_asr(media, *, model, executable, language):  # noqa: ARG001
        return AsrResult(
            data=b"1\n00:00:01,000 --> 00:00:02,000\ntext\n",
            provenance={"kind": "asr", "engine": "openai-whisper", "model_name": model},
        )

    monkeypatch.setattr(video_batch, "transcribe_openai_whisper", fake_asr)
    runner = video_batch.VideoBatchRunner(tmp_path / "root", tmp_path / "task")
    runner.ingestor = FakeIngestor()
    runner.frames = FakeFrames()
    runner._download = lambda url, output, mode: output.write_bytes(b"media")  # type: ignore[method-assign]

    first = runner.run(inventory, mode="sample")
    assert first["state"] == "complete"
    assert first["items"]["1"]["state"] == "applied"
    second = runner.run(inventory, mode="sample")
    assert second["state"] == "complete"
    assert second["items"] == first["items"]
    assert (tmp_path / "task" / "video-batch-report.json").exists()
