# Neon

## 什么是Neon

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



## Neon intrinsic

Neon intrinsic 是编译器知道的精确实现函数。Neon intrinsic 是一组定义的 C 和 C++ 函数，`arm_neon.h`受 Arm 编译器和 GCC 支持。这些函数使您无需直接编写汇编代码即可使用 Neon，因为函数本身包含内联到调用代码中的短汇编内核。此外，寄存器分配和流水线优化由编译器处理，因此避免了汇编程序员面临的许多困难。



### 优缺点

使用 Neon 内在函数有很多好处：

- 功能强大：Neon intrinsic 使程序员可以直接访问 Neon 指令集，而无需手写汇编代码。
- 可移植：手写的 Neon 汇编指令可能需要针对不同的目标处理器重写。包含 Neon 内在函数的 C 和 C++ 代码可以针对新目标或新执行状态（例如，从 AArch32 迁移到 AArch64）进行编译，只需进行最少的代码更改或无需更改代码。
- 灵活：程序员可以在需要时利用 Neon，或者在不需要时使用 C/C++，同时避免许多低级工程问题。

然而，Neon intrinsic 函数可能并非在所有情况下都是正确的选择：

- 使用 Neon intrinsic 的学习曲线比导入库或依赖编译器更陡峭。
- 手工优化的汇编代码可能会提供最大范围的性能改进，即使它更难以编写。



### 宏

为了使用内在函数，必须支持高级 SIMD 架构，并且某些特定指令在任何情况下都可能启用或不启用。当定义以下宏且等于1时，相应的功能可用：

* `__ARM_NEON`
  * 编译器支持高级 SIMD。AArch64 始终为 1。
* `__ARM_NEON_FP`
  * 支持 Neon 浮点运算。AArch64 始终为 1。
* `__ARM_FEATURE_CRYPTO`
  * 提供加密指令。因此，加密 Neon 内在函数是可用的。
* `__ARM_FEATURE_FMA`
  * 可以使用融合乘法累加指令。因此，使用这些的 Neon 内在函数是可用的。



### 类型

可用的数据类型分为三大类，其中`arm_neon.h`遵循以下模式：

- `baseW_t`：标量数据类型
- `baseWxL_t`：向量数据类型
- `baseWxLxN_t`：向量数组数据类型

其中：

- `base`：基本数据类型。
- `W`：基本类型的宽度。
- `L`：向量数据类型中标量数据类型实例的数量，例如标量数组。
- `N`：向量数组类型中向量数据类型实例的数量，例如标量数组的结构。

一般来说`W`，`L`向量数据类型的长度为 64 或 128 位，因此完全适合 Neon 寄存器。N 对应于同时对多个寄存器进行操作的指令。



### 功能

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



## 参考

[Optimizing C code with Neon intrinsics](https://developer.arm.com/documentation/102467/0201)