# F005 Public/Local 索引与检索验收

- Feature：F005
- 相关规范：IDX、SEC
- 状态：Implemented（2026-08-29；projection/SQLite FTS5/fallback 基础能力，完整恢复验收待补）
- 实现证据：`tools/indexing.py`、`tests/test_indexing.py`
- 修订（ADR-0017，2026-09-15）：QMD 适配器已退役（`tools/indexing.py:411`），降级链为 FTS5（simple/unicode61）→ LIKE。本文件中所有「QMD 待补 / QMD cache / 向量与 RRF 质量」的表述均已失效，保留仅为历史记录；实体检索能力以 FTS5 → LIKE 为准。

## 本轮证据（2026-08-29）

- AC-F005-001/002/006：`tests/test_indexing.py::IndexingTests::test_retriever_prefers_persistent_fts5_when_available` 验证持久索引存在且 scope 匹配时返回 `method: fts5` 且 `warnings: []`、`degraded: false`（FTS5 已是主路径，不是降级路径）。QMD 适配器已退役（`tools/indexing.py:411`，见 ADR-0017），原先的 `qmd_unavailable` 告警已无生产者。
- scope 隔离：SQLite 索引记录自身 scope；不匹配时不读取索引，回退确定性路径，避免 public 查询误读 local/private 内容。

完整 QMD cache 权限、损坏索引保留旧版本和 unavailable 对象状态元数据仍待后续验收。

## 索引替换回滚增量证据（2026-08-30）

- `tests/test_indexing.py::IndexingTests::test_rebuild_swap_failure_restores_previous_index` 注入最终 SQLite 文件替换失败，验证旧主索引自动恢复、仍可读取且没有把失败重建暴露为空索引。

## 索引恢复增量证据（2026-08-30）

- `SQLiteIndex.recover()` 在重建前执行 SQLite `quick_check`、scope 和 projection hash 校验；损坏索引通过原子 rebuild 恢复并保留 `.previous`，有效索引直接返回 `valid`，不重复重建。
- `tests/test_indexing.py::IndexingTests::test_sqlite_index_recover_rebuilds_corrupt_index_and_keeps_previous` 与 `test_sqlite_index_recover_reports_valid_without_rebuild` 覆盖损坏恢复和健康索引路径。
- 该证据增强 AC-F005-001/002 的恢复边界；真实 QMD 安装、向量/RRF 质量与大规模性能仍属于环境验收。

## Public allowlist 收紧增量证据（2026-08-27）

- `tests/test_indexing.py::IndexingTests::test_public_projection_requires_complete_release_allowlist` 验证 public index 同时要求 `vault_id=public`、`public_publishable=true`、`public_release=true`、`status=published` 和有效保密等级 `public`；draft、未确认发布和 internal 条目均被排除。
- 该 allowlist 由 IndexBuilder、SQLite FTS5 rebuild 和 Retriever 共用，避免不同检索路径产生权限不一致；完整真实 QMD/向量质量验收仍待补。

本轮 unavailable 元数据增量证据（2026-08-27）：`tests/test_indexing.py::IndexingTests::test_unavailable_metadata_is_searchable_without_body` 验证 LIKE fallback 可命中 unavailable 标题，返回 `availability_reason: vault_unavailable` 且不返回 snippet/body。

## QMD runtime 增量证据（2026-08-30）

> 已失效（ADR-0017，2026-09-15）：QMD 适配器退役，`IndexingTests::test_qmd_cache_probe_is_fail_closed` 已删除。QMD cache 权限与网络边界不再是本条的验收对象。

## AC-F005-001 Projection 隔离与可重建

