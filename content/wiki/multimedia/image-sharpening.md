---
aliases: []
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
kind: reference
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- wikipedia-unsharp-masking-v2
- working-multimedia-image-sharpening
status: published
tags:
- needs-fact-check
- web-source-added
- working-migration
title: 锐化
updated_at: '2026-09-05'
---
# 锐化

## 来源与迁移记录

### 迁移与校验记录

- 原始位置：`content/working/c-intermediate/multimedia/image-sharpening.md`
- 原文快照：`working-multimedia-image-sharpening`（personal-note；用于保留作者原始整理，不等同于外部权威来源）
- 外部链接：1 条；链接仅作为待补来源线索，尚未自动认定为事实依据。
- 当前状态：`draft`；事实正确性、来源逐条对应和必要的权威来源补齐待人工审查。

### 来源补充
- 来源隔离：当前绑定中的 `web-multimedia-image-sharpening` 经正文检查确认是错误页/残留文本，已移除当前引用；Source 文件和历史审计记录保留。

- 已联网读取：`https://en.wikipedia.org/wiki/Unsharp_masking`；来源正文已保存为不可变 Source 快照。

## 详细章节

### 锐化

#### DE 概述

DE：Detail Enhancement 细节增强

RAWNF模块能够过滤掉图片中的噪声，并保留边缘信息；但是会导致一些纹理和高频的细节丢失。

DE模块就是用来恢复和提升细节信息用的。



#### DE 原理

$$
FinalNoise = A*HF(noise) + B* MF(noise) + C*LF(noise) \\

Y' = Y + FinalNoise \\

noise = RAWNF_{input} - RAWNF_{output} \\
$$



* Y是上一级模块的输出，Y'是DE模块的输出。
* HF/MF/LF是从RAWNF输出的noise中提取的高频/中频/低频信息。
* A, B, C是HF/MF/LF的增益系数，用来控制加回的强度。



#### Sharpen

##### Sharpen概念

锐度：摄影媒介处理图像边缘反差的程度。

* 高锐度图像的边缘清晰而且边缘部分的反差较大，所以整个图像看上去清晰，引人注目。
* 低锐度图像的边缘模糊，不清哳。



锐化：增加图像边缘反差的过程。

普通的相机sensor和镜头出图不够清晰，通过做锐化，可以使图像升级到高端相机镜头的图像质量。

对于数码相机，这种不清晰是由相机传感器的抗锯齿滤镜和去马赛克处理引起的，此外跟相机的镜头也有关系。



##### Sharpen原理

虽然锐化过程尤法重建上面的理想图像，但是它可以创建更明显的边缘外观。有效锐化的关键是在使边缘看起来足够明显之间达成微妙的平衡，同时还要使可见的under and overshoots（称为“锐化光晕”）最小化。



##### Unsharp Mask

通过减去低通滤波的图像，得到Unsharp Mask（高频信息，边缘信息）。
通过高对比度图像、边缘信息、原始图像得到锐化后的图像。



#### 算法原理

要想实现更好的sharpen效果，只做USM是不够的，还要做Clipping。
Clipping的作用是去除/降低overshoot和undershoot
#### 参考
- Unsharp Mask：https://en.wikipedia.org/wiki/Unsharp_masking
- 锐化与光晕控制：Gonzalez R C, Woods R E. Digital Image Processing[M]. 4th ed, 2018
