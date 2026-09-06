---
aliases: []
confidentiality: public
domain: computer-science
evidence:
- claim: 数据结构是组织和存储数据、以便高效访问数据的方式。
  claim_id: data-structure-optimization-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-860a76a134ac
    exact: In computer science, a data structure is a way to organize and store data
      that is usually chosen for efficient access to data.
  targets:
  - evidence_id: evidence-860a76a134ac
    source_id: wikipedia-data-structure-v2
id: data-structure-optimization
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- wikipedia-data-structure-v2
- working-computer-science-data-structure-optimization
status: published
tags:
- performance
- optimization
- data-structure
- cache
title: 数据结构优化
updated_at: '2026-09-06'
---
# 数据结构优化

## 一句话结论

数据结构优化从两方面入手：一是选择合适的存储结构（数组、栈、队列、链表、树、哈希表、堆、图等各有优缺点、适用场景不同），二是在满足精度要求下选择合适的数据类型（存储空间更小、更适合硬件结构），从而提升访问速度、缓存利用率并发挥硬件平台特性。

## 核心概念

- **逻辑结构与存储结构**：逻辑结构是数据元素间相互关系的抽象数学模型（集合、线性、树形、图形结构），与存储无关；存储结构指数组、栈、队列、链表、树、哈希表、堆、图等具体数据组织方式。
- **数据类型对性能的影响**：在满足精度要求的前提下，一是选择存储空间更小的数据类型，二是选择更适合硬件结构的数据类型。
- **小尺寸类型的优势**：小尺寸类型数据的访问速度比大尺寸类型数据快，且能在缓存中放更多的数据。
- **稀疏矩阵存储格式**：坐标存储、行压缩、对角存储以及埃尔帕克（ELLPACK）存储等，用于稀疏矩阵向量乘法的性能对比。

## 工作机制

1. 分析典型数据结构的性能：按逻辑结构（数学模型）与存储结构（具体组织方式）分类，明确各自的优缺点与适用场景。
2. 根据访问模式与硬件特性选择数据类型：小尺寸类型访问更快、缓存容纳更多。
3. 在满足正确性与计算精度的前提下做数据类型转换，帮助发挥硬件平台特性、提升运算性能。
4. 针对具体算法（如稀疏矩阵向量乘）选用合适的存储格式，并实现多种格式做测试对比以确定最优方案。

## 示例或代码

以稀疏矩阵向量乘法为例：稀疏矩阵向量乘是科学工程计算的核心算法，采用坐标存储、行压缩、对角存储以及埃尔帕克存储四种稀疏矩阵存储格式分别实现稀疏矩阵向量乘法，并进行测试对比，选择性能最优的存储格式。

## 常见误区

- **只选数据结构、忽略数据类型**：数据类型同样显著影响性能——小尺寸类型访问更快、缓存可容纳更多数据。
- **为性能牺牲精度或正确性**：数据类型转换与结构选择必须在满足正确性以及计算精度的前提下进行。
- **不结合场景选结构**：不同存储结构优缺点不同、适用场景各不相同，应结合访问模式与硬件特性选择。

## 证据映射

| claim_id | 来源 | 要点 |
| --- | --- | --- |
| data-structure-optimization-definition | wikipedia-data-structure-v2 | 数据结构是组织和存储数据、以便高效访问数据的方式 |

## 待验证项

无

## 关联知识

- [[algorithm-optimization]]：算法优化
- [[cpu-cache-optimization]]：缓存命中率与数据布局优化
- [[program-performance-analysis]]：程序性能的分析与测量

## 详细章节

### 数据结构优化

#### 典型数据结构的性能分析

按照分类标准的不同，数据结构可以分为逻辑结构和存储结构，数据的逻辑结构是指数据对象中的数据元素之间的相互关系，与数据的存储尚未关联，是从具体问题抽象出来的数学模型，主要分为集合结构、线性结构、树形结构、图形结构等。

常用的数据存储结构有数组、栈、队列、链表、树、哈希表、堆、图等，这些数据结构有各自的优缺点，适用的场景也各不相同。

在满足精度要求的情况下，不同的数据类型也会对程序的性能有影响，具体包括两个方面，一是选择存储空间更小的数据类型，二是选择更适合硬件结构的数据类型。



#### 选择合适的数据类型

通常小尺寸类型数据的访问速度比大尺寸类型数据快，且小尺寸的数据可以在缓存中放更多的数据。

不同的数据类型的程序在相同架构上的性能也有所不同。此时在满足正确性以及计算精度的要求下，可以对数据类型进行转换，帮助发挥硬件平台特性，提升程序的运算性能。



#### 选择合适的数据结构

以稀疏矩阵向量乘法为例。稀疏矩阵向量乘是科学工程计算的核心算法，为了提升稀疏矩阵向量乘法的性能，将采用坐标存储、行压缩、对角存储以及埃尔帕克存储四种稀疏矩阵存储格式实现稀疏矩阵向量乘法并进行测试对比。
