---
aliases:
- 发布-订阅
- Observer Pattern
confidentiality: public
domain: computer-science
evidence:
- claim: 观察者模式是一种软件设计模式，其中一个对象被称为主题（subject）。
  claim_id: observer-pattern-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-334b0ce05d11
    exact: the observer pattern is a software design pattern in which an object, called
      the subject
  targets:
  - evidence_id: evidence-334b0ce05d11
    source_id: web-computer-science-observer-pattern
id: observer-pattern
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-observer-pattern
status: published
tags:
- design-pattern
- behavioral
- observer
title: 观察者模式
updated_at: '2026-09-06'
---
# 观察者模式

## 一句话结论

观察者模式定义了一种**一对多的依赖关系**：一个被称为**主题（Subject）**的对象维护一份**观察者（Observer）**列表，并在自身状态变化时**自动通知**所有观察者（典型做法是调用它们的更新方法）。它让"被观察对象"与"依赖对象"不必紧耦合，同时满足"状态一变、所有依赖者自动同步更新"的需求。

## 核心概念

- **定义**：观察者模式是一种软件设计模式，其中主题（又称事件源/事件流）维护依赖者（观察者/事件汇）的列表，并在状态变化时自动通知它们，典型做法是调用它们的某个方法。
- **一对多依赖**：一个主题对应多个观察者；状态变化时所有观察者被自动更新。
- **标准化接口**：主题通过统一接口认识观察者，直接管理订阅列表，从而避免紧耦合。
- **同步直接耦合**：典型实现中主题直接调用观察者方法（同步、直接）；异步实现可通过事件队列。
- **与发布-订阅的区别**：观察者模式没有中间代理（broker），主题与观察者互相持有直接引用。

## 工作机制

- 定义 `Subject` 与 `Observer` 的标准化接口。
- 主题维护观察者列表，并管理注册/注销；状态变化时调用每个观察者的 `update()` 操作通知它们。
- 观察者负责向主题注册/注销自己（以便被通知），并在收到通知时更新自身状态以与主题状态同步。
- 通知通常是同步、直接的——主题直接调用观察者方法；也可用事件队列实现异步。
- 模式适用于事件驱动的数据处理：数据到达不可预测（用户输入、HTTP 请求、GPIO 信号、分布式数据库更新、GUI 模型变化等）。

## 示例或代码

经典场景：GUI 工具包 / MVC 框架中的事件处理——模型（主题）变化时，多个视图（观察者）自动刷新。

Python 示意：

```python
class Subject:
    def __init__(self):
        self._observers = []
        self._state = None
    def attach(self, observer):            # 注册观察者
        self._observers.append(observer)
    def detach(self, observer):            # 注销观察者
        self._observers.remove(observer)
    def notify(self):                      # 状态变化时自动通知
        for obs in self._observers:
            obs.update(self)
    def set_state(self, value):
        self._state = value
        self.notify()

class Observer:
    def update(self, subject):             # 观察者更新接口
        print(f"observed state: {subject._state}")

subj = Subject()
subj.attach(Observer())
subj.attach(Observer())
subj.set_state("changed")                  # 两个观察者都会被通知
```

## 常见误区

- **把观察者模式等同于发布-订阅**：观察者模式是"直接引用 + 同步调用"，无中间代理；发布-订阅才有 broker、松耦合、异步分发。
- **忽略注销机制**：观察者忘记注销会导致内存泄漏（订阅对象被意外持有）。
- **滥用导致更新风暴/级联通知**：观察者链过长、无环检测时会引发难以排查的连锁更新。
- **误以为必须是异步**：典型观察者模式是同步直接的，异步是可选扩展。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| observer-pattern-definition | web-computer-science-observer-pattern | 主题维护观察者列表并自动通知状态变化，通过标准化接口管理订阅，避免紧耦合 |

## 待验证项

无。英文定义直接来自 Wikipedia《Observer pattern》条目，已锚定原文逐字引文。

## 关联知识

- [[mediator-pattern]] —— 中介者把对象间交互集中到中介对象；观察者则是主题-观察者直连通知。
- [[command-pattern]] —— 事件处理系统中常把请求封装为命令，再经观察者机制派发。
- [[software-design]] —— 行为型模式在 23 种 GoF 模式中的定位。
- [[object-oriented]] —— 面向对象接口与多态，是观察者模式的实现基础。

## 详细章节

### 定义

在软件设计与软件工程中，观察者模式是一种软件设计模式：一个称为**主题（subject，又称事件源或事件流）**的对象，维护一份其**依赖者（observers，又称事件汇）**的列表，并在状态变化时自动通知它们，典型做法是调用它们的某个方法。主题通过标准化接口认识观察者，并直接管理订阅列表。

观察者模式是 23 个著名的"四人组"（Gang of Four）设计模式之一，用于解决反复出现的设计难题，目标是设计灵活、可复用的面向对象软件，产出更易于实现、变更、测试和复用的对象。

### 参与者

- **Subject（主题）**：维护观察者列表，提供注册/注销接口，状态变化时通知所有观察者。
- **Observer（观察者）**：定义 `update()` 接口，接收主题的通知并同步自身状态。
- **ConcreteSubject（具体主题）**：持有具体状态，状态变化时触发通知。
- **ConcreteObserver（具体观察者）**：实现 `update()`，维护与主题状态一致的自身状态。

### 结构

- 主题持有一组观察者引用（一对多），通过抽象接口 `Observer` 认识它们。
- 观察者向主题注册/注销；主题状态变化时遍历列表调用 `update()`。
- 依赖关系建立后，主题无需知道观察者的具体类型，观察者也只依赖主题的公开接口。
- 运行时对象数量可增减——新的观察者随时可订阅/退订。

### 适用场景

- 一个对象状态变化时需要同时更新一组依赖对象，且依赖者数量开放（可增可减）。
- 需要在不使对象紧耦合的前提下建立一对多依赖。
- 事件驱动系统：GUI 事件处理、MVC 中模型-视图同步、消息驱动的运行时。
- 数据到达不可预测的场景（用户输入、网络请求、传感器信号、分布式更新等）。

### 优缺点

优点：

- 主题与观察者松耦合——主题只依赖抽象接口，观察者只依赖主题公开接口。
- 支持广播通信：一个状态变化自动通知所有订阅者。
- 符合开闭原则：新增观察者无需修改主题。
- 观察者可独立注册/注销，运行时灵活调整。

缺点：

- 直接引用 + 同步调用造成"隐式"依赖，难以追踪完整调用链。
- 通知顺序不确定；观察者更新异常可能影响主题。
- 注册/注销管理不当会泄漏内存（GC 语言中的强引用保留）。
- 级联通知可能引入性能与调试问题。

### 与相关模式关系

- **与发布-订阅（架构模式）**：观察者模式无 broker、直接耦合；发布-订阅通过消息总线/事件管理器解耦双方。
- **与中介者模式**：观察者是"一对多、被观察者广播"；中介者集中"多对多"交互，对象间不直接通信。
- **与命令模式**：观察者可配合命令模式，把通知内容封装为命令对象以便撤销/队列化。

## 参考

https://en.wikipedia.org/wiki/Observer_pattern
