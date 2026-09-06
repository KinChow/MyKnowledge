---
aliases:
- 图像质量评价
- IQA
- 视频质量评价
- Image Quality Assessment
confidentiality: public
domain: multimedia
evidence:
- claim: 图像质量可以表示成像系统对形成图像的信号进行采集、处理、存储、压缩、传输和显示时的准确程度。
  claim_id: image-quality-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-20ab7f83863b
    exact: Image quality can refer to the level of accuracy with which different imaging systems capture, process, store, compress, transmit and display the signals that form an image.
  targets:
  - evidence_id: evidence-20ab7f83863b
    source_id: wikipedia-image-quality-v2
id: image-quality-assessment
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- wikipedia-image-quality-v2
- working-multimedia-image-quality-assessment
status: published
tags:
- camera
- isp
- iqa
- quality
- multimedia
title: 图像视频质量评价
updated_at: '2026-09-04'
---

# 图像视频质量评价

## 一句话结论

图像质量表示成像系统对形成图像的信号进行采集、处理、存储、压缩、传输和显示时的准确程度。图像/视频质量评价（IQA）通过分析图像特性评估其失真程度：按主体分**主观**（人，MOS/DMOS）与**客观**（机器，分类器/回归器）；按参考源分**全参考/半参考/无参考**。成像领域用 DXO Mark 式评测（清晰度/噪声/曝光/颜色/均匀性/稳定性 + ISO/CPIQ 标准）；编解码领域用 PSNR/SSIM/VMAF/LPIPS 等有参算法。

## 核心概念

- **IQA 分类**：主观（MOS/DMOS，心理学实验）vs 客观（机器评价）；全参考/半参考/无参考。
- **成像评测维度**：清晰度（MTF50/ringing）、噪声（SNR/彩噪/暗信号）、曝光（ISO/色调曲线/对比度）、颜色（ΔE/白平衡/饱和度）、均匀性（色差/shading/畸变）、稳定性（时域）。
- **行业标准**：ISO TC4（12233/12232/15739 等）、CPIQ（IEEE P1858）。
- **编解码有参**：PSNR（像素统计）、SSIM（结构）、VMAF（机器学习融合）、LPIPS（深度学习）。
- **DXO**：综合主客观评分融合权重排名。

## 工作机制

1. **评测维度**：按清晰度/噪声/曝光/颜色/均匀性/稳定性采集客观指标（MTF50、SNR、ΔE 等）与主观感知。
2. **评测环境**：控制光源（自动照明）、图卡（点图/枯叶图/色卡/MTF 图/HDR 图）、分析软件（DXOMARK Analyzer）。
3. **编解码评价**：有参——信号域（PSNR）、视觉特征（SSIM）、机器学习（VMAF 融合 VIF/DLM/运动量）、深度学习（LPIPS）；无参——抖动/清晰度/亮度/噪声一致性。

## 示例或代码

```text
有参评价指标：
  PSNR  ：MSE/峰值信噪比，像素统计，简单快但与主观一致性低
  SSIM  ：亮度+对比度+结构三方面，融入人眼结构感知
  VMAF  ：SVM 融合 VIF（信息保真）+ DLM（细节丢失）+ 运动量
  LPIPS ：CNN 特征回归，深度学习

清晰度指标：
  MTF50：对比度剩 50% 的频率（cycle/pixel 或 cycle/height）
  Ringing：振铃（黑亮边缘增强出过度带）
  Nyquist：数字图像能给出的最大频率（分辨率的一半）
```

## 常见误区

- **"PSNR 高就一定质量好"**：MSE/PSNR 与主观一致性低，相同 PSNR 可对应感官差异很大的失真。
- **"客观评价能替代主观"**：客观评价目标是逼近主观（MOS/DMOS），但主观准确可靠、客观自动便捷，两者互补。
- **"无参考评价容易"**：无参考只有失真图像，难度最高、精度最低。
- **"成像评测只测清晰度"**：还需噪声、曝光、颜色、均匀性、稳定性等多维度（DXO 式）。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| image-quality-definition | wikipedia-image-quality-v2 | 图像质量 = 成像系统各环节的准确程度 |

## 待验证项

无。

## 关联知识

