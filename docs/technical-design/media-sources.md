# 音视频与视频来源实现设计（F014）

规范以 [系统设计 §5.10](../myknowledge-system-design.md) 为准；决策取舍见 [ADR-0013](../adr/0013-asr-derived-snapshot-strength.md)。规范 ID：ARC-005、SRC-002。

## 目标与非目标

**目标**：让播客、会议演讲、Bilibili/YouTube 视频等音视频材料能进入 Source → snapshot → evidence item → claim 主链路，并让读者从 `strength` 就能看出它与文本来源的证据等级差异。F014 的首个完整任务是 [CS336 课程归档演练](./cs336-course-archive-task.md)，它用于验证全链路，不新增一个课程 Feature。

**非目标**：不改变 §6.9 的引文规范化与逐字匹配规则；不扩展 `snapshot-manifest/v1`；不新增 `strength` 取值；不实现媒体播放器或字幕编辑器；不把某一门课程的目录模型固化为新的长期 Feature。

## 当前基线（2026-08-30 实测）

- `source_types` 现有 7 个取值：`blog`、`doc`、`book`、`contest`、`pr`、`local-file`、`personal-note`。
- `source_type` 位于 `hash_inputs.source_semantic`，因此**只能新增取值，不能重命名**（SRC-002）。
- `snapshot-manifest/v1` 已有 `extractor_name`、`extractor_version`、`extractor_options_hash`、`source_media_type`，足以表达 ASR 溯源，无需扩展 schema。
- `archive.physical_dedup.owner_key: [vault_id, snapshot_sha256]`，转录稿自动继承跨 vault 物理去重。
- 本机（macOS 26.6.2 / arm64）尚未安装 `yt-dlp`、`ffmpeg`、`whisper-cpp`；`uv`、`brew`、`python3` 可用。

## 已实现切片：transcript-only Source（2026-09-07）

第一切片已落地为 `source_type: video` 的本地字幕导入，不下载或保存媒体原件：

```bash
python -m tools.cli source \
  --video-transcript /tmp/lecture.vtt \
  --url 'https://www.bilibili.com/video/BV1j9Kc6mEq4?p=1' \
  --source-id cs336-p01 --domain computer-science
```

命令只产生 Preview；把返回的 `operation_id` 交给 `source --apply <id> --confirm` 才会写入。VTT/SRT 被规范化为带 `HH:MM:SS.mmm` 时间范围的 Markdown transcript，源文件和 `archive/manifest.jsonl` 同时记录视频 URL、输入字幕 hash、解析器版本及 `archive_policy: transcript-only`。apply 前会重新校验字幕文件的 hash/stat，字幕漂移会返回 `hash_mismatch`。该切片不写 `archive/raw/`，因此不把字幕文件误报为视频原件。

实现入口：`tools/ingest/video_transcript.py`、`tools/ingest/source_ingestor.py`；测试入口：`tests/ingest/test_video_transcript.py`。平台字幕下载、ASR、关键帧和图片附件属于后续切片，不能由本切片的通过结果代替。

平台字幕切片已追加：`tools/ingest/video_subtitles.py` 通过成熟工具 `yt-dlp` 请求
`--skip-download --write-subs --sub-format vtt`，只把选定字幕轨道送入同一 canonical parser；
人工字幕优先，只有请求显式设置 `--allow-automatic-subtitles` 才尝试自动字幕。Source 中记录
`yt-dlp` 版本、字幕语言、`manual/automatic` 来源和字幕输入 hash；无字幕返回
`video_subtitles_missing`，不自动把失败降级成伪造文本。CLI 示例：

```bash
python -m tools.cli source --video-subtitles \
  --url 'https://www.bilibili.com/video/BV1j9Kc6mEq4?p=1' \
  --source-id cs336-p01 --domain computer-science \
  --allow-automatic-subtitles
```

