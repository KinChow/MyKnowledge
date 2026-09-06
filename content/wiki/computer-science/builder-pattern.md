---
aliases:
- builder
- 建造者
- 生成器
confidentiality: public
domain: computer-science
evidence:
- claim: 建造者模式将复杂对象的构建与其表示分离。
  claim_id: builder-pattern-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-d8f8bf13741f
    exact: The builder pattern separates the construction of a complex object from
      its representation
  targets:
  - evidence_id: evidence-d8f8bf13741f
    source_id: web-computer-science-builder-pattern
id: builder-pattern
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-builder-pattern
status: published
tags:
- design-pattern
- creational
- builder
- object-oriented
title: 建造者模式
updated_at: '2026-09-06'
---
# 建造者模式

## 一句话结论

建造者模式是一种**创建型设计模式**：**将一个复杂对象的构建与它的表示分离**，使得**同一个构建过程可以创建不同的表示**。它把"如何一步步构建复杂对象"封装到独立的 `Builder` 对象中，客户端（或 `Director`）不直接创建复杂对象，而是委托给建造者，通常配合**方法链（method chaining）/ 流畅 API（fluent API）**使用。

## 核心概念

- **Product（产品）**：被构建的复杂对象。
- **Builder（建造者接口）**：定义构建产品各部件的方法（如 `buildPartA()`、`buildPartB()`）以及返回产品的方法。
- **ConcreteBuilder（具体建造者）**：实现 `Builder` 接口，负责实际创建并组装各部件，提供获取最终产品的方法。
- **Director（导演）**：定义并控制**构建过程的顺序**，调用建造者的各 `buildPart` 方法；导演不依赖具体建造者类。
- **方法链 / 流畅 API**：`buildX()` 返回建造者自身，支持链式调用，最终 `build()` 产出产品。

## 工作机制

### GoF 意图

> 建造者设计模式的意图是**把复杂对象的构建与其表示分离**；这样一来，同一个构建过程可以创建不同的表示。
> （The intent of the builder design pattern is to separate the construction of a complex object from its representation. By doing so, the same construction process can create different representations.）

### 解决的问题

- **如何让一个类（同一构建过程）创建同一复杂对象的不同表示？**
- **如何简化"负责创建复杂对象"的类？**

直接在类中创建并组装复杂对象是不灵活的：它把该类"绑定"到某一种特定表示上，之后想独立地改变表示就必须修改该类。建造者模式把"创建并组装复杂对象各部件"封装进独立的 `Builder` 对象中。

### 工作流程

1. `Director` 持有 `Builder` 接口。
2. `Director` 按固定顺序调用 `builder.buildPartA()`、`buildPartB()` 等。
3. `ConcreteBuilder` 在每一步实际创建并组装对应的产品部件。
4. `Director` 完成后调用 `builder.getResult()` 取得最终产品。
5. 同一 `Director`（同一构建过程）换成不同的 `ConcreteBuilder`，即可得到不同的产品表示。

### UML 说明（时序）

`Director` 调用 `Builder1.buildPartA()` → 创建并组装 `ProductA1`；再调用 `buildPartB()` → 创建并组装 `ProductB1`；`Builder1` 实现了 `Builder` 接口，因此 `Director` 与"具体被实例化的类（即哪种表示被创建）"解耦。

## 示例或代码

**Java（经典 Builder + 流畅 API）：**

```java
// 产品
public class Computer {
    private final String cpu;
    private final String ram;
    private final String storage;
    private Computer(Builder b) {
        this.cpu = b.cpu; this.ram = b.ram; this.storage = b.storage;
    }
    // 建造者
    public static class Builder {
        private String cpu;
        private String ram;
        private String storage;
        public Builder cpu(String v) { this.cpu = v; return this; }   // 链式
        public Builder ram(String v) { this.ram = v; return this; }
        public Builder storage(String v) { this.storage = v; return this; }
        public Computer build() { return new Computer(this); }
    }
}

// 客户端：同一构建过程产出不同表示
Computer gaming = new Computer.Builder()
        .cpu("i9").ram("64GB").storage("2TB SSD").build();
Computer office  = new Computer.Builder()
        .cpu("i5").ram("16GB").storage("512GB SSD").build();
```

**Python：**

```python
class Computer:
    def __init__(self, cpu="", ram="", storage=""):
        self.cpu, self.ram, self.storage = cpu, ram, storage

class ComputerBuilder:
    def __init__(self):
        self._cpu = ""
        self._ram = ""
        self._storage = ""
    def cpu(self, v): self._cpu = v; return self     # 返回自身以链式调用
    def ram(self, v): self._ram = v; return self
    def storage(self, v): self._storage = v; return self
    def build(self):
        return Computer(self._cpu, self._ram, self._storage)

gaming = ComputerBuilder().cpu("i9").ram("64GB").build()
```

**C++：**

