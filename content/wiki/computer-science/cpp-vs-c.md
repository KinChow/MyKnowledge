---
aliases:
- c-vs-c
confidentiality: public
domain: computer-science
evidence:
- claim: 'C++ language

    From cppreference.com'
  claim_id: cpp-vs-c-audit-1
  support: direct
  supporting_quotes:
  - evidence_id: evidence-cb5fe00c391e
    exact: 'C++ language

      From cppreference.com'
  targets:
  - evidence_id: evidence-cb5fe00c391e
    source_id: web-computer-science-c-vs-c
id: cpp-vs-c
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-c-vs-c
- working-computer-science-c-vs-c
status: published
tags:
- cpp
- c
- oop
- comparison
- programming-language
title: C++ VS C
updated_at: '2026-09-06'
---
# C++ VS C

## 一句话结论

C++ 是 C 语言的超集，几乎完美兼容 C；C++ 的精髓在于面向对象编程（封装、继承、多态），而 C 是面向过程语言（程序被分解为函数、自上而下），两者的核心差异正是 OOP 与 POP 编程范式之别。

## 核心概念

- **面向对象编程（OOP）**：程序被分解为对象（class）；自下而上；支持继承；通过 public/private/protected 控制权限；通过 class 封装控制数据可见性；继承后可产生多态，子类可替代父类。
- **面向过程编程（POP）**：程序被分解为函数（function）；自上而下；不支持继承；无法控制权限，只能依照文件做有限的权限控制（实际上仍能使用 extern）；所有数据全局可见；没有继承就没有多态。
- **C++ 是 C 的超集**：C 语言功能非常强大（Unix 就是 C 语言编写），C++ 几乎完美兼容 C。

## 工作机制

- **封装**：C++ 将数据（变量）和操作数据的方法（函数）包装在一起，隐藏实现细节、暴露有限接口，提高可维护性和安全性。
- **继承**：子类可扩展和重写父类方法，增强代码复用、简化代码结构、提高开发效率。
- **多态**：同一接口可以被不同对象实现、可以有不同行为，可通过重写（override）实现，提高代码灵活性和可扩展性。
- **struct 区别**：C 语言中 `struct` 不能包含函数、不支持继承、不支持构造/析构、不支持运算符重载、不支持模板、无访问修饰符、内存布局因编译器而异且须显式使用 `struct` 关键字；C++ 中 `struct` 可包含成员函数、可继承、可有构造/析构、可重载运算符、可为模板 `struct`、可用 `alignas` 控制对齐、可用 public/protected/private 修饰成员、定义后无需再写 `struct` 关键字。

## 示例或代码

```cpp
// C 语言：struct 只能组合数据，必须显式使用 struct 关键字
struct Point { int x; int y; };
struct Point p;

// C++：struct 可以有成员函数，定义后无需 struct 关键字
struct Point {
    int x, y;
    int sum() const { return x + y; }
};
Point p{1, 2};
```

## 常见误区

- **以为"C++ 是 C 的超集"等于两者等价**：C++ 几乎完美兼容 C，但精髓是面向对象编程（封装、继承、多态），C 则是面向过程编程。
- **以为 C 语言无法实现权限控制**：C 中数据全局可见，只能依照文件做有限权限控制，但实际上还是能使用 `extern`。
- **以为 C++ 的 struct 与 C 相同**：C++ 中 struct 拥有成员函数、继承、构造/析构、运算符重载、模板等面向对象特性，与 C 中仅做数据组合的 struct 差异显著。
- **以为 C 可以做到继承/多态**：C 不支持继承，没有继承就没有多态。

## 证据映射

| claim_id | 来源 | 要点 |
| --- | --- | --- |
| cpp-vs-c-audit-1 | web-computer-science-c-vs-c | C++ 语言（源自 cppreference.com）作为对比的基准来源 |

## 待验证项

无

## 关联知识

- [[cpp-overview]]：C++ 语言概述与特性
- [[cpp-vs-java]]：C++ 与 Java 的对比
- [[cpp-vs-python]]：C++ 与 Python 的对比
- [[cpp-class-and-raii]]：C++ 对象生命周期与面向对象机制

## 详细章节

### C++ VS C

* ﻿﻿C++是C语言的超集，基于C语言的体系开发
* ﻿﻿C语言功能非常强大，Unix就是C语言编写的。﻿
* ﻿﻿C++几乎完美兼容了C语言
* ﻿﻿C++的精髓在于面向对象编程：封装、继承、多态



#### 面向对象编程（OOP）和面向过程编程（POP）

* Object Oriented Programing
  * 程序被分解为对象（class）
  * 自下而上
  * 支持对象的继承
  * 通过public private protect来控制权限
  * 通过class封装来控制数据的可见与否
  * 继承以后可以产生多态，子类可以替代父类
* Procedural Oriented Programming
  * 程序被分解为函数（function）
  * 自上而下
  * 不支持继承
  * 无法控制权限，只能依照文件而不是代码做有限的权限控制（但实际上还是能使用extern）
  * 所有数据全局可见
  * 没有继承就没有多态



##### 封装

C++的封装，将数据（变量）和操作数据的方法（函数）包装在一起

* ﻿隐藏实现细节
* ﻿暴露有限接口供外部调用
* ﻿提高了可维护性和安全性



##### 继承

C++的继承，子类可以拓展和重写父类方法

* ﻿﻿增强了代码的复用
* ﻿﻿简化代码结构
* ﻿﻿提高开发效率



##### 多态

C++的多态，同一接口可以被不同对象实现，可以有不同行为

* ﻿可以通过重写override实现
* ﻿提高了代码的灵活性和可拓展性





#### struct区别

* 函数成员：

  - C语言中，`struct`不能包含函数。

  - C++中，`struct`可以包含成员函数，这使得`struct`可以像类（class）一样拥有行为。

* 继承：

  - C语言的`struct`不支持继承。

  - C++的`struct`可以继承自其他`struct`或`class`，这是面向对象编程的一个重要特性。

* 构造函数和析构函数：

  - C语言的`struct`不支持构造函数和析构函数。

  - C++的`struct`可以有构造函数和析构函数，这允许在创建和销毁`struct`实例时执行特定的代码。

- 运算符重载：

  - C语言不支持运算符重载。

  - C++允许在`struct`中重载运算符，这使得`struct`可以使用像加法、减法等自定义的运算。

- 模板：

  - C语言不支持模板。

  - C++中的`struct`可以是模板`struct`，这允许创建泛型数据结构，可以用于不同类型的数据。

- 内存对齐：

  - C语言对内存对齐的要求比较宽松，`struct`的布局可能因编译器而异。

  - C++提供了`alignas`关键字，允许开发者指定`struct`成员的对齐方式，以确保跨平台的一致性和性能。

- 访问修饰符：

  - C语言中，`struct`成员没有明确的访问修饰符。

  - C++中，可以使用`public`、`protected`和`private`关键字来修饰`struct`的成员。

- 使用：

  * C语言中，必须显式使用 `struct` 关键字来声明结构。 

  * C++中，不需要在定义该类型之后使用 `struct` 关键字。
