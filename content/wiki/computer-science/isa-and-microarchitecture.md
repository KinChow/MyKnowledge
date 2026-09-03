---
aliases:
- 多核软件设计
- ISA 分类
confidentiality: public
domain: computer-science
evidence:
- claim: ISA 是软件命令与硬件执行之间的接口，规定程序可见的属性（概念结构与功能行为），并区别于逻辑设计与物理实现。
  claim_id: isa-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-f997d3883be5
    exact: |-
      The ISA is the interface between what the software commands
      and what the hardware carries out
  - evidence_id: evidence-26b01009ad0d
    exact: |-
      the attributes of a
      system as seen by the programmer, i.e., the conceptual
      structure and functional behavior as distinct from the
      organization of the dataflow and controls, the logic design,
      and the physical implementation
  targets:
  - evidence_id: evidence-f997d3883be5
    source_id: ddca-lecture8-isa-ii
  - evidence_id: evidence-26b01009ad0d
    source_id: ddca-lecture8-isa-ii
- claim: 微架构是 ISA 的具体实现，描述如何实际执行指令；可在遵循 ISA 语义的前提下乱序执行，同时把指令结果按 ISA 规定的顺序呈现给软件。
  claim_id: isa-vs-micro
  support: direct
  supporting_quotes:
  - evidence_id: evidence-934896f7d3b4
    exact: |-
      Microarchitecture: How the underlying implementation
      actually executes instructions
  - evidence_id: evidence-0fcb148be49a
    exact: |-
      Microarchitecture can execute instructions in any order as long
      as it obeys the semantics specified by the ISA when making the
      instruction results visible to software
  targets:
  - evidence_id: evidence-934896f7d3b4
    source_id: ddca-lecture9a-isa-microarchitecture
  - evidence_id: evidence-0fcb148be49a
    source_id: ddca-lecture9a-isa-microarchitecture
- claim: 同一 ISA 可以有多个不同的微架构实现。
  claim_id: same-isa-implementations
  support: direct
  supporting_quotes:
  - evidence_id: evidence-b1430ecb4f5d
    exact: There can be many implementations of the same ISA
  targets:
  - evidence_id: evidence-b1430ecb4f5d
    source_id: ddca-lecture9a-isa-microarchitecture
- claim: 典型 RISC 倾向采用简单编码和 load/store，典型 CISC 倾向采用复杂或变长编码并可在单条指令内执行多个操作。
  claim_id: risc-cisc-tendencies
  support: direct
  supporting_quotes:
  - evidence_id: evidence-a8d12c44797d
    exact: RISC uses a small set of simple, fixed-length instructions and follows
      a load/store approach, enabling efficient and fast execution.
  - evidence_id: evidence-fc615f4beb99
    exact: CISC uses a larger set of complex, variable-length instructions that can
      perform multiple operations, often requiring multiple clock cycles.
  targets:
  - evidence_id: evidence-a8d12c44797d
    source_id: risc-cisc
  - evidence_id: evidence-fc615f4beb99
    source_id: risc-cisc
- claim: GPU 也可以拥有 ISA；NVIDIA PTX 是面向 GPU 的虚拟机和 ISA，并可翻译为目标硬件指令集。
  claim_id: gpu-isa
  support: direct
  supporting_quotes:
  - evidence_id: evidence-0825f3e4aba0
    exact: This document describes PTX, a low-level parallel thread execution virtual machine and instruction set architecture (ISA). PTX exposes the GPU as a data-parallel computing device.
  - evidence_id: evidence-381ecdafff03
    exact: PTX programs are translated at install time to the target hardware instruction set.
  targets:
  - evidence_id: evidence-0825f3e4aba0
    source_id: nvidia-ptx-isa
  - evidence_id: evidence-381ecdafff03
    source_id: nvidia-ptx-isa
- claim: Arm AArch64 状态使用固定长度的 A64 指令集，指令编码为 32 位。
  claim_id: arm-a64-encoding
  support: direct
  supporting_quotes:
  - evidence_id: evidence-457f06b7cbd6
    exact: AArch64 state supports a single instruction set, called A64. This is a fixed-length instruction set that uses 32-bit instruction encodings.
  targets:
  - evidence_id: evidence-457f06b7cbd6
    source_id: arm-ddi0487-instruction-sets
