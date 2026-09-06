---
aliases: []
confidentiality: public
domain: computer-science
evidence:
- claim: Nine major versions of the architecture have been defined to date, denoted
    by the version numbers 1 to 9. Of these, the first three versions are now obsolete
  claim_id: von-neumann-architecture-audit-1
  support: direct
  supporting_quotes:
  - evidence_id: evidence-802fb55860c5
    exact: Nine major versions of the architecture have been defined to date, denoted
      by the version numbers 1 to 9. Of these, the first three versions are now obsolete
  targets:
  - evidence_id: evidence-802fb55860c5
    source_id: arm-a-profile-architectures
id: von-neumann-architecture
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- arm-a-profile-architectures
- working-computer-science-von-neumann-architecture
status: published
tags:
- architecture
- computer-organization
- stored-program
- cpu
title: 冯诺依曼结构
updated_at: '2026-09-06'
---
# 冯诺依曼结构

## 一句话结论

冯·诺依曼结构（存储程序计算机）以**运算单元为中心**，采用**存储程序原理**，指令和数据统一按地址线性编址于存储器，程序由操作者预先存储后由控制器按指令流驱动执行。

## 核心概念

- **存储程序原理**：程序与数据都存放在存储器中，可编程、可存储。
- **以运算单元为中心**的体系结构。
- **按地址访问、线性编址**的存储器空间。
- **控制流由指令流产生**；指令由**操作码和地址码**组成；数据以**二进制**编码。
- 计算机五大部件：运算器、控制器、存储器、输入设备、输出设备。

## 工作机制

1. 一台计算机由**处理器单元**（算术逻辑单元 + 处理器寄存器）、**控制器单元**（指令计数器 + 程序计数器）、内存、更大容量的外部存储（硬盘）以及输入输出设备构成；
2. 计算机程序抽象为：从输入设备读取输入信息，通过运算器和控制器执行存储在存储器里的程序，最终把结果输出到输出设备；
3. 控制器依据指令计数器/程序计数器控制程序流程（不同条件下的分支和跳转），数据以二进制编码存储与运算。

## 示例或代码

- **五大部件归约**：计算机的任何一个部件都可以归到运算器、控制器、存储器、输入和输出设备。
- **存储程序计算机的两个核心点**：可编程、可存储。
- **结构示意图**：`von-neumann-architecture.assets/Von_Neumann_Architecture.jpg`（单一系统总线的体系结构演化）。

## 常见误区

- **“程序无需预存即可执行”**：存储程序计算机必须先通过操作者把程序存入存储器（可编程、可存储）。
- **“控制器和运算器是一回事”**：处理器单元负责算术与逻辑运算（ALU + 寄存器），控制器单元负责控制程序流程（指令计数器 + 程序计数器）。
- **“指令不区分操作码和地址码”**：指令由操作码和地址码组成，数据以二进制编码。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| von-neumann-architecture-audit-1 | arm-a-profile-architectures | 该架构至今定义了 1–9 共九个主要版本，前三版已废弃（此 claim 来自 ARM 架构文档，与本页冯·诺依曼主题相关性较弱，为迁移期遗留引用） |

## 待验证项

无。

## 关联知识

- [[harvard-architecture]] —— 对偶模型：指令/数据分离存储、独立总线。
- [[cpu-and-memory]] —— 存储程序执行与指令流水线。
- [[cpu-history]] —— ENIAC / EDVAC 的历史起源。
- [[instructions]] —— 指令格式、ELF 与程序装载执行。

## 详细章节

### 冯诺依曼结构

存储程序计算机在体系结构上主要特点有：

1. 以运算单元为中心
2. 采用存储程序原理
3. 存储器是按地址访问、线性编址的空间
4. 控制流由指令流产生
5. 指令由操作码和地址码组成
6. 数据以二进制编码



存储程序计算机的两个核心点：

* 可编程
* 可存储



一台计算机包含部分

* 包含算术逻辑单元和处理器寄存器的处理器单元，来完成各种算术和逻辑运算
* 包含指令计算器和程序计数器的控制器单元，用来控制程序的流程，通常是不同条件下的分支和跳转。
* 存储数据和指令的内存
* 更大容量的外部存储 硬盘
* 输入输出设备

简单的想计算机的任何一个部件都可以归到运算器、控制器、存储器、输入和输出设备



计算机程序可以抽象为从输入设备读取输入信息，通过运算器和控制器来执行存储在存储器里的程序，最终把结果输出到输出设备。



<img src="von-neumann-architecture.assets/Von_Neumann_Architecture.jpg" alt="Single system bus evolutions of the architecture" style="zoom:50%;" />
