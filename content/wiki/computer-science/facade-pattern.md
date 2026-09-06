---
aliases:
- 外观模式
- Facade Pattern
- Façade Pattern
confidentiality: public
domain: computer-science
evidence:
- claim: 外观模式用一个充当"门面"的对象作为前端接口，遮蔽更复杂的底层或结构性代码，为客户端提供更简单的接口。
  claim_id: facade-pattern-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-b410664f922a
    exact: front-facing interface masking more complex underlying or structural code.
      This pattern hides the complexities of the larger system and provides a simpler
      interface to the client. It typically involve
  targets:
  - evidence_id: evidence-b410664f922a
    source_id: web-computer-science-facade-pattern
id: facade-pattern
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-facade-pattern
status: published
tags:
- design-pattern
- structural
- facade
title: 外观模式
updated_at: '2026-09-06'
---
# 外观模式

## 一句话结论

外观模式（Facade Pattern）用一个**门面对象**作为面向客户端的**简化前端接口**，把复杂子系统的多个类封装在背后，向客户端隐藏实现细节——客户端只与门面交互，从而降低耦合、简化使用。

## 核心概念

- **Facade（外观/门面）**：一个包装类，封装一组对子系统的调用，向客户端暴露简化接口。
- **Subsystem（子系统）**：由多个相互依赖的类构成的复杂系统，客户端原本需直接面对它们。
- **隐藏复杂性**：客户端不需要理解子系统内部结构即可使用其能力。
- **单一包装类**：门面通常是一个包含客户端所需成员的类，成员代表客户端访问子系统。

## 工作机制

1. 子系统内部保持原有结构，不做改动。
2. 门面类聚合子系统各组件，提供少数高层的便捷方法。
3. 客户端只调用门面方法，门面内部负责编排子系统对象完成请求。
4. 客户端不直接持有子系统类引用，减少客户端与子系统的耦合。

门面并不禁止客户端直接使用子系统——它提供的是"更简单、更常用的入口"，同时保留底层灵活性的出口。

## 示例或代码

以"计算机开机"为例——客户端只需调一次 `turnOn()`，无需逐个启动 CPU、内存、硬盘：

```java
class CPU { public void start() { System.out.println("CPU start"); } }
class Memory { public void load() { System.out.println("Memory load"); } }
class HardDrive { public void read() { System.out.println("HardDrive read"); } }

// Facade：门面，封装开机流程
public class Computer {
    private CPU cpu = new CPU();
    private Memory memory = new Memory();
    private HardDrive hd = new HardDrive();

    public void turnOn() {
        cpu.start();
        memory.load();
        hd.read();
    }
}

// 客户端只依赖门面
public class Client {
    public static void main(String[] args) {
        new Computer().turnOn(); // 一行搞定，隐藏内部三个子系统的细节
    }
}
```

## 常见误区

- **把外观当适配器**：外观提供"更简单的接口"；适配器把接口"转成另一个指定接口"（且必须尊重既有接口并支持多态行为）。
- **把外观当装饰器**：装饰器动态添加行为；外观只做入口简化、不改变行为语义。
- **误以为门面会封装子系统所有能力**：门面只暴露常用入口，应保留对子系统的直接访问。
- **把门面当作万能层**：门面不应承载业务逻辑，它只是转发与编排，否则会退化成"上帝对象"。

## 证据映射

| claim_id | 来源 | 要点 |
| --- | --- | --- |
| facade-pattern-definition | web-computer-science-facade-pattern | 门面对象作为前端接口遮蔽复杂底层代码，为客户端提供简化接口 |

## 待验证项

无。定义已由 web 源（Wikipedia Facade pattern 条目）锚定。

## 关联知识

- [[software-design]] —— 设计模式分类：外观属于结构型模式。
- [[object-oriented]] —— 封装与聚合是外观模式的基础。
- [[adapter-pattern]] —— 与外观易混淆；适配器转换接口，外观简化接口。
- [[decorator-pattern]] —— 也包装对象，但目的是动态添加行为。
- [[facade-pattern]] 相关——外观常用于给复杂子系统（如编译器、SDK）提供易用入口。
- [[class-diagram]] —— 用 UML 类图表达 Facade 与子系统各类的关系。

## 详细章节

### 定义

外观模式（Facade Pattern，也拼作 Façade）是 GoF 二十三种设计模式之一，属于结构型模式。类比建筑中的"门面"，它是充当**前端接口**、遮蔽更复杂的底层或结构性代码的对象。开发者常在系统非常复杂、由许多相互依赖的类组成，或源码不可用时采用该模式：隐藏大系统的复杂性，为客户端提供更简单的接口。

### 参与者

- **Facade**：知道哪些子系统类负责处理请求，把客户端请求委派给相应子系统对象。
- **Subsystem 类**：实现子系统功能，处理由 Facade 指派的工作；它们不知道 Facade 的存在。
- **Client**：只与 Facade 交互，不直接访问子系统类。

### 结构

```
Client → Facade ──► SubsystemClassA
                  ├─► SubsystemClassB
                  └─► SubsystemClassC
```

### 适用场景

- 需要为复杂子系统提供一个简单的统一入口。
- 希望减少客户端与子系统之间的耦合与依赖数量。
- 需要按层次组织子系统，用门面作为各层之间的通信点。
- 需要改善库的可用性与可读性，隐藏复杂交互（如一个简化 API 背后屏蔽多组件协作）。

### 优点与缺点

优点：

- 对客户端屏蔽子系统组件，降低客户端使用难度。
- 促进子系统与客户端之间的松耦合。
- 便于分层：门面成为层次间的边界。
- 可作为一个庞大的单体或紧耦合系统重构的起点。

缺点：

- 门面可能成为与所有类都耦合的"上帝对象"。
- 若客户端需要子系统更细粒度的能力，门面会成为瓶颈或需开洞（直接访问子系统）。
- 增加了一层间接，可能引入额外的调用开销。

### 与相关模式的关系

- **与适配器（Adapter）**：外观定义更简单的接口；适配器把一个接口转换成另一个接口。
- **与装饰器（Decorator）**：装饰器在不改变接口的情况下添加行为；外观隐藏子系统细节。
- **与中介者（Mediator）**：外观对子系统是"单向门面"；中介者协调多个对象的复杂交互。
- **与单例（Singleton）**：门面常实现为单例，因为通常只需一个门面实例。

## 参考
- https://en.wikipedia.org/wiki/Facade_pattern