- claim: AArch64 的 R0-R30 是 31 个通用寄存器，分别可按 X0-X30 或 W0-W30 访问；SP 与 PC 是独立的架构状态。
  claim_id: arm-aarch64-registers
  support: direct
  supporting_quotes:
  - evidence_id: evidence-bac48d53df0d
    exact: 31 general-purpose registers, R0 to R30.
  - evidence_id: evidence-3523e066d483
    exact: A 64-bit general-purpose register named X0 to X30.
  - evidence_id: evidence-d02733c9167f
    exact: A 32-bit general-purpose register named W0 to W30.
  - evidence_id: evidence-66da003c916a
    exact: A 64-bit dedicated Stack Pointer register.
  - evidence_id: evidence-6d0028ea3af7
    exact: A 64-bit Program Counter holding the address of the current instruction.
  targets:
  - evidence_id: evidence-bac48d53df0d
    source_id: arm-ddi0487-aarch64-registers
  - evidence_id: evidence-3523e066d483
    source_id: arm-ddi0487-aarch64-registers
  - evidence_id: evidence-d02733c9167f
    source_id: arm-ddi0487-aarch64-registers
  - evidence_id: evidence-66da003c916a
    source_id: arm-ddi0487-aarch64-registers
  - evidence_id: evidence-6d0028ea3af7
    source_id: arm-ddi0487-aarch64-registers
- claim: Arm 内存模型中的 Shareability 属性规定硬件需要在一组观察者之间保证的内存一致性程度。
  claim_id: arm-memory-coherency
  support: direct
  supporting_quotes:
  - evidence_id: evidence-37ff700ccf96
    exact: In the Arm memory model, the Shareability memory attribute indicates the degree to which hardware must ensure memory coherency between a set of observers.
  targets:
  - evidence_id: evidence-37ff700ccf96
    source_id: arm-ddi0487-memory-model
id: isa-and-microarchitecture
kind: knowledge
publication_scope: public
related: []
sources:
- isa-microarchitecture
- risc-cisc
- ddca-spring2026-readings
- ddca-lecture8-isa-ii
- ddca-lecture9a-isa-microarchitecture
- arm-ddi0487-instruction-sets
- arm-ddi0487-aarch64-registers
- arm-ddi0487-memory-model
- nvidia-ptx-isa
status: published
tags:
- computer-architecture
- isa
- multicore
title: ISA 与微架构：处理器体系结构的三层拆分
updated_at: '2026-09-03'
---
# ISA 与微架构：处理器体系结构的三层拆分

## 一句话结论

在本文的工程分层中，处理器体系结构 = ISA + 微架构 + 电路/物理实现。ISA 不是 CPU 独有的“语言”：CPU、GPU、DSP 以及部分 NPU/TPU 等可编程执行设备都可能定义自己的指令集或命令集。ISA 是软件与执行设备之间的抽象接口；微架构是在约束和目标下实现该接口的内部组织，同一 ISA 可以对应多个不同实现。

## 核心概念

- **ISA**：执行设备对软件暴露的指令、寄存器、数据类型、寻址方式、内存组织、异常/特权和可见语义等约定。这里的“设备”不局限于 CPU。
- **RISC/CISC**：描述指令集设计的常见取舍。load/store、编码长度和操作数是否可直接来自内存是典型观察维度，但不能用几条标签给所有 ISA 贴绝对结论。
- **微架构**：ISA 的具体实现，例如取指/译码、发射与调度、执行单元、寄存器文件、流水线、缓存/预取、片上互连、分支预测和功耗控制。GPU 的线程束调度、SIMT 执行和共享内存组织也属于其微架构层。
- **硬件实现**：RTL、门级逻辑、存储器阵列、时钟/电源和物理版图等更底层实现；它们通常不直接成为软件可见的 ISA 约定。

## 工作机制

