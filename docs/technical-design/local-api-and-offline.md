# FastAPI 本地服务与离线降级实现设计

- 状态：Implemented（2026-08-28；FastAPI retrieve/query/ask 基础运行面）
- 相关 Feature：F006
- 相关规范：API、IDX、SEC
- 相关 ADR：ADR-0006、ADR-0007
- 相关验收：[F006](../acceptance/F006-local-api-and-offline.md)

## 本轮成熟方案调查（F006-2026-08-28）

- FastAPI 0.115+（<https://github.com/fastapi/fastapi>，MIT）与 Pydantic v2：直接复用请求模型、字段约束和 OpenAPI 路由；限制是它不提供内容授权或 token 生命周期，因此 scope/capability 仍由本地 adapter 管理。
- Starlette TestClient（<https://www.starlette.io/testclient/>，BSD-3-Clause）作为同步集成测试入口，直接复用 HTTP 层行为；限制是仅覆盖进程内服务，不替代真实 loopback/Origin/Host 安全测试。
- 替代基线：直接使用 Python `http.server`（PSF License）可减少依赖，但缺少 Pydantic 校验、统一错误和 ASGI 测试生态，本轮不采用。

API 只做本地 adapter，领域检索委托 `tools.indexing.Retriever`；对象 read/backlinks 只解析显式 `vault_id`，并复用 `safe_id`。当服务由显式 `root` 启动且未注入测试 token 时，启动会原子轮换 `state/capability-token`，设置目录 0700、文件 0600；token 只保存在进程状态和受保护文件，旧进程 token 不再接受。POST/写请求还由 Starlette middleware 校验 loopback Host/Origin，跨站请求在 capability 之前拒绝。外部依赖离线可安装后不需要网络调用；升级 FastAPI/Pydantic 可能改变校验/错误细节，需重新跑 API 契约测试。token、正文和私有路径不交给框架日志，能力边界由 MyKnowledge 保留。

本轮写入 API 调查（2026-08-27）：FastAPI 0.115+（MIT，<https://github.com/fastapi/fastapi>）与 Pydantic 2.x（MIT，<https://github.com/pydantic/pydantic>）复用类型约束、`extra=forbid` 和 OpenAPI schema；Starlette 0.48+ TestClient（BSD-3-Clause，<https://github.com/encode/starlette>）作为同步契约测试。替代方案为直接暴露 `http.server`/手写 JSON 解析，无法提供同等 schema 拒绝和 ASGI middleware 边界，明确不采用。新增 source/wiki preview、operation apply、vault check 只委托现有 `WriteOperation`/`VaultRegistry`，不在 API 层直接编辑 canonical Markdown；SDK 离线安装后运行不需要网络，升级需重跑 API 与安全测试。Capability token 可选校验固定 audience `myknowledge-local-api`，错误 audience fail-closed，scope 仍由本地 adapter 管理。

本轮请求体门禁调查（2026-08-27）：Starlette middleware（BSD-3-Clause，<https://github.com/encode/starlette>）提供请求头/流式边界钩子，FastAPI 保持统一错误响应；替代方案是依赖业务 Pydantic `max_length`，无法阻止超大 JSON 在解析前消耗内存，因此不采用。当前 API 在 middleware 读取 `Content-Length`，超过 1 MiB 返回 `request_too_large`，并对无该头的 chunked 请求按 chunk 有界计数；未超限 body 缓存后交给下游，超限请求不执行 capability、解析或写入。升级 Starlette/FastAPI 后需重跑流式门禁测试。

本轮启动加载调查（2026-08-30）：Astro/Starlight 的 content collection 与 Pagefind 均以构建期生成物作为只读输入；API 复用同一 `queries/public/manifest.json` projection contract。替代方案是启动时扫描 `wiki/` 或接受任意客户端传入文件路径，会绕过 public allowlist 和 leak gate，明确排除。`create_app(root=...)` 在未注入测试数据时仅加载 schema/projection 正确的 public manifest；manifest 缺失或非法时返回空但可诊断的离线检索，不读取 canonical/private/practice。

citation replay 复用 W3C Web Annotation 的 TextQuote/TextPosition 语义（<https://www.w3.org/TR/annotation-model/>，W3C Recommendation）：`tools.citation.replay` 只读校验 snapshot、Unicode 半开区间、exact 与 hash，不将模型返回的标题/URL 当作证据。替代方案是仅信任模型引用，无法抵抗正文漂移，明确不采用。

## 目标与边界

FastAPI 是本机 adapter，不是第二个内容真相源。它读取 Vault Registry、canonical projection 和索引，写入只能提交 operation preview/apply；不提供公网监听、账号系统或服务端权限继承。

## 接口

`POST /api/retrieve` 是结构化检索的规范接口；`GET /api/query` 是为浏览器、旧 CLI 和书签保留的兼容别名。两者必须进入同一个领域函数、使用同一请求归一化和 `query-result/v1` 响应，不能各自维护一套排序、权限或降级逻辑。

