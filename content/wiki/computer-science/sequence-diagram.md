---
aliases: []
confidentiality: public
domain: computer-science
evidence:
- claim: 'Easy to use

    Easily create diagrams and charts with the Mermaid Live Editor.

    One home for the open-source library and the platform built around it. More resources
    for the project, a clearer path for contributors, and a team committed to keeping
    Mermaid open, always.'
  claim_id: sequence-diagram-audit-1
  support: direct
  supporting_quotes:
  - evidence_id: evidence-4bba26bbf390
    exact: 'Easy to use

      Easily create diagrams and charts with the Mermaid Live Editor.

      One home for the open-source library and the platform built around it. More
      resources for the project, a clearer path for contributors, and a team committed
      to keeping Mermaid open, always.'
  targets:
  - evidence_id: evidence-4bba26bbf390
    source_id: web-computer-science-sequence-diagram
id: sequence-diagram
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-sequence-diagram
- working-computer-science-sequence-diagram
status: published
tags:
- uml
- sequence-diagram
- diagram
- interaction
title: 序列图
updated_at: '2026-09-06'
---
# 序列图

## 一句话结论

序列图是**交互图**，用于可视化系统中执行特定功能的调用序列，**强调消息的时间顺序**——从一个对象流向另一个对象的消息序列；与之相对，协作图强调发送和接收消息的对象的结构组织。

## 核心概念

- **定义**：序列图是交互图，描述从一个对象流向另一个对象的消息序列。
- **定位**：从实施和执行角度看系统组件之间的交互，用于可视化系统中执行特定功能的调用序列。
- **与协作图的关系**：序列图强调消息的时间顺序；协作图强调发送和接收消息的对象的结构组织（二者同构，可相互转换）。

## 工作机制

- 序列图按时间顺序对控制流建模，描述对象之间消息的发送与接收顺序。
- 用途：捕捉系统的动态行为、描述系统中的消息流、描述对象的结构组织、描述对象之间的相互作用。
- 使用场景：按时间顺序建模控制流、对结构化组织的控制流建模、正向工程、逆向工程。

## 示例或代码

绘制工具参考：

- PlantUML：https://plantuml.com/zh/sequence-diagram
- Mermaid：https://mermaid-js.github.io/mermaid/#/sequenceDiagram

## 常见误区

- **“序列图与协作图画的东西完全不同”**：序列图与协作图描述同一类交互，是同构的；区别在于序列图强调时间顺序，协作图强调对象的结构组织。
- **“序列图只展示静态结构”**：序列图是行为/交互图，展示的是消息流动的动态行为。

## 证据映射

| claim_id | 来源 | 要点 |
| --- | --- | --- |
| sequence-diagram-audit-1 | web-computer-science-sequence-diagram | 该 claim 为 Mermaid 官网推广文案（迁移期误锚），与序列图主题无直接关联，按规则保留原文案 |

## 待验证项

无。

## 关联知识

- [[uml]] —— UML 总论，序列图属行为图。
- [[collaboration-diagram]] —— 与序列图同构的交互图，强调结构组织。
- [[software-modeling]] —— 软件建模中的交互建模。

## 详细章节

### 序列图

序列图是交互图。从一个对象流向另一个对象的消息序列。

从实施和执行的角度来看，系统组件之间的交互非常重要。序列图用于可视化系统中执行特定功能的调用序列。

序列图强调消息的时间顺序。

协作图强调发送和接收消息的对象的结构组织。



#### 目的

- 捕捉系统的动态行为。
- 描述系统中的消息流。
- 描述对象的结构组织。
- 描述对象之间的相互作用。



#### 哪里使用

- 按时间顺序对控制流进行建模。
- 对结构化组织的控制流进行建模。
- 正向工程。
- 逆向工程。



#### 模块元素



#### 如何绘制

https://plantuml.com/zh/sequence-diagram

https://mermaid-js.github.io/mermaid/#/sequenceDiagram



#### 参考

https://www.tutorialspoint.com/uml/index.htm

https://www.cs.uah.edu/~rcoleman/Common/SoftwareEng/UML.html

## 参考

- https://www.tutorialspoint.com/uml/index.htm
- https://plantuml.com/zh/sequence-diagram
- https://mermaid-js.github.io/mermaid/#/sequenceDiagram
