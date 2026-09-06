---
aliases:
- 责任链
- 职责链模式
- Chain of Responsibility Pattern
confidentiality: public
domain: computer-science
evidence:
- claim: 责任链模式是一种行为型设计模式，由一个命令对象源和一系列处理对象组成。
  claim_id: chain-of-responsibility-pattern-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-7da1c940faf7
    exact: the chain-of-responsibility pattern is a behavioral design pattern consisting
      of a source of command objects and a series of processing objects
  targets:
  - evidence_id: evidence-7da1c940faf7
    source_id: web-computer-science-chain-of-responsibility-pattern
id: chain-of-responsibility-pattern
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-chain-of-responsibility-pattern
status: published
tags:
- design-pattern
- behavioral
- chain-of-responsibility
title: 责任链模式
updated_at: '2026-09-06'
---
# 责任链模式

## 一句话结论

责任链模式把**请求的发送者与接收者解耦**：一串**处理对象**排成链，每个处理对象决定是自己处理该请求、还是把它**转发给链上的下一个处理对象**。发送者无需知道具体由谁处理，请求沿链传递直到某个处理器接住（或链尾无人处理）。它促进**松耦合**，并支持在运行时动态调整责任链。

## 核心概念

- **定义**：责任链模式是一种行为型设计模式，由"命令对象源 + 一系列处理对象"组成。
- **处理逻辑**：每个处理对象包含定义其能处理哪些类型命令对象的逻辑；其余的传给链中下一个处理对象。
- **可扩展链**：存在向链尾追加新处理对象的机制。
- **松耦合**：发送者与接收者解耦，不依赖特定处理器。
- **与装饰器模式的区别**：装饰器中所有类都处理请求；责任链中（严格定义下）**恰好一个**类处理请求。但很多实现（日志、UI 事件、Servlet Filter）允许多个元素共同承担责任。

## 工作机制

- 定义"接收者对象链"，链上每个节点依据**运行时条件**决定：处理该请求，或转发给链中下一个接收者（若有）。
- 请求沿链传递，直到某个接收者处理它。
- 发送者不再与特定接收者耦合——它把请求发给"这条链"即可。
- 可在运行时增删节点，动态调整处理职责。
- 现实例子：视图收到无法处理的事件时派发给其 superview，一路传到 view controller / window，最后到 application 对象（链尾）。

## 示例或代码

经典场景：日志系统（DEBUG→INFO→ERROR 逐级处理/上报）、Java Servlet Filter、UI 事件冒泡。

Python 示意（日志级别责任链）：

```python
class Logger:                        # Handler 处理器
    def __init__(self, level, successor=None):
        self._level = level
        self._successor = successor  # 链中的下一个
    def handle(self, msg, level):
        if level <= self._level:     # 自己能处理
            print(f"[{self._level}] {msg}")
        elif self._successor:
            self._successor.handle(msg, level)  # 转发给下一个

# 组装链：DEBUG -> INFO -> ERROR
chain = Logger("DEBUG", Logger("INFO", Logger("ERROR")))
chain.handle("debug msg", 1)    # 被 DEBUG 处理
chain.handle("info msg", 2)     # DEBUG 不处理，转发给 INFO
chain.handle("error msg", 3)    # 一路转发到 ERROR
```

## 常见误区

- **把责任链当装饰器**：装饰器让**所有**节点处理请求（层层包装）；责任链（严格 GoF 定义）让**恰好一个**节点处理。
- **忽略链尾处理**：无人能处理时应有兜底策略（丢弃/默认处理/报错）。
- **链过长影响性能/可调试性**：请求沿途传递，长链有额外开销，需记录链上各节点。
- **处理对象职责不清**：每个节点必须明确"我处理什么、我转发什么"。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| chain-of-responsibility-pattern-definition | web-computer-science-chain-of-responsibility-pattern | 责任链由命令对象源与处理对象链组成，处理对象决定自处理或转发，促进松耦合 |

## 待验证项

无。英文定义直接来自 Wikipedia《Chain-of-responsibility pattern》条目，已锚定原文逐字引文。

## 关联知识

- [[command-pattern]] —— 责任链传递的"请求"常封装为命令对象。
- [[observer-pattern]] —— UI 事件处理既可用责任链（冒泡）也可用观察者（监听）。
- [[software-design]] —— 行为型模式在 23 种 GoF 模式中的定位。
- [[object-oriented]] —— 多态与解耦是责任链的实现基础。

## 详细章节

### 定义

在面向对象设计中，责任链模式是一种行为型设计模式，由一个**命令对象源**与一系列**处理对象**组成。每个处理对象包含定义它能够处理哪些类型命令对象的逻辑；其余的传给链中下一个处理对象。链尾存在添加新处理对象的机制。该模式促进松耦合。

责任链模式在结构上与装饰器模式几乎相同，区别在于：装饰器中所有类都处理请求；而责任链（严格 GoF 定义）中**恰好一个**链上类处理请求。然而，很多实现（如日志器、UI 事件处理、Java Servlet Filter 等）允许多个链上元素共同承担责任。

责任链模式是 23 个著名 GoF 设计模式之一。它解决的问题：避免"请求发送者与接收者耦合"；支持"多个接收者都可能处理同一请求"。

### 参与者

- **Handler（处理者接口）**：定义处理请求的接口，并持有对下一个处理者的引用。
- **ConcreteHandler（具体处理者）**：实现处理逻辑，依据条件决定自己处理或转发给后继者。
- **Client（客户端）**：把请求发给链首（无需知道具体由谁处理）。

### 结构

- 处理者对象通过"后继引用"串成链（链表式结构）。
- 请求从链首进入，逐节点传递，直到某节点处理或到达链尾。
- 链的组装可由客户端或配置完成，运行时可变。

### 适用场景

- 请求的发送者与接收者需要解耦，接收者可能动态变化。
- 多个对象都可能处理同一请求，且处理顺序/职责可能调整。
- 需要在运行时动态增删处理节点（拦截器、过滤器）。
- 日志、事件冒泡、权限校验、参数过滤等管道式处理。

### 优缺点

优点：

- 发送者与接收者解耦。
- 可动态调整处理链，增强灵活性。
- 符合单一职责：每个处理器只管自己负责的一类请求。
- 新增处理器不改动现有节点。

缺点：

- 请求可能到达链尾仍无人处理（需要兜底）。
- 长链带来性能与调试开销。
- 责任在链上分散，整体行为不易一览。

### 与相关模式关系

- **与装饰器模式**：结构几乎相同；区别在于"所有节点都处理"（装饰器）vs"恰好一个节点处理"（责任链严格定义）。装饰器可看作"每个节点都处理并继续传递"的责任链变体。
- **与命令模式**：责任链中的请求常封装为命令对象；命令模式负责请求的封装，责任链负责请求的分发。
- **与观察者模式**：UI 事件既可用责任链冒泡，也可用观察者监听，二者互补。

## 参考

https://en.wikipedia.org/wiki/Chain-of-responsibility_pattern
