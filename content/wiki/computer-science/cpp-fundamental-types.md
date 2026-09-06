---
aliases:
- cpp-fundamental-types
- cpp-basic-types
- cpp-基础类型
confidentiality: public
domain: computer-science
evidence:
- claim: 以下类型统称为基础类型（fundamental types）：（可有 cv 限定的）void、std::nullptr_t（C++11）、整型类型与浮点类型。
  claim_id: cpp-fundamental-types-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-d2dd17001b46
    exact: 'The following types are collectively called fundamental types: (possibly
      cv-qualified) void; std::nullptr_t (since C++11); integral types; floating-point
      types.'
  targets:
  - evidence_id: evidence-d2dd17001b46
    source_id: web-computer-science-cpp-fundamental-types
- claim: 除最小位宽外，C++ 标准保证 1 == sizeof(char) <= sizeof(short) <= sizeof(int) <= sizeof(long)
    <= sizeof(long long)。
  claim_id: cpp-fundamental-types-size-guarantee
  support: direct
  supporting_quotes:
  - evidence_id: evidence-760eedda3335
    exact: Besides the minimal bit counts, the C++ Standard guarantees that 1 == sizeof(char)
      <= sizeof(short) <= sizeof(int) <= sizeof(long) <= sizeof(long long).
  targets:
  - evidence_id: evidence-760eedda3335
    source_id: web-computer-science-cpp-fundamental-types
id: cpp-fundamental-types
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-cpp-fundamental-types
status: published
tags:
- cpp
- fundamental-types
- type-system
- memory
title: C++基础类型
updated_at: '2026-09-06'
---
# C++基础类型

## 一句话结论

C++ 的**基础类型（fundamental types）**是语言内建的、不基于其他类型构造的类型，包括：（可有 cv 限定的）`void`、`std::nullptr_t`（C++11）、整型类型（`bool`、`char`、`wchar_t`、`char8_t`/`char16_t`/`char32_t`、带符号/无符号整数类型）与浮点类型（`float`/`double`/`long double`）。C++ 只保证 `1 == sizeof(char) <= sizeof(short) <= sizeof(int) <= sizeof(long) <= sizeof(long long)` 等最小关系，而**不保证**各类型在平台上的确切字节数——精确大小需用 `sizeof`/`<cstdint>` 的定宽类型确认。

## 核心概念

- **基础类型集合**：`void`、`std::nullptr_t`、整型类型、浮点类型（可有 cv 限定）。
- **`void`**：值为空集的类型，不完整且无法补全；禁止 `void` 对象/数组/引用，但允许 `void*` 与返回 `void` 的函数。
- **`std::nullptr_t`**：空指针字面量 `nullptr` 的类型；独立类型，本身不是指针或指向成员的指针；`sizeof(std::nullptr_t) == sizeof(void*)`。
- **整型类型**：`bool`、字符类型（`char`、`wchar_t`、`char8_t`/`char16_t`/`char32_t`）、带符号整数（`signed char`、`short`、`int`、`long`、`long long`）、无符号整数（`unsigned char`、`unsigned short`、`unsigned int`、`unsigned long`、`unsigned long long`）。
- **浮点类型**：`float`、`double`、`long double`。
- **大小保证**：`1 == sizeof(char) <= sizeof(short) <= sizeof(int) <= sizeof(long) <= sizeof(long long)`；`int` 至少 16 位宽，在 32/64 位系统上几乎总是至少 32 位。
- **cv 限定**：`const`/`volatile` 可限定基础类型（如 `const int`）。

## 工作机制

- **对象类型与表示**：基础类型是内建对象类型；其存储大小以 `sizeof` 度量，`sizeof(char) == 1`（一个 char 的大小 = 一个"字节"，可能是 8 位以上）。
- **整型修饰符**：`short`/`long`/`long long` 控制长度，`signed`/`unsigned` 控制符号；`int` 在出现修饰符时可省略。
- **字符类型**：`char` 的符号性由实现定义；`wchar_t` 宽度实现定义；`char8_t`（C++20）/`char16_t`/`char32_t`（C++11）分别是 UTF-8/16/32 码元类型，与对应 `unsigned char`/`uint_least16_t`/`uint_least32_t` 同大小、符号与对齐，但是不同类型。
- **最小位宽保证**：`int` 无长度修饰符时保证至少 16 位，32/64 位系统几乎总为至少 32 位。
- **定宽类型**：需要精确大小用 `<cstdint>` 的 `int8_t`/`int32_t`/`uint64_t` 等，避免依赖平台相关的默认大小。
- **语法要点**：见下方大小表与代码示例。

