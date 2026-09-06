---
aliases: []
confidentiality: public
domain: computer-science
evidence:
- claim: Khronos 的 OpenCL 页面说明，OpenCL 通过核心规范纳入已广泛部署的能力，并支持开发者依赖跨实现能力。
  claim_id: maleoon-opencl-cross-platform
  support: direct
  supporting_quotes:
  - evidence_id: evidence-4eadd0c0e1f0
    exact: OpenCL 3.1 brings widely deployed, field-proven capabilities into the core
      specification to expand functionality, including SPIR-V ingestion, that developers
      can rely on across implementations.
  targets:
  - evidence_id: evidence-4eadd0c0e1f0
    source_id: khronos-opencl-overview-v2
id: optimizing-opencl-for-maleoon-gpus
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- khronos-opencl-overview-v2
- working-computer-science-optimizing-opencl-for-maleoon-gpus
status: published
tags:
- opencl
- gpu
- optimization
- performance
title: Maleoon Gpu的OpenCL优化
updated_at: '2026-09-06'
---
# Maleoon Gpu的OpenCL优化


## 一句话结论

针对终端 Maleoon GPU 的 OpenCL 优化要点：调优 Local size（每个 warp 为 SIMD32/64，local size 太小会浪费 warp 内线程）；减少标量 char 的 load/store（用向量读写提升带宽利用率）；避免 bank conflict；留意 vec8/vec16 拆分带来的带宽损失；多用 shared memory；必要时用 native 数学函数、fma、内聚 kernel 降低寄存器压力。

## 核心概念

- **Local size 优化**：每个 warp 的线程数为 SIMD32 或 SIMD64；小核模式下 local size 太小会导致 warp 内大量线程无法有效运算。
- **标量 char load/store**：一个时钟周期最多处理一定 thread 的 load/store；char 相对 int 总线利用率仅 8/32=25%。
- **bank conflict**：所有 thread 访问同一 bank（地址 overlap）时发生。
- **vec8/vec16**：vload16 拆成 4 个 vec4 后 thread 地址交错，LS 单元每周期只处理 2 个 thread（8B），带宽利用率 25%；vec8 为 50%。
- **shared memory**：片上 memory（latency 约 30 cycles）远高于片外，同样存在 bank conflict。
- **其他**：类型强转影响 TU 优化、native 数学函数、fma 替代乘加、变量早释放、循环不变量外提、& 替代取模、half 无法走 TU、TU 使用限制。

## 工作机制

1. local size 从 3×1/1×16 改为 3×64/2×32 后性能分别提升 10 倍/2 倍（camera 后处理预览与视频处理）。
2. 用 vload4/vstore4（int）替换 vload16/vstore16（char），例如 memcpy_int4 替换 memcpy_char16/char8。
3. filter 矩阵 < 16KB 时先 load 到 shared memory 再频繁访问。
4. cropresizeUV/cropresizeY 中把 int 保存改为 short，编译器把 mul+add 合并成 mad。
5. 2 的幂次取模/除法用 & 实现（如 w & (patternStride-1)）。
6. TU 访存带宽约为 LSC 的 2 倍，但要求：不能用强制类型转换、只能 vload2 以上、仅 readonly buffer（kernel 对该指针无写操作）。

## 示例或代码

（w % patternStride → w & (patternStride - 1) 等代码片段见 ## 详细章节。）

## 常见误区

- 忽略 local size 太小导致 warp 内线程空转。
- 用标量 char 频繁 load/store，浪费总线带宽。
- 在 kernel 内做 short→char→short 类型强转，导致 TU 优化无法使用。
- 大量中间变量延迟释放导致寄存器超标（>128 会引入 pvt 逻辑）。

## 证据映射

| claim_id | 来源 | 要点 |
| --- | --- | --- |
| maleoon-opencl-cross-platform | khronos-opencl-overview-v2 | OpenCL 3.1 核心规范纳入 field-proven 能力（含 SPIR-V） |

## 待验证项

- 性能提升量（3×64、2×32 分别 10 倍/2 倍）来自实测记录，未标注具体设备与基准，待复核。
- “性能一被会获得提升”等原文笔误已在提炼中规避，原文保留。

## 关联知识

- [[opencl-optimizations-list]] —— OpenCL 优化清单。
- [[opencl-optimization-guideline]] —— OpenCL 优化指导。
- [[overview-of-opencl]] —— OpenCL 基础。


## 详细章节

### Maleoon Gpu的OpenCL优化

#### Local Size的优化

##### 原理

每个warp的线程数目是simd32或者simd64；如果按照小核模式配置的local size太小，会导致一个warp内的大量线程无法进行有效的运算。



##### 优化示例

local size从3×1和1×16修改为3×64和2×32后，性能分别提升了10倍和2倍，所以，针对终端的camera 拍照后处理预览和视频的处理算法需要进行Local size的调优。





