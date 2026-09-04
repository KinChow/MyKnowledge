---
aliases:
- Neon
- ARM NEON
- SIMD
confidentiality: public
domain: computer-science
evidence:
- claim: NEON 是 ARM 高级 SIMD（Advanced SIMD）架构的实现：32 个 128 位向量寄存器 + SIMD 指令同时操作多个数据通道。
  claim_id: neon-role
  support: direct
  supporting_quotes:
  - evidence_id: evidence-068c54a90cb8
    exact: "Neon is the implementation of Arm’s Advanced SIMD architecture.  \n     \n
      \    The purpose of Neon is to accelerate data manipulation by providing: \n
      \     \n      Thirty-two 128-bit vector registers, each capable of containing
      multiple lanes of data. \n      SIMD instructions to operate simultaneously
      on those multiple lanes of data"
  targets:
  - evidence_id: evidence-068c54a90cb8
    source_id: arm-neon-intro
- claim: 程序员可通过多种方式利用 NEON：NEON 库（如 Arm Compute Library）、编译器自动向量化、Neon intrinsics、手写汇编。
  claim_id: neon-ways
  support: direct
  supporting_quotes:
  - evidence_id: evidence-1a3104fe62bf
    exact: "As a programmer, there are a number of ways you can make use of Neon technology:
      \n      \n      Neon-enabled open source libraries such as the Arm Compute Library
      provide one of the easiest ways to take advantage of Neon. \n      Auto-vectorization
      features in your compiler can automatically optimize your code to take advantage
      of Neon. \n      Neon intrinsics are function calls that the compiler replaces
      with appropriate Neon instructions. This gives you direct, low-level access
      to the exact Neon instructions you want, all from C, or C++ code. \n      For
      very high performance, hand-coded Neon assembler can be the best approach for
      experienced programmers"
  targets:
  - evidence_id: evidence-1a3104fe62bf
    source_id: arm-neon-intro
- claim: Neon intrinsics 是 arm_neon.h 定义的 C/C++ 函数，编译器内联短汇编内核并处理寄存器分配与流水线优化。
  claim_id: intrinsics
  support: direct
  supporting_quotes:
  - evidence_id: evidence-b972ba96913c
    exact: Intrinsics are functions whose precise implementation is known to a compiler.
      The Neon intrinsics are a set of C and C++ functions defined in arm_neon.h which
      are supported by the Arm compilers and GCC. These functions let you use Neon
      without having to write assembly code directly, since the functions themselves
      contain short assembly kernels which are inlined into the calling code. Additionally,
      register allocation and pipeline optimization are handled by the compiler so
      many difficulties faced by the assembly programmer are avoided
  targets:
  - evidence_id: evidence-b972ba96913c
    source_id: arm-neon-why-intrinsics
- claim: arm_neon.h 数据类型分三类：baseW_t 标量、baseWxL_t 向量、baseWxLxN_t 向量数组。
  claim_id: intrinsics-conventions
  support: direct
  supporting_quotes:
  - evidence_id: evidence-83f47882ed36
    exact: "There are three major categories of data type available in arm_neon.h
      which follow these patterns: \n      \n      baseW_t scalar data types \n      baseWxL_t
      vector data types \n      baseWxLxN_t vector array data types"
  targets:
  - evidence_id: evidence-83f47882ed36
    source_id: arm-neon-conventions
id: arm-neon
kind: knowledge
publication_scope: public
related: []
sources:
- arm-neon-intro
- arm-neon-why-intrinsics
- arm-neon-conventions
status: published
tags:
- arm
- neon
- simd
- vectorization
title: ARM NEON：SIMD 扩展与 intrinsics
updated_at: '2026-09-04'
---

# ARM NEON：SIMD 扩展与 intrinsics

## 一句话结论

NEON 是 ARM 高级 SIMD（Advanced SIMD）架构的实现，提供 32 个 128 位向量寄存器与 SIMD 指令以同时操作多个数据通道，加速多媒体/信号处理/图像等定点与浮点密集型应用。程序员可通过库（Arm Compute Library）、编译器自动向量化、Neon intrinsics（`arm_neon.h`）或手写汇编利用它；intrinsics 是最常用的平衡点——直接访问 NEON 指令而免去手写汇编的负担。

