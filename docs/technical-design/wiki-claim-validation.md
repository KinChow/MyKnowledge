# Wiki Claim 与证据验证实现设计

- 状态：Draft
- 相关 Feature：F002、F003
- 相关规范：WIKI、EVD、VAL
- 相关 ADR：ADR-0001、ADR-0004、ADR-0005、ADR-0010
- 相关验收：[F002](../acceptance/F002-wiki-contract.md)、[F003](../acceptance/F003-evidence-validation.md)

## 目标与非目标

目标是实现 Wiki schema、Claim/Evidence 映射、snapshot + TextQuote/TextPosition selector 校验和验证报告失效。本阶段不实现复杂语义检索；检索 adapter 只能提供候选上下文，不能替代本设计的证据门禁。

## 流程

解析 Wiki → 确定性 schema 校验 → 在 owner Vault 上下文解析 target(source_id, evidence_id)，扩展为完整 ObjectRef → 按 `(vault_id, snapshot_sha256)` 读取不可变 snapshot → 在 selector 范围内匹配 supporting_quotes → 执行跨 vault 冲突/一致性检查 → 生成验证输入 → （可选）LLM 规范审计 → 人工审计确认 → 保存 semantic/content/evidence/snapshot/selector/hash 绑定报告 → 写入 durable validation attestation → 计算 private/public publishability。

## 三层发布门禁

按 ADR-0010，`published` 要求三层同时成立，缺一不可：

| 层 | 是否必须运行 | 通过要求 | 不通过/未运行时 |
| --- | --- | --- | --- |
| 确定性校验 | 必须 | 必须全部通过 | 阻断，保持 draft/review |
| LLM 规范审计 | 可选 | 一旦运行，顶层 verdict 必须为 `pass` | 未运行 `validation_state: not_run`，不阻断；`fail` 阻断 |
| 人工审计 | 必须 | 必须存在绑定当前 hash 的通过记录 | 阻断，保持 draft/review |

三条硬规则：

1. LLM `pass` **不替代**人工审计；LLM `not_run` 也**不提高**人工审计的要求。人工审计在两种情况下都是同一道必过门。
2. LLM 无权使人工确认失效。人工确认只绑定 `(content_sha256, evidence_sha256)`；规则集变化只把既有 LLM 结论标记 `stale_ruleset`（可见、不阻断、可重跑）。
3. `not_run` 不得渲染成「已验证」。页面与 preview 必须区分 `not_run` / `pass` / `fail` / `stale_ruleset`，缺省文案是「未做语义审计」，不是空白。

## LLM 规范审计（依据规范，不做自由裁量）

审计不问「这条 claim 对不对」，只问「这条 claim 在给定引文下是否违反了列出的规范条目」。因此请求里必须带规则集，且规则集是**引用**而非副本：

- `rule_refs`：数组，每条含 `doc`（规范文档路径）、`section`（章节号或 spec ID）、`extract_sha256`（运行时按章节抽取的规则原文片段 hash）；
- `ruleset_sha256`：`rule_refs` 的 canonical JSON hash，随结论持久化用于重放；
- 每条 verdict 必须带 `applied_rule_refs`。无法映射到任一规则条目的意见记为 `advisory`，只作为人工审计的参考展示，**不参与 pass/fail 判定**；
- 顶层 verdict 只有在覆盖义务全部满足、所有 claim verdict 均为 `supported`、且逐字 quote 校验全部通过时才是 `pass`。

规则原文不落第二份副本：抽取器按 `(doc, section)` 从规范文档实时取文，`extract_sha256` 记录当次取到的内容。这样规则表不会与规范漂移，代价是章节重排会改变 hash，届时既有结论标记 `stale_ruleset`。

### 覆盖与举证义务（防敷衍）

权限降级不等于可以敷衍。LLM 一旦运行，必须满足下列义务，否则整次审计**无效**（记 `not_run` + `incomplete_coverage`），不接受部分交付：

