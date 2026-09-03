---
aliases:
- 程序性能的分析和测量
- 性能分析方法
confidentiality: public
domain: computer-science
evidence:
- claim: little 定律的等式为 l=λw：排队系统中顾客的时间平均数量等于到达率乘以平均逗留时间。
  claim_id: little-law
  support: direct
  supporting_quotes:
  - evidence_id: evidence-47e5f178256f
    exact: We consider here a famous and very useful law in queueing theory called
      Little's Law, also known as l = λw, which asserts that the time average number
      of customers in a queueing system, l, is equal to the rate at which customers
      arrive, λ, × the average sojourn time of a customer, w.
  targets:
  - evidence_id: evidence-47e5f178256f
    source_id: little-law-columbia
- claim: 概要形式以汇总的形式展示程序信息。
  claim_id: profile-form
  support: direct
  supporting_quotes:
  - evidence_id: evidence-f6c8afdf6614
    exact: Profilers provide a summary of execution statistics and/or events. They
      give an overview of the overall performance of the program, often broken down
      to the functions, loops or even user-specified sections.
  targets:
  - evidence_id: evidence-f6c8afdf6614
    source_id: osti-profiling-tracing
- claim: 分段查找通过二分定位（bisection）不断缩小范围，是定位性能回归或问题代码段的常用方法。
  claim_id: segmented-search
  support: direct
  supporting_quotes:
  - evidence_id: evidence-fb6d25a01405
    exact: 'The crucial task of localizing such regressions can be achieved

      using bisection, which attempts to find the bug-introducing commit using binary

      search. This approach is used extensively by many development teams, but it
      is'
  targets:
  - evidence_id: evidence-fb6d25a01405
    source_id: bisect-performance-regression
- claim: 事件记录形式（tracing）逐个记录每个事件，如函数的进入与退出。
  claim_id: trace-form
  support: direct
  supporting_quotes:
  - evidence_id: evidence-4321897985b6
    exact: Tracing is a profiling technique that captures specific program events,
      such as entering or exiting a function, every time they occur. This allows the
      collection of accurate profiling information about specific areas of the code.
  targets:
  - evidence_id: evidence-4321897985b6
    source_id: lumi-profiling-strategies
- claim: 快照形式（sampling）周期性对调用栈取快照，形成统计概况。
  claim_id: snapshot-form
  support: direct
  supporting_quotes:
  - evidence_id: evidence-5138110b0629
    exact: Sampling consists of taking regular snapshots of the application's call
      stack to create a statistical profile. This is a good option for low overhead
      profiling.
  targets:
  - evidence_id: evidence-5138110b0629
    source_id: lumi-profiling-strategies
- claim: 排队分析先定义系统（到达过程、服务过程、队列规则、服务台数），再收集到达率、服务时间与队列长度数据以理解系统行为。
  claim_id: wait-queue
  support: direct
  supporting_quotes:
  - evidence_id: evidence-8406af58cade
    exact: 'Steps to Use Queuing Theory

      1. Define the System: Identify the key components of the system, such as the
      arrival process, service process, queue discipline, and number of servers.

      2. Collect Data: Gather data on customer arrival rates, service times, and queue
      lengths to understand the system''s behavior.'
  targets:
  - evidence_id: evidence-8406af58cade
    source_id: queueing-theory-gfg
id: program-performance-analysis
kind: knowledge
publication_scope: public
related: []
sources:
- program-performance-analysis-notes
- little-law-columbia
- osti-profiling-tracing
- lumi-profiling-strategies
- bisect-performance-regression
- queueing-theory-gfg
status: published
tags:
- performance
- profiling
- measurement
title: 程序性能的分析与测量：视角、方法与信息形式
updated_at: '2026-09-03'
---
# 程序性能的分析与测量：视角、方法与信息形式

## 一句话结论

性能工作分两步：先用视角与方法把瓶颈**大致定位**（分段查找、排队分析、little 定律都属于估算/建模手段），再用测量拿到**定量证据**——概要形式看趋势、事件记录形式看细节、快照形式看瞬时状态。

## 核心概念

