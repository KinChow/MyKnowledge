---
domain: computer-science
source_ref: llvm-auto-vectorization
title: LLVM 自动向量化
---
# LLVM 自动向量化

> 本工作文档由 LLVM 官方文档《Auto-Vectorization in LLVM》
> （https://llvm.org/docs/Vectorizers.html，source_id: llvm-auto-vectorization）
> 派生，结构按官方页面组织，内容为完整转述（零删减）。新增的加工性判断以"注："标注。

## 总览：两个向量化器

LLVM 有两个向量化器：作用于循环的 **Loop Vectorizer**，以及 **SLP Vectorizer**。
两者面向不同的优化机会、使用不同的技术：

- **SLP Vectorizer**：把代码中发现的多个标量合并成向量；
- **Loop Vectorizer**：把循环中的指令拓宽（widen），一次操作多个连续迭代。

两个向量化器默认都启用。

## Loop Vectorizer

### 用法

Loop Vectorizer 默认启用，可通过 clang 命令行标志禁用：

```shell
$ clang ... -fno-vectorize  file.c
```

### 命令行标志

循环向量化器用代价模型（cost model）决定最优的向量化因子（vectorization factor）
与展开因子（unroll factor）。用户也可以强制指定具体值，`clang` 与 `opt` 都支持。

- 控制 SIMD 宽度：

```shell
$ clang  -mllvm -force-vector-width=8 ...
$ opt -loop-vectorize -force-vector-width=8 ...
```

- 控制展开因子：

```shell
$ clang  -mllvm -force-vector-interleave=2 ...
$ opt -loop-vectorize -force-vector-interleave=2 ...
```

### Pragma 循环提示指令

`#pragma clang loop` 指令允许为后续的 for / while / do-while / C++11 range-based for
循环指定向量化提示：可启用或禁用向量化与交错（interleaving），也可手动指定向量宽度
与交错次数。

显式启用：

```c
#pragma clang loop vectorize(enable) interleave(enable)
while(...) {
  ...
}
```

通过指定向量宽度与交错次数隐式启用：

```c
#pragma clang loop vectorize_width(2) interleave_count(2)
for(...) {
  ...
}
```

详见 Clang language extensions 文档。

### 诊断（Diagnostics）

许多循环无法被向量化：复杂的控制流、不可向量化的类型与函数调用。循环向量化器会生成
优化备注（optimization remarks），可用命令行选项查询：

- `-Rpass=loop-vectorize`：识别**成功**向量化的循环；
- `-Rpass-missed=loop-vectorize`：识别**失败**的循环，并指示是否显式指定了向量化；
- `-Rpass-analysis=loop-vectorize`：识别导致向量化**失败的具体语句**；配合
  `-fsave-optimization-record` 可列出多个失败原因（该行为未来可能变化）。

示例（含 switch 的循环）：

```c
#pragma clang loop vectorize(enable)
for (int i = 0; i < Length; i++) {
  switch(A[i]) {
  case 0: A[i] = i*2; break;
  case 1: A[i] = i;   break;
  default: A[i] = 0;
  }
}
```

`-Rpass-missed=loop-vectorize` 输出：

```
no_switch.cpp:4:5: remark: loop not vectorized: vectorization is explicitly enabled [-Rpass-missed=loop-vectorize]
```

`-Rpass-analysis=loop-vectorize` 指出 switch 语句无法被向量化：

```
no_switch.cpp:4:5: remark: loop not vectorized: loop contains a switch statement [-Rpass-analysis=loop-vectorize]
  switch(A[i]) {
  ^
```

要得到行列号，需加上 `-gline-tables-only` 与 `-gcolumn-info`（见 Clang 用户手册）。

### 特性

LLVM Loop Vectorizer 具备一系列特性以向量化复杂循环。

#### 未知循环次数（unknown trip count）

支持未知迭代次数的循环。当迭代起始与结束未知、且迭代次数不保证是向量宽度整数倍时，
向量化器把最后几个迭代以标量代码执行（保留标量副本会增加代码体积）：

```c
void bar(float *A, float* B, float K, int start, int end) {
  for (int i = start; i < end; ++i)
    A[i] *= B[i] + K;
}
```

#### 指针运行时检查（Runtime Checks of Pointers）

