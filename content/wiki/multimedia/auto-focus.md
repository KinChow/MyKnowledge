---
aliases:
- 自动对焦
- AF
- Auto Focus
confidentiality: public
domain: multimedia
evidence:
- claim: 自动对焦光学系统使用传感器、控制系统和马达，对自动或手动选择的点或区域进行对焦；方法分为主动式、被动式或混合式。
  claim_id: auto-focus-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-440f3d165e06
    exact: An autofocus (AF) optical system uses a sensor, a control system and a motor to focus on an automatically or manually selected point or area. Autofocus methods are distinguished as active, passive or hybrid types.
  targets:
  - evidence_id: evidence-440f3d165e06
    source_id: wikipedia-autofocus-v2
id: auto-focus
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- wikipedia-autofocus-v2
- working-multimedia-auto-focus
status: published
tags:
- camera
- isp
- autofocus
- 3a
- multimedia
title: 自动对焦（AF）
updated_at: '2026-09-04'
---

# 自动对焦（AF）

## 一句话结论

自动对焦（Auto Focus，AF）是相机/ISP 使被摄主体清晰成像（合焦）的机制：由传感器、控制系统和马达组成的光学系统，自动判断被摄主体、测量其与感光元件的距离，再驱动马达把镜头对焦装置推到相应位置。按测距方式分为**主动式**（激光/TOF）与**被动式**（相位对焦 PDAF、反差对焦 CDAF）；反差对焦是普及率最高的低成本方案，相位对焦对焦快但需专用 sensor。

## 核心概念

- **合焦**：拍摄时被摄物体清晰成像的状态；失焦即图像模糊。
- **主动式对焦**：发射探测波（激光/红外）测距，如激光对焦（LDAF）、TOF 对焦；低反差/弱光/细线条/运动物体场景占优。
- **被动式对焦**：不主动发射，分析成像，如相位对焦（PDAF）、反差对焦（CDAF）；省电、小型化、逆光占优。
- **反差对焦（CDAF）**：通过移动镜头比较图像反差（对比度），迭代收敛到反差最大处；成本低但耗时。
- **相位对焦（PDAF）**：用 sensor 上的成对相位检测像素计算相位差，一次驱动马达到合焦位；快但需专用 PDAF sensor。

## 工作机制

自动对焦是一个"检测 → 计算 → 驱动"闭环：

1. **检测主体**：自动判断拍摄主体（或用户触控选择的区域）。
2. **测量距离**：主动式发射探测波测距；被动式通过分析成像（反差/相位差）估计离焦量与方向。
3. **驱动合焦**：马达将镜头对焦装置推到相应距离刻度，实现合焦。

- **CDAF 过程**：反复迭代求反差最大——未合焦（虚焦）→ 移动镜头画面渐清晰（反差上升）→ 反差最高（合焦）→ 继续移动反差下降（错过）→ 回退到反差最高处。
- **PDAF 过程**：计算相位差 → 查表得马达理想位置 → 一次驱动到位，耗时更少。

## 示例或代码

对焦方式对比：

```text
主动式：激光对焦、TOF 对焦
  优势：低反差、弱光线、细线条、运动物体
  劣势：被摄体吸收光波、光波被玻璃反射等场景失效

被动式：相位对焦（PDAF）、反差对焦（CDAF）
  优势：无发射系统、耗能少、小型化、逆光场景
  劣势：细线条、弱光、偏光物体、运动物体

相位式：计算一次即可合焦
反差式：需计算多次（迭代收敛）
```

## 常见误区

- **"反差对焦最先进"**：CDAF 普及率最高、成本最低，但对焦耗时，纯色/低反差场景易失焦。
- **"相位对焦不用专用 sensor"**：PDAF 需要带金属遮罩的专用 PDAF sensor（像素上做相位检测），暗环境效果差。
- **"主动对焦总更好"**：激光/TOF 对距离有限制，远距离主体效果差；且对能吸收光波/玻璃反射场景失效。
- **"对焦快慢只看算法"**：反差对焦性能还受感光器采样帧率与镜头步进马达的协调影响。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| auto-focus-definition | wikipedia-autofocus-v2 | AF 光学系统 = 传感器+控制系统+马达，主动/被动/混合 |

