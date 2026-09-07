"""Video transcript normalization and Source integration tests."""

from pathlib import Path

from tools.archive_manifest import ArchiveManifest
from tools.common import sha256_text
from tools.front_matter import FrontMatter
from tools.ingest.source_ingestor import SourceIngestor
from tools.ingest.source_validator import SourceValidator
from tools.ingest.video_transcript import normalize_file, parse_subtitles

VTT = """WEBVTT\n\n00:01.250 --> 00:03.500\n你好 <i>世界</i>\n\n00:04,000 --> 00:05,000\nGPU kernel\n"""


def test_vtt_and_srt_are_normalized_to_stable_timestamped_markdown(tmp_path: Path):
    vtt = tmp_path / "sample.vtt"
    vtt.write_text(VTT, encoding="utf-8")
    body, metadata = normalize_file(vtt)
    assert "### [00:00:01.250 - 00:00:03.500]" in body
    assert "你好 世界" in body
    assert metadata["cue_count"] == 2
    assert metadata["extractor"] == "video-transcript/1"

    srt = tmp_path / "sample.srt"
    srt.write_text("1\n00:00:01,000 --> 00:00:02,000\n字幕\n", encoding="utf-8")
    assert parse_subtitles(srt.read_bytes(), ".srt")[0].start == "00:00:01.000"


def test_malformed_or_unsupported_transcript_is_rejected(tmp_path: Path):
    with_exception = tmp_path / "bad.srt"
    with_exception.write_text(
        "1\n00:00:03,000 --> 00:00:02,000\n坏\n", encoding="utf-8"
    )
    try:
        parse_subtitles(with_exception.read_bytes(), ".srt")
    except ValueError as exc:
        assert str(exc) == "transcript_timing_reversed"
    else:
        raise AssertionError("reversed timing was accepted")

    txt = tmp_path / "sample.txt"
    txt.write_text("not subtitles", encoding="utf-8")
    try:
        normalize_file(txt)
    except ValueError as exc:
        assert str(exc) == "transcript_format_unsupported"
    else:
        raise AssertionError("unsupported format was accepted")


def test_video_preview_apply_writes_transcript_only_source_and_manifest(tmp_path: Path):
    transcript = tmp_path / "lecture.vtt"
    transcript.write_text(VTT, encoding="utf-8")
    root = tmp_path / "vault"
    ingestor = SourceIngestor(root)
    preview = ingestor.preview(
        {
            "source_type": "video",
            "domain": "computer-science",
            "source_id": "cs336-p01",
            "url": "https://www.bilibili.com/video/BV1j9Kc6mEq4?p=1",
            "input_path": str(transcript),
            "archive_policy": "transcript-only",
        }
    )
    assert preview["state"] == "previewed"
    applied = ingestor.apply(preview["operation_id"], confirmed=True)
    assert applied["state"] == "applied"

    source_path = (
        root / "content" / "sources" / "computer-science" / "cs336-p01" / "cs336-p01.md"
    )
    metadata, body = FrontMatter.parse(source_path.read_text(encoding="utf-8"))
    assert metadata["source_type"] == "video"
    assert metadata["archive_policy"] == "transcript-only"
    assert metadata["retrieval"]["acquisition"] == "video"
    assert metadata["video"]["url"].endswith("?p=1")
    assert "input_path" not in metadata["retrieval"]
    assert str(transcript) not in source_path.read_text(encoding="utf-8")
    assert metadata["snapshot_sha256"] == sha256_text(body)
    assert not (root / "archive" / "raw").exists()
    entries = list(ArchiveManifest(root).entries())
    assert len(entries) == 1
    assert entries[0]["extractor"] == "video-transcript/1"

    assert SourceValidator().validate_source_file(source_path) == []


def test_video_request_rejects_non_platform_url(tmp_path: Path):
    transcript = tmp_path / "lecture.vtt"
    transcript.write_text(VTT, encoding="utf-8")
    result = SourceIngestor(tmp_path / "vault").preview(
        {
            "source_type": "video",
            "domain": "tools",
            "source_id": "bad-video",
            "url": "https://example.com/video",
            "input_path": str(transcript),
        }
    )
    assert result["state"] == "blocked"
    assert {error["path"] for error in result["errors"]} == {"url"}


def test_video_apply_expires_when_transcript_changes(tmp_path: Path):
    transcript = tmp_path / "lecture.vtt"
    transcript.write_text(VTT, encoding="utf-8")
    root = tmp_path / "vault"
    ingestor = SourceIngestor(root)
    preview = ingestor.preview(
        {
            "source_type": "video",
            "domain": "computer-science",
            "source_id": "cs336-p02",
            "url": "https://www.youtube.com/watch?v=loZ4xQ5RZuU",
            "input_path": str(transcript),
        }
    )
    transcript.write_text(VTT.replace("GPU kernel", "changed"), encoding="utf-8")
    applied = ingestor.apply(preview["operation_id"], confirmed=True)
    assert applied == {
        "state": "expired",
        "operation_id": preview["operation_id"],
        "error_code": "hash_mismatch",
    }
