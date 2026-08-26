# F003 Claim/Evidence 验收

- Feature：F003
- 相关规范：EVD、VAL
- 状态：Implemented（2026-08-27，102/102 测试通过）
- 实现证据：`tools/validation/{audit,provider,ruleset,corroboration,confirm}.py`、
  `config/json-schema/validation-response-v1.json`、`config/policy.yaml`
  `validation.ruleset.rule_ids`、`tests/validation/test_{audit,ruleset,corroboration}.py`
- 剩余待界定：AC-F003-006/010 的 cross-vault unavailable 完整语义依赖 F011
  private vault 挂载（当前单 vault 阶段按 unavailable 处理，保留最近 evidence_state）；
  真实 LLM 端到端集成测试依赖运行时 provider（ducc/ducx 冒烟已通过，未纳入离线测试）

## AC-F003-001 Claim 显式绑定 Evidence

- Given：知识型 Wiki 包含可验证 Claim；
- When：执行证据校验；
- Then：每个 Claim 都有有效 Evidence target，并能解析到不可变 snapshot、TextQuote/TextPosition selector 和 source locator 展示信息；
- 失败时不变量：缺失映射不得进入 `published`；
- 自动化级别：Integration。

## AC-F003-002 supporting_quotes 在 snapshot selector 内逐字匹配

- Given：quote 位于或不位于 target 指定的 snapshot selector；
- When：执行共享规范化匹配；
- Then：只有 selector 范围内、达到最小长度且逐字匹配的 `supporting_quotes.exact` 才通过；prefix/suffix/position 只能辅助恢复，不能单独放行；
- 自动化级别：Unit。

## AC-F003-003 验证报告绑定 hash

- Given：正文、语义字段或 Evidence 发生变化；
- When：复用旧验证报告；
- Then：报告失效，Wiki 不得继续以旧报告发布；
- 自动化级别：Integration。

## AC-F003-004 多 Source 一致与冲突

- Given：同一 Claim 有多个独立 source target，分别一致或冲突；
- When：执行 evidence consistency check；
- Then：按 `corroboration-v1` 先按 independence group、适用版本/时间范围和规范化 observation 做成对比较；相同范围的一致支持才派生 `evidence_state: corroborated`，存在相交范围冲突时设置 `status: review` + `evidence_state: conflicting`，不能按多数票或“最新来源”自动发布；
- 失败时不变量：任何未解决冲突不得进入 `published`、`private_publishable` 或 `public_publishable`；
- 自动化级别：Integration。

## AC-F003-012 Corroboration 规则可重放

- Given：多个 target 的 source 声明不同/未知 independence group，包含相同命题、版本不相交命题、单位/数值差异和无法结构化的引文；
- When：执行 `corroboration-v1` consistency check；
- Then：输出稳定的 observation hash、比较结果、冲突 target 对、版本/前提范围和人工复核原因；同组转载不贡献独立佐证，版本不相交只标记 `version_scoped`，未知/单位无法转换标记 `unresolved`；
- 失败时不变量：不能通过增加转载数量、隐含数值容差或多数票把冲突对象变为 `corroborated`/publishable；
- 自动化级别：Unit/Integration。

## AC-F003-005 转载链不计为独立来源

- Given：多个 source 内容相同，其中部分标记同一 `independence_group` 或 `derived_from` 关系；另有一组 source 域名各不相同但 `provenance` 未声明独立性；
- When：执行 corroboration 计算；
- Then：只有不同独立组才贡献 corroboration；LLM 判定独立性时每条结论必须回引 source 的 `provenance` 字段（`publisher`/`derived_from`/`independence_group`）或引文原文中的转载声明，并给出字符区间；无法从 `provenance` 或原文举证时输出 `independence_unknown` 并按单一 source 处理；
- 失败时不变量：**禁止以域名、站点名、URL 相似度、发布时间先后或"看起来像原创"作为独立性依据**；不能因重复转载数量增加而自动提升或发布 Claim；未回引 `provenance` 的独立性结论不得参与 `corroborated` 派生；
- 自动化级别：Unit/Integration。

