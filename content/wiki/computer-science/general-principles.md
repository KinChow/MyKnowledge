---
aliases: []
confidentiality: public
domain: computer-science
evidence:
- claim: Optimizations are implemented as Passes that traverse some portion of a program
    to either collect information or transform the program.
  claim_id: general-principles-audit-1
  support: direct
  supporting_quotes:
  - evidence_id: evidence-e5a7dc42e0a0
    exact: Optimizations are implemented as Passes that traverse some portion of a
      program to either collect information or transform the program.
  targets:
  - evidence_id: evidence-e5a7dc42e0a0
    source_id: web-computer-science-compilation-and-runtime-optimization
id: general-principles
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-compilation-and-runtime-optimization
- working-computer-science-general-principles
status: published
tags:
- performance-optimization
- compilation-optimization
- runtime-optimization
- cpu
- software-design
title: 总体原则
updated_at: '2026-09-06'
---
# 总体原则

## 一句话结论

软件性能优化覆盖编译期与运行期两个时期：编译期通过软件实现高效性、代码冗余识别与优化、算法优化，以及编译选项优化与编译技术演进发挥作用；运行期通过内存/缓存效率、CPU 指令体系与并发锁机制获得效率提升。其总体原则可概括为"降冗余、提效率"——减少指令数量，并提升访存效率、提升指令效率、降低执行阻塞。

## 核心概念

- **性能方程**：CPU处理时间 = 指令数 × 平均每条指令需要时钟周期数 × 每个时钟周期的时间。
- **编译期**：源代码 → 编译/链接 → 机器指令。
- **运行期**：内存、CPU（cache 子系统指令/数据、指令流水线）、操作系统与运行时。
- **编译期优化**：软件实现是否高效、代码冗余识别与优化、实现算法优化。
- **编译系统优化能力**：编译选项优化、现代编译技术演进。
- **运行期效率优化**：内存/缓存效率、CPU 指令体系、并发和锁机制。
- **总体原则**：降冗余（减少指令数量）、提效率（提升访存效率、提升指令效率、降低执行阻塞）。

## 工作机制

### 编译期
- **编译期优化**：评估软件实现是否高效、识别并优化代码冗余、实现算法优化。
- **编译系统优化能力**：通过编译选项优化与现代编译技术演进提升生成代码的质量。

### 运行期
- **内存/缓存效率**：i-cache 与 d-cache 效率优化、时间空间互换。
- **CPU 指令体系**：矢量指令集/SIMD、原子化指令。
- **并发和锁机制**：线程并发冲突消减、无锁/免锁机制。

### 总体原则
- **降冗余**：减少指令数量。
- **提效率**：提升访存效率、提升指令效率、降低执行阻塞。

## 示例或代码

**性能分析基准公式**：

CPU处理时间 = 指令数 * 平均每条指令需要时钟周期数 * 每个时钟周期的时间

**时期与优化要点对照**：

| 时期 | 关注对象 | 优化手段 |
| --- | --- | --- |
| 编译期 | 源代码 → 编译/链接 → 机器指令 | 软件实现效率、冗余识别、算法优化、编译选项 |
| 运行期 | 内存、CPU（cache、流水线）、OS/运行时 | 缓存效率、SIMD/原子指令、并发与锁机制 |

## 常见误区

- 只关注编译期优化而忽视运行期的访存与缓存效率。
- 把优化简单等同于减少指令，忽略"提效率"中访存效率、指令效率、执行阻塞三个维度。
- 忽视并发与锁机制对执行阻塞的影响。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| general-principles-audit-1 | web-computer-science-compilation-and-runtime-optimization | 优化以 Pass 形式实现，遍历程序的部分以收集信息或变换程序 |

## 待验证项

无。

## 关联知识

- [[compilation-and-runtime-optimization]] —— 编译与运行期优化。
- [[compiler-vectorization]] —— 编译器自动向量化。
- [[program-performance-analysis]] —— 程序性能分析。
- [[cpu-and-memory]] —— CPU 与内存机制。
- [[cpu-cache-optimization]] —— 缓存效率优化。
- [[software-design]] —— 软件设计总览。

## 详细章节

### 总体原则

CPU处理时间 = 指令数 * 平均每条指令需要时钟周期数 * 每个时钟周期的时间



#### 时期

编译期

* 源代码
* 编译/链接
* 机器指令



运行期

* 内存
* CPU
  * cache子系统指令、数据
  * 指令流水线
* 操作系统、运行时



#### 优化

编译期优化

* 软件实现是否高效
* 代码冗余识别与优化
* 实现算法优化



编译系统优化能力

* 编译选项优化
* 现代编译技术演进



运行期效率优化

* 内存/缓存效率
  * i-cache和d-cache效率优化
  * 时间空间互换
* CPU指令体系
  * 矢量指令集/SIMD
  * 原子化指令
* 并发和锁机制
  * 线程并发冲突消减
  * 无锁、免锁机制



#### 软件性能优化的总体原则

降冗余

* 减少指令数量



提效率

* 提升访存效率
* 提升指令效率
* 降低执行阻塞
