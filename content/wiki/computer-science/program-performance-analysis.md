---
aliases:
- 程序性能的分析和测量
- 性能分析方法
confidentiality: public
domain: computer-science
evidence:
- claim: little 定律的等式为 L=λ*W。
  claim_id: little-law
  support: personal
  supporting_quotes:
  - evidence_id: evidence-5e71c592c1bd
    exact: little定律的等式为：L=λ*W
  targets:
  - evidence_id: evidence-5e71c592c1bd
    source_id: program-performance-analysis-notes
- claim: 概要形式以汇总或平均值的形式展示一段时间的程序信息。
  claim_id: profile-form
  support: personal
  supporting_quotes:
  - evidence_id: evidence-c7bd2ab17520
    exact: 概要形式是以汇总或者平均值的形式来展示一段时间的程序信息
  targets:
  - evidence_id: evidence-c7bd2ab17520
    source_id: program-performance-analysis-notes
- claim: 分段查找是常用的定位程序分析代码段的方法之一。
  claim_id: segmented-search
  support: personal
  supporting_quotes:
  - evidence_id: evidence-72311733bcc6
    exact: 分段查找是常用定位程序分析代码段的方法之一
  targets:
  - evidence_id: evidence-72311733bcc6
    source_id: program-performance-analysis-notes
id: program-performance-analysis
kind: knowledge
publication_scope: public
related: []
sources:
- program-performance-analysis-notes
status: published
tags:
- performance
- profiling
- measurement
title: 程序性能的分析与测量：视角、方法与信息形式
updated_at: '2026-09-01'
---
# 程序性能的分析与测量：视角、方法与信息形式

## 一句话结论

性能工作分两步：先用硬件与软件两个视角把瓶颈**大致定位**（分段查找、等待排队、little 定律都属于估算手段），再用测量拿到**定量证据**——概要形式看趋势、事件记录形式看细节。

## 核心概念

- **硬件视角**：从处理器、内存、磁盘、网卡、总线及互联的资源配置与占用出发，判断可扩展性、并发能力与容量上限。
- **软件视角**：从程序出发，通过算法与代码实现、系统设置或硬件配置的调整改善性能表现。
- **分段查找**：按需获取某段代码的执行信息并分析，在时间或空间层面缩小问题范围。
- **little 定律**：`L=λ*W`——排队系统中的平均任务数等于到达率乘以平均停留时间。
- **概要形式 / 事件记录形式**：前者以汇总或平均值展示一段时间的信息，后者逐个记录每个事件。

## 工作机制

1. 先用视角与方法**估算**瓶颈方位——这一步本质是猜测，不给定量结论。
2. 用分段查找把范围收窄到具体代码段，再决定测量哪一层。
3. 用概要形式建立整体印象（处理器使用率、I/O 平均响应时间这类指标）。
4. 范围确定后再上事件记录形式拿细节：它能给出时间与位置，但数据量大、对系统压力大。
5. 用 little 定律做量级校验：到达率与停留时间已知时，队列长度不该与估算差一个数量级。

## 示例或代码

- **接口延迟升高**：先看概要形式的平均响应时间确认现象，再用分段查找定位是 DB 查询、序列化还是网络等待，最后对可疑段开事件记录。
- **队列积压**：用 `L=λ*W` 反推——若平均停留时间不变而队列变长，说明到达率上升而非处理变慢。

## 常见误区

- **把估算当结论**：视角与方法给出的是方位，不是定量数据；不测量就下结论是猜。
- **一上来就全量事件记录**：数据量与系统压力都很大，应先用概要形式缩范围。
- **只看平均值**：概要形式按汇总或平均展示，长尾问题会被平均掉。

## 证据映射

- 三条 claim 的 `support` 均为 **`personal`**：证据锚定在本人笔记快照 `program-performance-analysis-notes`（`source_type: personal-note`、`origin: personal`），因此整页 `strength` 派生为 `personal`，而不是 attested/verified。
- 这是**有意的**：本页内容是本人综合多个来源后改写的概念梳理（排队论的 little 定律、性能测量的信息形式分类等），来源已融进表述，无法逐句回指某一份外部原文。把它伪装成外部支撑才是失真。
- 正文中的操作顺序与误区是本人的实践判断，未上升为 claim。
- 若后续找到可锚定的外部原文（如排队论教材、性能分析专著），应新增外部 source 并把对应 claim 升级为 `direct`，届时 `strength` 才可能到 `attested`。

## 待验证项

- [ ] 为 little 定律补排队论原始文献的外部 source，把 `little-law` 从 personal 升级为 direct；
- [ ] 概要形式/事件记录形式的分类出自哪本书尚未确认，需查证后补出处；
- [ ] 等待排队方法只记录了定义，缺少可操作的测量步骤。

## 关联知识

- LLVM 自动向量化（编译器层面的性能优化手段）
- 循环优化与访存优化
- 处理器与内存层次结构
