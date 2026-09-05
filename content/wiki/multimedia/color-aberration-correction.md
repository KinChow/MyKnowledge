---
aliases: []
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
kind: reference
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- wikipedia-chromatic-aberration-v2
- working-multimedia-color-aberration-correction
status: published
tags:
- needs-fact-check
- web-source-added
- working-migration
title: 色差校正
updated_at: '2026-09-05'
---
# 色差校正

## 来源与迁移记录

### 迁移与校验记录

- 原始位置：`content/working/c-intermediate/multimedia/color-aberration-correction.md`
- 原文快照：`working-multimedia-color-aberration-correction`（personal-note；用于保留作者原始整理，不等同于外部权威来源）
- 外部链接：2 条；链接仅作为待补来源线索，尚未自动认定为事实依据。
- 当前状态：`draft`；事实正确性、来源逐条对应和必要的权威来源补齐待人工审查。

### 来源补充
- 来源隔离：当前绑定中的 `web-multimedia-color-aberration-correction` 经正文检查确认是错误页/残留文本，已移除当前引用；Source 文件和历史审计记录保留。

- 已联网读取：`https://en.wikipedia.org/wiki/Chromatic_aberration`；来源正文已保存为不可变 Source 快照。

## 详细章节

### 色差校正

#### 色差背景和产生原因

因为透镜对不同波长的色光有不同的折射率，所以光学上透镜无法将各种波长的色光都聚焦在同一点上。一般在高亮度或高对比度区域的边缘上明显的杂色，我们把它叫做色差 （chromatic aberration）。



##### 分类

###### 纵向色差（轴向色差）

当颜色随着焦点的移动而变化的时候，我们认为出现了纵向色差；

同时选择小光圈也会抑制纵向色差；因小光圈的镜片直径越小，景深更大，这使得红色和蓝色相对于绿色的弥散程度更轻，表现在图片上就是纵向色差被抑制了；



###### 横向色差（侧向色差）---最主要的色差问题



##### 纵向色差与横向色差的异同

*  相同点：
    *  两者都是因为不同波长的可见光在通过透镜时的折射率不同所导致的；
    *  两者在图像上都表现为突兀的颜色边缘，一般以紫边为主，蓝边、绿边、青边、红边、黄边也很常见；
    *  两者常见于图像中的高对比度区域；
*   不同点：
    *   纵向色差
        * 纵向色差均匀分布于整张图像之内；
        *  通过调节镜头光圈大小等参数，我们可以削弱纵向色差；
    *   横向色差
        *  从图像中心到图像边缘，横向色差会变得越来越严重
        * 无法通过调节镜头参数米削弱横向色差

对于消色镜头，红色分量和蓝色分量会呈现一致的变化规律；

而对于正常的镜头，红色分量和蓝色分量的变化规律并不一致，而是与他们的波长正相关；



#### 色差校正的方法

##### 全局校正

横向色差实际上是一种径向上的变形，距离图像中心越远，变形程度越大，通常我们需要将蓝色通道向外扩展，将红色通道向内收缩。



##### 局部校正

* 色差在图像上最直观的表现就是高亮度高对比度区域的彩色边缘；
*  我们可以通过像素点的梯度信息和色差（color difference）信息，来判断其是否属于边缘区域，然后根据其是否是“不正常”的颜色（以紫色为主），来判断是否要对他进行颜色上的修正；



#### 色差校正的难点

* 普适性与局部性
*  场景难以检测，校正尺度难以把握
#### 参考
- 色差（Chromatic Aberration）基础：https://en.wikipedia.org/wiki/Chromatic_aberration
- Cambridge in Colour - Understanding Chromatic Aberration：https://www.cambridgeincolour.com/tutorials/ chromatic-aberration.htm
