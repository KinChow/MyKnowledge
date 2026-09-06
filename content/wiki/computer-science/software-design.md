---
aliases: []
confidentiality: public
domain: computer-science
evidence:
- claim: '设计模式

    设计模式（Design pattern）代表了最佳的实践，通常被有经验的面向对象的软件开发人员所采用。设计模式是软件开发人员在软件开发过程中面临的一般问题的解决方案。这些解决方案是众多软件开发人员经过相当长的一段时间的试验和错误总结出来的。

    本教程将通过 Java 实例，一步一步向您讲解设计模式的概念。

    谁适合阅读本教程？

    无论您是新手，还是老手，本教程都值得一读。对于那些具有丰富的开发经验的开发人员，学习设计模式有助于了解在软件开发过程中所面临的问题的最佳解决方案；对于那些经验不足的开发人员，学习设计模式有助于通过一种简单快捷的方式来学习软件设计。

    阅读本教程前，您需要了解的知识：

    在您开始阅读本教程之前，您必须具备基本的 Java 编程的概念。如果您还不了解这些概念，那么建议您先阅读我们的 Java 教程。'
  claim_id: software-design-audit-1
  support: direct
  supporting_quotes:
  - evidence_id: evidence-26c0d56f8f5a
    exact: '设计模式

      设计模式（Design pattern）代表了最佳的实践，通常被有经验的面向对象的软件开发人员所采用。设计模式是软件开发人员在软件开发过程中面临的一般问题的解决方案。这些解决方案是众多软件开发人员经过相当长的一段时间的试验和错误总结出来的。

      本教程将通过 Java 实例，一步一步向您讲解设计模式的概念。

      谁适合阅读本教程？

      无论您是新手，还是老手，本教程都值得一读。对于那些具有丰富的开发经验的开发人员，学习设计模式有助于了解在软件开发过程中所面临的问题的最佳解决方案；对于那些经验不足的开发人员，学习设计模式有助于通过一种简单快捷的方式来学习软件设计。

      阅读本教程前，您需要了解的知识：

      在您开始阅读本教程之前，您必须具备基本的 Java 编程的概念。如果您还不了解这些概念，那么建议您先阅读我们的 Java 教程。'
  targets:
  - evidence_id: evidence-26c0d56f8f5a
    source_id: web-computer-science-software-design
id: software-design
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-software-design
- working-computer-science-software-design
status: published
tags:
- design-pattern
- oop
- software-design
- solid
title: 软件设计
updated_at: '2026-09-06'
---
# 软件设计

## 一句话结论

软件设计是**为一组或多组问题设想和定义软件解决方案的过程**，回答"要做什么、做成什么样、怎么去做"。它通过抽象、细化、模块化、信息隐藏等设计概念组织软件结构，以设计原则（正交四原则、SOLID、DRY、KISS、YAGNI、LOD）和设计模式（创建型/结构型/行为型）为工具，最终目标是更容易实现**高内聚低耦合**。

## 核心概念

- **抽象**：对可观测对象信息进行概括，表示基本特征而不包括背景细节或解释。
- **细化**：细节化的过程；层次结构通过逐步分解宏观语句开发，直到达到编程语言语句。抽象与细化是互补概念。
- **模块化**：软件架构分为称为模块的组件。
- **软件架构**：软件的整体结构，为系统提供概念完整性，良好架构在性能、质量、进度、成本上带来良好投资回报。
- **控制层次**：表示程序组件组织的程序结构。
- **结构分区**：程序结构分水平（每个主要功能单独分支）与垂直（控制和工作自上而下分布）。
- **数据结构**：数据各元素之间逻辑关系的表示。
- **信息隐藏**：不需要此类信息的其他模块无法访问该模块中包含的信息。
- **高内聚低耦合**：所有设计原则和设计模式都是为了更容易实现的目标。

## 工作机制

设计软件时需从多个方面权衡以满足目标和期望，包括：

