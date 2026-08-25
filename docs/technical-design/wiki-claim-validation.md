# Wiki Claim 与证据验证实现设计

- 状态：Draft
- 相关 Feature：F002、F003
- 相关规范：WIKI、EVD、VAL
- 相关 ADR：ADR-0001、ADR-0004、ADR-0005
- 相关验收：[F002](../acceptance/F002-wiki-contract.md)、[F003](../acceptance/F003-evidence-validation.md)

## 目标与非目标

目标是实现 Wiki schema、Claim/Evidence 映射、supporting_quote 校验和验证报告失效。本阶段不实现复杂语义检索。

## 流程

解析 Wiki → 确定性 schema 校验 → 检查 Claim 引用 → 在 locator 内匹配 quote → 生成验证输入 → 保存绑定 hash 的报告 → 计算 publishable。

## 失败处理

缺少来源、quote 不匹配、hash 不一致、locator 失效或 LLM 不可用时，知识型 Wiki 不得进入 published。

## 测试策略

覆盖正常 Claim、章节边界、规范化差异、短引文、来源漂移、验证报告失效和豁免类型。

## 未决问题

LLM 适配器的具体供应商和本地测试替身待实现阶段确定，但不能改变验证结果 schema。
