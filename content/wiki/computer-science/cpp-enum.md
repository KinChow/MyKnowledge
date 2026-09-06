---
aliases:
- cpp-enum
- cpp-枚举
confidentiality: public
domain: computer-science
evidence:
- claim: 枚举（enumeration）是一种独立类型，其值被限制在一个取值范围（range of values）内，可包含若干显式命名的常量（枚举项 enumerator）。
  claim_id: cpp-enum-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-a9c5a0247695
    exact: An enumeration is a distinct type whose value is restricted to a range
      of values (see below for details), which may include several explicitly named
      constants ("enumerators").
  targets:
  - evidence_id: evidence-a9c5a0247695
    source_id: web-computer-science-cpp-enum
- claim: 枚举分两类：无作用域枚举（enum-key 为 enum）与有作用域枚举（enum-key 为 enum class 或 enum struct）。
  claim_id: cpp-enum-kinds
  support: direct
  supporting_quotes:
  - evidence_id: evidence-19853330e477
    exact: 'There are two distinct kinds of enumerations: unscoped enumeration (declared
      with the enum-key enum) and scoped enumeration (declared with the enum-key enum
      class or enum struct).'
  targets:
  - evidence_id: evidence-19853330e477
    source_id: web-computer-science-cpp-enum
id: cpp-enum
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-cpp-enum
status: published
tags:
- cpp
- enum
- type
title: C++枚举
updated_at: '2026-09-06'
---
# C++枚举

## 一句话结论

枚举（enumeration）是 C++ 中一种**独立（distinct）类型**：它的值被限制在一个取值范围内，可包含若干显式命名的常量（称为枚举项 enumerator）。C++ 提供两类枚举：**无作用域枚举**（`enum`）与**有作用域枚举**（`enum class` / `enum struct`，C++11）。每个枚举项对应底层整型（underlying type）的一个值，枚举与底层类型具有相同的大小、值表示与对齐要求。

## 核心概念

- **枚举（enumeration）**：独立类型，值限制在一定范围，可含多个命名常量（枚举项）。
- **枚举项（enumerator）**：枚举中的命名常量，是底层整型类型的一个值。
- **底层类型（underlying type）**：枚举项的值的整型类型；枚举与其底层类型有相同大小、值表示和对齐。
- **无作用域枚举**：`enum`，枚举项泄漏到外层作用域。
- **有作用域枚举**：`enum class` / `enum struct`（两关键字完全等价），枚举项在枚举作用域内，不泄漏；不会隐式转换为其底层整型。
- **固定底层类型（C++11）**：`enum name : type { ... }` 可显式指定底层类型；无作用域枚举也可前向声明（opaque enum declaration）。
- **值规则**：未显式赋值时，第一个枚举项值为 0，其余为前一个枚举项的值加 1；可显式用 `= constant-expression` 指定。

## 工作机制

- **取值与表示**：枚举项是底层整型类型的值；每个枚举值与其底层类型的对应值具有相同表示。
- **无作用域枚举**：枚举项可见于其声明所在的外层作用域；可隐式转换为整型。
- **有作用域枚举（enum class）**：默认底层类型为 `int`；枚举项只在枚举作用域内可见；**不隐式转换**为整型（需要显式 `static_cast`），消除名称污染与隐式转换 bug。
- **值递增规则**：第一个无 `=` 的枚举项值为 0；其后无 `=` 的枚举项值为前一项值 +1。
- **固定底层类型**：`enum class Color : std::uint8_t { ... }` 控制大小与取值范围；无作用域枚举用 `enum name : type { ... }` 指定。
- **语法要点**：
  - `enum name { enumerator = constant-expression, ... }`
  - `enum name : type { ... }`（C++11）
  - `enum class|struct name : type { ... }`（C++11）

## 示例或代码

**无作用域枚举**：

```cpp
enum Color { Red, Green = 5, Blue };  // Red=0, Green=5, Blue=6
Color c = Red;
int n = c;             // 无作用域枚举可隐式转 int
```

**有作用域枚举（enum class）**：

```cpp
enum class Status : std::uint8_t {  // 固定底层类型，占 1 字节
    Ok = 0,
    Busy = 1,
    Error = 2,
};

Status s = Status::Ok;
// int n = s;             // 编译错误：不隐式转换为整型
auto code = static_cast<std::uint8_t>(s);  // 需显式转换
```

**前向声明 / opaque 枚举（C++11）**：

```cpp
enum class Direction : int;   // 前向声明（底层类型必须已知）
enum class Direction { North, South, East, West };  // 定义
```

