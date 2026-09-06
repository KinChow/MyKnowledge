---
aliases:
- JPEG
- JPEG 压缩
- 联合图像专家组
- ISO/IEC 10918
confidentiality: public
domain: multimedia
evidence:
- claim: JPEG 是数字图像、尤其是数码摄影图像常用的有损压缩方法。
  claim_id: jpeg-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-2dd7ed235a1a
    exact: JPEG is a commonly used method of lossy compression for digital images,
      particularly for those images produced by digital photography
  targets:
  - evidence_id: evidence-2dd7ed235a1a
    source_id: web-multimedia-jpeg
id: jpeg
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-multimedia-jpeg
status: published
tags:
- camera
- isp
- compression
- jpeg
- codec
- multimedia
title: JPEG 压缩
updated_at: '2026-09-06'
---

# JPEG 压缩

## 一句话结论

JPEG（Joint Photographic Experts Group，联合图像专家组，标准 ISO/IEC 10918 / ITU-T T.81）是数字图像、尤其是数码摄影图像**最常用的有损压缩方法**；压缩程度可调，在存储大小与图像质量之间选择权衡，典型 10:1 压缩仍被认为可接受。自 1992 年发布以来是全球使用最广的图像压缩标准。**基线 JPEG（baseline DCT）**流程：RGB → YCbCr 色彩空间变换 → 色度子采样（如 4:2:0）→ 8×8 分块 → DCT → 按量化表量化 → Huffman 熵编码；解码为逆过程。文件用 SOI/SOF0/DQT/DHT/EOI 等 marker 组织，JFIF/EXIF 在 APPn 中携带元数据。

## 核心概念

- **JPEG**：联合图像专家组制定，ISO/IEC 10918、ITU-T T.81（基线 DCT）/T.83/T.84/T.86。
- **有损压缩**：以人眼可接受的质量损失换取高压缩比；压缩程度由质量参数调节。
- **基线 DCT**：最常用的 JPEG 编码（SOF0），顺序式扫描。
- **YCbCr**：亮度 + 两个色度分量的色彩空间，便于色度子采样。
- **色度子采样**：对 Cb/Cr 降采样（4:4:4 / 4:2:2 / 4:2:0），利用人眼对色度不敏感。
- **8×8 分块 + DCT**：把每个块变换到频域，能量集中到低频。
- **量化表（DQT）**：按频率加权步长量化 DCT 系数——主要失真来源。
- **Huffman 熵编码（DHT）**：对量化系数做可变长编码。
- **Marker**：SOI/SOF0/DQT/DHT/EOI/APPn(EXIF) 等文件结构标记。

## 工作机制

1. **色彩空间变换**：RGB → YCbCr（亮度与色度分离）。
2. **子采样**：按 4:4:4 / 4:2:2 / 4:2:0 对色度分量降采样。
3. **分块**：每个分量切为 8×8 块。
4. **DCT**：对每块做离散余弦变换，得到 64 个频域系数。
5. **量化**：用量化表（quality 越高步长越小）量化系数，舍去心理视觉不敏感的高频。
6. **熵编码**：之字形扫描 + 游程/差分 + Huffman 编码（可含算术编码）。
7. **解码**：熵解码 → 反量化 → 逆 DCT → 上采样 → YCbCr→RGB。

## 示例或代码

```python
import cv2
# OpenCV 写 JPEG：quality 0~100，越高量化步长越小、画质越好
cv2.imwrite("photo.jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 95])
# 读取并打印 EXIF 方向等（APP1/APPn）
img = cv2.imread("photo.jpg", cv2.IMREAD_COLOR)
```

```text
JPEG 文件结构（部分 marker）：
SOI  (0xFFD8) Start Of Image
SOF0 (0xFFC0) Start Of Frame（baseline DCT，含尺寸/分量/子采样如 4:2:0）
DHT  (0xFFC4) Define Huffman Table
DQT  (0xFFDB) Define Quantization Table
APPn (0xFFEn) 应用数据（EXIF 用 APP1，结构基于 TIFF）
EOI  (0xFFD9) End Of Image
```

## 常见误区

