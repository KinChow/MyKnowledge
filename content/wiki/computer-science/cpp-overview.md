---
aliases: []
confidentiality: public
domain: computer-science
evidence:
- claim: 'Jun 14, 2026

    Editors:

    This is a living document under continuous improvement. Had it been an open-source
    (code) project, this would have been release 0.8. Copying, use, modification,
    and creation of derivative works from this project is licensed under an MIT-style
    license. Contributing to this project requires agreeing to a Contributor License.
    See the accompanying LICENSE file for details.'
  claim_id: cpp-overview-audit-1
  support: direct
  supporting_quotes:
  - evidence_id: evidence-99fe8a7b299c
    exact: 'Jun 14, 2026

      Editors:

      This is a living document under continuous improvement. Had it been an open-source
      (code) project, this would have been release 0.8. Copying, use, modification,
      and creation of derivative works from this project is licensed under an MIT-style
      license. Contributing to this project requires agreeing to a Contributor License.
      See the accompanying LICENSE file for details.'
  targets:
  - evidence_id: evidence-99fe8a7b299c
    source_id: web-computer-science-cpp-overview
id: cpp-overview
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-cpp-overview
- working-computer-science-cpp-overview
status: published
tags:
- cpp
- language-overview
- oop
- programming-language
title: C++概述
updated_at: '2026-09-06'
---
# C++概述

## 一句话结论

C++ 是基于 C 语言的面向对象语言，几乎完美兼容 C，具备编译型、强类型、手动内存管理、贴近硬件、零开销抽象等特点，往往在需要性能、操作底层的场景下使用。

## 核心概念

- **关键特性**：丰富的软件库、面向对象（封装/继承/多态/抽象）、编译型语言、手动内存管理、指针、强类型、完全兼容 C、贴近硬件（高性能、方便使用 GPU/FPGA 等新硬件）、零开销抽象（类、继承、模板、类型别名等）。
- **优点**：面向对象编程、多范式、低层次控制+高层次功能、性能好（"有限的可移植性"）。
- **缺点**：编程复杂学习成本高、部分库与平台相关、缺乏垃圾收集、不安全易造成内存泄漏。
- **一句话总结**：基于 C 语言的面向对象语言，往往在需要性能、操作底层的场景下使用 C++。

## 工作机制

- **演化**：C++98（1.0，第一个标准）→ C++03（1.0.1，修 bug）→ C++11（2.0，现代 C++）→ C++14（2.1）→ C++17（2.5，目前主流）→ C++20（3.0，大版本）。
- **学习路径**：像学外语一样（上手快、精通久）；精髓是积累的惯用法；把 C++ 当新语言而非"C 加上类"（参考 C++ Core Guidelines）；多写代码（leetcode）、多看代码（caffe、tensorflow、tvm、llvm），注重方法论与实际写代码结合。
- **Bjarne 洋葱原则**：复杂性管理——简单事情简单做；抽象层次——切得越深，哭得越多。
- **资源管理**：C++ 需要程序员手动分配和释放内存/资源，无垃圾自动回收；RAII 是 C++11 以后资源管理的解决方案。

## 示例或代码

C++ 版本演化对照：

| C++版本 | "版本号" | 说明 |
| --- | --- | --- |
| C++98 | 1.0 | 第一个C++标准 |
| C++03 | 1.0.1 | 修正了C++98标准的一些bug |
| C++11 | 2.0 | 全新的现代C++标准 |
| C++14 | 2.1 | C++11基础上的小改进 |
| C++17 | 2.5 | 中改进版本，目前主流 |
| C++20 | 3.0 | 大版本，加了很多新特性 |

## 常见误区

- **把 C++ 当作"C 加上类"**：应当把 C++ 当成新语言学习，精髓是惯用法而非语法。
- **以为 C++ 有自动垃圾回收**：C++ 需要手动分配/释放内存和资源，无自动 GC；RAII 是资源管理解决方案。
- **以为"可移植"意味着无需重新编译**：C++ 是编译型语言，跨平台（Arm/X86）必须重新编译。
- **以为 C++ 只是语法**：语言精髓是积累下来的惯用法，还应掌握工具链（g++/llvm、gdb、gprof、GNU Make/CMake）。

## 证据映射

| claim_id | 来源 | 要点 |
| --- | --- | --- |
| cpp-overview-audit-1 | web-computer-science-cpp-overview | C++ 概述文档是持续改进的活文档（release 0.8，MIT 风格许可） |

