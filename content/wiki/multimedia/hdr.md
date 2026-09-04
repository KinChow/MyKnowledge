---
aliases:
- HDR
- 高动态范围
- High Dynamic Range
- HDRI
confidentiality: public
domain: multimedia
evidence:
- claim: HDR（高动态范围）指场景或图像中光线水平变化大；动态范围指场景或图像中最亮区与最暗区之间的亮度范围。
  claim_id: hdr-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-15fd931b7867
    exact: "In this context, the term high dynamic range means there is a large amount of variation in light levels within a scene or an image. The dynamic range refers to the range of luminosity between the brightest area and the darkest area of that scene or image."
  targets:
  - evidence_id: evidence-15fd931b7867
    source_id: wiki-hdri
- claim: 摄影中的 HDR 技术通过拍摄同一场景多帧不同曝光再合并，得到高于单帧的、超出相机原生能力的动态范围。
  claim_id: hdr-capture
  support: direct
  supporting_quotes:
  - evidence_id: evidence-f41c52103f5f
    exact: "In photography and videography, a technique, commonly named high dynamic range (HDR) allows the dynamic range of photos and videos to be captured beyond the native capability of the camera. It consists of capturing multiple frames of the same scene but with different exposures and then combining them into one, resulting in an image with a dynamic range higher than the individually captured frames."
  targets:
  - evidence_id: evidence-f41c52103f5f
    source_id: wiki-hdri
id: hdr
kind: knowledge
publication_scope: public
related: []
sources:
- wiki-hdri
status: published
tags:
- camera
- isp
- hdr
- image-processing
- multimedia
title: 高动态范围（HDR）
updated_at: '2026-09-04'
---

# 高动态范围（HDR）

## 一句话结论

HDR（High Dynamic Range，高动态范围）指场景/图像中最亮与最暗区之间的亮度范围很大。相机的 HDR 成像通过拍摄同一场景**多帧不同曝光**再合并，得到超出单帧原生能力的动态范围，从而同时保留高光细节与暗部信噪比。HDR 合成的主要问题是鬼影与噪点，需经去鬼影（Rejection/Alignment/Optimization）后融合；受显示设备限制，最终需 DRC/色调映射压缩动态范围显示。

## 核心概念

- **动态范围（DR）**：最亮区与最暗区之间的亮度范围，衡量 sensor 在一幅图像里同时体现高光和阴影的能力。
- **多帧曝光合成**：多帧不同曝光 → 配准 → 融合 → 色彩恢复，得到高动态范围图像。
- **HDR 合成问题**：鬼影（运动物体在融合中虚影）、噪点（低曝光帧噪声）。
- **去鬼影**：Rejection-based / Alignment-based / Optimization-based。
- **动态范围压缩**：HDR 图在低动态范围显示设备上需 DRC/色调映射（见 [[tonemapping]]）。

## 工作机制

1. **采集**：对同一场景以不同曝光拍摄多帧（短曝光保留高光、长曝光保留暗部）。
2. **配准**：对齐各帧（消除相机抖动/运动导致的错位）。
3. **融合**：按像素质量（曝光适中、噪声低）加权合并各帧，扩展动态范围。
4. **色彩恢复**：融合后做色彩校正，还原场景真实颜色。
5. **压缩显示**：因显示设备动态范围有限，经 DRC/色调映射压缩到可显示范围。

## 示例或代码

动态范围定义与典型量级：

```text
DR = 20·log10(imax/imin)          （imax/imin 为最亮/最暗电流）

人眼          ~100 dB
普通 sensor   ~60 dB
高端 sensor   ~78 dB
自然场景      200+ dB
```

## 常见误区

- **"HDR 就是拉高对比度"**：HDR 是多帧不同曝光合成，扩展动态范围，不是简单对比度增强。
- **"HDR 图能直接显示"**：显示设备动态范围有限，HDR 图需 DRC/色调映射压缩后才能正常显示。
- **"HDR 没有代价"**：多帧合成降低帧率、易产生鬼影；BME/SME 等单帧方案各有分辨率/复杂度代价。
- **"HDR 能覆盖自然场景"**：sensor 动态范围（~60-80dB）远低于自然场景（200+dB），HDR 只是逼近。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| hdr-definition / hdr-capture | wiki-hdri | 动态范围定义 + 多帧曝光 HDR |

## 待验证项

无。

## 关联知识

