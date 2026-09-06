---
aliases:
- don't-repeat-yourself
confidentiality: public
domain: computer-science
evidence:
- claim: DRY（Don't Repeat Yourself）是软件开发原则，旨在减少很可能变化的信息的重复，用更不易变化的抽象替代，或用数据规范化从源头避免冗余。
  claim_id: dry-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-3e823b953bf6
    exact: '"Don''t repeat yourself" (DRY) is a principle of software development
      aimed at reducing repetition of information which is likely to change, replacing
      it with abstractions that are less likely to change, or using data normalization
      which avoids redundancy in the first place.'
  targets:
  - evidence_id: evidence-3e823b953bf6
    source_id: web-computer-science-dry
- claim: DRY 原则的经典表述是"系统中的每一项知识都必须有单一、明确、权威的表示"，出自 Andy Hunt 与 Dave Thomas 的《The Pragmatic
    Programmer》。
  claim_id: dry-single-authoritative
  support: direct
  supporting_quotes:
  - evidence_id: evidence-66159e87920c
    exact: The DRY principle is stated as "Every piece of knowledge must have a single,
      unambiguous, authoritative representation within a system". The principle has
      been formulated by Andy Hunt and Dave Thomas in their book The Pragmatic Programmer.
  targets:
  - evidence_id: evidence-66159e87920c
    source_id: web-computer-science-dry
id: dry
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-dry
status: published
tags:
- dry
- design-principle
- abstraction
- refactoring
title: DRY原则
updated_at: '2026-09-06'
---
# DRY原则

## 一句话结论

DRY（Don't Repeat Yourself，不要重复自己）是软件开发的一项根本原则：**系统中的每一项知识都必须有单一、明确、权威的表示（a single, unambiguous, authoritative representation）**。它主张减少"很可能变化的信息"的重复——用更不易变化的抽象替代重复，或用数据规范化从源头避免冗余，从而保证修改一个元素不会强迫修改其他逻辑上不相关的元素。

## 核心概念

- **DRY 的定义**：减少"很可能变化的信息"的重复，用"更不易变化的抽象"替代，或用数据规范化避免冗余。
- **经典表述**：Every piece of knowledge must have a single, unambiguous, authoritative representation within a system（每一项知识都必须有单一、明确、权威的表示）。
- **知识 vs 代码**：DRY 针对的是"知识（knowledge）"——系统里承载的每一条事实/规则/约束——而不是笼统地消灭一切代码重复。
- **单一选择原则（Single Choice Principle）**：DRY 的一种特殊情形。每当系统需要支持一组备选方案时，系统中应只有一个模块知道它们的完整清单。
- **WET 反模式**：DRY 的对立面，常被解读为 write everything twice（什么都写两遍）；WET 解决方案在多层架构中常见（同一信息在多处重复出现）。
- **AHA**：DRY 的另一种替代主张（Avoid Hasty Abstractions，避免草率抽象），强调在消除重复与过度抽象之间平衡。

## 工作机制

- **抽象替代**：识别出"很可能变化"的重复信息后，用一个更不易变化的抽象（函数、模块、生成器、框架）把它们收拢到一处。
- **数据规范化**：对数据层面的冗余，通过规范化（normalization）从源头消除重复存储。
- **同步保证**：DRY 成功应用后，修改系统的任何一个元素，都不需要修改其他逻辑上不相关的元素；逻辑相关的元素则会一致地、可预期地同步变化。
- **适用范围广**：Hunt 与 Thomas 把 DRY 应用得很宽——数据库 schema、测试计划、构建系统乃至文档都属于"知识"的载体。
- **单一选择原则**：把"备选方案的完整清单"只放在一个模块中，其他模块通过它来决策，避免在多个地方维护同一份选择逻辑。

## 示例或代码

**WET 反例**：给 Web 应用的表单加一个 "comment" 字段，字符串 "comment" 可能同时出现在：表单 label、HTML 标签、读函数名、私有变量、数据库 DDL、查询语句等六七处。修改它要改动多处，极易遗漏。

**DRY 做法**：用框架/数据驱动方式把上述编辑任务收拢到一处，只保留最关键的那次编辑，其余由框架或生成逻辑统一派生，把"新增知识变量"的扩展点留在单一位置。

**单一选择原则示例**（伪代码示意）：

