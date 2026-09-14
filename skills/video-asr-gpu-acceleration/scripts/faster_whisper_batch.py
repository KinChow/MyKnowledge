#!/usr/bin/env python3
"""Run one reproducible faster-whisper batch worker."""

from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path


def timestamp(seconds: float) -> str:
    milliseconds = max(0, int(round(seconds * 1000)))
    hours, milliseconds = divmod(milliseconds, 3_600_000)
    minutes, milliseconds = divmod(milliseconds, 60_000)
    whole_seconds, milliseconds = divmod(milliseconds, 1_000)
    return f"{hours:02d}:{minutes:02d}:{whole_seconds:02d},{milliseconds:03d}"


def atomic_write(path: Path, content: str) -> None:
    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    temporary.write_text(content, encoding="utf-8")
    temporary.replace(path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--model", default="large-v3-turbo")
    parser.add_argument("--model-cache-dir", type=Path, required=True)
    parser.add_argument("--language", default="zh")
    parser.add_argument("--beam-size", type=int, default=5)
    parser.add_argument("--compute-type", default="float16")
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--worker-index", type=int, required=True)
    parser.add_argument("--worker-count", type=int, required=True)
    parser.add_argument("--glob", default="*.m4a")
    parser.add_argument("--vad-filter", action="store_true")
    parser.add_argument("--retry-complete", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    from faster_whisper import WhisperModel

    if not 0 <= args.worker_index < args.worker_count:
        raise SystemExit("worker-index must be in [0, worker-count)")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    files = sorted(args.input_dir.glob(args.glob))[
        args.worker_index :: args.worker_count
    ]
    print(f"worker_index={args.worker_index} files={len(files)}", flush=True)
    load_started = time.perf_counter()
    model = WhisperModel(
        args.model,
        device=args.device,
        compute_type=args.compute_type,
        download_root=str(args.model_cache_dir),
    )
    print(f"model_load_s={time.perf_counter() - load_started:.3f}", flush=True)

    for audio_path in files:
        stem = audio_path.stem
        json_path = args.output_dir / f"{stem}.json"
        output_paths = (
            json_path,
            args.output_dir / f"{stem}.txt",
            args.output_dir / f"{stem}.srt",
        )
        if (
            all(path.exists() and path.stat().st_size > 0 for path in output_paths)
            and not args.retry_complete
        ):
            print(f"skip={audio_path.name}", flush=True)
            continue

        started = time.perf_counter()
        segments, info = model.transcribe(
            str(audio_path),
            language=args.language,
            beam_size=args.beam_size,
            vad_filter=args.vad_filter,
        )
        rows = [
            {"start": item.start, "end": item.end, "text": item.text}
            for item in segments
        ]
        decode_seconds = time.perf_counter() - started
        payload = {
            "audio": audio_path.name,
            "duration_s": info.duration,
            "decode_s": decode_seconds,
            "language": info.language,
            "model": args.model,
            "compute_type": args.compute_type,
            "beam_size": args.beam_size,
            "vad_filter": args.vad_filter,
            "segments": rows,
        }
        atomic_write(json_path, json.dumps(payload, ensure_ascii=False, indent=2))
        atomic_write(
            args.output_dir / f"{stem}.txt",
            "".join(item["text"] for item in rows),
        )
        srt = "".join(
            f"{index}\n{timestamp(item['start'])} --> {timestamp(item['end'])}\n"
            f"{item['text'].strip()}\n\n"
            for index, item in enumerate(rows, 1)
        )
        atomic_write(args.output_dir / f"{stem}.srt", srt)
        print(
            f"done={audio_path.name} decode_s={decode_seconds:.3f} "
            f"segments={len(rows)} duration_s={info.duration:.3f}",
            flush=True,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