#### 减少标量char数据的load/store（或者使用vload4替代vload1）

##### 原理

我们的硬件实现中，一个时钟周期最多处理一定thread的load/store。假如每个thread处理的都是char，与处理int类型相比，总线利用率只有8/32=25%，效率低下。

因此，应尽量避免使用标量char的load/store。可以用矢量读写，或用更大的数据类型，有助于提高带宽利用率。

boxfilter对不同radius单独优化





#### 尽力避免bank conlict

##### 所有thread访问的bank集中



##### thread地址overlap

多个thread访问同一个bank的不同偏移

需要了解bank数量及bank大小





#### 留意vec8/vec16

执行一次vload16，thread0要读取的地址范围是0~15，thread1要读取的地址范围是16~31，thread2要读取的地址范围是32~47，thread3要读收的地址范围是48~63，如此等等。

在vec16被拆分成4个vec4进行load/store的时候，拆出来的第一条vec4 load/stoe指令中，thread0要读取的地址范围是0~3，thread1要读取的地址范围是16~19，thread2要读取的地址范围是32~35，thread3要读取的地址范围是48~51。此时thread0/thread2都访问到bank0，thread1/thread3访问到bank4。Load Store单元每个时钟周期只能处理2个thread，也就是读写8B，带充利用率只有25％。类似的，vec8拆分后获得的带宽利用率是50%。

当然，只有在thread之间地址连续的时候才是这样的带宽效率损失。当patter发生变化时，情况要另外分析。



##### 优化示例

这种情况的最好做法是用vload4/vstore4（int）替换vload16/vstore16（char）。例子就是用memcpy_int4替换memcpy_char16和memepy_char8





#### 多用shared memory

##### 原理

有片上memoy用来做local memory（硬件一般称shared mnenory）。片上memory的访问性能（Latency大约30 cycles）远高了片外。

Shared memory的bank结构和前面介绍的cache ram完全相同，也会有bank conflict，这个要注意到。



##### 场景

如果filter矩阵小于16KB，可以把filter矩阵先load到shared memory，然后在计算过程中再频繁访问，性能一被会获得提升。





#### 数据类型的强制转换

算法中大量存在short数据类型转换成char类型，然后做一个偏移，再转换成short类型，这样的写法在spec中也不推荐。还影响性能，没有办法充分利用硬件的tu带宽，导致只读buffer转tu的优化设法使用。



##### 原理

针对只读buffer，可以针对buffer走tu的模式，但是，对于有类型强制转换的这类场景，不会做此优化。





##### 优化方法

这种情况的最好做法是传入的buffer是经过偏移后，不在gpu kernel内做类型的转换。





#### 在精度允许的情况下使用native的数学函数

##### 原理

为了精度考虑，opencl的很多数学函数，采用了绕行的指令，指令序列比较的长。所以在使用中建议采用native_xx 进行使用。



##### 优化方法

针对有数学函数的场景，使用native_xx 替代原有的算法功能。





#### 对于卷积类可以使用fma替代乘加，减少指令数

##### 原理

对于卷积类的算法，中间有大量的乘加操作，可以使用fma进行EU指令性能的优化。





#### Kernel中写法要内聚，变量尽可能早释放

##### 原理

Kernel如果编译完的reg数量太大，而且是因为中间的变量延迟释放导致的话，那需要在书写Kernel的时候尽可能使得算法内聚，用完的变量尽快释放。



##### 优化方法

可以把算法进行内聚，这样可以大量降低reg的使用量，在寄存器大大超过128的情况下，会引入pvt的逻辑





#### int转short

cropresizeUV和cropresizeY算子中，存在将输入的char和short数据保存到int类型中进行运算，导致在指令中有许多的move和and冗余指令，将其改成short类型进行保存，编译器将其优化并把mul和add指令合并成mad指令。





#### 除法 float防下溢int序列化

取余的算法和除法一样，因为CL精度的原因指令会比较复杂。

##### 循环不变量外提



##### 由于除数patternStride是2成4（2的幂次方），可通过&来实现

```
w % patternStride 
h % patterStride
```


改成

```
w & (patternStride - 1)
h & (patternstride - 1)
```







#### half类型不能进行LSC走tuTU优化

kernel中有大量ld指令，由于入参img_src是half类型，无法走TU优化，可将入参类型转成short，再通过convert_float等进行转换。





#### 非4字节对齐





#### Opencl kernel如何写能使用TU优化

TU访存带宽相比LSC更大，大约是LSC的2倍，能优化访存性能。



使用限制：

1.    不能用强制类型转换；
2.   只能支持vload2以上的；
3.   仅支持readonly的buffer，从kernel维度看，没有对该指针的写操作。