```cpp
class Computer {
public:
    void setCpu(const std::string& c) { cpu_ = c; }
    // ...
private:
    std::string cpu_;
};

class Builder {
public:
    virtual ~Builder() {}
    virtual void buildCpu() = 0;
    virtual void buildRam() = 0;
    virtual Computer getResult() = 0;
};

class GamingBuilder : public Builder {
    Computer c_;
public:
    void buildCpu() override { c_.setCpu("i9"); }
    void buildRam() override { /* ... */ }
    Computer getResult() override { return c_; }
};

class Director {
    Builder* b_;
public:
    Director(Builder* b) : b_(b) {}
    void construct() { b_->buildCpu(); b_->buildRam(); }
};
```

## 常见误区

- **把建造者当成"参数很多的构造函数"的替代品**：它不仅是解决构造参数过多，其本质是**分离"构建过程"与"表示"**，让同一过程产出不同表示。
- **混淆建造者与工厂**：工厂关注"创建**哪个**对象"（一次性产出成品）；建造者关注"如何**分步构建**一个复杂对象"（`Director` 控制步骤顺序）。
- **混淆建造者与抽象工厂**：抽象工厂创建一族相关对象、返回抽象类型；建造者创建**一个**复杂对象并返回完整产品，且逐步构建。
- **忽略 Director 角色**：省略 `Director` 只是"客户端直接指挥建造者"的变体，仍应保证构建顺序与部件组装的解耦，否则容易退回"类内直接组装"的旧问题。
- **以为方法链必须返回 `this`**：方法链是建造者的常见便捷实现（fluent API），但不是必须；也可用独立 `Director` 显式控制步骤。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| builder-pattern-definition | web-computer-science-builder-pattern | 建造者模式为对象创建问题提供灵活方案；把复杂对象的构建与其表示分离；是 GoF 23 个经典创建型模式之一；同一构建过程可通过不同 Builder 对象创建不同表示 |

## 待验证项

无。

## 关联知识

- [[factory-pattern]] —— 工厂方法模式：一次性创建单个对象，与建造者"分步构建"不同。
- [[abstract-factory-pattern]] —— 抽象工厂模式：创建一族相关对象。
- [[singleton-pattern]] —— 单例模式。
- [[prototype-pattern]] —— 原型模式：通过克隆创建对象。
- [[object-oriented]] —— 面向对象（封装、抽象）。
- [[software-design]] —— 软件设计总览：设计原则与设计模式。
- [[uml]] —— UML 建模（类图/时序图）。

## 详细章节

### 定义

建造者模式（Builder Pattern）是一种创建型设计模式：**把一个复杂对象的构建过程与它的表示分离**，使同一个构建过程能够创建不同的表示。它是 GoF《设计模式》中 23 个经典模式之一，核心在于把"构建复杂对象的步骤"从"对象的具体表示"中解耦。

### 结构（参与者）

- **Builder**：为创建产品的各个部件声明抽象接口（`buildPartA()`、`buildPartB()`、`getResult()` 等）。
- **ConcreteBuilder**：实现 `Builder` 接口，构造并组装产品部件，提供检索产品的方法。
- **Director**：使用 `Builder` 接口构造对象，负责定义构建的步骤与顺序。
- **Product**：被构建的复杂对象，包含由建造者创建的部件。

### 适用场景

- 对象的构造过程**步骤多、顺序固定**，且希望**同一过程产出不同表示**（如不同配置的电脑、不同口味的餐品、不同格式的文档）。
- 希望把"复杂对象如何组装"从使用它的类中抽离，简化该类。
- 需要避免"构造函数参数爆炸"（很多可选参数），用链式/命名参数提高可读性。
- 需要**分阶段**构造，且构建中间状态或顺序不应暴露给客户端。

### 实现要点

- 所有构建步骤放在 `Builder` 接口；`Director` 只依赖 `Builder` 接口，与具体建造者解耦。
- 链式（fluent）风格：`buildX()` 返回 `Builder` 自身，末尾 `build()` 产出不可变产品。
- 产品可设为**不可变**：构建器持有字段，`build()` 时一次性复制到产品，提升安全性。

### 优缺点

**优点**

- 把构建过程与表示分离，同一过程可产出不同表示。
- 将复杂对象的组装细节封装，客户端只需指定"要什么"，不用关心"怎么拼"。
- 提高代码可读性（链式/命名参数），避免构造函数参数爆炸。
- 对新增表示（新 `ConcreteBuilder`）开放，符合开闭原则。

**缺点**

- 每个产品都要至少一个 `ConcreteBuilder`，类数量增多。
- 比直接构造更繁琐；产品结构简单时属于过度设计。
- 若产品部件易变，"构建步骤"也会随之调整，需要同步维护 `Builder` 与 `Director`。

### 与其他模式的关系

- **与抽象工厂**：两者都强调构建复杂对象；抽象工厂返回"一族相关对象"，建造者逐步构建"一个复杂对象"。抽象工厂可作为建造者中"生产部件"的手段。
- **与工厂方法**：工厂方法"一步"创建对象，建造者"多步"构建对象。
- **与模板方法**：`Director` 的构建流程类似模板方法——步骤顺序固定，具体部件由 `ConcreteBuilder` 决定。
- **与单例**：建造者对象通常每次构建新建（有状态），不同于单例的"唯一实例"。

### 参考

- https://en.wikipedia.org/wiki/Builder_pattern
