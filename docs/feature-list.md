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
| F005 | Public/Local 索引与检索 | P1 | F001–F004 | 待建立 |
| F006 | FastAPI 本地服务与离线降级 | P1 | F005 | 待建立 |
| F007 | Astro 公共静态站和发布门禁 | P1 | F002, F003, F005 | 待建立 |
| F008 | Question、claim 绑定和 FSRS 复习 | P1 | F002, F003 | 待建立 |
| F009 | Agent Skill 受控读写 | P1 | F004–F006 | 待建立 |
| F010 | 存量内容迁移和质量清理 | P1 | F001–F004 | 待建立 |
| F011 | Private Vault 实现 | P2 | 保密契约稳定 | Deferred |
| F012 | 备份、恢复和可观测性 | P1 | 核心模块 | 待建立 |

## Feature 记录模板

每个 Feature 至少明确以下信息：

- 目标、用户价值、范围和非目标；
- 规范 ID、ADR、Technical Design 和 Acceptance 引用；
- 前置依赖、交付物和完成定义；
- 当前状态和可复核证据。

## 实施顺序

```text
F001 → F002 → F003 → F004
                    ├→ F005 → F006
                    ├→ F007
                    └→ F008 → F009
             F001–F004 稳定后 → F010
```

F010 不在 P0 写入门禁稳定前进行批量迁移。先用代表性样本验证迁移规则，再根据实测结果估算全量工作量。
