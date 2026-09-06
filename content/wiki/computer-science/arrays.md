---
aliases:
- Array
- 数组数据结构
- 一维数组
confidentiality: public
domain: computer-science
evidence:
- claim: 在计算机科学中，数组是由同内存大小的元素（值或变量）组成的数据结构，每个元素由至少一个数组下标（索引/键）标识，多个下标可组成索引元组。
  claim_id: arr-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-c4b9fe95c672
    exact: |-
      In computer science, an array is a data structure consisting of a collection of elements (values or variables), of the same memory size, each identified by at least one array index or key, the collection of which may be a tuple, known as an index tuple.
  targets:
  - evidence_id: evidence-c4b9fe95c672
    source_id: wiki-array-cs
- claim: 一般而言数组是同数据类型的可变线性集合；存储方式使每个元素的内存地址可由下标元组经数学公式计算得到；最简单的数据结构是线性数组（一维数组）。
  claim_id: arr-linear-storage
  support: direct
  supporting_quotes:
  - evidence_id: evidence-48aee0cfd4dd
    exact: |-
      In general, an array is a mutable and linear collection of elements with the same data type. An array is stored such that the position (memory address) of each element can be computed from its index tuple by a mathematical formula. The simplest type of data structure is a linear array, also called a one-dimensional array.
  targets:
  - evidence_id: evidence-48aee0cfd4dd
    source_id: wiki-array-cs
- claim: 数组有用主要因为元素下标可在运行时计算；因此数组元素必须同尺寸、使用同一种数据表示。
  claim_id: arr-runtime
  support: direct
  supporting_quotes:
  - evidence_id: evidence-3a0f8a1c609d
    exact: |-
      Arrays are useful mostly because the element indices can be computed at run time.
  - evidence_id: evidence-966acca3186e
    exact: |-
      For that reason, the elements of an array data structure are required to have the same size and should use the same data representation.
  targets:
  - evidence_id: evidence-3a0f8a1c609d
    source_id: wiki-array-cs
  - evidence_id: evidence-966acca3186e
    source_id: wiki-array-cs
- claim: 在使用处理器缓存或虚拟内存的系统中，相继元素连续存储时数组的扫描比稀疏散布快得多——这就是空间局部性（spatial
    locality），是引用局部性的一种。
  claim_id: arr-locality
  support: direct
  supporting_quotes:
  - evidence_id: evidence-158a9b77e84c
    exact: |-
      In systems which use processor cache or virtual memory, scanning an array is much faster if successive elements are stored in consecutive positions in memory, rather than sparsely scattered. This is known as spatial locality, which is a type of locality of reference.
  targets:
  - evidence_id: evidence-158a9b77e84c
    source_id: wiki-array-cs
- claim: 使用多维数组的算法会按可预测顺序扫描，程序员（或编译器）可据此选择行主序或列主序布局；例如计算矩阵乘积
    A·B 时，A 以行主序、B 以列主序存储最佳。
  claim_id: arr-major
  support: direct
  supporting_quotes:
  - evidence_id: evidence-4ae1136a3f28
    exact: |-
      Many algorithms that use multidimensional arrays will scan them in a predictable order. A programmer (or a sophisticated compiler) may use this information to choose between row- or column-major layout for each array.
  - evidence_id: evidence-45144fe6c9df
    exact: |-
      For example, when computing the product A·B of two matrices, it would be best to have A stored in row-major order, and B in column-major order.
  targets:
  - evidence_id: evidence-4ae1136a3f28
    source_id: wiki-array-cs
  - evidence_id: evidence-45144fe6c9df
    source_id: wiki-array-cs
- claim: 随机访问：因为知道基址且每个元素/引用同尺寸，第 i 个元素可在 O(1) 时间内访问。
  claim_id: arr-random-access
  support: direct
  supporting_quotes:
  - evidence_id: evidence-74c5ebb3931e
    exact: |-
      Random Access : i-th item can be accessed in O(1) Time as we have the base address and every item or reference is of same size.
  targets:
  - evidence_id: evidence-74c5ebb3931e
    source_id: web-computer-science-arrays
- claim: 缓存友好：元素/引用存储在连续位置，带来引用局部性优势。
  claim_id: arr-cache
  support: direct
  supporting_quotes:
  - evidence_id: evidence-74db51a83add
    exact: |-
      Cache Friendliness : Since items / references are stored at contiguous locations, we get the advantage of locality of reference.
  targets:
  - evidence_id: evidence-74db51a83add
    source_id: web-computer-science-arrays
- claim: 数组被用来构建其他数据结构，如栈、队列、双端队列、图、哈希表等。
  claim_id: arr-build-ds
  support: direct
  supporting_quotes:
  - evidence_id: evidence-2a1b432e458b
    exact: |-
      Arrays are used to build other data structures like Stack Queue, Deque, Graph, Hash Table, etc.
  targets:
  - evidence_id: evidence-2a1b432e458b
    source_id: web-computer-science-arrays
