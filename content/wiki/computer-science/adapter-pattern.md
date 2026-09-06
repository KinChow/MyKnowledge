---
aliases:
- 适配器
- Adapter Pattern
- Wrapper Pattern
confidentiality: public
domain: computer-science
evidence:
- claim: 适配器模式（又称包装器，与装饰器模式共享此别名）是一种允许将已存在类的接口用作另一个接口的软件设计模式。
  claim_id: adapter-pattern-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-15fc29d8064d
    exact: the adapter pattern is a software design pattern (also known as wrapper,
      an alternative naming shared with the decorator pattern) that allows the interface
      of an existing class to be used as another interface.
  targets:
  - evidence_id: evidence-15fc29d8064d
    source_id: web-computer-science-adapter-pattern
id: adapter-pattern
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-adapter-pattern
status: published
tags:
- design-pattern
- structural
- adapter
title: 适配器模式
updated_at: '2026-09-06'
---
# 适配器模式

## 一句话结论

适配器模式（Adapter Pattern，也称 Wrapper）通过引入一个适配器类，把已存在类的**接口转换为客户端所期望的另一个接口**，让原本接口不兼容的类无需修改源码即可协同工作。核心价值是"兼容既有代码、不改动被适配者"。

## 核心概念

- **Target（目标接口）**：客户端所期望使用的接口。
- **Adaptee（被适配者）**：接口不兼容、但功能上恰好能满足需求的既有类。
- **Adapter（适配器）**：将 Adaptee 的接口转换为 Target 的接口；它实现 Target，同时持有或继承 Adaptee。
- **类适配器（class adapter）**：通过多继承（实现 Target 接口 + 继承 Adaptee 类）完成，编译期绑定。
- **对象适配器（object adapter）**：通过组合（Adapter 内含 Adaptee 实例）与委派完成，运行期灵活、推荐优先使用。
- **Wrapper（包装器）**：Adapter 的别名，与装饰器模式共享这一命名。

## 工作机制

客户端只依赖 Target 接口，运行时拿到的是 Adapter 对象。当客户端调用 Target 接口的方法时，Adapter 把调用转发（委派）到内部 Adaptee 对象的对应方法：

1. 客户端调用 `Target.operation()`。
2. 该调用落到 `Adapter.operation()` 上。
3. `Adapter` 内部将请求翻译并转发给 `Adaptee.specificOperation()`。
4. 客户端感知不到 Adaptee 的存在，无需修改任何客户端与 Adaptee 的源码。

这种"通过独立 Adapter 工作、不改变 Adaptee 本身"的设计，就是适配器模式的关键思想。

## 示例或代码

以对象适配器为例，把旧的打印机接口适配成新的打印服务接口：

```java
// Target：客户端期望的接口
public interface PrintService {
    void print(String text);
}

// Adaptee：接口不兼容的既有类
public class LegacyPrinter {
    public void printOld(String s) {
        System.out.println("[Legacy] " + s);
    }
}

// Adapter：实现 Target，组合 Adaptee
public class PrinterAdapter implements PrintService {
    private LegacyPrinter legacy = new LegacyPrinter();
    @Override
    public void print(String text) {
        legacy.printOld(text); // 把新接口调用翻译成旧接口调用
    }
}

// 客户端只依赖 PrintService
public class Client {
    public static void main(String[] args) {
        PrintService service = new PrinterAdapter();
        service.print("hello"); // 底层打印由 LegacyPrinter 完成
    }
}
```

## 常见误区

- **把适配器当成装饰器**：两者都叫 Wrapper，但适配器是"转换接口以匹配客户端期望"，装饰器是"动态增加行为"。
- **只认类适配器**：类适配器依赖多继承、编译期绑定、不够灵活；对象适配器基于组合、运行期更灵活，是更常用的实现。
- **把适配器当成外观模式**：外观是"提供一个更简单的接口"来隐藏复杂子系统；适配器是"把接口转成另一个指定接口"。
- **误以为适配器能改 Adaptee 内部逻辑**：它只做接口翻译，不改动 Adaptee 的功能语义。

## 证据映射

| claim_id | 来源 | 要点 |
| --- | --- | --- |
| adapter-pattern-definition | web-computer-science-adapter-pattern | 适配器模式允许把已存在类的接口用作另一个接口，让不兼容的类协同工作 |

## 待验证项

无。定义已由 web 源（Wikipedia Adapter pattern 条目）锚定。

## 关联知识

- [[software-design]] —— 设计模式分类：创建型/结构型/行为型，适配器属于结构型。
- [[object-oriented]] —— 接口、继承、组合与多态，是适配器模式的语言基础。
- [[decorator-pattern]] —— 同样被称作 Wrapper，但目的不同（动态添加行为）。
- [[facade-pattern]] —— 提供简化接口；与适配器的"转换接口"目的对比。
- [[bridge-pattern]] —— 与适配器常被混淆，桥接是"解耦抽象与实现"。
- [[proxy-pattern]] —— 代理同样包装真实对象，但目的是控制访问而非转换接口。
- [[class-diagram]] —— 用 UML 类图表达 Target/Adaptee/Adapter 三者关系。

## 详细章节

### 定义

适配器模式（Adapter Pattern）是 GoF 二十三种设计模式之一，属于结构型模式。它允许将一个已存在类的接口用作另一个接口，使得接口不兼容的类能够一起工作。适配器也被称为"包装器"（Wrapper）——该命名与装饰器模式共享。

### 参与者

- **Target**：定义客户端使用的、与特定领域相关的接口。
- **Client**：与实现 Target 接口的对象协作。
- **Adaptee**：需要被适配的既有接口（通常功能正确但接口不符）。
- **Adapter**：将 Adaptee 的接口适配为 Target 的接口。

### 结构

对象适配器（推荐）：

```
Client → Target (interface)
              ↑
        Adapter (implements Target, contains Adaptee)
              ↓
         Adaptee (existing class)
```

类适配器（多继承语言中可用）：

```
Client → Target (interface)
              ↑
        Adapter (implements Target, extends Adaptee)
```

### 适用场景

- 想使用一个既有类，但它的接口与所需接口不兼容。
- 想创建一个可复用的类，与多个彼此没有关联的类协作。
- 想在不改动既有类源码的前提下，让其适配新接口。
- 需要把第三方库或遗留系统的接口统一到团队约定的接口上。

### 优点与缺点

优点：

- 单一职责：让接口转换逻辑独立成类。
- 开闭原则：引入 Adapter 而不修改 Client 与 Adaptee 的现有代码。
- 复用性：让既有类在多个不兼容上下文中复用。

缺点：

- 增加类的数量与间接层，使系统更复杂。
- 过度使用会让系统难以维护（一堆"转接头"）。
- 类适配器受多继承限制，且不如对象适配器灵活。

### 与相关模式的关系

- **与装饰器（Decorator）**：都叫 Wrapper，但适配器改接口，装饰器加行为。
- **与外观（Facade）**：外观定义一个更简单的接口，适配器把接口改成另一个接口。
- **与桥接（Bridge）**：桥接"解耦抽象与实现使两者可独立变化"，常被误认为适配器；适配器解决"已有接口不匹配"。
- **与代理（Proxy）**：代理为另一个对象提供替身以控制访问，不改变接口。

## 参考
- https://en.wikipedia.org/wiki/Adapter_pattern