- **硬件视角 / 软件视角**：硬件视角从处理器、内存、磁盘、网卡、总线及互联的资源配置与占用出发；软件视角从程序出发，通过算法与实现调整改善性能。
- **分段查找（bisection）**：用二分不断缩小范围，定位性能回归或问题代码段——通用定位手法，可对应调试/性能工程中的二分定位。
- **排队分析**：把程序执行抽象为排队系统，通过定义系统、收集到达率/服务时间/队列长度数据、选取模型，分析平均等待时间、队列长度与利用率。
- **little 定律**：`l=λw`——排队系统中顾客的时间平均数量等于到达率乘以平均逗留时间，用于量级校验。
- **信息形式**：概要形式（汇总/平均，看趋势）、事件记录形式（逐个记录事件，看细节）、快照形式（周期性取当前状态，定位瞬时问题）。

## 工作机制

1. 先用视角与方法**估算**瓶颈方位——这一步本质是猜测，不给定量结论。
2. 用分段查找把范围收窄到具体代码段，再决定测量哪一层。
3. 用概要形式建立整体印象（处理器使用率、I/O 平均响应时间这类指标）。
4. 范围确定后再上事件记录形式拿细节：它能给出时间与位置，但数据量大、对系统压力大。
5. 用 little 定律 / 排队分析做量级校验：到达率与停留时间已知时，队列长度不该与估算差一个数量级；利用率接近饱和时优先扩容或降负载。

## 示例或代码

- **接口延迟升高**：先看概要形式的平均响应时间确认现象，再用分段查找（二分）定位是 DB 查询、序列化还是网络等待，最后对可疑段开事件记录。
- **队列积压**：用 `L=λW` 反推——若平均停留时间不变而队列变长，说明到达率上升而非处理变慢。
- **排队分析**：收集到达率 λ 与平均服务时间，算利用率 `ρ=λ/μ`——接近 1 说明系统接近饱和，排队会显著恶化。

## 常见误区

- **把估算当结论**：视角与方法给出的是方位，不是定量数据；不测量就下结论是猜。
- **一上来就全量事件记录**：数据量与系统压力都很大，应先用概要形式缩范围。
- **只看平均值**：概要形式按汇总或平均展示，长尾问题会被平均掉；需要时用快照或事件记录看瞬时与分布。

## 证据映射

- 六条 claim 全部为 **`direct`**：
  - `little-law` ← Columbia 讲义（Karl Sigman《Notes on Little's Law》PDF，`little-law-columbia`）；
  - `profile-form` ← OSTI《High Performance Tools & Technologies》（`osti-profiling-tracing`）；
  - `segmented-search` ← UBC 论文《On the Effectiveness of Bisection in Performance Regression Localization》（`bisect-performance-regression`）；
  - `trace-form` / `snapshot-form` ← LUMI 超算官方文档（`lumi-profiling-strategies`：tracing 逐个记录、sampling 周期快照）；
  - `wait-queue` ← GeeksforGeeks 排队论（`queueing-theory-gfg`：定义系统与收集数据的步骤）。
- 因此整页 `strength` 派生为 `attested`（各 claim 单一来源），`public_publishable` 为 true，可公开发布。
- 本人笔记快照 `program-performance-analysis-notes` 作为概念梳理的基础，不再承担外部证据责任。
- 视角、操作顺序与误区是本人的实践判断，未上升为 claim。

## 待验证项

- 本页待验证项已全部收口，验证结论并入正文（证据映射/核心概念），无遗留。

## 关联知识

- LLVM 自动向量化（编译器层面的性能优化手段）
- 循环优化与访存优化
- 处理器与内存层次结构


## 详细章节

### 程序性能的分析和测量

#### 程序性能分析的视角

从硬件层面分析时，是以系统硬件资源的分析为起点，涉及到的系统硬件资源有处理器、内存、磁盘、网卡、总线以及之间的互联等。具体可以从影响性能的硬件资源配置方面展开分析。例如系统有多大的可扩展性、处理并发的能力、系统最大容量、系统可能的性能瓶颈以及通过更换或扩展哪些设备可以提高系统整体能力等。可以根据现有硬件资源信息，或者监测系统资源的占用情况，全面掌握硬件资源的可用情况。

从软件层面分析就是从程序的角度出发，通过调整程序中的算法与代码实现、系统设置或硬件配置等方法提高整体的性能表现。软件层面分析期望的是通过程序性能表现这一“现象”，来准确的定位影响程序性能原因的“本质”，并通过使用针对性的优化手段达到性能优化的目的。从软件层面对程序进行分析，通过优化人员对系统进行软硬一体的联调，可以解决许多类似的性能问题。例如使用大量资源后不释放、频繁的I/O操作、程序执行时频繁的缓存不命中、程序中语句执行效率低等。 



#### 程序性能分析的方法

