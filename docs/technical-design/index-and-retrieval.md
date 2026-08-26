# Public/Local 索引与检索实现设计

- 状态：Implemented（2026-08-29；projection 隔离、SQLite FTS5 与 deterministic fallback）
- 相关 Feature：F005
- 相关规范：IDX、SEC
- 相关 ADR：ADR-0007
- 相关验收：[F005](../acceptance/F005-index-and-retrieval.md)

## 目标与边界

本轮成熟方案调查（2026-08-29）：SQLite FTS5 官方 BM25/highlight/external-content 设计（<https://www.sqlite.org/fts5.html>，public domain）用于持久确定性索引；QMD 2.8.3（<https://github.com/tobi/qmd>，MIT）作为本地 BM25/vector/RRF 默认适配器；SQLite/LIKE 纯文本扫描零依赖但排序和规模能力有限，只作为最终 fallback。实现直接复用 FTS5 external-content + BM25，记录 index scope 防止跨 scope 复用；QMD 缺失不会伪装成成功。

本设计实现 public/local projection 的可重建索引，以及 QMD → SQLite FTS5 → deterministic LIKE 的只读检索链。当前 `Retriever` 在存在同 scope 的 SQLite 索引时实际走 FTS5，并以 `qmd_unavailable` 标记降级；索引缺失、scope 不匹配或损坏时回退 LIKE。QMD 的向量、rerank 和模型缓存能力是运行时可选项；第一阶段不要求自有 Embedding/FAISS/HybridRetriever。索引不是内容真相源，不能计算验证状态、改变发布状态或跨 Vault 放宽权限。

`QMDAdapter` 在调用前检查可执行程序、cache 本地目录、0700 权限及不位于 Git 工作树；检查失败返回 `provider_unavailable`/`cache_permissions`/`cache_in_git`，不下载、不联网，继续 FTS5/LIKE。

本轮 unavailable 元数据调查（2026-08-27）：SQLite FTS5 external-content（Public Domain，<https://sqlite.org/fts5.html>）允许索引可检索 metadata 与独立正文列；QMD 2.8.3（MIT，<https://github.com/tobi/qmd>）同样将状态/正文作为不同字段。替代方案是遇到 Vault 故障直接丢弃记录，会把“不可用”误报为“未找到”，不采用。LIKE fallback 现在可按标题命中 unavailable 对象，返回 owner/hash/status 元数据且 `snippet=null`；不会读取或生成隐藏正文 chunk。升级索引实现需保持 `query-result/v1` 和该隐私边界。

本轮 Registry projection 接入调查（2026-08-30）：SQLite FTS5（SQLite 3.46，Public Domain，<https://sqlite.org/fts5.html>）继续用于离线、事务化和可重建索引；Tantivy 0.22（MIT，<https://github.com/quickwit-oss/tantivy>）作为替代方案，吞吐和分词扩展更强，但会引入 Rust/native 依赖及新的索引格式升级边界。MyKnowledge 当前数据量和 fallback 契约优先选择 FTS5，直接消费 F011 的 `local-projection/v1`；索引层不自行扫描 Vault，也不重新推断 owner。故障 Vault 通过 projection 的状态元数据进入 warnings，正文只来自可用 owner。未来替换 backend 必须保持 `query-result/v1`、projection hash 和同一 confidentiality 边界。

## 数据流

```text
Vault Registry
  -> canonical projection + manifest hash
  -> IndexBuilder
  -> queries/public (入 Git) + queries/local (忽略) + SQLite FTS5
  -> QMD read-only adapter / FTS5 / LIKE
  -> QueryResult
```

每条索引记录至少包含 `object_type`、`object_id`、`vault_id`、`object_ref`、`confidentiality`、`status`、`availability`、`availability_reason`、`content_sha256`、`source_ref`、`generated_from` 和 `schema_version`。其中 `object_ref` 是不可歧义的 `{vault_id, object_type, object_id}`；不同 Vault 的同名对象必须作为不同记录保留。public index 只接受 `vault_id: public` 且 `public_publishable: true` 的 Wiki；local index 保留已挂载且允许本机读取的正文，同时为 unavailable/conflict 对象保留不含正文的状态元数据。

## 检索契约

```python
class SearchScope(TypedDict):
    scope: Literal["public", "local", "private"]  # private = explicitly selected internal vaults
    vault_ids: list[str] | None

class QueryResult(TypedDict):
    schema_version: Literal["query-result/v1"]
    items: list[dict]
    scope: Literal["public", "local", "private"]
    method: Literal["id", "title", "backlinks", "qmd", "fts5", "deterministic-fallback"]
    index_version: str
    generated_from: str
    availability: Literal["available", "unavailable", "conflict", "invalid"]
    availability_reason: str
    degraded: bool
    confidentiality_max: Literal["public", "internal"]
    limits: list[str]
    warnings: list[str]

class QueryItem(TypedDict):
    object_ref: dict  # {vault_id, object_type, object_id}
    title: str | None
    route: str | None
    snippet: str | None
    score: float | None
    availability: Literal["available", "unavailable", "conflict", "invalid"]
    availability_reason: str
    confidentiality: Literal["public", "internal"]
    content_sha256: str | None
    source_ref: str | None

class QueryError(TypedDict):
    code: str
    stage: str
    retryable: bool
    next_action: str

class AskResult(TypedDict):
    schema_version: Literal["ask-result/v1"]
    answer: str | None
    citations: list[dict]
    retrieval: QueryResult
    availability: Literal["available", "unavailable", "conflict", "invalid"]
    availability_reason: str
    confidentiality: Literal["public", "internal"]
    limits: list[str]
    warnings: list[str]
```

