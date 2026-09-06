---
aliases: []
confidentiality: public
domain: computer-science
evidence:
- claim: "* 全连接 Fully Connected Layer\n  * Feed forward, fully connected\n  * Multilayer
    Perceptron (MLP)\n* 卷积层 Convolutional Layer\n  * Feed forward, sparsely-connected,
    weight shading\n  * Convolutional Neural Network (CNN)\n  * Typically used for
    images\n* 循环网络 Recurrent Layer\n  * Feedback\n  * Recurrent Neural Network (RNN/LSTM)\n
    \ * Typically used for sequential data (e.g., speech, language)\n* 注意力机制 Attention "
  claim_id: calculate-mode-audit-1
  support: personal
  supporting_quotes:
  - evidence_id: evidence-d5d051b97c6c
    exact: "* 全连接 Fully Connected Layer\n  * Feed forward, fully connected\n  * Multilayer
      Perceptron (MLP)\n* 卷积层 Convolutional Layer\n  * Feed forward, sparsely-connected,
      weight shading\n  * Convolutional Neural Network (CNN)\n  * Typically used for
      images\n* 循环网络 Recurrent Layer\n  * Feedback\n  * Recurrent Neural Network (RNN/LSTM)\n
      \ * Typically used for sequential data (e.g., speech, language)\n* 注意力机制 Attention "
  targets:
  - evidence_id: evidence-d5d051b97c6c
    source_id: working-computer-science-calculate-mode
id: calculate-mode
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- working-computer-science-calculate-mode
status: published
tags:
- ai
- neural-network
- deep-learning
- model-compression
- quantization
- pruning
title: 计算模式
updated_at: '2026-09-06'
---
# 计算模式

## 一句话结论

计算模式围绕 AI 三大范式（监督学习、非监督学习、强化学习）与神经网络结构设计演进展开：主流网络模型分为全连接、卷积、循环、注意力四类，核心计算是权重求和，并通过激活函数引入非线性；为降低部署与运行开销，可采用模型量化（减少权重/激活的比特数）与网络剪枝（删除冗余、非关键权重）两类压缩手段。

## 核心概念

- **AI 三大范式流程**：监督学习、非监督学习、强化学习。
- **神经网络**：主要计算为权重求和。
- **激活函数**：tanh、ReLU、Sigmoid、Linear。
- **主流网络模型结构**：全连接层、卷积层、循环网络、注意力机制。
- **模型量化**：通过减少权重表示或激活所需的比特数来压缩模型。
- **网络剪枝**：研究模型权重中的冗余，尝试删除/修剪冗余和非关键的权重。

## 工作机制

### 主流网络模型结构
- **全连接 Fully Connected Layer**：前馈、全连接，即多层感知机（MLP）。
- **卷积层 Convolutional Layer**：前馈、稀疏连接、权重共享，即卷积神经网络（CNN），典型用于图像。
- **循环网络 Recurrent Layer**：带反馈，即循环神经网络（RNN/LSTM），典型用于序列数据（如语音、语言）。
- **注意力机制 Attention Layer**：注意力（矩阵乘）＋前馈、全连接，支撑基础模型（Foundation Models）与 Transformer。

### 压缩手段
- **网络剪枝**：研究模型权重中的冗余，删除/修剪冗余和非关键的权重。
- **模型量化**：通过减少权重表示或激活所需的比特数来压缩模型。

### 低比特量化特征
1. 参数压缩；
2. 提升速度；
3. 降低内存；
4. 功耗降低；
5. 提升芯片面积。

## 示例或代码

**网络结构—特性对照**：

| 结构 | 连接方式 | 典型模型 | 典型应用 |
| --- | --- | --- | --- |
| 全连接 | Feed forward, fully connected | MLP | — |
| 卷积层 | Feed forward, sparsely-connected, weight sharing | CNN | 图像 |
| 循环网络 | Feedback | RNN/LSTM | 序列数据（语音、语言） |
| 注意力机制 | Attention (matrix multiply) + Feed forward, fully connected | Foundation Models / Transformer | — |

**经典网络模型趋势**：模型越大越深。

## 常见误区

- **把量化和剪枝混为一谈**：网络剪枝处理权重中的冗余（删除/修剪非关键权重）；模型量化通过减少权重或激活所需的比特数压缩模型，二者机制不同。
- **忽视低比特量化的多方面收益**：低比特量化同时带来参数压缩、速度提升、内存降低、功耗降低等效果，并非单一指标收益。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| calculate-mode-audit-1 | working-computer-science-calculate-mode | 全连接（前馈全连接/MLP）、卷积层（稀疏连接/CNN/图像）、循环网络（反馈/RNN-LSTM/序列）、注意力机制四类主流网络结构 |

## 待验证项

无。

## 关联知识

- [[transformer]] —— 基于注意力机制的 Transformer 架构。
- [[matrix]] —— 矩阵运算（注意力/权重求和的基础）。
- [[davinci]] —— AI 计算芯片。
- [[gpu-overview]] —— GPU 与并行计算。

## 详细章节

### 计算模式

#### AI 三大范式流程

##### 监督学习

##### 非监督学习

##### 强化学习



#### 网络模型结构设计&演进

##### 神经网络

##### 主要计算：权重求和

###### 激活函数

###### tanh

###### ReLU

###### Sigmoid

###### Linear

##### 主流的网络模型结构

* 全连接 Fully Connected Layer
  * Feed forward, fully connected
  * Multilayer Perceptron (MLP)
* 卷积层 Convolutional Layer
  * Feed forward, sparsely-connected, weight shading
  * Convolutional Neural Network (CNN)
  * Typically used for images
* 循环网络 Recurrent Layer
  * Feedback
  * Recurrent Neural Network (RNN/LSTM)
  * Typically used for sequential data (e.g., speech, language)
* 注意力机制 Attention Layer
  * Attention (matrix multiply) + Feed forward, fully connected
  * Foundation Models
  * Transformer



##### 经典网络模型

模型越大越深



#### 模型量化&网络剪枝

##### 量化压缩 vs 网络剪枝

网络剪枝研究模型权重中

的冗余， 并尝试删除/修剪

冗余和非关键的权重。



模型量化是指通过减少权

重表示或激活所需的比特

数来压缩模型。



##### 低比特量化特征

1. 参数压缩；
2. 提升速度；
3. 降低内存；
4. 功耗降低；
5. 提升芯片面积；