若指针 A 与 B 指向连续地址，向量化不合法（A 的某些元素会在从 B 读之前被写）。
有些程序员用 `restrict` 关键字通知编译器指针不相交，但本例中向量化器无法知道 A 与
B 是否唯一。Loop Vectorizer 通过放置**运行时检查**处理：若数组 A 与 B 指向不相交的
内存则走向量化路径，若重叠则执行标量版本：

```c
void bar(float *A, float* B, float K, int n) {
  for (int i = 0; i < n; ++i)
    A[i] *= B[i] + K;
}
```

#### 归约（Reductions）

下例中 sum 变量被循环的连续迭代使用，通常这会阻止向量化；但向量化器能识别 sum 是
**归约变量**：sum 变成整数向量，循环结束时把向量各元素相加得到正确结果。支持多种
归约操作：加法、乘法、XOR、AND、OR。

```c
int foo(int *A, int n) {
  unsigned sum = 0;
  for (int i = 0; i < n; ++i)
    sum += A[i] + 5;
  return sum;
}
```

完全向量化归约需要重排操作顺序，对浮点运算有问题：浮点加法**不满足结合律**，结果
可能依赖求值顺序。C/C++ 标准隐式禁止改变浮点结果，因此 LLVM 仅在至少使用
`-fassociative-math -fno-signed-zeros -fno-trapping-math`（`-ffast-math` 的子集）时
才在多数目标上向量化浮点归约。在 AArch64、RISC-V 等目标上，LLVM 能生成保持精确结果
的 **ordered reductions（有序归约）**，实现有限度的、符合标准的向量化；但有序归约
通常比传统向量化归约低效，因此在这些目标上启用浮点重排仍可能得到更高效的归约。

#### 归纳变量（Inductions）

向量化器知道如何向量化归纳变量（例如把 i 的值存入数组）：

```c
void bar(float *A, int n) {
  for (int i = 0; i < n; ++i)
    A[i] = i;
}
```

#### 条件转换（If Conversion）

Loop Vectorizer 能把代码中的 IF 语句"展平"为单条指令流，支持最内层循环的任意控制流
（可含复杂嵌套的 IF/ELSE 甚至 GOTO）：

```c
int foo(int *A, int *B, int n) {
  unsigned sum = 0;
  for (int i = 0; i < n; ++i)
    if (A[i] > B[i])
      sum += A[i] + 5;
  return sum;
}
```

#### 指针归纳变量（Pointer Induction Variables）

下例使用 C++ 标准库的 accumulate 函数，循环用 C++ 迭代器（即指针）而非整数下标。
Loop Vectorizer 能识别指针归纳变量并向量化——这对大量使用迭代器的 C++ 程序很重要：

```c
int baz(int *A, int n) {
  return std::accumulate(A, A + n, 0);
}
```

#### 反向迭代器（Reverse Iterators）

可向量化向后计数的循环：

```c
void foo(int *A, int n) {
  for (int i = n; i > 0; --i)
    A[i] +=1;
}
```

#### 散聚（Scatter / Gather）

可向量化最终成为标量指令序列散聚（scatter/gather）内存的代码。很多情况下代价模型
会判定这不划算，LLVM 只在用 `-mllvm -force-vector-width=#` 强制时向量化：

```c
void foo(int * A, int * B, int n) {
  for (intptr_t i = 0; i < n; ++i)
      A[i] += B[i * 4];
}
```

#### 混合类型（Vectorization of Mixed Types）

可向量化混合类型的程序；代价模型会估算类型转换的开销并决定向量化是否划算：

```c
void foo(int *A, char *B, int n) {
  for (int i = 0; i < n; ++i)
    A[i] += 4 * B[i];
}
```

#### 全局结构体别名分析（Global Structures Alias Analysis）

对全局结构体的访问也可向量化，用别名分析保证访问不冲突；也支持在结构体成员的指针
访问上添加运行时检查。支持很多变体，但一些依赖忽略未定义行为（其他编译器这样做）的
变体仍保持不向量化：

```c
struct { int A[100], K, B[100]; } Foo;
void foo() {
  for (int i = 0; i < 100; ++i)
    Foo.A[i] = Foo.B[i] + 100;
}
```

#### 函数调用向量化（Vectorization of function calls）

Loop Vectorizer 可向量化**内建数学函数**（intrinsic math functions，清单见官方页面
表格）。注意：若数学库函数访问外部状态（如 errno），优化器可能无法向量化对应内建
函数；要更好地优化 C/C++ 数学库函数，使用 `-fno-math-errno`。

