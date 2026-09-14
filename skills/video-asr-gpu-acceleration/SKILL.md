---
name: video-asr-gpu-acceleration
description: Download or process video-to-text jobs with faster-whisper on a remote NVIDIA GPU, including Bilibili inventory, local-download fallback, BOS transfer, isolated Docker workers, CUDA compatibility, and MyKnowledge Source archival.
---

# Video ASR GPU Acceleration

Use this skill when local video transcription is too slow, or when a video or
playlist must be transcribed and archived as MyKnowledge Sources. The primary
path is `faster-whisper` with CTranslate2 inside a new Docker container.
vLLM/SGLang images provide the CUDA/PyTorch environment; they are not used as
the ASR serving layer.

For the formal archive workflow, use this order:

```text
metadata inventory -> download audio -> checksum -> BOS -> A100 ASR
-> result validation -> Source Preview/Apply -> index rebuild
```

## Boundaries

- Keep the experiment isolated from the repository and existing containers.
  Use `/tmp` and/or a newly named container; do not stop, restart, remove, or
  mutate unrelated containers.
- Use the `dev-machine-access` skill for SSH and relay access. Reuse the
  successful ledger path and an active relay session when available. Never put
  passwords, tokens, or private endpoints in commands saved to the repository.
- Use `bos-airgap-transfer` and `bos-toolkit` for BOS relay work. Validate both
  sides with object counts, byte totals, and SHA-256; do not use lrzsz/trzsz for
  a multi-gigabyte or auditable transfer.
- Use the same audio, language, model, and decoding settings when comparing
  CPU and GPU. Report model-load time separately from steady-state decode time.
- A latency result from one clip is not an ASR quality ranking. Do not claim
  CER/WER or model superiority without a corrected reference set.
- This skill does not require `perf-analysis`; record direct ASR timings and
  outputs instead.
- Do not write media originals into the repository by default. Use
  `transcript-only` Sources and retain large audio outside Git or in the BOS
  task prefix.

## Workflow

### 1. Establish the baseline

Locate the existing local ASR workflow and record:

- input audio path, duration, sample rate/channels, and SHA-256;
- model, language, decoding parameters, device, precision, and wall time;
- whether the time includes model load, audio decoding, VAD, alignment, or
  post-processing.

Prefer a bounded representative clip for the first test. Do not modify the
repository to create the fixture. Keep generated results under `/tmp` or an
explicit mounted temporary directory.

### 2. Inventory the source before downloading

For Bilibili or YouTube, run a metadata-only inventory first. A playlist URL
may contain unrelated entries, multiple recordings, or short test clips. Record
the source URL, item count, per-item platform URL, title, duration, language,
and explicit selection. Do not download or transcribe during inventory.

If the remote GPU host cannot reach the platform, do the inventory and audio
download on the local PC. This is the preferred fallback after a bounded
remote request timeout; do not keep retrying a blocked remote platform
request indefinitely. Install `yt-dlp` in a temporary environment and keep
download artifacts outside the repository:

```bash
python3 -m venv /tmp/video-asr-<task>-venv
/tmp/video-asr-<task>-venv/bin/pip install yt-dlp
/tmp/video-asr-<task>-venv/bin/yt-dlp --flat-playlist --dump-single-json \
  --skip-download '<playlist-or-video-url>' > /tmp/video-asr-<task>/inventory.json
```

For a selected playlist, download audio only and keep one file per item. Use
`--continue`, `--no-overwrites`, bounded socket/retry values, and a log. A
successful exit must be followed by a file-count, media-duration, and
no-`.part` check.

```bash
yt-dlp --no-playlist \
  --format 'bestaudio[ext=m4a]/bestaudio/best' \
  --output '/tmp/video-asr-<task>/audio/p%(playlist_index)02d-%(id)s.%(ext)s' \
  --write-info-json --write-description --continue --no-overwrites \
  --socket-timeout 15 --retries 3 --fragment-retries 3 --newline \
  'https://www.bilibili.com/video/<BV>?p=<N>'
```

### 3. Reach the GPU host and inspect it

For a remote NVIDIA host, first query the local access ledger, then use the
validated relay chain. Example for the A100 host used during validation:

