---
aliases:
- 计算摄影
- Computational Photography
- 计算摄影算法展望
- 计算成像
confidentiality: public
domain: multimedia
evidence:
- claim: 计算摄影指用数字计算代替光学过程的数字图像采集与处理技术。
  claim_id: computational-photography-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-625abfc36640
    exact: Computational photography refers to digital image capture and processing
      techniques that use digital computation instead of optical processes
  targets:
  - evidence_id: evidence-625abfc36640
    source_id: web-multimedia-prospects-of-computational-photography
id: prospects-of-computational-photography
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-multimedia-prospects-of-computational-photography
status: published
tags:
- camera
- computational-photography
- hdr
- light-field
- ai
- multimedia
title: 计算摄影算法展望
updated_at: '2026-09-06'
---

# 计算摄影算法展望

## 一句话结论

计算摄影（Computational Photography）指**用数字计算代替光学过程**的数字图像采集与处理技术：能提升相机能力、实现胶片摄影无法实现的功能（如数字全景、HDR、光场相机），或降低相机元件成本与尺寸。光场相机用新颖光学元件采集三维场景信息，实现 3D 图像、增强景深与选择性脱焦（后对焦）。该领域已扩展到计算机图形、计算机视觉与应用光学多个方向（Nayar 分类法）。展望趋势：**多帧堆栈（HDR/夜景/降噪/超分）、AI/深度学习图像处理、RAW 级计算、计算光学（编码孔径/编码曝光）** 将把相机从"记录光线"推向"计算成像"；计算摄影让业余用户能拍出接近专业水平的照片，但（截至 2019 年）仍不能全面超越专业级设备。

## 核心概念

- **计算摄影**：以数字计算替代光学过程的采集与处理技术。
- **传统摄影 vs 计算摄影**：前者靠光学/物理手段记录光，后者靠计算扩展能力。
- **光场相机（Light Field）**：微透镜阵列记录光线方向，支持重对焦（后对焦）、增强景深。
- **HDR / 多帧堆栈**：多曝光/多帧融合扩展动态范围、降噪、超分。
- **计算光学**：编码孔径/编码曝光等，让去模糊/去散焦成为良态问题。
- **计算照明**：结构化照明 + 计算处理实现重打光、材质/几何恢复。
- **AI 图像处理**：深度学习去噪、超分、去马赛克、语义增强。

## 工作机制

1. **多帧堆栈**：连续拍摄多张（不同曝光/不同时间/轻微抖动），对齐后融合——HDR（扩展动态范围）、降噪（信号平均）、超分（亚像素位移重建）。
2. **光场采集**：主镜头 + 微透镜阵列把光线按方向重排，计算重聚焦与合成孔径。
3. **编码曝光/编码孔径**：快门/光圈按编码模式开关，把运动模糊/散焦变成可解卷积的良态问题。
4. **AI 生成**：深度网络学习从退化图/RAW 重建清晰图像（去马赛克、去噪、超分、去模糊）。
5. **全景/合成**：多图配准、接缝融合生成全景；深度引导合成散景。

## 示例或代码

```text
计算摄影技术谱系（Nayar 分类法示意）：
├─ 计算光学（Computational Optics）     : 编码孔径、编码曝光、光场、波前编码
├─ 计算成像（Computational Imaging）    : 计算全息、相位恢复、非传统重建
├─ 计算照明（Computational Illumination）: 结构光重打光、图像增强、去模糊
├─ 计算摄影处理（Computational Processing）: HDR、全景、多帧降噪/超分、去马赛克
└─ 计算传感器（Computational Sensing）   : 片上计算、事件相机（DVS）
```

```python
# 多帧 HDR 简化示意（伪代码）
aligned = [align(f) for f in frames]          # 对齐（特征/光流）
weights = [exposure_weight(f) for f in frames]  # 按曝光给权重
hdr = merge(aligned, weights)                 # 融合扩展动态范围
tone = tonemap(hdr)                           # 色调映射（见 [[tonemapping]]）
```

## 常见误区

- **"计算摄影就是美颜滤镜"**：计算摄影是成像范式的扩展（HDR/光场/多帧/计算光学），滤镜只是很小一部分。
- **"计算摄影只是软件后处理"**：还包括计算光学（编码孔径/光场硬件）、计算照明等硬件与采集侧技术。
- **"计算摄影让光学不重要了"**：光学决定基础成像能力，计算摄影是在光学基础上扩展/弥补。
- **"计算摄影照片全面超过专业设备"**：截至 2019 年可让业余者拍出接近专业的照片，但仍不全面超越专业级设备。
- **"多帧融合没有代价"**：多帧需要时间/内存/功耗，运动场景要防鬼影，低光长曝光有手持限制。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| computational-photography-definition | web-multimedia-prospects-of-computational-photography | 计算摄影 = 以数字计算替代光学过程的采集/处理 |

