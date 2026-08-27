# Agent Skill 受控读写实现设计

- 状态：Implemented（2026-08-28；canonical Skill 与路由边界已落地）
- 相关 Feature：F009
- 相关规范：SKILL、OPS、SEC、IDX
- 相关 ADR：ADR-0006、ADR-0007
- 相关验收：[F009](../acceptance/F009-agent-skill.md)

## Canonical 位置

本轮成熟方案调查（2026-08-28）：

- MCP Python SDK（<https://github.com/modelcontextprotocol/python-sdk>，MIT，main/2026-08）：复用 tool/resource/stdio 的能力边界设计；限制是 SDK 不替 MyKnowledge 管理 Vault、confirmation 或 public leak policy，因此本轮先落地同样的结构化 action boundary，暂不宣称已接通 MCP transport。
- Claude/Codex tool boundary（MCP specification，<https://modelcontextprotocol.io/specification>，MIT 文档）：复用“工具只能暴露声明能力、参数结构化、错误可诊断”的原则；限制是宿主授权和 token 生命周期属于部署层，仍由本地 runtime 约束。
- 替代方案：直接暴露 shell/脚本调用（Python subprocess）实现面最小，但会允许任意命令、绕过 writer 和审计，故明确不采用。

本轮新增 `tools.skill_runtime.dispatch` 作为离线可测试的受控 adapter：action 白名单、危险字段拒绝、所有写入委托现有领域服务；MCP stdio/HTTP transport 仍是后续工作。依赖均可离线安装，升级 SDK/宿主只影响 transport，不改变领域 operation schema。

本轮 transport 调查（2026-08-27）：官方 MCP Python SDK `mcp==1.29.1`（MIT，<https://github.com/modelcontextprotocol/python-sdk>）的 `FastMCP`/`run_stdio_async` 直接复用标准 `tools/list` 与 `tools/call`，并提供结构化 input/output schema；MCP Specification 2025-06（MIT 文档，<https://modelcontextprotocol.io/specification/2025-06-18>）约束 JSON-RPC、stdio 消息边界和工具声明。替代方案是自研 JSON-RPC loop 或直接暴露 shell，前者增加协议兼容风险，后者绕过 capability/writer，均不采用。`tools/mcp_server.py` 只提供一个 `myknowledge_dispatch` 薄适配器，checkout root 在启动时固定，payload 不得选择路径或命令；SDK 缺失时启动失败为 `mcp_unavailable`，离线运行不需要网络。

本轮 MCP capability 增量调查（2026-08-30）：MCP specification 的 tool-call metadata 与 FastMCP typed arguments（MIT 文档/SDK）适合在 stdio 边界传递短生命周期 capability；替代方案是把 token 放入 action payload 或依赖“stdio 本地即可信”，前者会被领域字段白名单拒绝，后者无法覆盖被转发的敏感 action。`create_server(..., capability_token=...)` 现在对写入、校验、备份和练习 action 做恒时比较；public read/query 仍可在无 token 配置时运行。token 只存在进程参数/环境和 stdio 调用参数，不写仓库或日志。

本轮 token 生命周期调查（2026-08-27）：MCP capability metadata（MIT 文档，<https://modelcontextprotocol.io/specification/2025-06-18>）与 FastAPI bearer-token TTL 实践都要求短生命周期授权；替代静态永久 token 会导致 stdio 进程长期存活时权限无法收回。MCP server 现以进程启动时间作为 token issuance boundary，默认 3600 秒，过期返回 `capability_token_expired` 并要求重启获取新 token；仍使用恒时比较，token 不落盘、不写日志。该 TTL 只影响 transport authorization，不改变领域 confirmation/hash 门禁。

本轮 stdio 集成调查（2026-08-30）：官方 MCP Python SDK `ClientSession` + `stdio_client`（MIT，<https://github.com/modelcontextprotocol/python-sdk>）负责 JSON-RPC 初始化、`tools/list` 和 `tools/call` 消息边界；替代方案是直接向子进程写裸 JSON，无法证明协议握手和错误映射兼容。测试通过真实 `python -m tools.mcp_server` 子进程验证单一受控工具、固定 checkout root 与 capability fail-closed；传输异常不执行写入。

本轮查询路由调查（2026-08-27）：Pagefind 1.4（MIT，<https://github.com/CloudCannon/pagefind>）和 SQLite FTS5（Public Domain，<https://sqlite.org/fts5.html>）分别作为 public build/search 与本地 fallback；替代方案是 Skill 直接扫描任意 checkout 路径，会绕过 projection allowlist 和 confidentiality 门禁，明确排除。`query`/`read` action 只加载 public manifest 声明的 published/public 条目，local/private 必须转 API 并提供 capability；结果复用 `query-result/v1`，不写入 canonical 或索引。新增 source preview/apply、wiki validate、publish preview 均委托既有领域服务，Skill 不复制校验或直接写文件；离线时依赖本地服务与 operation store，外部 provider 不可用只返回结构化 unavailable/not-run。

本轮只读能力扩展调查（2026-08-30）：MCP specification 2025-06 的 `tools/list`/`tools/call` 与工具 annotations（MIT 文档，<https://modelcontextprotocol.io/specification/2025-06-18/server/tools>）要求工具声明结构化输入并由宿主执行授权；Typer commands（MIT，<https://typer.tiangolo.com/tutorial/commands/>）建议子命令只做参数解析并共享领域函数。采用 `retrieve`（与 `query` 共用 Retriever）和 `backlinks`（只消费 public projection 的 body/links）两个只读 action；不允许 Skill 传物理路径、scope 扩权或扫描 canonical/private 目录。替代方案是 Skill 自行遍历 `wiki/`，会绕过 public manifest 和 leak gate，明确排除。离线无网络、无写入；MCP capability 保护规则保持不变。

