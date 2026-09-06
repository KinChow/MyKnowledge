---
aliases:
- cpp-templates
- cpp-模板
confidentiality: public
domain: computer-science
evidence:
- claim: 模板是 C++ 实体，用于定义一族类（类模板）、一族函数（函数模板）、一族类型的别名（别名模板，C++11）、一族变量（变量模板，C++14）或概念（C++20）。
  claim_id: cpp-template-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-39b24f86fcf1
    exact: 'A template is a C++ entity that defines one of the following: a family
      of classes (class template), which may be nested classes; a family of functions
      (function template), which may be member functions; an alias to a family of
      types (alias template) (since C++11); a family of variables (variable template)
      (since C++14); a concept (constraints and concepts) (since C++20).'
  targets:
  - evidence_id: evidence-39b24f86fcf1
    source_id: web-computer-science-cpp-template
- claim: 模板由一个或多个模板参数参数化，模板参数分为三类：类型模板参数、非类型模板参数与模板模板参数。
  claim_id: cpp-template-parameters
  support: direct
  supporting_quotes:
  - evidence_id: evidence-a709323bd176
    exact: 'Templates are parameterized by one or more template parameters, of three
      kinds: type template parameters, non-type template parameters, and template
      template parameters.'
  targets:
  - evidence_id: evidence-a709323bd176
    source_id: web-computer-science-cpp-template
id: cpp-template
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-cpp-template
status: published
tags:
- cpp
- template
- generic-programming
- type
title: C++模板
updated_at: '2026-09-06'
---
# C++模板

## 一句话结论

C++ 模板（template）是一种**参数化的类型构造机制**：它定义一个 C++ 实体，用来表示一族类（类模板）、一族函数（函数模板）、一族类型的别名（别名模板）、一族变量（变量模板）或一个概念（concept）。模板由一个或多个模板参数参数化，提供实参（或由实参推导）后，实参替换形参得到模板的特化（specialization）——即具体的类型或函数。它是 C++ 泛型编程的基础。

## 核心概念

- **模板（template）**：定义一族类、一族函数、一族类型别名、一族变量或概念的 C++ 实体。
- **模板参数（template parameters）**：三类——类型模板参数（type）、非类型模板参数（non-type，如整数、指针、`auto` 值）与模板模板参数（template template，参数本身是模板）。
- **模板实参（template arguments）**：显式提供，或对函数模板（C++17 起含类模板）由实参推导得出。
- **特化（specialization）**：实参替换形参后得到的具体类型或具体函数左值。
- **类模板 / 函数模板 / 别名模板（C++11）/ 变量模板（C++14）/ 概念（C++20）**：模板可定义的几种实体。
- **模板化实体（templated entity）**：定义或创建于模板内的实体（如局部类、模板类的非模板成员函数），也被视为模板化。

## 工作机制

- **参数化**：模板由一个或多个模板参数参数化；`template<typename T>` / `template<class T>` 引入类型形参。
- **替换即特化**：当提供模板实参（或可推导时自动推导）后，实参被替换进形参位置，得到该模板的一个特化——一个具体类型或具体函数。
- **编译期生成**：同一模板以不同实参实例化会生成不同的特化实体；模板代码在编译期按需展开。
- **模板化成员**：类模板的非模板成员函数（如 `A<int>::f()`）本身不是函数模板，但仍被视为模板化实体。
- **语法要点**：
  - 类模板：`template<typename T> class Stack { ... };`
  - 函数模板：`template<typename T> T max(T a, T b) { ... }`
  - 默认模板实参、特化、偏特化（C++11 起支持函数模板偏特化相关能力演进）、可变参数模板（variadic templates，C++11）、折叠表达式（C++17）等高级机制均基于此展开。

## 示例或代码

**函数模板**：

```cpp
template<typename T>
T max_value(T a, T b) {
    return (a > b) ? a : b;
}

int main() {
    int m1 = max_value(3, 5);        // T 推导为 int
    double m2 = max_value(2.5, 1.0); // T 推导为 double
    // 显式指定：max_value<double>(3, 2.5)
    return 0;
}
```

**类模板**：

```cpp
template<typename T, int N>   // 类型形参 T + 非类型形参 N
class Buffer {
    T data[N];
public:
    T& at(int i) { return data[i]; }
    constexpr int size() const { return N; }
};

Buffer<int, 64> buf;  // T=int, N=64 的特化
buf.at(0) = 42;
```

**别名模板（C++11）与变量模板（C++14）**：