## 待验证项

无

## 关联知识

- [[cpp]]：C++ 语言综合问答
- [[cpp-vs-c]]：C++ 与 C 的对比（OOP 与 POP）
- [[cpp-vs-java]]：C++ 与 Java 的对比（编译/解释、内存管理）
- [[cpp-vs-python]]：C++ 与 Python 的对比（静态/动态、性能/便利）

## 详细章节

### C++概述

#### C++语言特点综述

##### 关键特性

* 丰富的软件库
* 面向对象
  * 封装（Encapsulation）：封装是将数据和方法组合在一起，对外部隐藏实现细节，只公开对外提供的接口。这样可以提高安全性、可靠性和灵活性。
  * 继承（Inheritance）：继承是从已有类中派生出新类，新类具有已有类的属性和方法，并且可以扩展或修改这些属性和方法。这样可以提高代码的复用性和可扩展性。
  * 多态（Polymorphism）：多态是指同一种操作作用于不同的对象，可以有不同的解释和实现。它可以通过接口或继承实现，可以提高代码的灵活性和可读性。
  * 抽象（Abstraction）：抽象是从具体的实例中提取共同的特征，形成抽象类或接口，以便于代码的复用和扩展。抽象类和接口可以让程序员专注于高层次的设计和业务逻辑，而不必关注底层的实现细节。

* 编译型语言
* 手动内存管理
* 指针
* 强类型语言
* 完全兼容C语言
* 贴近硬件
  * 使用原生的指令和类型，高性能
  * 方便使用新的硬件（包括GPU、FPGA等）
* 零开销抽象
  * 类、继承、模板、类型别名...
  * 将来：完全的类型和资源安全，概念、模块、并发、契约...



##### 优点

* 有限的可移植性
* 面向对象编程
* 多范式
* 低层次控制，高层次功能
* 性能好



##### 缺点

* 编程复杂，学习成本高
* 一些库特定与平台：图形无关
* 缺乏垃圾收集
* 不安全，容易造成内存泄漏



##### 一句话总结

基于C语言的面向对象语言，往往在需要性能操作底层的场景下使用C++语言



#### 演化

| C++版本 | “版本号” | 说明                     |
| ------- | -------- | ------------------------ |
| C++98   | 1.0      | 第一个C++标准            |
| C++03   | 1.0.1    | 修正了C++98标准的一些bug |
| C++11   | 2.0      | 全新的现代C++标准        |
| C++14   | 2.1      | C++11基础上的小改进      |
| C++17   | 2.5      | 一个中改进版本，目前主流 |
| C++20   | 3.0      | 大版本，加了很多新特性   |



#### 学习

##### 如何学习C++

* 想学习一门外语一样
  * 上手很快，真正掌握需要很久
* 惯用法
  * 语言的精髓不是语法，而是积累下来的惯用法
* 把C++当成新语言，而不是“C加上类”
  * 学习《C++核心指南》（[C++ Core Guideline](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)）
* 多写代码：leetcode
* 多看代码：caffe、tensorflow、tvm、llvm
  * ﻿﻿注重方法论和实际写代码相结合
  * ﻿﻿设计模式的学习
  * ﻿﻿UML建模． STL源码剖析



##### Bjarne的洋葱原则

* 复杂性管理
  * 简单事情简单做
* 抽象层次
  * 切得越深，哭得越多



#### 总结

* ﻿﻿C++几乎完美兼容了C语言
* ﻿﻿C++的精髓在于面向对象编程：封装、继承、多态
* ﻿﻿可以有效实现设计模式
* ﻿﻿C++属于编译型语言，在不同平台需要重新编译
* ﻿﻿C++属于静态语言，需要强制声明类型
* ﻿﻿C++需要程序员手动分配和释放内存/资源，没有垃圾自动回收。
    * ﻿﻿RAll是C++11以后资源管理的解決方案
* ﻿﻿使用C++的主要目的在于性能及可操控性（可预测性）
    * ﻿﻿底层控制
    * ﻿﻿编译器优化（g++/llvm） icc/nvcc
    * ﻿﻿STL库的使用
    * ﻿﻿多线程编程模型
* ﻿﻿使用C++不仅需要熟练使用编译器（g++/llvm），还需要使用工具
    * ﻿debug工具：gdb
    * ﻿profiler工具：gprof
    * ﻿构建工具：GNU Make/CMake
