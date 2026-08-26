# MyKnowledge Feature List

> 本文是交付路线和状态索引，不重复系统设计规范。规则以
> [MyKnowledge 证据驱动知识系统设计](./myknowledge-system-design.md) 为准。

## 状态定义

```text
Proposed → Designed → Ready → In Progress → Implemented → Accepted → Released
```

- `Implemented`：代码完成并通过开发者测试。
- `Accepted`：验收场景全部有证据，阻断级问题关闭。
- `Released`：已满足发布门禁并进入目标运行环境。

## Feature 总览

| ID | Feature | 优先级 | 依赖 | 验收 |
| --- | --- | --- | --- | --- |
| F001 | Source 导入、来源完备性和快照归档 | P0 | 规范 | [F001](./acceptance/F001-source-ingestion.md) |
| F002 | Wiki schema、状态机和内容契约 | P0 | F001 | [F002](./acceptance/F002-wiki-contract.md) |
| F003 | Claim/Evidence 与证据验证门禁 | P0 | F001, F002 | [F003](./acceptance/F003-evidence-validation.md) |
| F004 | Preview/Apply、幂等、锁、移动和废弃 | P0 | F001–F003 | [F004](./acceptance/F004-write-operation.md) |
| F005 | Public/Local 索引与检索 | P1 | F001–F004 | [F005](./acceptance/F005-index-and-retrieval.md) |
| F006 | FastAPI 本地服务与离线降级 | P1 | F005 | [F006](./acceptance/F006-local-api-and-offline.md) |
| F007 | Astro/Starlight 公共静态 Wiki 和发布门禁 | P1 | F002, F003, F005, F011（public projection） | [F007](./acceptance/F007-static-wiki-publishing.md) |
| F008 | Question 题型、claim 绑定和面试练习（后续） | Deferred | F002, F003（主链路稳定后） | [Deferred 设计](./deferred/f008-question-design.md)，验收待单独编写 |
| F009 | Agent Skill 受控读写 | P1 | F004–F006 | [F009](./acceptance/F009-agent-skill.md) |
| F010 | 存量内容迁移和质量清理 | P1 | F001–F004 | [F010](./acceptance/F010-content-migration.md) |
| F011 | Private Vaults 独立私有 Git 子仓库（0..N） | P1 | F001–F004、SEC 契约 | [F011](./acceptance/F011-private-vault.md) |
| F012 | 备份、恢复和可观测性 | P1 | 核心模块 | [F012](./acceptance/F012-backup-and-observability.md) |

## Feature 记录模板

每个 Feature 至少明确以下信息：

- 目标、用户价值、范围和非目标；
- 规范 ID、ADR、Technical Design 和 Acceptance 引用；
- 前置依赖、交付物和完成定义；
- 当前状态和可复核证据。

当前与本次方案直接相关的状态：F001/F002/F003 已实现（2026-08-27，F003 LLM 证据审计链路 + corroboration-v1 + 人工确认写入完成）；F004 已进入 `Implemented`（通用 writer，领域验收未闭合）；F011 已进入 `Implemented`（只读 Registry，完整 Vault 验收未闭合）；F005–F010、F012（含 F008）仍为 `Designed`，尚未声称代码 `Implemented` 或 `Accepted`；验收文档中的 `Not Implemented` 是有意保留的事实边界。当前 checkout 还没有 `skills/myknowledge/SKILL.md` 和领域 writer/backend；F009 的 canonical Skill 文件存在性本身是验收门，不得从文档路径的预留描述推断已实现。

F008 已转入本轮独立 Feature，不改变 Source → Wiki → Evidence 主链路；题型为单选题、多选题和面向面试的简答题，复习调度采用 FSRS，题目与复习状态仅保留在 local/private，不进入 public projection。

## 实施顺序

```text
F001 → F002 → F003 → F004
                    ├→ F005 → F006 → F009
                    ├→ F007
             F001–F004 稳定后 → F010
             F011（Vault Registry） ─┬→ F005/F006/F007/F009
             F012（audit/backup） ───┴→ F004–F011 的恢复与观测门
```

F011 与 F001–F004 同一套 schema/hash/operation 实现；F007 只消费 F011 生成的 public projection，不 checkout 或读取任何 private vault。F011 的 private projection 和 internal LLM provider 不得成为 public build 依赖；实现必须支持 0..N 个外挂仓库、逐 vault 状态和独立备份。

F011 与 F012 是横向基础能力：F011 为 F005/F006/F007/F009 提供 Vault Registry、owner/ref 和逐 vault availability；F012 为 F004/F005/F006/F009/F011 提供 durable audit、备份状态、恢复演练和可观测性。它们不能被实现顺序图中的单一路径遗漏，未配置 remote/backup 时只能报告 `unconfigured`，不能标记为已恢复。

当前主链路不等待 F008；F009 只提供 Source/Wiki/Query/Publish 等受控操作，不包含题库和复习功能。F008 在基础知识链路稳定后单独启动。

F007 的 `public_release` 默认是 `false`，只有人工对当前输出 hash 创建 public confirmation，projection 根据 durable event/operation record 派生为 `true` 才能发布；F011 的 private Git remote 与加密备份位置当前保持 TBD/`unconfigured`，未配置时必须告警且不能声称恢复链路就绪。

## 设计与验收索引

- F005/F006：[索引与检索](./technical-design/index-and-retrieval.md)、[FastAPI 本地服务](./technical-design/local-api-and-offline.md)
- F007：[静态 Wiki Technical Design](./technical-design/static-wiki-publishing.md)（通过 [Acceptance](./acceptance/F007-static-wiki-publishing.md)）
- F009：[Agent Skill Technical Design](./technical-design/agent-skill.md)（通过 [Acceptance](./acceptance/F009-agent-skill.md)）
- F010：[内容迁移 Technical Design](./technical-design/content-migration.md)（通过 [Acceptance](./acceptance/F010-content-migration.md)）
- F011：[Private Vault Technical Design](./technical-design/private-vault-submodule.md)（通过 [Acceptance](./acceptance/F011-private-vault.md)）
- F012：[备份与可观测性 Technical Design](./technical-design/backup-and-observability.md)（通过 [Acceptance](./acceptance/F012-backup-and-observability.md)）

F007 和 F011 均按“完整能力包”交付：projection、门禁、fallback、失败恢复、可观测性和验收场景必须同一版本完成，不先交付会被后续重写的临时实现。

F010 不在 P0 写入门禁稳定前进行批量迁移。先用代表性样本验证迁移规则，再根据实测结果估算全量工作量。
