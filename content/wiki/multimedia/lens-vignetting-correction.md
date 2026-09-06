---
aliases:
- 镜头暗角校正
- Lens Vignetting Correction
- Lens Shading
- 暗角
- 渐晕
confidentiality: public
domain: multimedia
evidence:
- claim: 暗角是图像边缘相对于中心亮度或饱和度降低的现象。
  claim_id: vignetting-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-2342d6d34d74
    exact: In photography and optics, vignetting is a reduction of an image's brightness or saturation toward the periphery compared to the image center.
  targets:
  - evidence_id: evidence-2342d6d34d74
    source_id: wikipedia-vignetting-v2
id: lens-vignetting-correction
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- wikipedia-vignetting-v2
- working-multimedia-lens-vignetting-correction
status: published
tags:
- camera
- lens
- isp
- vignetting
- multimedia
title: 镜头暗角校正
updated_at: '2026-09-04'
---

# 镜头暗角校正

## 一句话结论

暗角（Vignetting / Lens Shading）是图像边缘相对中心亮度或饱和度降低的现象：镜头的通光量从中心到边角减小（Luma shading / 亮度均匀性），或 RGB plane 不重合（Color shading / 色彩均匀性）。Luma shading 源于 lens 机械结构与光学特性，Color shading 源于 Lens 折射率与 CRA 不匹配。暗角校正（Lens Shading Correction，LSC）基本思想是 PCOR(x,y) = P_IN(x,y) × F(x,y)，用分块 + 双线性插值生成矫正函数；评测用均匀光源（A/C/D65）客观 + 单色物体主观。

## 核心概念

- **暗角（Vignetting）**：图像边缘相对中心亮度/饱和度降低。
- **Luma shading**：通光量中心→边角减小，中心亮四周渐暗（亮度均匀性）。
- **Color shading**：RGB plane 不重合，中心与四周颜色不一致（色彩均匀性）。
- **成因**：Luma——lens 机械结构/光学特性（中间穿透力强）；Color——Lens 折射率、CRA 不匹配（微透镜 CRA vs Lens CRA）。
- **校正**：PCOR = P_IN × F(x,y)；分 NxM 中心对称 block + 双线性插值。

## 工作机制

1. **成因**：Luma shading（通光量径向衰减）与 Color shading（RGB 平面不重合）导致中心/边缘亮度或颜色不一致。
2. **校正函数**：对每个像素乘矫正因子 F(x,y)，PCOR(x,y) = P_IN(x,y) × F(x,y)，依赖像素坐标。
3. **分块插值**：图像分 NxM 中心对称 block，每个 block 的矫正函数由四顶点坐标双线性插值得到。
4. **评测**：客观（均匀光源 A/C/D65）+ 主观（单色物体：天空/地板/墙面/白纸）。

## 示例或代码

```text
暗角校正公式：
  PCOR(x,y) = P_IN(x,y) × F(x,y)
  P_IN：每个输入像素值
  F(x,y)：矫正函数，依赖每帧像素坐标

分块双线性插值：
  输入图像分 NxM 个 block（可不等大小，须中心对称）
  每个 block 矫正函数由 block 四顶点坐标双线性插值得到
```

## 常见误区

- **"暗角只是亮度问题"**：还分 Color shading（RGB 平面不重合，中心/四周颜色不一致）。
- **"暗角是 sensor 问题"**：主要源于镜头光学（通光量/折射率/CRA），sensor 微透镜 CRA 不匹配是协同因素。
- **"暗角不影响算法"**：亮度不均会影响后续算法准确性（AWB/CCM），需在校正前消除。
- **"矫正函数是固定的"**：每帧像素坐标相关的矫正函数，分块插值逼近真实 shading。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| vignetting-definition | wikipedia-vignetting-v2 | 暗角 = 边缘相对中心亮度/饱和度降低 |

## 待验证项

无。

## 关联知识

- [[black-level-correction]] —— 与 LSC 同属 raw 域前端。
- [[basic-of-color]] —— Color shading 与色彩均匀性相关。
- [[image-quality-assessment]] —— 均匀性（shading/暗角）是成像评测维度。

## 详细章节

### 镜头暗角概念

由于镜头光学系统原因，使得获得的图像中间比较亮，边缘比较暗，这个现象就是光学系统中的渐晕。由于渐晕现象带来的图像亮度不均会影响后续算法处理的准确性，需要先经过镜头暗角校正功能来消除渐晕给图像带来的影响。

Lens shading 一般被称之为暗角或镜头阴影或者镜头暗影，是指图像中心区域和图像四角区域的亮度或者色彩不一致的现象。

- **Luma shading（亮度均匀性）**：就是所谓的 vignetting，镜头的通光量从中心到边角减小，造成 sensor 的亮度响应从中心到边角的变小。图像看起来是中心亮、四周逐渐变暗。
- **Color shading（色彩均匀性）**：就是 RGB plane 没有重合，图像看起来就是中间颜色和四周颜色不一致。

### 产生原因

#### Luma shading

- lens 机械结构：lens 的工艺误差、导致光线在 lens 内的传播受到影响
- lens 光学特性：lens 中间区域的穿透能力大于边缘区域

#### color shading

- Lens 折射率：Lens 对不同光线的折射程度不一样
- CRA 不匹配：SENSOR 感光区域上面微透镜的 CRA 和 Lens 的 CRA 不匹配导致

### 镜头暗角校正原理

基本思想：
$$
PCOR(x,y)= P_{IN}(x,y)*F(x,y)
$$

- P_IN(x,y)：每一个输入的像素值
- F(x,y)：矫正函数，矫正的因素依赖于框架中每帧像素的坐标值

### 方法

#### 双线性插值

- **拆分 block**：将输入图像分为 NxM 个 block；每个 block 大小可以不一样，但要满足中心对称。
- **双线性插值**：每个 block 的矫正函数都是由 block 四个顶点坐标双线性插值得到。

### 镜头暗角的评测方法

- **客观评测**：主要对一些均匀光源，如 A 光、C 光、D65 等。
- **主观评测**：主要对一些色彩单一的物体拍摄，如天空、地板、墙面、白纸、天花板等。

## 参考

- Vignetting（渐晕/暗角）：https://en.wikipedia.org/wiki/Vignetting
- Lens Shading Correction：https://www.opticsforhire.com/blog/lens-shading
