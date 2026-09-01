# 音视频与转录来源实现设计（F014）

规范以 [系统设计 §5.10](../myknowledge-system-design.md) 为准；决策取舍见 [ADR-0013](../adr/0013-asr-derived-snapshot-strength.md)。规范 ID：ARC-005、SRC-002。

## 目标与非目标

**目标**：让播客、会议演讲、视频等音视频材料能进入 Source → snapshot → evidence item → claim 主链路，并让读者从 `strength` 就能看出它与文本来源的证据等级差异。

**非目标**：不改变 §6.9 的引文规范化与逐字匹配规则；不扩展 `snapshot-manifest/v1`；不新增 `strength` 取值；不实现媒体播放器或字幕编辑器。

## 当前基线（2026-08-30 实测）

- `source_types` 现有 7 个取值：`blog`、`doc`、`book`、`contest`、`pr`、`local-file`、`personal-note`。
- `source_type` 位于 `hash_inputs.source_semantic`，因此**只能新增取值，不能重命名**（SRC-002）。
- `snapshot-manifest/v1` 已有 `extractor_name`、`extractor_version`、`extractor_options_hash`、`source_media_type`，足以表达 ASR 溯源，无需扩展 schema。
- `archive.physical_dedup.owner_key: [vault_id, snapshot_sha256]`，转录稿自动继承跨 vault 物理去重。
- 本机（macOS 26.6.2 / arm64）尚未安装 `yt-dlp`、`ffmpeg`、`whisper-cpp`；`uv`、`brew`、`python3` 可用。

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

## 迁移与回滚

`source_types` 只新增取值，因此既有 163 篇 source 的 semantic hash 不变，无需重验。回滚只需移除新增枚举值与 `asr_snapshot` 段；已建立的音视频 source 会因未知 `source_type` 被拒绝，这是 fail-closed 的预期行为。

## 未决问题

- macOS 26 的 `SpeechAnalyzer`/`SpeechTranscriber` 在中文技术术语上的词错误率未实测，因此暂不列为首选抽取器（枚举中保留 `speechanalyzer` 占位）。
- 是否需要把 CSL-JSON 导出作为独立 Feature（当前 `citation/v1` 是内部锚定契约，不是学术引用格式）。
