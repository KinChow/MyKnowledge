---
aliases:
- cpp-pointers
- cpp-指针
confidentiality: public
domain: computer-science
evidence:
- claim: 指针声明用于声明指针类型或指向成员的指针类型的变量。
  claim_id: cpp-pointer-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-8a6e78baf7e3
    exact: Declares a variable of a pointer or pointer-to-member type.
  targets:
  - evidence_id: evidence-8a6e78baf7e3
    source_id: web-computer-science-cpp-pointer
- claim: 每种指针类型都有一个特殊的空指针值；空指针不指向任何对象或函数，解引用空指针是未定义行为，且所有同类型空指针彼此相等。
  claim_id: cpp-pointer-null
  support: direct
  supporting_quotes:
  - evidence_id: evidence-ce3a391eb822
    exact: Pointers of every type have a special value known as null pointer value
      of that type. A pointer whose value is null does not point to an object or a
      function (the behavior of dereferencing a null pointer is undefined), and compares
      equal to all pointers of the same type whose value is also null.
  targets:
  - evidence_id: evidence-ce3a391eb822
    source_id: web-computer-science-cpp-pointer
id: cpp-pointer
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-cpp-pointer
status: published
tags:
- cpp
- pointer
- memory
- type
title: C++指针
updated_at: '2026-09-06'
---
# C++指针

## 一句话结论

指针（pointer）是 C++ 中**保存对象或函数地址的变量**，其声明用于声明指针类型或指向成员的指针类型的变量。C++ 提供指向对象的指针、指向 `void` 的指针（通用"未知类型"传递）、指向函数的指针以及指向成员的指针。每种指针类型都有**空指针值（null pointer value）**：空指针不指向任何对象或函数，**解引用空指针是未定义行为**。现代 C++ 强烈建议用智能指针（`std::unique_ptr`/`std::shared_ptr`）管理动态资源，裸指针仅用于"非拥有"的观察。

## 核心概念

- **指针（pointer）**：保存对象或函数地址的变量；声明形式 `S D;` 中 `D` 为指向 `S` 的指针。
- **指向对象的指针**：保存对象地址，可解引用（`*p`）或 `->` 访问成员，支持指针算术。
- **指向 `void` 的指针**：`void*` 用于传递未知类型的对象（C 接口常见），使用前必须由调用者转回正确类型。
- **指向函数的指针**：保存函数地址，可调用（`(*pf)(args)` / `pf(args)`）。
- **指向成员的指针**：指向数据成员或成员函数的指针（非对象地址）。
- **空指针（null pointer）**：每种指针类型特有的特殊值；不指向对象/函数，解引用是 UB。
- **空指针常量**：值为 0 的整型字面量，或（C++11 起）`std::nullptr_t` 纯右值（通常为 `nullptr`）；宏 `NULL` 是实现定义的空指针常量。
- **悬垂/失效指针（dangling/invalid pointers）**：指向已结束生命周期的存储的指针；使用其值受求值上下文约束。
- **constness**：`const T*` 与 `T* const` 表示不同的常性层级。

## 工作机制

- **声明与解引用**：`int x = 5; int* p = &x;` 取地址得指针；`*p` 解引用访问所指对象；`p->member` 访问成员。
- **空指针初始化**：零初始化与值初始化将指针初始化为空值；空指针常量（`nullptr`/`0`/`NULL`）可初始化或赋值空指针。
- **空指针用途**：表示"对象不存在"（如 `std::function::target()` 返回空）、错误指示（如 `dynamic_cast` 失败）；接收指针参数的函数通常需检查空值并区别处理（如 `delete` 对空指针不做事）。
- **指针与数组**：数组名可隐式退化为首元素指针；指针算术 `p + i` 按元素大小步进。
- **指向 void**：`void*` 不能解引用/算术，需先转型；`std::malloc` 返回 `void*`，`std::qsort`/`pthread_create` 期望回调接收 `const void*`。
- **智能指针（现代 C++）**：`std::unique_ptr`（独占所有权）、`std::shared_ptr`（共享所有权）、`std::weak_ptr`（弱引用）在析构时自动释放，避免裸指针的资源泄漏。

## 示例或代码

**声明、取址、解引用与空指针**：

```cpp
#include <iostream>

int main() {
    int x = 42;
    int* p = &x;            // 声明指向 int 的指针，取 x 的地址
    std::cout << *p << '\n'; // 解引用：输出 42
    *p = 10;                 // 通过指针写对象
    std::cout << x << '\n';  // 10

    int* q = nullptr;        // 空指针（C++11）
    if (q == nullptr) { /* 空指针不指向任何对象 */ }
    // int v = *q;          // 解引用空指针 —— 未定义行为，禁止

    int** pp = &p;           // 指向指针的指针
    return 0;
}
```

**指针与数组 / 指针算术**：

```cpp
int arr[3] = {1, 2, 3};
int* pa = arr;              // 数组退化为首元素指针
for (int i = 0; i < 3; ++i) {
    std::cout << *(pa + i) << ' ';  // pa[i] 等价
}
```

**指向 void（C 接口惯用法）**：

```cpp
void* buf = std::malloc(64);   // malloc 返回 void*
int* ibuf = static_cast<int*>(buf);  // 调用者负责转回正确类型
std::free(ibuf);
```

**指向函数的指针**：

```cpp
int add(int a, int b) { return a + b; }
int (*pf)(int, int) = &add;   // 也可直接写 add（函数到指针隐式转换）
int r = pf(2, 3);             // 通过指针调用
```

