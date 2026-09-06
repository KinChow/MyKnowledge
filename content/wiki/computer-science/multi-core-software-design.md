---
aliases: []
confidentiality: public
domain: computer-science
evidence:
- claim: '- Superscalar processors enable CPI < 1 (i.e., IPC > 1) by executing multiple
    instructions in parallel'
  claim_id: multi-core-software-design-audit-1
  support: direct
  supporting_quotes:
  - evidence_id: evidence-098639dc3686
    exact: '- Superscalar processors enable CPI < 1 (i.e., IPC > 1) by executing multiple
      instructions in parallel'
  targets:
  - evidence_id: evidence-098639dc3686
    source_id: cornell-superscalar-execution
id: multi-core-software-design
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- cornell-superscalar-execution
- multi-core-software-design-notes
- working-computer-science-multi-core-software-design
status: published
tags:
- multi-core
- isa
- microarchitecture
- cache
- performance
- cpp
title: 多核软件设计
updated_at: '2026-09-06'
---
# 多核软件设计

## 一句话结论

多核软件设计建立在"体系结构 = ISA + 微架构 + 硬件实现"的基础上：理解指令集（ISA）、CPU 核微架构（流水线/超标量/乱序/分支预测/多线程）与 Cache 子系统（地址映射/替换/写回/一致性），再通过 Top-Down 分析、PMU/ESL 数据分析找到性能瓶颈，最后用减少指令数、提升 IPC（如增强局部化、多核并行化、矢量处理）等手段进行软件调优，才能充分发挥多核处理器的性能。

## 核心概念

- **体系结构 = ISA + 微架构 + 硬件实现**。
- **ISA（指令集架构）**：计算机的抽象模式，执行 ISA 所定义指令的设备称为其实现；分为精简指令集（RISC，MIPS/ARM）与复杂指令集（CISC，x86）。
- **CPU 核微架构**：流水线、超标量、乱序执行、分支预测、多核/多线程。
- **Cache 子系统**：地址映射策略、替换策略、一致性策略。
- **性能模型**：CPU 处理时间 = 指令数 × 平均每条指令所用时钟周期数 × 每个时钟周期的时间。
- **性能分析**：Top-Down 分析、PMU（Performance Monitor Unit）数据分析、ESL（Electronic System Level Design）数据分析。

## 工作机制

### ISA 与指令集分类

| 维度 | CISC（复杂指令集） | RISC（精简指令集） |
| --- | --- | --- |
| 指令编码复杂度 | 复杂 | 简单 |
| 可访存指令类型 | 寄存器-存储器结构，大量不同类型指令可访存 | load-store 类型，只允许通过 load/store 访问存储器 |
| 指令字长 | 不固定 | 固定（16 或 32 bits） |
| 指令执行时间 | 不固定 | ≈1 cycle |
| 通用寄存器数量 | 较少 | 较多 |
| 目标代码 | 小 | 大 |

以 ARMv8（RISC）为例：定义 AArch64 与 AArch32 两种执行状态；A64 指令集含 31 个通用寄存器 X0~X30 及 SP、PC；支持数据处理、load/store、Branch/exception/system、协处理器及杂项指令；有 EL0~EL3 四个异常级别。

### CPU 核微架构

- **流水线**：将指令处理拆成多个 stage（IF 取指、DE 译码、EX 执行、MEM 访存、WB 写回），不能缩短单条指令时间但可提升吞吐量；需处理结构/数据/控制三类冒险。
- **超标量**：一个时钟周期执行一条以上指令，由硬件动态完成指令打包或冒险处理，常结合动态流水线调度与乱序执行。
- **乱序执行**：指令乱序发射、乱序执行、顺序提交，通过 Re-Order Buffers（ROB）保证精确异常。
- **分支预测**：软件方法（消除转移、循环展开、指令调度）与硬件方法（延迟槽/转移预测），预测方向（BHT）与内容（BTB）。
- **多核多线程（TLP）**：交叉多线程、多核处理器（CMP）、同时多线程（SMT）。

### Cache 子系统

- **Memory Wall**：访存 miss 到 DDR 可能造成 150~300 cycles 阻塞，Cache 利用局部性（时间/空间局部性）缓解。
- **地址映射**：全相联、直接相联、多路组相联；地址拆解为 Block offset、Set Index、Tag 三部分。
- **替换算法**：随机、轮转、LRU（常用 PLRU 简化）、MRU、LFU。
- **写回策略**：write-through 与 write-back。
- **多核一致性**：MOESI（Modified/Owned/Exclusive/Shared/Invalid）。

## 示例或代码

性能调优公式：`CPU处理时间 = 指令数 * 平均每条指令所用时钟周期数 * 每个时钟周期的时间`

- **减少指令数**：增强处理局部化、多核软件架构优化、软硬件协同。
- **减少平均每条指令所用时钟周期数（提升 IPC）**：增加指令并发度、使用矢量处理、减少数据依赖。
- **增强局部化**：函数重排提高 cache 命中率、拆分循环体提升 cache 利用率、结构体重排、循环展开（unroll）增加指令并行度。
- **多核并行化**：核间通信走消息队列（省去硬件队列、OS 响应时间）；任务合理调度；likely/unlikely 分支预测 + 指令/数据预取。
- **矢量处理**：将多个标量放到一个矢量内，一次指令调用完成多个标量的运算。

