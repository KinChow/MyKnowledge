# 规范到验收追踪矩阵

本文是索引，不是新的规范来源。完整约束以
[系统设计规范](./myknowledge-system-design.md) 为准。

## ID 约定

| 前缀 | 范围 |
| --- | --- |
| SYS | 系统不变量 |
| SRC / ARC | Source 与原文归档 |
| WIKI / EVD | Wiki、Claim、Evidence |
| VAL | 确定性和 LLM 验证 |
| OPS | 写操作协议 |
| IDX / API / WEB | 索引、后端和公开站 |
| QST / SKILL / MIG / SEC | 题目、Agent、迁移和保密 |

## P0 基线

| 规范 ID | Feature | ADR | 实现设计 | 验收 | 测试 | 状态 |
| --- | --- | --- | --- | --- | --- | --- |
| SRC-001 | F001 | ADR-0001 | source-ingestion | AC-F001-001/002/004/005/009/010 | 待实现 | Designed |
| ARC-001 | F001 | ADR-0003 | source-ingestion | AC-F001-003/006 | 待实现 | Designed |
| ARC-002 | F001/F003 | ADR-0003/0005 | source-ingestion, evidence-anchoring, wiki-claim-validation | AC-F001-001/004/006/011/012/013, AC-F003-001/002/006 | 待实现 | Designed |
| WIKI-001 | F002 | ADR-0001 | wiki-claim-validation | AC-F002-001/002/004/005 | 待实现 | Designed |
| WIKI-002 | F002 | ADR-0004 | wiki-claim-validation | AC-F002-003/004 | 待实现 | Designed |
| EVD-001 | F003 | ADR-0001/0005 | wiki-claim-validation | AC-F003-001/002/004/005/006/012 | 待实现 | Designed |
| VAL-001 | F003 | ADR-0005/0010 | wiki-claim-validation | AC-F003-003/007/008/011/012/013/014/015/016 | 待实现 | Designed |
| OPS-001 | F004 | ADR-0006 | write-operation-and-locking | AC-F004-001/002/003/004/005/006/010/011 | tests/test_write_operation.py（preview/apply/回滚/fencing 基础）；领域场景待补 | Implemented（部分） |
| ARC-003 | F001/F003 | ADR-0003/0005 | source-ingestion, wiki-claim-validation | AC-F001-007/008/010, AC-F003-009/010/011 | 待实现 | Designed |
| ARC-004 | F001/F011/F012 | ADR-0003/0002 | source-ingestion, private-vault-submodule, backup-and-observability | AC-F001-006, AC-F011-004, AC-F012-005 | 待实现 | Designed |
| OPS-003 | F004/F011/F012 | ADR-0006/0002 | write-operation-and-locking, private-vault-submodule, backup-and-observability | AC-F004-007/008, AC-F011-016/018, AC-F012-004/005 | 待实现 | Designed |
| OPS-004 | F004 | ADR-0006 | write-operation-and-locking | AC-F004-009 | 待实现 | Designed |

## Public Wiki、索引与 Private Vault