- 必须对每个可验证 claim × 每个 target 返回 verdict，缺任何一条即无效；
- 只给 advisory 而不给 verdict 视为未覆盖；
- `rationale` 必须引用 target snapshot 内的具体字符区间（`quote_sha256` + offset），泛泛结论不满足 schema；
- `not_run` 只能由运行时观测事实产生（`provider_unavailable` / `offline` / `context_exceeded` / `malformed_output` / `incomplete_coverage`）；模型不能自行声明 `not_run`，操作者选择不跑则不写审计报告（没跑就是没跑，不留「已审」痕迹）。

审计报告 append-only。人工审计界面必须展示本页历史 `fail` 次数与最近一次 `fail` 命中的规则条目——用可见性抑制「重跑刷绿」，不用锁定机制。

单次调用，`temperature=0`，持久化 `call_id`、`input_hash`、`ruleset_sha256`、`schema_version`。不做多次采样聚合——确定性采样下重复调用要么恒同（无信息量）要么说明 provider 并非确定性（声明失效），两种情况都不该用「取最保守」掩盖。

## 人工审计

人工审计是对当前 `(content_sha256, evidence_sha256)` 的一次显式背书，写入 durable `operation-confirmation/v1`（`scope: publish`、`decision: approve|reject`），内容包含：确认时刻的两个内容 hash、`DeterministicReport` 摘要 hash、LLM 审计状态（`not_run` / `pass` / `fail` / `stale_ruleset` 及其 `ruleset_sha256`）与历史 fail 次数。

正文、语义字段或 evidence 变化使确认失效，必须重新审计。规则集变化**不**使确认失效，只标记 LLM 结论 `stale_ruleset`。确认记录写入 owner `audit/validation/`，只依赖 Git 历史提供顺序与防篡改，不再自建 hash chain。


## Validator 契约

确定性 validator 必须先于 provider 运行，并输出结构化 `DeterministicReport`（canonical schema version `deterministic-validation/v1`）：对象/Vault 解析、selector 范围、quote 匹配、source independence group、版本冲突、有效 confidentiality、当前 hash 和阻断 code。LLM 只能接收已通过确定性检查的 target 上下文，不能新增 target 或放宽 quote 规则。所有 snapshot、wiki 和 claim 都以不可信数据传入显式数据边界；provider request 禁止 tools、外部 URL、浏览和隐式网络，模型输出不能触发文件写入、状态变更或新的引用解析。

Provider adapter 输入固定为 `ValidationRequest`，输出只能是 schema version 声明的 verdict/claim verdict/理由/引用片段；adapter 不得写 canonical 文件。响应经过 JSON schema、claim ID、target ID 和 quote hash 二次校验后才保存 report。多 source 一致只产生 `corroborated` 信号，不等于事实正确；存在版本、前提、数值或结论冲突时设置 `status: review` + `evidence_state: conflicting`。

Provider 能力不足、不可用、超时或返回 malformed 输出时，结果是 `validation_state: not_run` + 结构化 `not_run_reason`（`provider_unavailable` / `offline` / `context_exceeded` / `malformed_output` / `incomplete_coverage`），**不是** `fail`，也不触发能力协商。这是 LLM 可选化的直接推论：不可用是环境事实，不是审计结论。操作者主动跳过不写审计报告，因此没有 `skipped_by_operator` 这个值。报告只保存 opaque provider identity 与 `not_run_reason`，不保存 endpoint、模型版本、密钥或完整请求响应。

## LLM 规范审计（依据规范，不做自由裁量）

审计不问「这条 claim 对不对」，只问「这条 claim 在给定引文下是否违反了列出的规范条目」。因此请求里必须带规则集：