- **"JPEG 是无损的"**：JPEG 本身是有损压缩（存在 JPEG-LS 等无损变体，但不是通用 JPEG）。
- **"质量因子就是压缩比"**：质量因子决定量化表步长，压缩比由内容与质量共同决定。
- **"JPEG 适合所有图像"**：文字、线条图、图形 UI 用 JPEG 会有振铃/块效应，PNG/WebP 更合适；照片才是 JPEG 的主场。
- **"重复保存 JPEG 无损失"**：每次有损重编码都会累积失真（generation loss），应避免反复编辑保存。
- **"JPEG 和 JPEG 2000 是同一标准"**：JPEG 2000（小波、无损可选）是后继但未广泛取代 JPEG。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| jpeg-definition | web-multimedia-jpeg | JPEG = 数码图像最常用的有损压缩，压缩可调、质量/大小权衡 |

## 待验证项

- 具体 marker 字节与量化表数值来自公开资料（Wikipedia/规范），待按 ISO/IEC 10918 复核。
- 不同平台 JPEG 质量因子到量化表的映射存在差异（OpenCV/Android/硬件编码器），以具体实现为准。

## 关联知识

- [[image-compression]] —— JPEG 是图像压缩的具体实例（空间、有损）。
- [[image-file-format]] —— JPEG 的容器格式（JFIF/EXIF/文件扩展名）。
- [[image-quality-assessment]] —— JPEG 伪影与质量评测（块效应/振铃/PSNR/SSIM）。
- [[isp-system]] —— JPEG 编码位于 ISP pipeline 之外（拍照编码环节）。
- [[basic-of-color]] —— YCbCr 色彩空间与子采样涉及的颜色知识。

## 详细章节

### 标准与历史

JPEG 由联合图像专家组（Joint Photographic Experts Group）制定，常指 JPEG 1 标准族：ISO/IEC 10918 与 ITU-T T.81（基线 DCT）/T.83/T.84/T.86。1992 年 9 月发布。自发布以来是全球使用最广的图像压缩标准与数字图像格式，每天产生数十亿张 JPEG 图像。后继/扩展包括 JPEG 2000（小波）、JPEG-LS（无损）、JPEG XT、HEIF/AVIF（现代替代）。

### 典型使用

JPEG 广泛用于数码相机、手机拍照、Web 图片、社交网络分享等对压缩比敏感、对轻微失真可接受的场景。压缩程度可调，允许在存储大小与图像质量之间选择权衡；JPEG 典型达到 10:1 压缩，质量损失虽可感知但被广泛认为可接受。

### JPEG 压缩流程

#### 编码

1. **色彩空间变换（Color space transformation）**：RGB → YCbCr，把亮度与色度分离。
2. **降采样（Downsampling）**：按子采样格式（4:4:4/4:2:2/4:2:0）对 Cb/Cr 分量降采样。
3. **分块（Block splitting）**：每个分量切为 8×8 的块。
4. **离散余弦变换（DCT）**：每块变换为 64 个频域系数，能量集中在低频。
5. **量化（Quantization）**：用量化表对系数做有损量化；质量越高步长越小。
6. **熵编码（Entropy coding）**：之字形扫描、游程编码与差分编码后做 Huffman（或算术）编码。

#### 解码

熵解码 → 反量化 → 逆 DCT → 色度上采样 → YCbCr → RGB，重建图像。基线 JPEG 支持 8 位精度。

### 文件结构

JPEG 文件由分段（segment）与 marker 组成：SOI 开始、SOF0 帧信息（尺寸/分量/子采样）、DQT 量化表、DHT Huffman 表、DRI/RSTn 重启、APPn 应用数据（如 EXIF 用 APP1，结构基于 TIFF）、COM 注释、EOI 结束。扩展名 .jpg/.jpeg/.jpe/.jfif 等，MIME image/jpeg，魔数 0xFF 0xD8。

### 压缩质量与伪影

- **块效应（Blocking）**：8×8 块边界可见方块，低质量时明显。
- **振铃（Ringing）**：高频锐利边缘附近出现波纹（Gibbs 现象）。
- **色度失真**：子采样导致彩色边缘渗色。
- **质量权衡**：quality 越高伪影越少、文件越大；评测用 PSNR/SSIM/VMAF（见 [[image-quality-assessment]]）。

### 在相机链路中的角色

拍照流程中 ISP 输出 YUV 经 JPEG 编码器保存（OpenCV/Android/硬件编解码器都支持质量参数）；相机还常写入 EXIF（APP1）元数据（拍摄参数、方向、缩略图）。录像则使用视频编码（H.264/H.265），JPEG 用于单帧照片与缩略图。

## 参考

- JPEG：https://en.wikipedia.org/wiki/JPEG
- ISO/IEC 10918-1 / ITU-T T.81（基线 DCT 规范）