## 待验证项

无。

## 关联知识

- [[overview-of-3a]] —— 自动对焦（AF）是相机 3A（AE/AF/AWB）之一，与自动曝光、自动白平衡联动。
- [[android-camera-architecture]] —— AF 是 Camera HAL3 流水线中 3A 控制的一部分。

## 详细章节

### 简介

摄影中常遇图像模糊，一般是对焦异常（"失焦"）导致；自动对焦使拍出的样张更清晰。自动对焦是复杂的光电一体化过程：自动判断拍摄主体 → 测量被摄主体与相机感光元器件之间的距离 → 驱动马达将镜头的对焦装置推到相应距离刻度。拍摄照片时，被摄物体清晰成像，叫做合焦。

### 分类

- **主动式**：激光对焦、TOF 对焦等。优势：低反差、弱光线、细线条、运动物体；劣势：被摄体能吸收光波、光波被玻璃反射等场景。
- **被动式**：相位对焦、反差对焦等。优势：无发射系统、耗能少、小型化、逆光场景；劣势：细线条、弱光、偏光物体、运动物体。

#### 反差对焦（CDAF）

反差对焦（Contrast Detection Auto Focus），又称对比度对焦，普及率最高、最广泛、成本相对较低。它是一个反复迭代逐渐收敛的过程：计算反差度 → 移动镜头比较反差度 → 直到反差度最大。实质是求最大值的过程，类似手动对焦（模糊-清晰-模糊，回到清晰焦距）：

1. 未合焦状态图像虚焦
2. 镜头移动，画面渐清晰，对比度上升
3. 合焦状态对比度最高、画面最清晰，继续移动
4. 继续移动发现对比度下降，错过焦点
5. 镜头回退至对比度最高处，完成对焦

优缺点：物理成本低、无单独子系统、不占独立空间、对焦精度高；但对焦耗时，纯色或低反差场景对焦时间过长或精度低。难点：降低序列图像规模减少对比次数；更快更密集的数据源；感光器采样帧率（实时刷新率）与镜头采样帧率（FPS，步进马达与镜头协调）是关键。

#### 相位对焦（PDAF）

相位对焦（Phase Detection Auto Focus）全称"相位检测自动对焦"：计算相位差 → 查表计算马达理想位置 → 驱动马达快速对焦。PDAF sensor 在 CMOS 一半位置加金属遮盖，从像素传感器中找出成对像素点，通过相位差检测找出准确对焦点，马达一次将镜片推到相应位置。优点：一般计算一次即可合焦、马达移动距离更短；缺点：专用 PDAF sensor、暗环境效果差。对比：相位式一次合焦、反差式需多次。

#### 激光对焦（LDAF）

激光对焦（Laser Detection Auto Focus）也称测距式对焦：通过独立红外激光传感器向被摄物体发射低功率红外激光，反射后被接收，计算出距离后驱动镜片到相应位置。优点：暗环境、纹理不明显的纯色区域；缺点：对焦距离有限制，远距离主体效果差。

#### TOF 对焦

TOF（Time of Flight，飞行时间）：传感器发射红外光，经被摄物体反射，通过计算发射反射时间差或相位差得到距离。优点：一次合焦、降低处理器计算负担、降低背景光干扰；缺点：物理器件性能要求高、时间测量精度要求高。

## 参考

- 反差对焦（CDAF）与相位对焦（PDAF）原理：https://en.wikipedia.org/wiki/Autofocus
- 相机自动对焦技术综述：https://www.cambridgeincolour.com/tutorials/camera-autofocus.htm
- 激光对焦 / TOF 对焦（主动对焦）：https://www.dpreview.com/articles/0465668628/how-autofocus-systems-work
