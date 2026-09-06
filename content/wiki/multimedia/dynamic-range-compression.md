---
aliases:
- 动态范围压缩
- Dynamic Range Compression
- DRC
confidentiality: public
domain: multimedia
evidence:
- claim: |-
    In this context, the term high dynamic range means there is a large amount of variation in light levels within a scene or an image. The dynamic range refers to the range of luminosity between the brightest area and the darkest area of that scene or image.
  claim_id: dynamic-range-compression-audit-1
  support: direct
  supporting_quotes:
  - evidence_id: evidence-15fd931b7867
    exact: |-
      In this context, the term high dynamic range means there is a large amount of variation in light levels within a scene or an image. The dynamic range refers to the range of luminosity between the brightest area and the darkest area of that scene or image.
  targets:
  - evidence_id: evidence-15fd931b7867
    source_id: wiki-hdri
id: dynamic-range-compression
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- wiki-hdri
- working-multimedia-dynamic-range-compression
status: published
tags:
- camera
- isp
- dynamic-range
- drc
- multimedia
title: 动态范围压缩
updated_at: '2026-09-04'
---

# 动态范围压缩

## 一句话结论

动态范围（Dynamic Range，也称对比度）是 Sensor 最大/最小输出信号的比值，即图像最亮与最暗部分的灰度比。高动态范围（HDR）指场景/图像中光线水平变化大。动态范围压缩（DRC）的核心功能是让高 Bit 图在低 Bit 显示器上显示时保留更多细节：通过**灰度映射曲线**（核心是直方图均衡 HE/CLAHE）把高动态范围压缩到显示范围。压缩时采用等比压缩会缩小亮度等级差异造成细节丢失；全局（HE/CLAHE）与局部（双边滤波分离高低频、local gamma）方法配合可保留/增强局部细节。

## 核心概念

- **动态范围/对比度**：Sensor 最大/最小输出信号比值；人眼范围约 10⁴ cd/m²，Rec.709 显示约 2⁸ cd/m²。
- **灰度直方图**：横轴亮度等级、纵轴像素占比；量化评测对比度的客观工具。
- **直方图均衡（HE）**：通过映射使直方图覆盖更广，提高对比度；需保证映射后大小关系不变、数值不越界。
- **CLAHE**：对平坦区域 CDF 斜率过大，设固定阈值均分超阈值部分，抑制过度增强噪声。
- **局部增强**：双边滤波分离高低频（低频均衡+高频叠加）、local gamma（分 patch 均衡+边界平滑）。

## 工作机制

1. **分析**：用灰度直方图量化图像亮度分布（对比度评测）。
2. **全局映射**：配置灰度映射曲线（HE：CDF 映射；CLAHE：限幅后均衡），把高动态范围压缩到显示范围，等比压缩会损失细节。
3. **局部增强**：双边滤波把图像分为高频（细节）+低频，低频均衡后叠加增益高频；或 local gamma 分 patch 单独均衡 + 边界平滑，保留/增强局部细节。

## 示例或代码

```text
动态范围（对比度）量级：
  真实世界 10^9 cd/m² | 人眼 10^4 | Rec.709 2^8

直方图均衡（HE）两条件：
  1. 映射后暗点仍是暗点、亮点仍是亮点（大小关系不变）
  2. 映射后不越界（8bit 不超过 0-255）

CLAHE：
  平坦区 CDF 斜率过大 → 设固定阈值均分超阈值部分 → 平缓 CDF → 抑制噪声

局部增强：
  双边滤波 → 高频图（细节）+ 低频图
  低频均衡 + 增益高频 → 全局对比度增强同时保留局部细节
```

## 常见误区

- **"DRC 就是拉高亮度"**：DRC 是动态范围压缩（高 Bit→低 Bit 显示保留细节），核心是灰度映射曲线（直方图均衡）。
- **"压缩不会损失细节"**：等比压缩会缩小亮度等级差异、造成细节丢失。
- **"直方图均衡随便做"**：需保证大小关系不变、数值不越界；平坦区会过度增强噪声（用 CLAHE 限幅）。
- **"全局均衡就够"**：全局增强可能丢失局部细节，需双边滤波/local gamma 等局部方法补充。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| dynamic-range-compression-audit-1 | wiki-hdri | HDR = 场景光线变化大，动态范围 = 最亮最暗亮度范围 |