```text
// 一个模块集中维护"支付方式"的完整清单
enum PaymentMethod { CreditCard, Alipay, Wechat }
// 其余模块只消费这个清单，不各自枚举
```

## 常见误区

- **把 DRY 理解为"消灭一切重复代码"**：DRY 针对的是"知识"的重复，不是字面意义的任何代码相似。两段长得像但语义独立的代码不是 DRY 要解决的问题。
- **为 DRY 而过度抽象**：过早抽出抽象可能引入不稳定的中间层；与 YAGNI 存在张力——"未来才需要的知识"不应现在就去抽象（见 [[yagni]]）。
- **忽略"很可能变化"这个限定**：对不会变化的信息强行去重，收益低而成本高。
- **只追求"少写几行"**：DRY 的目标是"单一权威表示 + 同步一致性"，不是单纯的代码行数减少。
- **把 WET 简单等同于"坏代码"**：某些情况下显式重复反而更简单直接（见 [[kiss]]），需要权衡。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| dry-definition | web-computer-science-dry | DRY 旨在减少很可能变化的信息的重复，用更不易变化的抽象替代或用数据规范化避免冗余 |
| dry-single-authoritative | web-computer-science-dry | 经典表述："每一项知识都必须有单一、明确、权威的表示"，出自 The Pragmatic Programmer |

## 待验证项

无。

## 关联知识

- [[kiss]] —— 保持简单：避免因过度设计/过度抽象违背 DRY 的本意。
- [[yagni]] —— 不要实现不需要的功能：与 DRY 的"抽象时机"形成张力。
- [[solid]] —— 面向对象设计原则（单一职责等）与 DRY 一脉相承。
- [[lod]] —— 最少知识原则。
- [[software-design]] —— 软件设计总览。
- [[refactoring-concepts-and-principles]] —— 重构：消除重复的实践手段。
- [[object-oriented]] —— 面向对象：用封装/继承实现知识复用。

## 详细章节

### DRY原则

#### 定义与出处

DRY（Don't Repeat Yourself）是软件开发的一项原则，旨在减少"很可能变化的信息"的重复，做法是用更不易变化的抽象（abstraction）来替代重复，或者使用数据规范化（data normalization）从源头避免冗余。

该原则由 Andy Hunt 与 Dave Thomas 在《The Pragmatic Programmer》中提出，经典表述为：

> Every piece of knowledge must have a single, unambiguous, authoritative representation within a system.

他们把它应用得相当广泛：数据库 schema、测试计划、构建系统乃至文档，都属于"知识"的载体。DRY 成功应用后，修改系统的任何一个元素，都不需要修改其他逻辑上不相关的元素；而逻辑相关的元素会一致地、可预期地变化并保持同步。

#### 单一选择原则

DRY 的一个特殊情形是单一选择原则（Single Choice Principle），由 Bertrand Meyer 定义：

> Whenever a software system must support a set of alternatives, one and only one module in the system should know their exhaustive list.

即：当系统需要支持一组备选方案时，系统中应当只有一个模块知道它们的完整清单。该原则在 Eiffel 语言的设计中得到应用。

#### WET 与 AHA

DRY 的对立面常被称为 WET，一个逆向缩略词，通常解读为 write everything twice（什么都写两遍），也有 write every time / we enjoy typing / waste everyone's time 等变体。

WET 解决方案常见于多层架构：例如在 Web 应用中给表单加一个 "comment" 字段，字符串 "comment" 可能同时出现在表单 label、HTML 标签、读函数名、私有变量、数据库 DDL、查询语句等多处。DRY 的做法是用框架或生成逻辑把上述编辑任务收拢到一处，只保留最关键的一次编辑，把"新增知识变量"的扩展点留在单一位置。

另一种替代主张是 AHA（Avoid Hasty Abstractions，避免草率抽象），强调不应在未充分理解重复结构前就仓促抽象——在消除重复与过度抽象之间保持平衡。

#### 实践建议

- 先识别"很可能变化"的知识点，再决定用抽象、规范化还是生成器去收敛。
- 让"备选方案的完整清单"只存在一个模块中（单一选择原则）。
- 在 DRY 与 KISS/YAGNI 之间权衡：抽象要基于真实需求与变化趋势，而不是猜测未来。

## 参考

- Wikipedia — Don't repeat yourself: https://en.wikipedia.org/wiki/Don%27t_repeat_yourself
- Andy Hunt, Dave Thomas — The Pragmatic Programmer