程序性能分析的目的是对当前程序的性能进行评估，分析出当前的程序性能与理论性能之间的差异，并找出程序性能提升的方法。 



##### 分段查找

进行程序性能分析之前需要首先定位导致程序性能瓶颈产生的原因，才能针对性的开展后续的优化。分段查找是常用定位程序分析代码段的方法之一，可以在时间或空间层面进行，主要思想是根据需要获取某段代码的执行信息并进行分析，查找问题所在。



##### 等待排队

等待排队可以抽象为办理业务排队直到业务办理结束所耗费的整体时间。对应于程序则为程序进入就绪队列到程序执行完成所耗费的时间。等待排队方法主要分析等待进程数以及进程需等待多久。



##### little 估算

little定律的等式为：L=λ*W。其中变量的意思是L 表示在一段时间内排队系统中的平均任务或项目数量即排队队列中的任务数，λ表示在规定的时间间隔内新进入系统的平均任务或项目数量即新任务到达率，W 表示任务或项目在整个系统中花费的平均时间即任务的平均花费时间。



#### 程序性能的测量

运用程序性能分析的视角及方法的目的是找到程序性能瓶颈的大概方位，或者分析出程序中制约性能表现的位置。其本质是一种猜测或估算，并不能精准的定位或给出定量的数据。 



##### 程序性能测量的信息类型

###### 概要形式

概要形式是以汇总或者平均值的形式来展示一段时间的程序信息，必须等待一段时间来获取信息，是比较费时的。其特点是比较适合掌握初步信息，以及用来追溯调查过去的概况，比如处理器使用率高、I/O的平均响应时间长等现象。



###### 事件记录形式

事件记录形式是逐个记录每个事件，生成系统信息。使用事件记录形式来分析性能情况的时候，需要在同一台计算机下进行测量并且可以跟踪出发与到达，并不能记录程序处理的过程，跟踪过程产生的数据量较大，对系统造成的压力也相应变得很大，可以在确定了某个范围后，来查看详细信息。优点在于可以获得关于时间、位置等详细的信息，缺点是在核对进程到达和出发时会比较费时，效率较低。



###### 快照形式

快照形式是记录当前信息的方式，来生成性能信息。例如可以显示进程的瞬间状态。优点是比较适合查找引起性能问题的原因。 



##### 程序性能分析工具类型

Linux性能观测工具按类别可分为系统级别和进程级别，系统级别是对整个系统的性能做统计，而进程级别则可以具体到某个进程的信息。 



###### 计数器类型

在系统内核中，一般会生成一些用于对事件发生次数进行计数的统计数据，称为计数器。通常计数器为无符号的整型数，事件发生时递增。计数器的使用可以认为是零开销的，因为它们默认就是开启的，而且始终由操作系统内核维护，唯一的使用开销是从用户空间读取它们的时候。 



####### 虚拟内存统计工具`vmstat`

####### 输入输出统计工具`iostat`

####### 实时状态工具`top`

####### 当前进程信息统计工具`ps`



###### 跟踪类型

跟踪工具是跟踪收集每个事件的数据，然后供性能分析。一般情况下，跟踪工具的话是默认不启用。因为跟踪工具捕获存储数据数据会有开销，需要很大的存储空间来存放跟踪的数据。



####### 程序调试工具`gdb`

####### 堆栈统计信息工具`pstack`

####### 跟踪系统调用工具`strace`



###### 剖析类型

性能剖析通常是按照特定的时间间隔对系统的状态进行采样，然后对这些样本进行分析与研究。性能剖析的目标是寻找性能瓶颈，查找引发性能问题的原因及热点代码。源程序首先被插入将用于性能测试的代码，代码插入的工作原理是让编译器修改函数调用，并插入代码以记录这些调用、调用者或者完整调用栈以及可能需要的时间信息。插入代码之后，程序再运行，最后得到结果。结果中包含程序分析所需要的信息。 



####### 函数剖析工具`gprof`

####### 可视化软件性能分析工具`oneAPI`

####### 性能分析工具`perf`

####### CUDA程序性能分析工具`nvprof`



###### 监控类型

性能监视记录了一段时间内的性能统计数据。通过性能监视，可以将过去的记录信息和现在的做比较，这样就能够找出程序基于时间的运行规律。 



####### 系统活动情况报告工具`sar`

####### 监控网络工具`netstat`

####### 监控硬盘工具`iotop`

####### 实时系统监控工具`mpstat`
