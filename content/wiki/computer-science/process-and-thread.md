---
aliases: []
confidentiality: public
domain: computer-science
evidence:
- claim: "pthreads(7)          Miscellaneous Information Manual         pthreads(7)\n
    \      pthreads - POSIX threads\n       POSIX.1 specifies a set of interfaces
    (functions, header files)\n       for threaded programming commonly known as POSIX
    threads, or\n       Pthreads.  A single process can contain multiple threads,
    all of\n       which are executing the same program."
  claim_id: process-and-thread-audit-1
  support: direct
  supporting_quotes:
  - evidence_id: evidence-baeadaee5ee2
    exact: "pthreads(7)          Miscellaneous Information Manual         pthreads(7)\n
      \      pthreads - POSIX threads\n       POSIX.1 specifies a set of interfaces
      (functions, header files)\n       for threaded programming commonly known as
      POSIX threads, or\n       Pthreads.  A single process can contain multiple threads,
      all of\n       which are executing the same program."
  targets:
  - evidence_id: evidence-baeadaee5ee2
    source_id: web-computer-science-process-and-thread
id: process-and-thread
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-process-and-thread
- working-computer-science-process-and-thread
status: published
tags:
- process
- thread
- scheduling
- concurrency
title: 进程和线程
updated_at: '2026-09-06'
---
# 进程和线程

## 一句话结论

进程是执行用户程序的环境（包含进程空间内的数据和内核里的元数据/上下文），一个进程可包含多个线程，它们都执行同一个程序（POSIX.1 以 Pthreads 接口规定线程编程）。本页涵盖进程内存布局、动态库机制、多线程调度策略与并发/并行。

## 核心概念

- **进程内存布局**：进程是执行用户程序的环境，包括进程空间内的数据和内核里的元数据（上下文）；栈存放函数参数、局部变量等（使用一级缓存），堆是动态内存、由程序分配释放（使用二级缓存），使用栈的效率比堆高。
- **动态库机制**：Linux 下动态链接通过 PLT&GOT 实现，并通过 PLT&GOT 实现延迟绑定；全局偏移表（GOT）存放外部函数地址的数据表，程序链接表（PLT）存放额外代码的表。
- **多线程调度**：CFS 调度策略（SCHED_NORMAL 分时调度、用户进程默认策略；SCHED_BATCH 假定任务 CPU 密集、有较小的调度开销和较大的交互时延）与 RT 类调度器策略（SCHED_FIFO 有优先级的先进先出；SCHED_RR 为 FIFO 的简单增强，相同优先级有时间分片机制）。
- **并发与并行**：并发是一个处理器同时处理多个任务；并行是多个处理器或多核处理器同时处理多个不同的任务。
- **伪共享**：多线程修改互相独立的变量时，若这些变量落在同一个缓存行（cache line），就会影响彼此的性能。

## 工作机制

- **内存组织**：进程空间内的数据按栈/堆等区域组织，栈用于函数调用（参数、局部变量），堆用于动态内存的分配与释放。
- **动态链接**：动态库通过 PLT 与 GOT 配合实现延迟绑定；使用 `-fPIC` 编译时，模块内部的函数和变量均放到 PLT 或 GOT 表中。
- **调度机制**：分时任务走 CFS（SCHED_NORMAL/SCHED_BATCH），实时任务走 RT 类调度器（SCHED_FIFO/SCHED_RR），按策略决定进程/线程的执行顺序与时间片。
- **并发同步**：常用同步原语为自旋锁、互斥锁、读写锁；优化方式包括正确选择锁、减少临界区范围、减少竞争、无锁机制、免锁机制。
- **伪共享优化**：对热点数据进行 cache line 对齐。

## 示例或代码

详细章节未提供可运行的代码示例，以术语与策略清单形式呈现：

- 调度策略对照：`SCHED_NORMAL`（分时调度，用户进程默认）→ `SCHED_BATCH`（CPU 密集，调度开销小、交互时延大）→ `SCHED_FIFO`（有优先级的先进先出）→ `SCHED_RR`（FIFO 增强，相同优先级有时间分片）。
- 同步原语：自旋锁、互斥锁、读写锁。
- 伪共享优化：热点数据 cache line 对齐。

## 常见误区

- **混淆并发与并行**：并发是一个处理器同时处理多个任务；并行是多个处理器或多核处理器同时处理多个不同的任务。
- **忽略栈与堆的效率差异**：栈（函数参数、局部变量，一级缓存）与堆（动态内存，二级缓存）访问效率不同，使用栈的效率比堆高。
- **忽略伪共享**：多线程修改互相独立的变量时，若变量位于同一个缓存行，也会影响彼此性能；应让热点数据 cache line 对齐。

## 证据映射

| claim_id | 来源 | 要点 |
| --- | --- | --- |
| process-and-thread-audit-1 | web-computer-science-process-and-thread | POSIX.1 规定线程编程接口（POSIX threads/Pthreads）；一个进程可包含多个线程，都执行同一个程序 |

## 待验证项

无。

## 关联知识

- [[cpu-and-memory]] —— 进程内存布局与 CPU/内存机制
- [[cpu-pipeline-and-hazards]] —— CPU 流水线与性能
- [[process-optimization]] —— 进程优化
- [[cpp-concurrent-programming-and-cuda]] —— C++ 并发编程

## 详细章节

### 进程和线程

#### 进程内存布局

进程是执行用户程序的环境，包括进程空间内的数据和内核里的元数据（上下文）



栈：存放函数参数、局部变量等，使用一级缓存

堆：动态内存，程序中分配释放，使用二级缓存

使用栈的效率比堆要高



#### 动态库机制

linux下动态链接是通过PLT&GOT实现，并通过PLT&GOT实现延迟绑定。

全局偏移表（GOT，Global Offset Table）存放外部的函数地址的数据表

程序链接表（PLT，Procedure Link Table）存放额外代码的表



使用-fPIC，模块内部的函数和变量均放到PLT或GOT表中





#### 多线程调度机制

CFS调度策略

* SCHED_NORMAL
  * 分时调度，用户进程默认策略
* SCHED_BATCH
  * 假定任务是cpu密集的，有较小的调度开销和较大的交互时延



RT类调度器策略

* SCHED_FIFO
  * 有优先级的先进先出
* SCHED_RR
  * FIFO的简单增强，相同的优先级有时间分片机制





#### 并发和并行

并发：一个处理器同时处理多个任务

并行：多个处理器或者多核的处理器同时处理多个不同的任务



常用同步原语

* 自旋锁
* 互斥锁
* 读写锁



优化方式：

* 正确选择锁
* 减少临界区范围
* 减少竞争
* 无锁机制
* 免锁机制



伪共享：多线程修改互相独立的变量时，如果变量在同一个缓存行（cache line），就会影响彼此的性能，这就是伪共享



优化方式：热点数据进行cache line对齐