1. **抽象与实现分离**：ISA 描述程序可见状态和指令语义；微架构可以用流水线、乱序执行、投机和隐藏状态改变内部执行顺序，但必须保持 ISA 规定的可见结果。
2. **同 ISA 的兼容性有边界**：相同 ISA 是重要前提，但二进制还可能依赖可选扩展、ABI、操作系统、运行时和设备特性，不能据此保证“任意同 ISA 设备”都能直接运行。
3. **RISC/CISC 是倾向而非性能定理**：固定长度不等于每条指令一个周期；CPI、延迟和吞吐由具体指令、实现和工作负载共同决定。
4. **访存方式只是一个维度**：典型 RISC 多采用 load/store，典型 CISC 有更多带内存操作数的指令，但现代 ISA 常包含扩展、压缩编码和向量/矩阵指令，边界并不绝对。
5. **性能是跨层结果**：ISA 会影响指令数、编码密度、向量/矩阵表达能力和编译器可用的优化；微架构与内存系统决定这些指令如何被实际执行。
6. **缓存一致性不能简单归入某一层**：缓存容量、相联度、替换和预取通常是微架构策略；内存顺序、可观察性、Shareability 和一致性保证可能属于 ISA/系统架构可见契约。

## 示例或代码

- **同 ISA 不同微架构**：同一 ISA 可以由不同处理器实现；比较性能时仍需检查实现是否支持所需扩展、ABI 和操作系统。
- **Armv8-A 示例**：AArch64 状态使用 A64，Arm 官方手册定义其为 32 位固定长度编码；AArch64 有 31 个通用寄存器 X0-X30/W0-W30，SP 和 PC 是独立架构状态。
- **GPU 示例**：NVIDIA PTX 是面向 GPU 的虚拟 ISA。CUDA/C++ 等高层语言可生成 PTX，PTX 再被翻译到目标 GPU 的硬件指令集；因此 CUDA 编程模型、PTX 虚拟 ISA 和 GPU 原生 ISA 不是同一层。

## 常见误区

- **把 ISA 优劣等同于性能优劣**：不能脱离编译器、扩展、微架构、内存系统和工作负载比较 ISA；“一条指令”也不等于固定延迟。
- **把所有加速器都当成 CPU**：GPU 有自己的线程/数据并行 ISA；NPU/TPU 可能公开 ISA，也可能只公开编译器、运行时或命令接口。除非厂商文档明确说明，不要把 CUDA、XLA、MLIR 或某个 API 自动称为硬件 ISA。
- **认为缓存策略完全不属于体系结构**：实现策略和架构保证要分开。缓存层级/替换通常不直接暴露给软件，而内存顺序和一致性语义可能会暴露。
- **认为多核就是多个独立 CPU**：多核共享内存时，架构规定的可见性与实现中的缓存一致性协议共同决定软件观察到的结果和代价。

## 证据映射

- ISA/微架构的接口与分离：ETH Zürich DDCA L8/L9a 讲义，尤其是“ISA 是软件命令与硬件执行之间的接口”以及“微架构是 ISA 的具体实现”。
- ARMv8-A 的 A64 编码、AArch64 寄存器和内存模型：Arm Architecture Reference Manual for A-profile architecture（DDI0487，官方文档服务的具体章节快照）。
- GPU ISA：NVIDIA PTX ISA 9.3 官方文档；它明确区分 PTX 虚拟 ISA 与目标 GPU 硬件指令集。
- ETH Zürich `readings` 页面是 DDCA 课程资料索引，`schedule` 页面是讲义下载入口；二者用于发现和定位资料，课程日程本身不承担技术 claim 的证据责任。
- RISC/CISC 的对照仍保留原教育性 source，但正文已把“定长、单周期、寄存器多少、代码大小”等改成常见倾向，避免把教学简化当成 ISA 的硬性定义。

## 待验证项

- 本页待验证项已全部收口，验证结论已并入正文（证据映射/核心概念），无遗留。

## 关联知识

- CPU/GPU 指令执行与三类冒险
- 程序性能的分析与测量
- LLVM 自动向量化


## 处理器之外的 ISA

ISA 的关键不是“是不是 CPU”，而是是否存在一组由执行设备解释、并作为软件/编译器目标的指令与状态约定。

- **CPU**：x86-64、Arm A64、RISC-V 等，通常直接承载操作系统和应用程序的指令执行。
- **GPU**：NVIDIA PTX 是虚拟 ISA，目标 GPU 还会执行厂商相关的原生硬件 ISA；GPU ISA 的线程、线程束/SIMT、地址空间和同步语义与 CPU ISA 有明显不同。
- **DSP/FPGA/AI 加速器**：可以有面向向量、信号处理、矩阵或张量操作的 ISA，也可以只提供微码、命令流或专用编译器接口。NPU/TPU 是否存在公开、稳定、可由用户直接编程的 ISA，要以具体产品文档为准。

