---
aliases:
- C++ 视频课程
- C++ 课程大纲
- cpp video course
confidentiality: public
domain: computer-science
evidence:
- claim: C++ 是高级通用编程语言，1985 年作为 C 语言的扩展首次发布并加入面向对象特性，其后不断扩展，并通过模板支持泛型编程。
  claim_id: cpp-course-language
  support: direct
  supporting_quotes:
  - evidence_id: evidence-66af4c868854
    exact: C++ is a high-level, general-purpose programming language created by Danish
      computer scientist Bjarne Stroustrup. First released in 1985 as an extension
      of the C programming language, adding object-oriented (OOP) features, it has
      since expanded significantly over time adding more OOP and other features; as
      of 1997 standardization, C++ has added functional features, in addition to facilities
      for low-level memory manipulation for systems like microcomputers or to make
      operating systems like Linux or Windows, and even later came features like generic
      programming (through the use of templates).
  targets:
  - evidence_id: evidence-66af4c868854
    source_id: web-computer-science-cpp-course
- claim: 标准模板库（STL）是影响 C++ 标准库的软件库，提供算法、容器、函子与迭代器四大组件。
  claim_id: cpp-course-stl
  support: direct
  supporting_quotes:
  - evidence_id: evidence-1f513b7ce17d
    exact: The Standard Template Library (STL) was a software library originally designed
      by Alexander Stepanov for the C++ programming language that influenced many
      parts of the C++ Standard Library, though no longer is actively maintained and
      is now mostly integrated into the C++ standard library itself. It provides four
      components called algorithms, containers, functors, and iterators.
  targets:
  - evidence_id: evidence-1f513b7ce17d
    source_id: web-computer-science-cpp-course
- claim: STL 容器分为顺序容器（vector、deque、list）与关联容器（set、map 等），容器是存储数据的对象。
  claim_id: cpp-course-containers
  support: direct
  supporting_quotes:
  - evidence_id: evidence-a18f9c4f3194
    exact: The STL contains sequence containers and associative containers. The containers
      are objects that store data. The standard sequence containers include vector,
      deque, and list. The standard associative containers are set, multiset, map,
      multimap, hash_set, hash_map, hash_multiset and hash_multimap.
  targets:
  - evidence_id: evidence-a18f9c4f3194
    source_id: web-computer-science-cpp-course
id: cpp-course-video
kind: reference
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-cpp-course
status: published
tags:
- cpp
- course
- outline
- video
title: C++ 视频课程大纲
updated_at: '2026-09-06'
---

# C++ 视频课程大纲

## 课程概览

这是一套从零开始的 C++ 视频课程大纲，共 56 节，覆盖**环境搭建、语法基础、面向对象、模板与泛型、STL 标准库、现代 C++（智能指针/移动语义/Lambda）、并发与多线程、协程、原子操作与内存模型、概念约束**等主题。课程以“每节一个知识点 + 随堂编程练习”的方式推进，适合已有一点编程基础、希望系统学习 C/C++ 的学习者按顺序观看。C++ 本身是 1985 年作为 C 语言扩展发布的高级通用语言（见下方证据），课程内容与之对应地覆盖了从过程式、面向对象到泛型与并发的完整语言图景。

## 学习路径与模块划分

### 一、环境与入门（1–5）

1. **软件安装**（05:37）——安装 IDE 与编译器（如 Visual Studio / GCC），配置可编译运行的开发环境。
2. **编写 Hello World 程序**（06:55）——第一个程序：`main` 函数、`#include`、`std::cout`，理解“写码→编译→运行”的流程。
3. **变量和类型**（11:04）——内置类型（整型/浮点/字符/布尔）、变量声明与初始化、作用域与常量。
4. **运算符**（15:40）——算术、关系、逻辑、位运算符与优先级/结合性。
5. **编程练习**（18:01）——综合运用 1–4 节知识完成入门练习。

### 二、控制流与容器（6–9）

6. **条件判断**（07:58）——`if/else`、`switch`、三元运算符。
7. **循环**（06:59）——`for`、`while`、`do-while`、`break`/`continue`。
8. **数组和向量**（08:18）——定长数组、多维数组与 `std::vector` 动态数组。
9. **编程练习(2)**（16:48）——控制流与数组/向量的综合练习。

### 三、函数（10–12）

10. **函数(上)**（11:31）——函数声明与定义、参数传递（值/引用）、返回值。
11. **函数(下)：函数重载、递归函数**（08:33）——重载决议与递归程序设计。
12. **函数编程练习**（14:13）——以函数为单元的综合练习。

### 四、指针与引用（13）

13. **指针与引用**（13:32）——地址、解引用、指针算术、引用别名；为后续内存管理与面向对象打基础。

### 五、面向对象（14–19）

14. **类和对象(一)**（14:39）——封装、成员函数、构造函数、访问控制。
15. **类的继承与多态**（12:46）——继承层次、虚函数与运行时多态。
16. **类的编程练习**（11:11）——用面向对象方式编写一个可交互的面积计算程序。
17. **类和对象：静态成员、友元、override 与 final、const 函数**（10:13）——进阶类机制与修饰符。
18. **结构、联合、枚举**（09:31）——`struct`、`union`、`enum`/`enum class`。
19. **运算符的重载**（10:38）——为自定义类型定义运算符语义。

