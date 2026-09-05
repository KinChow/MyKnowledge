---
aliases: []
confidentiality: public
domain: multimedia
evidence:
- claim: |-
    The HAL sits between the camera driver and the higher-level Android framework and defines an interface that you must implement so apps can correctly operate the camera hardware.
  claim_id: isp-system-audit-1
  support: direct
  supporting_quotes:
  - evidence_id: evidence-d937f440c251
    exact: |-
      The HAL sits between the camera driver and the higher-level Android framework and defines an interface that you must implement so apps can correctly operate the camera hardware.
  targets:
  - evidence_id: evidence-d937f440c251
    source_id: aosp-camera-architecture
id: isp-system
kind: reference
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- aosp-camera-architecture
- working-multimedia-isp-system
status: published
tags:
- needs-fact-check
- web-source-added
- working-migration
title: ISP系统
updated_at: '2026-09-05'
---
# ISP系统

## 来源与迁移记录

### 迁移与校验记录

- 原始位置：`content/working/c-intermediate/multimedia/isp-system.md`
- 原文快照：`working-multimedia-isp-system`（personal-note；用于保留作者原始整理，不等同于外部权威来源）
- 外部链接：0 条；链接仅作为待补来源线索，尚未自动认定为事实依据。
- 当前状态：`draft`；事实正确性、来源逐条对应和必要的权威来源补齐待人工审查。

### 来源补充
- 来源隔离：当前绑定中的 `web-multimedia-isp-system` 经正文检查确认是错误页/残留文本，已移除当前引用；Source 文件和历史审计记录保留。

- 已联网读取：`https://en.wikipedia.org/wiki/Image_signal_processor`；来源正文已保存为不可变 Source 快照。

## 详细章节

### ISP系统

#### 数字成像系统

数字成像系统是为了模仿人的视觉系统，尽可能地把现实场景恢复得与人眼接近。

将自然界中光信号转化为电信号，然后将模拟电信号转化为数字信号的过程，将数字信号进行处理，最终到显示设备送显或者文件格式存储。



#### 目的

图像是人类视觉的基础，是自然景物的客观反映，是人类认识世界和人类本身的重要来源。

”图“是物体反射或透射光的分布，”像“是人类视觉系统所接受的图在人脑中形成的印象或认识。

数字成像系统是为了模仿人的视觉系统，尽可能地把现实场景恢复得与人眼接近。整个ISP pipeline都是围绕对真实世界的还原而设计的。



#### 组成

* 镜头（Lens）
  * 镜头由透镜组成，景物的光线通过透镜在sensor平面形成清晰的像。透镜越多，成像效果越出色，但是成本也越高。
* 红外滤光片（可选）
  * 人眼无法观察红外光线，但是sensor可以，所以需要滤除红外光，让图像更接近人类观察的效果。
* 图像传感器（Sensor）
  * 将镜头的光信号转化为电信号，再经过内部AD将模拟电信号转化为数字信号。
  * sensor中每个像素点只能感光R、G、B中的一种，这些最原始的感光数据称为RAW数据。
  * 类型
    * CCD
    * CMOS
* ISP
  * 将RAW数据处理成三通道的彩色图像。
* 显示



#### 应用

* 手机相机
* 数码相机
* 行车记录仪
* 安防系统
* 无人机
* 汽车ADAS系统



#### ISP处理流程

##### pipeline

经过ISP的处理后，图像信号反映更加真实的现实场景。

ISP pipeline有多种，以下是其中一种。

```mermaid
flowchart TD
	subgraph raw[RAW域处理流程]
		direction LR
		黑电平与线性化-->坏点矫正
		坏点矫正-->RAW域降噪
		RAW域降噪-->镜头暗角矫正
		镜头暗角矫正-->白平衡增益
		白平衡增益-->绿平衡矫正
		绿平衡矫正-->去马赛克
	end
	subgraph rgb[RGB域处理流程]
		direction LR
		色差矫正-->色彩矫正
		色彩矫正-->动态范围压缩
		动态范围压缩-->GAMMA
		GAMMA-->3DLUT
	end
	subgraph yuv[YUV域处理流程]
		direction LR
		色差增强-->细节增强
		细节增强-->锐化
		锐化-->YUV域降噪
		YUV域降噪-->色调映射
	end
	sensor-->raw
	raw-->rgb
	rgb-->yuv
	yuv-->显示
```





##### RAW域处理流程

* 黑电平与线性化
* 坏点矫正
* RAW域降噪
* 镜头暗角矫正
* 白平衡增益
* 绿平衡矫正
* 去马赛克



##### RGB域处理流程

* 色差矫正
* 色彩矫正
* 动态范围压缩
* GAMMA
* 3DLUT



##### YUV域处理流程

* 色彩增强
* 细节增强
* 锐化
* YUV域降噪
* 色调映射



##### 主pipeline以外处理

* 自动曝光
* 自动对焦
* 自动白平衡
* 闪光灯
* 图像缩放
* 图像压缩
* 畸变矫正
* 图像防抖
* 深度图
* JPEG