## 待验证项

- Nayar 分类法的具体分域与代表论文来自公开资料（Wikipedia/学术），待按原文复核。
- 光场相机（微透镜阵列）参数与产品化进展（如 Lytro 已停产）以最新公开资料为准。

## 关联知识

- [[hdr]] / [[tonemapping]] / [[dynamic-range-compression]] —— 多帧 HDR 与色调映射是计算摄影核心算法。
- [[depth-map-and-application]] —— 深度图驱动合成散景、3D、AR。
- [[isp-system]] —— 计算摄影与 ISP 主 pipeline 协同（RAW 计算）。
- [[image-quality-assessment]] —— 计算摄影结果（多帧/合成）的质量评测。
- [[image-compression]] —— 计算摄影输出常经压缩编码保存。

## 详细章节

### 定义

计算摄影指用数字计算代替光学过程的数字图像采集与处理技术。它能提升相机能力，或引入胶片摄影完全无法实现的功能（如机内计算数字全景、高动态范围图像、光场相机），或降低相机元件的成本与尺寸。计算摄影的定义已演化为覆盖计算机图形、计算机视觉与应用光学的一批主题领域，常用 Shree K. Nayar 提出的分类法组织。

### 与传统摄影的对比

- **传统摄影**：主要靠光学与化学/电子传感器记录光，能力受限于镜头、传感器与物理曝光。
- **计算摄影**：采集侧与处理侧都引入计算——多帧融合、计算光学、结构化照明、AI 重建，突破物理硬件的限制。

### 核心领域

#### 计算成像（Computational Imaging）

把数据采集与数据处理结合，通过间接手段重建物体图像，以获得更高分辨率或额外信息（如光学相位、3D 重建）。编码孔径成像：用针孔阵列替代单针孔，解卷积恢复图像，早期用于天文与 X 光成像。编码曝光成像：把快门开关编码以改变运动模糊核，使运动去模糊成为良态问题。镜头编码孔径：插入宽带掩模修改光圈，使散焦去模糊成为良态问题，也可改善光场采集质量。

#### 计算光学（Computational Optics）

设计光学元件与计算解码配合，例如波前编码、光场光学；编码孔径可用颜色滤光片在不同波长施加不同编码，比二进制掩模让更多光到达传感器。

#### 计算照明（Computational Illumination）

结构化控制摄影照明，再处理采集图像生成新图像，应用包括基于图像的重打光、图像增强、图像去模糊、几何/材质恢复。HDR 用同一场景不同曝光的照片扩展动态范围；也可处理融合不同照明的同题材图像（lightspace）。

#### 计算处理（Computational Processing）

对传统采集图像做计算改善：HDR 合成、全景拼接、多帧降噪、超分、去马赛克、去模糊、合成散景、RAW 计算等。

### 关键算法

- **多帧堆栈**：HDR（多曝光）、夜景（多帧降噪）、超分（亚像素融合）、去鬼影。
- **深度与散景**：深度图驱动选择性模糊（见 [[depth-map-and-application]]）。
- **去模糊**：编码曝光/编码孔径让去卷积良态化。
- **AI 重建**：深度学习去马赛克/去噪/超分/RAW 处理。

### 趋势与展望

- **RAW 级计算**：计算前移到 RAW 域，保留更多信息（与 ISP 协同，见 [[isp-system]]）。
- **AI 普及**：神经网络推理内置于 SoC，实现实时夜景/人像/超分。
- **传感器创新**：事件相机（DVS）、堆叠式传感器、片上计算。
- **计算光学回归**：编码孔径/光场/波前编码与 AI 解码结合。
- **效果**：让业余用户拍出接近专业的照片；截至 2019 年仍不全面超越专业级设备，但差距持续缩小。

### 挑战

- **运动与鬼影**：多帧融合在运动场景的鲁棒性。
- **实时与功耗**：计算量大，需软硬协同（NPU/ISP）。
- **评测**：合成结果的真实性、细节保真与伪影（见 [[image-quality-assessment]]）。
- **内容归属**：AI 生成/增强的真实性边界。

## 参考

- Computational photography：https://en.wikipedia.org/wiki/Computational_photography
- Nayar, S.K. 计算摄影分类法（Computational Cameras: Approaches, Benefits and Limits）
