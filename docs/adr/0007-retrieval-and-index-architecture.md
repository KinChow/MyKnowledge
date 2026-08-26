# ADR-0007：检索和索引架构

- 状态：Accepted
- 日期：2026-08-26
- 相关规范：IDX、SEC、WEB
- 相关 Feature：F005、F006、F007、F009

## 背景

系统同时需要公开静态搜索、本地 source/wiki 检索和自然语言/混合检索。公开构建必须可复现，本地模式默认尝试使用 QMD；QMD 内部是否启用向量/RRF 取决于本机已安装能力，不把独立 Embedding/FAISS 服务作为第一阶段依赖。系统必须在 QMD 不可用时离线可用；索引不能成为内容真相源，也不能决定 Wiki 的验证或发布状态。

## 候选方案

### A. 只用 SQLite FTS5（基线）

SQLite 内置、离线、确定性、支持 BM25/highlight/snippet，Python/FastAPI 部署简单，能从 Markdown 投影重建。缺点是语义召回和复杂 rerank 需要额外组件，中文分词效果需要明确测试。

### B. 只用 QMD

QMD 已提供 hash 增量索引、BM25、向量、RRF、LLM rerank、CJK normalization、行号读取和 MCP，能快速获得较完整的本地语义检索。缺点是 Node `>=22` 运行时和模型依赖扩大部署面；其索引 schema、排序和升级节奏不是 MyKnowledge 的稳定契约，不能让它决定状态或写 canonical 文件。

### C. Elasticsearch/OpenSearch/Qdrant 等独立服务

适合多人和大规模部署，但引入服务、权限、备份和网络硬依赖，超出个人 Git 知识库第一阶段边界。

## 决策

采用“QMD 默认只读适配器 + SQLite FTS5 必选确定性基线 + 明确 fallback”的完整能力包。第一阶段不实现自有 `EmbeddingRetriever`/`HybridRetriever`/独立 FAISS 索引；如未来需要，只能作为兼容 adapter 接入，不得改变或删除 FTS5/LIKE 基线：

本地运行时的默认策略固定为：

```yaml
retrieval:
  default: qmd
  fallback: [fts5, deterministic-fallback]
  qmd:
    version: 2.8.3
    mode: read-only
```

`default: qmd` 只影响本地自然语言/混合查询；精确 ID、标题和反向索引仍可走确定性直达。配置缺失、QMD 健康检查失败或 QMD 只具备关键词能力时，路由器按 `fallback` 顺序切换并在 `QueryResult.degraded`/`limits` 中说明原因；不能把没有向量能力的 QMD 报告为自有 hybrid/semantic 实现。

1. `IndexBuilder` 从 `sources/`、`wiki/` 和当前版本允许索引的对象 projection 生成 canonical `queries/local` 和 SQLite FTS5 数据库；public projection 只从 `public_publishable` Wiki 生成 Pagefind 输入。索引均可删除后从权威内容重建。
2. FTS5 表使用 external-content 或普通 content 表均可，但同步由 MyKnowledge application 负责；每条记录携带 `object_ref={vault_id, object_type, object_id}`、`confidentiality`、`status`、`source_ref`、`content_sha256` 和 `schema_version`。更新使用 content hash 增量，删除使用 tombstone/事务同步，不能只更新索引文本而不更新 metadata。
3. `QmdRetriever` 是本地自然语言/混合检索的默认实现，统一返回 `QueryResult`。MyKnowledge 先生成隔离的 local projection 和 manifest，再调用固定版本 QMD CLI/MCP；QMD 只返回带 `vault_id`/`object_type` 的候选 ID、分数、行号和片段，随后由 MyKnowledge 重新读取 canonical projection、检查 owner/confidentiality/hash，并映射为同一 `QueryResult`。QMD 不能写 `sources/`、`wiki/`、`queries/`，不能创建/删除对象，不能改变 `status`、`evidence_state`、`validation_state` 或发布结果。QMD 是否使用本地向量/重排由其 capability report 表达；MyKnowledge 不依赖未声明的模型或缓存。
4. 查询路由仍可对精确 ID、标题和反向索引走确定性直达；需要自然语言或混合召回时优先调用 QMD。QMD 不可安装、Node 版本不满足、模型缺失、索引损坏、MCP/CLI 超时或输出 schema 不兼容时，自动切换到 `FtsRetriever`；FTS5 不可用时再切换到 Python 标准库/SQLite LIKE 的窄 fallback，分别标记 `method: fts5` 或 `method: deterministic-fallback`，不伪装成语义检索。
5. QMD 索引、向量文件、模型缓存和 rerank 结果不进入 public Git；版本通过 lockfile/manifest 固定，升级必须跑离线 query fixture、中文回归和结果一致性检查。QMD 的 license、网络调用和模型数据路径在安装前记录。QMD cache 必须是本机 `0700`、network-disabled、read-only 输入，且不能被共享回答缓存复用。public Astro 构建不调用 QMD，仍只使用 public projection + Pagefind。
6. RAG 的检索、生成和 citation 校验与证据验证分离：召回片段不能直接让 Wiki 变成 `published`。internal chunk 只能在其 owner private vault 的 local index 中存在，chunk 必须保留 `vault_id`；回答必须标记 `confidentiality: internal`，不写共享缓存。
7. 每个检索能力按一次完整能力包交付：接口、索引生成、fallback、可观测性、测试和恢复同时落地，不先交付一个会被后续重写的临时检索实现。

## 统一接口

```python
class Retriever(Protocol):
    def search(self, query: str, scope: SearchScope, top_k: int = 8) -> QueryResult:
        ...
```

`QueryResult` 至少包含 `items[]`、`method`、`index_version`、`degraded`、`confidentiality_max` 和 `limits[]`；每个 item 必须可回到 `object_id` 与 `source_ref`。任何 adapter 返回无法解析的 ID 都丢弃并记录 warning，不把裸文本展示为可信引用。

## 后果

优点：QMD 默认提供成熟的本地混合语义召回，SQLite/FTS5 和 LIKE 保证离线降级可用，接口和内容权限仍由 MyKnowledge 控制；索引损坏或 QMD 缺失不会阻断基本查询。

代价：需要维护 FTS5 与 QMD 两套适配和结果回归；中文分词、QMD Node 运行时和模型缓存要做环境检查；本地语义搜索的质量仍需用用户数据和固定 fixture 评估，不能把 QMD 分数当作事实正确性。

## 重新评估条件

当语料规模、并发、召回质量或权限需求超过 SQLite/QMD 组合边界，或需要多人共享索引时，再评估 OpenSearch/Qdrant/pgvector 等独立服务；迁移仍必须实现同一 `Retriever` 契约和 FTS5 fallback。
