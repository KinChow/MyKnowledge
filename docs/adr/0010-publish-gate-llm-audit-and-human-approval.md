# ADR-0010：发布门禁 = 确定性校验 + 可选 LLM 规范审计 + 必须人工审计

- 状态：Accepted
- 日期：2026-08-26
- 相关规范：VAL、EVD、OPS、SEC
- 相关 Feature：F002、F003、F004、F007
- 相关 ADR：ADR-0001、ADR-0005（引文匹配仍是确定性阻断门）

## 背景

基线版本把 LLM 证据验证做成**必须运行且必须通过**的阻断门（主规范不变量 6/7）：LLM 不可用、返回 malformed JSON、或验证失败都不得发布。配套代价是一整套 provider capability 协商（`provider-capability/v1` + `provider-capability-normalization/v1` + token 预算证明 + fail-closed 规则）、三次采样保守聚合、以及 `verdict: exempt` 豁免矩阵。

这套设计有两个不成立的前提：

1. **可用性前提**：单人本地知识库经常在离线、无 key、provider 限流的状态下工作。把 LLM 做成硬前置，等价于把「能不能发布」绑定到一个不受控的外部服务上。
2. **可信度前提**：LLM 判定不可重放。三次采样 + `temperature=0` 自相矛盾——确定性采样下三次调用要么恒同（三次无意义）要么 provider 并未真的确定性（capability 声明失效）。用不可重放的判定去守一个要求可重放的门，门本身就是假的。

但反过来把 LLM 完全降为「告警、不阻断」也不可接受：那样从 draft 到 published 之间就只剩确定性检查，而确定性检查只能证明「引文逐字存在于 snapshot 的 selector 范围内」，不能证明「这段引文支持这条 claim」。语义那一步会彻底失去把关。

## 候选方案

- **A：LLM 必须运行且必须通过（基线）**。语义把关最强，但发布可用性绑定外部服务，且需要 capability 协商 + 多次采样这套无法真正兑现可重放性的机制。
- **B：LLM 降为纯告警，不参与发布判定**。可用性最好，实现最省，但语义把关消失，`published` 的含义退化为「引文字面存在」。
- **C：LLM 可选运行、若运行必须通过；人工审计必须通过**（本 ADR 决策）。语义把关由「人」兜底而不是由「服务可用性」兜底；LLM 是可选的加速器与第二双眼睛，而不是发布的必要条件。

## 决策

发布门禁由三层组成，`published` 要求三层同时成立：

1. **确定性校验（必须运行、必须通过）**：schema、target 解析、snapshot 可读、selector 范围、`supporting_quotes.exact` 逐字匹配、hash 绑定。这一层可重放，是唯一自动阻断门。
2. **LLM 规范审计（可选运行；一旦运行，其结论必须为 pass 才能发布）**：不运行时 `validation_state: not_run`，不阻断，但**不给出任何「已验证」表述**。运行后为 `fail` 时阻断发布，且不能通过重跑刷掉——须先改内容或改 claim。
3. **人工审计（必须运行、必须通过）**：由人在 preview 阶段对当前 `content_sha256` + `evidence_sha256` 做一次显式确认，写入 durable 审计记录。**LLM pass 不替代人工审计；LLM `not_run` 也不加重人工审计的要求**——人工审计在两种情况下都是同一道必过门。

LLM 审计**必须依据写下来的规范条目**执行，不做自由裁量。规则集以**引用**方式给出，不另建一份手工维护的规则表：

- `rule_refs`：数组，每条含 `doc`（规范文档路径）、`section`（章节号或 spec ID）、`extract_sha256`（运行时按章节抽取出的规则原文片段 hash）；
- `ruleset_sha256`：`rule_refs` 的 canonical JSON hash，随审计结论持久化，用于重放；
- 每条 verdict 必须带 `applied_rule_refs`，且必须引用 target snapshot 内的具体字符区间（`quote_sha256` + offset）作为理由依据。无法映射到任一规则条目的意见记为 `advisory`，只作人工审计参考，**不参与 pass/fail 判定**。

