"""Keyframe extraction and Source attachment tests."""

from pathlib import Path

from tools.front_matter import FrontMatter
from tools.ingest.source_ingestor import SourceIngestor
from tools.ingest.video_frames import VideoFrameService, extract_keyframes


def test_extract_keyframes_deduplicates_timestamps_and_hashes_png(
    monkeypatch, tmp_path: Path
):
    media = tmp_path / "video.mp4"
    media.write_bytes(b"media")
    output = tmp_path / "frames"

    def fake_run(command, **kwargs):  # noqa: ARG001
        if command[1] == "-version":

            class Version:
                stdout = "ffmpeg version test\n"
                stderr = ""
                returncode = 0

            return Version()
        Path(command[-1]).write_bytes(b"PNG fixture")

        class Run:
            stdout = ""
            stderr = ""
            returncode = 0

        return Run()

    monkeypatch.setattr("tools.ingest.video_frames.subprocess.run", fake_run)
    frames, extractor = extract_keyframes(
        media, output, [2.0, 1.0, 2.0], executable="ffmpeg"
    )
    assert [frame["timestamp_seconds"] for frame in frames] == [1.0, 2.0]
    assert all(frame["sha256"].startswith("sha256:") for frame in frames)
    assert extractor["extractor"] == "ffmpeg"
    assert extractor["options"]["timestamps_seconds"] == [1.0, 2.0]


def test_video_frame_apply_attaches_confirmed_pngs_and_manifest(
    monkeypatch, tmp_path: Path
):
    transcript = tmp_path / "lecture.vtt"
    transcript.write_text(
        "WEBVTT\n\n00:00:01.000 --> 00:00:02.000\ntranscript\n",
        encoding="utf-8",
    )
    media = tmp_path / "lecture.mp4"
    media.write_bytes(b"media fixture")
    root = tmp_path / "vault"
    source_service = SourceIngestor(root)
    ingested = source_service.ingest(
        {
            "source_type": "video",
            "domain": "tools",
            "source_id": "frame-video",
            "url": "https://www.youtube.com/watch?v=test",
            "input_path": str(transcript),
        }
    )
    assert ingested["state"] == "applied", ingested
    source = root / "content/sources/tools/frame-video/frame-video.md"

    def fake_run(command, **kwargs):  # noqa: ARG001
        if command[1] == "-version":

            class Version:
                stdout = "ffmpeg version test\n"
                stderr = ""
                returncode = 0

            return Version()
        Path(command[-1]).write_bytes(b"PNG frame")

        class Run:
            stdout = ""
            stderr = ""
            returncode = 0

        return Run()

    monkeypatch.setattr("tools.ingest.video_frames.subprocess.run", fake_run)
    frames = VideoFrameService(root)
    applied = frames.extract(source, media, [1.5], executable="ffmpeg")
    assert applied["state"] == "applied", applied

    frame_dir = source.parent / "media" / "frames"
    assert len(list(frame_dir.glob("frame-*.png"))) == 1
    assert (frame_dir / "manifest.json").exists()
    metadata, body = FrontMatter.parse(source.read_text(encoding="utf-8"))
    assert metadata["frame_manifest"]["path"].endswith("media/frames/manifest.json")
    assert any(item["kind"] == "frame" for item in metadata["attachments"])
    assert "transcript" in body