- `ruleset`：条目数组，每条含 `spec_id`（如 `VAL`/`EVD`）、`rule_id`、规则原文；
- `ruleset_sha256`：canonical JSON hash，随审计结论一并持久化；
- 每条 verdict 必须带 `applied_rule_refs`。无法映射到任一规则条目的意见记为 `advisory`，只作为人工审计的参考展示，**不参与 pass/fail 判定**；
- 顶层 verdict 只有在所有 claim verdict 均为 `supported`、无 `advisory` 之外的规则违反、且逐字 quote 校验全部通过时才是 `pass`。

`ruleset_sha256` 变化与内容 hash 变化等效：既有 LLM 审计结论立即失效，需重新审计或以 `not_run` 走人工审计通道。

单次调用，`temperature=0`，持久化 `call_id`、`input_hash`、`ruleset_sha256`、`schema_version`。不做多次采样聚合——确定性采样下重复调用要么恒同（无信息量）要么说明 provider 并非确定性（声明失效），两种情况都不该用「取最保守」掩盖。

## 人工审计

人工审计是对当前 `(content_sha256, evidence_sha256)` 的一次显式背书，写入 durable `operation-confirmation/v1`（`scope: publish`、`decision: approve|reject`），内容包含：确认时刻的两个内容 hash、`DeterministicReport` 摘要 hash、LLM 审计状态（`not_run` / `pass` 及其 `ruleset_sha256`）、以及审计人看到的 advisory 列表 hash。

正文、语义字段、evidence 或 ruleset 任一变化都使确认失效，必须重新审计——不存在「小改不用重审」的豁免。审计记录写入 owner `audit/validation/`，只依赖 Git 历史提供顺序与防篡改，不再自建 hash chain。

### Multi-source corroboration/conflict 算法（`corroboration-v1`）

“多个来源都这么写”不能用计数器实现。验证器先把每个 target 变成带 owner 和适用范围的 observation，再做成对比较；任何多数票都不能覆盖一个未解释的冲突。

1. **结构归一**：按 `(vault_id, source_id, evidence_id, snapshot_sha256, selector_sha256)` 去重；同一 source/evidence 的重复 target 只保留一条并记录 `duplicate_target`。`independence_group` 优先取 Source 的声明；缺失或相互矛盾时退回唯一 `source ObjectRef`，并写 `independence_unknown` 告警，不能凭域名推断独立。

   独立性判定交给 LLM 规范审计执行（人工无法在规模上逐对核对转载链），但它的举证义务比其他 verdict 更严：**每条独立性结论必须回引 source 的 `provenance` 字段**（`publisher`、`derived_from`、`independence_group`）或引文原文中的转载声明，并给出对应字符区间。**禁止以域名、站点名、URL 相似度、发布时间先后或"看起来像原创"作为独立性依据**——同一机构可以有多个域名，转载站也可以有独立域名，域名与独立性没有可靠映射。无法从 `provenance` 或原文举证时必须输出 `independence_unknown`，按单一 source 处理，不得猜测。
2. **观察提取**：每次 provider call 必须对已固定的 target 返回 `claim_verdict` 和可选的结构化 observation：`subject`、`predicate`、`object`、`qualifiers`（版本、时间范围、前提、单位）及 `observation_sha256`。这些字段只能描述给定 quote，不能新增 target、URL 或文件路径。无法结构化或 quote 不足时记为 `unmapped`/`unavailable`，不参与 corroboration。
3. **规范化**：使用固定 `corroboration-v1` normalizer：Unicode NFC、大小写只作用于自然语言标签、保留代码标识符和标点；单位必须先转换到声明的 canonical unit；没有明确单位或转换规则时为 `unresolved`。数值默认精确比较，不设隐含容差；需要容差必须由 claim 的显式 qualifier 声明并进入 hash。版本/时间范围使用半开区间，只有相交范围才可产生冲突。
4. **成对判定**：相同 normalized proposition 且适用范围相交，标记 `supports_same`；谓词相反、数值/单位不一致或前提互斥，标记 `conflicts`；范围不相交标记 `version_scoped`（不算冲突，但要求 claim 写出范围）；无法比较标记 `unresolved`。比较结果保存双方 target、independence group、qualifier 摘要和 comparator version。
5. **聚合**：任一 `conflicts`（且来自不同 independence group、范围相交）即 `evidence_state: conflicting`、`status: review`；没有冲突且至少两个不同 independence group 的 `supports_same` 才是 `corroborated`；只有一个 group 支持是 `supported`；部分覆盖是 `partial`，无法比较是 `unresolved`。同一 group 的转载、摘要和 `derived_from` 链永远不能贡献第二个独立组。
6. **人工边界**：冲突报告必须列出冲突对和版本/前提，不自动选择“最新”或多数结果。人工修改 claim 的适用范围、单位或版本窗口会改变 `evidence_sha256`，旧 attestation 立即失效。算法版本、normalizer 配置 hash、observation/hash 集合写入 durable validation attestation，便于重放。

