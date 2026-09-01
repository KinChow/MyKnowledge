---
aliases:
- CPU 和内存
- 指令流水线
confidentiality: public
domain: computer-science
evidence:
- claim: CPU 流水线把一条指令分成若干 stage，前后两条指令的 stage 在时间上可以重叠进行。
  claim_id: pipeline-overlap
  support: personal
  supporting_quotes:
  - evidence_id: evidence-6568f40245c9
    exact: CPU流水线方式：将一条指令分成若干stage，流水线方式前后两条指令的stage在时间上可以重叠进行
  targets:
  - evidence_id: evidence-6568f40245c9
    source_id: cpu-and-memory-notes
- claim: 结构冒险又称资源冲突，指不同指令争用同一部件产生的冲突。
  claim_id: structural-hazard
  support: personal
  supporting_quotes:
  - evidence_id: evidence-7371f8b9b056
    exact: 又称资源冲突，指的是用不同指令争用同一部件产生的冲突
  targets:
  - evidence_id: evidence-7371f8b9b056
    source_id: cpu-and-memory-notes
- claim: 控制冒险指由转移指令引起的流水线中断。
  claim_id: control-hazard
  support: personal
  supporting_quotes:
  - evidence_id: evidence-4cb70d6945a3
    exact: 指的是由转移指令而引起的流水线中断
  targets:
  - evidence_id: evidence-4cb70d6945a3
    source_id: cpu-and-memory-notes
id: cpu-pipeline-and-hazards
kind: knowledge
publication_scope: public
related: []
sources:
- cpu-and-memory-notes
status: published
tags:
- cpu
- pipeline
- computer-architecture
title: CPU 指令流水线与三类冒险
updated_at: '2026-09-01'
---
# CPU 指令流水线与三类冒险

## 一句话结论

流水线不缩短单条指令的执行时间，而是让相邻指令的阶段重叠以提高吞吐；代价是引入结构、数据、控制三类冒险，每类都有对应的硬件或编译期解法。

## 核心概念

- **五阶段**：取指令（IF）→ 指令译码（ID）→ 指令执行（EXE）→ 访存取数（MEM）→ 写回（WB）。
- **重叠执行**：把一条指令切成若干 stage，前后指令的 stage 在时间上重叠；满载时每个时钟周期输出一条指令。
- **三类冒险**：结构（资源争用）、数据（后序指令依赖前序结果）、控制（转移指令打断流水）。
- **多发技术**：超标量在一个时钟周期并发多条独立指令；超流水在一个时钟周期内再分段。

## 工作机制

1. 单条指令的绝对执行时间不变——流水线提升的是吞吐率，不是延迟。
2. 结构冒险的解法在**资源侧**：暂停取指、指令与数据分设存储器、指令预取占用独立访存通道。
3. 数据冒险的解法在**依赖侧**：硬件 stall、插入 nop、数据旁路把结果直接送运算单元、编译期重排指令。
4. 控制冒险的解法在**预测侧**：尽早判定转移与目标地址、双向预取、提前形成条件码、提高猜准率。
5. 超标量与超流水都**不调整指令执行顺序**，并行度依赖编译期把可并行指令搭配好。

## 示例或代码

- **数据旁路的效果**：`a = b + c; d = a + e;` 后一条依赖前一条的结果，无旁路时要等写回，有旁路时 ALU 结果直接转发，省下若干周期。
- **分支猜准率的意义**：循环体内的条件跳转方向高度可预测，猜错代价是清空已预取的流水段——这是循环展开能提速的一个来源。

## 常见误区

- **以为流水线让单条指令变快**：它只提高吞吐率，单条指令的绝对时间没有缩短。
- **把超标量当乱序执行**：超标量并发多条指令但不调整顺序，乱序执行是另一套机制。
- **只关注数据冒险**：结构与控制冒险同样会打断流水，且解法完全不同。

## 证据映射

- 三条 claim 的 `support` 均为 `personal`：证据锚定在本人笔记快照 `cpu-and-memory-notes`（`source_type: personal-note`、`origin: personal`），整页 `strength` 派生为 `personal`。
- 本页是对本人既有笔记的**重组**，不是新增判断：claim 逐字对应笔记原句，正文的分类归纳（三类冒险按资源/依赖/预测分侧）来自笔记已有结构。
- 原始出处不可逐句回指：五阶段划分与冒险分类属计算机体系结构通识，笔记未记录具体教材。若后续锚定到教材原文，应新增外部 source 并把 claim 升级为 `direct`。
- 「每个时钟周期可以并发多条独立指令」这句在笔记中出现两次（超标量与超流水各一次），锚定时返回 `ambiguous_selector`，因此改用控制冒险那句——**引文必须唯一定位**，这是规范的要求而非工具缺陷。

## 待验证项

- [ ] 补充体系结构教材的外部 source，把三条 claim 从 personal 升级为 direct；
- [ ] 笔记中的内存部分（cache 层次、访存延迟）尚未整理进本页；
- [ ] 超标量与乱序执行的边界需要更准确的表述与出处。

## 关联知识

- 多核软件设计与 ISA 分类
- 程序性能的分析与测量
- LLVM 自动向量化