该模式同样是 Preview → Apply，且不下载视频、不写 `archive/raw/`。真实探测显示当前
CS336 Bilibili 合集没有公开字幕轨道，因此该任务应进入本地 ASR 路径。

本地 ASR 切片使用 `whisper.cpp` 的 SRT 输出模式：

```bash
python -m tools.cli source --video-asr \
  --from-file /tmp/lecture.mp4 \
  --url 'https://www.bilibili.com/video/BV1j9Kc6mEq4?p=1' \
  --asr-model /models/ggml-large-v3-turbo.bin \
  --source-id cs336-p01 --domain computer-science
```

适配器不实现 ASR 模型本身，只调用成熟的 `whisper.cpp` 可执行文件；模型权重留在
外部环境，manifest/source 只记录模型名、模型 SHA-256、引擎版本、语言和线程参数。
媒体输入只用于转录完整性 hash，`transcript-only` 仍不归档媒体原件。ASR transcript
默认属于派生证据，强度封顶和人工片段解锁仍需后续 evidence validator 切片接通。

同一 Source 也支持成熟的 `openai-whisper` CLI：设置
`--asr-engine openai-whisper --asr-model turbo --asr-model-sha256 <sha256>`；模型 hash
由独立模型管理流程计算并显式传入，避免把本机缓存路径写入 canonical metadata。

关键帧使用 `video-frames preview` / `video-frames apply`，底层调用成熟的 `ffmpeg`
单帧 PNG 输出。Preview 只接受显式时间点（秒），去重并排序后把每张图片的 timestamp、
输入视频 hash、ffmpeg 版本/参数和图片 hash 写入 operation；Apply 经人工确认后才把
图片和 `media/frames/manifest.json` 放到 Source 目录。媒体漂移、ffmpeg 缺失或抽帧失败
都会阻断，未确认的 staging 不进入 Source，也不进入 `archive/raw/`。

## F014 的功能边界

F014 交付的是可复用的视频 Source 能力，而不是某一门课程的内容。通用能力包括：

- 单个 Bilibili/YouTube URL 或用户明确给出的 playlist/合集的 metadata inventory；
- 平台人工字幕、自动字幕、本地 ASR 的统一 transcript snapshot；
- 视频片段、音频片段、关键帧和 OCR 结果的派生产物登记；
- `media_fragment` 时间定位、TextQuote/TextPosition evidence selector 和 ASR strength gate；
- 可恢复、幂等、hash 绑定和 partial/blocked 状态；
- 对官方网页/PDF/Git 资料的 `local-file`/`fetch` 来源登记，但不自动进行无界课程爬取。

课程、专题或合集只是一次任务的编排输入。任务可以使用一个 collection Source 或多个已存在 Source，但不得因为 CS336 而新增 `course` source type、课程专用 Wiki schema 或不可复用的目录字段。

## 数据模型

`config/vocab.yaml`：`source_types` 新增 `podcast`、`video`、`talk`、`paper`、`spec`、`software`、`dataset`（对齐 CSL / Zotero item type 子集，映射关系写在注释里，不通过改名表达）；`archive_policies` 新增 `transcript-only`。

`evidence_items.locator` 新增可选字段 `media_fragment`（W3C Media Fragments URI 语法，如 `#t=1450,1520`）。它与 `heading_slug` 同性质：只用于阅读定位，不参与 `selector_sha256`、`quote_sha256` 或任何失效轴。

`config/policy.yaml` 新增：

~~~yaml
asr_snapshot:
  extractor_names: [whisper.cpp, mlx-whisper, speechanalyzer]
  max_strength: attested
  human_verified_segment_unlocks: true
~~~

## 转录获取链（三档，按成本递增）