`QueryResult.availability` 的聚合是固定规则，不由检索适配器自由解释：索引和请求 scope 都可用时为 `available`；部分对象不可用但仍有可用结果时仍为 `available`，受影响对象必须逐条返回 `availability`/`availability_reason` 并在 `warnings`/`degraded` 中说明；没有可用索引或没有可安全读取的 scope 时为 `unavailable`；冲突导致无法确定 owner/候选时为 `conflict`；请求结构错误直接返回 `QueryError`，不伪造 `invalid` 结果。已知但暂时不可用的对象仍保留 `content_sha256`，只有从未生成 canonical 内容 hash 的对象才允许为 `null`。

`AskResult.answer` 在 `availability: unavailable|conflict` 时必须为 `null`。每个 citation 必须符合 `citation/v1`，至少包含 `object_ref`、与检索 item 相同的 `content_sha256` 和 `citation-locator/v1` 的 `locator`。locator 的四种形式（`source`、`evidence`、`text-quote`、`text-position`）最终都要回放到同一 owner Vault 的不可变 snapshot；selector 必须同时带 `TextQuoteSelector` exact 和 `TextPositionSelector` 的 Unicode code-point 半开区间，按固定 normalization version 校验。检索适配器不能只给自然语言标题、URL 或模型自报的引用；citation 必须能回到本次 `retrieval.items`，再由 resolver 重新解压并验证 snapshot/selector hash。

精确 ID、标题和反向索引优先走确定性直达；自然语言/混合查询按默认链路调用。adapter 返回的每个候选必须带 `vault_id` 和 `object_type`，再从 canonical projection 读取并校验 owner、hash 和状态；无法解析的候选丢弃并记录 warning。

`degraded` 只表示检索实现相对默认链路降级（例如 `qmd` 不可用而使用 `fts5`），不表示内容质量下降，也不改变 Wiki 的 validation/publication 状态。`unavailable` 对象仍可作为无正文状态 item 返回；空正文不能作为普通命中。错误响应使用 `QueryError`，不能把 provider/index/vault 故障包装成空结果或成功回答。

`scope: public` 固定只读取 public allowlist，忽略调用方提供的 private `vault_ids`；`scope: private` 必须显式给出一个或多个 internal `vault_id`，不允许以“全部 private”作为隐式权限；`scope: local` 默认读取当前可用且允许本机读取的 vault，并在结果中逐条报告 `availability`。`projection` 只表示索引生成视图（例如 public/local/private projection），不作为查询请求字段或权限别名。unavailable 对象可以出现在精确 read/backlink 的状态结果中，但不进入正文检索候选；若查询命中其 metadata，返回 `availability: unavailable` 和 `limits`，不能返回空正文。`method`、scope 和错误枚举必须与 `/api/retrieve` 和 Agent Skill 共用，QMD 内部使用 BM25/向量/RRF 仍统一报告为 `qmd`。

查询入口必须先执行 policy 资源校验：未知字段、超过 `max_query_chars`/`max_top_k`/`max_vault_ids`、请求体或 timeout 超限直接返回结构化错误，不能静默截断。QMD 运行目录和 cache 必须是本机 `0700`、不在 Git、network-disabled；adapter 在启动和每次查询前检查 cache owner/mode 与 manifest hash。检查失败时切换 FTS5/LIKE，并在 `limits`/`warnings` 记录原因。QMD、FTS5 和 LIKE 都只能读取投影，不能写 canonical、audit 或共享回答缓存。

## 生成与失效

IndexBuilder 使用输入集合 hash、policy version 和 schema version 作为 manifest；先写临时目录和临时 SQLite 事务，校验数量、唯一 ID、owner 和 hash 后原子替换。失败时保留上一版 index。内容 hash 变化增量更新，Vault registry hash 变化时所有相关索引失效并重建。

QMD 只读取隔离的 local projection，固定版本和运行模式；不写 canonical 文件，不上传 internal 内容。归档正文只有在 local/private policy 明确 `include_archive: true` 且 owner vault 可用时才进入本地 RAG projection，public projection 永不包含 archive。QMD 不可用、Node/模型缺失、cache 权限不正确、超时、输出 schema 不兼容或权限校验失败时切换 FTS5，再切换 LIKE，并在 `degraded`/`limits` 中说明。第一阶段不生成自有向量文件；未来的向量 adapter 必须单独声明模型/索引版本和重建一致性。

## 安全与测试

查询 scope 不能绕过冲突、unavailable、confidentiality 或 cross-vault reference。测试覆盖 projection 隔离、两种 Vault、ID 冲突、相同 snapshot 的 owner 保留、QMD/FTS5/LIKE fallback、索引损坏恢复和结果可追溯。
