# F005 Public/Local 索引与检索验收

- Feature：F005
- 相关规范：IDX、SEC
- 状态：Implemented（2026-08-27；projection/fallback 基础能力，完整 FTS5/QMD 索引验收待补）
- 实现证据：`tools/indexing.py`、`tests/test_indexing.py`

## AC-F005-001 Projection 隔离与可重建

- Given：同时存在 public、private、draft、unavailable 和 deprecated 对象；
- When：生成 public/local index；
- Then：public 只包含 `public_publishable`，local 只包含允许读取的可用对象并保留 `vault_id`；索引带输入 hash 和 schema version；
- 失败时不变量：索引失败保留上一版索引，不产生半成品。
- 对应测试：`tests/test_indexing.py::IndexingTests::test_public_projection_filters_private`；当前状态：通过。

## AC-F005-002 检索 fallback 契约

- Given：QMD、SQLite FTS5 或 LIKE fallback 依次可用/不可用；
- When：执行相同查询；
- Then：按 QMD → FTS5 → LIKE 顺序降级，返回相同 QueryResult schema，并明确 `degraded` 状态；
- 失败时不变量：检索降级不改变 Wiki 状态和发布门禁。

## AC-F005-003 结果可追溯

- Given：检索命中 Wiki、Source 或 evidence；
- When：读取结果；
- Then：返回稳定 `object_ref={vault_id, object_type, object_id}`、content hash 和可定位的 source/evidence 引用；public 结果不包含 private 元数据。
- 失败时不变量：同 snapshot 物理去重、同名对象或 QMD 候选都不能丢失 owner、availability 或 hash；无法解析的候选必须丢弃并记录 warning。
- 自动化级别：Unit/Integration。

## AC-F005-004 Archive/RAG 投影边界

- Given：local/private projection 同时包含 source/wiki 和 archive snapshot，public projection 只包含 public Wiki；
- When：生成 FTS5/QMD/LIKE 索引；
- Then：archive 只有在 local/private policy 明确允许时进入本地 RAG，并始终保留 owner/hash；public Pagefind 和 public index 不含 archive；
- 失败时不变量：不能把 RAG chunk 当成 evidence，也不能把 internal archive 送入 public index/cache；
- 自动化级别：Security/Integration。

## AC-F005-005 unavailable 元数据不伪造正文

- Given：local projection 中存在 Vault unavailable、revision mismatch 或冲突对象；
- When：生成索引并执行精确 read、backlink 和关键词查询；
- Then：索引保留 owner、hash、availability/原因元数据但不生成正文 chunk；read 返回结构化 unavailable，搜索不把空正文当命中；
- 失败时不变量：不能把故障对象当成不存在、把同名对象或同 hash 的另一 owner 代替，或将 unavailable 内容送入 RAG/public cache；
- 自动化级别：Unit/Integration/Security。

## AC-F005-006 查询资源、QMD cache 与网络边界

- Given：查询包含未知字段、超长文本、超大 `top_k`/Vault 列表，或 QMD cache 位于非 `0700` 目录、尝试联网或写入 canonical；
- When：执行 QMD/FTS5/LIKE 路由；
- Then：请求超限返回 `query_limit_exceeded`/`request_too_large`；QMD 仅读取 local projection，在权限为 `0700` 的本机 cache 中运行且 network-disabled；不满足条件时降级到 FTS5/LIKE，并保留统一 QueryResult；
- 失败时不变量：不能静默截断、扩大 scope、把 QMD 结果写回 canonical 或把 cache/内部正文提交到 public Git；
- 自动化级别：Unit/Security/Integration。
- 对应测试：`tests/test_indexing.py::IndexingTests::test_fallback_search_and_limits`；当前状态：基础 fallback 通过。