- Given：同时存在 public、private、draft、unavailable 和 deprecated 对象；
- When：生成 public/local index；
- Then：public 只包含 `public_publishable`，local 只包含允许读取的可用对象并保留 `vault_id`；索引带输入 hash 和 schema version；
- 失败时不变量：索引失败保留上一版索引，不产生半成品。
- 对应测试：`tests/test_indexing.py::IndexingTests::test_public_projection_filters_private`；当前状态：通过。
- SQLite FTS5 重建与 BM25 查询：`tests/test_indexing.py::IndexingTests::test_sqlite_fts5_rebuild_and_search`；当前状态：通过。

## AC-F005-002 检索 fallback 契约

> 已修订（ADR-0017，2026-09-15）：QMD 适配器已退役，降级链由「QMD → FTS5 → LIKE」变为 **FTS5（simple/unicode61）→ LIKE**；凡本文件提及 `qmd` 的断言均视为历史记录。

## Private scope 隔离增量证据（2026-08-27）

- `tests/test_indexing.py::IndexingTests::test_private_scope_excludes_public_owner` 验证 IndexBuilder 与 Retriever 共用 scope 过滤，`scope=private` 不把 public owner 混入 QMD/FTS5/LIKE 候选；public allowlist 与 private owner 边界在 provider 之前生效。
- `test_vault_allowlist_is_applied_before_retrieval_result_generation` 验证显式 `vault_ids` 在 Retriever 内部过滤，调用方不再依赖检索完成后的结果裁剪来表达 owner 权限。

- Given：SQLite FTS5 或 LIKE fallback 依次可用/不可用；
- When：执行相同查询；
- Then：按 FTS5 → LIKE 顺序降级，返回相同 QueryResult schema，并明确 `degraded` 状态（降级告警为 `fts5_unavailable`/`index_scope_mismatch` 等，不再是 `qmd_unavailable`）；
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

## AC-F005-006 查询资源、缓存与网络边界

> 已修订（ADR-0017，2026-09-15）：原条文包含的 QMD cache（0700、network-disabled）断言随 QMD 适配器退役而失效。存活的不变量是**查询资源上限**与**不写 canonical/不联网**，见下。

- Given：查询包含未知字段、超长文本、超大 `top_k`/Vault 列表；
- When：执行 FTS5/LIKE 路由；
- Then：请求超限返回 `query_limit_exceeded`/`request_too_large`；检索只读取本机 projection（`queries/public`、`queries/local`）与 `state/index/` 下的 SQLite 索引，不联网、不写 canonical；不满足条件时降级到 LIKE，并保留统一 QueryResult；
- 失败时不变量：不能静默截断、扩大 scope、把检索结果写回 canonical 或把 cache/内部正文提交到 public Git；
- 自动化级别：Unit/Security/Integration。
- 对应测试：`tests/test_indexing.py::IndexingTests::test_fallback_search_and_limits`、`::test_retriever_enforces_vault_id_limit_before_provider`；当前状态：基础 fallback 与资源上限通过。

## 本轮 QMD adapter 证据（2026-08-27）

> 已失效（ADR-0017，2026-09-15）：`QMDAdapter` 与 `IndexingTests::test_qmd_results_are_normalized_and_projection_allowlisted` 均已删除，QMD 不再参与检索路由。该节仅作历史记录。

- ~~`tests/test_indexing.py::IndexingTests::test_qmd_results_are_normalized_and_projection_allowlisted` 使用注入式 QMD provider 验证候选结果必须重新映射到当前 projection allowlist，private/未知 owner 不会进入 public QueryResult。~~
- ~~`QMDAdapter.search` 仅调用本地 `qmd search ... --json`，检查 cache 权限和 Git 边界；命令失败、schema 无效或 provider 不可用时继续 FTS5/LIKE，不能伪造 qmd 成功。~~
- 边界：真实 QMD 安装、向量模型和 RRF 质量仍属于环境验收，当前不标记 F005 Accepted。

## 本轮 Registry projection 接入证据（2026-08-30）