## AC-F003-006 snapshot owner 与 unavailable 隔离

- Given：evidence target 指向某 private Vault 的 snapshot，且该 Vault 未挂载、revision 不匹配或同 hash 在多个 Vault 物理去重；
- When：执行 deterministic validation；
- Then：resolver 必须按 `(vault_id, snapshot_sha256)` 解析；受影响对象返回 `availability: unavailable`/对应阻断码，`evidence_state` 不被改成 `missing`，无关 Vault 继续验证；
- 失败时不变量：不能仅凭裸 snapshot hash 读取另一个 owner 或把 unavailable 当作证据不存在；
- 自动化级别：Unit/Integration。

## AC-F003-007 验证报告 hash 与人工审计持久化

- Given：Wiki 正文、语义字段、evidence、source semantic hash 或 target selector 发生变化，或仅有临时 provider report 而没有 durable 人工审计记录；
- When：尝试复用报告并发布；
- Then：报告与人工审计确认同时失效并保持 draft/review；只有当前 hash 绑定的 `operation-confirmation/v1`（`scope: publish`、`decision: approve`）写入 owner `audit/validation/` 后才能进入 private/public publishability；确认记录必须包含两个内容 hash、`DeterministicReport` 摘要 hash、LLM 审计状态（`not_run`/`pass`/`fail`/`stale_ruleset` 及其 `ruleset_sha256`）与历史 fail 次数；
- 失败时不变量：不能因 `state/llm-validation/` 缓存存在就声称可复现验证；不能只有 LLM 结论而无人工确认；
- 自动化级别：Integration/Repository。

## AC-F003-008 LLM 审计可选运行且必须依据规范条目

- Given：确定性校验已通过；LLM provider 分别处于可用、离线/不可用、返回 malformed 输出三种状态；审计请求携带规则集与 `ruleset_sha256`；
- When：执行 LLM 规范审计；
- Then：可用时单次调用（`temperature=0`）产出顶层 verdict，每条 claim verdict 必须带 `applied_rule_refs` 与 target 内引用区间，无法映射到规则条目的意见记为 `advisory` 且不参与 pass/fail；离线/不可用/malformed 一律落到 `validation_state: not_run` + 结构化 `not_run_reason`，不得记为 `fail`；`call_id`、`input_hash`、`ruleset_sha256`、`schema_version` 写入报告；
- 失败时不变量：不做多次采样聚合；不得把 `not_run` 表述为已验证；不得用未回引规则条目的自由裁量意见阻断或放行发布；`rule_refs` 只能引用规范文档章节，不得另建手工维护的规则表副本；
- 自动化级别：Unit/Integration。

## AC-F003-013 三层发布门禁的组合判定

- Given：一个页面的确定性校验通过，LLM 审计分别为 `not_run` / `pass` / `fail` / `stale_ruleset`，人工审计分别为存在有效确认 / 无确认 / 确认已因内容变更失效；
- When：计算 publishability 并尝试发布；
- Then：只有「确定性 pass + LLM ∈ {not_run, pass, stale_ruleset} + 存在绑定当前 `(content_sha256, evidence_sha256)` 的人工审计 approve」才能进入 `published`；LLM `fail` 阻断；缺少或已失效的人工审计阻断；LLM `pass` 不替代人工审计；
- 失败时不变量：LLM `not_run` 不得因此提高或降低人工审计要求；LLM 无权使人工确认失效；不得存在任何绕过人工审计的发布路径；
- 自动化级别：Integration。

## AC-F003-014 LLM 审计的覆盖与举证义务

- Given：一页含 N 个可验证 claim × M 个 target；provider 分别返回：全覆盖且逐条带引用区间 / 漏掉部分 claim / 某 claim 只给 advisory 不给 verdict / `rationale` 无引用区间 / 模型自行声明 `not_run`；
- When：校验 provider 输出并写入审计报告；
- Then：只有全覆盖 + 每条 verdict 带 `applied_rule_refs` 与 target 内引用区间时才是一次有效审计；其余情况整次审计无效，记 `validation_state: not_run` + `not_run_reason: incomplete_coverage`，不保存部分结论；模型自行声明的 `not_run` 被拒绝，`not_run` 只能由运行时观测事实产生；
- 失败时不变量：不接受部分交付；不得把 advisory 计入覆盖；不得用无引用的泛泛结论构成 `pass`；操作者主动跳过时不得写出任何「已审」记录；
- 自动化级别：Unit/Integration。

