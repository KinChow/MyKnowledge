---
aliases:
- 桥接
- Bridge Pattern
- Handle/Body Pattern
confidentiality: public
domain: computer-science
evidence:
- claim: 桥接模式将抽象与其实现解耦，使两者可以独立变化，是 GoF 提出的设计模式。
  claim_id: bridge-pattern-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-b14e9e7ce7de
    exact: The bridge pattern is a design pattern used in software engineering that
      is meant to "decouple an abstraction from its implementation so that the two
      can vary independently", introduced by the Gang of
  targets:
  - evidence_id: evidence-b14e9e7ce7de
    source_id: web-computer-science-bridge-pattern
id: bridge-pattern
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-bridge-pattern
status: published
tags:
- design-pattern
- structural
- bridge
title: 桥接模式
updated_at: '2026-09-06'
---
# 桥接模式

## 一句话结论

桥接模式（Bridge Pattern）通过把**抽象（Abstraction）与实现（Implementor）解耦**，使两者可以**独立变化**——抽象层定义高层接口，实现层通过组合被抽象引用，编译期不再绑定具体实现，运行期可自由切换。只有一个固定实现时，它退化为 C++ 的 Pimpl 惯用法。

## 核心概念

- **Abstraction（抽象）**：定义抽象接口，并持有 Implementor 引用。
- **RefinedAbstraction（扩展抽象）**：扩展 Abstraction 的接口。
- **Implementor（实现接口）**：定义实现类家族的接口。
- **ConcreteImplementor（具体实现）**：实现 Implementor，可有多套互相替换。
- **解耦**：抽象与实现分别位于独立继承层次，通过组合连接，避免编译期绑定。

## 工作机制

桥接模式用**组合代替继承**来连接抽象与实现：

1. `Abstraction` 声明高层接口，内含一个 `Implementor` 类型的引用。
2. 客户端创建 `Abstraction` 时注入具体的 `ConcreteImplementor`。
3. `Abstraction` 的方法委托给内部 `Implementor` 执行。
4. 抽象层与实现层各成继承体系，互不依赖，可各自扩展。

由于实现是运行期注入的，切换实现不需要改动抽象层代码；新增抽象或新增实现也互不影响。

## 示例或代码

以"图形 + 颜色"两个维度为例（传统继承会产生 形状×颜色 组合爆炸）：

```java
// Implementor：颜色实现
public interface Color { String fill(); }
public class Red implements Color { public String fill() { return "red"; } }
public class Blue implements Color { public String fill() { return "blue"; } }

// Abstraction：图形抽象，持有颜色引用
public abstract class Shape {
    protected Color color;
    protected Shape(Color color) { this.color = color; }
    public abstract String draw();
}

// RefinedAbstraction
public class Circle extends Shape {
    public Circle(Color color) { super(color); }
    public String draw() { return "circle filled with " + color.fill(); }
}
public class Square extends Shape {
    public Square(Color color) { super(color); }
    public String draw() { return "square filled with " + color.fill(); }
}

// 运行期组合：2 种图形 × 2 种颜色，无需 4 个子类
Shape s = new Circle(new Red());
System.out.println(s.draw()); // circle filled with red
```

## 常见误区

- **把桥接当成适配器**：桥接在"设计阶段"解耦抽象与实现；适配器在"已有代码"上转换接口。桥接常被误称为适配器。
- **把桥接当成简单的接口**：桥接的核心是让抽象与实现两个维度各自独立演化，而不仅是定义接口。
- **以为桥接只是多态**：多态是机制，桥接是用组合把"抽象层次"和"实现层次"两棵树连起来的结构意图。
- **忽略 Pimpl 关系**：当只有一个固定实现时，桥接就是 C++ 的 Pimpl 惯用法，不要把两者对立。

## 证据映射

| claim_id | 来源 | 要点 |
| --- | --- | --- |
| bridge-pattern-definition | web-computer-science-bridge-pattern | 桥接模式解耦抽象与实现，使两者可独立变化 |

## 待验证项

无。定义已由 web 源（Wikipedia Bridge pattern 条目）锚定。

## 关联知识

- [[software-design]] —— 设计模式分类：桥接属于结构型模式。
- [[object-oriented]] —— 组合优先于继承，是桥接模式的设计动机。
- [[adapter-pattern]] —— 与桥接常被混淆；适配器转换接口，桥接解耦抽象与实现。
- [[composite-pattern]] —— 桥接与组合可结合使用（组合树中的节点按桥接解耦实现）。
- [[abstract-factory]] —— 抽象工厂可配合桥接创建平台无关的实现。
- [[class-diagram]] —— 用 UML 类图表达 Abstraction/Implementor 两个继承层次。

## 详细章节

### 定义

桥接模式（Bridge Pattern）是 GoF 二十三种设计模式之一，属于结构型模式。其意图是"把抽象与实现解耦，使两者可以独立地变化"。它使用封装、聚合，并可使用继承来把职责分离到不同类中。当抽象与其实现都需要频繁变化时，桥接尤其有用。

### 参与者

- **Abstraction**：定义抽象接口，维护 Implementor 引用。
- **RefinedAbstraction**：扩展或精化 Abstraction 定义的接口。
- **Implementor**：定义实现类的接口，通常比 Abstraction 更底层、更具体。
- **ConcreteImplementor**：实现 Implementor 接口，供 Abstraction 委托调用。

### 结构

```
Abstraction ────► Implementor (interface)
   ↑                    ↑
RefinedAbstraction  ConcreteImplementor(s)
```

抽象层次（Abstraction / RefinedAbstraction）与实现层次（Implementor / ConcreteImplementor）是两条独立的继承链，通过 Abstraction 持有的 Implementor 引用相连。

### 适用场景

- 希望避免抽象与其实现的编译期绑定，让实现可在运行期选择。
- 抽象和实现都需要以子类方式独立扩展，且两者维度正交（多维变化）。
- 对实现类的修改不影响客户端与抽象层。
- 想对客户端隐藏实现细节（如 Pimpl 惯用法）。

### 优点与缺点

优点：

- 分离抽象接口及其实现，提高可扩展性与可维护性。
- 改善可扩展性：可独立扩展抽象层次与实现层次。
- 对客户端隐藏实现细节。
- 符合开闭原则：新增抽象或新增实现都无需改动对方。

缺点：

- 增加系统设计与理解的复杂度（多一层间接）。
- 若只需一个固定实现，引入桥接属于过度设计。

### 与相关模式的关系

- **与适配器（Adapter）**：桥接设计于开始之时（事先解耦）；适配器作用于已有系统（事后转换接口）。
- **与抽象工厂（Abstract Factory）**：抽象工厂可创建一组平台相关对象，配合桥接实现跨平台。
- **与组合（Composite）**：桥接与组合可同时使用：组合树的对象可用桥接让实现可替换。
- **与策略（Strategy）**：结构相似，但桥接偏"结构"，策略偏"行为"。

## 参考
- https://en.wikipedia.org/wiki/Bridge_pattern
