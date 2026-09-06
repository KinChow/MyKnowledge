---
aliases:
- 频域降噪
- Frequency Domain Noise Reduction
- 频域去噪
confidentiality: public
domain: multimedia
evidence:
- claim: |-
    There are many noise reduction algorithms in image processing. In selecting a noise reduction algorithm, one must weigh several factors: the available computer power and time available; whether sacrificing some real detail is acceptable if it allows more noise to be removed; and the characteristics of the noise and the detail in the image, to better make those decisions.
  claim_id: frequency-domain-noise-reduction-audit-1
  support: direct
  supporting_quotes:
  - evidence_id: evidence-04c098537dac
    exact: |-
      There are many noise reduction algorithms in image processing. In selecting a noise reduction algorithm, one must weigh several factors: the available computer power and time available; whether sacrificing some real detail is acceptable if it allows more noise to be removed; and the characteristics of the noise and the detail in the image, to better make those decisions.
  targets:
  - evidence_id: evidence-04c098537dac
    source_id: wiki-noise-reduction
id: frequency-domain-noise-reduction
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- wiki-noise-reduction
- working-multimedia-frequency-domain-noise-reduction
status: published
tags:
- camera
- isp
- noise-reduction
- frequency-domain
- multimedia
title: 频域降噪
updated_at: '2026-09-04'
---

# 频域降噪

## 一句话结论

频域降噪利用信号在空间上的连续性，把图像变换到频率域后在频域分离信号与噪声：噪声（及边缘/细节）是高频，平滑区域是低频。通过傅里叶变换/DCT/小波变换到频域，滤除或阈值处理高频（噪声），再反变换回空域。选择降噪算法需权衡算力/时间、是否接受牺牲细节换降噪、噪声与细节特性。小波变换（噪声系数小，丢小系数去噪，硬/软阈值）与 BM3D 是主流方法。

## 核心概念

- **频域**：频率变量 (u,v) 定义的空间；低频 = 慢变化（平滑区），高频 = 快变化（边缘/细节/噪声）。
- **傅里叶变换**：任何周期函数是不同振幅/相位正弦波的叠加；空域↔频域变换基础。
- **高斯滤波**：高通（边缘锐化）vs 低通（平滑模糊）。
- **DCT**：离散余弦变换，实偶函数的傅里叶只含余弦项，实数域替代；阈值滤高频去噪。
- **小波变换**：有限长衰减小波基；噪声系数小，丢小系数去噪；硬阈值逼近好但振荡、软阈值光滑但误差大。
- **BM3D**：稀疏 3D 变换域协同滤波。

## 工作机制

1. **变换**：把图像从空域变换到频域（傅里叶/DCT/小波）。
2. **分离**：在频域识别噪声（高频、小系数）与信号。
3. **处理**：滤波（高通/低通）或阈值处理（小波软/硬阈值、DCT 阈值）去除噪声高频分量。
4. **反变换**：变换回空域得到去噪图像。

## 示例或代码

```text
频域对应关系：
  低频 = 平滑区域（慢变化）
  高频 = 边缘、细节、噪声（快变化）

小波阈值去噪流程：
  原始图像 → 小波变换得各维度系数 → 阈值处理 → 小波重构 → 去噪图像
  硬阈值：逼近性好但附加振荡
  软阈值：光滑但误差较大
```

## 常见误区

- **"噪声全是高频"**：噪声主要是高频，但边缘/细节也是高频；无差别滤高频会抹掉细节。
- **"傅里叶变换够用"**：DFT 需复数运算实时不便；DCT 是实数域替代；小波能更好保存尖峰/突变。
- **"低通滤波就好"**：低通丢尖锐细节使图像模糊，需权衡降噪与保细节（算力/时间、细节损失）。
- **"小波阈值随便选"**：硬阈值逼近好但有振荡，软阈值光滑但误差大，需按信号特性选择。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| frequency-domain-noise-reduction-audit-1 | wiki-noise-reduction | 选降噪算法权衡算力/细节损失/噪声特性 |

