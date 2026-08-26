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

本轮查询路由调查（2026-08-27）：Pagefind 1.4（MIT，<https://github.com/CloudCannon/pagefind>）和 SQLite FTS5（Public Domain，<https://sqlite.org/fts5.html>）分别作为 public build/search 与本地 fallback；替代方案是 Skill 直接扫描任意 checkout 路径，会绕过 projection allowlist 和 confidentiality 门禁，明确排除。`query`/`read` action 只加载 public manifest 声明的 published/public 条目，local/private 必须转 API 并提供 capability；结果复用 `query-result/v1`，不写入 canonical 或索引。

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
