---
aliases:
- 访问者
- Visitor Pattern
confidentiality: public
domain: computer-science
evidence:
- claim: 访问者模式是一种软件设计模式，它把算法与对象结构分离开来。由于这种分离，可以在不修改对象结构的前提下为现有对象结构添加新操作，它是面向对象编程中遵循开闭原则的一种方式。
  claim_id: visitor-pattern-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-d6bf0661e3cf
    exact: A visitor pattern is a software design pattern that separates the algorithm
      from the object structure
  targets:
  - evidence_id: evidence-d6bf0661e3cf
    source_id: web-computer-science-visitor-pattern
id: visitor-pattern
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-visitor-pattern
status: published
tags:
- design-pattern
- behavioral
- visitor
title: 访问者模式
updated_at: '2026-09-06'
---
# 访问者模式

## 一句话结论

访问者模式**把"算法（操作）"与"对象结构"分离**：通过**双分派（double dispatch）**，让一个"访问者"对象对一族类中的每个元素执行相应操作，从而**无需修改这些类**就能为对象结构**添加新操作**。它是遵循**开闭原则**的一种典型方式——对扩展开放、对修改封闭。

## 核心概念

- **定义**：访问者模式是一种软件设计模式，把算法与对象结构分离；新操作可被添加到现有对象结构而无需修改结构。
- **开闭原则**：在 OOP 中遵循开闭原则的一种方式。
- **新增虚函数而不改类**：访问者允许向一族类添加新的"虚函数"，而无需修改这些类本身。
- **双分派（Double Dispatch）**：元素调用 `accept(visitor)`，再回调访问者中对应元素类型的 `visit` 方法，实现按"实际类型"分派。
- **GoF 定义**："表示一个作用于对象结构各元素的操作。访问者让你在不改变元素类的前提下定义新操作。"

## 工作机制

- 元素类声明 `accept(visitor)`；具体元素实现时，把自身（`this`）传给访问者对应类型的 `visit` 方法。
- 访问者类为每种元素类声明一个 `visit` 方法，具体访问者实现这些方法，即实现"作用于该对象结构"的算法；算法状态由具体访问者本地维护。
- 客户端创建对象结构并实例化具体访问者；执行操作时对顶层元素调用 `accept`。
- 组合元素通常遍历其子元素，对每个子元素调用 `accept`。
- 因操作被外置为访问者对象，**新增操作 = 新增访问者类**，对象结构类无需改动。

## 示例或代码

经典场景：编译器对 AST 做类型检查/代码生成/打印；对"形状"结构求面积/周长。

Python 示意：

```python
class Shape:                                   # Element
    def accept(self, visitor): ...

class Circle(Shape):
    def __init__(self, r): self.r = r
    def accept(self, visitor):
        return visitor.visit_circle(self)      # 双分派：回调具体类型的 visit

class Square(Shape):
    def __init__(self, s): self.s = s
    def accept(self, visitor):
        return visitor.visit_square(self)

class AreaVisitor:                             # Visitor：算法外置
    def visit_circle(self, c): return 3.14 * c.r * c.r
    def visit_square(self, s): return s.s * s.s

shapes = [Circle(2), Square(3)]
area = AreaVisitor()
print([sh.accept(area) for sh in shapes])      # [12.56, 9]
# 新增"周长"操作只需新增 PerimeterVisitor，无需改 Shape/Circle/Square
```

## 常见误区

- **把访问者当普通回调/遍历**：核心是双分派——元素回调访问者、访问者按元素实际类型分派。
- **在元素类中硬编码新操作**：那正是模式要避免的"修改现有类"。
- **对象结构频繁变化时使用**：新增元素类型需要为每个访问者加一个 `visit` 方法，此时访问者模式带来负担。
- **忽略双分派语义**：静态类型语言若分派错误（按声明类型而非实际类型）会失效。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| visitor-pattern-definition | web-computer-science-visitor-pattern | 访问者分离算法与对象结构，可在不修改结构的前提下添加新操作，遵循开闭原则 |

## 待验证项

无。英文定义直接来自 Wikipedia《Visitor pattern》条目，已锚定原文逐字引文。

## 关联知识

- [[iterator-pattern]] —— 访问者遍历对象结构时常用迭代器获取元素。
- [[composite-pattern]]（结构型） —— 访问者常作用于组合/树形结构（如 AST）。
- [[compilation-principle]] —— 编译器对语法树/中间表示做语义分析时大量使用访问者。
- [[object-oriented]] —— 多态与开闭原则是访问者模式的理论基础。

## 详细章节

### 定义

访问者模式是一种软件设计模式，它把**算法与对象结构分离**。由于这种分离，可以在不修改对象结构的前提下，为现有对象结构添加新操作。它是面向对象编程与软件工程中遵循**开闭原则**的一种方式。

本质上，访问者允许向一族类添加新的虚函数而无需修改这些类：取而代之创建一个访问者类，实现该虚函数所有合适的特化版本。访问者以实例引用为输入，通过**双分派**实现目标。这使得可以独立于对象结构的类、通过添加新的访问者对象来创建新操作。GoF 对访问者的定义："表示一个作用于对象结构各元素的操作。访问者让你在不改变元素类的前提下定义新操作。"

### 参与者

- **Visitor（访问者接口）**：为每种元素类声明一个 `visit` 方法。
- **ConcreteVisitor（具体访问者）**：实现各 `visit` 方法，实现作用于对象结构的算法；算法状态在具体访问者本地维护。
- **Element（元素接口）**：声明 `accept(visitor)` 方法。
- **ConcreteElement（具体元素）**：实现 `accept`，最简单的形式即调用访问者对应的 `visit` 方法；组合元素通常遍历子元素并逐一调用其 `accept`。
- **Client（客户端）**：创建对象结构与具体访问者，触发操作。

### 结构

- 元素与访问者互相依赖接口：元素 `accept(visitor)` → 调用 `visitor.visit(this)`；访问者按元素实际类型重载 `visit`。
- 对象结构（如 AST/树）由元素组成；客户端对顶层元素调用 `accept` 触发整棵结构上的操作。
- 该结构天然适合在**公共 API** 上"挂接"外部操作，无需修改被访问类的源码。

### 适用场景

- 对象结构稳定（元素类型基本不变），但经常需要在结构上执行新的、不相关的操作。
- 希望把复杂算法从数据结构类中剥离，集中到访问者中。
- 需要对异构对象结构执行一组不同操作（打印、序列化、校验、语义分析）。
- 希望在不修改元素类的前提下扩展操作（开闭原则）。

### 优缺点

优点：

- 符合开闭原则：新增操作无需修改元素类。
- 把相关操作内聚到访问者，便于集中维护与测试。
- 通过双分派实现按实际类型选择操作。
- 适用于公共 API：外部可对类执行新操作而不改源码。

缺点：

- 新增元素类型需为所有访问者增加 `visit` 方法（与开闭原则冲突于"对元素开放"一侧）。
- 元素内部状态若私有，访问者无法访问（常需暴露访问接口，破坏封装）。
- 双分派机制在静态类型语言中稍复杂。

### 与相关模式关系

- **与迭代器模式**：访问者遍历结构时用迭代器获取元素，二者常搭配。
- **与组合模式**：访问者尤其适用于组合/树形结构（如 AST），对每个节点执行操作。
- **与解释器模式**：解释器对 AST 求值可基于访问者实现多种解释/变换。
- **与命令模式**：访问者把"结构上的操作"对象化，与命令"把请求对象化"思想相近，但访问者基于双分派。

## 参考

https://en.wikipedia.org/wiki/Visitor_pattern
