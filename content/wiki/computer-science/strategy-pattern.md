---
aliases:
- 政策模式
- Policy Pattern
confidentiality: public
domain: computer-science
evidence:
- claim: 策略模式（又称政策模式）是一种允许在运行时选择算法的行为型软件设计模式。
  claim_id: strategy-pattern-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-2b9d28717063
    exact: the strategy pattern (also known as the policy pattern) is a behavioral
      software design pattern that enables selecting an algorithm at runtime
  targets:
  - evidence_id: evidence-2b9d28717063
    source_id: web-computer-science-strategy-pattern
id: strategy-pattern
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-strategy-pattern
status: published
tags:
- design-pattern
- behavioral
- strategy
title: 策略模式
updated_at: '2026-09-06'
---
# 策略模式

## 一句话结论

策略模式是一种**行为型设计模式**，它把一族可互换的算法各自封装成独立的策略对象，让程序在**运行时**从这一族算法中选择要用的那一个；由于策略是"组合"进上下文（Context）而不是"继承"硬编码的，算法可以**独立于使用它的客户端而变化**，调用代码也因此更灵活、更可复用。

## 核心概念

- **定义**：策略模式（Strategy Pattern，又称政策模式 Policy Pattern）是一种行为型软件设计模式，允许在运行时选择算法。
- **运行时决策**：不是直接实现单一算法，而是让代码接收"运行时指令"，确定使用一族算法中的哪一个。
- **组合优于继承**：行为被定义为独立接口 + 实现该接口的具体类；上下文通过组合持有策略，而非通过继承把行为钉死在类上。
- **算法与客户端解耦**：策略（算法）可独立于使用它的客户端变化，客户端无需修改即可切换行为。
- **实现机制多样**：策略可通过函数指针、一等函数、类/类实例（OOP 语言）或反射访问语言内部代码存储等方式被保存与取用。

## 工作机制

- 上下文（Context）持有一个策略接口的引用；客户端在构造时或运行时把某个具体策略注入上下文。
- 调用时，上下文把算法请求**委托**给当前持有的策略对象，自身不实现具体算法。
- 切换算法只需替换策略对象引用即可——既可以在**设计时**决定，也可以在**运行时**动态改变。
- 由于使用的是组合而非继承，替换实现不会破坏使用该行为的类，也无需大量改动代码。
- 存储策略"代码"的机制可以是函数指针、一等函数、类实例，或通过反射访问语言实现内部的代码存储。

## 示例或代码

经典例子——汽车刹车行为：一个 `Car` 对象的刹车行为可以从 `BrakeWithABS()` 切换到 `Brake()`，只需改变其 `brakeBehavior` 成员指向的实现，而无需修改 `Car` 类本身。

Python 示意（策略 = 一组可互换的排序算法）：

```python
from abc import ABC, abstractmethod

class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data): ...

class BubbleSort(SortStrategy):
    def sort(self, data):
        return sorted(data)  # 示意

class QuickSort(SortStrategy):
    def sort(self, data):
        return sorted(data, reverse=False)  # 示意

class Sorter:                     # Context 上下文
    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy
    def set_strategy(self, strategy: SortStrategy):  # 运行时切换
        self._strategy = strategy
    def run(self, data):
        return self._strategy.sort(data)

s = Sorter(BubbleSort())
print(s.run([3, 1, 2]))
s.set_strategy(QuickSort())       # 运行时替换算法
print(s.run([3, 1, 2]))
```

## 常见误区

- **与状态模式混淆**：策略模式的算法选择由**客户端**决定，且策略对象通常无内部状态流转；状态模式则是对象**内部状态变化**触发行为切换（状态模式可视为"能通过接口方法调用切换策略"的策略模式）。
- **误以为必须用接口+继承**：函数指针、一等函数等机制同样是合法实现，不必强行套 OOP 类层次。
- **过度设计**：当算法数量少且固定、switch/if-else 简单清晰时，引入策略模式反而增加复杂度（YAGNI）。
- **忘记"运行时切换"才是价值点**：如果从不需要动态替换算法，策略模式的主要收益就丧失了。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| strategy-pattern-definition | web-computer-science-strategy-pattern | 策略模式是一种行为型设计模式，允许在运行时选择算法；策略（算法）可独立于使用它的客户端变化 |

## 待验证项

无。英文定义直接来自 Wikipedia《Strategy pattern》条目，已锚定原文逐字引文。

## 关联知识

- [[state-pattern]] —— 状态模式可被解释为一种"能通过接口方法切换策略"的策略模式。
- [[template-pattern]] —— 模板方法定义算法**骨架**并让子类填充分支；策略则整体替换算法。
- [[object-oriented]] —— 面向对象四大特性与"组合优于继承"。
- [[software-design]] —— 行为型模式在 23 种 GoF 模式中的定位。
- [[common-performance-design-patterns]] —— 性能设计模式中的策略式结构选择。

## 详细章节

### 定义

在计算机编程中，策略模式（又称政策模式）是一种行为型软件设计模式，它允许在运行时选择算法。与直接实现单一算法不同，代码接收"运行时指令"以确定使用一族算法中的哪一个，从而使算法可以独立于使用它的客户端而变化。

策略模式是 Gamma 等人在《设计模式》（Design Patterns）一书中收录的模式之一，该书推广了"用设计模式描述如何设计灵活、可复用的面向对象软件"这一思想。把"使用哪个算法"的决策推迟到运行时，使调用代码更灵活、更可复用。

### 参与者

- **Strategy（策略接口）**：定义一族算法共有的接口，每个具体策略实现该接口。
- **ConcreteStrategy（具体策略）**：实现策略接口，封装某一种具体算法。
- **Context（上下文）**：持有一个策略对象的引用，将算法请求委托给当前策略；不关心具体算法实现，也不因算法变化而修改。

### 结构

- 上下文与策略接口之间存在**组合**（聚合）关系：上下文保存一个策略引用。
- 策略接口之下派生多个具体策略类，各自实现一种算法。
- 客户端决定使用哪个具体策略并注入上下文；运行时可通过替换策略引用切换算法。
- 行为以"独立接口 + 实现类"形式定义，做到行为与使用行为的类之间的解耦。

### 适用场景

- 一个类因其行为（算法）的不同而有多个变体，需要用其中一种。
- 需要避免大量条件分支（if-else / switch）来选择行为。
- 算法在运行时应可切换，或希望把"选择算法"与"使用算法"分离。
- 同一个算法族需要在不同上下文/客户端间复用。

### 优缺点

优点：

- 算法与客户端解耦，行为可独立变化而不破坏使用方。
- 符合开闭原则：新增算法只需新增具体策略，不改动上下文。
- 运行时/设计时均可切换行为，灵活性高。
- 消除大量条件语句，可维护性更好。

缺点：

- 客户端必须了解各策略的差异并自行选择，承担了选择成本。
- 增加类数量（每个策略一个类）。
- 策略对象本身不携带状态流转，若需要共享算法状态需额外设计。

### 与相关模式关系

- **与状态模式**：状态模式可被解释为策略模式的一种——二者结构相似（都通过接口委托行为），区别在于状态模式由"对象内部状态改变"驱动切换，策略模式由"客户端选择"驱动切换。
- **与模板方法**：模板方法在超类中固定算法**骨架**、由子类填写**可变的步骤**；策略模式则整体替换算法对象，靠组合而非继承。
- **与桥接/装饰器等结构型模式**：策略关注行为层面的算法族组织，常与其他模式组合使用。

## 参考

https://en.wikipedia.org/wiki/Strategy_pattern