| 规范 ID | Feature | ADR | 实现设计 | 验收 | 测试 | 状态 |
| --- | --- | --- | --- | --- | --- | --- |
| IDX-002 | F005/F006/F009 | ADR-0007 | [index-and-retrieval](./technical-design/index-and-retrieval.md), [local-api-and-offline](./technical-design/local-api-and-offline.md) | AC-F005-001/002/003/004/005/006, AC-F006-001/002/004/005/007, AC-F009-005 | tests/test_indexing.py（projection/FTS5/同 scope 路由/fallback）；QMD/API 完整场景待补 | Implemented（部分） |
| API-001 | F006/F009 | ADR-0006/0007 | [local-api-and-offline](./technical-design/local-api-and-offline.md), [agent-skill](./technical-design/agent-skill.md) | AC-F006-001/003/005/006/007/008/009/010, AC-F009-005/006 | tests/test_api.py + tests/test_citation.py（query/retrieve/ask/read/backlinks/token/Origin-Host/资源限制/citation replay 基础；完整 API/Skill 待补） | Implemented（部分） |
| API-002 | F006/F009 | ADR-0007 | [local-api-and-offline](./technical-design/local-api-and-offline.md) | AC-F006-002/004/005/009/010, AC-F009-004/005 | 待实现 | Designed |
| WEB-003 | F007 | ADR-0009 | [static-wiki-publishing](./technical-design/static-wiki-publishing.md) | AC-F007-001/002/003/004/005/006/007/008/009/010/011/012/013/014/015/016/017/018/019/020/021/022/023/024/025 | queries/public/manifest.json（空 allowlist 输入）；真实发布与 leak gate 待补 | Implemented（部分） |
| WEB-001 | F007 | ADR-0009 | [static-wiki-publishing](./technical-design/static-wiki-publishing.md) | AC-F007-001/005/006/009/012/013/014/015/016/017/018/019/020/021/022/023/024/025 | frontend 工程骨架；真实 projection/浏览器/leak gate 待补 | Implemented（部分） |
| WEB-002 | F007/F010 | ADR-0009 | [static-wiki-publishing](./technical-design/static-wiki-publishing.md) | AC-F007-002/003/007/008 | 待实现 | Designed |
| WEB-003 | F007/F010 | ADR-0009 | [static-wiki-publishing](./technical-design/static-wiki-publishing.md) | AC-F007-001/008/011/012/013/014/015/016/017/018, AC-F010-001/003 | 待实现 | Designed |
| SEC-002 | F007/F011 | ADR-0002/0009 | [private-vault-submodule](./technical-design/private-vault-submodule.md), [static-wiki-publishing](./technical-design/static-wiki-publishing.md) | AC-F007-004/009, AC-F011-006/010/012/013/014 | 待实现 | Designed |
| SEC-003 | F011 | ADR-0002 | [private-vault-submodule](./technical-design/private-vault-submodule.md) | AC-F011-005/007/012/013/014 | 待实现 | Designed |
| OPS-002 | F011 | ADR-0002/0006 | [private-vault-submodule](./technical-design/private-vault-submodule.md) | AC-F011-001/002/003/004/008/009/011/014/015/016 | tests/test_vault_registry.py（Registry、跨 Vault 同名与同 Vault 冲突基础）；领域场景待补 | Implemented（部分） |
| SKILL-001 | F009 | ADR-0006/0007 | [agent-skill](./technical-design/agent-skill.md) | AC-F009-001/002/003/004/005/006/007/008/009/010 | tests/test_skill_contract.py + tests/test_skill_runtime.py（白名单、危险参数、preview/apply 基础）；运行集成待补 | Implemented（部分） |
| VAL-002 | F003/F009/F011 | ADR-0001/0002/0010 | [wiki-claim-validation](./technical-design/wiki-claim-validation.md), [agent-skill](./technical-design/agent-skill.md) | AC-F003-008/011/012/013/014/015/016, AC-F009-004/008/009, AC-F011-007 | 待实现 | Designed |
| MIG-001 | F010 | ADR-0001/0005 | [content-migration](./technical-design/content-migration.md) | AC-F010-001/002/003 | tools/inventory_legacy.py + tools/migrate_legacy.py + tests/test_inventory.py/test_migration.py（只读 preview）；真实迁移待补 | Implemented（部分） |
| BAK-001 | F012 | ADR-0002/0006 | [backup-and-observability](./technical-design/backup-and-observability.md) | AC-F012-001/002/003/004/006/007/008 | tools/backup.py + tests/test_vault_registry.py（entries、manifest/篡改校验）；恢复场景待补 | Implemented（部分） |
| BAK-002 | F012/F011 | ADR-0002/0003 | [backup-and-observability](./technical-design/backup-and-observability.md), [private-vault-submodule](./technical-design/private-vault-submodule.md) | AC-F012-005/007/008/AC-F011-009/011/018 | 待实现 | Designed |
| SEC-004 | F006/F009/F011 | ADR-0002/0007 | [local-api-and-offline](./technical-design/local-api-and-offline.md), [agent-skill](./technical-design/agent-skill.md), [private-vault-submodule](./technical-design/private-vault-submodule.md) | AC-F006-006/008/009, AC-F009-009, AC-F011-017 | 待实现 | Designed |
| SCH-001 | F002 | ADR-0001/0006 | [schema validation](./technical-design/schema-validation.md) | AC-F002-001/003/004/006/007 | 待实现 | Designed |
| QST-001 | F008 | ADR-0008 | [question-and-practice](./technical-design/question-and-practice.md) | AC-F008-001/002/003/004/005 | tests/test_question.py + tests/test_api.py（hash 失效、评分记录、FSRS unavailable、practice API 基础）；恢复/leak gate 待补 | Implemented（部分） |
| SEC-005 | F007/F011 | ADR-0002/0009 | [static-wiki-publishing](./technical-design/static-wiki-publishing.md), [private-vault-submodule](./technical-design/private-vault-submodule.md) | AC-F007-021/022/023/024/025, AC-F011-012/013/014 | 待实现 | Designed |

## 验收场景完整覆盖