## 待验证项

无。

## 关联知识

- [[space-domain-noise-reduction]] —— 空域降噪与频域降噪互补。
- [[time-domain-noise-reduction]] —— 时域降噪利用帧间相关性。
- [[demosaic]] —— 降噪位于 raw 域处理链。

## 详细章节

### 背景

图像作为二维信号，某点的灰度级就是该点幅度；频率是信号变化的快慢，即图像空间上灰度变化快慢。频域是频率变量 (u,v) 定义的空间，图像频率分量 (u,v) 与空间变量 (x,y)（灰度变化模式）的联系：

1. 变化最慢的频率成分（u=v=0）对应一幅图像的平均灰度级
2. 当从变换原点移开时，低频对应图像的慢变化分量（平滑部分）
3. 进一步离开原点时，高频对应图像中变化越来越快的灰度级

什么地方灰度级变化越来越快？图像边缘（高频显示边缘）、细节处（灰度急剧变化）、图像噪声（噪点与正常点颜色不同、灰度快速变化，也是高频）。

### 方法

#### 频域降噪方法

思想：利用信号在空间上的连续性，将图像信号变换到频率域，在频率域将信号和噪声分离，进而完成降噪。

#### 傅里叶变换

空域-频域变换方法，图像的傅里叶变换（Fourier Transform）。任何周期函数都可以看作是不同振幅、不同相位正弦波的叠加。

#### 高通高斯滤波器

- 高频通过，低频衰减。
- 图像减少了灰度级的平滑过渡而突出了边缘等细节部分，使图像变得锐化。

#### 低通高斯滤波器

- 低频通过，高频衰减。
- 图像丢失尖锐的细节部分而突出了平滑过渡部分，使图像变得模糊。

#### DCT变换

DCT（Discrete Cosine Transform，离散余弦变换），类似于离散傅里叶变换。离散傅里叶变换需要进行复数运算，在实时处理中非常不便；根据离散傅里叶变换的性质，实偶函数的傅里叶变换只含实的余弦项，因此构造了实数域的变换——离散余弦变换（DCT）。利用 DCT 降噪的思路：对图像做 DCT 变换，在变换后的频率域设置阈值、过滤掉高频部分（通常认为噪声都是高频部分），再 DCT 反变换回图像。

#### 小波变换

图像小波变换（Wavelet Transform）：将傅里叶变换中无限长的三角函数基换成有限长的会衰减的小波基。对 M×N 的二维图像先经过水平滤波器组分解成低频和高频分量，再通过垂直滤波器组，最终分解为 4 个子带图像数据（M/2）×（N/2）；变换后的 3 个高频分量 LH、HL、HH，低频分量 LL 送到下一级滤波器组做第二级变换，依次类推，最终完成二维 Haar 小波变换。

小波变换可以很好地保存有效信号的尖峰和突变部分。结论：在小波域，噪声的小波系数相对较小，所以常采用将较小的小波系数丢掉的方法降噪。

**阈值去噪流程**：1. 原始图像 2. 小波变换得到各维度系数 3. 阈值处理 4. 小波重构得到去噪图像 5. 最终图像。

- **阈值门限选取**：固定阈值估计、极值阈值估计。
- **阈值函数处理**：硬阈值去噪（重构信号逼近性更好，但有附加振荡）；软阈值去噪（重构信号更光滑，但误差相对较大）。

### 应用

BM3D（稀疏 3D 变换域协同滤波）。

## 参考

- 图像傅里叶变换与频域滤波：Gonzalez R C, Woods R E. Digital Image Processing[M]. 4th ed, 2018
- 小波去噪（软/硬阈值）：Donoho D L. De-noising by soft-thresholding[J]. IEEE Trans IT, 1995
- BM3D：Dabov K, et al. Image Denoising by Sparse 3-D Transform-Domain Collaborative Filtering[J]. IEEE TIP, 2007
