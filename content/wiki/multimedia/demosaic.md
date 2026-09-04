---
aliases:
- 去马赛克
- Demosaicing
- Debayering
- CFA interpolation
confidentiality: public
domain: multimedia
evidence:
- claim: 去马赛克（Demosaicing，又称色彩重建）是从覆有滤色阵列（CFA，如 Bayer 滤色阵）的传感器输出的不完整颜色采样，重建全彩图像的数字图像处理算法。
  claim_id: demosaic-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-1b4036ae3965
    exact: "Demosaicing, also known as color reconstruction, is a digital image processing algorithm used to reconstruct a full color image from the incomplete color samples output from an image sensor overlaid with a color filter array (CFA) such as a Bayer filter."
  targets:
  - evidence_id: evidence-1b4036ae3965
    source_id: wiki-demosaicing
- claim: 传感器每个像素在滤色片后只输出三种滤色之一的光强，因此需要算法为每个像素估计所有颜色分量的色级，而非单一分量。
  claim_id: demosaic-single-pixel
  support: direct
  supporting_quotes:
  - evidence_id: evidence-97ea187b1d05
    exact: "Since each pixel of the sensor is behind a color filter, the output is an array of pixel values, each indicating a raw intensity of one of the three filter colors. Thus, an algorithm is needed to estimate for each pixel the color levels for all color components, rather than a single component."
  targets:
  - evidence_id: evidence-97ea187b1d05
    source_id: wiki-demosaicing
- claim: 高级去马赛克算法利用像素的空间相关与谱相关：空间相关指同质小区域内像素取相近颜色值，谱相关指小区域内不同颜色平面的像素值相互依赖。
  claim_id: demosaic-correlation
  support: direct
  supporting_quotes:
  - evidence_id: evidence-453b0e3eba11
    exact: "More sophisticated demosaicing algorithms exploit the spatial and/or spectral correlation of pixels within a color image. Spatial correlation is the tendency of pixels to assume similar color values within a small homogeneous region of an image. Spectral correlation is the dependency between the pixel values of different color planes in a small image region."
  targets:
  - evidence_id: evidence-453b0e3eba11
    source_id: wiki-demosaicing
- claim: Bayer 滤色阵的排列为半绿、四分之一红、四分之一蓝，故也称 BGGR、RGBG、GRBG 或 RGGB。
  claim_id: bayer-pattern
  support: direct
  supporting_quotes:
  - evidence_id: evidence-429e23e81582
    exact: "The filter pattern is half green, one quarter red and one quarter blue, hence is also called BGGR, RGBG, GRBG, or RGGB."
  targets:
  - evidence_id: evidence-429e23e81582
    source_id: wiki-bayer-filter
- claim: Bayer 每个像素只记录三色之一，数据本身无法给出完整 RGB 值，需用去马赛克算法由周围同色像素插值得到每个像素的完整红绿蓝值。
  claim_id: bayer-needs-demosaic
  support: direct
  supporting_quotes:
  - evidence_id: evidence-d3cba69be38a
    exact: "Since each pixel is filtered to record only one of three colors, the data from each pixel cannot fully specify each of the red, green, and blue values on its own. To obtain a full-color image, various demosaicing algorithms can be used to interpolate a set of complete red, green, and blue values for each pixel. These algorithms make use of the surrounding pixels of the corresponding colors to estimate the values for a particular pixel."
  targets:
  - evidence_id: evidence-d3cba69be38a
    source_id: wiki-bayer-filter
- claim: 去马赛克最常见的伪影是摩尔纹（Moiré），表现为重复图案、颜色伪影或不真实的迷宫状排列。
  claim_id: demosaic-artifacts
  support: direct
  supporting_quotes:
  - evidence_id: evidence-1717e3722229
    exact: "The most frequent artifact is Moiré, which may appear as repeating patterns, color artifacts or pixels arranged in an unrealistic maze-like pattern."
  targets:
  - evidence_id: evidence-1717e3722229
    source_id: wiki-bayer-filter
id: demosaic
kind: knowledge
publication_scope: public
related: []
sources:
- wiki-bayer-filter
- wiki-demosaicing
status: published
tags:
- camera
- isp
- image-processing
- bayer
- demosaic
title: 去马赛克（Demosaicing）
updated_at: '2026-09-04'
---

# 去马赛克（Demosaicing）

## 一句话结论

去马赛克（Demosaicing，又称色彩重建/CFA 插值）是把覆有 Bayer 滤色阵列的传感器输出的单色采样（每像素只有 R/G/B 之一）重建为全彩图像的过程。其核心是利用像素的**空间相关**（同质区颜色相近）与**谱相关**（不同颜色平面相关）来插值缺失的颜色分量；不同的插值策略在清晰度、伪彩色、摩尔纹等伪影之间权衡，是相机 ISP 中承上（raw 域）启下（后续色彩处理）的关键一步。

## 核心概念