最小接口：

```text
GET  /api/health
GET  /api/query?q=&scope=public|local|private&vault_ids=&top_k=
GET  /api/read/{vault_id}/{object_type}/{object_id}
GET  /api/backlinks/{vault_id}/{object_type}/{object_id}
POST /api/source/preview
POST /api/wiki/preview
POST /api/operation/{operation_id}/apply
POST /api/validate/{vault_id}/{object_type}/{object_id}
GET  /api/vault/check
POST /api/retrieve
POST /api/ask
POST /api/citation/replay
```

### 规范化请求

```json
{
  "query": "Transformer attention",
  "scope": "local",
  "vault_ids": ["public", "team-internal"],
  "top_k": 8,
  "include_sources": true,
  "include_archive": false
}
```

`POST /api/retrieve` 只接受 `query`、`scope`、可选 `vault_ids`、`top_k`、`include_sources` 和 `include_archive`；未知字段拒绝。`GET /api/query` 将 `q` 映射为 `query`，逗号分隔的 `vault_ids` 映射为数组，其余参数按相同上限解析，然后调用完全相同的 `RetrieveRequest`。GET 别名不允许写入、provider 调用或改变查询范围；不能把 `projection` 当作 scope，也不能保留历史 `scope=wiki` 别名。

资源上限由 `config/policy.yaml` 固定：`query` 最多 `max_query_chars`，`top_k` 不得超过 `max_top_k`，`vault_ids` 不得超过 `max_vault_ids`，单条 snippet 不超过 `max_result_snippet_chars`，单次请求不得超过 `max_request_body_bytes`，后端检索超过 `request_timeout_seconds` 必须返回可诊断的降级/错误结果。超限使用 `query_limit_exceeded` 或 `request_too_large`，不能静默截断查询或扩大权限。

`POST /api/ask` 使用相同的 `scope`/`vault_ids`/`top_k` 请求部分，但返回独立的 `ask-result/v1`：`answer`、`citations[]`、完整 `retrieval` QueryResult、`availability`、`availability_reason`、`confidentiality`、`limits` 和 `warnings`。`AskResult.citations[]` 必须能回到 `QueryItem.object_ref` 和 snapshot/locator；生成答案不能写 canonical、验证状态、发布状态或共享缓存。没有 LLM 或引用校验能力时返回 `availability: unavailable` 和具体原因，不能把检索片段冒充生成答案。

Ask 的 `answer` 在不可用或冲突时为 `null`；每个 citation 必须符合 `citation/v1`，包含 `object_ref`、匹配检索 item 的 `content_sha256` 和 `citation-locator/v1` 的 `locator`。locator 可以从 source/evidence 记录间接引用，也可以内嵌 `TextQuoteSelector`/`TextPositionSelector`，但最终都必须解析到同一 owner Vault 的不可变 `snapshot_sha256`。重放顺序固定为：按完整 ObjectRef 解析对象 -> 按 owner Vault 解压 snapshot -> 重新校验 snapshot hash -> 在同一 normalization version 下验证 quote exact 和 position 的 Unicode code-point 半开区间 -> 校验 `selector_sha256`（若存在）。缺少 snapshot、selector、owner 或 exact 匹配时 citation 无效，不能只返回模型生成的标题、URL 或未绑定的文本片段；近似匹配只能生成重新锚定建议。

检索响应严格按 `query-result/v1` 返回：顶层必须包含 `schema_version`、`items`、`scope`、`method`、`index_version`、`generated_from`、`availability`、`availability_reason`、`degraded`、`confidentiality_max`、`limits` 和 `warnings`；每个 item 必须包含 `object_ref`、`availability`、`availability_reason`、`confidentiality` 和 `content_sha256`（已知 hash 不得因 unavailable 而清空）。混合可用性按索引设计中的固定聚合规则处理，不得把受影响对象静默过滤成“未找到”。写操作响应另使用 operation 契约，才包含 `operation_id`；不能把写操作字段强行塞进 QueryResult。`POST /api/ask` 使用独立的 `ask-result/v1`，顶层包含 `schema_version`、`answer`、`citations`、`retrieval`（完整 QueryResult）、`availability`、`availability_reason`、`confidentiality`、`limits` 和 `warnings`。错误还必须包含 `code`、`stage`、`retryable` 和 `next_action`。对象读取和写入路径必须显式包含 `vault_id`，因为不同 Vault 可以拥有同名 `object_id`；public scope 可提供兼容的省略形式，但只解析保留的 `public` Vault。`local`/`private` scope 缺少 `vault_id` 时只允许查询，不允许单对象 read/backlinks 以 manifest 顺序猜测 owner。写接口拒绝调用方提供的派生字段和物理路径；`target_vault` 必须是 operation 字段。

