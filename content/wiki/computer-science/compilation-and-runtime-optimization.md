---
aliases: []
confidentiality: public
domain: computer-science
evidence:
- claim: Optimizations are implemented as Passes that traverse some portion of a program
    to either collect information or transform the program.
  claim_id: compilation-and-runtime-optimization-audit-1
  support: direct
  supporting_quotes:
  - evidence_id: evidence-e5a7dc42e0a0
    exact: Optimizations are implemented as Passes that traverse some portion of a
      program to either collect information or transform the program.
  targets:
  - evidence_id: evidence-e5a7dc42e0a0
    source_id: web-computer-science-compilation-and-runtime-optimization
id: compilation-and-runtime-optimization
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-compilation-and-runtime-optimization
- working-computer-science-compilation-and-runtime-optimization
status: published
tags:
- compiler
- llvm
- optimization
- linker
title: 编译与运行优化
updated_at: '2026-09-06'
---
# 编译与运行优化

## 一句话结论

编译与运行优化覆盖编译器前端（预编译、词法分析、语法分析、语义分析）、中端（中间代码及其中间代码优化，包括死代码删除、过程间优化、内联优化、循环优化、向量化等）与后端（目标代码生成、目标文件格式），最后经汇编与链接（静态/动态链接、链接时优化）产出可运行程序；优化以遍历程序片段的 Pass 形式实现。

## 核心概念

- **编译流程**：编译器把源程序一步步转换为目标程序的整体过程。
- **LLVM 编译器架构**：LLVM 将编译器划分为前端、中端、后端三个部分。
- **编译器前端**：包括预编译、词法分析、语法分析、语义分析等阶段。
- **编译器中端**：围绕中间代码展开，中间代码先于优化存在，中端执行各类中间代码优化。
- **编译器后端**：负责目标代码生成与目标文件格式处理。
- **汇编和链接**：把目标文件汇编并链接成可执行程序，链接分为静态链接、动态链接，还包括链接时优化。
- **Pass（优化遍）**：优化以 Pass 形式实现，每个 Pass 遍历程序的某一部分来收集信息或变换程序。

## 工作机制

- **前端**：预编译 → 词法分析 → 语法分析 → 语义分析，将源程序转换为可供中端处理的中间表示。
- **中端**：先生成中间代码，再执行中间代码优化；优化手段包括编译优化选项、死代码删除、过程间优化、内联优化、循环优化（循环展开、循环分布、循环剥离）、向量化（循环向量化、块级向量化）、浮点优化、数据预取等。
- **后端**：目标代码生成与目标文件格式处理，产出目标文件。
- **汇编和链接**：汇编目标文件；链接分静态链接与动态链接；链接时优化在链接阶段实施优化。
- **Pass 机制**：优化被实现为 Pass——遍历程序某一部分，要么收集信息，要么变换程序（compilation-and-runtime-optimization-audit-1）。

## 示例或代码

原稿为章节骨架，未提供代码示例。相关编译优化选项与示例可参见 [[gcc]]、[[loop-optimization]]、[[statement-optimization]] 等页。

## 常见误区

- **把编译流程当作单一环节**：实际编译贯穿前端（预编译/词法/语法/语义）、中端（中间代码与优化）、后端（目标代码生成）以及汇编与链接多个阶段。
- **认为优化只发生在某个阶段**：优化既出现在中端的中间代码优化，也出现在后端的链接时优化（LTO）。
- **把链接当作简单合并**：链接分为静态链接与动态链接，二者在行为与产物上有区别，此外还存在链接时优化。

## 证据映射

| claim_id | 来源 | 要点 |
| --- | --- | --- |
| compilation-and-runtime-optimization-audit-1 | web-computer-science-compilation-and-runtime-optimization | 优化以 Pass 形式实现，Pass 遍历程序某一部分来收集信息或变换程序 |

## 待验证项

- 本文为迁移生成的目录骨架，各章节正文待补充并逐一核实来源。

## 关联知识

- [[compilation-principle]]：编译原理（编译四步、词法/语法/语义分析、中间代码、代码优化）
- [[gcc]]：GCC 编译器的使用与优化选项
- [[loop-optimization]]：循环级优化
- [[statement-optimization]]：语句级优化
- [[compilers-on-linux]]：Linux 下的编译器

## 详细章节

### 编译与运行优化

#### 概述

##### 编译流程



##### LLVM编译器架构



#### 编译器前端

##### 预编译



##### 词法分析



##### 语法分析



##### 语义分析



##### 相关选项



#### 编译器中端

##### 中间代码



##### 中间代码优化



###### 编译优化选项

###### 死代码删除

###### 过程间优化



###### 内联优化

###### 循环优化

###### 循环展开



###### 循环分布



###### 循环剥离



###### 向量化

###### 循环向量化

###### 块级向量化



###### 浮点优化

###### 数据预取



##### 相关选项





#### 编译器后端

##### 目标代码生成



##### 目标文件格式



##### 相关选项



#### 汇编和链接

##### 汇编



##### 链接

###### 静态链接

###### 动态链接

###### 静态链接 vs 动态链接



###### 链接时优化





##### 相关选项
