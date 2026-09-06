---
aliases: []
confidentiality: public
domain: computer-science
evidence:
- claim: PlantUML 中文部署图页面以“部署图”为标题，并提供部署图元素声明示例。
  claim_id: deployment-diagram-source
  support: direct
  supporting_quotes:
  - evidence_id: evidence-aa3141cb7913
    exact: '部署图

      声明元素

      [] 放置长描述文本。'
  targets:
  - evidence_id: evidence-aa3141cb7913
    source_id: web-computer-science-deployment-diagram
id: deployment-diagram
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-deployment-diagram
- working-computer-science-deployment-diagram
status: published
tags:
- uml
- deployment-diagram
- diagram
title: 部署图
updated_at: '2026-09-06'
---
# 部署图

## 一句话结论

部署图是**节点及节点之间关系的集合**，用于可视化系统的**部署视图**：描述系统物理组件的拓扑（硬件拓扑）与部署软件组件的物理实体，通常由部署团队使用，描述系统的静态部署视图。

## 核心概念

- **定义**：部署图是节点及节点之间关系的集合，这些节点是部署组件的物理实体。
- **部署视图**：部署图用于可视化系统的部署视图，通常由部署团队使用。
- **物理拓扑**：部署图用于可视化系统物理组件的拓扑，其中部署了软件组件。

## 工作机制

- 部署图描述系统的静态部署视图，由节点及其关系组成。
- 用途：可视化系统的硬件拓扑、描述用于部署软件组件的硬件组件、描述运行时处理节点。
- 使用场景：对系统的硬件拓扑建模、为嵌入式系统建模、为客户端/服务器系统建模硬件细节、对分布式应用程序的硬件细节建模、用于正向和逆向工程。

## 示例或代码

绘制工具参考：https://plantuml.com/zh/deployment-diagram

元素声明示例：`[]` 放置长描述文本。

## 常见误区

- **“部署图是描述软件模块的”**：部署图描述的是物理节点（硬件）及其上部署的软件组件的拓扑，属于物理部署视图；软件模块的组织由组件图表达。
- **“部署图用于展示运行时处理流程”**：部署图描述的是静态部署视图与硬件拓扑，而非运行时的动态流程。

## 证据映射

| claim_id | 来源 | 要点 |
| --- | --- | --- |
| deployment-diagram-source | web-computer-science-deployment-diagram | PlantUML 中文部署图页面以“部署图”为标题，提供声明元素示例（[] 放置长描述文本） |

## 待验证项

无。

## 关联知识

- [[uml]] —— UML 总论，部署图属结构图（部署视角）。
- [[component-diagram]] —— 部署图描述组件部署到的物理节点。
- [[software-modeling]] —— 软件建模中的部署建模。

## 详细章节

### 部署图

部署图是节点及节点之间关系的集合。这些节点是部署组件的物理实体。

部署图用于可视化系统的部署视图。通常由部署团队使用。

部署图用于可视化系统物理组件的拓扑，其中部署了软件组件。

部署图用于描述系统的静态部署视图。部署图由节点及其关系组成。



#### 目的

- 可视化系统的硬件拓扑。
- 描述用于部署软件组件的硬件组件。
- 描述运行时处理节点。



#### 哪里使用

- 对系统的硬件拓扑进行建模。
- 为嵌入式系统建模。
- 为客户端/服务器系统建模硬件细节。
- 对分布式应用程序的硬件细节进行建模。
- 用于正向和逆向工程。



#### 如何绘制

https://plantuml.com/zh/deployment-diagram



#### 参考

https://www.tutorialspoint.com/uml/index.htm

https://www.cs.uah.edu/~rcoleman/Common/SoftwareEng/UML.html

## 参考

- https://www.tutorialspoint.com/uml/index.htm
- https://plantuml.com/zh/deployment-diagram
