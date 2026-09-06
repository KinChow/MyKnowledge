---
aliases:
- abstract-factory
- 抽象工厂
confidentiality: public
domain: computer-science
evidence:
- claim: 抽象工厂模式是一种软件工程设计模式，提供了一种创建相关对象族而不强制其具体类的方式。
  claim_id: abstract-factory-pattern-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-a5bf12e5cae1
    exact: The abstract factory pattern in software engineering is a design pattern
      that provides a way to create families of related objects without imposing their
      concrete classes
  targets:
  - evidence_id: evidence-a5bf12e5cae1
    source_id: web-computer-science-abstract-factory-pattern
id: abstract-factory-pattern
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-abstract-factory-pattern
status: published
tags:
- design-pattern
- creational
- factory
- object-oriented
title: 抽象工厂模式
updated_at: '2026-09-06'
---
# 抽象工厂模式

## 一句话结论

抽象工厂模式是一种**创建型设计模式**：它**提供一个创建一系列相关或相互依赖对象的接口，而无需指定它们的具体类**。通过把一组具有共同主题的"单个工厂"封装在一个工厂接口下，客户端用该通用接口创建**一族**相关对象，从而把"对象的创建细节"与"对象的使用"解耦。

## 核心概念

- **对象族（families of related objects）**：一组在逻辑上相关、需要一起使用且保持一致性的产品对象（如一套 UI 的按钮 + 文本框 + 滚动条）。
- **AbstractFactory（抽象工厂）**：声明创建一族产品对象的接口。
- **ConcreteFactory（具体工厂）**：实现抽象工厂，生产某一特定"主题/变体"的具体产品。
- **AbstractProduct（抽象产品）**：一族产品各自的抽象类型。
- **ConcreteProduct（具体产品）**：具体工厂实际创建的产品实例。
- **对象组合（object composition）**：该模式依赖组合——对象创建实现在工厂接口暴露的方法中，工厂对象可在运行时被替换。

## 工作机制

### GoF 定义

> 《设计模式》把抽象工厂描述为"**一个用于创建一族相关或相互依赖对象的接口，而不指定它们的具体类**"。
> （"an interface for creating families of related or dependent objects without specifying their concrete classes."）

### 工作流程

1. 客户端组件创建**抽象工厂的具体实现**（选择某一主题/变体）。
2. 客户端通过**工厂的通用接口**调用创建方法。
3. 工厂方法内部**实际创建**具体对象，但只向客户端返回**抽象类型**的引用/指针。
4. 客户端只知道产品接口，不知道收到的具体对象类型，因此可在运行时无缝更换工厂来切换整族产品。

### 解决的问题

- **封装对象创建**：在一个独立的（工厂）对象中定义并实现创建对象的接口。
- **委托对象创建**：把创建委托给工厂对象，而不是直接创建对象。
- 让类独立于"对象如何被创建"；类可被配置一个工厂对象并用它创建对象，工厂对象可在运行时被交换。

### 设计意图

将一组对象的**实现细节**与它们的**通用用法**分离。引入新的派生类型时，无需改动使用基类的代码——工厂是代码中"具体类在此构造"的位置，模式旨在把"创建"与"使用"隔离。

## 示例或代码

**Java：**

```java
// 抽象产品
interface Button { void render(); }
interface TextBox { void show(); }

// 抽象工厂：声明创建一族产品的接口
interface UIFactory {
    Button createButton();
    TextBox createTextBox();
}

// 具体产品（变体 A：Dark 主题）
class DarkButton implements Button {
    public void render() { System.out.println("Dark button"); }
}
class DarkTextBox implements TextBox {
    public void show() { System.out.println("Dark textbox"); }
}

// 具体工厂（变体 A）
class DarkUIFactory implements UIFactory {
    public Button createButton() { return new DarkButton(); }
    public TextBox createTextBox() { return new DarkTextBox(); }
}

// 客户端：只依赖抽象接口
public class App {
    private final Button button;
    private final TextBox textBox;
    public App(UIFactory factory) {          // 运行时注入具体工厂
        this.button = factory.createButton();
        this.textBox = factory.createTextBox();
    }
    public void render() { button.render(); textBox.show(); }

    public static void main(String[] args) {
        new App(new DarkUIFactory()).render();   // 换一个工厂即换整族产品
    }
}
```

**C++：**

```cpp
class Button { public: virtual void render() = 0; virtual ~Button() {} };
class TextBox { public: virtual void show() = 0; virtual ~TextBox() {} };

class UIFactory {
public:
    virtual ~UIFactory() {}
    virtual std::unique_ptr<Button> createButton() = 0;
    virtual std::unique_ptr<TextBox> createTextBox() = 0;
};

class DarkButton : public Button { public: void render() override {} };
class DarkTextBox : public TextBox { public: void show() override {} };

class DarkUIFactory : public UIFactory {
public:
    std::unique_ptr<Button> createButton() override {
        return std::make_unique<DarkButton>();
    }
    std::unique_ptr<TextBox> createTextBox() override {
        return std::make_unique<DarkTextBox>();
    }
};
```

**Python：**

