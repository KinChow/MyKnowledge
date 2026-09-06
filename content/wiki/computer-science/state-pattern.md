---
aliases:
- 状态机模式
- State Pattern
confidentiality: public
domain: computer-science
evidence:
- claim: 状态模式是一种行为型软件设计模式，允许对象在内部状态改变时改变其行为。
  claim_id: state-pattern-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-2a74aa5b6462
    exact: The state pattern is a behavioral software design pattern that allows an
      object to alter its behavior when its internal state changes
  targets:
  - evidence_id: evidence-2a74aa5b6462
    source_id: web-computer-science-state-pattern
id: state-pattern
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-state-pattern
status: published
tags:
- design-pattern
- behavioral
- state
title: 状态模式
updated_at: '2026-09-06'
---
# 状态模式

## 一句话结论

状态模式是一种**行为型设计模式**，它让一个对象在**内部状态改变时自动改变自己的行为**，看起来就像"换了一个类"。它把每个状态对应的行为封装成独立的状态对象，上下文（Context）把状态相关行为**委托**给当前状态对象，从而避免大量条件分支，行为可随状态动态切换。

## 核心概念

- **定义**：状态模式是一种行为型软件设计模式，允许对象在内部状态改变时改变其行为。
- **与有限状态机的关系**：模式与有限状态机的概念非常接近。
- **与策略模式的关系**：状态模式可被解释为一种"能够通过模式接口中定义的方法调用切换策略"的策略模式。
- **委托给状态对象**：上下文把状态特定行为委托给不同的 `State` 对象。
- **封装变化行为**：用独立状态对象封装同一对象在不同内部状态下的变化行为，避免条件语句、提升可维护性。

## 工作机制

- 上下文（Context）持有对某个状态对象的引用，该引用代表"当前状态"。
- 上下文把状态相关行为委托给当前状态对象（例如 `handle(this)`）。
- 状态对象在完成操作后可调用上下文的 `setState(...)` 改变上下文的当前状态，从而切换到下一个状态。
- 新增状态只需定义新的状态类；运行时通过替换当前状态对象改变对象行为。
- 上下文不直接实现状态特定行为，因此与"如何实现状态行为"解耦。

## 示例或代码

经典例子：TCP 连接、文档编辑器的草稿/已发布状态、订单状态流转。以"开关灯"为例，灯在开/关两种状态下行为不同。

Python 示意（电风扇风量切换：停止→低→高→停止）：

```python
class Fan:
    def __init__(self):
        self._state = OffState()
    def set_state(self, state):
        self._state = state
        print(f"-> {state.__class__.__name__}")
    def pull(self):              # 委托给当前状态，状态负责切换
        self._state.pull(self)

class State:
    def pull(self, fan): ...

class OffState(State):
    def pull(self, fan):
        fan.set_state(LowState())

class LowState(State):
    def pull(self, fan):
        fan.set_state(HighState())

class HighState(State):
    def pull(self, fan):
        fan.set_state(OffState())

fan = Fan()
fan.pull()   # -> LowState
fan.pull()   # -> HighState
fan.pull()   # -> OffState
```

## 常见误区

- **与策略模式混淆**：状态模式的切换由**对象内部状态变化**驱动；策略模式由**客户端选择**驱动，状态对象不负责切换。
- **把状态机逻辑写死在上下文**：那正是模式要消除的条件语句堆砌。
- **状态对象共享与并发**：无状态化/共享状态对象时需注意线程安全。
- **误以为状态转换只发生在状态对象内部**：转换也可由上下文决定，关键是职责归属要清晰。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| state-pattern-definition | web-computer-science-state-pattern | 状态模式允许对象在内部状态改变时改变行为，接近有限状态机，可视为可切换策略的策略模式 |

## 待验证项

无。英文定义直接来自 Wikipedia《State pattern》条目，已锚定原文逐字引文。

## 关联知识

- [[strategy-pattern]] —— 状态模式可被解释为"能通过接口方法切换策略"的策略模式。
- [[statechart-diagram]] —— UML 状态图用于建模对象的状态与状态转移。
- [[software-design]] —— 行为型模式在 23 种 GoF 模式中的定位。
- [[object-oriented]] —— 多态委托是状态模式的实现基础。

## 详细章节

### 定义

状态模式是一种行为型软件设计模式，它允许一个对象在内部状态改变时改变其行为。该模式与有限状态机（finite-state machine）的概念非常接近。状态模式可被解释为一种策略模式——一种能够通过模式接口中定义的方法调用来切换策略的策略模式。

状态模式用于在计算机编程中封装"同一对象在不同内部状态下的变化行为"。与退回到条件语句相比，它是对象在运行时改变行为、并提升可维护性的更干净的方式。新状态可通过定义新状态类来添加；类可通过替换当前状态对象在运行时改变行为。

### 参与者

- **State（状态接口）**：定义状态特定行为的接口（如 `handle(context)`）。
- **ConcreteState（具体状态）**：实现接口，封装某个特定状态下的行为；可在操作后切换上下文的状态。
- **Context（上下文）**：持有当前状态对象引用，把状态特定行为委托给它；提供 `setState()` 以改变当前状态。
- **（可选）客户端**：触发上下文的状态相关操作。

### 结构

- 上下文不直接实现状态特定行为，而是引用 `State` 接口执行状态行为（`state.handle()`），使上下文与"状态行为如何实现"解耦。
- 具体状态类实现/封装各自状态下的行为。
- 运行时交互：上下文调用当前状态的 `handle(this)` → 状态执行操作并调用 `setState(...)` 改变上下文当前状态 → 下次调用时上下文使用新状态。

### 适用场景

- 对象行为随内部状态显著变化，且状态较多。
- 存在大量围绕同一对象状态的 if-else / switch 分支。
- 状态转换规则复杂，希望把每个状态及其转换内聚到独立类中。
- 希望新增状态不影响现有类（开闭原则）。

### 优缺点

优点：

- 状态特定行为被内聚封装，消除大量条件分支，提升可维护性。
- 符合开闭原则：新增状态只需新增状态类。
- 状态转换显式化、集中化，行为变化更易追踪。
- 上下文与状态行为解耦，职责清晰。

缺点：

- 状态多时类数量膨胀。
- 状态对象之间切换逻辑分散在多个状态类中，全局流程不易一览。
- 若状态需要共享数据，设计上需要额外协调。

### 与相关模式关系

- **与策略模式**：二者结构相同（都通过接口委托行为）；区别在驱动者——状态模式由内部状态变化驱动（状态可切换上下文），策略模式由客户端选择驱动。
- **与状态图（UML）**：状态模式是有限状态机的 OOP 实现，状态图为其建模工具。
- **与命令模式**：可结合使用——状态行为由命令触发，命令模式处理操作封装。

## 参考

https://en.wikipedia.org/wiki/State_pattern