追踪矩阵不能用“同一 Feature 的某几个代表场景”代替完整映射。下面列出每个当前 Feature 验收文档中的全部场景；新增场景必须同时更新本表并通过 `npm run validate:docs`。

| Feature | 全部验收场景 |
| --- | --- |
| F001 | AC-F001-001, AC-F001-002, AC-F001-003, AC-F001-004, AC-F001-005, AC-F001-006, AC-F001-007, AC-F001-008, AC-F001-009, AC-F001-010, AC-F001-011, AC-F001-012, AC-F001-013 |
| F002 | AC-F002-001, AC-F002-002, AC-F002-003, AC-F002-004, AC-F002-005, AC-F002-006, AC-F002-007 |
| F003 | AC-F003-001, AC-F003-002, AC-F003-003, AC-F003-004, AC-F003-005, AC-F003-006, AC-F003-007, AC-F003-008, AC-F003-009, AC-F003-010, AC-F003-011, AC-F003-012, AC-F003-013, AC-F003-014, AC-F003-015, AC-F003-016 |
| F004 | AC-F004-001, AC-F004-002, AC-F004-003, AC-F004-004, AC-F004-005, AC-F004-006, AC-F004-007, AC-F004-008, AC-F004-009, AC-F004-010, AC-F004-011 |
| F005 | AC-F005-001, AC-F005-002, AC-F005-003, AC-F005-004, AC-F005-005, AC-F005-006 |
| F006 | AC-F006-001, AC-F006-002, AC-F006-003, AC-F006-004, AC-F006-005, AC-F006-006, AC-F006-007, AC-F006-008, AC-F006-009, AC-F006-010 |
| F007 | AC-F007-001, AC-F007-002, AC-F007-003, AC-F007-004, AC-F007-005, AC-F007-006, AC-F007-007, AC-F007-008, AC-F007-009, AC-F007-010, AC-F007-011, AC-F007-012, AC-F007-013, AC-F007-014, AC-F007-015, AC-F007-016, AC-F007-017, AC-F007-018, AC-F007-019, AC-F007-020, AC-F007-021, AC-F007-022, AC-F007-023, AC-F007-024, AC-F007-025 |
| F009 | AC-F009-001, AC-F009-002, AC-F009-003, AC-F009-004, AC-F009-005, AC-F009-006, AC-F009-007, AC-F009-008, AC-F009-009, AC-F009-010 |
| F010 | AC-F010-001, AC-F010-002, AC-F010-003 |
| F011 | AC-F011-001, AC-F011-002, AC-F011-003, AC-F011-004, AC-F011-005, AC-F011-006, AC-F011-007, AC-F011-008, AC-F011-009, AC-F011-010, AC-F011-011, AC-F011-012, AC-F011-013, AC-F011-014, AC-F011-015, AC-F011-016, AC-F011-017, AC-F011-018 |
| F012 | AC-F012-001, AC-F012-002, AC-F012-003, AC-F012-004, AC-F012-005, AC-F012-006, AC-F012-007, AC-F012-008 |

## 完整性要求

- 每条 `必须` 级规范至少映射一个 Feature 和一个验收场景。
- 每个 P0 Feature 必须有 Technical Design 和 Acceptance。
- 每个验收场景必须关联自动化测试或明确的人工验证方式。
- F007 必须证明静态站点不依赖 FastAPI、LLM 或任何 private vault；F011 必须证明多个外挂仓库、单仓库不可用、跨仓库冲突和逐 vault 备份状态不会破坏 public repo 或无关 vault。
- 本地自然语言/混合检索默认使用 QMD；FTS5 是必选确定性 fallback，QMD/FTS5 不可用时回退 Python/SQLite LIKE，三种路径和 QueryResult 契约必须同时验收；public Astro 构建不依赖 QMD。
- 本矩阵中的状态不能替代验收证据。
- `availability` 与 `availability_reason`、durable audit/confirmation、local API capability token、URL SSRF/文件竞态和 Vault 路径隔离必须分别有拒绝/恢复证据；不能只用一次 happy-path smoke 代替。
- Provider source context 必须有 prompt-injection/tool/URL 禁用和 capability alias 冲突的拒绝证据；QMD cache、query limit、GET/POST 检索等价性必须有资源边界测试。
- 发布锁、逐 Vault fencing token、未知 warning 阻断、全量 public 输入扫描、编码路径穿越、额外 HTML allowlist 和 Mermaid SVG 安全必须有独立拒绝/恢复证据。
- Durable record 只校验单条 `record_sha256` 与 target owner；顺序与篡改证据来自 Git 历史，不自建 audit hash chain。