## 核心概念

- **NEON（Advanced SIMD）**：ARM 的 SIMD 扩展，32 个 128 位向量寄存器，每个寄存器含多个数据通道（lane），SIMD 指令对多个通道同时运算。
- **利用 NEON 的四种方式**：①NEON 库（如 Arm Compute Library）②编译器自动向量化 ③Neon intrinsics（`arm_neon.h`）④手写汇编（最高性能但最难）。
- **intrinsics 机制**：`arm_neon.h` 中的 C/C++ 函数，编译器内联短汇编内核，并处理寄存器分配与流水线优化。
- **数据类型约定**：`baseW_t`（标量）、`baseWxL_t`（向量）、`baseWxLxN_t`（向量数组）。

## 工作机制

NEON 的 SIMD 执行模型：

1. **数据布局**：128 位向量寄存器拆分为多个通道（如 4×32 位、8×16 位、16×8 位）。
2. **单指令多数据**：一条 SIMD 指令对寄存器内所有通道同时执行同一操作。
3. **intrinsics 映射**：`arm_neon.h` 函数 → 编译器内联的短汇编内核 → 后端 NEON 指令；编译器负责寄存器分配与调度。

## 示例或代码

```c
#include <arm_neon.h>
// 两个 4×32 位浮点向量逐元素相加（128 位寄存器 = 4 通道）
float32x4_t a = vld1q_f32(ptr_a);
float32x4_t b = vld1q_f32(ptr_b);
float32x4_t c = vaddq_f32(a, b);
```

## 常见误区

- **NEON 不等于自动向量化**：NEON 是硬件扩展；编译器自动向量化只是利用它的方式之一，`-O3` 也可能不触发（取决于循环结构与成本模型，见 compiler-vectorization）。
- **intrinsics 不是万能**：学习曲线比用库陡峭，手工汇编可能获得更大性能空间。
- **宏判断特性**：`__ARM_NEON`（AArch64 恒 1）、`__ARM_NEON_FP`、`__ARM_FEATURE_CRYPTO`、`__ARM_FEATURE_FMA` 分别标识可用特性。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| neon-role / neon-ways | arm-neon-intro | SIMD 定义 + 四种利用方式 |
| intrinsics | arm-neon-why-intrinsics | arm_neon.h 机制 |
| intrinsics-conventions | arm-neon-conventions | 类型三分类 |

## 待验证项

无。

## 关联知识

- [[compiler-vectorization]] —— 编译器自动向量化（NEON 是其目标之一）。
- [[architecture-and-organization]] —— ARM 架构与微架构（NEON 属于处理器执行流水线的一部分）。

## 详细章节

#### 什么是Neon

Neon 是适用于 ARM Cortex-A 和 Cortex-R 系列处理器的一种实现数据并行化 SIMD（Single Instruction Multiple Data）扩展架构。

Neon 的目的是通过提供以下功能来加速数据操作：

- 32 个 128 位向量寄存器，每个向量寄存器都能够包含多个数据通道。
- SIMD 指令可同时对多个数据通道进行操作。



作为程序员，您可以通过多种方式利用 Neon 技术：