- [[tonemapping]] —— HDR 图显示前的动态范围压缩。
- [[auto-exposure]] —— 多帧 HDR 需要不同曝光，与 AE 联动。
- [[demosaic]] —— HDR 融合发生在 raw 域处理后。

## 详细章节

### HDR 背景与动态范围

HDR 全称为 High Dynamic Range（高动态范围），目的是保留高光部分细节，同时提高欠曝部分的信噪比，让暗的和亮的部分都能看到更多细节。动态范围是衡量 sensor 在一幅图像里能同时体现高光和阴影内容的能力，以最亮/最暗电流之比的对数表示：

```text
DR = 20·log10(imax/imin)

人眼        100 dB
普通 sensor  60 dB
高端 sensor  78 dB 左右
自然场景    200+ dB
```

HDR 处理步骤：①获得 HDR 影像 ②以 HDR 方式处理 ③HDR 方式存储 ④HDR 方式显示。ISP 所说的 HDR 主要是 HDR 成像获取；由于显示设备动态范围有限，需 DRC 和 tone mapping 做动态范围压缩。一般认为 HDR 为 60dB 以上，实际图像对比度达 1000:1，10bit 有效带宽出图。

HDR 带来的问题：sensor 成本增加；有效带宽增加对 ISP 后续处理带来困难；仍远达不到自然场景的动态范围（200dB）。

### HDR 合成常见问题

- **鬼影**：同一位置的不同曝光帧像素不一致（相机抖动或物体局部运动），融合图像运动物体出现虚影。
- **噪点**：低曝光图像存在噪点，影响 HDR 合成质量。

### 去鬼影方法

- **Rejection-based（排除法）**：排除不同曝光像素间的不一致性，选取相对一致的像素。优点：结果解释性和可控性强、实现复杂度低；缺点：只参考当前位置像素信息，无法准确还原高反差运动物体的照度。
- **Alignment-based（对齐法）**：图像对齐，消除抖动/运动。优点：理论上找到对应点即可完全还原场景照度、不损失动态范围，对局部非刚性运动可精细化处理；缺点：很难完全对齐并引起新 artifact，稠密运动场计算复杂度较大。
- **Optimization-based（优化法）**：定义全局能量函数使其最小化。优点：综合亮度/对齐/运动信息、端到端、解决融合问题、效果相对最好；缺点：迭代次数多、计算量大。

### HDR 算法

#### 多帧曝光合成

步骤：①提取灰度图像 ②图像配准 ③灰度融合 ④图像色彩恢复。优点：保持图像空间分辨率；缺点：降低成像帧率、容易造成鬼影现象。

#### BME HDR

Binning Multiplexed Exposure HDR（BME-HDR）：交错长短曝光，通过择优选择短曝光或长曝光实现 HDR。优点：不影响成像帧率；缺点：垂直空间分辨率减半、会有鬼影现象。

#### SME HDR

Spatially Multiplexed Exposure HDR（SME-HDR）：同行像素不同曝光，通过 Sony 特殊算法实现 HDR。优点：全分辨率 HDR 输出；缺点：插值算法复杂。

#### Quadra HDR

- **正常模式**：快门时间一致，四像素合一，提高暗场景成像能力和信噪比。
- **HDR 模式**：设置长/中/短三种曝光时间，合成一帧 HDR 图像。

优缺点：场景和相机的相对运动减弱、减轻鬼影现象；缺点：demosaic 技术要求高、损失空间分辨率。

#### Stagger HDR

传感器级时序错开曝光的 HDR 方案（厂商私有实现）。

#### Google 的 HDR Plus

Google 用短曝光多帧 + 计算摄影（超分辨率融合）实现的 HDR 方案。

### Tone Mapping（HDR 动态范围压缩）

- **Global tone mapping**：①将不同曝光比生成的融合图像（通常 bit 位宽较大）进行数据压缩 ②通过全局亮度信息调整图像整体对比度，特别是保留高光区域信息。
- **Local tone mapping**：通过图像局部区域的亮度信息重新分布亮度，提高局部对比度和细节。

（完整色调映射算法见 [[tonemapping]]。）

## 参考

- https://en.wikipedia.org/wiki/High-dynamic-range_imaging
- Debevec P, Malik J. Recovering High Dynamic Range Radiance Maps from Photographs[C]. SIGGRAPH, 1997.
- Reinhard E, et al. High Dynamic Range Imaging: Acquisition, Display, and Image-Based Lighting[M]. 2nd ed, 2010.
