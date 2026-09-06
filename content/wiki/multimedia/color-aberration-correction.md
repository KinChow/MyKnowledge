---
aliases:
- 色差校正
- Chromatic Aberration
- 色差
confidentiality: public
domain: multimedia
evidence:
- claim: 色差是镜头无法将所有颜色聚焦到同一点的现象。
  claim_id: chromatic-aberration-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-c78a7d62f3fe
    exact: In optics, chromatic aberration (CA), also called chromatic distortion, color aberration, color fringing, or purple fringing, is a failure of a lens to focus all colors to the same point.
  targets:
  - evidence_id: evidence-c78a7d62f3fe
    source_id: wikipedia-chromatic-aberration-v2
id: color-aberration-correction
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- wikipedia-chromatic-aberration-v2
- working-multimedia-color-aberration-correction
status: published
tags:
- camera
- lens
- isp
- chromatic-aberration
- multimedia
title: 色差校正
updated_at: '2026-09-04'
---

# 色差校正

## 一句话结论

色差（Chromatic Aberration，CA）是镜头无法将所有颜色聚焦到同一点的现象：透镜对不同波长色光折射率不同，导致高亮度/高对比度区域边缘出现杂色（通常为紫边）。色差分**纵向（轴向）**与**横向（侧向）**两类：纵向均匀分布、可用小光圈抑制；横向从中心到边缘渐重、无法用镜头参数消除，是最主要的色差问题。校正上，横向色差是径向变形（蓝通道外扩、红通道内缩），用全局/局部校正消除边缘彩色伪影。

## 核心概念

- **色差（CA）**：透镜无法将所有颜色聚焦到同一点；高对比度边缘的杂色（紫边为主）。
- **纵向（轴向）色差**：颜色随焦点移动变化；均匀分布于整图；小光圈可抑制。
- **横向（侧向）色差**：最主要的色差；从中心到边缘渐重；无法用镜头参数削弱。
- **消色镜头**：红蓝分量变化规律一致；正常镜头红蓝分量与波长正相关。
- **校正**：全局（蓝通道外扩、红通道内缩）+ 局部（梯度+色差信息判定边缘伪彩）。

## 工作机制

1. **成因**：透镜对不同波长色光折射率不同，色光无法聚焦在同一点。
2. **分类判定**：颜色随焦点变化 → 纵向；中心到边缘渐重 → 横向。
3. **全局校正**：横向色差是径向变形，距中心越远变形越大；将蓝色通道向外扩展、红色通道向内收缩。
4. **局部校正**：用像素梯度 + 色差（color difference）信息判断是否边缘区域、是否"不正常"颜色（紫为主），对其做颜色修正。

## 示例或代码

```text
色差分类判定：
  纵向（轴向）：颜色随焦点移动变化；整图均匀分布；小光圈可抑制
  横向（侧向）：中心→边缘渐重；无法用镜头参数消除（主要问题）

全局校正：
  横向色差 = 径向变形 → 蓝色通道向外扩展、红色通道向内收缩

局部校正：
  梯度 + 色差信息 → 判定高对比度彩色边缘（紫边）→ 修正
```

## 常见误区

- **"色差只有紫边"**：蓝边、绿边、青边、红边、黄边也很常见，紫边最常见。
- **"缩小光圈能解决色差"**：只能抑制纵向色差；横向色差无法用镜头参数削弱。
- **"色差是传感器问题"**：色差是镜头光学问题（折射率差异），传感器只是呈现它。
- **"全局校正够用"**：局部校正对高对比度边缘的伪彩更有效，全局校正主要处理径向变形。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| chromatic-aberration-definition | wikipedia-chromatic-aberration-v2 | 色差是镜头无法聚焦所有颜色到同一点 |

## 待验证项

无。

## 关联知识

- [[basic-of-color]] —— 色差影响色彩还原，是色彩链的镜头端误差源。
- [[lens-vignetting-correction]] —— 镜头另一类光学误差（暗角）。
- [[android-camera-architecture]] —— ISP 对镜头光学误差的校正模块。

## 详细章节

### 色差背景和产生原因

因为透镜对不同波长的色光有不同的折射率，所以光学上透镜无法将各种波长的色光都聚焦在同一点上。一般在高亮度或高对比度区域的边缘上明显的杂色，我们把它叫做色差（chromatic aberration）。

#### 分类

**纵向色差（轴向色差）**：当颜色随着焦点的移动而变化的时候，我们认为出现了纵向色差。同时选择小光圈也会抑制纵向色差；因小光圈的镜片直径越小、景深更大，这使得红色和蓝色相对于绿色的弥散程度更轻，表现在图片上就是纵向色差被抑制了。

**横向色差（侧向色差）**：最主要的色差问题。

#### 纵向色差与横向色差的异同

- **相同点**：两者都是因为不同波长的可见光在通过透镜时的折射率不同所导致的；两者在图像上都表现为突兀的颜色边缘（以紫边为主，蓝边、绿边、青边、红边、黄边也很常见）；两者常见于图像中的高对比度区域。
- **不同点**：
  - 纵向色差：均匀分布于整张图像之内；通过调节镜头光圈大小等参数可以削弱。
  - 横向色差：从图像中心到图像边缘越来越严重；无法通过调节镜头参数削弱。

对于消色镜头，红色分量和蓝色分量会呈现一致的变化规律；而对于正常的镜头，红色分量和蓝色分量的变化规律并不一致，而是与它们的波长正相关。

### 色差校正的方法

#### 全局校正

横向色差实际上是一种径向上的变形，距离图像中心越远，变形程度越大，通常我们需要将蓝色通道向外扩展，将红色通道向内收缩。

#### 局部校正

- 色差在图像上最直观的表现就是高亮度高对比度区域的彩色边缘；
- 我们可以通过像素点的梯度信息和色差（color difference）信息，来判断其是否属于边缘区域，然后根据其是否是"不正常"的颜色（以紫色为主），来判断是否要对他进行颜色上的修正。

### 色差校正的难点

- 普适性与局部性
- 场景难以检测，校正尺度难以把握

## 参考

- 色差（Chromatic Aberration）基础：https://en.wikipedia.org/wiki/Chromatic_aberration
- Cambridge in Colour - Understanding Chromatic Aberration：https://www.cambridgeincolour.com/tutorials/chromatic-aberration.htm
