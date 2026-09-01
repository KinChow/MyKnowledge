# F014 音视频与转录来源验收

- Feature：F014
- 相关规范：ARC-005、SRC-002（系统设计 §5.10、§5.6、§6.7、§6.9）
- ADR：ADR-0013
- 实现设计：[音视频与转录来源](../technical-design/media-sources.md)
- 状态：Designed（2026-08-30；尚未实现，全部场景待实现）
- 测试运行：`.venv/bin/python -m pytest tests/ingest/ tests/validation/`

## Fixture 约定

转录稿 fixture 必须是**真实产物**：使用一集真实播客经 `whisper.cpp` 产生的 VTT/文本输出，不手写假转录稿。人工字幕 fixture 使用平台导出的人工字幕文件。

## AC-F014-001 新增 source_type 不影响既有 source

- Given：`vocab.yaml` 的 `source_types` 新增 `podcast`、`video`、`talk`、`paper`、`spec`、`software`、`dataset`，既有 7 个取值全部保留；
- When：重算全部既有 source 的 semantic hash；
- Then：163 篇既有 source 的 `content_sha256` 与语义 hash 全部不变，无需重验；新类型 source 可正常建立；
- 失败时不变量：**不得重命名或删除既有取值**（`source_type` 位于 `hash_inputs.source_semantic`，改名会触发全库重验）；CSL 对齐只能通过映射表表达；
- 自动化级别：Unit。
- 对应测试：待实现。
- 当前状态：待实现。

## AC-F014-002 media_fragment 不参与任何 hash

- Given：一个含 `locator.media_fragment: "#t=1450,1520"` 的 evidence item；
- When：计算 `selector_sha256`、`quote_sha256` 与 wiki 的 `evidence_sha256`；
- Then：三者与不含 `media_fragment` 时完全一致；修改 `media_fragment` 不使任何 claim 失效；
- 失败时不变量：`media_fragment` 与 §5.5 的章节 locator 同性质，只用于阅读定位，不得引入新的失效轴；
- 自动化级别：Unit。
- 对应测试：待实现。
- 当前状态：待实现。

## AC-F014-003 ASR 派生的 claim 强度封顶 attested

- Given：一条 claim，其 evidence target 指向由 `whisper.cpp` 生成的 snapshot（manifest 中 `extractor_name`、`extractor_version`、`extractor_options_hash` 已记录），且其它条件本可派生 `verified`；
- When：执行确定性校验与 strength 派生；
- Then：`strength` 为 `attested`，不是 `verified`；页面上可见该强度标识；
- 失败时不变量：不得静默保留 `verified`；不得由作者字段覆写派生结果；
- 自动化级别：Unit。
- 对应测试：待实现。
- 当前状态：待实现。

## AC-F014-004 片段级人工校对解除上限

- Given：AC-F014-003 的同一条 claim，其引用片段已人工逐字校对并标注 `human_verified_segment`；
- When：重新执行 strength 派生；
- Then：上限解除，该 claim 可按常规规则派生 `verified`；同一份转录稿内未校对区间的其它 claim 仍被封顶为 `attested`；
- 失败时不变量：标注必须是片段级，不得以 source 级开关一次性解除整篇；
- 自动化级别：Unit。
- 对应测试：待实现。
- 当前状态：待实现。

## AC-F014-005 人工字幕按准原文处理、自动字幕按 ASR 处理

- Given：同一场演讲的两份字幕——平台人工字幕与平台自动字幕；
- When：分别建立 snapshot 并派生 strength；
- Then：人工字幕支撑的 claim 可派生 `verified`；自动字幕支撑的 claim 被封顶为 `attested`；
- 失败时不变量：判据是字幕来源而不是文件格式，`.vtt` 后缀本身不构成任何强度依据；
- 自动化级别：Unit。
- 对应测试：待实现。
- 当前状态：待实现。

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
