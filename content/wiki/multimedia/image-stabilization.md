---
aliases: []
confidentiality: public
domain: multimedia
evidence:
- claim: 图像防抖是一组在曝光期间减少相机或其他成像设备运动导致模糊的技术。
  claim_id: image-stabilization-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-1d64ca8df123
    exact: Image stabilization (IS) is a family of techniques that reduce blurring associated with the motion of a camera or other imaging device during exposure.
  targets:
  - evidence_id: evidence-1d64ca8df123
    source_id: wikipedia-image-stabilization-v2
id: image-stabilization
kind: reference
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- wikipedia-image-stabilization-v2
- working-multimedia-image-stabilization
status: published
tags:
- needs-fact-check
- web-source-added
- working-migration
title: 图像防抖
updated_at: '2026-09-05'
---
# 图像防抖

## 来源与迁移记录

### 迁移与校验记录

- 原始位置：`content/working/c-intermediate/multimedia/image-stabilization.md`
- 原文快照：`working-multimedia-image-stabilization`（personal-note；用于保留作者原始整理，不等同于外部权威来源）
- 外部链接：2 条；链接仅作为待补来源线索，尚未自动认定为事实依据。
- 当前状态：`draft`；事实正确性、来源逐条对应和必要的权威来源补齐待人工审查。

### 来源补充
- 来源隔离：当前绑定中的 `web-multimedia-image-stabilization` 经正文检查确认是错误页/残留文本，已移除当前引用；Source 文件和历史审计记录保留。

- 已联网读取：`https://en.wikipedia.org/wiki/Image_stabilization`；来源正文已保存为不可变 Source 快照。

## 详细章节

### 图像防抖

#### 需求

* 三脚支架
* 单脚支架
* 外置器械
* 无需器械

目标：更智能、更便携、更低成本的专业防抖效果



#### 抖动导致的问题

* 模糊
* 倾斜
* 摇摆
* 头尾分离
* 眩晕感
* 果冻效应
* 运动模糊
* 视频抖动



#### 图像防抖分类

* 光学防抖（OIS）
    * 镜头移动
    * sensor移动
    * 两者一起移动
* 电子防抖（EIS）
* 视频后处理过滤器
* 外置的防抖支架
* 防抖CCD



##### 光学防抖技术

人眼防抖机制

* 内耳前庭：检测
* 大脑：处理
* 眼球转动或摇头：抵抗



外置稳像设备

* 陀螺仪：检测
* 支架物理移动：抵抗
* 优点：可调幅度大、无需相机支持
* 缺点：使用不方便



单反相机的光学防抖技术

* sensor防抖
    * 依靠传感器位移来进行防抖补偿
* 镜头防抖
    * 依靠凹片镜移动来实现光路折射的转变
    * 优势：“所见即所得”



手机的光学防抖技术

* OIS陀螺仪
* OIS控制器
* OIS马达
    * X轴
    * Y轴
* 霍尔传感器
    * X轴
    * Y轴



常见陀螺仪种类

* 机械陀螺仪
* 激光陀螺仪
* MEMS陀螺仪



##### 电子防抖技术

###### 果冻效应消除原理

果冻效应原理

卷帘快门和全局快门对比



###### 运动模糊消除原理

运动模糊的实质：由点扩散函数所导致的图像衰退



###### 盲目解卷积法

存在的问题

* PSF函数存在不可预知性
* 忽视了噪声
* 计算时间长



###### 多帧短曝光法



###### 视频抖动消除原理

常见的视频帧匹配法

* 灰度投影法
* 块匹配法
* 位平面匹配法
* 特征点匹配法
* 光流法
* SIFT匹配法



影响因素

* 缺乏特征 (Lack of Feature, LOF)
* 重复模式 (Repeated Pattern, RP)
* 低信噪比 (Low SNR)
* 存在运动物体（Moving Objects）
* 透视角造成同一物体远近运动量不同
* 光照突然变化
* 运动模糊(Motion Blur)
* 大面积阴影

#### 参考
- OIS/EIS 防抖技术综述：https://en.wikipedia.org/wiki/Image_stabilization
- 果冻效应与卷帘快门：https://en.wikipedia.org/wiki/Rolling_shutter