```bash
python3 /Users/zhouzijian01/.codex/skills/dev-machine-access/scripts/dev_machine_ledger.py path --host 10.55.87.81
ssh relay
ssh root@10.55.87.81
```

Inside the host, inspect identity, GPU availability, active GPU processes,
Docker containers/images, disk space, and the target input/model locations:

```bash
hostname
nvidia-smi --query-gpu=name,driver_version,memory.total,memory.free --format=csv,noheader
nvidia-smi --query-compute-apps=gpu_uuid,pid,process_name,used_gpu_memory --format=csv,noheader
docker ps --format '{{.Names}}\t{{.Image}}\t{{.Status}}'
docker images --format '{{.Repository}}:{{.Tag}}\t{{.Size}}'
df -h /ssd1 /ssd2 /ssd3 /ssd4 /tmp
```

Prefer an image already present on the host. The validated examples are:

```text
iregistry.baidu-int.com/zhouzijian01/sglang:qwen38flashnext
iregistry.baidu-int.com/hub-official/vllm-openai:v0.26.0
```

### 4. Transfer and create isolated containers

Create a unique task directory on `/ssd2` on the GPU host, for example
`/ssd2/video-asr-<task>`. Upload the local audio directory and inventory to a
unique BOS prefix, then download it on the GPU host. Keep the input and output
prefixes separate. Use `bos sync` for directories and upload a sorted checksum
manifest beside them:

```bash
# local PC
(cd /tmp/video-asr-<task>/audio && find . -type f -print0 | sort -z \
  | xargs -0 shasum -a 256) > /tmp/video-asr-<task>/audio.files.sha256
bcecmd bos sync /tmp/video-asr-<task>/audio/ \
  bos:/aihc-private-hcd/zhouzijian01/attn-moe-test/video-asr-<task>/input/audio/ \
  --concurrency 8
bcecmd bos cp /tmp/video-asr-<task>/audio.files.sha256 \
  bos:/aihc-private-hcd/zhouzijian01/attn-moe-test/video-asr-<task>/input/audio.files.sha256
```

On the GPU host, verify the BOS listing before processing, then sync to the
explicit `/ssd2` task directory. Recompute SHA-256 there and require every
file to match. Do not start ASR on a partial directory.

Use the existing image if present, but create a new task container. Choose a
unique name and inspect GPU allocation before starting workers. The preferred
batch layout is one `--gpus all` task container plus one worker process per
GPU. Each worker must receive its own `CUDA_VISIBLE_DEVICES` value at process
launch, and the worker index must match the GPU index. Verify the mapping with
`torch.cuda.device_count()` and `nvidia-smi`; do not assume an unset process
environment variable isolates a worker.

```bash
docker run -dit \
  --name video-asr-sglang-<task> \
  --privileged \
  --gpus all \
  --ipc=host \
  --network=host \
  --ulimit memlock=-1 \
  --ulimit stack=67108864 \
  -v /ssd1:/ssd1 \
  -v /ssd2:/ssd2 \
  -v /ssd3:/ssd3 \
  -v /ssd4:/ssd4 \
  -v /usr/local/cuda-13.0/compat:/opt/cuda-compat:ro \
  -v /ssd2/video-asr-<task>:/workspace/video-asr \
  -e LD_LIBRARY_PATH=/opt/cuda-compat:/usr/local/nvidia/lib64:/usr/local/cuda/lib64 \
  -e http_proxy=http://agent.baidu.com:8891 \
  -e https_proxy=http://agent.baidu.com:8891 \
  -e PIP_INDEX_URL=https://pip.baidu-int.com/simple/ \
  --entrypoint bash \
  iregistry.baidu-int.com/zhouzijian01/sglang:qwen38flashnext
```

The vLLM image can be substituted when requested, using the same mounts and
entrypoint pattern. Pass the proxy only for the current setup or download
operation; do not persist credentials or secrets in the image.

Verify each container before installing anything:

```bash
docker exec <container> python -u -c \
  'import torch; print(torch.__version__, torch.version.cuda, torch.cuda.is_available(), torch.cuda.get_device_name(0))'
```

