# Acceptance 验收规范

验收文档回答“怎样证明 Feature 完成”。设计规则引用系统规范，执行结果保存到 `reports/acceptance/`。

## 场景格式

每个场景使用 `AC-Fxxx-nnn`，至少包含 Given、When、Then、失败时不变量、自动化级别、对应测试和当前状态。

## 通过规则

- 正常路径、边界、外部失败、重复执行和恢复场景必须覆盖；
- P0 的阻断级场景全部通过后，Feature 才能进入 `Accepted`；
- `Implemented` 不等于 `Accepted`；
- 无测试证据的人工结论必须记录验证环境和复核人。

## P0 验收

- [F001 Source 导入与归档](./F001-source-ingestion.md)
- [F002 Wiki 契约](./F002-wiki-contract.md)
- [F003 证据验证](./F003-evidence-validation.md)
- [F004 写操作](./F004-write-operation.md)

## P1/P2 验收

- [F005 Public/Local 索引与检索](./F005-index-and-retrieval.md)
- [F006 FastAPI 本地服务与离线降级](./F006-local-api-and-offline.md)
- [F007 Astro/Starlight 公共静态 Wiki](./F007-static-wiki-publishing.md)
- [F009 Agent Skill 受控读写](./F009-agent-skill.md)
- [F010 存量内容迁移和质量清理](./F010-content-migration.md)
- [F011 Private Vaults 子仓库（0..N）](./F011-private-vault.md)
- [F012 备份、恢复和可观测性](./F012-backup-and-observability.md)
