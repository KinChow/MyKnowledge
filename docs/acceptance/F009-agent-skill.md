# F009 Agent Skill 受控读写验收

- Feature：F009
- 相关规范：SKILL、OPS、SEC
- 状态：Implemented（2026-08-28；canonical Skill 基础契约，完整运行验收待补）
- 实现证据：`skills/myknowledge/SKILL.md`、`tests/test_skill_contract.py`
- 当前边界：已接入离线受控 runtime（action 白名单与 writer 委托）；尚未接入完整 source/wiki/publish/query API 调用、token 生命周期和 MCP server transport。

## 练习评分路由增量证据（2026-08-27）

## Action schema 增量证据（2026-08-27）

- `tools.skill_runtime.dispatch` 为每个受控 action 建立显式字段白名单；`tests/test_skill_runtime.py::test_skill_runtime_rejects_unknown_and_dangerous_actions` 验证 query 携带未审计 `provider_url` 时返回 `skill_payload_unknown_field`，不会进入 Retriever 或 provider。
- 该边界复用 MCP Python SDK 的结构化 tool input 思路（MIT）；Skill 仍保留 MyKnowledge 自己的 writer、Vault、confirmation 和 public leak 门禁。

- `tests/test_skill_runtime.py::test_skill_question_answer_preserves_scoring_mode_boundary` 验证 Skill 入口透传 `manual`/`deterministic`/`llm` 评分模式，并拒绝未知模式；实际评分仍由 `QuestionStore` 执行，Skill 不创建 provider、不直接写入 practice 文件。

## Question create validator 路由增量证据（2026-08-27）

- `tests/test_skill_runtime.py::test_skill_question_create_requires_validator_backed_wiki_path` 验证题目创建必须提供相对 `wiki_path`；Skill 先调用 `WikiValidator` 再委托 `QuestionStore`，缺路径或路径穿越直接拒绝，不能绕过 claim/evidence 绑定。
- `tests/test_skill_runtime.py::test_skill_question_create_delegates_validated_report` 进一步验证合法路径的调用顺序和参数：validator 报告原样传入 QuestionStore，不由 Skill 伪造或替换。

## 本轮证据（2026-08-28）

- AC-F009-001/002/006：`tests/test_skill_runtime.py::test_skill_runtime_write_preview_delegates_to_writer` 和 `test_skill_runtime_apply_requires_explicit_confirmation` 验证 Skill 只能通过现有 writer 生成 preview，Apply 未确认时返回 `awaiting_confirmation` 且工作树不变。
- AC-F009-006/010：`test_skill_runtime_rejects_unknown_and_dangerous_actions` 验证未知 action 和 shell/command 等危险字段返回结构化 `skill_action_not_allowed`/`skill_payload_forbidden`。

这些测试证明的是 runtime 安全边界和委托关系，不等同于 MCP transport、token 生命周期、provider 保密策略或完整发布流程已 Accepted。

## AC-F009-001 Skill 是唯一写入口

- Given：Codex/Claude Code 从当前仓库 `skills/myknowledge/` 加载 MyKnowledge Skill；
- When：执行 source/wiki/query/validate/publish 工作流；
- Then：Skill 只能调用领域 CLI/API，所有写入经过 preview、confirmation、hash 和 writer；
- 失败时不变量：Skill 不直接编辑 Markdown、manifest、queries 或 state。
- 对应测试：`tests/test_skill_contract.py::test_canonical_skill_exists_and_routes_through_tools`；当前状态：通过。

## AC-F009-007 Canonical Skill 来源

- Given：本地不存在外部 Skill 仓库或外部同步副本；
- When：Agent 初始化 MyKnowledge Skill；
- Then：仍可从当前 checkout 的 `skills/myknowledge/` 加载并调用，外部副本不是运行依赖；
- 失败时不变量：不能回退到未审计的同名外部 Skill。
- 对应测试：`tests/test_skill_contract.py::test_canonical_skill_exists_and_routes_through_tools`；当前状态：通过。

## AC-F009-002 Preview 与 Apply 门禁

- Given：存在未确认或 hash 已变化的 operation；
- When：Skill 请求 Apply；
- Then：操作被拒绝并返回阻断原因；确认只绑定当前 operation；
- 失败时不变量：不产生部分写入。

## AC-F009-003 Vault 与保密边界

- Given：多个 Vault、internal source 或 unavailable Vault；
- When：Skill 选择 target 或执行查询/发布；
- Then：必须显式使用稳定 `vault_id`，执行 provider/保密检查，按对象返回 unavailable；
- 其中不可用对象必须返回 `availability: unavailable` 和阻断码 `upstream_unavailable`，不能改写 `evidence_state` 为 missing；
- 失败时不变量：不能跨 Vault 引用或把 internal 投影到 public。

## AC-F009-004 Provider runtime 注入

- Given：Skill runtime 提供或不提供可用 provider；
- When：执行 LLM 规范审计；
- Then：provider 可用时调用并按 `wiki-validation/v1` 校验输出；不可用、超时或输出 malformed 时返回 `validation_state: not_run` + 结构化 `not_run_reason`，不阻断人工审计通道；endpoint、模型和密钥不进入仓库或普通日志。
- 失败时不变量：不做 provider capability 协商；不得把 provider 缺失记为 `fail`；不得把 `not_run` 表述为已验证。
- 自动化级别：Unit/Integration。

## AC-F009-008 Provider 不可用不是审计结论