### 5. Install and validate the ASR runtime

Install the tested package versions through the internal index:

```bash
docker exec <container> bash -lc \
  'python -m pip install --index-url https://pip.baidu-int.com/simple/ \
    --trusted-host pip.baidu-int.com --no-cache-dir faster-whisper==1.2.1'
```

If the pip request through the proxy repeatedly returns `SSLEOFError`, make
one bounded retry with the internal mirror excluded from the proxy. Keep the
proxy for external model downloads:

```bash
docker exec <container> bash -lc \
  'unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY ALL_PROXY all_proxy; \
   export no_proxy=pip.baidu-int.com; \
   python -m pip install --index-url https://pip.baidu-int.com/simple/ \
     --trusted-host pip.baidu-int.com --no-cache-dir faster-whisper==1.2.1'
```

If the image uses CUDA 13 but the CTranslate2 GPU wheel requires CUDA 12
libraries, install the user-space compatibility wheels in the container:

```bash
docker exec <container> bash -lc \
  'python -m pip install --index-url https://pip.baidu-int.com/simple/ \
    --trusted-host pip.baidu-int.com --no-cache-dir \
    nvidia-cublas-cu12 nvidia-cudnn-cu12'
```

For every ASR process in that container, prepend the wheel library paths:

```bash
export LD_LIBRARY_PATH=/usr/local/lib/python3.12/dist-packages/nvidia/cublas/lib:/usr/local/lib/python3.12/dist-packages/nvidia/cudnn/lib:/usr/local/lib/python3.12/dist-packages/nvidia/cuda_nvrtc/lib:/opt/cuda-compat:/usr/local/nvidia/lib64:/usr/local/cuda/lib64
```

The diagnostic failure to recognize is:

```text
RuntimeError: Library libcublas.so.12 is not found or cannot be loaded
```

Do not treat this as an ASR model failure before checking the CUDA user-space
library mismatch.

### 6. Run isolated batch transcription

Use a persistent model process, cache models outside the container overlay, and
stage the bundled worker script
[scripts/faster_whisper_batch.py](scripts/faster_whisper_batch.py) into the
task mount. The script writes JSON, SRT, and TXT atomically, skips completed
JSON files, and assigns sorted inputs by `worker-index::worker-count`.

```bash
# local PC: upload the checked-in worker through the task's BOS code prefix
bcecmd bos cp /path/to/MyKnowledge/skills/video-asr-gpu-acceleration/scripts/faster_whisper_batch.py \
  bos:/aihc-private-hcd/zhouzijian01/attn-moe-test/video-asr-<task>/code/faster_whisper_batch.py

# GPU host: stage it in the same /ssd2 task directory
mkdir -p /ssd2/video-asr-<task>/skill-scripts /ssd2/video-asr-<task>/logs
bcecmd bos cp \
  bos:/aihc-private-hcd/zhouzijian01/attn-moe-test/video-asr-<task>/code/faster_whisper_batch.py \
  /ssd2/video-asr-<task>/skill-scripts/faster_whisper_batch.py

for gpu in 0 1 2 3 4 5 6 7; do
  docker exec -d -e CUDA_VISIBLE_DEVICES=$gpu \
    video-asr-sglang-<task> \
    bash -lc 'python /workspace/video-asr/skill-scripts/faster_whisper_batch.py \
      --input-dir /workspace/video-asr/input/audio \
      --output-dir /workspace/video-asr/results \
      --model large-v3-turbo \
      --model-cache-dir /ssd2/models/whisper \
      --worker-index ${CUDA_VISIBLE_DEVICES} --worker-count 8 \
      --language zh --beam-size 5 \
      > /workspace/video-asr/logs/worker-${CUDA_VISIBLE_DEVICES}.log 2>&1'
done
```

Before launching all workers, verify one mapping:

```bash
docker exec -e CUDA_VISIBLE_DEVICES=3 video-asr-sglang-<task> \
  python -c 'import torch; print(torch.cuda.device_count(), torch.cuda.get_device_name(0))'
```

