---
aliases: []
confidentiality: public
domain: computer-science
evidence:
- claim: "UML® — Unified Modeling Language\nA specification defining a graphical language
    for visualizing, specifying, constructing, and documenting the artifacts of distributed
    object systems.\n- Title:\n- Unified Modeling Language\n- Acronym:\n- UML®\n-
    Version:\n- \n                            2.5."
  claim_id: software-modeling-audit-1
  support: direct
  supporting_quotes:
  - evidence_id: evidence-68991efb07fc
    exact: "UML® — Unified Modeling Language\nA specification defining a graphical
      language for visualizing, specifying, constructing, and documenting the artifacts
      of distributed object systems.\n- Title:\n- Unified Modeling Language\n- Acronym:\n-
      UML®\n- Version:\n- \n                            2.5."
  targets:
  - evidence_id: evidence-68991efb07fc
    source_id: web-computer-science-software-modeling
id: software-modeling
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-software-modeling
- working-computer-science-software-modeling
status: published
tags:
- uml
- modeling
- software-engineering
- architecture
title: 软件建模
updated_at: '2026-09-06'
---
# 软件建模

## 一句话结论

软件建模体现了软件设计的思想，**在需求和实现之间架起一座桥梁**：模型是所研究系统的抽象，通过外部、交互、结构化、行为四个视角描述系统，实现过程为“需求 → 模型 → 实现”。

## 核心概念

- **模型**：并不是软件系统的完备表示，而是所研究系统的抽象；通过不同视角描述一个系统。
- **四个视角**：
  - 外部视角：对系统上下文或环境建模；
  - 交互视角：对系统及其环境之间、或系统构件之间的交互建模；
  - 结构化视角：对系统的组织或所处理的数据结构建模；
  - 行为视角：对系统的动态行为以及系统如何响应事件建模。
- **建模原则**（4 条）：模型的选择影响问题发现与解决；每个模型可有多种表达方式，使用者与用途是评判关键；最好的模型切合实际、简化不掩盖重要细节；孤立的模型是不完整的。
- **建模方法**：结构化方法、面向对象方法、基于构件方法、面向服务方法、面向方面方法、模型驱动方法、形式化方法。
- **建模语言**：UML（统一建模语言）是软件建模的重要载体。

## 工作机制

软件建模的实现过程从需求入手，用模型表达分析设计过程，最终把模型映射成软件实现：

```
需求 -> 模型 -> 实现
```

在软件过程中，不同方法（结构化、面向对象、构件、服务、方面、模型驱动、形式化）各有其建模思想与工具，选择取决于领域和场景。

## 示例或代码

- 面向对象方法：见 [[uml]] 及其各类图（类图、用例图、序列图等）。
- 模型驱动方法（Model Driven Development）：把模型作为开发的中心产物，逐层映射到实现。

## 常见误区

- **“模型就是系统的完整表示”**：模型并不是软件系统的完备表示，而是所研究系统的抽象，简化必须不掩盖重要细节。
- **“只要画一张图就完成了建模”**：孤立的模型是不完整的；软件建模需要通过多个视角（外部、交互、结构化、行为）全面描述系统。
- **“软件建模只有一种方法”**：不同领域和场景有不同的建模方法（结构化、面向对象、构件、服务、方面、模型驱动、形式化等）。

## 证据映射

| claim_id | 来源 | 要点 |
| --- | --- | --- |
| software-modeling-audit-1 | web-computer-science-software-modeling | 该 claim 为 UML 规范描述文本（UML 2.5，用于可视化、指定、构建与文档化分布式对象系统的构件），与软件建模主题相关，原文案保留 |

## 待验证项

无。

## 关联知识

- [[uml]] —— 软件建模的核心建模语言。
- [[class-diagram]] / [[object-diagram]] / [[component-diagram]] / [[deployment-diagram]] —— 结构建模。
- [[use-case-diagram]] / [[sequence-diagram]] / [[collaboration-diagram]] / [[statechart-diagram]] / [[activity-diagram]] —— 行为建模。

## 详细章节

### 软件建模

#### 概述

软件建模体现了软件设计的思想，在需求和实现之间架起一座桥梁，通过模型指导软件系统的具体实现。

模型并不是软件系统的一个完备表示，而是所研究**系统的抽象**。软件建模通过不同视角描述一个系统。

* 外部视角：对系统上下文或环境进行建模
* 交互视角：对系统及其环境或者系统的构件之间的交互进行建模
* 结构化视角：对系统的组织或者系统所处理的数据结构进行建模
* 行为视角：对系统的动态行为以及系统如何响应事件进行建模



#### 原则

1. 选择建立什么样的模型对如何发现和解决问题具有重要的影响。正确的模型有助于提高开发者的洞察力。
2. 每个模型可以有多种表达方式。使用者的身份和使用的原因是评判模型好坏的关键。 
3. 最好的模型总是能够切合实际。模型是现实的简化，必须保证简化过程不会掩盖任何重要的细节。
4. 孤立的模型是不完整的。



#### 过程

软件建模的实现过程是从需求入手，用模型表达分析设计过程，最终将模型映射成软件实现。

需求 -> 模型 -> 实现



#### 方法

在不同领域和场景下有不同的软件建模方法，其各自的建模思想和采用的建模工具也不相同。

* 结构化方法（structured method）
* [面向对象方法（object oriented method）](./methods/object-oriented.md)
* 基于构件方法（component base development）
* 面向服务方法（service oriented method）
* 面向方面方法（aspect oriented method）
* 模型驱动方法（model driven development）
* 形式化方法（format method）



#### [UML](./UML/UML.md)

## 参考

- https://www.tutorialspoint.com/uml/index.htm
- https://www.omg.org/spec/UML/
