---
aliases: []
confidentiality: public
domain: computer-science
evidence:
- claim: 协作图是 UML 图的主要类型之一。
  claim_id: collaboration-diagram-claim-1
  support: direct
  supporting_quotes:
  - evidence_id: evidence-3496321a9b05
    exact: The main types of UML diagrams include Class diagrams, Object diagrams,
      Use case diagrams, Sequence diagrams, Collaboration diagrams, Activity diagrams,
      Statechart diagrams, Deployment diagrams, and Component diagrams.
  targets:
  - evidence_id: evidence-3496321a9b05
    source_id: web-computer-science-collaboration-diagram
id: collaboration-diagram
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-collaboration-diagram
- working-computer-science-collaboration-diagram
status: published
tags:
- uml
- collaboration-diagram
- diagram
- interaction
title: 协作图
updated_at: '2026-09-06'
---
# 协作图

## 一句话结论

协作图（又称合作图）是**交互图的另一种形式**：它代表系统的结构组织和发送/接收的消息，**强调发送和接收消息的对象的结构组织**；其目的与序列图类似，二者是同构的，可相互转换。

## 核心概念

- **定义**：协作图是交互图的另一种形式，代表系统的结构组织和发送/接收的消息；结构组织由对象和链接组成。
- **定位**：协作图的目的类似于序列图。
- **与序列图的区别**：序列图强调消息的时间顺序；协作图强调发送和接收消息的对象的结构组织。
- **UML 图中的地位**：协作图是 UML 图的主要类型之一（与类图、对象图、用例图、序列图、活动图、状态图、部署图、组件图并列）。

## 工作机制

- 协作图描述对象间的动态合作关系，可看成类图与序列图的交集，重点描述对象之间的相互通信关系。
- 用途：捕捉系统的动态行为、描述系统中的消息流、描述对象的结构组织、描述对象之间的相互作用。
- 使用场景：按时间顺序建模控制流、对结构化组织的控制流建模、正向工程、逆向工程。
- 与序列图的选择：如果强调时间和顺序则使用序列图；如果强调上下级关系则使用协作图。

## 示例或代码

绘制工具参考：https://plantuml.com/zh/sequence-diagram（协作图与序列图语法相通）

## 常见误区

- **“协作图与序列图内容完全不同”**：二者目的类似且同构，可相互转换而不丢失信息；区别只在强调时间顺序（序列图）还是对象结构组织（协作图）。
- **“协作图只画对象不画消息”**：协作图同样描述发送/接收的消息，只是以结构组织为表达重点。

## 证据映射

| claim_id | 来源 | 要点 |
| --- | --- | --- |
| collaboration-diagram-claim-1 | web-computer-science-collaboration-diagram | 协作图是 UML 图的主要类型之一 |

## 待验证项

无。

## 关联知识

- [[uml]] —— UML 总论，协作图属行为图。
- [[sequence-diagram]] —— 与协作图同构的交互图，强调时间顺序。
- [[software-modeling]] —— 软件建模中的交互建模。

## 详细章节

### 协作图

协作图是交互图的另一种形式。它代表系统的结构组织和发送/接收的消息。结构组织由对象和链接组成。

协作图的目的类似于序列图。

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



#### 参考

https://www.tutorialspoint.com/uml/index.htm

https://www.cs.uah.edu/~rcoleman/Common/SoftwareEng/UML.html

## 参考

- https://www.tutorialspoint.com/uml/index.htm
- https://www.cs.uah.edu/~rcoleman/Common/SoftwareEng/UML.html