## 常见误区

- **把"多核并行"理解为必然加速**：多核并行引入资源互斥、并行度、任务调度、任务合理拆分等问题，不是所有流程都能并行，且可能带来额外系统开销与资源争用。
- **忽略 Cache 层的影响**：性能瓶颈常在 Memory Wall（访存延迟），只优化指令数而忽视数据局部化与 cache 命中率，收益有限。
- **把超标量与多核混为一谈**：超标量是单核内一个周期执行多条指令（ILP），多核/多线程是线程级并行（TLP），机制不同。
- **只采集 PMU 事件而不做结构化分析**：CPU 产生数百个 PMU 事件，需用 Top-Down 等结构化框架定位主要瓶颈。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| multi-core-software-design-audit-1 | cornell-superscalar-execution | 超标量处理器通过并行执行多条指令使 CPI < 1（即 IPC > 1） |

## 待验证项

无。

## 关联知识

- [[common-performance-design-patterns]] —— 性能设计模式（并行处理、去锁设计等）。
- [[isa-and-microarchitecture]] —— ISA 与微架构专题。
- [[cpu-pipeline-and-hazards]] —— 流水线与冒险。
- [[cpu-cache-optimization]] —— cache 优化。
- [[architecture-and-organization]] —— 计算机体系结构。
- [[loop-optimization]] —— 循环优化与展开。
- [[arm-neon]] —— ARM SIMD/矢量处理（NEON）。
- [[compilation-and-runtime-optimization]] —— 编译期优化（likely/unlikely、循环展开）。

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

ISA（instruction set architecture）是计算机的抽象模式，执行ISA所定义指令的设备称为其实现



##### 指令集分类

* 精简指令集（RISC）
    * 以MIPS、ARM为代表，一条指令完成一个基本动作，多条指令组合完成一个复杂功能
* 复杂指令集（CISC）
    * 以x86为代表，一条指令完成一个复杂功能



|                | 复杂指令集（CISC）                        | 精简指令集（RISC）                                 |
| -------------- | ----------------------------------------- | -------------------------------------------------- |
| 指令编码复杂度 | 复杂                                      | 简单                                               |
| 可访存指令类型 | 寄存器-存储器结构，大量不同类型指令可访存 | load-store类型，只允许通过load-store指令访问存储器 |
| 指令字长       | 不固定                                    | 固定（16或32 bits）                                |
| 指令执行时间   | 不固定                                    | ≈1cycle                                            |
| 通用寄存器数量 | 较少                                      | 较多                                               |
| 目标代码       | 小                                        | 大                                                 |



##### ISA-RISC（ARMv8）

*  ARMV8架构定义了AArch64和AArch32两种执行状态，支持A64和T32、A32指令集
*   提供32bit固定长度指令码
*  A64指令集包含31个通用寄存器X0~X30，以及SP（x31）和PC，共33个。其中W0~W31分别是X0~X31的低32位
*   支持指令类型
    * 数据处理（数据传输、算术逻辑运算、比较、浮点运算、vector data等）
    * load/store
    * Branch/exception/system
    * 协处理器指令
    * 杂项（软中断、状态寄存器读写等）



###### 寄存器文件描述

###### 通用寄存器

ARMv8提供31个通用寄存器R0-R30：

*   在AArch64架构，通用寄存器X0-X30是64bit宽度
*   在AArch32架构，通用寄存器W0-W30是32bit宽度



###### 特殊寄存器

* Stack Pointer register (SP)
    * 指向当前栈指针，AArch64叫做SP，AArch32叫做WSP
* Program Counter (PC)
    * 指向当前指令的地址
* 32个SIMD&FP registers
    * SIMD操作
* Process state, PSTATE
    * 对进程状态信息的集合，包括如下寄存器，条件寄存器NZCV、异常屏蔽寄存器DAIF、SP选择寄存器SPSEL、异常等级寄存器
    * CurrentEL，所有指令集都可以通过PSTATE反馈状态
* System registers
    * 为执行控制、状态和一般系统配置提供支持
* Performance Monitors support
    * 64bit周期计算器
    * 最多支持32个implementation DEFINE事件计数器，定义在PMCR_EL0.N字段。
    * 系统寄存器对周期计数器和事件寄存器的访问以及相关控制



###### 寻址模式

* 立即数寻址
* 寄存器寻址
* 寄存器间接寻址
* 基址寻址
* 寄存器移位寻址
* 堆栈寻址
* 多寄存器寻址
* 相对寻址



###### 异常级别

ARMv8-A有四个异常级别，从EL0到EL3。对于异常级别ELn，整数n增加表示软件执行的特权权限变大了

* EL0 非特权执行（unprivileged execution）
* EL1 主要用于运行操作系统内核
* EL2 支持非安全操作的虚拟化
* EL3 支持安全状态和非安全状态之间的转换



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

*   为什么需要Cache子系统
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

* 随机替换（Random）：利用生成随机数的方法随机替换cacheline
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