- **兼容性**：软件能与其互操作的其他产品一起运行（如兼容旧版本）。
- **可扩展性**：无需对底层架构重大更改即可添加新功能。
- **模块化**：包含定义明确的独立组件，可独立实施和测试，便于工作分工。
- **容错**：能抵抗组件故障并从故障中恢复。
- **可维护性**：衡量错误修复或功能修改的难易程度，常是模块化和可扩展性的产物。
- **可靠性**：软件在规定的条件下执行所需功能。
- **可重用性**：其他项目中几乎无需修改即可使用现有软件的部分或全部功能。
- **鲁棒性**：在压力下运行、容忍不可预测和无效输入。
- **安全性**：承受和抵抗敌对行为与影响。
- **可用性**：用户界面必须对目标用户/受众可用。
- **性能**：在用户可接受的时间范围内执行任务且不需太多内存。
- **可移植性**：在不同条件和环境中使用。
- **可扩展性**：适应不断增加的数据、功能和用户数量。

## 示例或代码

设计模式的经典分类（以 Java 教程为例）：

- **创建型**：隐藏对象创建逻辑而非用 `new` 直接实例化——单例、工厂、抽象工厂、建造者、原型。
- **结构型**：关注类和对象的组合，用继承组合接口并定义组合对象获得新功能——代理、桥接、装饰器、适配器、门面、组合、享元。
- **行为型**：关注对象之间的通信——观察者、模板、策略、职责链、迭代器、状态、访问者、备忘录、命令、解释器、中介。

## 常见误区

- **把"软件设计"等同于"画图/写文档"**：软件设计是一组面向目标的决策过程，回答要做什么、做成什么样、怎么做，不只是产出设计图。
- **忽略非功能性的"设计考虑"**：只关注功能而忽视性能、可扩展性、可维护性、鲁棒性等维度，会导致架构脆弱。
- **把设计原则与设计模式混为一谈**：原则（如 SOLID、DRY）是指导方针，模式（如单例、策略）是可复用解决方案；原则是模式之上的思想。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| software-design-audit-1 | web-computer-science-software-design | 设计模式代表了最佳实践，是软件开发人员在开发过程中面临的一般问题的解决方案，由众多开发者长期试验总结而来 |

## 待验证项

无。

## 关联知识

- [[common-performance-design-patterns]] —— 性能设计模式：五元组模板与四大原则—十二大模式。
- [[solid]] —— SOLID 五原则详解。
- [[orthogonal-design-principles]] —— 正交设计四原则。
- [[object-oriented]] —— 面向对象分析与设计、四大特性。
- [[four-rules-of-simple-design]] —— 简单设计四原则。
- [[lod]] —— LOD（迪米特法则/最少知识原则）。
- [[refactoring-concepts-and-principles]] —— 重构概念与原则。
- [[uml]] —— 软件建模与 UML 图。

## 详细章节

### 软件设计

#### 概述

软件设计是为一组或多组问题设想和定义软件解决方案的过程。

回答以下问题：

- 要做什么？
- 做成什么样？
- 怎么去做？



#### 概念

设计概念为软件设计者提供了应用更复杂方法的基础。

* 抽象
  * 抽象是对可观测对象信息进行概括的过程或结果。这是一种表示基本特征的行为，而不包括背景细节或解释。
* 细化
  * 细节化的过程。
  * 层次结构是通过逐步分解功能的宏观语句来开发的，直到达到编程语言语句。在每个步骤中，将给定程序的一条或几条指令分解为更详细的指令。
  * 抽象和细化是互补的概念。
* 模块化
  * 软件架构分为称为模块的组件。
* 软件架构
  * 软件的整体结构以及该结构为系统提供概念完整性。良好的软件架构将在项目预期结果产生良好的投资回报，例如在性能、质量、进度和成本方面。
* 控制层次
  * 一种程序结构，表示程序组件的组织，并暗示了控制层次。
* 结构分区
  * 程序结构可以分为水平和垂直两种。
    * 水平分区为每个主要程序功能定义了模块化层次的单独分支。
    * 垂直分区表明控制和工作应该在程序结构中自上而下分布。
* 数据结构
  * 数据各个元素之间逻辑关系的表示。
* 软件程序
  * 它侧重于单独处理每个模块。
* 信息隐藏
  * 不需要此类信息的其他模块无法访问该模块中包含的信息。



#### 设计考虑

设计软件时，需要考虑很多方面，这些方面反映创建软件要满足的目标和期望。

* 兼容性
  * 该软件能够与其互操作的其他产品一起运行。例如，一个软件需要兼容其旧版本。
* 可扩展性
  * 无需对底层架构进行重大更改即可将新功能添加到软件中。
