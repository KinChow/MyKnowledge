---
aliases: []
confidentiality: public
domain: computer-science
evidence:
- claim: 哈佛架构将程序指令和数据存储在独立的存储单元中，并通过独立总线访问。
  claim_id: harvard-architecture-audit-1
  support: direct
  supporting_quotes:
  - evidence_id: evidence-714c76f0e212
    exact: Harvard architecture is a computer design model where program instructions
      and data are stored in separate memory units that are accessed through independent
      buses.
  targets:
  - evidence_id: evidence-714c76f0e212
    source_id: geeksforgeeks-harvard-architecture-v2
id: harvard-architecture
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- geeksforgeeks-harvard-architecture-v2
- working-computer-science-harvard-architecture
status: published
tags:
- architecture
- computer-organization
- memory
- cpu
title: 哈佛结构
updated_at: '2026-09-06'
---
# 哈佛结构

## 一句话结论

哈佛结构是一种**将程序指令和数据分开存储、通过独立总线访问**的计算机设计模型（Split Cache）：指令与数据可并行存取、可有不同字宽，从而带来较高的执行效率。

## 核心概念

- **分离存储（Split Cache）**：程序指令储存与数据储存分开的存储器结构。
- **独立总线**：指令与数据通过各自的总线访问，可同时进行存取。
- **不同数据宽度**：指令和数据的字宽、定时、实现技术、内存地址可以不同。
- **程序需外部加载**：程序需要由操作者加载，处理器无法自行初始化。

## 工作机制

1. 中央处理器首先到**程序指令储存器**读取程序指令内容；
2. 解码后得到数据地址；
3. 再到相应的**数据储存器**读取数据，进行下一步操作（通常是执行）。
4. 由于指令与数据存储分离，可同时存取、可预先读取下一条指令，因此微处理器通常具有较高执行效率。

## 示例或代码

- **指令/数据特性不同**：指令可存储在只读存储器（ROM）中，而数据存储器一般需要读写存储器（RAM 等）。
- **地址宽度不同**：一些系统中指令存储器比数据存储器多，因此指令地址比数据地址更宽。
- **寄存器无需共同特征**：两个寄存器不需要有共同的特性（字宽、定时、实现技术和内存地址均可不同）。

## 常见误区

- **“处理器能自行初始化程序”**：恰恰相反，程序需要由操作者加载，处理器无法自行初始化。
- **“指令和数据必须用同一存储/总线”**：哈佛结构的核心正是二者分离、通过独立总线访问。
- **“指令和数据必须具有相同宽度”**：指令与数据可以有不同字宽、不同定时与不同地址宽度。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| harvard-architecture-audit-1 | geeksforgeeks-harvard-architecture-v2 | 哈佛架构将程序指令与数据存储在独立存储单元，通过独立总线访问 |

## 待验证项

无。

## 关联知识

- [[von-neumann-architecture]] —— 对偶模型：存储程序、统一存储器结构。
- [[cpu-and-memory]] —— CPU 与内存交互、流水线机制。
- [[instructions]] —— 指令的取指与执行。
- [[cpu-cache-optimization]] —— 缓存优化与访存性能。

## 详细章节

### 哈佛结构

一种将程序指令储存和数据储存分开的存储器结构(Split Cache)。



 中央处理器首先到程序指令储存器中读取程序指令内容，解码后得到数据地址，再到相应的数据储存器中读取数据，并进行下一步的操作（通常是执行）。



程序指令储存和数据储存分开，数据和指令的储存可以同时进行，可以使指令和数据有不同的数据宽度。



程序需要由操作者加载；处理器无法自行初始化。



哈佛架构的微处理器通常具有较高的执行效率。其程序指令和数据指令分开组织和储存的，执行时可以预先读取下一条指令。



在哈佛架构，两个寄存器不需要有共同的特征。特别是，字宽、定时、实现技术和内存地址都可以不同。在一些系统中，指令可以存储在只读存储器（ROM）中，而数据存储器一般需要读写存储器（RAM等）。在一些系统中，指令存储器比数据存储器多，因此指令地址比数据地址更宽。



#### 参考

* https://zh.wikipedia.org/wiki/%E5%93%88%E4%BD%9B%E7%BB%93%E6%9E%84

## 参考

* 哈佛结构 - 维基百科：https://zh.wikipedia.org/wiki/%E5%93%88%E4%BD%9B%E7%BB%93%E6%9E%84
