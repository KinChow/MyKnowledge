---
aliases:
- 中介者
- Mediator Pattern
confidentiality: public
domain: computer-science
evidence:
- claim: 中介者模式定义了一个对象来封装一组对象之间的交互方式。
  claim_id: mediator-pattern-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-8ceb83051de3
    exact: the mediator pattern defines an object that encapsulates how a set of objects
      interact
  targets:
  - evidence_id: evidence-8ceb83051de3
    source_id: web-computer-science-mediator-pattern
id: mediator-pattern
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-mediator-pattern
status: published
tags:
- design-pattern
- behavioral
- mediator
title: 中介者模式
updated_at: '2026-09-06'
---
# 中介者模式

## 一句话结论

中介者模式**定义一个中介对象来封装一组对象之间如何交互**，让这些对象不再**彼此显式引用**，而是统一通过中介者通信。它把"多对多"的网状依赖收敛为"多对一"的星状依赖，从而**降低耦合**，并使对象间的交互可以被独立地变化。注意：它与"代理/中间件（Broker）"模式不是一回事。

## 核心概念

- **定义**：中介者模式定义一个对象来封装一组对象如何交互；被视为行为型模式，因为它能改变程序的运行行为。
- **促进松耦合**：通过让对象不显式引用彼此来降低耦合，允许交互独立变化。
- **星状通信**：对象不再直接通信，而是通过中介者间接通信；中介者控制与协调交互。
- **角色**：Mediator（中介者）、ConcreteMediator（具体中介者）、Colleague（同事对象）。
- **区别于 Broker**：中介者模式与"代理/中间件模式"不要混淆。

## 工作机制

- 定义一个独立的（中介者）对象，封装一组对象之间的交互。
- 各对象把交互委托给中介者，而不是彼此直接交互。
- 对象通过中介者间接交互，中介者负责控制与协调整个交互过程。
- 对象只认识并引用中介者，彼此没有显式知识，从而松耦合。
- 客户端可用中介者向其他客户端发消息，也可通过中介者上的事件接收消息。

## 示例或代码

经典场景：聊天室（聊天室 = 中介者，用户 = 同事）、GUI 中多个控件协调、航班调度塔台。

Python 示意：

```python
class ChatRoom:                        # Mediator 中介者
    def __init__(self):
        self._users = {}
    def register(self, user):
        self._users[user.name] = user
    def send(self, message, sender, to=None):
        if to:
            self._users[to].receive(message, sender)
        else:                          # 广播给所有人
            for u in self._users.values():
                if u.name != sender:
                    u.receive(message, sender)

class User:                            # Colleague 同事
    def __init__(self, name, room):
        self.name = name
        self._room = room
        self._room.register(self)
    def send(self, message, to=None):
        self._room.send(message, self.name, to)
    def receive(self, message, sender):
        print(f"{self.name} got from {sender}: {message}")

room = ChatRoom()
alice, bob = User("alice", room), User("bob", room)
alice.send("hi bob", to="bob")         # 用户不直接互相引用
```

## 常见误区

- **与 Broker/代理模式混淆**：中介者是"对象间通信的中枢协调者"；Broker 是消息路由/中间件，二者关注点不同。
- **把中介者写成"上帝对象"**：所有逻辑都塞进中介者会让它成为新的维护热点，需要控制复杂度。
- **在对象数量少、交互简单时强行使用**：简单直连足够时，引入中介者是过度设计。
- **忽略"交互可独立变化"的价值**：中介者模式的意义在于交互规则集中、可独立演进。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| mediator-pattern-definition | web-computer-science-mediator-pattern | 中介者封装一组对象的交互方式，对象不显式彼此引用，从而松耦合、交互可独立变化 |

## 待验证项

无。英文定义直接来自 Wikipedia《Mediator pattern》条目，已锚定原文逐字引文。

## 关联知识

- [[observer-pattern]] —— 观察者是"主题-观察者"直接通知；中介者集中"多对多"交互。
- [[facade-pattern]]（结构型）—— 门面封装子系统对外接口；中介者协调子系统内部交互，二者常被对比。
- [[software-design]] —— 行为型模式在 23 种 GoF 模式中的定位。
- [[object-oriented]] —— 松耦合设计原则的实现之一。

## 详细章节

### 定义

在软件工程中，中介者模式定义一个对象来**封装一组对象之间如何交互**。它被视为行为型模式，因为它能改变程序的运行行为。中介者模式的本质是"定义一个封装一组对象如何交互的对象"，它通过让对象不显式引用彼此来促进松耦合，并允许交互被独立地变化。客户端类可用中介者向其他客户端发送消息，也可通过中介者上的事件接收消息。

在中介者模式下，对象间的通信被封装进中介者对象：对象不再直接通信，而是通过中介者通信。这减少了通信对象间的依赖，从而降低耦合。

### 参与者

- **Mediator（中介者接口）**：定义同事对象通信的接口。
- **ConcreteMediator（具体中介者）**：实现协调逻辑，维护并协调各同事对象，控制交互。
- **Colleague（同事接口/基类）**：定义各同事对象与中介者通信的接口；持有中介者引用。
- **ConcreteColleague（具体同事）**：实现自身行为，需要交互时委托给中介者。

### 结构

- 同事对象只引用中介者，彼此不直接引用（从网状耦合收敛为星状）。
- 中介者引用所有同事对象，负责消息分发与交互协调。
- 交互流程：同事 A → 中介者（转发/协调）→ 同事 B。
- 交互规则集中在中介者中，可独立变化而不影响各同事对象。

### 适用场景

- 一组对象之间存在复杂网状交互，直接引用导致耦合过高。
- 希望集中控制与协调交互规则，便于统一修改。
- 需要复用对象而不复用其交互关系。
- 交互逻辑复杂到应该被独立封装/测试时。

### 优缺点

优点：

- 降低对象间耦合，从多对多退化为多对一。
- 交互集中，符合单一职责，便于修改与测试。
- 提高对象可复用性（对象不再依赖具体交互伙伴）。
- 简化对象协议。

缺点：

- 中介者可能变得庞大复杂（"上帝对象"风险）。
- 对象间交互过多依赖中介者，中介者成为单点。
- 新增中介者/交互类型时需同步维护。

### 与相关模式关系

- **与观察者模式**：观察者是"一对多、被观察者主动通知"；中介者是"多对多、交互集中协调"。中介者内部可借助观察者机制实现通知。
- **与门面（Facade）模式**：门面对外提供统一接口（单向）；中介者协调内部对象间交互（双向）。
- **与代理/中间件（Broker）**：中介者是进程内协调者；Broker 是消息路由中间件，二者注意区分。

## 参考

https://en.wikipedia.org/wiki/Mediator_pattern
