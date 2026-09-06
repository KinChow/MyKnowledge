---
aliases:
- singleton
- 单例
confidentiality: public
domain: computer-science
evidence:
- claim: 单例模式是一种软件设计模式，它将一个类的实例化限制为唯一的单个实例。
  claim_id: singleton-pattern-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-325ec7d0f256
    exact: the singleton pattern is a software design pattern that restricts the instantiation
      of a class to a singular instance
  targets:
  - evidence_id: evidence-325ec7d0f256
    source_id: web-computer-science-singleton-pattern
id: singleton-pattern
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-singleton-pattern
status: published
tags:
- design-pattern
- creational
- singleton
- object-oriented
title: 单例模式
updated_at: '2026-09-06'
---
# 单例模式

## 一句话结论

单例模式是一种**创建型设计模式**，它将一个类的实例化**限制为唯一的单个实例**，并提供一个**全局访问点**来获取该实例。它常用于系统中恰好需要一个对象来协调全局动作的场景（如日志器、配置管理器、数据库连接池、线程池、门面对象），且相比全局变量不会污染命名空间，还支持**惰性分配与初始化**。

## 核心概念

- **唯一实例**：确保一个类在系统生命周期内只存在一个实例。
- **全局访问点**：通过类级静态方法（如 `getInstance()` / `instance()`）让客户端随时取到唯一实例。
- **控制实例化**：私有化构造器，隐藏 `new` 的创建路径，客户端无法直接创建第二个实例。
- **惰性初始化（lazy allocation）**：实例在首次被访问时才创建，而全局变量在很多语言中会一直占用资源。
- **不污染命名空间**：单例作为类成员存在，不会像全局变量那样污染全局（或所在）命名空间。
- **来源**：术语源自数学中的"单例集合（singleton）"概念。

## 工作机制

### 三个承诺（Wikipedia 归纳）

1. **只存在一个实例**（ensure they only have one instance）。
2. **提供对该实例的便捷访问**（provide easy access to that instance）。
3. **控制自身实例化**（control their instantiation，例如隐藏类的构造函数）。

### 典型实现步骤

1. 将构造函数私有化（C++/Java 中同时禁用拷贝构造与拷贝赋值）。
2. 类内部持有一个指向唯一实例的静态成员（指针/引用/类变量）。
3. 提供静态方法 `instance()`：实例为空则创建并赋值，否则直接返回已有实例。
4. 多线程环境需保证线程安全（互斥锁、双重检查锁定 double-checked locking、静态内部类、Java 枚举等）。

### 与全局变量的区别

| | 全局变量 | 单例 |
| --- | --- | --- |
| 命名空间 | 污染全局/所在命名空间 | 作为类成员，不污染命名空间 |
| 资源占用 | 多数语言一直占用资源 | 支持惰性分配与初始化 |
| 访问控制 | 可被任意读写 | 可封装访问逻辑与状态 |

## 示例或代码

**Java（双重检查锁定 + volatile）：**

```java
public final class Config {
    private static volatile Config instance;
    private Config() { /* 私有构造，隐藏 new */ }
    public static Config getInstance() {
        if (instance == null) {                 // 第一次检查
            synchronized (Config.class) {        // 加锁
                if (instance == null) {          // 第二次检查（双检锁）
                    instance = new Config();
                }
            }
        }
        return instance;
    }
    public void load() { /* ... */ }
}
```

**C++（局部静态变量，C++11 起线程安全）：**

```cpp
class Logger {
public:
    static Logger& instance() {
        static Logger inst;   // 首次调用时构造，C++11 保证线程安全
        return inst;
    }
    void log(const std::string& msg) { /* ... */ }
    Logger(const Logger&) = delete;            // 禁用拷贝
    Logger& operator=(const Logger&) = delete; // 禁用赋值
private:
    Logger() = default;                        // 私有构造
};
```

**Python（模块级单例 / `__new__` 拦截）：**

```python
class DatabaseConnection:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def execute_query(self, sql): ...
```

## 常见误区

