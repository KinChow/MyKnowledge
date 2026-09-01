---
aliases:
- LLVM 自动向量化
- Loop Vectorizer
- SLP Vectorizer
confidentiality: public
domain: computer-science
evidence:
- claim: LLVM 有两个向量化器：作用于循环的 Loop Vectorizer，以及 SLP Vectorizer。
  claim_id: two-vectorizers
  support: direct
  supporting_quotes:
  - evidence_id: evidence-878e7e0d7d13
    exact: 'LLVM has two vectorizers: The Loop Vectorizer, which operates on Loops,
      and the SLP Vectorizer'
  targets:
  - evidence_id: evidence-878e7e0d7d13
    source_id: llvm-auto-vectorization
- claim: SLP 向量化器把代码中找到的多个标量合并成向量。
  claim_id: slp-merges-scalars
  support: direct
  supporting_quotes:
  - evidence_id: evidence-41839e947a4e
    exact: The SLP vectorizer merges multiple scalars that are found in the code into
      vectors
  targets:
  - evidence_id: evidence-41839e947a4e
    source_id: llvm-auto-vectorization
- claim: 向量化的 SIMD 宽度可以用命令行标志 -force-vector-width 控制。
  claim_id: force-vector-width
  support: direct
  supporting_quotes:
  - evidence_id: evidence-b37af9d946eb
    exact: Users can control the vectorization SIMD width using the command line flag
      “-force-vector-width”
  targets:
  - evidence_id: evidence-b37af9d946eb
    source_id: llvm-auto-vectorization
id: llvm-auto-vectorization
kind: knowledge
publication_scope: public
related: []
sources:
- llvm-auto-vectorization
status: published
tags:
- compiler
- vectorization
- llvm
title: LLVM 自动向量化：两个向量化器与宽度控制
updated_at: '2026-09-01'
---
# LLVM 自动向量化：两个向量化器与宽度控制

## 一句话结论

LLVM 的自动向量化由两个独立的向量化器承担——Loop Vectorizer 作用于循环、SLP Vectorizer 把散落的标量合并成向量；调优时先判断代码属于哪一类，再用 `-force-vector-width` 等标志干预。

## 核心概念

- **Loop Vectorizer**：作用于循环，把一次处理一个元素的循环改写为一次处理多个元素。
- **SLP Vectorizer**：把代码中找到的多个标量合并成向量，针对的是不成循环的直线代码。
- **SIMD 宽度**：一条向量指令同时处理的元素个数，可由命令行标志显式指定。

## 工作机制

1. 两个向量化器面向不同的优化机会，使用不同的技术，因此同一段代码可能只被其中一个处理。
2. Loop Vectorizer 处理循环形态；直线代码里的多个标量运算由 SLP Vectorizer 合并。
3. 宽度不由用户猜测：默认由编译器按目标平台选择，需要固定时用 `-force-vector-width` 指定。

## 示例或代码

```shell
clang -mllvm -force-vector-width=8 ...
opt -loop-vectorize -force-vector-width=8 ...
```

## 常见误区

- **以为只有循环能被向量化**：直线代码里的标量运算由 SLP Vectorizer 负责，不是"没有循环就没有向量化"。
- **默认宽度一定最优**：宽度是可干预的调优参数，但改宽度前应先确认瓶颈确实在向量化上。

## 证据映射

- `two-vectorizers`、`slp-merges-scalars`、`force-vector-width` 三条 claim 均由 `llvm-auto-vectorization` source 快照中的对应句子直接支撑（direct），来源是 LLVM 官方文档 `https://llvm.org/docs/Vectorizers.html`。
- claim 表述严格不超出引文字面：引文只说"两个向量化器"与"SLP 合并标量"，因此 claim 不写"哪个更快""默认启用哪个"这类文档未写的判断。
- 正文的推论性内容（调优顺序、常见误区）留在正文，不上升为 claim。

## 待验证项

- [ ] 补充 Loop Vectorizer 的运行时指针检查与 epilogue 向量化细节，当前只锚定了总览段落；
- [ ] 与 GCC 的向量化实现对照，明确两者在 SLP 上的差异；
- [ ] 引文为英文原文，尚未评估是否需要为中文读者提供逐句对照。

## 关联知识

- 循环优化与编译器优化选项
- SIMD 指令集与数据并行
- 程序性能的分析和测量