## 待验证项

无。

## 关联知识

- [[hdr]] —— DRC 处理的是 HDR 合成后的高动态范围图像。
- [[tonemapping]] —— 色调映射与 DRC 同属动态范围压缩。
- [[auto-exposure]] —— 动态范围是 sensor 成像能力的基础指标。

## 详细章节

### 动态范围压缩的定义

#### 对比度定义

动态范围也称作对比度，是衡量成像质量的重要参数。对比度高、画面通透、亮暗分明、层次丰富、质感突出。

#### 对比度压缩

| | 对比度范围 |
| --- | --- |
| 真实世界 | 10⁹ cd/m² |
| 人眼范围 | 10⁴ cd/m² |
| Rec 709 | 2⁸ cd/m² |

黑白照片添加彩色网格后会变成"彩色照片"，说明人眼有一定分辨率，因此过小的亮度差异不容易被人眼识别。

#### 动态范围

动态范围压缩时采用等比压缩，会缩小亮度等级之间的差异，造成细节丢失。动态范围是指 Sensor 支持的最大输出信号和最小输出信号的比值，或者说图像最亮部分与最暗部分的灰度比值，也就是常说的对比度。动态范围压缩的核心功能，就是让高 Bit 图在低 Bit 显示器上显示时，保留多图像细节。

#### 直方图

灰度直方图：横坐标亮度等级，纵坐标为该亮度等级 pix 数量在全部 pix 中的比例。直方图可以清晰反映图像中所有 pix 的分布情况，可以作为量化评测对比度的客观工具。通过特殊的映射关系，将相同亮度值的 pix 映射为其他亮度值，就能改变直方图分布情况，进而改变对比度高低。合理的灰度映射可以使直方图覆盖范围更广、提高图像对比度，这种映射称为直方图均衡。因此配置合理的灰度映射曲线就是 DRC 核心算法。

#### value stretch

由于照明不足、成像传感器动态范围太小等原因，会造成图像对比度过小。对比拉伸的思想是提高图像处理时灰度级的动态范围。

#### 映射曲线

配置灰度映射曲线（DRC 核心）。

### 动态范围压缩的原理

#### 全局

**直方图均衡（HE）**：两个条件必须保证——像素亮度映射后一定保证原来大小关系不变（暗点依旧是暗点、亮点依旧是亮点）；像素亮度映射后数值不能越界（8bit 系统映射后不能超过 0-255 范围）。

**累积分布函数（CDF）**：核心是用某等级亮度下 pix 数量占比，映射出新亮度值。

**CLAHE（Contrast Limited Adaptive histogram equalization）**：图像中的大片平坦区域会造成该区域 CDF 曲线斜率过大。采用设定固定阈值、均分直方图中超过阈值部分的手段，可以明显平缓最终的 CDF 曲线，抑制过度增强噪声。

#### 局部

**双边滤波**：通过双边滤波把图像分为高频和低频两张图，其中高频图就是图像中 local 区域的细节。对低频图做正常的均衡处理后，叠加上经过一定增益的高频图，就实现了在进行全局对比度增强时保留或增强局部细节。

**local gamma**：另一种常见增强局部对比度的方式是使用局部 gamma 曲线。核心原理是将原图分为不同 patch，每个 patch 根据自身直方图分布情况单独做均衡，然后在各 patch 之间边界做好平滑。好处是尽可能多地保留或增加局部细节。

## 参考

- 直方图均衡（HE/CLAHE）：https://en.wikipedia.org/wiki/Adaptive_histogram_equalization
- 双边滤波分离高低频做局部增强：Tomasi C, Manduchi R. Bilateral Filtering for Gray and Color Images[C]. ICCV, 1998