向量化器还了解目标上的特殊指令，会向量化映射到这些指令的函数调用循环。例如下列循环
在 x86 上存在 SSE4.1 roundps 指令时会被向量化：

```c
void foo(float *f) {
  for (int i = 0; i != 1024; ++i)
    f[i] = floorf(f[i]);
}
```

许多数学函数只有在文件用指定目标向量库构建（提供该数学函数的向量实现）时才能向量化。
clang 用 `-fveclib` 选项指定，可选向量库：
`Accelerate, libmvec, MASSV, SVML, SLEEF, Darwin_libsystem_m, ArmPL, AMDLIBM`：

```shell
$ clang ... -fno-math-errno -fveclib=libmvec file.c
```

#### 向量化过程中的部分展开（Partial unrolling during vectorization）

现代处理器有多个执行单元，只有并行度高的程序才能用满机器整个宽度。Loop Vectorizer
通过对循环做**部分展开**提升指令级并行（ILP）。下例把整个数组累加进 sum，效率低——
处理器只能用一个执行端口；展开后允许两个或更多执行端口同时工作：

```c
int foo(int *A, int n) {
  unsigned sum = 0;
  for (int i = 0; i < n; ++i)
      sum += A[i];
  return sum;
}
```

Loop Vectorizer 用代价模型决定何时展开有利，取决于寄存器压力与生成代码的体积。

#### 尾声向量化（Epilogue Vectorization）

向量化循环时常需要标量余数（epilogue）循环来处理尾部迭代（当循环次数未知或不能整除
向量化×展开因子时）。当向量化与展开因子较大时，迭代次数较小的循环可能把大部分时间
花在标量（而非向量）代码上。内层循环向量化器增强了 epilogue 向量化：用更可能让
小迭代次数循环仍以向量代码执行的向量化/展开因子组合来向量化尾声循环。控制流结构化地
避免复制运行时指针检查，并优化小迭代次数循环的路径长度。

#### 早退向量化（Early Exit Vectorization）

对带单个早退（early exit）的循环向量化时，早退之后的循环块会被谓词化（predicated），
向量循环总是经 latch 退出。循环以单个 BranchOnTwoConds VPInstruction 终止：
- 早退条件为真时，经 `vector.early.exit` 中间块退出（该块负责计算早退块使用的
  循环定义变量在退出时的值）；
- latch 退出条件为真时，经 middle.block 在退出块与标量余数循环之间选择；
- 否则 BranchOnTwoConds 跳回区域头继续执行。

BranchOnTwoConds 在溶解循环区域后被降低为一条条件分支链。

### 性能（Performance）

官方页面给出 clang 在 gcc-loops 基准（GCC autovectorization 页面的一组循环，
by Dorit Nuzman）上的执行时间对比：GCC-4.7、ICC-13、Clang-SVN 在 -O3 下开启/关闭
循环向量化，tuned for "corei7-avx"，运行于 Sandybridge iMac；以及相同配置的
Linpack-pc（Mflops，越高越好）。

### 持续开发方向（Ongoing Development Directions）

- **Vectorization Plan**：建模并升级 LLVM Loop Vectorizer 的基础设施。

## SLP Vectorizer

### 详情（Details）

SLP 向量化（又名 superword-level parallelism，超字级并行）的目标是把**相似且独立**的
指令合并成向量指令。内存访问、算术运算、比较运算、PHI 节点都可用该技术向量化。

例如下列函数对输入 (a1, b1) 与 (a2, b2) 执行非常相似的操作，基本块向量化器可把
这些合并为向量运算：

```c
void foo(int a1, int a2, int b1, int b2, int *A) {
  A[0] = a1*(a1 + b1);
  A[1] = a2*(a2 + b2);
  A[2] = a1*(a1 + b1);
  A[3] = a2*(a2 + b2);
}
```

SLP 向量化器**自底向上**、跨基本块处理代码，寻找可合并的标量。

### 用法（Usage）

SLP Vectorizer 默认启用，可通过 clang 命令行标志禁用：

```shell
$ clang -fno-slp-vectorize file.c
```

## Sandbox Vectorizer

Sandbox Vectorizer 是用于构建模块化向量化流水线的**实验性**框架，构建在 Sandbox IR
之上，聚焦于易测试性与易开发性。
