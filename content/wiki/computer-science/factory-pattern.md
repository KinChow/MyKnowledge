---
aliases:
- factory
- factory-method
- 工厂方法
- 工厂模式
confidentiality: public
domain: computer-science
evidence:
- claim: 工厂方法模式是一种设计模式，它使用工厂方法解决在创建对象时不指定其具体类的问题。
  claim_id: factory-pattern-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-338be05a0097
    exact: the factory method pattern is a design pattern that uses factory methods
      to deal with the problem of creating objects without having to specify their
      exact classes
  targets:
  - evidence_id: evidence-338be05a0097
    source_id: web-computer-science-factory-pattern
id: factory-pattern
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-factory-pattern
status: published
tags:
- design-pattern
- creational
- factory
- object-oriented
title: 工厂模式
updated_at: '2026-09-06'
---
# 工厂模式

## 一句话结论

工厂模式（标准名称为**工厂方法模式，Factory Method Pattern**）是一种**创建型设计模式**：**定义一个用于创建对象的接口，让子类决定实例化哪一个具体类，从而把对象的实例化延迟到子类**。客户端通过调用工厂方法而非 `new` 构造函数来创建对象，实现"面向抽象编程、解耦创建与使用"。

## 核心概念

- **工厂方法（factory method）**：一个专门用来创建对象的方法，客户端调用它而不是直接调用构造函数。
- **Product（产品）**：工厂方法所创建对象的抽象类型（接口/抽象类）。
- **ConcreteProduct（具体产品）**：具体被实例化的类。
- **Creator（创建者）**：声明工厂方法的抽象类/接口，可能提供默认实现。
- **ConcreteCreator（具体创建者）**：覆写工厂方法，决定实例化哪个具体产品。
- **延迟实例化（defer instantiation）**：把"实例化哪个类"的决定权从客户端下放给子类。

## 工作机制

### GoF 定义

> "定义一个创建对象的接口，但让子类决定要实例化哪个类。工厂方法让类把实例化延迟到子类。"
> （Define an interface for creating an object, but let subclasses decide which class to instantiate. Factory method lets a class defer instantiation to subclasses.）

### 解决的问题

- **如何让对象的子类重定义其后续且不同的实现？** 在超类中建立工厂方法，把对象的创建推迟到子类的工厂方法中完成。
- **如何把对象的实例化延迟到子类？** 通过调用工厂方法而不是直接调用构造函数来创建对象。

### 结构

- `Creator` 声明抽象方法 `factoryMethod()`；`ConcreteCreator` 实现 `factoryMethod()` 并实例化某个具体产品。
- 客户端持有 `Product` 抽象类型，对 `Creator` 调 `factoryMethod()` 获取产品，从而与具体被实例化的类解耦。
- 该模式**依赖继承**：对象创建被委托给实现工厂方法的子类（也可依赖接口实现）。

### 相比直接创建对象的好处

直接创建对象常伴随复杂过程，可能不适合放在使用它的对象内部：会产生大量重复代码、需要调用方不具备的信息、抽象层次不足或超出调用方职责范围。工厂方法通过一个独立的方法来创建对象，子类可覆写以指定要创建的产品派生类型。

## 示例或代码

**Java：**

```java
// 产品抽象与具体产品
interface Product { void use(); }

class ProductA implements Product {
    public void use() { System.out.println("Using Product A"); }
}

// Creator：定义工厂方法
abstract class Creator {
    public abstract Product factoryMethod();       // 延迟到子类
    public void businessLogic() {                   // 创建者自身的业务逻辑
        Product p = factoryMethod();
        p.use();
    }
}

// ConcreteCreator：子类决定实例化哪个类
class CreatorA extends Creator {
    public Product factoryMethod() { return new ProductA(); }
}

// 客户端
public class Main {
    public static void main(String[] args) {
        Creator creator = new CreatorA();
        creator.businessLogic();
    }
}
```

**Python：**

```python
class Product:
    def use(self): ...

class ProductA(Product):
    def use(self):
        print("Using Product A")

class Creator:
    def factory_method(self) -> Product:  # 抽象工厂方法
        raise NotImplementedError
    def business_logic(self):
        self.factory_method().use()

class CreatorA(Creator):
    def factory_method(self) -> Product:
        return ProductA()

CreatorA().business_logic()
```

**C++：**

```cpp
class Product { public: virtual ~Product() {} virtual void use() = 0; };
class ProductA : public Product { public: void use() override { /* ... */ } };

class Creator {
public:
    virtual ~Creator() {}
    virtual std::unique_ptr<Product> factoryMethod() = 0;
    void businessLogic() { factoryMethod()->use(); }
};

class CreatorA : public Creator {
public:
    std::unique_ptr<Product> factoryMethod() override {
        return std::make_unique<ProductA>();
    }
};
```