**智能指针（推荐）**：

```cpp
#include <memory>
std::unique_ptr<int> up = std::make_unique<int>(7);  // 独占所有权
std::shared_ptr<int> sp = std::make_shared<int>(8);  // 共享所有权
// 作用域结束自动释放，无需手动 delete
```

## 常见误区

- **解引用空指针**：未定义行为，最常见的崩溃来源之一；使用前先判空。
- **解引用悬垂指针**：指向已释放/已结束生命周期的对象的指针是悬垂的，使用是 UB（如函数返回局部变量地址）。
- **混淆 `const T*` 与 `T* const`**：前者"指向常量的指针"（所指对象不可改），后者"常量指针"（指针本身不可改）。
- **忘记 `void*` 不能解引用/算术**：`void*` 必须先转型为具体类型指针才能使用。
- **用裸指针管理动态内存导致泄漏/双重释放**：现代 C++ 用 `std::unique_ptr`/`std::shared_ptr` 管理所有权；裸指针只做非拥有观察。
- **混淆数组与指针**：数组名会退化为指针，但数组不是指针；`sizeof(arr)` 是数组大小而非指针大小。
- **把 `NULL` 当 `nullptr` 用**：`NULL` 是实现定义的空指针常量（可能为 0L），有歧义风险；C++11 起优先用 `nullptr`。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| cpp-pointer-definition | web-computer-science-cpp-pointer | 指针声明声明指针或指向成员的指针类型的变量 |
| cpp-pointer-null | web-computer-science-cpp-pointer | 每种指针类型都有空指针值；空指针不指向对象/函数，解引用是 UB，同类型空指针彼此相等 |

## 待验证项

无。

## 关联知识

- [[cpp-fundamental-types]] —— C++ 基础类型：`void`、`nullptr_t` 与指针的关系。
- [[cpp-class-and-struct]] —— 类与结构体：`this` 指针、对象指针。
- [[cpp-union]] —— 联合体。
- [[cpp-enum]] —— 枚举类型。
- [[cpp-template]] —— 模板：`T*`、智能指针的模板实现。
- [[cpp-keywords]] —— `nullptr`、`void`、`new`、`delete` 等关键字。
- [[cpp-class-and-raii]] —— RAII：智能指针的资源管理思想。
- [[cpp-overview]] —— C++ 语言总览。

## 详细章节

### C++指针

#### 定义与语法

指针声明用于声明一个指针类型或指向成员的指针类型的变量。指针声明是任何简单声明，其声明符（declarator）具有如下形式：

```
* attr(可选) cv(可选) declarator          (1)
```

指针声明符：声明 `S D;` 将 `D` 声明为指向声明说明符序列 `S` 所确定类型的指针。

#### 指向对象的指针

指向对象的指针保存对象的地址，可解引用访问所指对象，支持指向数组元素的指针算术（按元素大小步进）。

#### 指向 void 的指针

`void*` 用于传递未知类型的对象，这在 C 接口中很常见：`std::malloc` 返回 `void*`；`std::qsort` 期望用户提供的、接受两个 `const void` 实参的回调；`pthread_create` 期望接受并返回 `void*` 的用户回调。在所有情况下，由调用者负责在使用前把指针转回正确的类型。

#### 指向函数的指针

指向函数的指针可以用非成员函数或静态成员函数的地址初始化。由于函数到指针的隐式转换，取址运算符是可选的：

```cpp
void f(int);
void (*p1)(int) = &f;
void (*p2)(int) = f;   // 与 &f 相同
```

#### 空指针

每种类型的指针都有一个特殊值，即该类型的空指针值（null pointer value）。值为空的指针不指向任何对象或函数（解引用空指针是未定义行为），并且与该类型所有同样为空的指针相等。

空指针常量（null pointer constant）可用来把指针初始化为空，或把空值赋给已有指针，它可以是：

- 值为零的整型字面量；
- `std::nullptr_t` 类型的纯右值（通常为 `nullptr`，C++11 起）。

宏 `NULL` 也可使用，它展开为实现定义的空指针常量。

空指针可用于表示对象不存在（如 `std::function::target()`），或作为其他错误条件指示（如 `dynamic_cast`）。通常，接收指针参数的函数几乎总需要检查该值是否为空并区别处理（例如，`delete` 表达式在传入空指针时不执行任何操作）。

零初始化和值初始化也会把指针初始化为其空值。

#### 失效指针

指针值 `p` 在求值上下文 `e` 中有效（valid）当且仅当满足下列条件之一：

- `p` 是空指针值；
- `p` 是指向函数的指针；
- `p` 是指向对象 `o` 的指针或指向对象 `o` 末尾之后的指针，且 `e` 处于 `o` 的存储区域的持续期内。

#### constness

`const`/`volatile`（cv 限定）可施加于指针所指类型或指针自身：`const T* p`（指向 const 的指针，所指不可改）与 `T* const p`（const 指针，指针本身不可改）语义不同。

#### 现代 C++ 实践

裸指针只承担"非拥有观察"职责；动态资源的所有权用 `std::unique_ptr`（独占）、`std::shared_ptr`（共享）、`std::weak_ptr`（弱引用）管理，从而避免泄漏与双重释放。需要"可选"引用语义时也常用指针判空表示不存在。

## 参考

- cppreference — Pointers: https://en.cppreference.com/w/cpp/language/pointer
- cppreference — nullptr (keyword): https://en.cppreference.com/w/cpp/keyword/nullptr
- cppreference — Smart pointers: https://en.cppreference.com/w/cpp/memory