## AC-F003-015 规则集变更只标记 stale_ruleset，不使人工确认失效

- Given：页面内容与 evidence 不变，但被引用的规范章节变更导致 `extract_sha256` / `ruleset_sha256` 改变；
- When：重新计算 publishability；
- Then：既有 LLM 结论标记 `stale_ruleset` 并在页面与 preview 可见，不阻断；人工审计确认因只绑定 `(content_sha256, evidence_sha256)` 而**仍然有效**；页面可继续保持 `published`；
- 失败时不变量：规则措辞变更不得引发全库人工确认集体失效；`stale_ruleset` 不得被渲染成 `pass`；
- 自动化级别：Integration。

## AC-F003-016 fail 历史可见但不锁定

- Given：某页曾有一次或多次 LLM `fail`，随后内容被修改并重新审计通过；
- When：进入人工审计界面并发布；
- Then：审计报告 append-only，界面必须展示历史 `fail` 次数与最近一次 `fail` 命中的规则条目；重跑本身不被禁止；人工确认记录中保存历史 fail 次数；
- 失败时不变量：不得删除或覆盖历史 fail 报告；不得在人工审计界面隐藏 fail 历史；
- 自动化级别：Integration。

## AC-F003-009 代码与中文引文规范化不扩大范围

- Given：snapshot 同时包含中文排版换行、英文词边界、C/C++ 指针/乘法符号和 Markdown 包装文本；
- When：执行共享 quote normalization 和 TextPosition/TextQuote 匹配；
- Then：只按 extractor 提供的 offset map 处理展示标记，代码标点和英文空格语义保持，多个候选返回 `ambiguous_selector`；
- 失败时不变量：不能通过删除全部空白、剥离代码字符或扩大 selector 范围制造假匹配；
- 自动化级别：Unit/Security。

## AC-F003-010 unavailable 不改写证据质量

- Given：Wiki 已有可计算的 evidence_state，但其 owner Vault 暂时未挂载、revision 不匹配或 local sidecar 不可用；
- When：执行 deterministic validation 和 projection；
- Then：返回 `availability: unavailable`、原因和 `validation_state: unavailable`，保留最近 evidence_state（首次计算才为 unresolved），不生成 publishable projection；
- 失败时不变量：不能把 unavailable 写成 `evidence_state: missing`，也不能读取另一个 Vault 的同 hash snapshot；
- 自动化级别：Unit/Integration。

## AC-F003-011 不可信 Source 上下文隔离

- Given：snapshot/wiki/claim 文本包含伪造的系统指令、工具调用或外部 URL；
- When：构造 LLM 审计请求并执行；
- Then：所有 source 文本按数据隔离传入显式数据边界，tools/外部 URL/隐式网络均禁用；provider 输出只按 `wiki-validation/v1` schema 解析，claim ID、target ID、quote hash 二次校验后才保存；
- 失败时不变量：provider 输出不能改变 canonical、状态、发布或引用；不能新增 target、URL 或文件路径；模型正文里的任何指令都不得改变门禁判定；
- 自动化级别：Security/Unit/Integration。

## Provider timeout 兼容性增量证据（2026-08-27）

- `tests/validation/test_provider.py::test_agent_cli_timeout_maps_to_context_exceeded_without_pid_attribute` 注入标准库 `TimeoutExpired`（无 pid 属性），验证 Agent CLI adapter 返回 `context_exceeded`，并以 best-effort 方式执行进程组清理，不产生未捕获异常或伪造 fail。

- `tests/validation/test_audit.py::AuditTests::test_provider_timeout_exception_is_normalized_to_not_run` 验证注入 provider 直接抛出 `TimeoutError` 时，编排层仍写入结构化 `not_run/context_exceeded`，不把 provider 实现异常暴露为审计结论。
