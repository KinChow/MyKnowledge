---
aliases:
- 传感器
- 图像传感器
- Image Sensor
- CMOS
- CCD
confidentiality: public
domain: multimedia
evidence:
- claim: 图像传感器用于成像，能够检测并传递形成图像所需的信息。
  claim_id: image-sensor-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-fc1795855e8e
    exact: An image sensor or imager is a sensor used for imaging. It detects and conveys information used to form an image.
  targets:
  - evidence_id: evidence-fc1795855e8e
    source_id: wikipedia-image-sensor-v2
id: sensor
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- wikipedia-image-sensor-v2
- working-multimedia-sensor
status: published
tags:
- camera
- sensor
- isp
- cfa
- multimedia
title: 图像传感器
updated_at: '2026-09-05'
---

# 图像传感器

## 一句话结论

图像传感器用于成像，检测并传递形成图像所需的信息：将镜头的光信号转化为电信号，再经内部 AD 转化为数字信号；每个像素只感光 R/G/B 中的一种，输出最原始的 RAW 数据。类型上 CCD 与 CMOS 光电转换原理相同、电荷与读取方式不同。sensor 由物镜、IR 滤光片、微透镜、滤光镜（CFA）、像素阵列、电路层堆叠而成（BSI 后照式/FSI 前照式差异在像素阵列与电路层前后）。常见缺陷包括黑电平、串扰（频谱/折射/电子转移）、光晕（亮度/色彩晕影）与卷帘快门果冻效应。

## 核心概念

- **图像传感器**：将光信号转化为电信号，再经 AD 转为数字信号，输出 RAW 数据。
- **CCD / CMOS**：光电转换原理相同，电荷与读取方式不同。
- **sensor 栈结构**：物镜 → IR 滤光片 → 微透镜 → 滤光镜（CFA）→ 像素阵列/电路层。
- **BSI（后照式）**：像素阵列在前、电路层在后，接收光更多、光电转换强；FSI（前照式）电路层在前、工艺简单。
- **滤光镜（CFA）**：只允许特定光通过；RGGB/MONO/RYYB/RGB-IR/RCCB/RCCC 等排列。
- **像素阵列**：光电二极管+电容，光→电流→电压。
- **工作时序**：帧时间 = 曝光时间 + 读取时间 + 帧间空白；sof/eof 标记帧边界。
- **sensor 缺陷**：黑电平（暗电流/放大/AD）、串扰、光晕、卷帘果冻效应。

## 工作机制

1. **光电转换**：光电二极管基于反向截止与光电效应——光强度越大反向电流越大，电流经电容转为电压信号。
2. **读取**：单像素（光→电压→模拟放大→AD 转换）；整图按行读取（行选择→放大→AD→列选择并转串→输出）。
3. **滤光**：IR 滤光片过滤红外光消除偏色；CFA 只允许特定光通过，每个像素只采集一种颜色 → 输出 Bayer RAW。
4. **时序**：sof 为第一行读取开始、eof 为最后一行读取结束，帧时间 = 曝光 + 读取 + 帧间空白。
5. **缺陷处理**：黑电平矫正（参考标定数据与 Optical black）；串扰用 color correction/BSI/加深电子井改善；光晕用 shading 矫正。

## 示例或代码

```text
sensor 栈（BSI 后照式）：
  物镜 → IR 滤光片 → 微透镜 → 滤光镜(CFA) → 像素阵列 → 电路层
sensor 栈（FSI 前照式）：
  物镜 → IR 滤光片 → 微透镜 → 滤光镜(CFA) → 电路层 → 像素阵列

帧时间 = 曝光时间 + 读取时间 + 帧间空白
sof = 帧开始（第一行读取开始）  eof = 帧结束（最后一行读取结束）

CFA 排列：RGGB（主流）/ MONO / RYYB / RGB-IR / RCCB / RCCC
```

## 常见误区

- **"CCD 和 CMOS 原理不同"**：两者光电转换原理相同，区别在电荷与读取方式。
- **"BSI 一定比 FSI 好"**：BSI 像素阵列在前接收光更多、光电转换强，但 FSI 工艺简单、成本低，需权衡。
- **"传感器直接输出彩色图像"**：每个像素只感光一种颜色，输出的是 Bayer RAW，颜色经 demosaic 等后续重建。
- **"黑电平应该为零"**：完全遮光时 sensor 输出不为 0（暗电流/放大/AD 引入），需黑电平矫正。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| image-sensor-definition | wikipedia-image-sensor-v2 | 图像传感器用于成像，检测并传递成像所需信息 |

## 待验证项

- sensor 栈结构、CFA 排列、读取时序、缺陷成因等具体内容来自内部工作笔记（working-multimedia-sensor），无公开权威来源，待人工复核。