因此，“ISA 是 CPU 的语言”可以作为入门类比，但作为定义应改为“ISA 是处理器或可编程执行设备的软件-硬件接口”。


## 详细章节

### 多核软件设计

#### 现代处理器基本架构

$$
体系结构 = ISA + 微架构 + 硬件实现
$$

##### 体系结构

* ISA
    * CISC
    * RISC
* 组成（微架构）
    * CPU核
        * 流水线
        * 超标量
        * 乱序执行
        * 分支预测
        * 多核/多线程
    * cache子系统
        * 地址映射策略
        * 替换策略
        * 一致性策略
* 硬件

#### ISA

ISA（instruction set architecture）是执行设备对软件暴露的抽象接口，规定指令、寄存器、数据类型、寻址方式、内存组织以及异常和特权等可观察约定。执行 ISA 所定义指令的设备称为该 ISA 的一种实现；这里的设备不只包括 CPU，也可以包括 GPU、DSP 和其他可编程加速器。

##### 指令集分类

* 精简指令集（RISC）
    * 以早期 MIPS、经典 ARM 等为代表，倾向使用较简单、规则的指令，并通过多条指令组合完成复杂功能
* 复杂指令集（CISC）
    * 以 x86 为代表，倾向提供更复杂的指令、寻址方式和内存操作数

RISC 和 CISC 是描述设计取舍的常用术语，不是覆盖所有现代 ISA 的严格二分。具体 ISA 可能同时包含固定长度、变长、压缩、向量或矩阵等不同形式的扩展。

| 观察维度 | 典型 CISC 倾向 | 典型 RISC 倾向 | 注意事项 |
| --- | --- | --- | --- |
| 指令编码复杂度 | 可能更复杂 | 通常更规则 | 具体 ISA 可能有多种编码格式 |
| 可访存指令类型 | 可能有较多带内存操作数的指令 | 通常采用 load/store | 这是设计维度，不是唯一分类标准 |
| 指令字长 | 常见变长 | 常见固定或少数长度 | RISC 不必然只有 16/32 位 |
| 指令执行时间 | 不固定 | 不由 RISC 标签保证固定 | 延迟、吞吐和 CPI 依赖具体指令及微架构 |
| 通用寄存器数量 | 历史上常见较少 | 历史上常见较多 | 不是 RISC/CISC 的定义条件 |
| 目标代码大小 | 历史上可能较小 | 历史上可能较大 | 受编译器、编码密度和扩展影响 |

##### ISA-RISC（Armv8-A）

* Armv8-A 定义 AArch64 和 AArch32 两种执行状态。AArch64 使用 A64 指令集；AArch32 使用 A32 和 T32 指令集，具体可用状态受处理器实现和配置影响。
* Arm 官方手册定义 A64 为固定长度指令集，使用 32 位指令编码。固定编码有利于取指和译码规则化，但不意味着每条指令固定一个时钟周期。
* A64 指令集包含 31 个通用寄存器 X0-X30；同一寄存器的低 32 位分别以 W0-W30 访问。SP 和 PC 是独立的架构状态，不应把它们计作第 32、33 个通用寄存器。
* 常见指令类别包括：
    * 数据处理：数据传输、算术逻辑运算、比较
    * 浮点和 SIMD/向量数据处理
    * load/store
    * branch、exception、system
    * 由具体架构扩展提供的 SVE/SME 等向量和矩阵指令

###### 寄存器文件描述

####### 通用寄存器

* 在 AArch64 状态，通用寄存器为 X0-X30，宽度为 64 位；W0-W30 是对应 X 寄存器的低 32 位视图。
* 在 AArch32 状态，通用寄存器通常以 R0-R15 表示，其中 R13 通常作为栈指针、R14 作为链接寄存器、R15 作为程序计数器；不能用 AArch64 的 W0-W30 描述 AArch32 通用寄存器。

####### 特殊寄存器和架构状态

* Stack Pointer register（SP）
    * AArch64 使用独立的 64 位 SP，低 32 位可通过 WSP 访问；AArch32 通常使用 R13 作为栈指针
* Program Counter（PC）
    * 保存当前指令地址相关的程序计数状态；AArch64 的 PC 不是 X0-X30 中的通用寄存器
* 32 个 SIMD/FP registers（V0-V31）
    * 用于 SIMD 和浮点操作；具体宽度和可用扩展由架构状态定义
