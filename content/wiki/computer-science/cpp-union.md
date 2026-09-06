---
aliases:
- cpp-union
- cpp-联合体
confidentiality: public
domain: computer-science
evidence:
- claim: 联合体（union）是一种特殊的类类型，同一时刻只能持有它的一个非静态数据成员。
  claim_id: cpp-union-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-299f8a4a797c
    exact: A union is a special class type that can hold only one of its non-static
      data members at a time.
  targets:
  - evidence_id: evidence-299f8a4a797c
    source_id: web-computer-science-cpp-union
- claim: 读取联合体最近未被写入的成员是未定义行为。
  claim_id: cpp-union-layout-ub
  support: direct
  supporting_quotes:
  - evidence_id: evidence-33493e72bb98
    exact: It is undefined behavior to read from the member of the union that wasn't
      most recently written.
  targets:
  - evidence_id: evidence-33493e72bb98
    source_id: web-computer-science-cpp-union
id: cpp-union
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-cpp-union
status: published
tags:
- cpp
- union
- type
- memory-layout
title: C++联合体
updated_at: '2026-09-06'
---
# C++联合体

## 一句话结论

联合体（union）是 C++ 中一种**特殊的类类型**：它在同一时刻只能持有它的一个非静态数据成员。所有非静态数据成员共享同一块存储（同一地址），union 的大小至少足以容纳其最大的数据成员。它常用于省内存的类型复用（如解析协议、类型擦除），但**读取最近未被写入的成员是未定义行为**——现代 C++ 推荐用 `std::variant` 替代裸 union 管理"哪个成员活跃"。

## 核心概念

- **union 的定义**：特殊的类类型，同一时刻只能持有一个非静态数据成员。
- **存储共享**：所有非静态数据成员具有相同地址；union 大小至少足以容纳最大的数据成员。
- **活跃成员（active member）**：最近一次被写入/构造的成员；只有活跃成员可以被读取。
- **UB 边界**：读取最近未被写入的成员是未定义行为（许多编译器以非标准扩展允许"类型双关/type punning"）。
- **语法**：`union name { members };`，声明方式与 class/struct 类似。
- **限制**：union 可以有成员函数（含构造函数、析构函数），但不能有虚函数；不能有基类，也不能作为基类。
- **匿名联合体（anonymous union）**：未命名且不同时定义任何变量的联合体，其成员可直接在当前作用域访问。

## 工作机制

- **内存布局**：union 至少与最大数据成员一样大（通常不会更大）；各非静态数据成员被分配在最大成员所占的相同字节中。分配细节由实现定义，但所有非静态数据成员地址相同。
- **活跃成员切换**：成员的生命周期从该成员被置为活跃时开始；此前若其他成员活跃，其生命周期随之结束。对具有用户自定义构造/析构函数的类成员，切换活跃成员通常需要显式析构 + placement new。
- **平凡特殊成员函数**：union 类型的平凡移动构造/移动赋值/拷贝构造/拷贝赋值会拷贝对象表示（object representation）；拷贝前会启动目标中与源对应的嵌套成员的生命周期。
- **标准布局公共子序列**：若两个 union 成员都是标准布局类型，在任意编译器上检查它们的公共子序列（common subsequence）是良定义的（C++ 常见子序列保证）。
- **type punning**：通过 union 重新解释字节（读非活跃成员）在标准 C++ 中属于 UB，但很多编译器作为非标准扩展支持。

## 示例或代码

**基本用法**：

```cpp
#include <cstdint>
#include <iostream>

union Value {
    std::uint32_t u;
    float f;
    std::uint16_t h[2];
};

int main() {
    Value v;
    v.f = 1.0f;             // 写入 f，f 成为活跃成员
    std::cout << v.u << '\n'; // 读取非活跃成员 u —— 标准中是 UB（type punning）
    return 0;
}
```

**带类类型成员的 union**：切换活跃成员需要显式析构 + placement new：

```cpp
#include <string>
#include <new>

struct S { std::string s; };

union U {
    int i;
    S s;
    U() : i(0) {}
    ~U() {}                    // 需要手工管理 std::string 的生命周期
};

// 切换到 s 活跃：u.s.~S(); new (&u.s) S("hello");
```

**匿名联合体**：

```cpp
struct Widget {
    union {                    // 匿名联合体：成员直接可访问
        int x;
        float y;
    };
};
// w.x 与 w.y 共享同一地址
```

**建议**：现代 C++ 中用 `std::variant` 管理"当前活跃成员"更安全（自动跟踪并处理析构/移动）。

