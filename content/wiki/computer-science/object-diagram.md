---
aliases: []
confidentiality: public
domain: computer-science
evidence:
- claim: "New! Render PlantUML diagrams directly inside GitHub\n        with our official
    browser extension —\n        No server. No tokens. No tracking. Zero permissions
    but clipboard. —\n        Try it out and let us know what you think!"
  claim_id: object-diagram-audit-1
  support: direct
  supporting_quotes:
  - evidence_id: evidence-c1a3cd81e546
    exact: "New! Render PlantUML diagrams directly inside GitHub\n        with our
      official browser extension —\n        No server. No tokens. No tracking. Zero
      permissions but clipboard. —\n        Try it out and let us know what you think!"
  targets:
  - evidence_id: evidence-c1a3cd81e546
    source_id: web-computer-science-object-diagram
id: object-diagram
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-object-diagram
- working-computer-science-object-diagram
status: published
tags:
- uml
- object-diagram
- diagram
title: 对象图
updated_at: '2026-09-06'
---
# 对象图

## 一句话结论

对象图是**类图的一个实例**：它把一组对象及其关系呈现为实例，表示系统在**特定时刻的静态快照**，用于从实际角度理解对象行为与关系、制作系统原型和逆向工程。

## 核心概念

- **定义**：对象图是对象及对象之间关系的集合，是类图的一个实例。
- **与类图的关系**：对象图派生自类图、依赖于类图；类图与对象图基本概念相似，都表示系统的静态视图。
- **快照性质**：对象图的静态视图是系统在特定时刻的快照，而不是抽象的类结构。

## 工作机制

- 对象图把类图中的抽象类关系实例化为具体的对象及对象间关系。
- 用途：正向与逆向工程、呈现系统的对象关系、交互的静态视图、从实际角度理解对象行为及其关系。
- 使用场景：制作系统原型、逆向工程、建模复杂的数据结构、从实际角度理解系统。

## 示例或代码

绘制工具参考：https://plantuml.com/zh/object-diagram

## 常见误区

- **“对象图就是类图”**：对象图是类图的实例，显示类的多个对象实例而不是实际的类，二者是抽象与实例的关系。
- **“对象图表示的是任意时刻的系统结构”**：对象图表示的是系统在特定时刻的快照（静态视图），而非整个系统的抽象结构。

## 证据映射

| claim_id | 来源 | 要点 |
| --- | --- | --- |
| object-diagram-audit-1 | web-computer-science-object-diagram | 该 claim 为 PlantUML 官网推广文案（迁移期误锚），与对象图主题无直接关联，按规则保留原文案 |

## 待验证项

无。

## 关联知识

- [[class-diagram]] —— 对象图所实例化的类图。
- [[uml]] —— UML 总论，对象图属结构图。
- [[software-modeling]] —— 软件建模中的结构建模。

## 详细章节

### 对象图

对象图为类图的一个实例。

对象图是对象及对象之间关系的集合。

对象图表示系统的静态视图。

对象图的用法类似于类图，但它们用于从实际角度构建系统原型。

对象图派生自类图，因此对象图依赖于类图。

对象图表示类图的一个实例。类图和对象图的基本概念相似。对象图也表示系统的静态视图，但此静态视图是系统在特定时刻的快照。

对象图用于将一组对象及其关系呈现为实例。



#### 目的

- 正向和逆向工程。
- 系统的对象关系
- 交互的静态视图。
- 从实际角度理解对象行为及其关系。



#### 哪里使用

- 制作系统原型。
- 逆向工程。
- 建模复杂的数据结构。
- 从实际角度理解系统。



#### 如何绘制

https://plantuml.com/zh/object-diagram



#### 参考

https://www.tutorialspoint.com/uml/index.htm

https://www.cs.uah.edu/~rcoleman/Common/SoftwareEng/UML.html

## 参考

- https://www.tutorialspoint.com/uml/index.htm
- https://plantuml.com/zh/object-diagram