### 基础类型大小参考表（常见 64 位平台，非标准保证）

| 类型 | 常见大小 | 备注 |
| --- | --- | --- |
| `bool` | 1 字节 | 存 `true`/`false` |
| `char` / `signed char` / `unsigned char` | 1 字节 | `sizeof(char) == 1` 由标准保证 |
| `short` / `unsigned short` | 通常 2 字节 | 至少 16 位 |
| `int` / `unsigned int` | 通常 4 字节 | 至少 16 位；常见 32 位 |
| `long` / `unsigned long` | Windows 4 字节 / Linux 8 字节 | 平台相关，勿假设 |
| `long long` / `unsigned long long` | 通常 8 字节 | 至少 64 位 |
| `float` | 通常 4 字节 | IEEE-754 单精度 |
| `double` | 通常 8 字节 | IEEE-754 双精度 |
| `long double` | 平台相关（x86 常 16 字节） | 实现定义 |
| `wchar_t` | 平台相关 | Windows 2 字节 / Linux 4 字节 |
| `char16_t` / `char32_t` | 2 / 4 字节 | UTF-16/32 码元 |
| `char8_t` | 1 字节 | UTF-8 码元（C++20） |
| `void*` / `nullptr_t` | 通常 8 字节（64 位） | `sizeof(nullptr_t) == sizeof(void*)` |

## 示例或代码

**基础类型声明与 sizeof**：

```cpp
#include <cstdint>
#include <iostream>

int main() {
    bool b = true;
    char c = 'A';
    int i = 42;
    long l = 42L;
    long long ll = 42LL;
    unsigned int ui = 42u;
    float f = 3.14f;
    double d = 3.14;
    long double ld = 3.14L;

    std::cout << sizeof(char) << sizeof(short) << sizeof(int)
              << sizeof(long) << sizeof(long long) << '\n';  // 满足 1<=... 链

    std::int32_t fixed = 100;        // <cstdint> 定宽类型：保证 32 位
    std::uint64_t u64 = 100ULL;      // 保证 64 位
    return 0;
}
```

**void 与 nullptr_t**：

```cpp
#include <cstddef>

void f();                // 返回 void 的函数
void* p = nullptr;       // void* 可指向未知类型；不能解引用
std::nullptr_t n = nullptr;  // nullptr 的类型
// 静态断言：sizeof(nullptr_t) == sizeof(void*)
static_assert(sizeof(std::nullptr_t) == sizeof(void*));
```

**字符与宽字符**：

```cpp
char16_t u16 = u'A';     // UTF-16 码元（C++11）
char32_t u32 = U'A';     // UTF-32 码元（C++11）
char8_t u8  = u8'A';     // UTF-8 码元（C++20）
wchar_t w   = L'A';      // 宽字符，宽度实现定义
```

**整型修饰符与 int 省略**：

```cpp
unsigned x = 42;    // unsigned int
long y = 42L;       // long int
unsigned long long z = 42ULL;  // 组合修饰符
```

## 常见误区

- **假设 `int` 一定 4 字节 / `long` 一定 8 字节**：C++ 只保证大小关系，不保证绝对字节数；跨平台需用 `<cstdint>` 定宽类型。
- **把 `char` 当 8 位定宽类型**：`char` 的位宽是实现定义（通常 8 位），`sizeof(char) == 1` 但 1 字节可以是 64 位。
- **混淆 `char` 的符号性**：`char` 的 `signed`/`unsigned` 是实现定义的；需要确定符号用 `signed char`/`unsigned char`。
- **对 `void` 做对象/引用/数组**：`void` 是不完整类型，不能有 `void` 对象、引用或数组，只能有 `void*` 或返回 `void`。
- **假设 `wchar_t`/`long double` 平台无关**：它们的宽度/表示是平台相关的。
- **忽略整型提升与溢出**：运算中小整型会提升，未定义溢出（有符号）——与类型大小一起理解。
- **把 `nullptr_t` 当指针类型**：它是独立类型，不是指针，只是其纯右值都是空指针常量。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| cpp-fundamental-types-definition | web-computer-science-cpp-fundamental-types | 基础类型 = void、nullptr_t、整型、浮点（可有 cv 限定） |
| cpp-fundamental-types-size-guarantee | web-computer-science-cpp-fundamental-types | 标准保证 sizeof(char) <= sizeof(short) <= sizeof(int) <= sizeof(long) <= sizeof(long long) |