The expected count is `1`; the visible device name should be the selected GPU.
For fewer GPUs, replace the loop and `--worker-count` consistently. Do not
launch eight workers with `worker-count=1` against the same shared directory.

For already bounded audio, start with `language=zh`, `beam_size=5`,
`vad_filter=false`, and `compute_type=float16`. Compare `beam_size=1` only
after inspecting text quality. Test VAD separately for long videos with
substantial silence; do not assume it is faster.

### 7. Validate ASR and repair tail artifacts

Require equal counts of JSON/SRT/TXT and parse every JSON. Check that each
segment has non-empty text, non-negative ordered starts, `end >= start`, and
that the final timestamp is near the decoded audio duration. Do not silently
accept repeated tail text or segments extending far beyond the audio.

If only a minority of items have tail anomalies, rerun those items with
`vad_filter=true` into a separate directory. Compare both candidates by
overrun, tail repetition, and body text; retain both raw candidates and a
selection report. Normalize the selected result only after this comparison:
drop segments whose start is after the audio duration and clamp an overlapping
final segment to the duration. Never overwrite the raw ASR candidate.

### 8. Import into MyKnowledge Sources

Use `transcript-only` Source ingestion. The real audio file must remain the
`input_path` used to calculate `media_input_sha256`; do not import a generated
SRT as an ordinary local subtitle, because that loses the fact that the text
was ASR-derived and loses the media hash.

Use the existing Source Preview/Apply service and record provenance including
engine, engine version, CTranslate2 version, model, model hash when available,
language, device/GPU, precision, beam size, VAD choice, and selected-candidate
report. Do not hand-edit front matter or write Source Markdown directly.

For a collection layout, decide the target before Preview and verify that the
repository's path resolver can create the requested nested path:

```text
content/sources/<domain>/<collection>/<source-id>/<source-id>.md
```

Do not encode `/` in `source_id`, pass a collection name as `domain`, create
placeholder files to trick path discovery, or apply flat Sources and manually
move them afterward. If the current Source writer cannot create nested
collection paths, extend its first-class path contract and tests before the
formal Apply; a task-local path adapter is acceptable only when it is explicit,
hash-bound, and verified on a disposable checkout.

For a batch, Preview all items first, inspect operation IDs and target paths,
then obtain the required human confirmation events and Apply. If any operation
expires or its input hash changes, re-preview that item; do not bypass the
hash/confirmation gate.

### 9. Record and interpret results

Always record:

- host/GPU/driver, container image and unique container name;
- package versions and CUDA library workaround, if any;
- audio duration and SHA-256;
- model load time, each steady-state run, median, RTF, language, beam size,
  VAD, precision, segment count, and output artifact path;
- failures and whether they were environment, download, or inference errors.
- BOS prefix, receiver-side object counts, byte totals, checksum-manifest path,
  and Source target path.

Use the following validated A100 result as a sanity-check reference, not a
guarantee: on a 60.0106875-second clip, `large-v3-turbo` with
`faster-whisper==1.2.1` and `ctranslate2==4.8.2` reached 1.155 seconds median
with FP16/beam 5 (RTF 0.0193), and 0.714 seconds with FP16/beam 1 (RTF 0.0119).
The prior local CPU Whisper Turbo measurement was 14.925 seconds on the same
clip. INT8/beam 5 measured 1.332 seconds in that test and was slower than
FP16; recheck on the target hardware before selecting a precision.

Keep the model process resident in production. The validated model load was
about 51.8 seconds on a cold cache and about 3.2 seconds with the cache warm.
For long videos, split into bounded chunks, run one process per deliberately
allocated GPU, and merge timestamps with each chunk's absolute offset. After
Source Apply, rebuild the public FTS5 index and run doctor; a stale index is an
incomplete handoff even when Source validation passes. Keep the BOS input,
output, and checksum prefixes until the receiving side and Source files have
both been verified. Do not delete the remote `/ssd2` task directory, container,
or BOS artifacts without explicit cleanup authorization.

## Cleanup and handoff

Leave the container and cached model only when the user wants a reusable test
environment. Otherwise report the exact container and artifact paths and ask
before removing them. Never clean shared model directories or unrelated
containers automatically.