- **把单例等同于全局变量**：单例不污染命名空间、支持惰性初始化、可封装访问逻辑，与裸全局变量不同。
- **忽略线程安全**：懒汉式在多线程下可能创建出多个实例；需用双检锁/静态内部类/枚举等保证只初始化一次。
- **被序列化/反射/克隆破坏唯一性**：Java 序列化需 `readResolve()`、反射可调用私有构造、克隆可复制实例——需逐一防护。
- **滥用单例**：把依赖写成隐藏的全局状态，导致耦合与难测试；多数场景应优先使用依赖注入，而非进程内单例。
- **把"全局可访问"误当成"全局可变状态"**：单例仍可能有并发下的状态竞争问题，它只保证"一个实例"，不保证"线程安全"。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| singleton-pattern-definition | web-computer-science-singleton-pattern | 单例模式将类的实例化限制为唯一实例，是 GoF 设计模式之一；当系统恰需要一个对象协调动作时有用；允许类确保只有一个实例、提供便捷访问、控制实例化 |

## 待验证项

无。

## 关联知识

- [[factory-pattern]] —— 工厂方法模式（单例可作为其基础，对象创建由子类决定）。
- [[abstract-factory-pattern]] —— 抽象工厂模式（单例可作为工厂对象的存放位置）。
- [[builder-pattern]] —— 建造者模式。
- [[prototype-pattern]] —— 原型模式。
- [[object-oriented]] —— 面向对象（封装、抽象、继承、多态）。
- [[software-design]] —— 软件设计总览：设计原则与设计模式。
- [[uml]] —— UML 建模（类图/对象图）。

## 详细章节

### 定义

单例模式（Singleton Pattern）是一种创建型设计模式：**保证一个类仅有一个实例，并提供一个访问它的全局访问点**。它是《设计模式：可复用面向对象软件的基础》（GoF 四书）中 23 个经典模式之一，属于创建型模式。模式名称来自数学概念"单例集合"——只包含一个元素的集合。

### 结构（参与者）

- **Singleton（单例类）**
  - 持有一个静态私有成员，保存唯一实例。
  - 将构造函数私有化（并禁用拷贝/赋值），阻止外部直接实例化。
  - 提供一个静态方法（如 `instance()` / `getInstance()`）作为全局访问点，负责"首次创建、之后复用"。

### 适用场景

- 系统中**恰好需要一个对象**来协调跨模块动作，例如日志器（所有对象需要统一写入点）、配置管理器、数据库连接池、线程池。
- 需要**惰性分配与初始化**，避免全局变量常驻占用资源。
- 门面（Facade）对象常被实现为单例，因为只需要一个门面对象。
- 作为其他模式的基础：抽象工厂、工厂方法、建造者、原型等模式中的"工厂对象"常以单例形式全局存放。

### 实现方式

1. **饿汉式（eager）**：类加载时即创建，线程安全但可能浪费资源、启动变慢。
2. **懒汉式（lazy）+ 方法级同步**：简单但每次访问都加锁，性能差。
3. **双重检查锁定（double-checked locking）**：先无锁检查、再加锁二次检查，需 `volatile` 防止指令重排。
4. **静态内部类（holder）**：Java 中通过静态内部类持有实例，兼顾懒加载与线程安全。
5. **枚举（Java enum）**：天然防止反射/序列化破坏，是最推荐的方式之一。
6. **局部静态变量（C++11 起）**：函数内静态局部变量的初始化由标准保证线程安全。

### 优缺点

**优点**

- 保证唯一实例，避免重复创建与状态不一致。
- 提供全局访问点，方便调用。
- 惰性初始化，按需创建、节省资源。
- 相比全局变量不污染命名空间。

**缺点**

- 隐藏依赖关系，难以进行单元测试（需重置实例或引入依赖注入）。
- 全局可变状态会引入隐式耦合与并发问题。
- 可能被过度使用，成为"披着单例外衣的全局变量"。
- 多线程实现有额外复杂度与出错风险。

### 与其他模式的关系

- 单例可作为**抽象工厂/工厂方法/建造者/原型**模式中"工厂/原型对象"的宿主（常以单例保存）。
- **门面（Facade）** 对象常实现为单例。
- 单例与**依赖注入/对象池**在"对象生命周期管理"目标上互补：单例是进程内唯一实例，对象池是复用多个实例。

### 参考

- https://en.wikipedia.org/wiki/Singleton_pattern
