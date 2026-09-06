---
aliases:
- 图像压缩
- Image Compression
- 数据压缩
- 有损压缩
- 无损压缩
confidentiality: public
domain: multimedia
evidence:
- claim: 数据压缩（也称 source coding 或 bit-rate reduction）是用比原始表示更少的比特数对信息进行编码的过程。
  claim_id: image-compression-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-a195894bbdb2
    exact: data compression, source coding, or bit-rate reduction is the process of
      encoding information using fewer bits than the original representation
  targets:
  - evidence_id: evidence-a195894bbdb2
    source_id: web-multimedia-image-compression
id: image-compression
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-multimedia-image-compression
status: published
tags:
- camera
- isp
- compression
- codec
- multimedia
title: 图像压缩
updated_at: '2026-09-06'
---

# 图像压缩

## 一句话结论

图像压缩是数据压缩在图像上的应用：用比原始表示更少的比特数编码图像信息，任何压缩要么有损（lossy，移除"不必要/次要"信息）要么无损（lossless，消除统计冗余、不丢任何信息）。压缩利用**编码冗余、像素间冗余（空间/时间）与心理视觉冗余**三类冗余减比特；空间编码（帧内，DCT/小波 + 量化 + 熵编码，如 JPEG/JPEG 2000/HEVC-I）与时间编码（帧间，运动补偿，如 H.264/H.265/AV1）是两大方向。无损格式（PNG/GIF/JPEG-LS）保真但压缩比低，有损格式（JPEG/WebP/HEIF）以可控失真换高压缩比，用压缩比/比特率与 PSNR/SSIM/VMAF 等评测（见 [[image-quality-assessment]]）。在相机链路中，压缩发生在 ISP 输出之后（JPEG/HEIF 编码）或录像编码（H.264/H.265）。

## 核心概念

- **数据压缩**：用更少比特编码信息的编码过程；执行压缩的器件叫**编码器（encoder）**，执行逆过程（解压）的叫**解码器（decoder）**，合称 CODEC。
- **有损压缩**：移除不必要/次要信息，压缩比高、有失真；无损压缩：消除统计冗余，无信息丢失、压缩比低。
- **三类冗余**：编码冗余（码字概率不均）、像素间冗余（相邻像素/帧相关）、心理视觉冗余（人眼不敏感的信息）。
- **空间编码（帧内）**：单帧内的冗余消除（变换+量化+熵编码）。
- **时间编码（帧间）**：视频帧间冗余消除（运动估计/补偿 + 残差编码）。
- **压缩比/比特率**：原始比特数 / 压缩后比特数；每像素/每帧的比特率。

## 工作机制

1. **空间压缩**：变换（DCT/小波，去相关集中能量）→ 量化（丢心理视觉不敏感的高频）→ 熵编码（Huffman/算术/范围编码，编码冗余）。
2. **时间压缩（视频）**：运动估计/补偿利用帧间冗余，只编码残差与运动矢量。
3. **无损压缩**：预测/变换后无损量化 + 熵编码，不丢任何信息（如 PNG、JPEG-LS、FLAC 思路）。
4. **解码**：熵解码 → 反量化 → 逆变换 → 重建图像/帧。

## 示例或代码

```text
压缩分类：
├─ 无损（lossless）   : PNG、GIF、BMP(RLE)、JPEG-LS、WebP(无损)、FLIF
└─ 有损（lossy）      : JPEG、JPEG 2000、WebP(有损)、HEIF/AVIF、H.264/H.265/AV1
                        ├─ 空间（帧内）：JPEG(DCT)、JPEG 2000(小波)
                        └─ 时间（帧间）：H.264/H.265/AV1（运动补偿 + 帧内帧）
```

```python
import cv2
# OpenCV 写 JPEG，quality 0~100，越大画质越好、文件越大
cv2.imwrite("out.jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 90])
# PNG 无损，压缩级别 0~9
cv2.imwrite("out.png", img, [cv2.IMWRITE_PNG_COMPRESSION, 3])
```

## 常见误区

- **"压缩就一定损失质量"**：无损压缩（PNG/JPEG-LS）不丢任何信息。
- **"压缩比越高越好"**：有损压缩比越高失真越大，需在存储/带宽与质量间权衡；视频还要权衡编码延迟与计算量。
- **"压缩只利用空间冗余"**：视频还有时间冗余（帧间），静态图也可用调色板/预测等多类冗余。
- **"压缩只是编码器的事"**：压缩质量与源图像（ISP 输出噪声/细节）、编码参数、评测方法强相关。
- **"重复压缩无害"**：有损格式反复转码会累积失真（generation loss）。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| image-compression-definition | web-multimedia-image-compression | 压缩 = 用更少比特编码；有损/无损两类 |