### 六、预处理与泛型（20–22）

20. **宏定义**（06:19）——预处理指令 `#define` 与宏替换。
21. **函数模板**（09:01）——泛型函数，一次定义、多类型复用。
22. **类模板**（09:14）——泛型类（如自定义容器雏形）。

### 七、模块化与错误处理（23–25）

23. **命名空间**（06:27）——`namespace` 组织符号、避免命名冲突。
24. **异常**（07:45）——`try/catch/throw` 异常处理机制。
25. **类型转换**（10:45）——`static_cast`/`reinterpret_cast` 等显式与隐式转换。

### 八、函数式与现代 C++（26–29）

26. **函数指针**（08:22）——指向函数的指针与回调。
27. **STL 标准库：容器**（12:14）——`vector`、`list`、`deque` 等顺序容器（见证据：STL 容器）。
28. **STL 标准库：map 和 set**（06:46）——关联容器与键值访问。
29. **函数封装与绑定**（07:45）——`std::function`、`std::bind` 把可调用对象统一管理。

### 九、智能指针与移动语义（30–35）

30. **智能指针(上) unique_ptr**（09:04）——独占所有权、RAII 自动释放。
31. **智能指针(下) shared_ptr 和 weak_ptr**（09:14）——共享所有权、引用计数与弱引用防循环。
32. **Lambda 表达式**（09:14）——匿名函数对象、捕获列表。
33. **右值引用和移动语义（上）**（12:45）——移动构造/移动赋值、转移资源所有权。
34. **右值引用和移动语义(下)**（07:44）——移动语义的进阶应用与性能收益。
35. **完美转发**（07:49）——`std::forward` 与引用折叠。

### 十、编译期与类型元编程（36–39）

36. **常量表达式和 constexpr**（11:26）——编译期求值常量。
37. **decltype 运算符**（10:22）——推导表达式的静态类型。
38. **类的特殊成员函数**（10:23）——默认/拷贝/移动构造与赋值、析构。
39. **类型特征 Type Traits**（09:52）——`std::is_*` 编译期类型判断（模板元编程基础）。

### 十一、算法库（40）

40. **Algorithm 算法库**（08:50）——`std::sort`、`std::find` 等通用算法（见证据：STL 四大组件）。

### 十二、并发与并行（41–52）

41. **并行编程**（09:44）——多线程/多核并行编程总览。
42. **线程 thread**（13:34）——`std::thread` 的创建、join/detach。
43. **promise 和 future**（10:00）——线程间结果传递与同步。
44. **互斥和锁 mutex & lock**（08:17）——`std::mutex`、`lock_guard`/`unique_lock` 保护共享数据。
45. **多线程死锁，std::lock 防死锁的原理**（09:51）——死锁成因与 `std::lock` 同时锁定多个锁。
46. **读写锁，shared_lock 的原理和使用**（07:54）——读共享/写独占的 `shared_mutex`/`shared_lock`。
47. **条件变量**（09:22）——`std::condition_variable` 等待/通知机制。
48. **信号量 Semaphore，std::counting_semaphore**（10:03）——计数信号量控制并发资源访问。
49. **异步任务，async 和 packaged_task**（07:29）——`std::async` 便捷异步、`packaged_task` 包装任务。
50. **线程屏障 barrier 和 latch**（07:07）——多线程同步点与一次性闸门。
51. **协程**（09:05）——C++20 无栈协程的挂起/恢复模型。
52. **协程可等待对象**（08:12）——`co_await`、Awaiter 定制。

### 十三、原子与内存模型（53–55）

53. **原子类型 atomic_flag**（07:07）——最简原子布尔与自旋锁。
54. **无锁算法和结构，CAS 原子操作**（08:34）——`compare_exchange` 与无锁编程。
55. **内存模型与顺序**（07:49）——顺序一致性、acquire/release 等内存序。

### 十四、概念约束（56）

56. **概念和约束（Concept，Constraint， Requires）**（时长未标注）——C++20 概念约束模板参数。

## 使用建议

- 按模块顺序观看，每节动手敲代码（“编程练习”章节务必自己先做再看答案）。
- 第 13 节（指针与引用）与第 30–35 节（智能指针/移动语义）是 C++ 区别于多数语言的重点，建议放慢节奏。
- 面向对象章节可与 [[cpp-class-and-raii]]、[[cpp]] 等页面互相印证；STL 章节结合 [[cpp-course-chapters]] 章节索引与 [[cpp-overview]] 概览使用。

## 参考

- 本课程为 CS205 C/C++ Program Design（南方科技大学，2021 秋）视频课章节整理；视频见 Bilibili BV1Vf4y1P7pq。
- [cppreference: C++ language](https://en.cppreference.com/w/cpp/language) —— 各主题的权威语言参考。
- [Wikipedia: C++](https://en.wikipedia.org/wiki/C%2B%2B) —— 语言概览。
- [Wikipedia: Standard Template Library](https://en.wikipedia.org/wiki/Standard_Template_Library) —— STL 组成。
