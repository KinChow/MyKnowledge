---
aliases:
- cpp-class-struct
- cpp-类与结构体
- cpp-struct
confidentiality: public
domain: computer-science
evidence:
- claim: 类（class）是由类说明符（class-specifier）定义的用户自定义类型。
  claim_id: cpp-class-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-c1d493a5d1a7
    exact: Classes are user-defined types, defined by class-specifier, which appears
      in decl-specifier-seq of the declaration syntax.
  targets:
  - evidence_id: evidence-c1d493a5d1a7
    source_id: web-computer-science-cpp-class-and-struct
- claim: class、struct 与 union 都是类关键字（class-key）；class 与 struct 除默认成员访问与默认基类访问外完全相同。
  claim_id: cpp-class-vs-struct
  support: direct
  supporting_quotes:
  - evidence_id: evidence-0d439ba9d56a
    exact: class-key is one of class, struct and union. The keywords class and struct
      are identical except for the default member access and the default base class
      access.
  targets:
  - evidence_id: evidence-0d439ba9d56a
    source_id: web-computer-science-cpp-class-and-struct
id: cpp-class-and-struct
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-cpp-class-and-struct
status: published
tags:
- cpp
- class
- struct
- oop
- type
title: C++类与结构体
updated_at: '2026-09-06'
---
# C++类与结构体

## 一句话结论

C++ 的类（class）与结构体（struct）都是**用户自定义类型（user-defined type）**，由类说明符（class-specifier）定义。`class` 与 `struct` 两个关键字**几乎完全等价**，唯一区别是**默认成员访问权限**（class 默认 `private`，struct 默认 `public`）与**默认基类访问权限**（class 默认 `private` 继承，struct 默认 `public` 继承）。它们可以包含数据成员、成员函数、静态成员、嵌套类、构造函数、析构函数等，是 C++ 面向对象编程的核心载体。

## 核心概念

- **类（class）**：用户自定义类型，由 class-specifier 定义。
- **class-key**：`class`、`struct`、`union` 三者之一。
- **class vs struct 差异**：除默认成员访问与默认基类访问外，两者完全一致。
- **成员（members）**：数据成员、成员函数、静态成员、嵌套类、成员模板、位域（bit-field）、using 声明等。
- **访问说明符（access specifiers）**：`public` / `protected` / `private`，控制成员的可见性。
- **特殊成员函数**：默认构造、拷贝构造、移动构造（C++11）、拷贝赋值、移动赋值（C++11）、析构函数。
- **`this` 指针**：非静态成员函数内指向调用对象的指针。
- **继承与多态**：基类/派生类、虚函数、`override`/`final`（C++11）、纯虚函数与抽象类。

## 工作机制

- **定义**：`class-key attr(可选) class-head-name final(可选) base-clause(可选) { member-specification }`。
- **默认访问**：`class` 的成员默认 `private`；`struct` 的成员默认 `public`。继承同理：`class` 派生默认 `private` 继承，`struct` 派生默认 `public` 继承。
- **成员函数**：在类内声明、类外定义；非静态成员函数通过 `this` 访问调用对象。
- **构造函数与初始化列表**：`Class(...) : member(args), ... { }` 初始化成员；默认成员初始化器（C++11）提供类内初值。
- **析构函数**：对象生命周期结束时调用，用于释放资源（配合 RAII）。
- **继承与多态**：派生类继承基类成员；`virtual` 成员函数支持运行时多态；`override`（C++11）显式标记重写；`final`（C++11）禁止进一步派生或重写。
- **语法要点**：见下方代码示例。

## 示例或代码

**class 默认 private，struct 默认 public**：

```cpp
class C { int a; };      // a 默认 private
struct S { int b; };     // b 默认 public

// 显式指定访问级别更清晰
class Point {
public:
    Point(int x, int y) : x_(x), y_(y) {}
    int x() const { return x_; }
private:
    int x_, y_;
};
```

**继承的默认访问差异**：

```cpp
struct Base {};
class D1 : Base {};   // 默认 private 继承（class 派生）
struct D2 : Base {};  // 默认 public 继承（struct 派生）
```

**构造函数 / 析构 / 拷贝 / 移动（RAII 示例）**：

```cpp
#include <utility>

class Buffer {
public:
    explicit Buffer(std::size_t n) : data_(new int[n]), size_(n) {}
    ~Buffer() { delete[] data_; }                     // 析构释放资源

    Buffer(const Buffer& other)                       // 拷贝构造（深拷贝）
        : data_(new int[other.size_]), size_(other.size_) {
        for (std::size_t i = 0; i < size_; ++i) data_[i] = other.data_[i];
    }
    Buffer(Buffer&& other) noexcept                   // 移动构造（C++11）
        : data_(other.data_), size_(other.size_) { other.data_ = nullptr; }

    Buffer& operator=(const Buffer& other) { /* 拷贝赋值 */ return *this; }
    Buffer& operator=(Buffer&& other) noexcept {      // 移动赋值
        std::swap(data_, other.data_);
        std::swap(size_, other.size_);
        return *this;
    }
private:
    int* data_;
    std::size_t size_;
};
```

**继承与多态**：

```cpp
class Shape {
public:
    virtual ~Shape() = default;
    virtual double area() const = 0;   // 纯虚函数 → 抽象类
};

class Circle final : public Shape {    // final：不可再被派生
public:
    explicit Circle(double r) : r_(r) {}
    double area() const override { return 3.14159 * r_ * r_; }
private:
    double r_;
};
```