- Given：provider 不支持结构化输出、无法容纳当前 evidence 上下文、或返回不符合 schema 的响应；
- When：执行 LLM 规范审计；
- Then：一律返回 `validation_state: not_run` 与对应 `not_run_reason`（`provider_unavailable`/`context_exceeded`/`malformed_output`），报告只记录 opaque provider identity 与原因；确定性校验与人工审计不受影响；
- 失败时不变量：不得把接口能力缺失解释为"模型不够聪明"，也不得用不满足契约的响应伪造 `pass`；不得因此阻断发布；
- 自动化级别：Unit/Integration。

## AC-F009-009 Internal 内容的 provider 边界

- Given：Skill 需要审计 internal source；
- When：选择 provider 并执行审计；
- Then：只有满足 runtime 保密策略的 provider 才会被调用；不满足时返回 `validation_state: not_run` + `not_run_reason: provider_unavailable`；
- 失败时不变量：不能把 internal 正文发给不满足保密要求的 provider，不能记录 endpoint/key/完整 prompt 或 response；
- 自动化级别：Security/Integration。

## AC-F009-005 查询契约

- Given：QMD、FTS5 或 LIKE fallback；
- When：Skill 执行 query/read；
- Then：返回统一 QueryResult，并保留 evidence/source 定位和 confidentiality；
- 失败时不变量：查询不触发写入。

## AC-F009-006 错误和审计

- Given：操作失败、被拒绝或需要人工确认；
- When：Skill 返回结果；
- Then：返回 operation_id、错误 code、下一步动作和安全摘要，不返回凭据或敏感正文。

## AC-F009-010 Canonical Skill 文件存在性

- Given：Agent 初始化当前 checkout 的 MyKnowledge 能力；`skills/myknowledge/SKILL.md` 缺失、损坏或试图从未审计的外部同名 Skill 回退；
- When：Skill loader 启动；
- Then：只有当前仓库中通过版本控制的 canonical Skill 可以被加载；缺失或校验失败时返回 `skill_unavailable`，不执行任何写入/发布操作；
- 失败时不变量：不能静默加载外部副本、直接编辑文件或把“Skill 已加载”当作领域功能已实现；
- 自动化级别：Repository/Security。

## AC-F009-011 MCP stdio transport

- Given：MCP client 连接当前 checkout 的 stdio server；When：执行 `tools/list` 和 `tools/call`；Then：只暴露结构化 `myknowledge_dispatch`，action 仍经过既有白名单和 writer，server 启动时固定 root，payload 不能注入命令或路径；stdio 不可用时返回启动错误而不执行写入。
- 对应测试：`tests/test_skill_runtime.py::test_mcp_server_exposes_one_controlled_tool_bound_to_checkout`；当前状态：通过（官方 `mcp==1.29.1`）。

## AC-F009-012 Public query/read projection 路由

- Given：public manifest 同时包含 published/public 与 private、draft 或未发布条目；When：Skill 执行 `query`/`read`；Then：只读取 public allowlist，返回统一 QueryResult/read result，private/local scope 返回 `skill_public_query_only` 或 `skill_private_read_requires_api`，不扫描任意路径；当前状态：通过 `tests/test_skill_runtime.py::test_skill_public_query_and_read_use_projection_allowlist`。

## 本轮领域路由证据（2026-08-27）

- `tests/test_skill_runtime.py::test_skill_source_preview_and_apply_delegate_to_source_service` 验证 source preview/apply 委托 `SourceIngestor`，未确认时保持 `awaiting_confirmation`，确认后才写入。
- `tests/test_skill_runtime.py::test_skill_wiki_validate_and_publish_preview_are_domain_only` 验证 wiki 校验和 publish preview 委托 `WikiValidator`，路径越界返回 `path_invalid`，发布预览不会直接编辑 Markdown。
- F009 仍为 Implemented（部分）：token 生命周期、完整 publish confirmation、provider capability 和全量 API parity 尚未闭合。

## MCP capability 增量证据（2026-08-30）

- `create_server(..., capability_token=...)` 对写入、校验、备份和练习 action 启用恒时 token 校验；public query/read 在未配置 token 时仍可运行。
- `tests/test_skill_runtime.py::test_mcp_server_enforces_configured_capability_for_sensitive_actions` 验证敏感 action 缺少或使用错误 token 时阻断，正确 token 才进入既有 writer。该边界不替代 operation confirmation/hash 门禁。

## 真实 stdio transport 增量证据（2026-08-30）

- `tests/test_skill_runtime.py::test_mcp_stdio_transport_lists_and_calls_controlled_tool` 使用官方 SDK `ClientSession`/`stdio_client` 启动真实 `tools.mcp_server` 子进程，验证 `tools/list` 只暴露 `myknowledge_dispatch`，`tools/call` 缺少 token 返回 `capability_token_invalid`，正确 token 仅生成 preview、不会直接写入 checkout。

## Canonical Skill runtime 门禁证据（2026-08-27）

- `tests/test_skill_runtime.py::test_skill_status_is_fail_closed_for_canonical_skill` 验证当前 checkout 缺少或损坏 `skills/myknowledge/SKILL.md` 时返回 `skill_unavailable`，合法 canonical 文件才返回 `skill-status/v1/available`。
- `skill_status` 为只读检查，不从外部副本回退，也不触发任何写入、发布或 provider 调用。

## 只读 retrieve/backlinks 增量证据（2026-08-30）

- `tests/test_skill_runtime.py::test_skill_retrieve_and_backlinks_are_projection_only` 验证 `retrieve` 与 `query` 共享 `query-result/v1`/Retriever，`backlinks` 只从 public projection 声明的条目计算；private vault 请求返回 `skill_private_read_requires_api`，不会扫描或写入 canonical 内容。
- 该证据增强 AC-F009-005/012 的只读路由边界；完整 publish confirmation、token 生命周期和全量 API parity 仍待闭合。