## 常见误区

- **认为可以任意读取 union 的任何成员**：读取最近未被写入的成员是未定义行为（除非用编译器扩展做 type punning）。
- **忽略类类型成员的生命周期管理**：union 含 `std::string` 等成员时，切换活跃成员需要显式析构 + placement new，否则泄漏或 UB。
- **把 union 当"节省所有类型的存储"的通用工具**：它只节省"不同时使用"的成员的空间；使用前必须明确哪个成员活跃。
- **试图给 union 加虚函数或基类**：union 不能有虚函数，不能有基类也不能作为基类。
- **混淆 union 与 struct**：struct 的所有成员同时存在且独立地址；union 的成员互斥共享同一地址。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| cpp-union-definition | web-computer-science-cpp-union | union 是同一时刻只能持有一个非静态数据成员的特殊类类型 |
| cpp-union-layout-ub | web-computer-science-cpp-union | 读取最近未被写入的成员是未定义行为 |

## 待验证项

无。

## 关联知识

- [[cpp-class-and-struct]] —— 类与结构体：union 是 class-key 之一，与 class/struct 并列。
- [[cpp-fundamental-types]] —— C++ 基础类型。
- [[cpp-pointer]] —— 指针：`new`/placement new 用于切换 union 活跃成员。
- [[cpp-enum]] —— 枚举类型。
- [[cpp-template]] —— 模板。
- [[cpp-keywords]] —— `union` 关键字。
- [[cpp-overview]] —— C++ 语言总览。

## 详细章节

### C++联合体

#### 定义

union 是一种特殊的类类型（special class type），同一时刻只能持有它的一个非静态数据成员（non-static data member）。

#### 语法

union 声明的类说明符（class specifier）与 class 或 struct 声明类似：

```
union attr(可选) class-head-name(可选) { member-specification }
```

- `class-head-name`：被定义的 union 的名称，可选地以嵌套名说明符（nested-name-specifier）开头；名称可以省略，此时 union 未命名（anonymous union）。
- `member-specification`：访问说明符、成员对象与成员函数声明/定义的列表。
- union 可以有成员函数（包括构造函数与析构函数），但不能有虚函数。
- union 不能有基类，也不能被用作基类。
- 至多一个变体成员（variant member）可以有默认成员初始化器（default member initializer，C++11 起）。

#### 存储布局

union 至少与容纳其最大数据成员所需的空间一样大（通常不会更大）。其他数据成员被有意分配在最大成员所占的相同字节内。分配的细节是实现定义的，但所有非静态数据成员具有相同的地址。每个成员都如同它是该类的唯一成员一样被分配。

#### 活跃成员与 UB

union 在任意时刻至多持有一个非静态数据成员的值；当前"活跃"的成员是最近一次被写入的成员。**读取最近未被写入（非活跃）的成员是未定义行为**。许多编译器以非标准语言扩展的形式实现了读取非活跃成员（type punning）的能力，但依赖它移植性差。

#### 成员生命周期

union 成员的生命周期在该成员被置为活跃时开始；若之前有其他成员活跃，其生命周期随之结束。当 union 的成员是具有用户自定义构造/析构函数的类时，切换活跃成员通常需要显式析构函数调用与 placement new。

union 类型的平凡移动构造、移动赋值（C++11 起）、拷贝构造与拷贝赋值运算符会拷贝对象表示；若源与目标不是同一对象，这些特殊成员函数会在拷贝前启动目标中与源中对应成员的嵌套成员的生命周期。否则它们不做任何事。经由平凡特殊函数构造/赋值后，两个 union 对象具有相同的对应活跃成员（如果有）。

若两个 union 成员是标准布局（standard-layout）类型，那么在任意编译器上检查它们的公共子序列（common subsequence）都是良定义的。

#### 匿名联合体

匿名联合体（anonymous union）是未命名且未同时定义任何变量（包括 union 类型对象、引用或指向 union 的指针）的 union 定义。其成员可以在外围作用域中直接访问。

#### 实践建议

- 只在"同一时刻最多使用一个成员"的场景使用 union（协议解析、紧凑变体、类型擦除）。
- 优先使用 `std::variant` 管理活跃成员与销毁，避免手写析构/placement new 的出错风险。
- 若必须做 type punning，优先使用 `std::memcpy` 或明确记录编译器扩展行为，避免依赖 UB。

## 参考

- cppreference — union declaration: https://en.cppreference.com/w/cpp/language/union
- cppreference — std::variant: https://en.cppreference.com/w/cpp/utility/variant
