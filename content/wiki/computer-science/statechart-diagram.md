---
aliases: []
confidentiality: public
domain: computer-science
evidence:
- claim: "New! Render PlantUML diagrams directly inside GitHub\n        with our official
    browser extension —\n        No server. No tokens. No tracking. Zero permissions
    but clipboard. —\n        Try it out and let us know what you think!"
  claim_id: statechart-diagram-audit-1
  support: direct
  supporting_quotes:
  - evidence_id: evidence-40b9db19760a
    exact: "New! Render PlantUML diagrams directly inside GitHub\n        with our
      official browser extension —\n        No server. No tokens. No tracking. Zero
      permissions but clipboard. —\n        Try it out and let us know what you think!"
  targets:
  - evidence_id: evidence-40b9db19760a
    source_id: web-computer-science-statechart-diagram
id: statechart-diagram
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-statechart-diagram
- working-computer-science-statechart-diagram
status: published
tags:
- uml
- state-diagram
- diagram
title: 状态图
updated_at: '2026-09-06'
---
# 状态图

## 一句话结论

状态图用于表示**系统的事件驱动状态变化**：任何实时系统都会对内部/外部事件作出反应，状态图描述一个类、接口等对象在不同状态下如何因事件发生状态转移，是对类图行为上的补充。

## 核心概念

- **定义**：状态图用于表示系统的事件驱动状态变化，基本描述一个类、接口等的状态变化。
- **状态机**：状态图描述一个状态机——由外部或内部事件控制、定义对象不同状态的机器。
- **状态特定性**：状态特定于系统的组件/对象。
- **事件**：导致状态变化的外部因素。

## 工作机制

- 实时系统受内部/外部事件影响，这些事件负责系统的状态变化。
- 状态图通过内部/外部因素可视化系统的反应。
- 用途：对系统的动态方面建模、对反应系统的生命周期建模、描述对象在其生命周期中的不同状态、定义状态机来对对象的状态建模。
- 使用场景：对系统的对象状态建模、对反应系统建模（反应系统由反应对象组成）、识别导致状态变化的事件、正向与逆向工程。

## 示例或代码

绘制工具参考：

- PlantUML：https://plantuml.com/zh/state-diagram
- Mermaid：https://mermaid-js.github.io/mermaid/#/stateDiagram

## 常见误区

- **“状态图是描述数据流的”**：状态图描述的是对象状态随事件发生的转移，而非数据流。
- **“状态图与活动图一样”**：状态图关注对象状态与事件驱动的转移；活动图虽然是一种特殊的状态图，但关注的是流程/控制流。

## 证据映射

| claim_id | 来源 | 要点 |
| --- | --- | --- |
| statechart-diagram-audit-1 | web-computer-science-statechart-diagram | 该 claim 为 PlantUML 官网推广文案（迁移期误锚），与状态图主题无直接关联，按规则保留原文案 |

## 待验证项

无。

## 关联知识

- [[uml]] —— UML 总论，状态图属行为图。
- [[activity-diagram]] —— 活动图是状态图的一种特殊形式。
- [[software-modeling]] —— 软件建模中的行为建模。

## 详细章节

### 状态图

预计任何实时系统都会受到某种内部/外部事件的反应。这些事件负责系统的状态变化。

状态图用于表示系统的事件驱动状态变化。它基本上描述了一个类、接口等的状态变化。

状态图用于通过内部/外部因素可视化系统的反应。

状态特定于系统的组件/对象。

状态图描述了一个状态机。状态机可以定义为定义对象不同状态的机器，这些状态由外部或内部事件控制。



#### 目的

- 对系统的动态方面进行建模。
- 对反应系统的生命周期进行建模。
- 描述对象在其生命周期中的不同状态。
- 定义状态机来对对象的状态进行建模。



#### 哪里使用

- 对系统的对象状态进行建模。
- 对反应系统进行建模。反应系统由反应对象组成。
- 识别导致状态变化的事件。
- 正向和逆向工程。



#### 模块元素



#### 如何绘制

https://plantuml.com/zh/state-diagram

https://mermaid-js.github.io/mermaid/#/stateDiagram



#### 参考

https://www.tutorialspoint.com/uml/index.htm

https://www.cs.uah.edu/~rcoleman/Common/SoftwareEng/UML.html

## 参考

- https://www.tutorialspoint.com/uml/index.htm
- https://plantuml.com/zh/state-diagram
- https://mermaid-js.github.io/mermaid/#/stateDiagram
