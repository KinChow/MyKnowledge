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

## Feature 分类（正交轴）

Feature 按**两个正交轴**归类，任何新 Feature 必须且只能落在一个象限，不能
横跨多类（若横跨，说明拆得不够细，应拆分）：

```text
               纵向（数据链上的位置）
        ┌───────────────────────────────────────┐
  横向  │            │                            │
  （被  │  核心链路    │  消费端 / 能力面           │
  谁依  │  数据事实    │  对外提供入口              │
  赖）  │  F001–F005  │  F006–F010                │
        ├────────────┼────────────────────────────┤
        │  横向基础    │  演进 / 独立域              │
        │  被多方依赖  │  可并行，不阻塞主链路        │
        │  F011–F012  │  F013–F014                │
        └────────────┴────────────────────────────┘
```

| 象限 | 轴 | 判定条件 | 当前成员 |
| --- | --- | --- | --- |
| **核心链路** | 纵向 | 参与 Source → Wiki → Evidence → Write → Index 数据链，被 ≥3 个下游依赖 | F001, F002, F003, F004, F005 |
| **横向基础** | 横向 | 不直接产生内容，但被 ≥2 个其它 Feature 依赖的公共能力 | F011, F012 |
| **消费端 / 能力面** | 纵向 | 依赖核心链路，向用户/Agent/浏览器提供入口 | F006, F007, F008, F009, F010 |
| **演进 / 独立域** | 横向 | 不进入主链路数据流，可独立推进 | F013, F014 |

**判定规则（新增 Feature 时使用）**：

1. 若它扩展主链路某环节（新来源类型、新校验规则）→ 归核心链路；
2. 若它被 ≥2 个已有 Feature 依赖且自身不产内容 → 归横向基础；
3. 若它消费核心链路并向外部提供入口 → 归消费端；
4. 若它独立于主链路数据流 → 归演进/独立域；
5. 若同时命中多个象限 → 拆分为多个 Feature，每个只落一个象限（正交约束）。

## Feature 总览

| ID | Feature | 分类 | 优先级 | 依赖 | 验收 |
| --- | --- | --- | --- | --- | --- |
| F001 | Source 导入、来源完备性和快照归档 | 核心链路 | P0 | 规范 | [F001](./acceptance/F001-source-ingestion.md) |
| F002 | Wiki schema、状态机和内容契约 | 核心链路 | P0 | F001 | [F002](./acceptance/F002-wiki-contract.md) |
| F003 | Claim/Evidence 与证据验证门禁 | 核心链路 | P0 | F001, F002 | [F003](./acceptance/F003-evidence-validation.md) |
| F004 | Preview/Apply、幂等、锁、移动和废弃 | 核心链路 | P0 | F001–F003 | [F004](./acceptance/F004-write-operation.md) |
| F005 | Public/Local 索引与检索 | 核心链路 | P1 | F001–F004 | [F005](./acceptance/F005-index-and-retrieval.md) |
| F006 | FastAPI 本地服务与离线降级 | 消费端 | P1 | F005 | [F006](./acceptance/F006-local-api-and-offline.md) |
| F007 | Astro/Starlight 公共静态 Wiki 和发布门禁 | 消费端 | P1 | F002, F003, F005, F011（public projection） | [F007](./acceptance/F007-static-wiki-publishing.md) |
| F008 | Question 题型、claim 绑定和面试练习 | 消费端 | P1 | F002, F003 | [F008](./acceptance/F008-question-practice.md) |
| F009 | Agent Skill 受控读写 | 消费端 | P1 | F004–F006 | [F009](./acceptance/F009-agent-skill.md) |
| F010 | 存量内容迁移和质量清理 | 消费端 | P1 | F001–F004 | [F010](./acceptance/F010-content-migration.md)、[迁移台账](./f010-migration-ledger.md) |
| F011 | Private Vaults 独立私有 Git 子仓库（0..N） | 横向基础 | P1 | F001–F004、SEC 契约 | [F011](./acceptance/F011-private-vault.md) |
| F012 | 备份、恢复和可观测性 | 横向基础 | P1 | 核心模块 | [F012](./acceptance/F012-backup-and-observability.md) |
| F013 | 数据分域、五层布局与三条写入通道 | 演进/独立域 | P0 | F002, F004（F007/F011/F012 需同步路径） | [F013](./acceptance/F013-layers-and-channels.md) |
| F014 | 音视频与转录来源 | 演进/独立域 | P2 | F001, F013 | [F014](./acceptance/F014-media-sources.md) |

## 新增 Feature 流程

新 Feature 从提出到进入本表必须走以下流程，**编号由本仓库唯一分配，不回收不复用**：