- [[noise-evaluation]] —— 噪声评价（SNR/视觉噪声）。
- [[basic-of-color]] —— 颜色评价（ΔE/白平衡/色域）。
- [[dynamic-range-compression]] —— 曝光/对比度评价相关。

## 详细章节

### IQA简介

#### IQA是什么

图像质量评价（Image Quality Assessment, IQA）以及视频质量评价，主要通过对图像进行特性分析研究，然后评估出图像优劣（图像失真程度）的方法。

- **按评价主体划分**：主观质量评价（人对于图片的主观感知评价，用 MOS 或 DMOS 指标定量描述，通过开展主观心理学实验获取）；客观质量评价（评价主体为机器，通常是设计一个分类器或回归器对图片进行评价）。
- **按是否有参考源划分**：全参考（拥有无失真的原始图像，精度相对较高）；半参考（只有原始图像的部分信息或从参考图像中提取的部分特征）；无参考（仅有失真图像而无任何参考图像，难度较高、精度较低）。

评价主体分类：主观评价准确可靠但耗时耗力；客观评价逼近主观评价水平、自动便捷。

#### IQA能做什么

场景价值（采编传显）：

- **成像领域**：手机拍照、车载、监控等领域，用于测量 Lens->Sensor->ISP->后处理增强等通路形成的各种质量损失（如偏色、对焦模糊、噪声、渐晕等），帮助产品提升产品质量。
- **编解码领域**：图像/视频编解码、传输领域，用来测量编码器引入的损伤（如块效应、模糊等），帮助提升编解码质量。

### 成像领域

#### DXO Mark总览

- 从清晰度、噪声、曝光、颜色、均匀性、以及时域稳定性等指标进行评测
- 综合照片、变焦、视频场景等主客观评分，融合权重，计算总体得分，进行排名

#### 成像评测维度

- **清晰度**：解析力（客观 MTF50/Acutance/ringing；主观 模糊/过锐）、AF（客观 准确性/速度；主观 清晰度/速度）。
- **噪声**：噪声（客观 SNR/grain size；主观 大小/密集度/对比度）、彩噪（客观 coloration index；主观 彩噪数量/颜色）、暗信号与像素缺陷（客观 Dark Signal/Bright pixels/Dark pixels）。
- **曝光**：ISO（客观 ISO sensitivity）、色调曲线（客观 gamma2.2）、灰阶/高动态/对比度（客观 contrast range/tonal range；主观 死黑/过曝/朦胧）。
- **颜色**：白平衡与色偏（客观 Δab；主观 偏色/不白）、饱和度（客观 ΔH；主观 不艳丽）。
- **均匀性**：横向色差（客观 distance of color center；主观 边缘带颜色）、纵向色差（客观 MTF 通道差；主观 紫边）、shading（客观 luminance/color vignetting；主观 暗角）、畸变（客观 TV 系数；主观 周边压扁/拉长）。
- **稳定性**：清晰度（客观 zoom 解析力/zoom AF code/运动 AF code；主观 主体清晰）、曝光（客观 ΔY；主观 亮度闪烁）、噪声（客观 Y 均方差；主观 噪声跳动）、颜色（客观 Δab；主观 颜色跳变）、FOV（客观 缩放平滑；主观 缩放卡/位置跳跃）、防抖（客观 ΔX/ΔY/ΔRoll/ΔYaw/Δpitch；主观 画面抖动）。

#### DXO客观评测方法

- **整套环境**：光源（控制亮度、色温等；带照度反馈回路的自动照明控制系统）、图卡（点图/枯叶图/色卡/MTF 图卡——点图测 shading/锐度/畸变/焦距、径向 MTF 图测不同位置 MTF、HDR 图测动态与色调范围/色调曲线/噪声、色卡测白平衡/色彩还原度/色彩敏感度）、分析软件（DXOMARK Analyzer）、其他（架子、滑轨等）。

#### 行业标准

- **ISO TC4**：ISO 12233（分辨率和空间频率）、ISO 12232（ISO/标准输出感光度）、ISO 15739（噪声和动态范围）、ISO 14524（色调曲线 OECF）、ISO 17850（几何畸变）、ISO 17957（均匀度/阴影测量）、ISO 18844（耀斑 Flare）、ISO 19084（色移/紫边）、ISO 19567（纹理）。
- **CPIQ (IEEE P1858)**：空间频率响应、横向色位移、颜色均匀度、几何畸变、纹理模糊、噪声、色度。

