---
aliases:
- Matrix
- 矩阵数据结构
- 行主序
- 列主序
confidentiality: public
domain: computer-science
evidence:
- claim: 在数学中，矩阵是由数或其他数学对象构成的矩形数组，其元素或条目按行和列排布，通常满足加法与乘法的特定性质。
  claim_id: mx-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-d81b6af46b9f
    exact: |-
      In mathematics, a matrix (pl.: matrices) is a rectangular array of numbers or other mathematical objects with elements or entries arranged in rows and columns, usually satisfying certain properties of addition and multiplication.
  targets:
  - evidence_id: evidence-d81b6af46b9f
    source_id: wiki-matrix-math
- claim: 矩阵中的数（或其他对象）称为其条目或元素；横排称为行，竖排称为列。
  claim_id: mx-entries
  support: direct
  supporting_quotes:
  - evidence_id: evidence-e86fe133ba1a
    exact: |-
      The numbers (or other objects) in the matrix are called its entries or its elements. The horizontal and vertical lines of entries in a matrix are respectively called rows and columns.
  targets:
  - evidence_id: evidence-e86fe133ba1a
    source_id: wiki-matrix-math
- claim: 矩阵的尺寸由其行数与列数定义；m 行 n 列的矩阵称为 m×n 矩阵（m-by-n 矩阵），m 与
    n 称为它的维度。
  claim_id: mx-size
  support: direct
  supporting_quotes:
  - evidence_id: evidence-6191c4e9ca2a
    exact: |-
      The size of a matrix is defined by the number of rows and columns it contains. A matrix with m rows and n columns is called an m × n matrix, or m-by-n matrix, where m and n are called its dimensions.
  targets:
  - evidence_id: evidence-6191c4e9ca2a
    source_id: wiki-matrix-math
- claim: 单行矩阵称为行矩阵或行向量，单列矩阵称为列矩阵或列向量；行数与列数相同的矩阵称为方阵。
  claim_id: mx-special
  support: direct
  supporting_quotes:
  - evidence_id: evidence-cfc56980b96c
    exact: |-
      Matrices with a single row are called row matrices or row vectors, and those with a single column are called column matrices or column vectors. A matrix with the same number of rows and columns is called a square matrix.
  targets:
  - evidence_id: evidence-cfc56980b96c
    source_id: wiki-matrix-math
- claim: 矩阵可用于紧凑地书写和处理多个线性方程，即线性方程组。
  claim_id: mx-linear-eq
  support: direct
  supporting_quotes:
  - evidence_id: evidence-5e6f5a199d47
    exact: |-
      Matrices can be used to compactly write and work with multiple linear equations, that is, systems of linear equations.
  targets:
  - evidence_id: evidence-5e6f5a199d47
    source_id: wiki-matrix-math
- claim: 计算矩阵乘积 A·B 时，A 以行主序、B 以列主序存储最佳——程序员或编译器可依据扫描顺序选择多维数组的行主序或列主序布局。
  claim_id: mx-layout
  support: direct
  supporting_quotes:
  - evidence_id: evidence-45144fe6c9df
    exact: |-
      For example, when computing the product A·B of two matrices, it would be best to have A stored in row-major order, and B in column-major order.
  - evidence_id: evidence-4ae1136a3f28
    exact: |-
      Many algorithms that use multidimensional arrays will scan them in a predictable order. A programmer (or a sophisticated compiler) may use this information to choose between row- or column-major layout for each array.
  targets:
  - evidence_id: evidence-45144fe6c9df
    source_id: wiki-array-cs
  - evidence_id: evidence-4ae1136a3f28
    source_id: wiki-array-cs
id: matrix
kind: reference
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- wiki-matrix-math
- wiki-array-cs
- working-computer-science-matrix
status: published
tags:
- data-structure
- matrix
- linear-algebra
- memory-layout
title: 矩阵
updated_at: '2026-09-05'
---
# 矩阵

## 一句话结论

矩阵是**按行和列排布的矩形数组**（数学对象），在计算机中落成二维数组的行主序/列主序两种布局。它的性能要点不在数学而在**存储顺序与扫描顺序的一致性**——让最内层循环沿连续内存方向跑，缓存命中率决定矩阵运算快慢一个数量级。

## 核心概念

- **条目/元素**：矩阵中的数；横排为行、竖排为列。
- **维度**：m 行 n 列记作 m×n。
- **行向量 / 列向量 / 方阵**：单行、单列、行列数相同。
- **行主序 / 列主序**：二维数组线性化的两种方式（C 风格 vs Fortran 风格）。

## 工作机制

### 存储布局

```text
A = | 1 9  -13 |      行主序内存序列: 1, 9, -13, 20, 5, -6
    | 20 5  -6 |      列主序内存序列: 1, 20, 9, 5, -13, -6

行主序: addr(A[i][j]) = base + (i·ncols + j) · size
列主序: addr(A[i][j]) = base + (j·nrows + i) · size
```

### 布局选择原则

使用多维数组的算法按可预测顺序扫描：让扫描方向与内存连续方向一致。矩阵乘 A·B 的三重循环中，A 按行访问、B 按列访问——A 存行主序、B 存列主序时两个访存流都连续，性能最佳。

## 常见误区

- **"矩阵乘法慢是算法问题"**：朴素三重循环的访存模式同样关键——布局错了缓存全 miss；BLAS 的分块（tiling）就是在补这个。
- **"行主序比列主序好"**：无优劣，只有与扫描顺序匹配与否；numpy 同时提供 C order 与 F order。
- **"数学矩阵就是二维数组"**：数学上矩阵受加法/乘法性质约束；二维数组只是它的容器，稀疏矩阵等另有专门存储。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| mx-definition / mx-entries / mx-size / mx-special / mx-linear-eq | wiki-matrix-math（Wikipedia） | 矩阵定义、条目行列、尺寸维度、行/列向量与方阵、线性方程组 |
| mx-layout | wiki-array-cs（Wikipedia） | A·B 乘法布局选择与行/列主序原理 |

## 待验证项

无。

## 关联知识

- [[arrays]] —— 矩阵的底层容器：二维数组的地址公式与局部性。
- [[arm-neon]] / [[compiler-vectorization]] —— 矩阵运算的向量化加速。
- [[image-scaling]] / [[color-correction-and-3d-lut]] —— ISP 中矩阵变换的工程应用。

## 详细章节

### 定义

矩阵是矩形数组：数或其他数学对象的元素（条目）按行列排布，通常满足加法与乘法的特定性质。横排为行、竖排为列；m 行 n 列称 m×n 矩阵，m、n 称为维度。单行/单列分别称行向量/列向量；行列数相同称方阵。

### 应用

- 紧凑书写与求解线性方程组（Ax = b）。
- 图的邻接矩阵、图像变换、3D 变换（图形学）。
- ISP：色彩校正矩阵（CCM）、3D LUT。
- 机器学习：张量运算的基础。

## 参考

- https://en.wikipedia.org/wiki/Matrix_(mathematics)
- https://en.wikipedia.org/wiki/Array_(data_structure)#Row-_and_column-major_order