本轮 publish confirmation 调查（2026-08-27）：MCP typed tool boundary（MIT，<https://modelcontextprotocol.io/specification/2025-06-18/server/tools>）与现有 `release_confirmation.write_event()` 的 append-only nonce/hash 门禁可组合；替代方案是 Skill 直接写 `release/public-confirmations/*.json`，会绕过 schema、人工 actor、reason 脱敏和 nonce 重放保护。新增 `publish_confirm` 仅接收结构化 event 并委托 `write_event`，不生成或修改确认内容；离线运行，token/凭据不落盘，发布 authority 仍归 release confirmation 与 projection generator。

本轮 `ask` 能力调查（2026-08-27）：FastAPI `/api/ask` 的 `RetrieveRequest`/`ask-result/v1`（FastAPI 0.115+、Pydantic 2.x，MIT；<https://github.com/fastapi/fastapi>、<https://github.com/pydantic/pydantic>）提供与 API 一致的 query/scope/top-k 结构，并在 provider 不可用时明确返回 `availability=unavailable`；MCP Python SDK `FastMCP` typed tool（1.29.1，MIT；<https://github.com/modelcontextprotocol/python-sdk>）提供结构化 `tools/call` 边界。直接复用请求字段和 `ask-result/v1` 响应语义，Skill 只调用同一 public projection `Retriever`，不自行生成答案；LLM/provider 仍由 API/独立 provider 层负责。替代方案是 Skill 直接调用 provider URL 或把检索片段伪装成回答，会泄露 endpoint/凭据并破坏 `unavailable` 语义，明确排除。离线运行不联网、不写 canonical/index/practice；升级 FastAPI/MCP 只需重跑 schema/transport 测试，provider 不可用时保持可诊断的 `provider_unavailable`。

Skill 直接位于本仓库 `skills/myknowledge/`，Codex 或 Claude Code 从当前 checkout 加载。Skill 不依赖外部 Skill 仓库；外部同步只能是发布后的复制动作。

## 能力面

Skill 暴露四类当前工作流：

| 能力 | 行为 |
| --- | --- |
| `query/read` | 只读检索和证据定位；规范调用 `POST /api/retrieve`，兼容 `GET /api/query` 但走同一领域函数 |
| `source` | local-file/fetch/personal source preview/apply |
| `wiki` | claim/evidence preview、验证和 apply |
| `publish` | private publish 或 public release preview/人工确认/apply |

Question 工具暂不暴露，留给 F008 的单选、多选和面试简答设计。

每个工具只调用 `tools/` 或 FastAPI 领域接口，不直接打开或写入 Markdown、manifest、queries、state、Git 或 Vault 物理路径。Skill 不自行计算派生状态，不自行选择 `target_vault`。调用本地 API 的所有 POST（包括 retrieve/ask）必须从受保护运行态取得 capability token，并把 token 作为进程间受控凭据传递；Skill 输出和日志不得包含 token、绝对路径、provider endpoint/key 或完整敏感正文。Query request 的长度、`top_k`、Vault 数量和 body 上限由 policy 校验，不能在 Skill 层静默截断或扩大 scope。

## 写入协议

```text
intent -> preview -> show diff/hash/vault/confidentiality/warnings
       -> user confirmation(operation_id)
       -> apply -> recheck registry/hash -> atomic writer
```

`apply` 只接受同一 `operation_id` 和未过期 precondition。public release preview 默认 `public_release: false`，只有人工通过独立 `public-release-confirmation/v1` event（`actor_type: human`、当前 `release_input_sha256` 匹配）才能继续；Agent 不能代替该动作。internal private publish 必须显示 warning，并要求 `operation-confirmation/v1`（`scope: publish_private`）携带 `warning_code` 与 `warning_text_sha256`。

## Provider runtime

Skill runtime 选择 provider 并注入，不把 endpoint、模型版本或密钥写入仓库。按 ADR-0010，LLM 规范审计是可选层，因此不做 provider capability 协商：provider 不可用、上下文放不下当前输入、或返回不符合 `wiki-validation/v1` 的响应时，一律返回 `validation_state: not_run` + 结构化 `not_run_reason`，不阻断确定性校验与人工审计通道。审计一旦运行则必须满足覆盖与举证义务（全 claim 全 target 覆盖、逐条回引 `applied_rule_refs`、rationale 引用原文区间），否则同样记 `not_run: incomplete_coverage`。Source snapshot/wiki/claim 是不可信数据，provider request 禁用 tools、外部 URL 和隐式网络，输出不能触发任何写操作。

## 错误、权限和测试

返回统一错误：`code`、`operation_id`、`vault_id`、`stage`、`retryable`、`next_action`；不得回显敏感正文。所有 durable operation/validation/release 结果必须能通过单条 `record_sha256` 与 target owner 校验；顺序与篡改证据来自 Git 历史，不自建 audit hash chain，`record_sha256` 不匹配返回 `hash_mismatch`。测试覆盖直接文件写入阻断、scope 越权、capability token 缺失/跨站请求、跨 Vault 引用、未确认 apply、hash 失效、provider unavailable、public release false、query/retrieve 等价和 record 篡改。