- **Bayer CFA**：单芯片传感器普遍采用的滤色阵列，排列为半绿、四分之一红、四分之一蓝（RGGB/BGGR/GRBG/GBRG）。
- **去马赛克（Demosaicing）**：从 CFA 不完整颜色采样重建全彩图像；又称 CFA 插值 / Debayering。
- **空间相关（Spatial correlation）**：同质小区域内像素颜色相近，可作为插值依据。
- **谱相关（Spectral correlation）**：同一小区域内不同颜色平面（R/G/B）的像素值相互依赖，可用色差（R-G、B-G）或色调（R/G、B/G）约束插值。
- **伪影（Artifacts）**：摩尔纹、锯齿、伪彩色——去马赛克质量的主要权衡点。

## 工作机制

1. **采集**：sensor 每个像素只记录一种颜色（Bayer 阵各像素在红/绿/蓝滤色片后输出对应光强）。
2. **补色**：对每个像素，用其周围同色像素（空间相关）+ 异色平面关系（谱相关）估计缺失的两个颜色分量。
3. **输出**：得到每个像素的完整 RGB（RGB444/真彩色），进入后续白平衡、色彩校正等处理。

## 示例或代码

以 RGGB 阵中一个绿色像素（G）为例，其红色分量由两侧红色像素插值、蓝色分量由上下蓝色像素插值（双线性）：

```text
R  G  R
G  B  G      ->  中心 G 像素的 R = (左右 R 平均)，B = (上下 B 平均)
R  G  R
```

更高级的 MHC（Malvar-He-Cutler）算法在双线性基础上加入拉普拉斯跨通道校正：

```text
G 通道已知；估计 R 时用 R 邻域 + G 的二阶梯度（Laplacian）做交叉校正：
R_est = R_mean + (G_center - G_laplacian) / 2  （示意）
```

## 常见误区

- **"去马赛克只影响分辨率"**：去马赛克策略直接决定边缘清晰度、伪彩色与摩尔纹强度，是图像质量的关键一环。
- **"Bayer 阵都是 RGGB"**：RGGB/BGGR/GRBG/GBRG 都是 Bayer（只是排列方向不同），还有 Foveon X3、three-CCD 等不需要去马赛克的方案。
- **"双线性插值就够"**：双线性有严重的模糊、伪彩色与拉链效应；现代 ISP 用边缘自适应/MHC 等更优算法。
- **"摩尔纹是镜头问题"**：摩尔纹主要源于 Bayer 亚采样在高频细节区恢复错误颜色，属于去马赛克/采样层面的问题（可在 CFA 前加低通滤波缓解）。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| demosaic-definition / demosaic-single-pixel / demosaic-correlation | wiki-demosaicing | 定义 + 单像素单色 + 空间/谱相关 |
| bayer-pattern / bayer-needs-demosaic / demosaic-artifacts | wiki-bayer-filter | 滤色阵排列 + 需插值 + 摩尔纹伪影 |

## 待验证项

无。

## 关联知识

- [[android-camera-architecture]] —— Camera HAL3 流水线中，去马赛克位于 raw 域处理链（BLC/DPC 之后、色彩处理之前）。

## 详细章节

### 色彩感知方式对比

- **three-CCD camera**：三块感光片分别接收 R/G/B，无需去马赛克，但体积与成本高。
- **Foveon X3**：垂直堆叠三层感光元件（各层对不同波长敏感），无需去马赛克。
- **Bayer CFA**：单芯片、每像素单色，需去马赛克——消费级相机的主流方案。

### 去马赛克方法

- **最近邻复制（Nearest neighbor replication）**：最简单；缺陷是分辨率降低（相当于下采样）。
- **双线性插值（Bilinear）**：用邻域同色像素平均；缺陷是模糊、伪彩色、拉链效应（zipper）。
- **MHC（Malvar-He-Cutler Linear Image Demosaicking）**：基于谱相关，在双线性基础上添加 Laplacian 跨通道校正。优点比双线性锐利；缺点仍有较明显伪彩色。来源：https://www.ipol.im/pub/art/2011/g_mhcd/article.pdf
- **边缘自适应（Edge-adaptive）**：结合谱相关与空间相关（边缘检测），沿边缘方向插值避免跨边缘插值导致的锯齿与颜色溢出；代表如 Hamilton-Adams 算法。来源：https://patents.google.com/patent/US5652621A/en

### 去马赛克难点

- **摩尔纹**：CFA 的亚采样特性在高频区域容易恢复出错误颜色而产生细密摩尔纹；缓解思路是采样分辨率远高于景物细节（CFA 前加低通滤波、提高像素密度）。
- **锯齿效应**：插值未沿边缘进行而是横跨边缘，产生模糊与颜色溢出；按空间相关原则沿边缘插值可缓解。
- **伪彩色**：插值不当出现在色彩边缘处的错误颜色；常用中值滤波缓解，但对点多、线多的图像需谨慎（易丢细节）。

## 参考

- https://en.wikipedia.org/wiki/Demosaicing
- https://en.wikipedia.org/wiki/Bayer_filter
- Malvar H, He L, Cutler R. High-Quality Linear Interpolation for Demosaicing of Bayer-Patterned Color Images[C]. ICASSP, 2004.（MHC 论文）
- Hamilton J F, Adams J E. Adaptive Color Plane Interpolation in Single Sensor Color Electronic Camera: US Patent 5,652,621[P]. 1997.
