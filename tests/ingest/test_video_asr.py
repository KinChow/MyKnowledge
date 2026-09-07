"""whisper.cpp adapter and video Source ASR integration tests."""

from pathlib import Path

import pytest

from tools.ingest import source_ingestor, video_asr
from tools.ingest.source_ingestor import SourceIngestor


def test_whisper_cpp_adapter_reads_srt_and_records_model_hash(
    monkeypatch, tmp_path: Path
):
    media = tmp_path / "audio.wav"
    model = tmp_path / "ggml-large-v3-turbo.bin"
    media.write_bytes(b"audio fixture")
    model.write_bytes(b"model fixture")

    def fake_run(command, **kwargs):  # noqa: ARG001
        if command[-1] == "--version":

            class Version:
                stdout = "whisper.cpp test\n"
                stderr = ""
                returncode = 0

            return Version()
        output_base = Path(command[command.index("-of") + 1])
        output_base.with_suffix(".srt").write_text(
            "1\n00:00:01,000 --> 00:00:02,000\nASR output\n", encoding="utf-8"
        )

        class Run:
            stdout = ""
            stderr = ""
            returncode = 0

        return Run()

    monkeypatch.setattr(video_asr.subprocess, "run", fake_run)
    result = video_asr.transcribe_whisper_cpp(
        media, model, executable="whisper-cli", language="zh", threads=4
    )
    assert b"ASR output" in result.data
    assert result.provenance["engine"] == "whisper.cpp"
    assert result.provenance["model_name"] == model.name
    assert result.provenance["language"] == "zh"
    assert result.provenance["threads"] == 4
    assert result.provenance["model_sha256"].startswith("sha256:")


def test_openai_whisper_adapter_reads_external_srt(monkeypatch, tmp_path: Path):
    media = tmp_path / "audio.wav"
    media.write_bytes(b"audio fixture")

    def fake_run(command, **kwargs):  # noqa: ARG001
        output_dir = Path(command[command.index("--output_dir") + 1])
        (output_dir / "audio.srt").write_text(
            "1\n00:00:01,000 --> 00:00:02,000\nOpenAI ASR\n", encoding="utf-8"
        )

        class Run:
            stdout = ""
            stderr = ""
            returncode = 0

        return Run()

    monkeypatch.setattr(video_asr.subprocess, "run", fake_run)
    result = video_asr.transcribe_openai_whisper(
        media, executable="whisper", model="turbo"
    )
    assert b"OpenAI ASR" in result.data
    assert result.provenance["engine"] == "openai-whisper"
    assert result.provenance["model_name"] == "turbo"


def test_whisper_cpp_adapter_blocks_missing_inputs(tmp_path: Path):
    media = tmp_path / "audio.wav"
    model = tmp_path / "model.bin"
    with pytest.raises(RuntimeError, match="asr_media_missing"):
        video_asr.transcribe_whisper_cpp(media, model)
    media.write_bytes(b"audio")
    with pytest.raises(RuntimeError, match="asr_model_missing"):
        video_asr.transcribe_whisper_cpp(media, model)


def test_video_source_records_asr_provenance_without_raw_media(
    monkeypatch, tmp_path: Path
):
    media = tmp_path / "lecture.mp4"
    model = tmp_path / "model.bin"
    media.write_bytes(b"media fixture")
    model.write_bytes(b"model fixture")

    def fake_asr(*args, **kwargs):  # noqa: ARG001
        return video_asr.AsrResult(
            data=b"1\n00:00:01,000 --> 00:00:02,000\nASR transcript\n",
            provenance={
                "kind": "asr",
                "engine": "whisper.cpp",
                "engine_version": "test",
                "model_name": "model.bin",
                "model_sha256": "sha256:model",
                "language": "zh",
                "threads": 2,
                "format": "srt",
            },
        )

    monkeypatch.setattr(source_ingestor, "transcribe_whisper_cpp", fake_asr)
    root = tmp_path / "vault"
    preview = SourceIngestor(root).preview(
        {
            "source_type": "video",
            "domain": "computer-science",
            "source_id": "asr-video",
            "url": "https://www.bilibili.com/video/BV-test",
            "input_path": str(media),
            "asr_engine": "whisper.cpp",
            "asr_model_path": str(model),
            "asr_model_sha256": "sha256:model",
            "asr_language": "zh",
            "asr_threads": 2,
        }
    )
    assert preview["state"] == "previewed"
    assert (
        SourceIngestor(root).apply(preview["operation_id"], confirmed=True)["state"]
        == "applied"
    )
    source = root / "content/sources/computer-science/asr-video/asr-video.md"
    text = source.read_text(encoding="utf-8")
    assert "whisper.cpp" in text
    assert "model.bin" in text
    assert "sha256:model" in text
    assert "ASR transcript" in text
    assert "media_input_sha256" in text
    assert "transcript_input_sha256" not in text
    assert not (root / "archive/raw").exists()
