# ADR-0008：Question 门禁与 FSRS

- 状态：Accepted（F008 基础实现；完整运行面仍按 Acceptance 增量闭合）
- 日期：2026-08-25
- 相关规范：QST
- 相关 Feature：F008

## 决策

Question 必须绑定已验证或已发布的 `kind: knowledge` Wiki 的 claim_ids，题型为单选题、多选题和面向面试的简答题；复习调度采用 FSRS adapter，题目和复习状态仅保留在 local/private，public projection 不读取 practice。

## 后果

题目数量增长较慢但可信度更高；系统必须区分可重建索引和不可重建复习状态。

## 重新评估条件

引入非知识型题目或多种复习调度器时重新评估。