- claim: 在中间插入、中间删除、无序数据查找这类操作场景下，数组并不适用。
  claim_id: arr-middle-ops
  support: direct
  supporting_quotes:
  - evidence_id: evidence-49d49a2a0411
    exact: |-
      An array is not useful in places where we have operations like insert in the middle, delete from middle and search in a unsorted data.
  targets:
  - evidence_id: evidence-49d49a2a0411
    source_id: web-computer-science-arrays
id: arrays
kind: reference
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- wiki-array-cs
- web-computer-science-arrays
- working-computer-science-arrays
status: published
tags:
- data-structure
- array
- memory-layout
title: 数组
updated_at: '2026-09-05'
---
# 数组

## 一句话结论

数组是**同类型元素连续存储**的线性数据结构：地址 = 基址 + 下标 × 元素大小，因此随机访问 O(1)；连续性还带来空间局部性（缓存友好）。代价是尺寸固定、中间插删要搬移 O(n)。它是几乎所有数据结构的地基——栈、队列、哈希表、堆、矩阵都用数组构建。

## 核心概念

- **下标寻址**：元素位置由下标元组经数学公式计算——这是数组一切性能特征的根源。
- **同尺寸同表示**：随机寻址的前提，也是"数组只能存同类型"的原因。
- **空间局部性**：连续存储 + 顺序扫描 = 缓存命中率高。
- **行主序 / 列主序**：多维数组的两种线性化布局，选择取决于扫描顺序。

## 工作机制

### 地址计算

```
addr(a[i]) = base + i × element_size        （一维）
addr(a[i][j]) = base + (i × ncols + j) × element_size   （行主序二维）
```

### 复杂度

| 操作 | 复杂度 | 原因 |
| --- | --- | --- |
| 随机访问 a[i] | O(1) | 公式直接算地址 |
| 尾部插入/删除 | O(1) | 不搬移 |
| 中间插入/删除 | O(n) | 后续元素整体搬移 |
| 查找（无序） | O(n) | 必须线性扫描 |
| 查找（有序） | O(log n) | 二分（数组专属优势） |

### 行主序 vs 列主序

- **行主序（C 风格）**：按行连续存放，`a[i][j]` 地址随 j 连续增长；C/C++/Python(numpy 默认 C order)。
- **列主序（Fortran 风格）**：按列连续存放；Fortran、MATLAB、numpy 可选 `order='F'`。
- 选择原则：让**最内层循环沿连续方向扫描**——矩阵乘 A·B 中 A 行主序、B 列主序最佳。

## 常见误区

- **"数组 = 连续内存"**：C/C++ 原始数组、Java 基本类型数组是的；Python list/JS 数组存的是引用的连续数组，引用指向的对象本身不连续。
- **"动态数组（vector/list）就是数组"**：动态数组在其上加了自动扩容——满时倍增搬迁，均摊尾部插入 O(1)，但中间插删仍是 O(n)。
- **"缓存友好是小事"**：在大数组顺序扫描 vs 随机访问的性能差可达数倍到数十倍——数据局部性是性能工程的第一课（见 [[cpu-cache-optimization]]）。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| arr-definition / arr-linear-storage / arr-runtime / arr-locality / arr-major | wiki-array-cs（Wikipedia） | 定义、地址公式、运行时下标、空间局部性、行/列主序 |
| arr-random-access / arr-cache / arr-build-ds / arr-middle-ops | web-computer-science-arrays | O(1) 随机访问、缓存友好、构建其他结构、中间操作劣势 |

## 待验证项

无。

## 关联知识

- [[cpu-cache-optimization]] —— 空间局部性的硬件原理与调优实践。
- [[matrix]] —— 二维数组 + 线性代数语义。
- [[stack]] / [[queue]] —— 用数组实现的最基础线性结构。
- [[data-structure-optimization]] —— 连续 vs 链式结构的选型权衡。

## 详细章节

### 定义

数组是由同内存大小的元素组成的数据结构：每个元素由至少一个下标标识，存储方式使元素地址可由下标经公式计算。它一般可变、线性、元素同类型；最简单的形态是线性数组（一维数组）。注意 C/C++ 与 Java 原始数组中实际元素连续；Python/JS 中连续的是引用。

### 优势

- 随机访问 O(1)（基址 + 同尺寸）。
- 缓存友好（连续存储带来引用局部性；空间局部性）。
- 下标可在运行时计算，一个循环语句即可处理任意多元素。
- 是栈、队列、双端队列、图、哈希表等结构的构建基座。

### 劣势

- 中间插入/删除、无序查找场景不适用（搬移/线性扫描代价）。
- 静态数组尺寸固定；分配过小丢数据、过大浪费内存。

## 参考

- https://en.wikipedia.org/wiki/Array_(data_structure)
- https://www.geeksforgeeks.org/dsa/introduction-to-arrays/