只读不等于无授权：绑定 loopback 只限制网络位置，不自动授予读取 internal 内容的权限。`GET /api/query`、`GET /api/read` 和 `GET /api/backlinks` 仅在 `scope=public`（或兼容的 public object 路径）允许匿名；请求 `scope=local|private`、`vault_id != public` 或读取 internal object 时必须携带 `X-MyKnowledge-Capability`。`GET /api/vault/check` 无论 scope 都要求 capability token，因为它会暴露挂载状态、revision、冲突和备份可用性；`GET /api/health` 只返回脱敏进程/schema 状态，可匿名。token 缺失、错误或 scope 不匹配分别返回 `capability_token_required`/`capability_token_invalid`，不能通过 GET 别名绕过。

`scope=private` 要求调用方显式列出一个或多个 internal vault；`scope=local` 才允许默认使用全部当前可用 vault。任一 unavailable/conflict 对象都作为结构化 item/limit 返回，不伪装为“未找到”；不可用对象不返回正文。统一错误码至少包括 `schema_invalid`、`query_limit_exceeded`、`request_too_large`、`vault_unavailable`、`cross_vault_reference`、`hash_mismatch`、`confirmation_required`、`provider_unavailable`、`index_unavailable`、`leak_gate_failed`、`capability_token_required` 和 `operation_blocked`。

默认只绑定 `127.0.0.1`，启动时检查 root、Vault Registry 和 schema version。服务启动时生成至少 32 字节的随机 bearer token，先以 `O_CREAT|O_EXCL` 创建 `state/capability-token`，父目录权限为 `0700`、token 文件权限为 `0600`，再通过原子替换完成轮换；每次进程启动都轮换，旧 token 即使文件残留也必须失效，优雅退出时尽力删除。token 不含 endpoint、模型、密钥或正文；服务只在受保护的进程环境/继承 FD 中交给 Skill/CLI，绝不提供 HTTP 获取端点。每个请求还要校验固定 audience `myknowledge-local-api`、调用方所需 scope（`local-read`、`private-read`、`vault-check`、`write`）和 token 有效期/进程实例，token 比较使用恒定时间算法。所有 POST 端点（包括 `/api/retrieve`、`/api/ask`、验证、索引和 preview/apply）都要求 token；token 缺失返回 `capability_token_required`，错误、旧进程 token 或 scope/audience 不匹配返回 `capability_token_invalid`。token 不得出现在 URL、Cookie、浏览器 localStorage、仓库、审计或日志。服务必须校验 `Origin`/`Host` allowlist、拒绝跨站写请求并限制请求体大小；只有 public scope 的兼容 GET 读取可匿名访问。除非未来单独评审，否则不允许 remote bind；需要 Unix socket 也必须保持同一 token/文件权限门禁。日志禁止凭据、selector exact、private path 和敏感正文。

## 离线行为

本轮网络启动方案调查（2026-08-30）：Uvicorn 0.35.x（BSD-3-Clause，<https://www.uvicorn.org/>）是 FastAPI 官方文档推荐的轻量 ASGI 进程启动器，支持显式 `host/port`、优雅 shutdown 和应用工厂；Hypercorn 0.17.x（MIT，<https://github.com/pgjones/hypercorn>）作为替代方案支持更多 HTTP/2/QUIC 能力，但会扩大运行时配置和协议面。本项目直接复用 Uvicorn 的 ASGI runner，不启用 reload、远程 bind 或 proxy headers；`python -m backend.server` 固定默认 `127.0.0.1`，启动前拒绝非 loopback host，仍由 FastAPI 应用工厂生成每次进程轮换的 capability token。真实网络测试只验证 loopback health、public query 和受保护 POST，不能把 TestClient 结果当作网络验收。

无 FastAPI 时，`tools/query.py` 直接读取 `queries/public` 和静态 catalog，支持 public 浏览、精确查询和确定性搜索。QMD、FTS5、LLM validation、local index 或写入能力不可用时必须返回明确 `unavailable`/`degraded`，不得伪造成功。`/api/retrieve` 的请求 scope 必须使用 `public`/`local`/`private`，不能使用未定义的 `wiki` 别名；`/api/ask` 依赖 RAG/LLM，离线时必须返回 `unavailable`，不能把普通关键词命中伪装成生成式回答。local-file source 的导入仍可由 CLI 在无网络时执行，因为证据载体已在本机。

## 一致性与测试

CLI 和 API 共用领域函数和 QueryResult schema；测试覆盖 GET 别名与 POST 规范接口的逐字段等价、请求字段/长度/top_k/Vault 数量限制、QMD cache 权限和 network-disabled 约束、后端崩溃、旧索引保留、未授权绑定地址、token 文件权限/进程启动轮换/旧 token 失效/错误 scope、缺失/错误 capability token、跨站写请求、private scope 隔离、unavailable 元数据不泄漏正文、citation snapshot 解压重放与 selector hash 校验、preview 不改工作树和 operation hash 失效。
