# F006 FastAPI 本地服务与离线降级验收

- Feature：F006
- 相关规范：API、IDX、SEC
- 状态：Implemented（2026-08-28；retrieve/query/ask/read/backlinks 基础能力，完整 API 验收待补）
- 实现证据：`backend/app.py`、`tests/test_api.py`、`requirements.txt`
- 当前边界：read/backlinks/source/wiki preview/apply、token 生命周期、Origin/Host、citation replay 和完整 offline integration 尚未完成。

## AC-F006-001 API 与 CLI 一致

- Given：同一 public/local projection；
- When：通过 FastAPI 和离线 CLI 查询；
- Then：两者返回相同 QueryResult、状态和引用边界；
- 失败时不变量：API 不直接修改 canonical Markdown。
- 对应测试：`tests/test_api.py::test_get_post_query_equivalent`；当前状态：通过。

## AC-F006-002 后端不可用时降级

- Given：FastAPI、LLM 或 private vault 不可用；
- When：访问 public 静态站或离线查询；
- Then：public 浏览、搜索和图谱仍可用；受影响的写入、验证或 local 能力返回明确 `unavailable`；
- 失败时不变量：不得伪造验证通过或写入成功。
- 对应测试：`tests/test_api.py::test_ask_is_explicitly_unavailable_offline`；当前状态：通过。

## AC-F006-003 同名对象的显式 Vault 路由

- Given：两个 private vault 各有相同 `object_id` 的 Wiki；
- When：通过 API 和离线 CLI 读取、查询或查看 backlinks；
- Then：local 路由必须显式带 `vault_id`，返回 `object_ref` 与 owner 一致；public scope 只解析 `public` vault；
- 失败时不变量：不得按 manifest 顺序返回错误对象或泄漏另一 vault 的 metadata；
- 自动化级别：Unit/Integration。

## AC-F006-004 生成式问答离线边界

- Given：`/api/ask` 所需的 LLM、QMD 或 local index 不可用；
- When：请求 ask/retrieve；
- Then：`/api/retrieve` 可按 fallback 返回确定性结果，`/api/ask` 返回 `unavailable` 或明确 `degraded`，不声称已生成基于知识库的回答；
- 失败时不变量：不写入 canonical 内容、不改变验证或发布状态；
- 自动化级别：Integration。

## AC-F006-005 scope、错误和方法契约

- Given：请求分别使用 `public`、`local`、`private` scope，或省略/伪造 `vault_id`、使用未知 `scope: wiki`；
- When：调用 query/read/retrieve/ask/backlinks；
- Then：API、CLI 和 Skill 返回同一 QueryResult/错误 schema；private scope 要求显式 Vault，未知 scope 或跨 Vault owner 返回结构化错误，不按 manifest 顺序猜测；
- 失败时不变量：错误响应不泄漏 private path/正文/凭据，降级 method 不伪装为 qmd/hybrid；
- 自动化级别：Unit/Integration/Security。
- 对应测试：`tests/test_api.py::test_private_scope_requires_capability`；当前状态：通过基础 token 门。

## 新增本轮证据（2026-08-28）

- AC-F006-003：`test_public_read_and_backlinks` 验证显式 `public/wiki/object_id` 路由、正文读取和 backlinks owner；`test_read_missing_object_is_structured_404` 验证 `object_not_found` 结构化错误。通过基础 public 场景。
- AC-F006-005/008：`test_non_public_read_requires_capability_even_when_vault_unavailable` 验证 local read 缺 token 返回 401，携带 token 后返回 `vault_unavailable` 而非猜测 owner。通过基础授权边界。
- AC-F006-003/006：`test_object_route_rejects_path_traversal_and_unknown_type` 验证非法 object id 返回 422、未知 object type 不解析为 source。通过路径安全基础场景。

以上证据不代表 token 生命周期、Origin/Host、private vault 实体读取、citation replay 或写入端点已完成；这些场景仍保持待补状态。

## Token 生命周期增量证据（2026-08-30）

- AC-F006-009：`tests/test_api.py::test_capability_token_rotates_with_secure_permissions` 验证服务启动写入 token 文件，`state/` 权限为 0700、token 文件为 0600，连续启动生成不同 token，旧 token 返回 `403 capability_token_invalid`。
- 测试注入的固定 token 仅用于进程内 fixture；生产式显式 root 启动路径使用随机 token 文件，不提供 HTTP 获取端点。

Origin/Host allowlist、audience/scope token registry、优雅退出清理和 citation replay 仍待后续验收。

## Origin/Host 增量证据（2026-08-30）

- AC-F006-006/008：`tests/test_api.py::test_cross_origin_post_is_rejected_before_capability_check` 和 `test_non_loopback_host_is_rejected` 验证跨站 Origin、非 loopback Host 在 capability 校验前分别返回 `origin_not_allowed`/`host_not_allowed`。
- AC-F006-007：`tests/test_api.py::test_retrieve_enforces_policy_vault_limit` 验证超过 policy `max_vault_ids=16` 返回 `query_limit_exceeded`，不静默截断。

## 流式请求体门禁证据（2026-08-27）

- Starlette middleware 在缺失 `Content-Length` 的 chunked 请求上按 chunk 累加 body，超过 1 MiB 返回 `request_too_large`；未超限 body 才交给 FastAPI/Pydantic handler。
- 该门禁与 Content-Length 快速路径共用同一上限，不执行 capability、解析或写入超限请求；API 回归 17 项通过。真实网络服务器上的 chunked 压测仍需部署环境验收。

## Citation replay 增量证据（2026-08-30）