```cpp
template<typename T>
using Ptr = T*;            // 别名模板：一族类型的别名

template<typename T>
constexpr T pi = T(3.141592653589793);  // 变量模板

Ptr<int> p = nullptr;
double d = pi<double>;
```

**概念（C++20）约束模板参数**：

```cpp
#include <concepts>
template<std::integral T>
T add_one(T x) { return x + 1; }   // 仅接受整型实参
```

## 常见误区

- **把"模板"与"宏"混为一谈**：模板是类型安全的编译期参数化机制，不是文本替换。
- **忘记"实参替换得到特化"**：模板本身不是类型/函数，实参替换后才得到可用的具体实体。
- **在 .cpp 中实现类模板导致链接错误**：类模板的完整定义通常需要放在头文件中，以便实例化点可见。
- **混淆三类模板参数**：类型参数（`typename T`）、非类型参数（`int N`）与模板模板参数（`template<typename> class C`）适用场景不同。
- **忽视函数模板的实参推导**：多数场景实参可自动推导，无需显式指定；无法推导时才显式写出。
- **把模板与泛型运行时多态混淆**：模板是编译期机制（静态多态/泛型），与虚函数的运行时多态不同。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| cpp-template-definition | web-computer-science-cpp-template | 模板定义一族类/函数/别名/变量/概念 |
| cpp-template-parameters | web-computer-science-cpp-template | 模板参数分类型、非类型、模板模板三类；实参替换得特化 |

## 待验证项

无。

## 关联知识

- [[cpp-fundamental-types]] —— C++ 基础类型：模板实例化的基本构成。
- [[cpp-class-and-struct]] —— 类与结构体：类模板实例化出的实体类型。
- [[cpp-enum]] —— 枚举类型。
- [[cpp-union]] —— 联合体。
- [[cpp-pointer]] —— 指针类型。
- [[cpp-keywords]] —— `template`、`typename` 等关键字。
- [[cpp-overview]] —— C++ 语言总览。

## 详细章节

### C++模板

#### 定义

模板是 C++ 中定义以下实体之一的一种实体：

- 一族类（类模板，class template），可以包含嵌套类；
- 一族函数（函数模板，function template），可以是成员函数；
- 一族类型的别名（别名模板，alias template，C++11 起）；
- 一族变量（变量模板，variable template，C++14 起）；
- 一个概念（concept，C++20 起，见约束与概念）。

#### 模板参数与特化

模板由一个或多个模板参数参数化，共有三类：

1. **类型模板参数**（type template parameter）：用 `typename`/`class` 引入，实参是一个类型；
2. **非类型模板参数**（non-type template parameter）：实参是一个编译期常量（整数、指针、引用、`auto` 值等）；
3. **模板模板参数**（template template parameter）：实参本身是一个模板。

当提供了模板实参——或对函数模板（C++17 起还包括类模板）而言，由实参推导得出——实参就被替换进模板参数，从而得到该模板的一个**特化（specialization）**，即一个具体的类型或一个具体的函数左值。

#### 模板化实体

除模板本身外，以下实体也被视为模板化（templated）：

- 定义或创建于模板内 item-declaration 或复合语句中的实体（如局部类、局部/块变量、友元函数）；
- 模板化实体的成员（如类模板的非模板成员函数）；
- 作为模板化实体的枚举的枚举项（enumerator）；
- 出现在模板化实体声明中的 lambda 表达式的闭包类型（C++11 起）。

例如在 `template<typename T> struct A { void f() {} };` 中，`A::f` 不是函数模板，但仍被视为模板化实体。

#### 语法要点

```
template < 形参列表 > 声明
```

- `template` 关键字引入模板声明；
- 形参列表是非空、以逗号分隔的模板参数列表，每项可以是类型参数、非类型参数、模板参数或其中任一种的参数包（parameter pack，C++11 起）；
- 模板实参可显式给出，或对函数模板（及 C++17 起的类模板）由实参推导。

#### 高级机制

在基础模板之上，C++ 还提供：模板实参推导（template argument deduction）、类模板实参推导（CTAD，C++17）、显式全特化（explicit specialization）、偏特化（partial specialization）、依赖名（dependent names）、参数包与折叠表达式（C++11/C++17）、SFINAE、约束与概念（C++20）、requires 表达式（C++20）等。这些机制共同构成 C++ 泛型编程的完整体系。

## 参考

- cppreference — Templates: https://en.cppreference.com/w/cpp/language/templates
- cppreference — Class templates: https://en.cppreference.com/w/cpp/language/class_template
- cppreference — Function templates: https://en.cppreference.com/w/cpp/language/function_template
