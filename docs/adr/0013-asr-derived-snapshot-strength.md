# ADR-0013：ASR 派生 snapshot 的证据强度上限为 attested

- 状态：Accepted
- 日期：2026-08-30
- 相关规范：§5.10（音视频与转录来源）、§6.7（证据要求分档）、§6.9（引文规范化）、ARC-005、SRC-002
- 相关 Feature：F001、F003、F014

## 背景

引入播客、会议演讲、视频等音视频来源后，出现一个既有契约无法回答的问题：§6.9 的逐字 exact 匹配假设 snapshot 是**原文**，`quote_sha256` 与 `selector_sha256` 都建立在这个假设上。但音视频没有原文，只有时间轴；能进入 `ledger/archive/text/` 的只能是转录稿。

转录稿是 lossy 派生物。ASR 会把 `mmap` 转成 `M map`、把数字听错、丢失说话人切换。此时逐字匹配"通过"只证明**引文与转录稿一致**，并不证明说话人说过这句话。如果不加约束，音视频来源可以通过与文本来源完全相同的路径派生出 `verified`，而它的实际可信度明显更低——这会污染 `strength` 这个派生标识的语义，而 `strength` 正是读者和 Agent 唯一依赖的证据质量信号。

## 候选方案

- A. 禁止音视频作为证据来源：最保守，但会把作者亲述设计意图这类**一手直证**排除在外，且实际使用中这类材料价值很高。
- B. 不做区分，ASR 转录稿与文本快照同等对待：实现成本为零，但让 `verified` 失去意义，属于用契约的字面通过掩盖实质差异。
- C. 新增独立的 `strength` 取值（如 `transcribed`）：语义精确，但 `strengths` 枚举已有 9 个值，新增一个会波及 projection、前端展示、Agent 契约和全部相关测试，收益与成本不匹配。
- D.（选定）复用既有 `attested` 档并施加上限：ASR 派生的 claim 最高只能到 `attested`（有可查证入口 + 引文逐字匹配 + 未做语义审计），不得派生 `verified`；人工逐字校对该片段后解除上限。

## 决策

1. **强度上限**：当 claim 的 evidence target 指向的 snapshot 由 `policy.yaml` 的 `asr_snapshot.extractor_names` 中的抽取器生成时，该 claim 的 `strength` 上限为 `attested`。上限由 validator 施加，属于派生逻辑，作者不可覆写。
2. **溯源不新增 schema**：`snapshot-manifest/v1` 已有 `extractor_name`、`extractor_version`、`extractor_options_hash`、`source_media_type`，足以表达"这份快照是谁用什么版本、什么参数转出来的"。ASR 溯源复用这些字段，不扩展 schema。
3. **解除条件**：人工逐字校对该片段后标注 `human_verified_segment`，该片段恢复为准原文，上限解除。校对是片段级而非整篇级——全片校对成本过高会导致规范被绕过。
4. **人工字幕不受限**：平台提供的人工字幕属于准原文，按普通文本快照处理；自动字幕按 ASR 处理。判据是字幕的来源，不是文件格式。
5. **数字类断言**：仅由口头来源支撑的数字类断言一律按 `inferred` 处理并写明待验证动作，必须由文档或本人实测升级。这条不依赖 ASR 判定，而是口头来源的固有属性。
6. **时间锚点无 hash**：`evidence_items.locator.media_fragment` 采用 W3C Media Fragments URI 语法，与 §5.5 的章节 locator 同性质——只用于阅读定位，没有 hash 也没有失效轴。

## 后果

- `verified` 的语义保持干净：它继续意味着"引文逐字来自可复核原文，且通过语义审计"。
- 音视频来源可用，但读者能从 `strength` 直接看出它的证据等级差异，无需读 Front Matter。
- 代价是转录稿必须记录抽取器版本；更换 ASR 模型会产生新 snapshot（沿用 §5.6 的"不覆盖旧 snapshot"规则），旧 claim 继续绑定旧转录稿。
- 只做片段级校对意味着同一份转录稿内可能同时存在已校对与未校对区间，因此 `human_verified_segment` 必须是片段级标注而不是 source 级开关。

## 重新评估条件

- ASR 词错误率在中文技术术语场景下降到可与人工转录相当，且有可验证的度量方式；
- `strengths` 枚举因其他原因需要扩展时，重新评估是否值得引入独立的 `transcribed` 取值；
- 出现比 Media Fragments 更被广泛支持的时间锚点标准。
