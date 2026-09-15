# MyKnowledge 文档索引

> 本文是 docs/ 树的入口导航，不承载规范内容。**规范以
> [系统设计](./myknowledge-system-design.md) 为唯一事实源**；
> 功能状态以 [Feature List](./feature-list.md) 为准。

## 这是什么

MyKnowledge 是一个**证据驱动型个人知识管理系统**：外部资料 → 不可变 Source 快照 → 带 claim/evidence 的 Wiki 页面 → 确定性校验 + LLM 审计 + 人工确认 → public/local 投影发布。快速定位：先读系统设计 §0 导览，需要功能地图读 Feature List。

## 治理层（规范 / 交付索引）

| 文档 | 内容 | 适合 |
| --- | --- | --- |
| [系统设计](./myknowledge-system-design.md) | 总纲领：架构、数据模型、不变量、Agent 索引（§0.4） | 所有人/Agent 必读 |
| [Feature List](./feature-list.md) | 功能四象限分类、交付状态、新增 Feature 流程 | 排期与功能地图 |
| [追踪矩阵](./traceability-matrix.md) | 规范 ID ↔ Feature ↔ ADR ↔ 设计 ↔ 验收 ↔ 测试 映射 | 查证约束实现状态 |
| [ADR](./adr/README.md) | 长期架构决策与取舍原因 | 理解"为什么这样设计" |
| [Technical Design](./technical-design/README.md) | 各能力实现边界、失败处理、测试策略 | 实现开发 |
| [Acceptance](./acceptance/README.md) | 各 Feature 验收场景与通过规则 | 验收门禁 |

> 篇目不在此处硬计数：各目录的 `README.md` 索引由 `matrix check` 双向校验
> （README 必须覆盖目录内全部文档，链接必须指向真实文件），以那边为准。

> 机器校验：治理层索引与状态由 `python -m tools.cli matrix check` 统一校验
> （pre-commit 自动执行），改动治理文档后如提交被拦，先跑该命令看差异。

## 内容域（知识）

`docs/` 已不再承载知识内容：原知识域目录（`computer-science/`、`work-methods/`、
`multimedia/`、`tools/`、`reading-notes/`）及其 `contents.md` 导航页随 F010 迁移与
B5 退役删净（导航由 projection graph 派生），正文与快照落位 `content/sources/` 与
`content/wiki/`（见系统设计 §4.6）。迁移过程决策与批次基线见
[F010 迁移台账](./f010-migration-ledger.md)。`docs/` 现在只保留治理层文档。
