# F014 音视频与转录来源验收

- Feature：F014
- 相关规范：ARC-005、SRC-002（系统设计 §5.10、§5.6、§6.7、§6.9）
- ADR：ADR-0013
- 实现设计：[音视频与转录来源](../technical-design/media-sources.md)
- 状态：In progress（2026-09-07；transcript-only、平台字幕探测、ASR、批处理和关键帧已实现；完整真实任务及部分 AC 仍待完成）
- 测试运行：`/tmp/video-f014-test-env/bin/python -m pytest -q tests/ingest/test_video_transcript.py tests/ingest/test_video_inventory.py tests/ingest/test_source_ingestor.py`
- 首个真实任务：[CS336 课程归档演练](./cs336-course-archive-task.md)

## Fixture 约定

转录稿 fixture 必须是**真实产物**：使用一集真实播客经 `whisper.cpp` 产生的 VTT/文本输出，不手写假转录稿。人工字幕 fixture 使用平台导出的人工字幕文件。

## AC-F014-001 新增 source_type 不影响既有 source

- Given：`vocab.yaml` 的 `source_types` 新增 `podcast`、`video`、`talk`、`paper`、`spec`、`software`、`dataset`，既有 7 个取值全部保留；
- When：重算全部既有 source 的 semantic hash；
- Then：163 篇既有 source 的 `content_sha256` 与语义 hash 全部不变，无需重验；新类型 source 可正常建立；
- 失败时不变量：**不得重命名或删除既有取值**（`source_type` 位于 `hash_inputs.source_semantic`，改名会触发全库重验）；CSL 对齐只能通过映射表表达；
- 自动化级别：Unit。
- 对应测试：待实现。
- 当前状态：部分实现：`video` 已加入枚举并通过既有 Source 导入回归；其它计划中的媒体/学术类型仍待实现。

## AC-F014-002 media_fragment 不参与任何 hash

- Given：一个含 `locator.media_fragment: "#t=1450,1520"` 的 evidence item；
- When：计算 `selector_sha256`、`quote_sha256` 与 wiki 的 `evidence_sha256`；
- Then：三者与不含 `media_fragment` 时完全一致；修改 `media_fragment` 不使任何 claim 失效；
- 失败时不变量：`media_fragment` 与 §5.5 的章节 locator 同性质，只用于阅读定位，不得引入新的失效轴；
- 自动化级别：Unit。
- 对应测试：`tests/anchor/test_evidence_anchor.py`。
- 当前状态：已实现。

## AC-F014-003 ASR 派生的 claim 强度封顶 attested

- Given：一条 claim，其 evidence target 指向由 `whisper.cpp` 生成的 snapshot（manifest 中 `extractor_name`、`extractor_version`、`extractor_options_hash` 已记录），且其它条件本可派生 `verified`；
- When：执行确定性校验与 strength 派生；
- Then：`strength` 为 `attested`，不是 `verified`；页面上可见该强度标识；
- 失败时不变量：不得静默保留 `verified`；不得由作者字段覆写派生结果；
- 自动化级别：Unit。
- 对应测试：`tests/validation/test_video_strength.py`。
- 当前状态：已实现。

## AC-F014-004 片段级人工校对解除上限

- Given：AC-F014-003 的同一条 claim，其引用片段已人工逐字校对并标注 `human_verified_segment`；
- When：重新执行 strength 派生；
- Then：上限解除，该 claim 可按常规规则派生 `verified`；同一份转录稿内未校对区间的其它 claim 仍被封顶为 `attested`；
- 失败时不变量：标注必须是片段级，不得以 source 级开关一次性解除整篇；
- 自动化级别：Unit。
- 对应测试：`tests/validation/test_video_strength.py`。
- 当前状态：已实现。

## AC-F014-005 人工字幕按准原文处理、自动字幕按 ASR 处理

- Given：同一场演讲的两份字幕——平台人工字幕与平台自动字幕；
- When：分别建立 snapshot 并派生 strength；
- Then：人工字幕支撑的 claim 可派生 `verified`；自动字幕支撑的 claim 被封顶为 `attested`；
- 失败时不变量：判据是字幕来源而不是文件格式，`.vtt` 后缀本身不构成任何强度依据；
- 自动化级别：Unit。
- 对应测试：`tests/ingest/test_video_subtitles.py`、`tests/validation/test_video_strength.py`。
- 当前状态：部分实现：来源 provenance 已区分人工/自动；人工字幕准原文与自动字幕 ASR 的完整 strength 回归仍待补。

## AC-F014-007a transcript-only 本地字幕切片（已实现）

- Given：`source_type: video`、可访问的视频 URL，以及本地 `.vtt` 或 `.srt` 字幕文件；
- When：执行 `SourceIngestor.preview` → 人工确认 `apply`；
- Then：字幕被规范化为带时间范围的 Markdown snapshot，Source 与 manifest 记录视频 URL、字幕输入 hash、`video-transcript/1` 和 `archive_policy: transcript-only`；不写 `archive/raw/`；
- 失败时不变量：preview 后字幕文件发生内容或 stat 漂移，apply 返回 `hash_mismatch`；空字幕、反向时间或不支持后缀被阻断；
- 自动化级别：Unit + integration；
- 对应测试：`tests/ingest/test_video_transcript.py`；
- 当前状态：已实现并独立环境验证通过。

