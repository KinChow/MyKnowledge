---
aliases:
- 备忘录
- Memento Pattern
confidentiality: public
domain: computer-science
evidence:
- claim: 备忘录模式是面向对象编程领域的一种软件设计模式，允许回滚（恢复）一个对象的状态。
  claim_id: memento-pattern-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-24fca6832d34
    exact: The memento pattern is a software design pattern in the field of object-oriented
      programming that allows reverting the state of an object
  targets:
  - evidence_id: evidence-24fca6832d34
    source_id: web-computer-science-memento-pattern
id: memento-pattern
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-memento-pattern
status: published
tags:
- design-pattern
- behavioral
- memento
title: 备忘录模式
updated_at: '2026-09-06'
---
# 备忘录模式

## 一句话结论

备忘录模式允许**保存一个对象的内部状态，并在需要时将其恢复**（回滚），用途包括**撤销（undo）、版本控制与序列化**。它由三个对象协作：**发起人（Originator）**、**负责人（Caretaker）**与**备忘录（Memento）**；备忘录保存状态快照且**不可变**，从而在不破坏封装的前提下实现状态回退。

## 核心概念

- **定义**：备忘录模式是面向对象编程领域的一种软件设计模式，允许回滚（恢复）对象的状态；用途包括撤销、版本控制与序列化。
- **三个对象**：发起人（Originator）、负责人（Caretaker）、备忘录（Memento）。
- **快照机制**：负责人先向发起人索要备忘录对象；执行操作后可把备忘录归还发起人以回滚到之前的状态。
- **备忘录不可变**：备忘录对象本身是不可变的（immutable）。
- **单对象范围**：若发起人会改变其他对象/资源需谨慎——备忘录模式作用于**单个对象**。

## 工作机制

- 发起人是持有内部状态的对象；它提供 `createMemento()`（保存当前状态到备忘录）与 `restore(memento)`（从备忘录恢复状态）。
- 负责人要对发起人执行某些操作，但希望能在操作后轻松恢复之前的状态。
- 流程：负责人先向发起人索要备忘录 → 执行操作（序列）→ 需要回滚时把备忘录归还发起人。
- 备忘录本身不可变；只作为状态快照传递。
- 经典例子：伪随机数生成器（PRNG）——消费者作为负责人，用特定种子（备忘录）初始化 PRNG（发起人）以复现相同随机序列。

## 示例或代码

经典场景：文本编辑器撤销栈、数据库事务回滚、序列化快照。

Python 示意：

```python
class Memento:                       # 备忘录：不可变快照
    def __init__(self, state):
        self._state = state
    def get_state(self):
        return self._state

class Originator:                    # 发起人
    def __init__(self):
        self._state = ""
    def set_state(self, state):
        self._state = state
    def create_memento(self):
        return Memento(self._state)  # 保存当前状态
    def restore(self, memento):
        self._state = memento.get_state()

class Caretaker:                     # 负责人：保存/提供备忘录
    def __init__(self):
        self._mementos = []
    def save(self, m):
        self._mementos.append(m)
    def pop(self):
        return self._mementos.pop() if self._mementos else None

o, c = Originator(), Caretaker()
o.set_state("v1"); c.save(o.create_memento())
o.set_state("v2"); c.save(o.create_memento())
o.set_state("v3")
o.restore(c.pop())                   # 回滚到 v2
print(o._state)                      # v2
```

## 常见误区

- **让负责人能修改备忘录内容**：备忘录应不可变，只由发起人读取/解析。
- **把整个对象深拷贝直接当备忘录**：应封装"需要保存的状态"，并隔离内部表示。
- **忽略单对象范围限制**：若发起人同时影响其他对象/资源，只保存自身状态不足以完整回滚。
- **把备忘录模式当作通用序列化**：它是"状态快照回滚"机制，序列化只是应用之一。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| memento-pattern-definition | web-computer-science-memento-pattern | 备忘录模式允许回滚对象状态，用途包括撤销、版本控制与序列化 |

## 待验证项

无。英文定义直接来自 Wikipedia《Memento pattern》条目，已锚定原文逐字引文。

## 关联知识

- [[command-pattern]] —— 撤销常由命令模式（操作回滚）与备忘录模式（状态回滚）配合实现。
- [[state-pattern]] —— 备忘录可保存状态对象，与状态模式结合实现"状态恢复"。
- [[software-design]] —— 行为型模式在 23 种 GoF 模式中的定位。
- [[object-oriented]] —— 封装与信息隐藏是备忘录模式的设计动机。

## 详细章节

### 定义

备忘录模式是面向对象编程领域的一种软件设计模式，它允许**回滚（恢复）一个对象的状态**。该模式的用途包括撤销（undo）、版本控制与序列化。

备忘录模式由三个对象实现：**发起人（Originator）**、**负责人（Caretaker）**与**备忘录（Memento）**。发起人是有内部状态的对象；负责人要对发起人做某些操作，但希望能在操作后轻松找回之前的状态。流程：负责人先向发起人索要备忘录对象 → 执行它打算做的操作（或操作序列）→ 要回滚到操作前的状态时，把备忘录对象归还发起人。备忘录对象本身不可变。使用该模式时需注意：若发起人会改变其他对象或资源需谨慎——备忘录模式作用于**单个对象**。

### 参与者

- **Originator（发起人）**：拥有需要保存/恢复的内部状态；实现 `createMemento()`（把当前状态存入备忘录）与 `restore(memento)`（从备忘录恢复状态）。
- **Memento（备忘录）**：保存发起人内部状态的快照；不可变，对外只读。
- **Caretaker（负责人）**：负责保存与取用备忘录（如维护历史栈），但不修改备忘录内容，也不依赖其内部表示。

### 结构

- 发起人与备忘录之间存在"创建/恢复"关系；负责人与备忘录之间存在"保存/取用"关系。
- 备忘录封装发起人的内部状态，避免状态暴露给外部。
- 负责人持有备忘录的集合（历史），支持多级撤销。
- 交互时序：负责人请求发起人 `createMemento()` → 操作 → 归还备忘录 `restore()`。

### 适用场景

- 需要实现撤销/重做（保存操作前的状态）。
- 需要保存对象的历史快照用于恢复（版本控制）。
- 需要序列化/恢复对象状态。
- 需要在"不破坏封装"的前提下把状态导出/导入。

### 优缺点

优点：

- 不破坏封装即可保存/恢复状态。
- 状态快照可独立管理，负责人职责单一。
- 简化发起人（状态恢复逻辑外置）。

缺点：

- 若状态很大，备忘录占用大量内存。
- 负责人需妥善管理备忘录生命周期（避免泄漏）。
- 频繁快照性能开销可观。
- 只对单对象状态有效，跨对象回滚需另行设计。

### 与相关模式关系

- **与命令模式**：撤销机制中，命令负责"操作回滚"，备忘录负责"状态回滚"，二者常组合。
- **与状态模式**：备忘录可保存状态对象的快照，便于状态切换后恢复。
- **与原型（Prototype，创建型）**：都可复制对象状态，但备忘录侧重"可恢复的历史快照"。

## 参考

https://en.wikipedia.org/wiki/Memento_pattern