* 模块化
  * 生成的软件包含定义明确的独立组件，可带来更好的可维护性。在集成到目标软件系统之前，这些组件可以独立地被实施和测试。这允许在软件开发项目中进行工作分工。
* 容错
  * 软件能够抵抗组件故障并能够从组件故障中恢复。
* 可维护性
  * 衡量错误修复或功能修改的难易程度。高可维护性可以是模块化和可扩展性的产物。
* 可靠性（软件耐久性）
  * 软件能够在规定的条件下，执行所需的功能。
* 可重用性
  * 在其他项目中如果使用现有软件的部分或全部功能，几乎不需要修改。
* 鲁棒性
  * 软件能够在压力下运行、容忍不可预测和无效的输入。
* 安全性
  * 软件能够承受和抵抗敌对行为和影响。
* 可用性
  * 软件用户界面必须对其目标用户/受众可用。参数的默认值设定为对大多数用户来说是一个不错的选择。
* 性能
  * 软件在用户可接受的时间范围内执行其任务，并且不需要太多内存。
* 可移植性
  * 软件应该可以在不同的条件和环境中使用。
* 可扩展性
  * 软件能够很好地适应不断增加的数据、功能和用户数量。



#### 设计目的

所有设计原则和设计模式都是为了更容易实现**高内聚低耦合**。



#### 设计原则

* [正交四原则](./design-principles/正交四原则.md)
* [SOLID原则](./design-principles/SOLID.md)
* [DRY原则](./design-principles/DRY.md)
* [KISS原则](./design-principles/KISS.md)
* [YAGNI原则](./design-principles/YAGNI.md)
* [LOD原则](./design-principles/LOD.md)



#### 设计模式

设计模式是软件开发人员在软件开发过程中面临的一般问题的解决方案。这些解决方案是众多软件开发人员经过相当长的一段时间的试验和错误总结出来的。

##### 创建型

这些设计模式提供了一种在创建对象的同时隐藏创建逻辑的方式，而不是使用 new 运算符直接实例化对象。这使得程序在判断针对某个给定实例需要创建哪些对象时更加灵活。

* [单例模式](./design-patterns/creational-patterns/singleton-pattern.md)
* [工厂模式](./design-patterns/creational-patterns/factory-pattern.md)
* [抽象工厂模式](./design-patterns/creational-patterns/abstract-factory-pattern.md)
* [建造者模式](./design-patterns/creational-patterns/builder-pattern.md)
* [原型模式](./design-patterns/creational-patterns/prototype-pattern.md)



##### 结构型

这些设计模式关注类和对象的组合。继承的概念被用来组合接口和定义组合对象获得新功能的方式。

* [代理模式](./design-patterns/structural-patterns/proxy-pattern.md)
* [桥接模式](./design-patterns/structural-patterns/bridge-pattern.md)
* [装饰器模式](./design-patterns/structural-patterns/decorator-pattern.md)
* [适配器模式](./design-patterns/structural-patterns/adapter-pattern.md)
* [门面模式](./design-patterns/structural-patterns/facade-pattern.md)
* [组合模式](./design-patterns/structural-patterns/composite-pattern.md)
* [享元模式](./design-patterns/structural-patterns/flyweight-pattern.md)



##### 行为型

这些设计模式特别关注对象之间的通信。

* [观察者模式](./design-patterns/behavioral-patterns/observer-pattern.md)
* [模板模式](./design-patterns/behavioral-patterns/template-pattern.md)
* [策略模式](./design-patterns/behavioral-patterns/strategy-pattern.md)
* [职责链模式](./design-patterns/behavioral-patterns/chain-of-responsibility-pattern.md)
* [迭代器模式](./design-patterns/behavioral-patterns/iterator-pattern.md)
* [状态模式](./design-patterns/behavioral-patterns/state-pattern.md)
* [访问者模式](./design-patterns/behavioral-patterns/visitor-pattern.md)
* [备忘录模式](./design-patterns/behavioral-patterns/memento-pattern.md)
* [命令模式](./design-patterns/behavioral-patterns/command-pattern.md)
* [解释器模式](./design-patterns/behavioral-patterns/interpreter-pattern.md)
* [中介模式](./design-patterns/behavioral-patterns/mediator-pattern.md)



#### 参考

https://en.wikipedia.org/wiki/Software_design#Design_patterns

https://www.runoob.com/design-pattern/design-pattern-tutorial.html