## 常见误区

- **把工厂方法与"简单工厂"混为一谈**：简单工厂把创建逻辑集中在一个静态方法里（每次加产品都要改它），不是 GoF 的工厂方法；工厂方法依赖**继承**与**覆写**来开闭。
- **把工厂方法与抽象工厂混淆**：工厂方法创建**单个**产品对象、依赖继承、由子类决定产品；抽象工厂创建**一族相关**产品、依赖对象组合、由工厂接口决定。
- **认为工厂方法只是"换一种 new"**：其价值在于**延迟实例化到子类**，让创建者不依赖具体类，从而支持在运行时替换产品。
- **为每个类都套工厂**：没有"创建复杂/易变/需要抽象"的需求时，直接 `new` 更简单，过度设计会引入无谓复杂度。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| factory-pattern-definition | web-computer-science-factory-pattern | 工厂方法模式用工厂方法解决"不指定具体类创建对象"的问题；通过调用工厂方法（而非构造函数）创建对象；工厂方法可在接口声明由子类实现，或在基类实现由子类覆写；属 GoF 23 个经典创建型模式 |

## 待验证项

无。

## 关联知识

- [[abstract-factory-pattern]] —— 抽象工厂模式：创建一族相关产品，通常可组合工厂方法。
- [[singleton-pattern]] —— 单例模式（工厂对象常以单例保存）。
- [[builder-pattern]] —— 建造者模式：分步构建复杂对象。
- [[prototype-pattern]] —— 原型模式：通过克隆创建对象。
- [[object-oriented]] —— 面向对象（继承、多态、基于接口编程）。
- [[software-design]] —— 软件设计总览：设计原则与设计模式。
- [[solid]] —— SOLID 五原则（开闭原则与工厂方法密切相关）。

## 详细章节

### 定义

工厂方法模式（Factory Method Pattern）是一种创建型设计模式：**定义一个创建对象的接口，但让子类决定要实例化哪一个类，从而把实例化延迟到子类**。它是 GoF《设计模式》中 23 个经典模式之一，核心思想是把"创建对象"从"使用对象"中解耦，并利用**继承 + 覆写**实现创建逻辑的开放扩展。

### 结构（参与者）

- **Product**：工厂方法所创建对象的抽象类型，定义产品的公共接口。
- **ConcreteProduct**：实现 `Product` 接口的具体产品类。
- **Creator**：声明工厂方法（可抽象、可带默认实现），通常还包含依赖于产品的业务逻辑。
- **ConcreteCreator**：实现/覆写工厂方法，返回具体的 `ConcreteProduct` 实例。

### 适用场景

- 对象的创建过程复杂、易重复、需要更高抽象层次，不适合放在使用它的对象内部。
- 客户端不知道（或不应知道）要实例化的具体类，需要延迟到运行时/子类决定。
- 需要在不修改现有创建者代码的情况下，通过新增子类引入新的产品类型（对扩展开放、对修改封闭）。
- 框架层常用工厂方法：框架定义 `Creator` 的骨架流程，用户通过子类覆写工厂方法注入具体对象（模板方法思想的配合）。

### 实现要点

- 工厂方法返回**抽象类型**（接口/抽象类），客户端只依赖抽象。
- 创建者可把工厂方法声明为抽象，也可提供默认实现并允许子类覆写。
- 工厂方法通常配合**模板方法**：`Creator` 的骨架方法调用 `factoryMethod()` 获取产品并处理。

### 优缺点

**优点**

- 客户端与具体产品解耦，符合"面向接口而非实现编程"。
- 符合**开闭原则**：新增产品只需新增 `ConcreteCreator`/`ConcreteProduct` 子类，不改既有代码。
- 把复杂创建逻辑从使用方剥离，避免重复代码、提升抽象层次。

**缺点**

- 每新增一种产品往往需要新增一个创建者子类，类数量膨胀。
- 引入额外的类与抽象层次，增加理解与维护成本。
- 若产品类型稳定、创建简单，使用工厂方法属于过度设计。

### 与其他模式的关系

- **工厂方法与抽象工厂**：工厂方法创建单个对象、基于继承；抽象工厂创建一族相关对象、基于对象组合，抽象工厂内部常组合多个工厂方法。
- **工厂方法与模板方法**：工厂方法是模板方法的一种特例（延迟步骤由子类实现）。
- **工厂方法与单例**：单例常作为"工厂对象的存放容器"，保证只有一个工厂实例。
- **工厂方法与原型**：原型通过克隆避免子类化创建者；工厂方法则通过子类化创建者来创建对象。

### 参考

- https://en.wikipedia.org/wiki/Factory_method_pattern
