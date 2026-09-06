---
aliases: []
confidentiality: public
domain: computer-science
evidence:
- claim: 活动图可以用 if、repeat、fork 等关键字来表达控制流。
  claim_id: activity-diagram-claim-1
  support: direct
  supporting_quotes:
  - evidence_id: evidence-5b62633807b6
    exact: if、repeat、fork 等关键字来表达控制流。图形会自动生成。
  targets:
  - evidence_id: evidence-5b62633807b6
    source_id: web-computer-science-activity-diagram
- claim: 活动图支持自上而下描述流程，包括分支和循环。
  claim_id: activity-diagram-claim-2
  support: direct
  supporting_quotes:
  - evidence_id: evidence-93c134859d4a
    exact: 自上而下描述流程，包括分支和循环。
  targets:
  - evidence_id: evidence-93c134859d4a
    source_id: web-computer-science-activity-diagram
- claim: 文本中的顺序就是图中的顺序。
  claim_id: activity-diagram-claim-3
  support: direct
  supporting_quotes:
  - evidence_id: evidence-431fdcd364db
    exact: 文本中的顺序就是图中的顺序。
  targets:
  - evidence_id: evidence-431fdcd364db
    source_id: web-computer-science-activity-diagram
- claim: 调整步骤顺序或添加分支，只需编辑文本，无需重画。
  claim_id: activity-diagram-claim-4
  support: direct
  supporting_quotes:
  - evidence_id: evidence-b6462ea735be
    exact: 调整步骤顺序或添加分支，只需编辑文本，无需重画。
  targets:
  - evidence_id: evidence-b6462ea735be
    source_id: web-computer-science-activity-diagram
id: activity-diagram
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-activity-diagram
- working-computer-science-activity-diagram
status: published
tags:
- uml
- activity-diagram
- diagram
title: 活动图
updated_at: '2026-09-06'
---
# 活动图

## 一句话结论

活动图是**一种特殊的状态图**，本质上是用“活动 + 链接”描述系统控制流程的流程图：控制流从一个操作流向另一个操作，可以是顺序的、并发的或分支的，并通过 fork、join 等元素处理各种流程控制。

## 核心概念

- **定义**：活动图描述系统中的控制流程，由活动和链接组成；流可以是顺序的、并发的或分支的。
- **活动**：不过是系统的功能，活动图用于可视化系统中的控制流，描述系统执行时将如何工作。
- **定位**：活动图是一种特殊的状态图，基本上是一个流程图，表示从一个活动到另一个活动的流程。
- **控制流类型**：顺序、分支、并发，通过 fork、join 等元素处理。

## 工作机制

- 控制流从一个操作（活动）到另一个操作，可以是顺序、分支或并发的。
- 用途：画出系统的活动流程、描述从一项活动到另一项活动的顺序、描述系统的并行/分支/并发流程。
- 使用场景：使用活动对工作流程建模、建模业务需求、获取系统功能的高度理解、在稍后阶段调查业务需求。
- 文本化表达：可用 `if`、`repeat`、`fork` 等关键字表达控制流，图形自动生成；文本中的顺序就是图中的顺序；调整步骤顺序或添加分支只需编辑文本，无需重画。

## 示例或代码

活动图绘制工具：https://plantuml.com/zh/activity-diagram-beta

## 常见误区

- **“活动图就是普通状态图”**：活动图是状态图的一种特殊形式，但它关注的是流程/控制流，而非对象状态转移。
- **“活动图只能表达顺序流程”**：活动图的流可以是顺序、分支或并发的，通过 fork、join 等元素支持并发控制流。

## 证据映射

| claim_id | 来源 | 要点 |
| --- | --- | --- |
| activity-diagram-claim-1 | web-computer-science-activity-diagram | 活动图可用 if、repeat、fork 等关键字表达控制流，图形自动生成 |
| activity-diagram-claim-2 | web-computer-science-activity-diagram | 活动图支持自上而下描述流程，包括分支和循环 |
| activity-diagram-claim-3 | web-computer-science-activity-diagram | 文本中的顺序就是图中的顺序 |
| activity-diagram-claim-4 | web-computer-science-activity-diagram | 调整步骤顺序或添加分支只需编辑文本，无需重画 |

## 待验证项

无。

## 关联知识

- [[uml]] —— UML 总论，活动图属行为图。
- [[statechart-diagram]] —— 活动图是其一种特殊形式。
- [[software-modeling]] —— 软件建模中的行为建模。

## 详细章节

### 活动图

活动图描述了系统中的控制流程。它由活动和链接组成。流可以是顺序的、并发的或分支的。

活动不过是系统的功能。准备了许多活动图来捕获系统中的整个流程。

活动图用于可视化系统中的控制流。这是准备了解系统在执行时将如何工作。

活动图是一种特殊的状态图。

活动图基本上是一个流程图，表示从一个活动到另一个活动的流程。活动可以描述为系统的操作。

控制流从一个操作到另一个操作。此流程可以是顺序的、分支的或并发的。活动图通过使用不同的元素（例如 fork、join 等）来处理所有类型的流控制



#### 目的

- 画出系统的活动流程。
- 描述从一项活动到另一项活动的顺序。
- 描述系统的并行、分支和并发流程。



#### 哪里使用

- 使用活动对工作流程进行建模。
- 建模业务需求。
- 对系统功能的高度理解。
- 在稍后阶段调查业务需求。



#### 模块元素



#### 如何绘制

https://plantuml.com/zh/activity-diagram-beta



#### 参考

https://www.tutorialspoint.com/uml/index.htm

https://www.cs.uah.edu/~rcoleman/Common/SoftwareEng/UML.html

## 参考

- https://www.tutorialspoint.com/uml/index.htm
- https://plantuml.com/zh/activity-diagram-beta