因此 `corroborated` 只表达“独立来源对同一范围的一致支持”，不表达来源绝对正确；任何来源质量、时效或个人观察告警仍对读者可见。

`wiki-validation/v1` 是唯一跨 adapter 契约（请求侧不再单独定型 `wiki-validation-request/v1`，请求结构随契约同版本演进）。每个 claim verdict 只能是 `supported`、`partially_supported`、`unsupported`、`contradicted`、`unmapped`，并必须带 `applied_rule_refs` 与引用区间；单次调用必须返回完整 claim/target/quote 集合与 call ID。顶层 verdict 为 `pass` 的条件是：覆盖义务全部满足、全部 claim verdict 为 `supported`、逐字 quote 校验全部通过、且无 advisory 之外的规则违反。任一 `contradicted`/`unsupported` 即 `fail`。malformed、缺 claim、target 漂移、上下文截断、覆盖不全都不是「模型判断失败」而是协议不可用，记 `not_run` + `not_run_reason`，交由人工审计通道继续。

## 失败处理

确定性层的阻断项——缺少来源、target/snapshot/selector 不存在、quote 不匹配、source 冲突、同 Vault ID 冲突、跨 vault 引用、hash 不一致——一律阻断发布，保持 draft/review。缺少人工审计确认，或确认已因内容 hash 变化而失效，同样阻断。

LLM 不可用**不是**阻断项：记 `validation_state: not_run` + `not_run_reason`，页面与 preview 显示「未做语义审计」，人工审计通过后仍可发布。LLM `fail` 是阻断项；重跑不被禁止，但历史 fail 次数与命中规则条目必须在人工审计界面持续可见。

目标 vault unavailable 属于 F011 范畴：返回 `availability: unavailable` + `availability_reason`（`vault_unavailable`/`revision_mismatch`），保留最近一次可计算的 `evidence_state`，不能伪装成 source missing。

## 测试策略

覆盖正常 Claim、snapshot 边界、selector 消歧、规范化差异、短引文、来源漂移、多 source corroboration/冲突、验证报告失效和 private unavailable。

测试还必须固定 canonical snapshot 的 Unicode offset、malformed provider output（须落到 `not_run` 而非 `fail`）、provider 超时/离线、claim 覆盖不全须落到 `not_run: incomplete_coverage`、只给 advisory 不给 verdict 视为未覆盖、`ruleset_sha256` 变化只标记 `stale_ruleset` 而不使人工确认失效、LLM `not_run` 时人工审计仍可发布、敏感日志脱敏和报告重复应用幂等性。

## Provider 运行时边界

LLM provider 由 Codex/Claude Code 加载的 MyKnowledge Skill 在运行时选择和注入。具体 endpoint、模型版本和密钥读取方式不属于用户决策，也不写入验证 schema、Vault manifest、Git 或普通审计日志。验证器只依赖 Skill 提供的结构化结果，因此可以替换供应商而不改变验证结果 schema。没有可用或不满足 confidentiality 要求的 provider 时记 `not_run`，不做能力协商，也不阻断人工审计通道。
