---
aliases:
- 3A
- 3A统计
- AE
- AF
- AWB
- 自动曝光自动对焦自动白平衡
confidentiality: public
domain: multimedia
evidence:
- claim: 白平衡是对图像颜色强度进行全局调整、使白色或灰色等中性色正确呈现的过程。
  claim_id: three-a-white-balance
  support: direct
  supporting_quotes:
  - evidence_id: evidence-33a2fc20ca9d
    exact: |-
      In photography and image processing, color balance is the global adjustment of the intensities of the colors (typically red, green, and blue primary colors). An important goal of this adjustment is to render specific colors – particularly neutral colors like white or grey – correctly. Hence, the general method is sometimes called gray balance, neutral balance, or white balance. Color balance changes the overall mixture of colors in an image and is used for color correction.
  targets:
  - evidence_id: evidence-33a2fc20ca9d
    source_id: web-multimedia-auto-white-balance
id: overview-of-3a
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-multimedia-auto-white-balance
- working-multimedia-overview-of-3a
status: published
tags:
- camera
- isp
- 3a
- ae
- af
- awb
- multimedia
title: 3A统计概述
updated_at: '2026-09-05'
---

# 3A统计概述

## 一句话结论

3A（AE 自动曝光 / AF 自动对焦 / AWB 自动白平衡）是相机感知现实环境、正确配置 sensor 并为后续图像处理提供参考信息的核心统计环节：AE 输出亮度与运动信息、AF 输出距离/位置/深度信息、AWB 输出光源与肤色信息。一般在黑电平矫正与坏点矫正完成后、于 RAW 域统计区域/ROI 的直方图与均值等统计量（AE：RGB/Y 直方图、测光分区；AF：各块 focus value；AWB：R/G、B/G 均值与白点个数），供各算法决策。

## 核心概念

- **AE（自动曝光）**：通过光圈/快门/ISO 控制曝光量，输出亮度与运动信息。
- **AF（自动对焦）**：调整对焦位置使画面清晰，输出距离/位置/深度/运动/方向信息。
- **AWB（自动白平衡）**：补偿光源色温，还原中性色，输出光源与肤色信息。
- **曝光三角**：光圈（进光量）、快门（曝光时间）、ISO（感光度）三者共同决定曝光。
- **3A 统计信息**：在 RAW 域对统计区域/ROI 提取的直方图、均值、白点个数等，是 3A 算法的输入。
- **白平衡色温**：K 值表示"针对该色温光源做补偿"——K 低补偿偏蓝、K 高补偿偏红/黄。

## 工作机制

1. **触发时机**：一般在黑电平矫正和坏点矫正完成后，获取 3A 统计信息（RAW 域）。
2. **统计提取**：
   - AE：统计区域与 ROI 的 R/G/B、Y 的 256-bin 直方图与 RGB 联合直方图；按测光模式（点/中心/矩阵）给 M×N 分块不同权重。
   - AF：统计区域分为 M×N 块，每块计算 focus value（早期用拉普拉斯等固定高频滤波器，现常用 FIR/IIR 滤波器）。
   - AWB：统计每块 R/G/B 均值与白点个数、R/G 与 B/G 均值。
3. **决策与调节**：AE 调节 sensor（光圈/快门/ISO），AF 移动镜头，AWB 调整增益补偿色温，为后处理提供参考信息。

## 示例或代码

```text
AE 统计：区域/ROI 的 R、G、B、Y 256-bin 直方图 + RGB 联合直方图
        测光模式（点测光/中心测光/矩阵测光）→ M×N 分块不同权重
AF 统计：M×N 块 focus value（拉普拉斯/高频滤波，或 FIR/IIR 滤波器响应）
AWB 统计：M×N 块 R/G、B/G 均值 + 白点个数

白平衡色温补偿：
  画面偏黄（暖色过重）→ 提高 K（增加蓝色补偿）
  画面偏蓝（冷色过重）→ 降低 K（增加红色补偿）
```

## 常见误区

- **"3A 就是三个独立模块"**：三者共用 sensor 与统计硬件，统计信息在 RAW 域统一获取，且相互关联（如 AE 的亮度也影响 AF/AWB 判断）。
- **"白平衡只是调冷暖"**：本质是使中性色（白/灰）正确呈现的全局颜色强度调整，色温补偿只是实现手段。
- **"ISO 越大越好"**：ISO 大感光强但噪点增多；ISO 小画质好但对光感应弱。
- **"AF 统计只有高频滤波一种"**：早期用固定滤波器（如拉普拉斯），对无边缘场景失效；现常用可配置的 FIR/IIR 滤波器。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| three-a-white-balance | web-multimedia-auto-white-balance | 白平衡是使中性色正确呈现的全局颜色强度调整 |