* Process state（PSTATE）
    * 保存条件标志、异常屏蔽、当前执行状态等处理器状态；不要把 CurrentEL 简化成“所有指令都通过 PSTATE 反馈”的接口
* System registers
    * 为执行控制、状态管理、异常、虚拟化和系统配置提供支持
* Performance Monitors
    * 通过相关系统寄存器提供周期计数器和实现相关的事件计数器；计数器数量和事件集合应以具体实现文档为准

###### 寻址模式

不同 ISA 对寻址模式的命名不完全相同，Arm A64 中常见形式包括：

* 立即数寻址
* 寄存器寻址
* 基址加偏移寻址
* 前变址和后变址
* 寄存器移位或扩展后参与地址计算
* PC 相对寻址

“堆栈寻址”和“多寄存器寻址”在部分架构或指令扩展中存在，但不应直接当作所有 ISA 的统一基础寻址模式。

###### 异常级别

Armv8-A 的 AArch64 执行环境通常使用 EL0 到 EL3 四个异常级别；异常级别编号越高，通常代表更高的架构特权，但具体能力还受安全状态、实现和系统配置影响。

* EL0：非特权应用执行
* EL1：通常用于操作系统内核
* EL2：通常用于虚拟化管理
* EL3：通常用于安全监控和安全状态切换

##### ISA、微架构与缓存

* ISA 定义软件可观察的状态转换、内存访问语义、异常和同步约定。
* 微架构选择单周期、多周期、流水线、乱序、超标量、缓存层级、替换/预取和调度策略等内部实现。
* 多核系统中，缓存一致性协议、互连和缓存层级是实现的重要部分；但软件可观察的内存顺序、一致性和 Shareability 保证可能由 ISA/系统架构定义。

##### GPU/NPU/TPU 的层次

* GPU 可以有自己的 ISA。以 NVIDIA 为例，PTX 是面向 GPU 的虚拟 ISA，编译器或运行时再把它翻译到目标 GPU 的硬件指令集。
* CUDA 是编程模型和 API；PTX 是虚拟 ISA；GPU 原生机器指令又是另一层，三者不能互换。
* NPU/TPU 可能有公开 ISA、厂商私有指令、微码、命令流或仅面向编译器的接口。讨论具体芯片时，应明确是在谈用户编程接口、编译器 IR、虚拟 ISA、硬件 ISA 还是微架构。

#### CPU核微架构

##### 流水线

###### 流水线基本概念

* 将一条指令处理流程拆分成若干个stage，每个stage完成一个工作
* 流水线技术不能缩短单条指令执行时间，但通过重叠执行，提升并行度，可以提升整个系统吞吐量



###### Stage

* IF：取指阶段
* DE：译码阶段
* EX：执行，完成计算任务
* MEM：存储器访问（仅Load和Store）
* WB：结果写回通用寄存器



###### 流水线冒险

* 流水线冒险（pipeline hazards）
    * 阻止下一条指令在下一个cycle开始执行
* 结构冒险（structural hazards）
    * 当两条指令同时需要相同的硬件资源时，就会发生结构冒险
* 数据冒险（data hazards）
    * 当前指令需要等待之前指令完成，即依赖先前指令产生的结果（数据）值
* 控制冒险（control hazards）
    * 根据之前指令决定下一步需要执行的指令引起延时，即依赖关系是如何确定下一条指令地址（branches, jumps）



##### 超标量处理

###### 基本概念

*   一个时钟周期执行一条以上指令
*  一般有多个执行单元，如算术逻辑单元、乘法器等
*   由硬件在执行时动态完成指令打包或冒险处理
*   多数超标量处理器都结合动态流水线调度技术，通过指令相关性检测、动态分支预测等手段乱序执行



##### 乱序机制

###### 乱序机制主要思想

*   暂停指令的后续指令继续处理



###### 乱序机制基本概念

*   允许指令乱序发射，乱序执行
    * Issue stage具有buffer可以缓存多条待发射指令
    *   当待发射指令源操作数就绪后就发射到后续的执行单元



###### Precise Exception problems

Exception or Interrupt must appear between 2 instructions (la and la+ 1)

*   The effect of all instructions up to and including la is visible to software

*   No effect of any instruction after la can take place



###### 解决方案

指令顺序分发，乱序发射，乱序执行，顺序提交

* Out-of-order issue

