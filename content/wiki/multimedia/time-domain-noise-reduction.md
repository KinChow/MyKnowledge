---
aliases:
- 时域降噪
- TNR
- Temporal Noise Reduction
- 多帧降噪
- 3DNR
confidentiality: public
domain: multimedia
evidence:
- claim: 图像处理中有许多降噪算法；选择降噪算法时需要权衡可用算力与时间、是否接受牺牲细节以换取更多噪声去除、以及图像中噪声与细节的特性。
  claim_id: time-domain-noise-reduction-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-04c098537dac
    exact: |-
      There are many noise reduction algorithms in image processing. In selecting a noise reduction algorithm, one must weigh several factors: the available computer power and time available; whether sacrificing some real detail is acceptable if it allows more noise to be removed; and the characteristics of the noise and the detail in the image, to better make those decisions.
  targets:
  - evidence_id: evidence-04c098537dac
    source_id: wiki-noise-reduction
id: time-domain-noise-reduction
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- wiki-noise-reduction
- working-multimedia-time-domain-noise-reduction
status: published
tags:
- camera
- isp
- denoise
- temporal
- video
- multimedia
title: 时域降噪
updated_at: '2026-09-05'
---

# 时域降噪

## 一句话结论

时域降噪利用图像噪声在帧间随机出现、不具有相关性，而图像内容在帧间高度相关、连续变化的特点进行降噪。基本方法分两类：多图平均（拍照多帧加权平均）与运动估计/运动补偿（视频沿运动轨迹滤波）。进阶算法包括梯度方向算法（只对帧间噪声点时域滤波、保护细节）与 MASTF 运动自适应时空滤波（静态区时域平均、动态区时空域+运动补偿）。主要难点是配准（对齐不好导致模糊）、拖影（剧烈运动）与实时性能；2D 降噪牺牲清晰度、3D 降噪增加拖影，需按场景权衡。

## 核心概念

- **时域降噪原理**：噪声帧间随机不相关、内容帧间相关连续 → 沿时间方向滤波可在不伤细节的情况下去噪。
- **多图平均算法**：对同一场景多张图配准后加权平均，主要应用于拍照。
- **运动估计算法**：将当前帧分块，在参考帧中寻找最相近块，沿运动方向降噪，应用于视频。
- **运动补偿算法**：先运动估计再沿运动轨迹滤波。
- **梯度方向算法**：通过方向梯度将像素分为噪声点/边界点/内部点，只对噪声点时域滤波。
- **MASTF**：MOTION ADAPTIVE SPATIO-TEMPORAL FILTER，运动自适应时空滤波，静态/动态分区处理。
- **2D vs 3D 降噪**：2D 牺牲清晰度，3D 增加移动目标拖影。

## 工作机制

1. **多图平均**：输入多张连续图片 → 配准对齐 → 像素加权平均 → 输出合成图像。
2. **运动估计**：当前帧分为互不重叠的块，以前一帧为参考帧，按一定原则找到最相近参考块，沿运动方向滤波。
3. **梯度方向算法**：分析帧内邻域像素特点，用方向梯度把像素分为噪声点/边界点/内部点，只对帧间噪声点时域降噪 → 减少计算量并保护细节。
4. **MASTF 五步**：Moving Pixel Detection → Temporal Average Filter → Spatio-Temporal Noise Reduction Filter → Image Fusion → 2-D Adaptive Filter in Static Regions；静态区域直接时域平均、动态区域时空域结合+运动补偿。

## 示例或代码

```text
多图平均流程：
  开始 → 输入多张连续图片 → 图片序列配准对齐 → 像素加权平均 → 输出合成图像 → 结束

MASTF 五步：
  1. Moving Pixel Detection（运动像素检测）
  2. Temporal Average Filter（时域平均滤波）
  3. Spatio-Temporal Noise Reduction Filter（时空降噪滤波）
  4. Image Fusion（图像融合）
  5. 2-D Adaptive Filter in Static Regions（静态区 2D 自适应滤波）

典型权衡：
  2D 降噪：牺牲清晰度，降噪强度越高清晰度下降越严重
  3D 降噪：增加移动目标拖影，降噪强度越高拖影越厉害
```

## 常见误区

