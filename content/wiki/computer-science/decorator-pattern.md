---
aliases:
- 装饰器
- Decorator Pattern
- Wrapper Pattern
confidentiality: public
domain: computer-science
evidence:
- claim: 装饰器模式是一种设计模式，允许把行为动态地添加到单个对象上，而不影响同一类其他实例的行为。
  claim_id: decorator-pattern-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-44f254bb1d1a
    exact: the decorator pattern is a design pattern that allows behavior to be added
      to an individual object dynamically, without affecting the behavior of other
      instances of the same class. The decorator pattern provides a flexible alternative
      to subclassing for extending functionality.
  targets:
  - evidence_id: evidence-44f254bb1d1a
    source_id: web-computer-science-decorator-pattern
id: decorator-pattern
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-decorator-pattern
status: published
tags:
- design-pattern
- structural
- decorator
title: 装饰器模式
updated_at: '2026-09-06'
---
# 装饰器模式

## 一句话结论

装饰器模式（Decorator Pattern）通过把对象放进包装对象（Decorator）中，在**运行期动态**地给单个对象添加行为，而不影响同一类其他实例、也不需要改动源码；它是比继承更灵活、更细粒度的功能扩展方式。

## 核心概念

- **Component（组件接口）**：定义对象可以被动态添加职责的统一接口。
- **ConcreteComponent（具体组件）**：被装饰的原始对象，实现 Component。
- **Decorator（装饰器）**：实现 Component，同时持有一个 Component 引用，把请求转发给被包装对象，并可在转发前后附加行为。
- **ConcreteDecorator（具体装饰器）**：在转发基础上增加具体的新职责。
- **装饰器可叠加**：多个装饰器可以层层包装，每层各加一份职责。

## 工作机制

装饰器模式用"包装"代替"继承"：

1. `Decorator` 实现 `Component` 接口，从而对客户端透明（客户端感知不到被包装）。
2. `Decorator` 内含一个 `Component` 引用，把未改写的操作原样转发给被包装对象。
3. `ConcreteDecorator` 覆写需要增强的方法：先调用被包装对象的原方法，再附加新逻辑（或反之）。
4. 多个装饰器可叠加，运行期动态组合出任意行为集合。

关键点：职责的添加发生在**运行期**且只作用于被包装的**单个对象**，与编译期绑定、作用于整个类层次的继承形成鲜明对比。

## 示例或代码

以给文本加边框与滚动条为例：

```java
public interface Window {
    void draw();
}

public class SimpleWindow implements Window {
    public void draw() { System.out.println("draw window"); }
}

// 装饰器基类：转发给被包装对象
public abstract class WindowDecorator implements Window {
    protected Window inner;
    public WindowDecorator(Window inner) { this.inner = inner; }
    public void draw() { inner.draw(); }
}

// 具体装饰器：加边框
public class BorderDecorator extends WindowDecorator {
    public BorderDecorator(Window inner) { super(inner); }
    public void draw() { inner.draw(); System.out.println("+ border"); }
}

// 具体装饰器：加滚动条
public class ScrollDecorator extends WindowDecorator {
    public ScrollDecorator(Window inner) { super(inner); }
    public void draw() { inner.draw(); System.out.println("+ scrollbar"); }
}

// 运行期叠加：既加边框又加滚动条，且不影响其他 SimpleWindow 实例
Window w = new BorderDecorator(new ScrollDecorator(new SimpleWindow()));
w.draw();
```

## 常见误区

- **把装饰器和适配器混淆**：两者都被称作 Wrapper；装饰器"添加行为、不改接口"，适配器"转换接口"。
- **误以为装饰器改动整个类**：它只作用于被包装的单个对象实例，其他实例不受影响。
- **把继承当作唯一扩展手段**：继承在编译期绑定且影响整个类层次，装饰器在运行期、对象级扩展，更细粒度更灵活。
- **装饰器与代理混淆**：代理负责控制访问（如懒加载、权限），装饰器负责增强行为；两者结构相似但目的不同。

## 证据映射

| claim_id | 来源 | 要点 |
| --- | --- | --- |
| decorator-pattern-definition | web-computer-science-decorator-pattern | 装饰器模式动态给单个对象添加行为，不影响同类的其他实例 |

## 待验证项

无。定义已由 web 源（Wikipedia Decorator pattern 条目）锚定。

## 关联知识

- [[software-design]] —— 设计模式分类：装饰器属于结构型模式。
- [[object-oriented]] —— 继承、组合、多态是装饰器模式的语言基础。
- [[adapter-pattern]] —— 与装饰器共享 Wrapper 命名，但目的是转换接口。
- [[proxy-pattern]] —— 结构与装饰器相似，但目的是控制访问而非增强行为。
- [[facade-pattern]] —— 也包装对象，但提供简化接口而非逐层添加职责。
- [[class-diagram]] —— 用 UML 类图表达 Component/Decorator/ConcreteDecorator 的依赖关系。
- [[solid]] —— 装饰器有助于满足单一职责（SRP）与开闭原则（OCP）。

## 详细章节

### 定义

装饰器模式（Decorator Pattern）是 GoF 二十三种设计模式之一，属于结构型模式。在面向对象编程中，它允许把行为**动态地**添加到单个对象上，而不影响同一类其他实例的行为。它常被用来支持单一职责原则——把不同关注点的功能分布到职责清晰的类中；也支持开闭原则——无需修改源码即可扩展类功能。

### 参与者

- **Component**：定义可被动态添加职责的对象的统一接口。
- **ConcreteComponent**：被装饰的具体对象。
- **Decorator**：实现 Component 接口，并持有一个 Component 引用；默认把请求转发给该引用。
- **ConcreteDecorator**：在转发的基础上增加具体职责。

### 结构

```
Client → Component (interface)
            ↑           ↑
   ConcreteComponent  Decorator (holds Component)
                        ↑
                 ConcreteDecorator
```

装饰器链：`ConcreteDecorator → ConcreteDecorator → ConcreteComponent`，层层转发并附加职责。

### 适用场景

- 需要动态、透明地给单个对象添加职责，且不影响其他对象。
- 需要能撤销的职责（运行时增删）。
- 用继承会产生大量子类（如"带边框+带滚动条+带阴影…"的组合爆炸）时。
- 希望功能扩展符合开闭原则、不修改已有类。

### 优点与缺点

优点：

- 比继承更灵活：运行期组合、对象级作用域。
- 符合开闭原则与单一职责原则。
- 避免子类组合爆炸。

缺点：

- 会产生许多小类，增加系统复杂度与调试难度。
- 多层装饰后对象难以理解（"洋葱"结构）。
- 装饰器与被装饰对象严格同接口，无法方便地使用非 Component 接口的特性。

### 与相关模式的关系

- **与适配器（Adapter）**：都叫 Wrapper；适配器改接口，装饰器加行为。
- **与代理（Proxy）**：结构相似（都持有一个被包装对象）；代理控制访问，装饰器增强行为。
- **与组合（Composite）**：装饰器可视为只有一个子节点的组合对象，从而与组合模式结合使用。
- **与策略（Strategy）**：装饰器改变对象"外表/外壳"，策略改变对象"内核"。

## 参考
- https://en.wikipedia.org/wiki/Decorator_pattern