* In-order commit

* Introduce Re-Order Buffers(ROB)



##### 分支预测

###### 基本概念

*   频繁出现转移指令会产生控制冒险，而影响性能
*   深流水处理器中，在下一PC计算和最终转移结果计算之间有10个流水级以上



###### 预测方案

*   软件方法：消除转移，循环展开/较小的转移确定时间，指令调度尽早计算转移条件
*   硬件方法：延迟槽/转移预测



###### 分支预测内容

*   预测方向（taken/not taken 转移历史表BHT）
*   预测内容（跳转目标地址 转移目标缓存器BTB）



###### 错误预测恢复机制

* 将Complete和Commit分离：流水线恢复到转移指令后正确状态



##### 矢量处理DLP

###### 基本概念

* 又称数组处理，是一种实现直接操作一维数组指令集
* 一条矢量指令可以处理N个（N对）相同类型操作数



##### 多核多线程TLP

###### 基本概念

利用线程级并行TLP提升单个处理器利用率



###### 分类

* 交叉多线程：交错发出不同线程的多条指令，也称时间多线程。可以分为细颗粒度、粗颗粒度多线程，取决于线程交错换频率
* 多核处理器（CMP）：将两个或多个处理器集成到一个芯片，每个处理器独立执行线程
* 同时多线程（SMT）：在一个周期中发出多个线程的多条指令



#### Cache子系统

理解Cache子系统的必要性及意义需要解决以下问题：

*   为什么需要Cache子系統
*   Cache子系统基本架构
*   Cache系统如何建立地址映射规则
* CPU核如何从cache中获取数据
*   Cache系统如何替换数据
* Cache数据写回策略
* 多核系统如何保证cache一致性



##### 基本结构

###### Memory Wall

限制处理器发挥性能的主要瓶颈
处理器一个cycle通常允许并行执行4~8条指令，一次访存miss到DDR可能造成150~300cycles的阻塞



###### Cache

利用程序局部性原理减轻Memory Wall影响

*  时间局部性：如果某条指令被执行，则不久之后该指令可能再次被执行：如果某数据被访问，则不久之后该数据可能再次被访问
*  空间局部性：是指一旦程序访问了某个存储单元，则不久之后，其附近的存储单元也将被访问



##### 如何建立地址映射关系

* 全相联
* 直接相联
* 多路组相联



##### 获取数据

CPU向cache获取数据的过程就是查找数据所在cacheline是否在N-way set-associative cache中存在的过程
对于一个变量，它的地址可以被拆解为3部分：

*  Block offset：一个block可由m位地址长度进行编址，这个m位低地址就是block offset。由于cache 是使用block为基本单位与DDR交换数据，在查找过程中无需block offset的参与
* Set Index： 一个way中通常含有2^k条cacheline，则变量所在block可以用k位地址在该way里通过直接映射的方式确定一个set位置
*  Tag：得到了set位置，就可以用tag在每个way上与相应的tag进行比较，选取其中的cacheline输出数据



##### 替换数据

常用Cache替换算法

* 随机替换（Random）：利用生成随机数地方法随机替换cacheline
* 轮转替换（Round-Robin）：利用计数器轮转替换cacheline
* 最近最少使用（LRU，Least Recently Used）：使用一个链表，把被访问的数据按访问时间顺序加入一个链表头，发生替换时总是在链表尾进行摘链，把访问时间最旧的替换掉；这种算法只是理想状态的算法，在多路组相联时很难实现
    * PS：设计时，经常使用PLRU（Pseudo-LRU）替代LRU算法以简化设计难度
* 最近使用（MRU，Most Recently Used）：在发生替换的时候，把访问时间最新的cacheline替换掉，该算法在一个cacheline保留越久越可能被再次访问的场景效果较好
* 最不经常使用（LFU，Least Frequently Used）：统计每个cacheline使用频度，替换掉访问频度最低的一项



##### 数据写回

Cache子系统缓存CPU读取的数据/指令，同时也缓存CPU写入内存的数据

*  CPU读取数据/指令时，cache子系统只是简单的在cache内留一份拷贝
*  CPU写入数据时，会有两种不同的处理方法：write-through和write-back



##### 多核系统的Cache一致性

###### MOESI