- 调用库函数：直接在代码中使用Neon优化过的库函数，例如 [Arm Compute Library](https://developer.arm.com/ip-products/processors/machine-learning/compute-library)。
- 自动向量化：通过编译选项，编译器中的自动向量化功能可以自动优化代码以利用 Neon 指令。
- [Neon intrinsics](https://developer.arm.com/architectures/instruction-sets/simd-isas/neon/intrinsics)：可以使用函数调用编译器替换 Neon 指令。这可以使得在C或C++上直接调用底层访问 Neon 指令。
- 汇编方式：为了获得非常高的性能，手工编写 Neon 内联汇编代码可能是经验丰富的程序员的最佳方法。



Neon 是多媒体和信号处理、3D 图形、语音、图像处理或其他对定点和浮点性能至关重要的应用。



#### Neon intrinsic

Neon intrinsic 是编译器知道的精确实现函数。Neon intrinsic 是一组定义的 C 和 C++ 函数，`arm_neon.h`受 Arm 编译器和 GCC 支持。这些函数使您无需直接编写汇编代码即可使用 Neon，因为函数本身包含内联到调用代码中的短汇编内核。此外，寄存器分配和流水线优化由编译器处理，因此避免了汇编程序员面临的许多困难。



##### 优缺点

| 优点 | 缺点 |
| --- | --- |
| 功能强大：直接访问 Neon 指令集，无需手写汇编 | 学习曲线比导入库或依赖编译器更陡峭 |
| 可移植：C/C++ 代码可跨目标/执行状态编译（如 AArch32→AArch64） | 手工优化的汇编可能提供更大性能空间，但更难编写 |
| 灵活：需要时用 Neon，否则用 C/C++，避免低级工程问题 | |



##### 宏

为了使用内在函数，必须支持高级 SIMD 架构，并且某些特定指令在任何情况下都可能启用或不启用。当定义以下宏且等于1时，相应的功能可用：

| 宏 | 含义 | AArch64 |
| --- | --- | --- |
| `__ARM_NEON` | 编译器支持高级 SIMD | 始终为 1 |
| `__ARM_NEON_FP` | 支持 Neon 浮点运算（bitmap，AArch64 下 double-precision 恒置位） | 恒定义 |
| `__ARM_FEATURE_CRYPTO` | 提供加密指令（加密 Neon intrinsics 可用） | 按实现 |
| `__ARM_FEATURE_FMA` | 融合乘法累加指令可用 | 按实现 |



##### 类型

可用的数据类型分为三大类，其中`arm_neon.h`遵循以下模式：

| 类别 | 模式 | 说明 |
| --- | --- | --- |
| 标量 | `baseW_t` | 基本标量类型 |
| 向量 | `baseWxL_t` | L 个标量组成的向量（64/128 位，适合 NEON 寄存器） |
| 向量数组 | `baseWxLxN_t` | N 个向量组成的数组（对应同时操作多个寄存器的指令） |

命名含义：

| 字母 | 含义 |
| --- | --- |
| `base` | 基本数据类型 |
| `W` | 基本类型的宽度 |
| `L` | 向量中标量实例的数量 |
| `N` | 向量数组类型的数量（标量数组结构） |

一般来说`W`，`L`向量数据类型的长度为 64 或 128 位，因此完全适合 Neon 寄存器。N 对应于同时对多个寄存器进行操作的指令。



##### 功能

根据 Arm C 语言扩展，`arm_neon.h` 中的函数原型遵循通用模式：

```
ret v[p][q][r]name[u][n][q][x][_high][_lane | laneq][_n][_result]_type(args)
```

请注意，某些字母和名称已重载，但按上述顺序排列：

- `ret`

  函数的返回类型。

- `v`

  vector 的缩写，存在于所有 intrinsic 中。

- `p`

  表示成对运算。

- `q`

  表示饱和操作（除  `vqtb[l][x]` 外的AArch64 操作， 其中`q`表示 128 位索引和结果操作数）。

- `r`

  表示舍入运算。

- `name`

  基本操作的描述性名称。

- `u`

  表示有符号到无符号的转换。

- `n`

  表示缩小操作。

- `q`

  名称后缀，表示对 128 位向量进行操作。

- `x`

  表示 AArch64 中的高级 SIMD 标量运算。它可以是`b`、 `h`、 `s`或 `d`（即 8、16、32 或 64 位） 之一 。

- `_high`

  在 AArch64 中，用于涉及 128 位操作数的加宽和缩小运算。对于加宽 128 位操作数， `high`指的是源操作数的高 64 位。对于缩小范围，它指的是目标操作数的顶部 64 位。

- `_n`

  表示作为参数提供的标量操作数。

- `_lane`

  表示取自向量通道的标量操作数。 `_laneq`表示从 128 位宽度的输入向量通道中获取的标量操作数。（ `left | right`表示仅 `left`或 `right`将出现）。

- `type`

  缩写形式的主要操作数类型。

- `args`

  函数的参数。



#### 参考

[Optimizing C code with Neon intrinsics](https://developer.arm.com/documentation/102467/0201)