**切换 switch**：

```cpp
enum class Level { Low, Mid, High };
Level l = Level::Mid;
switch (l) {
    case Level::Low:  /* ... */ break;
    case Level::Mid:  /* ... */ break;
    case Level::High: /* ... */ break;
}
```

## 常见误区

- **用 `enum class` 却期望隐式转 int**：有作用域枚举不隐式转换，需 `static_cast`——这正是它比 `enum` 安全的原因。
- **混淆两类枚举的作用域**：`enum` 的枚举项泄漏到外层作用域，易冲突；`enum class` 不会。
- **忽略固定底层类型**：不指定时，无作用域枚举的底层类型是实现定义的（通常为 `int`）；跨平台/序列化时建议显式指定。
- **假设枚举项一定连续/从 0 开始**：显式赋值会打乱递增规则；第一个无 `=` 项才是 0。
- **依赖枚举项在内存中的确切布局**：枚举大小与表示由底层类型决定，不要假设其等价于某个特定整型，除非显式指定。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| cpp-enum-definition | web-computer-science-cpp-enum | 枚举是值受限的独立类型，可含多个命名常量（枚举项） |
| cpp-enum-kinds | web-computer-science-cpp-enum | 分无作用域（enum）与有作用域（enum class/enum struct）两类 |

## 待验证项

无。

## 关联知识

- [[cpp-fundamental-types]] —— C++ 基础类型：枚举的底层整型类型。
- [[cpp-class-and-struct]] —— 类与结构体：枚举可与类一起定义成员。
- [[cpp-union]] —— 联合体。
- [[cpp-template]] —— 模板：`is_enum`、`underlying_type` 等类型工具。
- [[cpp-pointer]] —— 指针类型。
- [[cpp-keywords]] —— `enum`、`enum class` 关键字。
- [[cpp-overview]] —— C++ 语言总览。

## 详细章节

### C++枚举

#### 定义

枚举（enumeration）是一种独立类型，其值被限制在一个取值范围内，可包含若干显式命名的常量（"枚举项" enumerator）。

枚举项的常量值是底层类型（underlying type）这一整型类型的值。枚举与其底层类型具有相同的大小、值表示（value representation）与对齐要求（alignment requirements）。此外，枚举的每个值与其底层类型的对应值具有相同的表示。

#### 两类枚举

C++ 存在两类截然不同的枚举：

- **无作用域枚举（unscoped enumeration）**：用 enum-key `enum` 声明；
- **有作用域枚举（scoped enumeration）**：用 enum-key `enum class` 或 `enum struct` 声明（`class` 与 `struct` 关键字完全等价）。

#### 语法

无作用域枚举：

```
enum name(可选) { enumerator = constant-expression, ... }        (1)
enum name(可选) : type { enumerator = constant-expression, ... }  (2)  (C++11)
enum name : type ;                                                (3)  (C++11)
```

有作用域枚举：

```
enum struct|class name { enumerator = constant-expression, ... }            (1)
enum struct|class name : type { enumerator = constant-expression, ... }     (2)
enum struct|class name ;                                                    (3)
enum struct|class name : type ;                                             (4)
```

- (1) 声明一个有作用域枚举类型，其底层类型为 `int`；
- (2) 声明一个有作用域枚举类型，其底层类型为 `type`；
- (3) 有作用域枚举的 opaque 声明；
- (4) 有作用域枚举并指定底层类型的 opaque 声明。

#### 枚举项与值规则

每个枚举项都成为该枚举类型的一个命名常量（即可见的名字），在声明所在的作用域可见（无作用域枚举）或在枚举作用域内可见（有作用域枚举），可在需要常量的任何地方使用。

每个枚举项都与底层类型的一个值关联：

- 若枚举项列表中提供了 `= constant-expression`，则该枚举项的值由该常量表达式定义；
- 若第一个枚举项没有 `=`，其关联值为 0；
- 其他未显式 `=` 的枚举项，其关联值为前一个枚举项的值加 1。

#### 实践建议

- 优先使用 `enum class`（有作用域、不隐式转换、无名称污染）。
- 对需要指定大小/跨平台二进制布局的枚举，显式指定底层类型。
- 用 `std::underlying_type` / `std::to_underlying`（C++23）在枚举与底层类型间转换。

## 参考

- cppreference — Enumeration declaration: https://en.cppreference.com/w/cpp/language/enum
- cppreference — `enum` keyword: https://en.cppreference.com/w/cpp/keyword/enum