1. **编号**：按顺序取下一个未用编号（当前为 F015）。若该编号曾用于已合并/废弃的 Feature，不回收，继续递增。
2. **起草**：用下方「Feature 记录模板」起草，明确目标、范围、依赖、验收。
3. **定分类**：按上节「判定规则」落到唯一象限；若横跨多象限，拆分后再编号。
4. **对齐规范**：在总纲领 [规范 ID 基线](./myknowledge-system-design.md#21-规范-id-基线) 与 [追踪矩阵](./traceability-matrix.md) 登记对应规范 ID 与验收场景。
5. **评审**：进入本表前经 ADR 决策（若改变既有契约）或 Feature 评审（若不改变）。
6. **记录**：在本表追加一行，更新实施顺序图与依赖关系；验收文档按
   [Acceptance 模板](./acceptance/README.md) 新建。

### 新增条目必须包含

| 项 | 必填 | 说明 |
| --- | --- | --- |
| ID | 是 | 顺序编号，不回收 |
| 分类 | 是 | 四象限之一，正交约束 |
| 优先级 | 是 | P0/P1/P2 |
| 依赖 | 是 | 前置 Feature，驱动实施顺序 |
| 验收链接 | 是 | 指向对应 Acceptance 文档 |
| 规范 ID | 是 | 在总纲领登记，经追踪矩阵映射到测试 |

> 状态列推进同样适用：`Implemented` 只是代码完成，`Accepted` 才意味着验收
> 场景全部有证据——不要把「实现过」当作「验收过」。

## Feature 记录模板

每个 Feature 至少明确以下信息：

- 目标、用户价值、范围和非目标；
- 分类（四象限之一）、规范 ID、ADR、Technical Design 和 Acceptance 引用；
- 前置依赖、交付物和完成定义；
- 当前状态和可复核证据。

当前与本次方案直接相关的状态：F001/F002/F003 已实现（2026-08-27，F003 LLM 证据审计链路 + corroboration-v1 + 人工确认写入完成）；F004 已进入 `Implemented`（2026-08-28 补齐：operation-confirmation/v1 确认事件绑定（AC-006/011）、双进程并发一致性（AC-003）、public apply 默认真实 projection 重建（AC-004-009 部分）；此前已有通用 writer、retire/purge 门禁和 private owner-root 路径绑定；跨 Vault staging 与领域 writer 统一迁移未闭合）；F005 已进入 `Implemented`（projection、SQLite FTS5、fallback 与 Registry owner-aware projection 接入，QMD/完整恢复验收未闭合）；F006 已进入 `Implemented`（FastAPI retrieve/query/ask 基础能力，完整 API 验收未闭合）；F007 已进入 `Implemented`（Astro 工程骨架、静态 graph、确定性 sitemap 与 leak gate，真实 projection/浏览器验收未闭合）；F008 已进入 `Implemented`（题目 schema、绑定、评分和 FSRS adapter 基础能力，完整验收未闭合）；F009 已进入 `Implemented`（canonical Skill 基础契约，完整运行验收未闭合）；F010 已进入 `Implemented`（legacy inventory 基础能力，Source-first 迁移未闭合）；F011 已进入 `Implemented`（Registry、owner-aware local projection，完整 Vault 写入/恢复验收未闭合）；F012 已进入 `Implemented`（状态、manifest、隔离恢复与 durable restore marker，外部 target 验收未闭合）。以上均不等同于 `Accepted`。

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
- F013：[分层与写入通道 Technical Design](./technical-design/layers-and-channels.md)（通过 [Acceptance](./acceptance/F013-layers-and-channels.md)）
- F014：[音视频与转录来源 Technical Design](./technical-design/media-sources.md)（通过 [Acceptance](./acceptance/F014-media-sources.md)）

F007 和 F011 均按“完整能力包”交付：projection、门禁、fallback、失败恢复、可观测性和验收场景必须同一版本完成，不先交付会被后续重写的临时实现。

F010 不在 P0 写入门禁稳定前进行批量迁移。先用代表性样本验证迁移规则，再根据实测结果估算全量工作量。

## F013 / F014 的交付边界

F013 是布局与通道 Feature，分三个独立可验收的批次交付（映射见 §4.6）：

- **批次 1（零风险）**：`queries/`、`state/`、`reports/` 迁入 `var/`；删除空目录 `specs/`。只改 `paths.py`、`.gitignore` 与 `policy.yaml` 的 projection 前缀。
- **批次 2（低风险，窗口收窄中）**：`sources/`、`wiki/` 迁入 `content/`；新建 `content/working|journal|decisions/`。`body_path` 变化会让已发布页面的 `public_release` 自动回落 `false`，需重新人工确认一次。**每多一个已发布页面就多一次重新确认，因此这一批次应尽早执行。**
- **批次 3（中风险，需独立 review）**：`archive/`、`audit/`、`release/` 迁入 `ledger/`；改约 15 个声明式 durable path 常量。跨 vault 路径模板必须在挂载第一个 private vault 之前定型。

F013 的第二部分是功能项，不依赖上述搬移：`review_by` 报告项（WIKI-003）、`content/working/` 的 TTL 报告、降级落位（CHN-001）。功能项可以在批次 1 之后、批次 2/3 之前先行交付。原计划的快速通道与 unmanaged 层文本检索命令已取消（ADR-0014 决策 4 / 候选 H）。

F014 定为 P2：它是给尚未跑满的主链路增加新入口。日常先用 `content/journal/` 记录"听了哪一集 + 时间点 + 一句话"，真正需要引用时再回去做片段转录。

F013 会改写下游 Technical Design 与 Acceptance 中的历史路径字面量。规范层（本文件、系统设计、ADR、追踪矩阵）已按目标布局对齐；描述**当前实现**的既有 Technical Design 与 Acceptance 文档保持历史路径，在对应批次的实现 commit 中同步更新——这样文档在任何时刻都自洽：规范描述目标，实现文档描述现状，`§4.6` 的映射表是两者之间的唯一权威桥。

## 修订记录

| 日期 | 变更 |
| --- | --- |
| 2026-09-02 | 引入四象限正交分类轴（核心链路/横向基础/消费端/演进独立域），总览表新增「分类」列；新增「新增 Feature 流程」与「新增条目必须包含」表，明确编号不回收与正交约束 |
