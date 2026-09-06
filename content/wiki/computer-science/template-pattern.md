---
aliases:
- 模板方法模式
- Template Method Pattern
confidentiality: public
domain: computer-science
evidence:
- claim: 模板方法是超类（通常是抽象超类）中的一个方法，以若干高层步骤的形式定义某个操作的骨架。
  claim_id: template-pattern-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-ad89a183fb52
    exact: The template method is a method in a superclass, usually an abstract superclass,
      and defines the skeleton of an operation in terms of a number of high-level
      steps
  targets:
  - evidence_id: evidence-ad89a183fb52
    source_id: web-computer-science-template-pattern
id: template-pattern
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-template-pattern
status: published
tags:
- design-pattern
- behavioral
- template-method
title: 模板方法模式
updated_at: '2026-09-06'
---
# 模板方法模式

## 一句话结论

模板方法模式在**基类（通常是抽象类）**中定义一个**算法骨架**（模板方法），骨架由若干高层步骤组成，步骤的"不变部分"写在基类、**可变部分**由**子类通过覆盖/填充辅助方法**提供。子类可以细化或重定义某些步骤，但**不应重写模板方法本身**，从而保证算法整体结构始终被遵循。

## 核心概念

- **定义**：模板方法是面向对象编程中的一种行为型设计模式，是超类（通常是抽象超类）中定义操作骨架的方法，以若干高层步骤表示。
- **骨架（Skeleton）**：模板方法包含算法中**不变**的部分，确保总算法始终被遵循。
- **辅助方法/原语操作**：可变部分通过发送自消息（self messages）请求执行辅助方法来实现；辅助方法可以是抽象方法或钩子方法（hook）。
- **钩子方法（Hook）**：在超类中为空实现（不做任何事），子类可（非必须）覆盖以微调算法。
- **子类填充**：子类用具体算法填充模板的可变/空部分；子类**不得**覆盖模板方法本身。

## 工作机制

- 基类实现模板方法：按固定顺序调用一系列步骤。
- 步骤分两类：抽象/原语操作（子类必须实现）与钩子方法（子类可选覆盖）。
- 子类继承模板方法（不覆盖它），只实现/覆盖辅助方法，即可复用不变骨架并定制可变部分。
- 体现**控制反转（Inversion of Control）**：高层代码不再决定运行哪些算法，低层算法在运行时被选择。

## 示例或代码

经典例子：GUI 框架中"显示视图"流程（设置焦点 → 绘制内容 → 重置焦点），绘制内容由子类实现。

Python 示意：

```python
from abc import ABC, abstractmethod

class View(ABC):                 # 抽象基类
    def _set_focus(self):
        print("View::setFocus")
    def _reset_focus(self):
        print("View::resetFocus")
    @abstractmethod              # 原语操作：子类必须实现
    def do_display(self): ...
    def display(self):           # 模板方法：定义算法骨架，不可被子类重写
        self._set_focus()
        self.do_display()
        self._reset_focus()

class MyView(View):              # 具体子类：只填充分支
    def do_display(self):
        print("MyView::doDisplay")

MyView().display()
```

## 常见误区

- **子类覆盖模板方法本身**：模板方法应保持"骨架唯一"，子类只填充步骤。
- **把所有方法都做成抽象**：会丢失"默认实现 + 可选覆盖（钩子）"的灵活性。
- **与策略模式混淆**：模板方法用**继承**在骨架内复用并定制步骤；策略用**组合**整体替换算法。
- **忽略钩子方法的"可选性"**：钩子存在意义就是给子类可选微调点，不是必须实现。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| template-pattern-definition | web-computer-science-template-pattern | 模板方法是超类中定义操作骨架的方法，步骤由辅助方法实现，子类填充可变部分 |

## 待验证项

无。英文定义直接来自 Wikipedia《Template method pattern》条目，已锚定原文逐字引文。

## 关联知识

- [[strategy-pattern]] —— 模板方法固定骨架（继承定制），策略整体替换算法（组合）。
- [[strategy-pattern]] 与 [[state-pattern]] —— 三者都关注行为变化，但机制（继承 vs 组合）不同。
- [[object-oriented]] —— 继承、抽象方法、多态是模板方法的实现基础。
- [[software-design]] —— 行为型模式在 23 种 GoF 模式中的定位。

## 详细章节

### 定义

在面向对象编程中，模板方法是 Gamma 等人在《设计模式》中提出的行为型设计模式之一。模板方法是超类（通常是抽象超类）中的一个方法，以若干**高层步骤**的形式定义某个**操作的骨架**；这些步骤本身由同一类中的**辅助方法**实现。

模板方法在基类中实现，包含算法中**不变**的部分，确保总算法始终被遵循。模板方法中可变的部分通过发送"自消息"请求执行额外的辅助方法来实现——辅助方法在基类中可有默认实现，也可以完全没有（即抽象方法）。基类的子类用随子类变化的特定算法"填充"模板中空置或可变的部分。**子类不重写模板方法本身**这一点非常重要。

### 参与者

- **AbstractClass（抽象类）**：实现模板方法（定义骨架），并声明抽象原语操作与/或提供钩子方法的默认（空）实现。
- **ConcreteClass（具体子类）**：实现原语操作以完成子类特有的算法步骤；可选地覆盖钩子方法微调行为。

### 结构

- 模板方法调用三类方法：具体方法（基类实现、不变）、抽象/原语操作（子类必须实现）、钩子方法（基类空实现、子类可选覆盖）。
- 子类继承模板方法而不覆盖它，只提供具体步骤。
- 类图中的关系：`ConcreteClass` 继承 `AbstractClass`，实现原语操作，模板方法定义于基类。

### 适用场景

- 多个类有相同算法流程，但其中某些步骤的实现各不相同。
- 需要"复用不变骨架 + 允许子类定制可变点"。
- 希望把公共行为上移到基类以避免代码重复。
- 框架设计中定义扩展点（钩子），供使用者挂接定制逻辑。

### 优缺点

优点：

- 代码复用：公共算法骨架集中在基类。
- 控制反转：框架定义流程，使用者提供细节。
- 钩子方法提供灵活的扩展点，不强制实现。
- 保证算法结构一致（不会被子类打乱）。

缺点：

- 继承是强耦合：子类与基类绑定，基类修改可能影响所有子类。
- 步骤过多时类层次复杂。
- 违反"组合优于继承"精神的场景下可用策略模式替代。

### 与相关模式关系

- **与策略模式**：模板方法通过继承在类内固定骨架并定制步骤；策略模式通过组合让对象持有并整体切换算法对象。
- **与状态模式**：都是"行为随环境变化"，但状态模式由内部状态驱动、通过委托实现。
- **与工厂方法**：工厂方法常作为模板方法内的一个"步骤"（创建步骤）被调用。

## 参考

https://en.wikipedia.org/wiki/Template_method_pattern