## 常见误区

- **以为 struct 不能有方法**：struct 与 class 几乎相同，都可以有构造函数、成员函数、继承等。
- **忘记默认访问差异**：`class` 默认 `private`、`struct` 默认 `public`；混用时可读性差，建议显式写访问说明符。
- **忽视特殊成员函数**：自定义析构/拷贝时要注意"三/五法则"（Rule of Three/Five），否则浅拷贝导致双重释放或悬垂。
- **把抽象类实例化**：含纯虚函数的类不能直接实例化，只能作为基类。
- **忽略 `this` 与 const 成员函数**：在 const 成员函数中修改成员会编译报错；`mutable` 成员例外。
- **过度使用继承**：能组合优先组合；继承应表达真正的 is-a 关系（与 [[solid]] 的开闭/里氏替换相关）。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| cpp-class-definition | web-computer-science-cpp-class-and-struct | 类是用户自定义类型，由 class-specifier 定义 |
| cpp-class-vs-struct | web-computer-science-cpp-class-and-struct | class 与 struct 仅默认成员/基类访问不同；union 引入联合体类型 |

## 待验证项

无。

## 关联知识

- [[cpp-union]] —— 联合体：class-key 之一，与 class/struct 并列但成员互斥共享地址。
- [[cpp-enum]] —— 枚举类型。
- [[cpp-template]] —— 模板：类模板实例化得到类类型。
- [[cpp-pointer]] —— 指针：`this` 指针、对象指针。
- [[cpp-fundamental-types]] —— C++ 基础类型。
- [[cpp-keywords]] —— `class`、`struct`、`public`、`private`、`virtual` 等关键字。
- [[cpp-class-and-raii]] —— RAII 与类资源管理。
- [[cpp-overview]] —— C++ 语言总览。
- [[object-oriented]] —— 面向对象范式。

## 详细章节

### C++类与结构体

#### 定义

类（class）是用户自定义类型（user-defined type），由类说明符（class-specifier）定义，类说明符出现在声明语法（declaration syntax）的 decl-specifier-seq 中。

#### 类说明符语法

```
class-key attr(可选) class-head-name final(可选) base-clause(可选) { member-specification }   (1)
class-key attr(可选) base-clause(可选) { member-specification }                                (2)
```

- `class-key` 是 `class`、`struct` 与 `union` 之一。关键字 `class` 与 `struct` 除默认成员访问与默认基类访问外完全相同。若为 `union`，则该声明引入联合体类型。
- `attr`（C++11）：任意数量的属性，可包含 `alignas` 说明符。
- `class-head-name`：被定义类的名称，可选地限定。
- `final`（C++11）：若存在，该类不能再被派生。
- `base-clause`：一个或多个基类以及每种继承方式的列表（见派生类）。
- `member-specification`：访问说明符、成员对象与成员函数声明/定义的列表。

#### 成员

类可包含：

- **数据成员（data members）**：对象的状态；
- **静态成员（static members）**：属于类而非单个对象；
- **成员函数（member functions）**：操作对象的函数；
- **嵌套类（nested classes）**；
- **成员模板（member templates）**；
- **位域（bit-fields）**；
- **using 声明**；
- **构造函数与成员初始化列表**、默认成员初始化器（C++11）；
- **友元（friend）**、`explicit`、转换构造函数；
- **特殊成员函数**：默认构造、拷贝/移动构造与赋值、析构函数。

#### 访问控制

成员访问说明符（member access specifiers）控制成员的可访问性：

- `public`：任何代码可访问；
- `protected`：类自身、友元与派生类可访问；
- `private`：仅类自身与友元可访问。

默认访问：`class` 为 `private`，`struct` 为 `public`。继承的默认访问同样：`class` 派生默认 `private` 基类访问，`struct` 派生默认 `public` 基类访问。

#### 特殊成员函数与 RAII

构造函数负责初始化（可配合成员初始化列表）；析构函数在对象生命周期结束时被调用，用于释放资源。自定义资源管理的类应遵守三/五法则：若需要自定义析构、拷贝构造或拷贝赋值中的任意一个，通常也需要另外两个（以及 C++11 起移动操作），以避免浅拷贝导致的悬垂指针或双重释放。

#### 继承与多态

派生类通过基类子句继承基类成员，并可用 `virtual` 成员函数实现运行时多态。`override`（C++11）用于显式声明重写基类虚函数；`final`（C++11）用于禁止继续派生或重写。含纯虚函数（`= 0`）的类是抽象类，不能被实例化。空基类优化（EBO）、虚基类等机制进一步丰富了继承体系。

#### 与 struct 的选择

`struct` 与 `class` 语义等价，仅是默认访问不同。惯例上：把"数据为主、行为为辅、默认公开"的轻量类型写成 `struct`，把"封装为主、默认私有"的类型写成 `class`。两者都可以自由混合成员函数、构造/析构与继承。

## 参考

- cppreference — Classes: https://en.cppreference.com/w/cpp/language/class
- cppreference — Class definition / struct specifier: https://en.cppreference.com/w/cpp/language/struct
- cppreference — Special member functions: https://en.cppreference.com/w/cpp/language/special_member_functions
