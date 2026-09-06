---
aliases: []
confidentiality: public
domain: computer-science
evidence:
- claim: Transformer 是一种仅基于注意力机制、完全不使用循环和卷积的网络架构。
  claim_id: transformer-audit-1
  support: direct
  supporting_quotes:
  - evidence_id: evidence-edeba6920028
    exact: We propose a new simple network architecture, the Transformer, based solely
      on attention mechanisms, dispensing with recurrence and convolutions entirely.
  targets:
  - evidence_id: evidence-edeba6920028
    source_id: arxiv-transformer-v2
id: transformer
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- arxiv-transformer-v2
- working-computer-science-transformer
status: published
tags:
- transformer
- attention
- deep-learning
- nlp
- neural-network
title: Transformer
updated_at: '2026-09-06'
---
# Transformer

## 一句话结论

Transformer 是一种仅基于注意力机制、完全不使用循环和卷积的网络架构（出自论文 *Attention Is All You Need*），其组成部分包括自注意力机制、位置编码、编码器和解码器、多头注意力、前馈神经网络、残差连接和层归一化。

## 核心概念

- **自注意力机制**：Transformer 的组成部分。
- **位置编码**：Transformer 的组成部分。
- **编码器和解码器**：Transformer 的组成部分。
- **多头注意力**：Transformer 的组成部分。
- **前馈神经网络**：Transformer 的组成部分。
- **残差连接和层归一化**：Transformer 的组成部分。

## 工作机制

Transformer 由以下部分构成，并以此为基础工作：

- 自注意力机制
- 位置编码
- 编码器和解码器
- 多头注意力
- 前馈神经网络
- 残差连接和层归一化

## 示例或代码

**学习与参考资料示例**：

- 原论文：*Attention Is All You Need*（NeurIPS 2017）。
- Transformer 视频及资料：论文逐段精读、Stanford CS25 - Transformers United、Transformer 教程。
- Vision Transformer 视频及资料：Swin Transformer、Vision Transformer 论文速读。

## 常见误区

- 将 Transformer 与基于循环或卷积的架构混淆——Transformer 完全基于注意力机制，不使用循环和卷积。
- 误以为 Transformer 只包含自注意力——它还包括位置编码、编码器和解码器、多头注意力、前馈神经网络、残差连接和层归一化等组成部分。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| transformer-audit-1 | arxiv-transformer-v2 | Transformer 仅基于注意力机制，完全不使用循环和卷积 |

## 待验证项

无。

## 关联知识

- [[calculate-mode]] —— 网络模型结构（注意力机制 / Transformer）。
- [[matrix]] —— 注意力矩阵乘的基础。
- [[davinci]] —— AI 计算芯片。
- [[gpu-overview]] —— GPU 与并行计算。

## 详细章节

### Transformer

#### 组成部分

自注意力机制

位置编码

编码器和解码器

多头注意力

前馈神经网络

残差连接和层归一化



#### 模型架构



#### 技术优势



#### 原理



#### 学习资料

##### Transformer视频及资料

* [Attention Is All You Need](https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf)
* [Transformer论文逐段精读【论文精读】](https://www.bilibili.com/video/BV1pu411o7BE)
* [Stanford CS25 - Transformers United](https://www.youtube.com/playlist?list=PLoROMvodv4rNiJRchCzutFw5ItR_Z27CM)
* [transformer教程](https://www.bilibili.com/video/BV1mf4y1o7kj/?vd_source=987a80114049bd0d05bfaf4f7a0d1491)



##### Vision Transformer视频及资料

* Swin Transformer

* [Vision Transformer论文速读](https://www.bilibili.com/read/cv20376143/)

## 参考

* [Attention Is All You Need](https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf)
* [Transformer论文逐段精读【论文精读】](https://www.bilibili.com/video/BV1pu411o7BE)
* [Stanford CS25 - Transformers United](https://www.youtube.com/playlist?list=PLoROMvodv4rNiJRchCzutFw5ItR_Z27CM)
* [transformer教程](https://www.bilibili.com/video/BV1mf4y1o7kj/?vd_source=987a80114049bd0d05bfaf4f7a0d1491)
* [Vision Transformer论文速读](https://www.bilibili.com/read/cv20376143/)