- `IndexBuilder.build_from_registry()` 直接消费 F011 `local-projection/v1`，不自行扫描 Vault；同名对象按 owner 三元组保留，并把 projection hash 写入 `QueryResult.generated_from/projection_sha256`。
- `tests/test_indexing.py::test_registry_projection_feeds_owner_aware_index` 通过两个独立 Git vault 验证 public/private 同名 Wiki 均进入 local index 且 owner 不覆盖。QMD、向量模型和大规模质量仍待环境验收。

## SQLite index freshness 证据（2026-08-27）

- `tests/test_indexing.py::IndexingTests::test_retriever_rejects_stale_fts5_index` 验证 canonical projection 内容变化后，旧 SQLite index 的 `generated_from` 不匹配即被拒绝并回退 deterministic fallback。
- `SQLiteIndex` 将 scope 与输入集合 hash 写入 `index_info`；旧版本/损坏 schema 按不可用处理，不会把陈旧命中报告为 FTS5 正常结果。

## 损坏索引恢复增量证据（2026-08-27）

- `tests/test_indexing.py::IndexingTests::test_rebuild_retains_previous_index` 验证 SQLite rebuild 成功替换时保留 `<index>.previous`，上一版本仍可独立读取。
- 临时事务或新索引写入失败时不触碰现有 index；查询发现损坏/陈旧索引时回退 deterministic fallback，等待显式 rebuild。

## Retriever 资源边界增量证据（2026-08-27）

- `Retriever.search()` 现在与 API 共用 `max_vault_ids=16` 及 `top_k`/query 限制；超限或非法 vault 列表在 QMD、FTS5 和 LIKE 之前统一返回 `query_limit_exceeded`。
- `tests/test_indexing.py::IndexingTests::test_retriever_enforces_vault_id_limit_before_provider` 验证直接调用检索层也不会绕过资源和 owner scope 门禁。

## Index CLI 增量证据（2026-08-27）

- `python -m tools.cli index rebuild|recover --root R --scope public --index I` 复用 `SQLiteIndex`，只读取 public projection manifest；`recover` 会执行 scope/generated_from/quick_check 校验并在需要时原子重建。
- `tests/test_indexing.py::IndexingTests::test_index_cli_rebuild_and_recover_use_public_projection` 验证 CLI rebuild 后 recover 返回 `state: valid`，不扫描或写入 canonical Wiki。

## F005 review 增量证据（2026-08-28）

- **FTS5 默认接线（修复关键缺口）**：review 发现 CLI query / FastAPI / Skill 三个入口构造 `Retriever` 时均未传 `index_path`——FTS5 索引可构建但无消费者，真实查询永远走 LIKE 降级（AC-F005-002 的降级链路此前只在注入式测试中成立）。现约定默认索引路径 `state/index/public.sqlite3`（`indexing.default_public_index_path`），三入口自动接线（存在即用，陈旧/损坏仍自动降级 LIKE）。对应测试：`F005WiringTests`；真实 checkout 演练：`index rebuild` 后 `query` 返回 `method: fts5` 并命中 aar。
  > 已失效（ADR-0019，2026-09-15）：原文"public apply 后由 `public_projection_rebuilder` 自动重建索引，失败与 projection 失败同语义（`applied_index_pending` + 显式 recover）"随写通道退场——`public_projection_rebuilder`、`IndexAutoRebuildTests` 与 `applied_index_pending` 均已删除。当前索引重建是**显式动作**：`python -m tools.cli index rebuild`（`projection generate` 不重建索引），写通道的失败语义只剩 `state: blocked` + 结构化错误码。
- **FTS5 特殊字符查询修复**：用户查询现按 FTS5 短语字面量包裹（双引号转义）；裸 MATCH 语法此前把 `c++`/`a-b`/引号当语法符号抛 OperationalError 并静默降级，真实技术查询永远用不上 FTS5。
- 边界不变：CJK 分词（unicode61 无中文分词器）仍属环境验收；QMD 已退役（ADR-0017），F005 维持 Implemented（部分）。