## 待验证项

- 各格式的压缩比/特性数据来自公开资料（Wikipedia 与格式规范），具体数值待按目标格式复核。
- 相机链路中 JPEG/HEIF 编码的具体参数（quality、色彩子采样）以产品实现为准。

## 关联知识

- [[jpeg]] —— 最常用的有损图像压缩标准，压缩技术的具体实例。
- [[image-file-format]] —— 压缩后图像的容器格式（JPEG/PNG/HEIF/RAW）。
- [[image-quality-assessment]] —— 压缩质量评测（PSNR/SSIM/VMAF）。
- [[isp-system]] —— 压缩位于 ISP pipeline 之外（编码环节）。
- [[image-scaling]] —— 与压缩同属主 pipeline 外的后处理能力。

## 详细章节

### 定义

数据压缩（data compression）、信源编码（source coding）或比特率缩减（bit-rate reduction）是用比原始表示更少的比特数对信息进行编码的过程。任何特定的压缩要么有损要么无损：

- **无损压缩**：通过识别并消除统计冗余来减少比特，不丢失任何信息。
- **有损压缩**：通过移除不必要或次要的信息来减少比特。

通常执行压缩的器件称为**编码器（encoder）**，执行逆过程（解压）的称为**解码器（decoder）**，二者合称编解码器（CODEC）。

### 冗余类型

压缩能有效的前提是数据存在冗余：

- **编码冗余（Coding redundancy）**：不同码字出现概率不同，用熵编码（Huffman/算术编码）给高概率码字短码、低概率长码。
- **像素间冗余（Interpixel redundancy）**：相邻像素/相邻帧高度相关，用预测、差分、变换去相关（空间），用运动补偿去相关（时间）。
- **心理视觉冗余（Psychovisual redundancy）**：人眼对某些信息不敏感（高频细节、色度分量、人眼对比敏感度），可安全舍弃（量化/子采样）。

### 图像压缩分类

#### 按保真度

- **无损**：PNG、GIF、BMP(RLE)、JPEG-LS、WebP 无损模式、FLIF——适合医学影像、线稿、文本截图等不允许失真的场景。
- **有损**：JPEG、JPEG 2000、WebP 有损、HEIF/AVIF、H.264/H.265/AV1——适合照片、视频等对高压缩比敏感的媒体。

#### 按时间维度

- **空间编码（帧内，Intra）**：对单帧图像压缩，利用帧内像素空间相关。代表：JPEG（DCT）、JPEG 2000（小波）。
- **时间编码（帧间，Inter）**：对视频帧序列压缩，利用帧间时间相关。代表：H.264/AVC、H.265/HEVC、AV1——运动估计/补偿 + 帧内帧（I 帧）间隔插入，编码残差与运动矢量。

### 常用方法

- **变换编码**：DCT（JPEG/H.26x）或小波变换（JPEG 2000），把空间相关能量集中到低频系数。
- **量化**：对变换系数分级，舍弃心理视觉不敏感部分——有损压缩的主要失真来源。
- **熵编码**：Huffman、算术编码、范围编码、上下文自适应（CABAC）——消除编码冗余。
- **预测编码**：无损（PNG 滤波、JPEG-LS 中值预测）与有损（帧内预测/帧间运动补偿）共用。

### 压缩评测

- **压缩比**：原始数据大小 / 压缩后大小。
- **比特率**：单位时间/单位面积比特数（bpp：bit per pixel）。
- **失真质量**：全参考 PSNR/SSIM/VMAF、无参考清晰度/块效应等（见 [[image-quality-assessment]]）。
- **速度/复杂度**：编码与解码延迟、吞吐、内存/功耗——相机/移动端需在质量与实时性间权衡。

### 在相机链路中的位置

- **拍照**：ISP 输出（YUV/RGB）经 JPEG 或 HEIF 编码保存；质量参数（quality、4:2:0 子采样）直接影响文件大小与画质。
- **录像**：ISP 输出帧经视频编码器（H.264/H.265/AV1）压缩；编码器前有镜头畸变矫正、防抖等几何修正，避免把错误内容编码进去。
- **RAW 与无损**：RAW 文件常带无损压缩（如不同厂商的 RAW 无损编码）以减小存储占用。

## 参考

- Data compression：https://en.wikipedia.org/wiki/Data_compression
- Image compression：https://en.wikipedia.org/wiki/Image_compression
- 有损/无损图像格式对比：PNG/JPEG/WebP/HEIF 规范