```python
class Button:
    def render(self): ...
class TextBox:
    def show(self): ...

class UIFactory:
    def create_button(self) -> Button: ...
    def create_text_box(self) -> TextBox: ...

class DarkButton(Button):
    def render(self): print("Dark button")
class DarkTextBox(TextBox):
    def show(self): print("Dark textbox")

class DarkUIFactory(UIFactory):
    def create_button(self) -> Button: return DarkButton()
    def create_text_box(self) -> TextBox: return DarkTextBox()

def build_app(factory: UIFactory):
    factory.create_button().render()
    factory.create_text_box().show()

build_app(DarkUIFactory())
```

## 常见误区

- **把抽象工厂与工厂方法混淆**：工厂方法创建**单个**对象、靠继承、由子类决定产品；抽象工厂创建**一族**对象、靠对象组合、由工厂接口决定整族产品（抽象工厂常组合多个工厂方法）。
- **误以为抽象工厂只是"多个工厂方法"的集合**：核心是**保证一族产品的一致性与可交换性**，且产品族整体可在运行时替换。
- **忽略"增加新产品"的代价**：抽象工厂对"增加新产品类型"不友好——往抽象工厂接口里加一个创建方法，所有具体工厂都要改；对"增加新变体（具体工厂）"友好。
- **用抽象工厂包装简单的、单一产品的创建**：没有"一族产品需保持一致"的需求时，工厂方法或直接 `new` 更合适，抽象工厂会引入不必要的复杂与抽象。
- **以为抽象工厂能解决所有创建问题**：过度抽象会增加调试与维护难度（分离与抽象层次越高，系统越难调试维护）。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| abstract-factory-pattern-definition | web-computer-science-abstract-factory-pattern | 抽象工厂通过封装一组具有共同主题的工厂来创建"相关对象族"而不强制具体类；客户端创建具体工厂实现，用通用接口创建属于该族的对象，不知具体类型；将对象族实现细节与通用用法分离，依赖对象组合，工厂对象可在运行时交换 |

## 待验证项

无。

## 关联知识

- [[factory-pattern]] —— 工厂方法模式：创建单个对象；抽象工厂通常组合工厂方法。
- [[singleton-pattern]] —— 单例模式（工厂对象常全局以单例保存）。
- [[builder-pattern]] —— 建造者模式：分步构建复杂对象。
- [[prototype-pattern]] —— 原型模式：通过克隆创建对象。
- [[object-oriented]] —— 面向对象（抽象、接口、多态）。
- [[software-design]] —— 软件设计总览：设计原则与设计模式。
- [[solid]] —— SOLID 五原则（依赖倒置、开闭原则）。

## 详细章节

### 定义

抽象工厂模式（Abstract Factory Pattern）是一种创建型设计模式：**提供一个创建一族相关或相互依赖对象的接口，而无需指定它们的具体类**。它是 GoF《设计模式》中 23 个经典模式之一，通过"封装一组具有共同主题的单个工厂"来创建对象族，依赖**对象组合**而非继承。

### 结构（参与者）

- **AbstractFactory**：声明创建一族抽象产品对象的接口（如 `createProductA()`、`createProductB()`）。
- **ConcreteFactory**：实现抽象工厂，为某一具体变体生产对应的具体产品。
- **AbstractProductA / AbstractProductB**：一族产品各自的抽象接口。
- **ConcreteProductA1 / ConcreteProductA2 / ...**：具体产品类。
- **Client**：仅依赖 `AbstractFactory` 与 `AbstractProduct` 接口；在运行时被注入具体工厂。

### 适用场景

- 需要创建**一族相关且必须保持一致**的对象（如同一操作系统主题下的窗口控件）。
- 希望客户端**不依赖具体类**，通过可交换的工厂在运行时切换整族产品。
- 需要把"产品族的实现细节"与"通用用法"分离，允许引入新变体而无需改动使用基类的代码。
- 工厂对象需要被配置/注入到一个类中，并在运行时被替换。

### 实现要点

- 工厂方法返回**抽象类型**的引用/指针；实际对象在具体工厂内构造。
- 工厂可被全局存放（常以单例实现），所有客户端代码通过单例获取正确工厂。
- 结合**工厂方法**：抽象工厂的每个创建方法可用工厂方法实现。
- 换产品族 = 换具体工厂，通常只需改动客户端的一行（注入不同工厂）。

### 优缺点

**优点**

- 保证一族产品的一致性，避免混用不匹配的产品。
- 客户端与具体类彻底解耦，符合"面向接口编程"。
- 对"新增产品族/变体"开放——新增一个具体工厂即可，不改客户端与既有工厂。
- 便于运行时切换整族产品（工厂对象可交换）。

**缺点**

- 对"新增产品类型"不友好：抽象工厂接口一旦新增方法，所有具体工厂都要同步实现。
- 引入较多类与抽象层次，增加初始编写、调试与维护成本。
- 分离与抽象程度越高，系统越难定位与修复问题；简单场景下属于过度设计。

### 与其他模式的关系

- **与工厂方法**：抽象工厂常由一组工厂方法组成；工厂方法创建单个产品，抽象工厂创建产品族。
- **与单例**：抽象工厂的工厂对象常以单例形式全局存储与访问。
- **与建造者**：两者都强调"构建复杂对象"，但抽象工厂强调"创建一族产品的一致性"，建造者强调"同一构建过程产出不同表示"。
- **与原型**：原型通过克隆原型实例创建对象，可被抽象工厂用作产品创建的实现手段。

### 参考

- https://en.wikipedia.org/wiki/Abstract_factory_pattern
