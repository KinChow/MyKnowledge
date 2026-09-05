---
aliases: []
confidentiality: public
domain: multimedia
evidence:
- claim: 图像缩放是对数字图像进行调整大小的过程。
  claim_id: image-scaling-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-dfa749e56cd3
    exact: In computer graphics and digital imaging, image scaling is the resizing of a digital image.
  targets:
  - evidence_id: evidence-dfa749e56cd3
    source_id: wikipedia-image-scaling-v2
id: image-scaling
kind: reference
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- wikipedia-image-scaling-v2
- working-multimedia-image-scaling
status: published
tags:
- needs-fact-check
- web-source-added
- working-migration
title: 图像缩放
updated_at: '2026-09-05'
---
# 图像缩放

## 来源与迁移记录

### 迁移与校验记录

- 原始位置：`content/working/c-intermediate/multimedia/image-scaling.md`
- 原文快照：`working-multimedia-image-scaling`（personal-note；用于保留作者原始整理，不等同于外部权威来源）
- 外部链接：1 条；链接仅作为待补来源线索，尚未自动认定为事实依据。
- 当前状态：`draft`；事实正确性、来源逐条对应和必要的权威来源补齐待人工审查。

### 来源补充
- 来源隔离：当前绑定中的 `web-multimedia-image-scaling` 经正文检查确认是错误页/残留文本，已移除当前引用；Source 文件和历史审计记录保留。

- 已联网读取：`https://en.wikipedia.org/wiki/Image_scaling`；来源正文已保存为不可变 Source 快照。

## 详细章节

### 图像缩放

#### 应用背景

改变图像的分辨率，以适应不同尺寸的显示设备和不同的图像使用场景（预览/拍照/录像的多分辨率输出、缩略图、分辨率适配等）。缩放质量直接影响清晰度与观感，是 ISP/视频链路的基本能力。

#### 实现方法

对缩放后的像素点在原图像中相对坐标点进行计算——即逆向映射：目标像素坐标经缩放比例映射回原图坐标（可能为浮点），再按插值算法取原图邻域像素计算输出值。不同插值算法在锐度、平滑度、计算量上权衡。

##### 最近邻域插值

取映射坐标最近的原图像素作为输出，不做任何计算。优点：最快、不引入新颜色；缺点：放大出现明显锯齿/马赛克，缩小产生摩尔纹与信息丢失。适用于实时预览或对质量要求低的场合。

##### 双线性插值

取映射坐标周围 2×2 个原图像素，按距离做两次线性插值（先水平后垂直）。优点：平滑、计算量适中，是默认缩放方案；缺点：边缘被模糊，放大仍不够锐利。

##### 双三次插值

取映射坐标周围 4×4 个原图像素，用三次核（如 Catmull-Rom/Bicubic）加权。优点：比双线性更锐利、振铃更少，图像质量更高；缺点：计算量大，可能引入轻微过冲（overshoot）。

##### 带边缘检测的图像放大算法

先检测图像边缘方向，沿边缘方向插值、垂直边缘方向抑制，避免边缘被模糊；或采用边缘自适应/内容自适应放大（如 Lanczos、基于梯度导向插值、深度学习超分）。质量最好但复杂度最高，用于高质量放大（如夜景/高倍变焦）。

#### 实现难度

##### 锯齿

放大时边缘出现阶梯状锯齿，源于插值未考虑边缘方向。缓解：边缘感知插值、抗锯齿滤波、超采样（多相位缩放）。

##### 模糊

缩小/放大平滑插值导致细节与边缘模糊。缓解：锐化后处理、边缘增强型插值、内容自适应缩放；缩小前先做低通滤波避免混叠。

#### 参考
- 最近邻/双线性/双三次插值：https://en.wikipedia.org/wiki/Image_scaling
- 高质量图像插值综述：Gonzalez R C, Woods R E. Digital Image Processing[M]. 4th ed, 2018