1. **平台已有字幕**：`yt-dlp --skip-download --write-subs --sub-format vtt`。人工字幕视为准原文，按普通文本快照处理；自动字幕按 ASR 处理。判据是字幕来源，不是文件格式。
2. **本地 ASR**：`whisper.cpp` + `ggml-large-v3-turbo`。选它而不是 Python 实现的理由是单二进制 + 可校验模型文件，`extractor_version` 与模型 sha256 可完整落入 manifest。
3. **片段转录**：`ffmpeg -ss <t-30> -t 120` 截取命中点前后各 30 秒再转录。**日常默认走这一档**，不做全片转录——全片转录的产出是大量永不阅读的文字，却会让"记一条播客"的成本高到规范被绕过。

## 正常流程

原始媒体（`podcast`/`video`/`talk`）建立 source → 生成转录稿并作为 snapshot 入 `ledger/archive/text/`，manifest 记录抽取器名称、版本与参数 hash → 在转录稿上建立 evidence item（selector + 可选 `media_fragment`）→ wiki claim 引用该 evidence item → 确定性校验在转录稿范围内逐字匹配。

对于合集/课程任务，先执行 metadata-only inventory，再由人工确认 scope；不得在 inventory 阶段自动下载或转录全部条目。每个选定条目必须保留平台 ID、原始 URL、resolved URL、平台序号、标题、时长、来源角色和独立 hash。官方课程网站、讲义、作业和代码仓库作为独立来源登记，平台视频只作为媒体来源，不因为标题相同而自动合并来源独立性。

## 失败流程与强度封顶

- validator 发现 evidence target 的 snapshot 由 `asr_snapshot.extractor_names` 中的抽取器生成时，把该 claim 的 `strength` 上限设为 `attested`。若其它条件本可派生 `verified`，必须降到 `attested` 并在页面上可见，不得静默保留 `verified`。
- 人工逐字校对某片段后标注 `human_verified_segment`，该片段恢复准原文地位。标注是**片段级**，因为同一份转录稿内可以同时存在已校对与未校对区间。
- 仅由口头来源支撑的数字类断言：`support` 必须是 `inferred`，正文必须写明待验证动作。
- 更换 ASR 模型或参数：按 §5.6 生成新 snapshot，不覆盖旧 snapshot；旧 claim 继续绑定旧转录稿，是否迁移由人工确认。
- 媒体原件不可归档时使用 `transcript-only`：此档下转录稿是主快照而非补充快照，`external_snapshot_is_supplemental` 的语义不适用。

## 安全边界

转录工具在本地运行、不联网；`yt-dlp` 的抓取受 §5.9 与 `security.fetch` 的既有约束（scheme、端口、重定向、私网拒绝）。模型文件不进仓库，只在 manifest 中记录版本与 hash 引用。

## 测试策略

fixture 必须是**真实产物**：用一集真实播客的 `whisper.cpp` 输出作为转录稿 snapshot，不手写假转录稿。核心断言是「ASR 派生的 claim 无法派生 `verified`」和「标注 `human_verified_segment` 后可解除上限」。`transcript-only` 需断言不写 `ledger/archive/raw/`、不触发 `raw_requires_lfs`。

F014 的首个端到端任务使用 [CS336 课程归档任务](./cs336-course-archive-task.md) 的真实 Bilibili 合集和 Stanford 官方资料。该任务必须先证明平台 inventory 和官方资源 allowlist，再选定少量条目做字幕/ASR/抽帧/Evidence；不能以“整套视频下载成功”替代功能验收。

## 迁移与回滚

`source_types` 只新增取值，因此既有 163 篇 source 的 semantic hash 不变，无需重验。回滚只需移除新增枚举值与 `asr_snapshot` 段；已建立的音视频 source 会因未知 `source_type` 被拒绝，这是 fail-closed 的预期行为。

## 未决问题

- macOS 26 的 `SpeechAnalyzer`/`SpeechTranscriber` 在中文技术术语上的词错误率未实测，因此暂不列为首选抽取器（枚举中保留 `speechanalyzer` 占位）。
- 是否需要把 CSL-JSON 导出作为独立 Feature（当前 `citation/v1` 是内部锚定契约，不是学术引用格式）。
