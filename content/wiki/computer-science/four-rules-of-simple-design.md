---
aliases:
- four-rules-of-simple-desgin
- four-rules-of-simple-design
confidentiality: public
domain: computer-science
evidence:
- claim: Beck 的简单设计规则按优先级排列，“通过测试”优先于“表达意图”。
  claim_id: four-rules-of-simple-design-rules
  support: direct
  supporting_quotes:
  - evidence_id: evidence-ecd538e916a0
    exact: The rules are in priority order, so “passes the tests” takes priority over
      “reveals intention”
  targets:
  - evidence_id: evidence-ecd538e916a0
    source_id: martin-fowler-beck-design-rules-v2
id: four-rules-of-simple-design
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- martin-fowler-beck-design-rules-v2
- working-computer-science-four-rules-of-simple-desgin
status: published
tags:
- refactoring
- simple-design
- software-design
title: 简单设计四原则
updated_at: '2026-09-06'
---
# 简单设计四原则

## 一句话结论

简单设计四原则（Beck）按优先级排列：① 通过所有测试 ② 尽可能消除重复 ③ 尽可能清晰表达 ④ 更少的代码元素。"通过测试"优先于"表达意图"。

## 核心概念

- **通过所有测试**：软件系统对外部需求被正确完成，包括功能性与非功能性需求，并通过用户验收标准。
- **尽可能消除重复**：让软件走向高内聚低耦合、达到良好正交的过程；原则表述为"最小化重复"而非"消除重复"。
- **尽可能清晰表达**：漂亮的代码如同优秀散文，从不隐藏设计者意图，恰如其分地抽象、直截了当地控制。
- **更少的代码元素**：尽可能降低设计复杂度，保持简单。

## 工作机制

四条规则按优先级排序，"通过测试"优先于"表达意图"：

1. 先保证软件通过所有测试（正确完成外部需求）。
2. 在满足测试的前提下，尽可能消除重复（走向高内聚低耦合、良好正交）。
3. 再追求清晰表达意图（代码阅读次数远大于修改次数）。
4. 最后减少代码元素、降低设计复杂度。

## 示例或代码

以"消除重复"为例：让软件走向高内聚低耦合、良好正交的过程。但并不是所有重复都可以消除，因此这条原则被描述为"最小化重复"，而不是"消除重复"。

## 常见误区

- **把"消除重复"理解为必须消灭一切重复**：原文表述是"最小化重复"。
- **忽略优先级**：四条规则有先后，"通过测试"优先于"表达意图"。
- **把"更少代码元素"等同于代码越少越好**：它指的是降低设计复杂度、保持简单。

## 证据映射

| claim_id | 来源 | 要点 |
| --- | --- | --- |
| four-rules-of-simple-design-rules | martin-fowler-beck-design-rules-v2 | 规则按优先级排列，"通过测试"优先于"表达意图" |

## 待验证项

无

## 关联知识

- [[refactoring-concepts-and-principles]] —— 重构是达成简单设计的途径。
- [[bad-smells-in-code]] —— 坏味道对应简单设计原则被违背。
- [[orthogonal-design-principles]] —— 正交设计四原则（重复意味着耦合）。
- [[solid]] —— SOLID 面向对象设计原则。

## 详细章节

### 简单设计四原则

#### 通过所有测试

软件系统对外部需求被正确地完成，包括功能性需求和非功能性需求，并通过了用户验收的标准



#### 尽可能消除重复

让软件走向高内聚低耦合，达到良好正交的过程

并不是所有的重复都可以消除，这条原则被描述为最小化重复，而不是消除重复。



#### 尽可能清晰表达

漂亮的代码如同优秀的散文，从不隐藏设计者的意图，恰如其分的抽象，直截了当的控制

代码阅读次数远远大于其修改次数



#### 更少的代码元素

尽可能降低设计复杂度，保持简单

## 参考
- https://martinfowler.com/bliki/BeckDesignRules.html
