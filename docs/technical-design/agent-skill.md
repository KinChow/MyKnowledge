# Agent Skill 受控读写实现设计

- 状态：Implemented（2026-08-28；canonical Skill 与路由边界已落地）
- 相关 Feature：F009
- 相关规范：SKILL、OPS、SEC、IDX
- 相关 ADR：ADR-0006、ADR-0007
- 相关验收：[F009](../acceptance/F009-agent-skill.md)

## Canonical 位置

本轮成熟方案调查：参考 MCP Python SDK 的 tool/resource/stdio 分层（https://github.com/modelcontextprotocol/python-sdk）和仓库现有受控 Skill 的 front matter + 运行规则；本地 canonical Skill 只做路由与安全约束，不复制领域写入实现。

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
