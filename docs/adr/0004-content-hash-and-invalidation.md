# ADR-0004：内容 Hash 与失效粒度

- 状态：Accepted
- 日期：2026-08-26
- 相关规范：WIKI、VAL
- 相关 Feature：F002、F003

## 决策

Hash 覆盖正文和语义字段，Evidence 单独计算 hash；tags、aliases、related 等分类字段变化不触发重验；source 阅读笔记按 locator 章节级影响展示，权威验证按不可变 snapshot/evidence item 的 selector 绑定失效。只改未被引用的章节不波及已有报告。

## 后果

分类调整成本低，但正文或语义变化必须重新验证。验证报告必须绑定相应 hash。

## 重新评估条件

验证成本或下游索引一致性要求发生变化时重新评估。
