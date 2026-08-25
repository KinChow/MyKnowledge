# ADR-0008：Question 门禁与 FSRS

- 状态：Accepted
- 日期：2026-08-25
- 相关规范：QST
- 相关 Feature：F008

## 决策

Question 必须绑定已验证或已发布的 `kind: knowledge` Wiki 的 claim_ids，题目门禁严于 Wiki。FSRS 复习进度作为不可重建数据单独备份。

## 后果

题目数量增长较慢但可信度更高；系统必须区分可重建索引和不可重建复习状态。

## 重新评估条件

引入非知识型题目或多种复习调度器时重新评估。
