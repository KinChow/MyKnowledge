# ADR-0005：引文规范化与验证

- 状态：Accepted
- 日期：2026-08-26
- 相关规范：EVD、VAL
- 相关 Feature：F003

## 决策

所有 `supporting_quotes.exact` 使用共享规范化函数：NFKC、受控的全角标点映射、连续排版空白折叠、删除零宽字符、保留大小写和代码标点；只有 extractor 明确提供 `markup_projection` 与 offset map 时才可去除 Markdown 包装标记。匹配限定在不可变 snapshot 的 TextPosition/TextQuote selector 范围内，并要求达到最小长度。实现必须维护 normalized-text 到 canonical snapshot code-point 的 offset map，确保归一化不会扩大 selector 范围。prefix/suffix/position 只用于消歧和恢复建议，近似匹配不能单独通过；出现多个归一化候选时返回 `ambiguous_selector`，不得放行。

## 后果

中文和 Markdown 格式差异不会造成无意义失败，但引文必须真实存在于被引用 snapshot/evidence item。

## 重新评估条件

出现无法表达的内容类型或规范化造成语义歧义时重新评估。
