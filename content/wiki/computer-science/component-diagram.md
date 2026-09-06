---
aliases: []
confidentiality: public
domain: computer-science
evidence:
- claim: PlantUML 支持用简单直观的文本描述创建组件图。
  claim_id: component-diagram-claim-1
  support: direct
  supporting_quotes:
  - evidence_id: evidence-6f35d0c7a293
    exact: 使用 PlantUML，您可以使用简单直观的文本描述来创建组件图
  targets:
  - evidence_id: evidence-6f35d0c7a293
    source_id: web-computer-science-component-diagram
- claim: 在 PlantUML 中，组件必须用中括号括起来，也可以用 component 定义组件。
  claim_id: component-diagram-claim-2
  support: direct
  supporting_quotes:
  - evidence_id: evidence-0d168b7dd5c5
    exact: 组件必须用中括号括起来。component定义一个组件。
  targets:
  - evidence_id: evidence-0d168b7dd5c5
    source_id: web-computer-science-component-diagram
- claim: 在 PlantUML 中，可以用关键字 as 给组件定义别名，并在稍后定义关系时使用。
  claim_id: component-diagram-claim-3
  support: direct
  supporting_quotes:
  - evidence_id: evidence-b66f23103eae
    exact: '并且可以用关键字as给组件定义一个别名。

      这个别名可以在稍后定义关系的时候使用。'
  targets:
  - evidence_id: evidence-b66f23103eae
    source_id: web-computer-science-component-diagram
- claim: 在 PlantUML 中，可以用 interface 关键字定义接口，并可用 as 定义别名。
  claim_id: component-diagram-claim-4
  support: direct
  supporting_quotes:
  - evidence_id: evidence-3c6199ce1cd9
    exact: 'interface关键字来定义接口。

      并且还可以使用关键字as定义一个别名。'
  targets:
  - evidence_id: evidence-3c6199ce1cd9
    source_id: web-computer-science-component-diagram
id: component-diagram
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-component-diagram
- working-computer-science-component-diagram
status: published
tags:
- uml
- component-diagram
- diagram
title: 组件图
updated_at: '2026-09-06'
---
# 组件图

## 一句话结论

组件图（又称构件图）是**组件及组件之间关系的集合**，表示系统的**实现视图**：在设计阶段把软件工件（类、接口等）按关系安排到不同组件中，用于可视化组件之间的组织与依赖关系，从而制作可执行系统。

## 核心概念

- **定义**：组件图是组件及组件之间关系的集合，这些组件由类、接口或协作组成。
- **实现视图**：组件图表示系统的实现视图。
- **物理方面**：组件图用于对系统的物理方面建模——驻留在节点中的元素，如可执行文件、库、文件、文档等。

## 工作机制

- 在设计阶段，系统的软件工件（类、接口等）根据它们之间的关系被安排在不同的组件中。
- 组件图用于可视化系统中组件之间的组织和关系，用于制作可执行系统。
- 用途：可视化系统的组件、使用正向和逆向工程构建可执行文件、描述组件的组织和关系。
- 使用场景：对系统的组件建模、为数据库模式建模、为应用程序的可执行文件建模、对系统的源代码建模。

## 示例或代码

PlantUML 组件图语法要点：

- 使用简单直观的文本描述创建组件图。
- 组件必须用中括号括起来（如 `[组件名]`），也可以用 `component` 关键字定义一个组件。
- 可以用关键字 `as` 给组件定义别名，稍后定义关系时使用该别名。
- 用 `interface` 关键字定义接口，也可以用 `as` 定义别名。

绘制工具参考：https://plantuml.com/zh/component-diagram

## 常见误区

- **“组件图就是类图”**：组件图表示系统的实现视图，描述代码构件的物理结构与依赖关系；类图是静态结构视图，二者视角不同。
- **“组件图用于描述运行时硬件”**：物理节点/硬件拓扑属于部署图的范畴；组件图关注可执行文件、库等软件工件。

## 证据映射

| claim_id | 来源 | 要点 |
| --- | --- | --- |
| component-diagram-claim-1 | web-computer-science-component-diagram | PlantUML 可用简单直观的文本描述创建组件图 |
| component-diagram-claim-2 | web-computer-science-component-diagram | 组件必须用中括号括起来，也可用 component 定义 |
| component-diagram-claim-3 | web-computer-science-component-diagram | 可用 as 给组件定义别名，供稍后定义关系使用 |
| component-diagram-claim-4 | web-computer-science-component-diagram | 可用 interface 定义接口，并用 as 定义别名 |

## 待验证项

无。

## 关联知识

- [[uml]] —— UML 总论，组件图属结构图（实现视角）。
- [[deployment-diagram]] —— 部署图描述组件部署到的物理节点。
- [[software-modeling]] —— 软件建模中的实现建模。

## 详细章节

### 组件图

组件图是组件及组件之间关系的集合。这些组件由类、接口或协作组成。

组件图表示系统的实现视图。

在设计阶段，系统的软件工件（类、接口等）根据它们之间的关系被安排在不同的组件中。

组件图用于对系统的物理方面进行建模。物理方面是驻留在节点中的元素，例如可执行文件、库、文件、文档等。

组件图用于可视化系统中组件之间的组织和关系，用于制作可执行系统。



#### 目的

- 可视化系统的组件。
- 使用正向和逆向工程构建可执行文件。
- 描述组件的组织和关系。



#### 哪里使用

- 对系统的组件进行建模。
- 为数据库模式建模。
- 为应用程序的可执行文件建模。
- 对系统的源代码进行建模。



#### 如何绘制

https://plantuml.com/zh/component-diagram



#### 参考

https://www.tutorialspoint.com/uml/index.htm

https://www.cs.uah.edu/~rcoleman/Common/SoftwareEng/UML.html

## 参考

- https://www.tutorialspoint.com/uml/index.htm
- https://plantuml.com/zh/component-diagram