## 待验证项

- AE/AF/AWB 统计信息的具体定义（直方图、focus value、白点统计等）来自内部工作笔记（working-multimedia-overview-of-3a），无公开权威来源，待人工复核。

## 关联知识

- [[auto-focus]] —— AF 算法与对焦原理。
- [[auto-white-balance]] —— AWB 算法与色温估计。
- [[black-level-correction]] —— 3A 统计在黑电平/坏点矫正之后进行。
- [[sensor]] —— 3A 调节的对象（曝光/增益）。
- [[terminology]] —— 3A 相关术语（PDAF、ASD、AFD 等）。

## 详细章节

### 3A基本概念

#### 3A的定义

- 自动曝光（Auto Exposure，AE）
  - 输出亮度、运动信息
- 自动对焦（Auto Focus，AF）
  - 输出距离、位置、深度、运动、方向信息
- 自动白平衡（Auto White Balance，AWB）
  - 输出光源、人脸信息

#### 3A的作用

感知现实环境，正确地配置相机，为其他处理提供参考信息：

- 对 sensor 进行调节
- 为后处理提供信息

#### 什么时候进行3A

一般在黑电平矫正和坏点矫正完成后，获取 3A 统计信息。

#### 相关概念

##### 曝光（Exposure）——亮度

光圈：控制进光量：

- 光圈开大：进光孔径增大，进入相机的光线越多，曝光量越多，画面越亮
- 光圈缩小：进光孔径缩小，进入相机的光线越少，曝光量越少，画面越暗

快门速度：控制曝光时间：

- 快门速度越快，曝光时间越短，适合抓拍或拍摄运动物体
- 快门速度越慢，曝光时间越长，适合记录光点运动轨迹

感光度：感光元件对光线敏感程度：

- ISO 越小，对光线的感应能力越弱，但是画质表现较好
- ISO 越大，对光线的感应能力越强，但是会形成噪点影响画质

##### 对焦（Focus）——清晰度

一张好的照片，清晰是基础。对焦成功与否决定照片的清晰度。

##### 白平衡（White Balance）

白平衡的色温 K 表示"针对该色温光源做补偿"：K 越低补偿越偏蓝（去暖色），K 越高补偿越偏红/黄（去冷色）。因此：

- 还原环境的真实色彩
  - 画面偏黄（暖色过重）就提高色温 K 值（增加蓝色补偿）
  - 画面偏蓝（冷色过重）就降低色温 K 值（增加红色补偿）
- 调整画面冷暖
  - 需要偏黄的暖色调效果时，降低色温 K 值（减少蓝色补偿）
  - 需要偏蓝的冷色调效果时，提高色温 K 值（增加蓝色补偿）

### 3A统计信息

#### AE统计信息

- 统计区域和 ROI 中 R/G/B 的 256-bin 直方图
- 统计区域和 ROI 中 Y 的 256-bin 直方图
- 统计区域和 ROI 中 RGB combine 直方图
- 对于不同测光（点测光、中心测光、矩阵测光），可以把全图分为 M×N 块，按照不同测光，每块权重不一样

#### AF统计信息

- 选取统计区域并分为 M×N 块，统计每块的 Focus value

Focus value 计算方法：

- 早期 ISP 会使用固定的 filter 来提取图像的细节
  - 比如使用拉普拉斯滤波器，提取图像的高频信号。图像使用高频滤波器，图像的细节被提取出来。细节越清晰，focus value 越大
  - 问题：当图像没有那么多边缘，或者图像边缘不锐利时，比如云彩，使用高频滤波器无法提取边缘，导致无法根据该滤波器提取其边缘是否为最锐利
- 现在常用 FIR filter 和 IIR filter
  - FIR 滤波器：根据系统的特点去添加不同的系统 bi，得到想要的频率响应特点（高通、低通、带通）
  - IIR 滤波器：更加灵活配置参数，设置想要的频率响应

#### AWB统计信息

- 选取统计区域并分为 M×N 块，统计每块的 R/G/B 均值与白点个数
- 选取统计区域并分为 M×N 块，统计每块的 R/G 和 B/G 均值

## 参考

- 3A（AE/AF/AWB）概述：https://en.wikipedia.org/wiki/Autofocus / https://en.wikipedia.org/wiki/Color_balance
- 曝光三角（光圈/快门/ISO）：https://en.wikipedia.org/wiki/Exposure_(photography)