#### 色彩

- **CIELAB**：为涵盖正常人可见范围所有色彩设计的色彩空间，其欧式距离与人眼所能识别的偏差相对应。
- **ΔE\*/ΔC\*/ΔH\*/Δab\***：分别表示欧式距离、色度误差、色调误差、色彩误差。
- **White balance**：白平衡，校正白点的色彩误差。

#### 清晰度

- **Modulation Transfer Function**：调制传递函数。
- **Spatial Frequency Response**：空间频率响应。
- **MTF50**：对比度剩余 50% 时对应的频率（常说的 MTF 多少线对），单位 cycle/pixel 或 cycle/height。
- **Ringing**：振铃效应，一黑亮边缘通过图像处理增强出更加黑亮过渡带的现象。
- **Nyquist**：奈奎斯特频率，数字图像中能给出的最大频率（分辨率的一半），超出此数字黑白线对无法呈现。

### 编解码领域

#### 视频编解码质量评价算法-有参

在视频编码环节，质量评价和测试分为以下几类（有参考）：

- **信号域**：以 PSNR 为代表，基于信噪比，仅孤立考虑像素差异。
- **视觉特征**：以 SSIM（MSSSIM）为代表，基于空间特征，只考虑空域（亮度相似度、对比度相似度和结构相似度）。
- **机器学习**：以 VMAF（开源）为代表，基于主观感知，考虑多种感知因素通过机器学习算法。
- **深度学习**：以 LPIPS（开源）为代表，基于 CNN 卷积网络提取特征进行回归。

##### PSNR

均方误差（MSE）和峰值信噪比（PSNR）是比较常见的两种基于像素统计的有参质量评价方法，通过计算待评测图像和参考图像对应像素点灰度值之间的差异，从统计角度衡量待评图像的质量优劣。由于简单易用速度快，应用十分广泛（H.264/AVC 和 H.265/HEVC 中 PSNR 依然是最主要的客观评价方法）。但 MSE/PSNR 与主观的感受一致性低，并不能完全反应人眼视觉系统的感受——相同 MSE/PSNR 可对应感官差异非常大的各种失真。

##### SSIM

结构一致性（SSIM）是基于结构信息的有参质量评价方法。基于人类视觉感知能高度自适应提取场景中的结构信息，该方法认为图像的结构失真的度量应是图像感知质量的最好近似，因此从亮度、对比度、结构三方面描述像素间的一致性。SSIM 实现简单、融入了人眼视觉感受信息，质量评估结果可靠；相同 MSE/PSNR 的失真图像，SSIM 能准确分辨出主观质量好坏。

##### VMAF

视频多评估方法融合（Video Multi-method Assessment Fusion，VMAF）指标是将人类视觉模型与机器学习相结合的视频质量评价指标。VMAF 在支持向量机（SVM）回归因子中使用下列基本指标进行融合：

- **空域指标**：视觉信息保真度（Visual Information Fidelity, VIF，用信息论比较人眼从失真与原始图像提取的信息）；细节丢失指标（Detail Loss Metric, DLM，衡量可能影响内容可见性的细节丢失，VMAF 中只使用 DLM）。
- **时域指标**：运动量（衡量相邻帧之间时域差异，计算像素亮度分量差值的均值）。

### 媒体质量评价探索

- **成像领域：图像视频的美学评价**：搭建美学评价模型，初步建立美学评价各子维度（光照、色彩、构图）的评价标准和总体评价能力。输入图像或视频，输出光照/构图/色彩，评价指标 MSE、SROCC。
- **视频无参质量评价算法**：包含抖动、清晰度、亮度、噪声等一致性评价算法。
- **有参算子：光影秩序错误检测算法**：亮度秩序错误（LOE-Lightness Order Error）作为客观衡量图像后处理对光影亮度改变程度的有参图像评价指标，用于 HDR 风格生成、CG 渲染等各类图像后处理方法的光影整体评价及问题定位。

## 参考

- Image quality：https://en.wikipedia.org/wiki/Image_quality
- DXO Mark / ISO TC4 / CPIQ（IEEE P1858）成像评测标准
- PSNR/SSIM/VMAF/LPIPS 编解码质量评价算法
