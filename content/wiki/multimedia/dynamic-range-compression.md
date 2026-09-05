---
aliases: []
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
kind: reference
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- wiki-hdri
- working-multimedia-dynamic-range-compression
status: published
tags:
- needs-fact-check
- web-source-added
- working-migration
title: 动态范围压缩
updated_at: '2026-09-05'
---
# 动态范围压缩

## 来源与迁移记录

### 迁移与校验记录

- 原始位置：`content/working/c-intermediate/multimedia/dynamic-range-compression.md`
- 原文快照：`working-multimedia-dynamic-range-compression`（personal-note；用于保留作者原始整理，不等同于外部权威来源）
- 外部链接：1 条；链接仅作为待补来源线索，尚未自动认定为事实依据。
- 当前状态：`draft`；事实正确性、来源逐条对应和必要的权威来源补齐待人工审查。

### 来源补充
- 来源隔离：当前绑定中的 `web-multimedia-dynamic-range-compression` 经正文检查确认是错误页/残留文本，已移除当前引用；Source 文件和历史审计记录保留。

- 已联网读取：`https://en.wikipedia.org/wiki/Adaptive_histogram_equalization`；来源正文已保存为不可变 Source 快照。

## 详细章节

### 动态范围压缩

#### 动态范围压缩的定义

##### 对比度定义

动态范围也称作对比度，是衡量成像质量的重要参数



细节丰富
对比度高、画面通透、亮暗分明、层次丰富、质感突出……



##### 对比度压缩

|          | 对比度范围 |
| -------- | ---------- |
| 真实世界 | 10^9 cd/m2 |
| 人眼范围 | 10^4 cd/m2 |
| Rec 709  | 2^8 cd/m2  |



黑白照片添加彩色网格后，会变成“彩色照片”，说明人眼有一定分辨率，因此过小的亮度差异不容易被人眼识别



##### 动态范围

动态范围压缩时采用等比压缩，会缩小亮度等级之间的差异，造成细节丢失。

动态范围是指Sensor支持的最大输出信号和最小输出信号的比值，或者说图像最亮部分与最暗部分的灰度比值，也就是常说的对比度。动态范围压缩的核心功能，就是让高Bit图在低Bit显示器上显示时，保留多图像细节。



##### 直方图

灰度直方图：横坐标亮度等级，纵坐标为该亮度等级pix数量在全部pix中的比例

直方图可以清晰的反应图像中所有pix的分布情况，因此可以作为量化评测对比度的客观工具



通过特殊的映射关系，将相同亮度值的pix，映射为其他亮度值，就能改变直方图分布情況，进而改变对比度高低。

合理的灰度映射，可以使直方图覆盖范围更广，提高图像对比度，这种映射称为直方图均衡。

因此配置合理的灰度映射曲线就是DRC核心算法。



##### value stretch

由于照明不足，成像传感器动态范围太小等原因，会造成图像对比度过小。
对比拉伸的思想是提高图像处理时灰度级的动态围。



##### 映射曲线



#### 动态范围压缩的原理

##### 全局

###### 直方图均衡（HE）

直方图均衡化过程中，有两个条件必须保证：
*    像素亮度映射后，一定要保证原来的大小关系不变，即暗点处理完之后依旧是暗点，亮点处理完之后依旧是亮点
*    像素亮度映射后，数值不能能越界，比如8bit系统中，亮度无论按照什么公式进行映射，映射后都不能超过0-255的范围



###### 累积分布函数（CDF）

核心：用某等级亮度下pix数量占比，映射出新亮度值



###### CLAHE (Contrast Limited Adaptive histogram equalization)

图像中的大片平坦区域，会造成该区域的CDF曲线斜率过大。

采用设定固定阈值，均分直方图中超过阈值部分的手段，可以明显平缓最终的CDF曲线，可以抑制过度增强噪声。



##### 局部

###### 双边滤波

通过双边滤波，将图像分为高频和低频两张图，其中高频图就是图像中local区域的细节。在对低频图做正常的均衡处理后，叠加上经过一定增益的高频图，就实现了在进行全局对比度增强时，保留或增强局部细节。



###### local gamma

除了双边滤波外，另外常见的增强局部对比度的方式就是使用局部gamma曲线。

核心原理是将原图分为不同patch，每个patch根据自身直方图分布情况单独做均衡， 然后在各patch之间边界做好平滑。
这样的好处是可以尽可能多的保留或增加局部细节
#### 参考
- 直方图均衡（HE/CLAHE）：https://en.wikipedia.org/wiki/Adaptive_histogram_equalization
- 双边滤波分离高低频做局部增强：Tomasi C, Manduchi R. Bilateral Filtering for Gray and Color Images[C]. ICCV, 1998