降权不等于可以敷衍。LLM 一旦运行，必须满足下列**覆盖与举证义务**，否则整次审计无效（记 `not_run` + `incomplete_coverage`），不允许部分交付：

- 必须对每个可验证 claim × 每个 target 返回 verdict；缺任何一条即无效；
- 只给 advisory 而不给 verdict 视为未覆盖；
- `rationale` 必须引用 target 内的字符区间，泛泛结论（"看起来合理"）不满足 schema；
- `not_run` 只能由运行时观测事实产生（`provider_unavailable` / `offline` / `context_exceeded` / `malformed_output` / `incomplete_coverage`），模型不能自行声明 `not_run`；操作者选择不跑就是没跑，不写审计报告。

配套简化（作为本决策的直接后果）：

- 删除 provider capability 协商体系：LLM 既然可选，「provider 能力不足」的正确处理是 `not_run` + 记录原因，而不是 fail-closed 的能力谈判。
- 删除三次采样保守聚合：单次调用，`temperature=0`，结论连同 `ruleset_sha256`、input hash 一起持久化。
- 删除 `verdict: exempt` 豁免矩阵与「豁免类型变化必须重判」规则：LLM 可选后，「免 LLM」不再需要一条专门通道。

### 被明确排除的过度审计

以下机制曾在本 ADR 草案中出现，经权衡后**不采纳**：

- **`fail` 锁定 / 防重跑**：单人库里改一个字符就换了 input hash，锁定拦不住有意重跑，只增加实现复杂度。替代做法是报告 append-only，人工审计界面必须展示「本页历史 fail 次数与最近一次 fail 的规则条目」——同样抑制刷绿，成本低得多。
- **`ruleset_sha256` 变化使人工审计确认失效**：规范章节改一个错别字会让全库确认集体失效，是灾难性的失效放大。人工确认只绑定内容 hash（`content_sha256` + `evidence_sha256`）；ruleset 变化只把既有 LLM 结论标记 `stale_ruleset`（可见、不阻断、可重跑）。
- **advisory 列表 hash 进入确认记录**：advisory 是噪音通道，不进 hash 体系。

## 后果

- 发布不再依赖网络与 provider，离线可完成全链路；发布权的最终归属明确落在人工审计上。
- LLM 审计的定位是**规模化的第二双眼睛**：人工无法逐页复核每条 claim 与每段引文的语义匹配，这正是 LLM 补位的地方。它权限被降到「不能单独放行、不能单独否决人的确认」，但质量义务被抬高到「跑就必须全覆盖并逐条举证」。
- `published` 的语义变为：引文确定性成立 + 人已审过；「LLM 也审过」是可选增强，在页面与报告中区分展示（`not_run` / `pass` / `fail` / `stale_ruleset`），不允许把 `not_run` 渲染成通过。
- 人工审计成为吞吐瓶颈。这是有意的取舍：单人库的真实约束是「作者愿意为多少页背书」，把这个约束显式化比用 LLM 假装规模化更诚实。
- 规则原文以引用方式取自规范文档，不存在第二份手工维护的规则表，因此不会出现规则表与规范漂移。代价是抽取器必须能稳定按章节定位，章节重排会改变 `extract_sha256`。
- 主规范 §3.2 不变量 6/7 与 §8.3 仍描述方案 A，与本 ADR 冲突，需在主规范修订中对齐；在那之前以本 ADR 为准。

## 重新评估条件

- 出现可重放、可离线、可自证确定性的本地验证模型（同一 input + ruleset 恒定输出），届时第 2 层可提升为必须运行。
- 人工审计积压到使 `published` 页面长期停滞，说明门禁与产出规模不匹配，需要重新讨论分级审计（例如按 `strength` 分档）。
- 章节引用式 `rule_refs` 频繁因章节重排而失效，说明需要为规则条目引入稳定锚点（而不是回到手工规则表）。
