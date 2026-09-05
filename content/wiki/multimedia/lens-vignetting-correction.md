---
aliases: []
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
kind: reference
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- wikipedia-vignetting-v2
- working-multimedia-lens-vignetting-correction
status: published
tags:
- needs-fact-check
- web-source-added
- working-migration
title: 镜头暗角校正
updated_at: '2026-09-05'
---
# 镜头暗角校正

## 来源与迁移记录

### 迁移与校验记录

- 原始位置：`content/working/c-intermediate/multimedia/lens-vignetting-correction.md`
- 原文快照：`working-multimedia-lens-vignetting-correction`（personal-note；用于保留作者原始整理，不等同于外部权威来源）
- 外部链接：2 条；链接仅作为待补来源线索，尚未自动认定为事实依据。
- 当前状态：`draft`；事实正确性、来源逐条对应和必要的权威来源补齐待人工审查。

### 来源补充
- 来源隔离：当前绑定中的 `web-multimedia-lens-vignetting-correction` 经正文检查确认是错误页/残留文本，已移除当前引用；Source 文件和历史审计记录保留。

- 已联网读取：`https://en.wikipedia.org/wiki/Vignetting`；来源正文已保存为不可变 Source 快照。

## 详细章节

### 镜头暗角校正

#### 镜头暗角概念

由于镜头光学系统原因，使得获得的图像中间比较亮，边缘比较暗，这个现象就是光学系统中的渐晕。由于渐晕现象带来的图像亮度不均会影响后续算法处理的准确性，需要先经过镜头暗角校正功能来消除渐晕给图像带来的影响。



Lens shading一般被称之为暗角或镜头阴影或者镜头暗影，是指图像中心区域和图像四角区域的亮度或者色彩不一致的现象。

* Luma shading（亮度均匀性）就是所谓的vignetting，镜头的通光量从中心到边角减小，造成sensor的亮度响应从中心到边角的变小。图像看起来是，中心亮，四周逐渐变暗。
* Color shading（色彩均匀性）就是RGB plane没有重合，图像看起来就是中间颜色和四周颜色不一致。



#### 产生原因

##### Luma shading

* lens机械结构：lens的工艺误差、导致光线在lens内的传播受到影响
* lens光学特性：lens中间区域的穿透能力大于边缘区域



##### color shading

* Lens折射率：Lens对不同光线的折射程度不一样
* CRA不匹配：SENSOR感光区域上面微透镜的CRA和Lens的CRA不匹配导致




#### 镜头暗角校正原理

基本思想
$$
PCOR(x,y)= P_{IN}(x,y)*F(x,y)
$$

* PIN(x,y)：每一个输入的像素值

* F(x,y)：矫正函数，矫正的因素依赖于框架中每帧像素的坐标值



#### 方法

##### 双线性插值

* 拆分block
    * 将输入图像分为NxM个block
    * 每个block大小可以不一样，但是要满足中心对称的
* 双线性插值
    * 每个block的矫正函数都是由block，四个顶点坐标双线性差值得来




#### 镜头暗角的评测方法

* 客观评测
  * 主要是对一些均匀光源，如A光、C光、D65等
* 主观评测
  * 主要是对一些色彩单一的物体拍摄，如天空、地板、墙面、白纸、天花板等

#### 参考
- Vignetting（渐晕/暗角）：https://en.wikipedia.org/wiki/Vignetting
- Lens Shading Correction：https://www.opticsforhire.com/blog/lens-shading
