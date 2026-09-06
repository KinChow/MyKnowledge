---
aliases: []
confidentiality: public
domain: computer-science
evidence:
- claim: 计算机算术研究计算机中的数字表示及算术运算的相应实现。
  claim_id: computer-arithmetic-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-90a430a0a898
    exact: Computer arithmetic is the scientific field that deals with representation
      of numbers on computers and corresponding implementations of the arithmetic
      operations.
  targets:
  - evidence_id: evidence-90a430a0a898
    source_id: wikipedia-computer-arithmetic-v2
id: operations
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- wikipedia-computer-arithmetic-v2
- working-computer-science-operations
status: published
tags:
- computer-arithmetic
- number-representation
- digital-circuit
title: 运行
updated_at: '2026-09-06'
---
# 运行

## 一句话结论

计算机算术研究计算机中数字的表示及算术运算的相应实现，包含两大主题：二进制编码（整数和补码、字符串和 Unicode、浮点数和定点数）与数字电路（门电路、加法器、乘法器）。

## 核心概念

- **计算机算术**：研究计算机中数字的表示方式以及算术运算的相应实现。
- **二进制编码**：包含整数和补码、字符串和 Unicode、浮点数和定点数等表示方式。
- **数字电路**：包含门电路、加法器、乘法器等实现算术运算的电路单元。

## 工作机制

- 表示层：先在计算机中用二进制对数字（整数、浮点数、定点数等）与非数字数据（字符串、Unicode）进行编码；
- 实现层：再通过门电路构造加法器、乘法器等数字电路，把算术运算落实到硬件实现。

## 示例或代码

详细章节当前为提纲占位，暂无具体示例与代码。

## 常见误区

无（详细章节为提纲占位，暂无误区相关内容）。

## 证据映射

| claim_id | 来源 | 要点 |
| --- | --- | --- |
| computer-arithmetic-definition | wikipedia-computer-arithmetic-v2 | 计算机算术是研究计算机中数字表示及算术运算相应实现的科学领域 |

## 待验证项

- [ ] 二进制编码下的"整数和补码 / 字符串和 Unicode / 浮点数和定点数"各小节当前为空，待补充内容；
- [ ] 数字电路下的"门电路 / 加法器 / 乘法器"各小节当前为空，待补充内容；
- [ ] 各小节补充权威来源并升级证据。

## 关联知识

- [[von-neumann-architecture]] —— 运算器、控制器等五大部件的冯·诺依曼结构
- [[cpu-and-memory]] —— CPU 与内存机制
- [[instructions]] —— 指令与二进制表示

## 详细章节

### 运行

#### 二进制编码

##### 整数和补码



##### 字符串和Unicode



##### 浮点数和定点数



#### 数字电路

##### 门电路



##### 加法器



##### 乘法器