## 关联知识

- [[black-level-correction]] —— 黑电平缺陷的矫正。
- [[defective-pixel-correction]] —— 坏点矫正（BPC）。
- [[lens-vignetting-correction]] —— 光晕（Lens shading）矫正。
- [[noise-evaluation]] —— 传感器噪声来源（光电转换/暗电流/增益）。
- [[isp-system]] —— sensor 输出 RAW 后的 ISP 处理链。
- [[optical-fundamentals]] —— 镜头光学与传感器成像的关系。

## 详细章节

- 将镜头的光信号转化为电信号，再经过内部 AD 将模拟电信号转化为数字信号。
- sensor 中每个像素点只能感光 R、G、B 中的一种，这些最原始的感光数据称为 RAW 数据。
- 类型：
  - CCD
  - CMOS
  - CMOS 和 CCD 光电转换原理相同，电荷和读取方式不同。

### sensor栈结构

#### 类型

##### BSI（后照式）

- 物镜
- IR 滤光片（IR cutter）
- 微透镜（micro lens）
- 滤光镜（color filter array）
- 像素阵列（sensor array）
- 电路层（wiring layer）

##### FSI（前照式）

- 物镜
- IR 滤光片（IR cutter）
- 微透镜（micro lens）
- 滤光镜（color filter array）
- 电路层（wiring layer）
- 像素阵列（sensor array）

##### BSI（后照式）和FSI（前照式）差异

FSI（前照式）电路层在前，像素阵列在后，优点工艺简单。

BSI（后照式）像素阵列在前，电路层在后，优点像素阵列可以接收更多的光，模组的光电转换强。

#### 滤光片（IR cutter）

滤光片过滤红外光，消除偏色。

#### 滤光镜（Color Filter Array）

滤光镜只允许特定的光通过，但是实际无法将所有的光分开。

##### 滤光镜分类

- RGGB
  - 主流 sensor，可以采集 R、G、B 信息。
- MONO
  - 收集亮度信息。
- RYYB
  - 将绿色分量替换为黄色分量。
- RGB-IR
  - 将 RGGB 中的一个绿色分量替换为 IR 信息。
- RCCB
  - 恢复亮度信息和 R 通道、B 通道信息。
- RCCC
  - 恢复亮度信息和 R 通道信息。

#### 像素阵列

单像素电路模型：光电二极管 + 电容

转换过程：

- e（光信号）→ a（电流信号）
- a（电流信号）→ v（电压信号）

光电二极管的工作原理：

- 二极管的反向截止特性
- 光电效应：光的强度越大，反向电流越大
- 电容：电流转电信号

#### 电路层

单个像素的读取过程：

1. 光信号转换为电压信号
2. 模拟放大
3. AD 转换

整图读取过程：

1. 行选择：一帧图像的输出是以行为单位的
2. 模拟放大
3. AD 转换
4. 列选择：多路选择器，并转串
5. 输出

#### 工作时序

$$
帧时间 = 曝光时间 + 读取时间 + 帧间空白
$$

读取时间：最后一行曝光结束到读取结束工作时间

sof：帧开始时刻，第一行读取开始的时刻

eof：帧结束时刻，最后一行读取结束的时刻

### sensor缺陷

#### 黑电平（black level）

##### 现象

用完全不透光的材料遮挡住 sensor 采集的光线，此时 sensor 的输出不为 0。

##### 产生原因

- 暗电流
- 模拟放大
- AD 转换

##### 如何改善

- 黑电平矫正：参考标定数据和 Optical black

#### 串扰（crosstalk）

##### 类型

- 频谱串扰
  - 产生原因：滤光镜无法完全滤除其他颜色的光
- 折射串扰
  - 产生原因：由于光的入射角度，本应入射到该像素点的光线，入射到其他像素点
- 电子转移串扰
  - 产生原因：像素的电子井存储过多电子，而产生溢出

##### 如何改善

- color correction 模块
- BSI 栈结构
- 增加电子井深度

#### 光晕（Lens shading）

##### 类型

- 亮度晕影
  - 产生原因：由于镜头是一个凸透镜，sensor 接收的光周边的强度比中间的强度小，中心和周边的亮度不一致
- 色彩晕影
  - 产生原因：类似三棱镜折射，经过透镜折射产生颜色不一致的现象

#### 果冻效应（Rolling shutter）

##### 现象

拍摄高速运动物体时，拍摄结果物体扭曲、倾斜、摇摆不定。

##### 产生原因

- 高速运动
- 卷帘曝光

## 参考

- Image sensor：https://en.wikipedia.org/wiki/Image_sensor
- 背照式传感器（BSI）：https://en.wikipedia.org/wiki/Back-illuminated_sensor