* Modified：一个cacheline如果拥有最新的正确数据就可被标记为Modified状态，这时内存中该数据的拷贝是未被更新的，并且其他的cacheline不能包含该数据
* Owned：一个cacheline如果拥有最新的正确数据可以被标记为Owned状态，其他拥有该数据拷贝的cacheline只能处于Shared状态
*   Exclusive：如果一个cacheline处于Exclusive状态，表明该cacheline以及内存中的数据拷贝都是处于最新状态，并且没有其他cacheline拥有该数据拷贝
*   Shared：一个处于Shared状态的cacheline拥有最新的数据拷贝，系统中其他cacheline也可处于shared状态并拥有最新的数据拷贝
* Invalid：处于Invalid状态的cacheline不持有任何有效数据



#### 基于处理器微架构的性能分析

##### Top-Down分析方法

* 微架构的Top-Down分析方法由intel公司的Ahmad Yasin于2014年提出
* 在Top-Down分析模型出现之前，一个很大的挑战就是：CPU会产生数百个PMU事件，这些事件与CPU性能或相关或不相关，面对如此多离散的PMU事件，如何快速准确的找到系统的瓶颈
* Top-down模型是一个结构化框架，它是一个树形结构，权重会分配给树中的节点，目的就是为了集中分析主要瓶颈



##### PMU数据分析

PMU: Performance Monitor Unit，性能监控单元
对于一段代码流程，可通过PMU采集的性能指标数据：

*   总耗时Cycle数
*   指令数
*   由于没有数据导致没有指令完成的Cycle数

对于采集数据的分析方法：
* 数据依赖
* Cache Miss
* 分支错误
* TLB Miss



##### ESL数据分析

* ESL （Electronic System Level Design）：电子系统级设计，是一套能够以紧耦合方式开发、优化和验证复杂SoC系统架构和嵌入式软件的方法论
*   Trace是一种硬件辅助观察处理器指定时间内PC跳转轨迹的工具



#### 基于处理器微架构的软件调优

##### 影响微处理器架构的性能因素

$$
CPU处理时间=指令数*平均每条指令所用时钟周期数*每个时钟周期的时间
$$



##### 性能调优方法

*    减少指令数
    * 增强处理局部化
    * 多核软件架构优化
    * 软硬件协同
*   减少平均每条指令所用时钟周期数，即提升IPC
    * 增加指令并发度
    * 使用矢量处理
    * 减少数据依赖



##### 增强局部化

* 利用cache提高执行效率
    * 处理单元访问cache效率最高，速度最快，代码、数据先从memory读到cache，执行到对应代码、数据时，再由处理器执行，可以提高执行效率
    * 代码有分段，例如判断引入不同分支的处理函数，到判断时处理器无法预测判断分支走向，如果判断后的分支函数不在cache内，需要从memory内读取再访问效率低，称为misses；反之，如果在cache内，称为hits
    * 数据访问同理
* 函数重排，提高函数cache命中率
    * 明确执行函数走向分支，可以按函数执行走向将函数代码段排序，提高命中率
* 拆分循环体内容，提升cache利用率
* 结构体重排，提高数据的cache命中率
* 循环展开，增加指令运行的并行度

    * 循环unroll：循环迭代间并行度挖掘技术

    * 循环unroll就是把循环展开n次，相应的循环次数变为原来的[1/n]次及对应的remainder

    * 循环unroll将原本的在不同迭代体中的指令并行到同一次迭代体中



##### 多核并行化

相对单核处理器，任务在多个核上并行执行，效率更高



###### 多核并行引入的问题

* 资源互斥
* 并行度
* 任务调度
* 任务合理拆分



###### 多核软件架构优化

* 通信消息机制优化
  * 核间通信走消息队列，可以省去硬件队列、os响应时间，效率更高
* 任务合理调度



###### 辅助处理器投机

* Likely/unlikely分支预测
  * 分支预测：通过likely和unlikely标识，分支重排让代码更紧凑
  * 告诉编译器高概率的分支，被一个条件触发的不同函数，将它们紧凑排列，使cache连续读取，提高cache命中率
* 指令/数据预取
  * 找到后续流程用到的代码、数据，超前读取到cache内，待流程走到对应代码、数据时，可以直接从cache访问。



###### 使用矢量处理

* 矢量处理：将多个标量放到一个矢量内，一次指令调用可以完成矢量内多个标量的运算
*  可将多个标量运算，合并成一次矢量运算，提高执行效率
