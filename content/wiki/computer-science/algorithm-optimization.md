---
aliases: []
confidentiality: public
domain: computer-science
evidence:
- claim: 算法效率描述算法使用的计算资源多少。
  claim_id: algorithm-optimization-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-50e682cdaa18
    exact: In computer science, algorithmic efficiency is a property of an algorithm
      which relates to the amount of computational resources used by the algorithm.
  targets:
  - evidence_id: evidence-50e682cdaa18
    source_id: wikipedia-algorithmic-efficiency-v2
id: algorithm-optimization
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- wikipedia-algorithmic-efficiency-v2
- working-computer-science-algorithm-optimization
status: published
tags:
- performance
- optimization
- algorithm
- complexity
title: 算法优化
updated_at: '2026-09-06'
---
# 算法优化

## 一句话结论

算法优化是通过对算法进行更好的设计来提升程序性能，可从"选择合适的算法"与"算法自身的优化"两方面入手；核心衡量指标是算法的时间复杂度与空间复杂度。

## 核心概念

- **算法**：计算机解决问题过程的描述，由一系列求解问题的指令构成，能根据规范的输入在有限的时间内获得有效的输出结果。
- **时间复杂度**：程序执行时间增长的变化趋势。
- **空间复杂度**：程序在运行过程中临时占用存储空间大小的一个量度。
- **常见复杂度量级**：常数阶、对数阶、线性阶、线性对数阶、平方阶、指数阶、阶乘阶等，依次顺序时间复杂度越来越大、执行效率越来越低。
- **算法优化的两个方向**：一是选择合适的算法，二是算法自身的优化（从算法过程出发降低复杂度、从算法编码出发优化编码方式）。

## 工作机制

1. 先用时间/空间复杂度衡量算法现状，确定性能量级。
2. 选择合适的算法：同一问题往往有多种算法可选（如排序算法有十余种，分为基于比较的插入、选择、交换三类），结合问题特征选最合适的。
3. 改进算法策略：
   - 从算法过程出发，尽量减少算法复杂度、提高运行效率；
   - 从算法编码出发，运用技巧优化编码方式、从编码角度提升性能。

## 示例或代码

以排序算法为例，常用的排序算法有十余种，分为基于比较的插入、选择、交换三类，如冒泡排序、快速排序等；实际选择时需根据数据特征（如规模、有序程度）权衡各算法的时间复杂度与空间复杂度。

## 常见误区

- **只盯时间复杂度**：算法复杂度同时包含时间与空间两个维度，忽略空间复杂度可能带来内存占用问题。
- **把算法优化等同于底层编码技巧**：选择更合适的算法往往比优化既有实现收益更大，优化应同时覆盖"选对算法"与"改进算法"两个层面。
- **不看复杂度量级就选算法**：常见量级从常数阶到阶乘阶依次变慢、执行效率依次降低，选择算法时应结合问题规模与数据特征。

## 证据映射

| claim_id | 来源 | 要点 |
| --- | --- | --- |
| algorithm-optimization-definition | wikipedia-algorithmic-efficiency-v2 | 算法效率描述算法使用的计算资源多少 |

## 待验证项

无

## 关联知识

- [[data-structure-optimization]]：数据结构优化
- [[loop-optimization]]：循环级优化
- [[statement-optimization]]：语句级优化
- [[compilation-and-runtime-optimization]]：编译与运行优化

## 详细章节

### 算法优化

#### 算法简介

任何问题的解决都有一定的方法和步骤，算法就是计算机解决问题过程的描述。从程序设计的角度看，算法由一系列求解问题的指令构成，能根据规范的输入，在有限的时间内获得有效的输出结果，代表了用系统的方法来描述解决问题的一种策略机制。 

算法复杂度这一指标用于考量算法需要的时间和空间。算法的时间复杂度，即程序执行时间增长的变化趋势。空间复杂度是指一个程序在运行过程中临时占用存储空间大小的一个量度。

一般来说，常见的时间复杂度量级有常数阶、对数阶、线性阶、线性对数阶、平方阶、指数阶、阶乘阶等，依次按照顺序时间复杂度越来越大，执行效率也越来越低。

算法优化是指通过对算法进行更好的设计以提升程序的性能，程序中的算法优化可以从选择合适的算法以及算法自身的优化这两方面进行考虑。



#### 选择适合算法

以排序算法为例，常用的排序算法有十余种，分为基于比较的插入、选择、交换这三类，如冒泡排序、快速排序等。 



#### 改进算法策略

改进算法策略的方法归结起来可以分为以下两点：

1. 从算法过程出发，尽量减少算法复杂度，提高其运行的效率。
2. 从算法编码出发，运用一些技巧优化算法中的编码方式，从编码角度提升算法性能。 