## 待验证项

无。

## 关联知识

- [[cpp-pointer]] —— 指针：`void*`、`nullptr_t` 与指针的关系。
- [[cpp-class-and-struct]] —— 类与结构体：用户自定义类型基于基础类型构造。
- [[cpp-enum]] —— 枚举：底层类型为整型类型。
- [[cpp-union]] —— 联合体。
- [[cpp-template]] —— 模板：`<cstdint>`、类型工具基于基础类型。
- [[cpp-keywords]] —— `void`、`char`、`int`、`float`、`bool`、`unsigned` 等关键字。
- [[cpp-overview]] —— C++ 语言总览。
- [[cpp-vs-c]] —— C 与 C++ 类型系统差异。

## 详细章节

### C++基础类型

#### 定义

以下类型统称为基础类型（fundamental types）：

- （可有 cv 限定的）`void`；
- `std::nullptr_t`（C++11 起）；
- 整型类型（integral types）；
- 浮点类型（floating-point types）。

（类型系统的总览见 type 页面，C++ 标准库提供的类型相关工具见 type utilities 列表。）

#### void

`void` 是值为空集的类型。它是一个无法补全的不完整类型（因此禁止 `void` 对象）。没有 `void` 数组，也没有 `void` 引用。然而，允许指向 `void` 的指针，也允许返回类型为 `void` 的函数（其他语言中的"过程"）。

#### std::nullptr_t

`std::nullptr_t` 命名空指针字面量 `nullptr` 的类型。它是一个独立类型，本身不是指针类型，也不是指向成员的指针类型。它的所有纯右值都是空指针常量。`sizeof(std::nullptr_t)` 等于 `sizeof(void*)`。名字 `std::nullptr_t` 声明于 `<cstddef>`（C++11 起）。

#### 整型类型

##### 标准整型

`int` 是基本整型。若使用了下列任一修饰符，`int` 关键字可以省略。若不存在长度修饰符，保证其宽度至少为 16 位；不过在 32/64 位系统上，几乎总是保证宽度至少为 32 位。

修饰符：

- **符号性（Signedness）**：`signed` / `unsigned`；
- **长度（length）**：`short`、`long`、`long long`。

`bool` 表示布尔值（`true`/`false`）。

字符类型：

- `char` —— 基本的字符类型；
- `wchar_t` —— 宽字符类型（宽度实现定义）；
- `char8_t` —— UTF-8 字符表示类型（C++20），要求足以表示任意 UTF-8 码元（8 位）；与 `unsigned char` 有相同大小、符号与对齐（因此与 `char`、`signed char` 也同大小同对齐），但是独立类型；
- `char16_t` —— UTF-16 字符表示类型（C++11），要求足以表示任意 UTF-16 码元（16 位）；与 `std::uint_least16_t` 同大小、符号与对齐，但是独立类型；
- `char32_t` —— UTF-32 字符表示类型（C++11），要求足以表示任意 UTF-32 码元（32 位）；与 `std::uint_least32_t` 同大小、符号与对齐，但是独立类型。

##### 大小保证

除最小位宽外，C++ 标准还保证：

```
1 == sizeof(char) <= sizeof(short) <= sizeof(int) <= sizeof(long) <= sizeof(long long)
```

注意：这允许极端情形——字节（byte）为 64 位、所有类型（包括 `char`）都是 64 位宽、`sizeof` 对每种类型都返回 1。

#### 浮点类型

标准浮点类型包括 `float`、`double` 与 `long double`。它们的表示（如 IEEE-754）由实现定义，`long double` 的精度与大小也依赖平台。

#### 实践建议

- 需要精确、可移植的固定宽度整型时使用 `<cstdint>` 中的 `int8_t`/`uint32_t`/`int64_t` 等。
- 表示字符序列时优先 `char`（或 C++20 的 `char8_t` + UTF-8 字符串），避免 `wchar_t` 的平台差异。
- 用 `sizeof`/`std::numeric_limits` 获取实际大小与范围，而不是依赖常识假设。

## 参考

- cppreference — Fundamental types: https://en.cppreference.com/w/cpp/language/types
- cppreference — Type: https://en.cppreference.com/w/cpp/language/type
- cppreference — std::numeric_limits: https://en.cppreference.com/w/cpp/types/numeric_limits