- AC-F006-010：`tests/test_citation.py::test_citation_replay_uses_unicode_codepoint_offsets` 验证 emoji/CJK 场景的 Unicode code-point offset 与 TextQuote/TextPosition replay。
- `test_citation_replay_rejects_snapshot_and_selector_drift` 验证 snapshot hash 漂移和 selector exact 变化分别返回 `snapshot_hash_mismatch`/`selector_unresolved`。

## AC-F006-006 本机 API 写保护

- Given：本机页面、未授权脚本或远程客户端请求 write/validate/index/publish POST 端点；
- When：缺少、伪造或跨 Origin 使用 capability token；
- Then：返回 `capability_token_required`/`capability_token_invalid`，canonical 文件、索引、状态和 provider 调用均不变；
- 失败时不变量：不能因为监听在 loopback 就允许跨站写入，token 不得出现在 URL、浏览器存储、仓库或日志；
- 自动化级别：Security/Integration。

## AC-F006-007 Query/retrieve 兼容别名和请求限制

- Given：同一 scope/query 分别通过 `GET /api/query?q=...` 和 `POST /api/retrieve` 请求，并分别使用未知字段、超长 query、过大的 `top_k` 或 Vault 列表；
- When：调用 API、CLI 和 Skill；
- Then：合法请求返回逐字段等价的 `query-result/v1`；GET 只负责参数归一化，不维护独立检索逻辑；非法请求返回 `query_limit_exceeded`/`request_too_large`，不静默截断；
- 失败时不变量：兼容别名不能绕过 capability token、scope/owner 检查、降级标记或错误 schema；
- 自动化级别：Unit/Integration/Security。

## AC-F006-008 Local/private GET 与 vault check 授权边界

- Given：API 绑定 `127.0.0.1`，请求分别读取 `scope=public`、`scope=local/private`、internal object，或调用 `/api/vault/check`；调用方可能缺少、伪造或使用不匹配 scope 的 capability token；
- When：执行 GET query/read/backlinks/vault-check；
- Then：public 只读 GET（以及脱敏 health）可匿名；local/private GET、internal object 和 vault check 必须要求 `X-MyKnowledge-Capability`，缺失/错误分别返回 `capability_token_required`/`capability_token_invalid`；GET 别名不能扩大 scope 或按 manifest 顺序猜 owner；
- 失败时不变量：loopback 位置不能替代内容授权，响应不泄漏 private path、正文、remote 或凭据；
- 自动化级别：Security/Integration。

## AC-F006-009 Capability token 生命周期

- Given：本地 API 连续启动两次，或请求使用上一进程留下的 token；另有 token 文件、父目录权限和错误 audience/scope fixture；
- When：调用 public、local/private、vault check 和写入端点；
- Then：每次启动生成新的随机 token，`state/` 为 `0700`、token 文件为 `0600`，旧 token 失效；缺失、错误、旧进程、audience 或 scope 不匹配分别返回 `capability_token_required`/`capability_token_invalid`；
- 失败时不变量：不存在 HTTP 获取端点，token 不进入 URL、Cookie、浏览器存储、仓库、审计或日志；
- 自动化级别：Security/Integration/Failure injection。

## AC-F006-010 Citation snapshot/selector replay

- Given：AskResult citation 分别使用 source、evidence、TextQuote 和 TextPosition locator，snapshot 以 zstd 物理压缩保存，并准备 hash、Unicode offset、selector hash 错误 fixture；
- When：读取 citation 并重放到 canonical snapshot；
- Then：只有完整 ObjectRef、owner Vault、解压后 snapshot hash、TextQuote exact、TextPosition Unicode code-point 半开区间和 selector hash 均匹配时 citation 有效；缺失、冲突、近似匹配或 hash 错误返回结构化不可用结果；
- 失败时不变量：不能用当前 source Markdown、压缩 blob hash、标题或 URL 替代权威 snapshot/selector，也不能把无效 citation 作为生成答案依据；
- 自动化级别：Unit/Integration/Security。

## AC-F006-011 Source/Wiki preview 与 operation apply

- Given：调用方提交 source 或 wiki 文件变更；When：调用 preview、未确认 apply、确认 apply；Then：缺 capability 被拒绝，preview 只生成 operation/hash 不改工作树，未确认返回 `awaiting_confirmation`，确认后通过同一 writer 原子应用；`GET /api/vault/check` 同样要求 capability。
- 对应测试：`tests/test_api.py::test_source_and_wiki_preview_apply_require_capability_and_confirmation`、`test_vault_check_requires_capability`；当前状态：通过。

## AC-F006-012 Private owner read/backlinks

- Given：两个显式挂载 vault 拥有同名 Wiki；When：携带 capability 调用 `/api/read/{vault_id}` 和 `/api/backlinks/{vault_id}`；Then：只读取指定 owner，返回 vault-relative path 和 owner ObjectRef，public/private scope 不交叉；当前状态：通过 `tests/test_api.py::test_private_vault_read_and_backlinks_are_owner_scoped`。

## AC-F006-013 请求体大小门禁

- Given：请求声明 `Content-Length` 超过 1 MiB；When：调用任意 API；Then：middleware 在 JSON 解析和 capability 处理前返回 413 `request_too_large`，不读取或写入 canonical/state；当前状态：通过 `tests/test_api.py::test_request_body_limit_is_fail_closed`。

## Validate API 增量证据（2026-08-27）

- `tests/test_api.py::test_validate_endpoint_requires_capability_and_reuses_wiki_validator` 验证 `/api/validate/{vault_id}/wiki/{object_id}` 缺 capability 返回 401，授权后按显式 owner 调用 WikiValidator 并返回 `validation-result/v1`。
- API 不复制规则或直接修改 canonical Markdown；非 Wiki object type 返回结构化 `object_type_not_supported`。