- **"时域降噪只用于视频"**：多图平均用于拍照场景（多帧合成），运动估计/补偿用于视频。
- **"降噪强度越高越好"**：2D 降噪牺牲清晰度、3D 降噪增加拖影，强度与画质需权衡（参见算法选择因素）。
- **"多帧平均不需要对齐"**：配准对齐不好会导致融合后图像模糊，配准是拍照多帧降噪的关键难点。
- **"静态区和动态区可以一样处理"**：MASTF 的核心是分区——静态区直接时域平均（不伤细节），动态区才需要时空域+运动补偿。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| time-domain-noise-reduction-definition | wiki-noise-reduction | 选降噪算法需权衡算力/细节取舍/噪声与细节特性 |

## 待验证项

- 多图平均、运动估计、梯度方向算法、MASTF 等具体算法描述来自内部工作笔记（working-multimedia-time-domain-noise-reduction），无公开权威来源，待人工复核。

## 关联知识

- [[frequency-domain-noise-reduction]] —— 频域降噪（WNR 等）。
- [[noise-evaluation]] —— 噪声分类与评价，Temporal noise 的定义。
- [[image-stabilization]] —— 帧间对齐与运动估计相关。
- [[isp-system]] —— 时域降噪模块在 ISP 流水线中的位置。
- [[terminology]] —— MCTF/MFNR/TNR 等术语。

## 详细章节

### 时域降噪的背景、原理

背景介绍：

- 图像内容在帧间具有很强的相关性，且每一帧内都是连续变化的；
- 图像噪声在帧间总是随机出现，不具有相关性，每帧内也是不连续的。

基本思想：

时域滤波利用噪声在帧间随机的、不连续的特点进行降噪。

### 时域降噪的常用算法、基本步骤

基本方法：

- 多图平均算法：主要应用于拍照场景降噪
- 运动估计算法：主要应用于视频场景降噪

#### 多图平均算法

其核心思想就是针对同一场景拍摄多张图，进行加权平均处理。

- 开始
- 输入多张连续图片
- 图片序列配准对齐
- 像素加权平均处理
- 输出合成图像
- 结束

#### 运动估计算法

先进行运动估计，然后沿着物体运动方向进行降噪处理。

#### 运动补偿算法

视频噪声特征分析：

- 每一帧的图像内容具有高度相关性。
- 高斯噪声在帧间不具有连续性。

时域降噪处理模型：

- 在时域上很好地获得物体的运动轨迹
- 沿着物体的运动轨迹对噪声进行有效的滤波

运动估计算法原理：

- 当前帧分为一定数量互不重叠的块，把前一帧作为参考帧。
- 在参考帧中按一定原则和策略找到和当前块最相近的参考块。

#### 梯度方向算法

基本思想：

通过分析帧内邻域像素特点，使用方向梯度原理，将像素点分为噪声点、边界点和内部点。只对帧间噪声点进行时域降噪处理。

算法优点：

- 该降噪算法在去除视频序列噪声的同时，也能很好地保护图像的细节。
- 通过像素点的划分，减少了不必要的计算量，以提升了算法性能。

#### MASTF算法

算法全称：MOTION ADAPTIVE SPATIO-TEMPORAL FILTER。

运动自适应降噪滤波器的框图，有五个重要步骤：

1. Moving Pixel Detection
2. Temporal Average Filter
3. Spatio-Temporal Noise Reduction Filter
4. Image Fusion
5. 2-D Adaptive Filter in Static Regions

主要特点：

1. 根据运动检测对图像进行分区，即静态区域和动态区域；
2. 对静态区域直接使用时域多图平均算法；
3. 对动态区域使用时空域结合算法，并用到了运动补偿算法。

算法优势：

在取得较好降噪效果的同时，也能获得较好的降噪性能。

### 时域降噪的问题、难点和优化方法

#### 时域降噪问题

- 配准问题：对于拍照多帧融合去噪处理时，如果图像对齐处理不好，会导致融合后图像模糊；
- 拖影问题：对于剧烈运动、变化较快的图像，容易产生"拖影"问题；
- 性能问题：对于视频降噪中，对实时性、流畅性要求高，参考帧选择不当会严重影响视频体验。

2D 降噪会牺牲清晰度，降噪强度越高相应画面清晰度会下降越严重。

3D 降噪会增加移动目标拖影，降噪强度越高，拖影越厉害。

#### 优化方法

优化配准：

- 保证拍摄图像的稳定
- 控制前后参考帧数量
- 结合运动检测的算法

减少拖影：

- 优化运动估计算法
- 计算物体运动强度
- 选择合适的融合帧数

提高性能：

- 图像的运动检测分区
- 图像的噪声进行分类
- 选择合适的融合帧数

## 参考

- 时域/时空域降噪：https://en.wikipedia.org/wiki/Noise_reduction
- MASTF 运动自适应时空滤波：参考 3DNR 专利与厂商白皮书
