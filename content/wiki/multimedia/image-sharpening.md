---
aliases:
- 锐化
- Sharpen
- Unsharp Mask
- USM
- 细节增强
confidentiality: public
domain: multimedia
evidence:
- claim: Unsharp masking（USM）是一种图像锐化技术，现已普遍用于数字图像处理软件。
  claim_id: image-sharpening-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-61e3978cb63e
    exact: Unsharp masking (USM) is an image sharpening technique, first implemented in darkroom photography, but now commonly used in digital image processing software.
  targets:
  - evidence_id: evidence-61e3978cb63e
    source_id: wikipedia-unsharp-masking-v2
id: image-sharpening
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- wikipedia-unsharp-masking-v2
- working-multimedia-image-sharpening
status: published
tags:
- camera
- isp
- sharpening
- unsharp-mask
- multimedia
title: 锐化
updated_at: '2026-09-04'
---

# 锐化

## 一句话结论

锐化（Sharpen）是增加图像边缘反差的过程，提升边缘清晰度。普通相机 sensor/镜头出图不够清晰（抗锯齿滤镜、去马赛克导致），锐化可提升到更高镜头质量。核心是 **Unsharp Mask（USM）**：减去低通滤波图像得到高频边缘信息（Unsharp Mask），叠加回原图实现锐化。ISP 中 DE（细节增强）模块在降噪后恢复被滤掉的高频细节（noise 的高/中/低频加权加回）。有效锐化的关键是平衡边缘明显度与"锐化光晕"（overshoot/undershoot，用 Clipping 控制）。

## 核心概念

- **锐度**：媒介处理图像边缘反差的程度；高锐度边缘清晰、反差大。
- **锐化**：增加图像边缘反差；弥补 sensor/镜头/去马赛克的模糊。
- **USM（Unsharp Mask）**：原图 − 低通滤波 = 高频边缘信息，叠加回原图。
- **DE（细节增强）**：降噪后从 noise（输入−输出）提取高/中/低频，加权加回恢复细节。
- **光晕控制**：overshoot/undershoot（锐化光晕）用 Clipping 去除/降低。

## 工作机制

1. **DE 细节增强**：降噪（RAWNF）会滤掉纹理/高频细节——noise = RAWNF_input − RAWNF_output，从中提取 HF/MF/LF，按增益 A/B/C 加回：Y' = Y + A·HF + B·MF + C·LF。
2. **USM 锐化**：原图减低通滤波得 Unsharp Mask（高频边缘），叠加回原图增强边缘反差。
3. **Clipping**：去除/降低 overshoot/undershoot（锐化光晕），保持边缘自然。

## 示例或代码

```text
DE 细节增强：
  noise = RAWNF_input - RAWNF_output
  FinalNoise = A*HF(noise) + B*MF(noise) + C*LF(noise)
  Y' = Y + FinalNoise
  （A/B/C 控制高/中/低频加回强度）

USM 锐化：
  UnsharpMask = 原图 - 低通滤波(原图)   # 高频边缘信息
  锐化图 = 原图 + 增益 * UnsharpMask
  （Clipping 去除 overshoot/undershoot）
```

## 常见误区

- **"锐化越多越清晰"**：过度锐化产生 overshoot/undershoot（锐化光晕），边缘出现黑白过带。
- **"USM 就够了"**：更好效果还需 Clipping 控制光晕。
- **"锐化能修复模糊"**：锐化增强边缘反差、创建更明显的边缘外观，但不能重建理想图像（无法恢复丢失的真实信息）。
- **"锐化与降噪无关"**：ISP 中 DE 依赖降噪后的 noise（输入−输出），两者紧密耦合。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| image-sharpening-definition | wikipedia-unsharp-masking-v2 | USM 是图像锐化技术 |

## 待验证项

无。

## 关联知识

- [[image-scaling]] —— 缩放模糊可用锐化补偿。
- [[space-domain-noise-reduction]] —— DE 与降噪（RAWNF）耦合。
- [[image-quality-assessment]] —— 锐度（MTF/ringing）是清晰度评价维度。

## 详细章节

### DE 概述

DE：Detail Enhancement 细节增强。RAWNF 模块能过滤掉图片中的噪声并保留边缘信息，但会导致一些纹理和高频的细节丢失。DE 模块就是用来恢复和提升细节信息用的。

### DE 原理

$$
FinalNoise = A*HF(noise) + B* MF(noise) + C*LF(noise) \\
Y' = Y + FinalNoise \\
noise = RAWNF_{input} - RAWNF_{output}
$$

- Y 是上一级模块的输出，Y' 是 DE 模块的输出。
- HF/MF/LF 是从 RAWNF 输出的 noise 中提取的高频/中频/低频信息。
- A, B, C 是 HF/MF/LF 的增益系数，用来控制加回的强度。

### Sharpen

#### Sharpen概念

锐度：摄影媒介处理图像边缘反差的程度。高锐度图像的边缘清晰而且边缘部分的反差较大，整个图像看上去清晰、引人注目；低锐度图像的边缘模糊、不清晰。

锐化：增加图像边缘反差的过程。普通的相机 sensor 和镜头出图不够清晰，通过做锐化可以使图像升级到高端相机镜头的图像质量。对于数码相机，这种不清晰是由相机传感器的抗锯齿滤镜和去马赛克处理引起的，此外跟相机的镜头也有关系。

#### Sharpen原理

虽然锐化过程无法重建上面的理想图像，但是它可以创建更明显的边缘外观。有效锐化的关键是在使边缘看起来足够明显之间达成微妙的平衡，同时还要使可见的 under and overshoots（称为"锐化光晕"）最小化。

#### Unsharp Mask

通过减去低通滤波的图像，得到 Unsharp Mask（高频信息，边缘信息）。通过高对比度图像、边缘信息、原始图像得到锐化后的图像。

### 算法原理

要想实现更好的 sharpen 效果，只做 USM 是不够的，还要做 Clipping。Clipping 的作用是去除/降低 overshoot 和 undershoot。

## 参考

- Unsharp Mask：https://en.wikipedia.org/wiki/Unsharp_masking
- 锐化与光晕控制：Gonzalez R C, Woods R E. Digital Image Processing[M]. 4th ed, 2018
