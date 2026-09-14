# ADR-0008：Question 门禁与 FSRS

- 状态：Accepted（基础契约；学习产品扩展见 ADR-0016）
- 日期：2026-08-25
- 相关规范：QST
- 相关 Feature：F008

## 决策

Question 必须绑定已验证或已发布的 `kind: knowledge` Wiki 的一个或多个 claim，题目和复习状态仅保留在 local/private，public projection 不读取 practice。复习调度采用 FSRS adapter；具体题型、短回合 session、领域分类和成熟组件复用边界由 ADR-0016 定义。

## 后果

题目数量增长较慢但可信度更高；系统必须区分可重建索引和不可重建复习状态。

## 重新评估条件

引入非知识型题目或多种复习调度器时重新评估。