## AC-F014-005a 平台字幕获取（已实现）

- Given：Bilibili/YouTube URL；
- When：执行 `source --video-subtitles`，调用 `yt-dlp` 的 `--skip-download` 和字幕选项；
- Then：优先获取人工字幕并规范化为同一 transcript snapshot，Source 记录 `yt-dlp` 版本、语言、`manual`/`automatic` 来源和输入 hash；
- 失败时不变量：只有显式允许自动字幕时才回退自动字幕；没有字幕返回 `video_subtitles_missing`；不下载视频，不写 `archive/raw/`；
- 自动化级别：Unit + integration + live probe；
- 对应测试：`tests/ingest/test_video_subtitles.py`；真实 Bilibili 探测记录为无字幕阻断；
- 当前状态：已实现并独立环境验证通过。

## AC-F014-003a 本地 ASR provenance（已实现）

- Given：本地音视频文件，以及外部 `whisper.cpp` 或 `openai-whisper` 可执行文件和模型；
- When：执行 `source --video-asr`；
- Then：读取 ASR CLI 生成的 SRT，转为 canonical transcript，并记录引擎版本、模型名/hash、语言、线程参数和媒体输入 hash；
- 失败时不变量：媒体、模型或 ASR 运行时缺失时结构化阻断；模型权重和媒体不写入仓库的 `archive/raw/`；
- 自动化级别：Unit + integration；
- 对应测试：`tests/ingest/test_video_asr.py`；真实 CS336 P1 30 秒样本使用 OpenAI Whisper Turbo 跑通，P9/P10 full transcript 使用 whisper.cpp 跑通并完成 canonical Apply。
- 当前状态：已实现并独立环境验证通过；ASR strength gate 由 `tests/validation/test_video_strength.py` 覆盖。

## AC-F014-008a 关键帧 manifest 与确认落位（已实现）

- Given：已存在的 `video` Source、本地媒体文件和人工选择的时间点；
- When：执行 `video-frames preview` 后人工确认 `video-frames apply`；
- Then：ffmpeg 生成 PNG，Source 的 `media/frames/` 和 manifest 记录视频 hash、时间戳、ffmpeg 版本/参数及图片 hash；
- 失败时不变量：媒体漂移、ffmpeg 缺失、抽帧失败或未确认不得把图片写入 Source；图片不能脱离视频 hash 单独成为事实证据；
- 自动化级别：Unit + integration；
- 对应测试：`tests/ingest/test_video_frames.py`；
- 当前状态：已实现并独立环境验证通过。

## AC-F014-006 口头来源的数字类断言必须降级

- Given：一条数字类断言（性能数据、比例、耗时），其唯一支撑来自口头来源；
- When：执行确定性校验与来源/语气矩阵检查；
- Then：`support` 必须是 `inferred`，正文必须写明待验证动作；否则校验失败且页面保持 `draft`；
- 失败时不变量：不得把口头给出的数字表述为外部普遍事实；升级必须依靠文档或本人实测；
- 自动化级别：Unit。
- 对应测试：待实现。
- 当前状态：待实现。

## AC-F014-007 transcript-only 归档策略

- Given：媒体原件不可归档，`archive_policy: transcript-only`；
- When：执行 source 导入与归档；
- Then：转录稿写入 `ledger/archive/text/` 并作为主快照；`ledger/archive/raw/` 无写入；不触发 `raw_requires_lfs` 前置检查；
- 失败时不变量：此档下转录稿不是补充快照，`external_snapshot_is_supplemental` 语义不适用；不得因缺少媒体原件而判定"抓取失败、不允许写入"；
- 自动化级别：Unit。
- 对应测试：待实现。
- 当前状态：待实现。

## AC-F014-008 更换抽取器生成新 snapshot 而非覆盖

- Given：一份已被 claim 引用的 ASR 转录稿；
- When：更换 ASR 模型或参数后重新转录；
- Then：生成新 snapshot 并追加 manifest 记录，旧 snapshot 保留；旧 claim 继续绑定旧转录稿；是否迁移由人工确认；
- 失败时不变量：沿用 §5.6，不覆盖旧 snapshot，不原地改写已被引用的 manifest 记录；
- 自动化级别：Unit。
- 对应测试：待实现。
- 当前状态：待实现。

## 首个真实任务

F014 的完整验收不能只依赖 unit fixture。首个真实任务是 [CS336 课程归档演练](./cs336-course-archive-task.md)，其任务级验收编号为 `TASK-CS336-001`–`TASK-CS336-010`，覆盖 Bilibili 合集 inventory、范围确认、官方 Stanford 资料 allowlist、字幕/ASR、关键帧、时间戳证据、漂移恢复和 public/private 隔离。

任务验收通过的条件是：所有阻断级任务场景通过，且至少一条真实视频产生可校验 transcript snapshot、至少一份官方资料产生可校验 text/PDF snapshot；任务失败或只完成 metadata inventory 时，F014 仍保持 `Designed`，不得标记为 `Accepted`。
