# Technical Design 实现设计

Technical Design 回答“如何实现”，不取代系统规范，也不记录长期决策历史。

## 必须编写的情况

- 跨越两个以上模块；
- 修改持久化 schema；
- 涉及失败恢复、幂等、锁或原子性；
- 引入外部依赖；
- 涉及公开/私有边界；
- 存在不可逆迁移或多个合理实现。

## 模板

每份实现设计应包含：目标与非目标、当前基线、模块边界、数据模型、接口契约、正常流程、失败流程、幂等与并发、安全边界、可观测性、测试策略、迁移回滚和未决问题。

## P0 设计

| 设计 | 状态 | 链接 |
| --- | --- | --- |
| Source 导入与归档 | Draft | [正文](./source-ingestion-and-archive.md) |
| 分层布局与写入通道 | （正文无状态行） | [正文](./layers-and-channels.md) |
| 证据锚定（evidence_anchor） | Draft | [正文](./evidence-anchoring.md) |
| Wiki Claim 验证 | Draft | [正文](./wiki-claim-validation.md) |
| 可执行 Schema Validator | Draft | [正文](./schema-validation.md) |
| 写操作与锁 | Implemented | [正文](./write-operation-and-locking.md) |

## 发布与运行面设计

| 设计 | 状态 | 链接 |
| --- | --- | --- |
| Public/Local 索引与检索 | Implemented | [正文](./index-and-retrieval.md) |
| FastAPI 本地服务与离线降级 | Implemented | [正文](./local-api-and-offline.md) |
| Agent Skill 受控读写 | Implemented | [正文](./agent-skill.md) |
| Question 题型与面试练习 | Implemented | [正文](./question-and-practice.md) |
| 存量内容迁移与质量清理 | Implemented | [正文](./content-migration.md) |
| 音视频与转录来源 | （正文无状态行） | [正文](./media-sources.md) |
| 备份、恢复与可观测性 | Implemented | [正文](./backup-and-observability.md) |
| Private Vaults 子仓库（0..N） | Implemented | [正文](./private-vault-submodule.md) |
| Astro/Starlight 静态 Wiki 发布 | Implemented | [正文](./static-wiki-publishing.md) |
| 2026-08-26 系统 Review 记录 | 历史快照（无状态行） | [正文](./system-review-2026-08-26.md) |

> 状态从各设计正文「- 状态：」行读取并简化为 Implemented/Draft；正文无状态行的
> 文档在此显式标注。索引完整性由 `tools.matrix_sync.check_doc_indexes` 机器校验。
