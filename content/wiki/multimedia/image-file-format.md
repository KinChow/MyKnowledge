---
aliases:
- 图像文件格式
- Image file format
- RAW
- DNG
- Exif
confidentiality: public
domain: multimedia
evidence:
- claim: 图像文件格式是数字图像的文件格式（如 JPEG、PNG、GIF），存储的数据可压缩或未压缩；压缩分有损压缩与无损压缩。
  claim_id: image-format-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-adc91f5255c3
    exact: "An image file format is a file format for a digital image. There are many formats that can be used, such as JPEG, PNG, and GIF."
  - evidence_id: evidence-3c749bf8166a
    exact: "The data stored in an image file format may be compressed or uncompressed. If the data is compressed, it may be done so using lossy compression or lossless compression."
  targets:
  - evidence_id: evidence-adc91f5255c3
    source_id: wiki-image-file-format
  - evidence_id: evidence-3c749bf8166a
    source_id: wiki-image-file-format
- claim: 相机 RAW 文件是包含相机直出未处理数据的文件，因尚未处理而得名，含大量可能冗余的数据。
  claim_id: raw-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-c499a5131665
    exact: "A camera raw image file is a file that contains unprocessed data straight from a digital camera. Such data can later be changed into a photo, either within a digital camera itself or by usage of external tools. Raw files are so named because they are not yet processed, and contain large amounts of potentially redundant data."
  targets:
  - evidence_id: evidence-c499a5131665
    source_id: wiki-raw-image-format
- claim: RAW 文件包含传感器每个像素读出的完整动态范围（通常 12 或 14 位）数据。
  claim_id: raw-sensor-data
  support: direct
  supporting_quotes:
  - evidence_id: evidence-a67ba30f551a
    exact: "Raw files thus contain the full dynamic range (typically 12- or 14-bit) data as read out from each of the camera's image sensor pixels."
  targets:
  - evidence_id: evidence-a67ba30f551a
    source_id: wiki-raw-image-format
- claim: 相机传感器几乎都覆有滤色阵列（CFA，通常是 Bayer 滤色阵）：由 2×2 的红/绿/蓝/（第二个）绿滤镜构成的马赛克。
  claim_id: raw-cfa
  support: direct
  supporting_quotes:
  - evidence_id: evidence-e17f2ae0d40a
    exact: "The camera's sensor is almost invariably overlaid with a color filter array (CFA), usually a Bayer filter, consisting of a mosaic of a 2x2 matrix of red, green, blue and (second) green filters."
  targets:
  - evidence_id: evidence-e17f2ae0d40a
    source_id: wiki-raw-image-format
id: image-file-format
kind: knowledge
publication_scope: public
related: []
sources:
- wiki-image-file-format
- wiki-raw-image-format
status: published
tags:
- camera
- image
- format
- raw
- dng
- multimedia
title: 图像文件格式
updated_at: '2026-09-04'
---

# 图像文件格式

## 一句话结论

图像文件格式分两个层次：**像素排列格式**（内存/存储中像素的排布方式，如 RGB888/NV12/UYVY，planar 与 packed）与**图像存储格式**（容器，封装像素数据 + 压缩 + 元数据，如 JPEG/PNG/TIFF/DNG）。相机 RAW 是包含传感器直出未处理数据的格式（通常 12/14 位，几乎都基于 Bayer CFA），DNG 是 Adobe 为统一各家 RAW 推出的通用格式。Exif 是可嵌入 JPEG/TIFF 等容器的拍摄元数据。

## 核心概念

- **像素排列格式**：planar（同类像素连续排列，如 YUV 先 Y 再 U 再 V）/ packed（每单元像素排一块，如 YUVYUVYUV）；用 FOURCC 区分，有大小端之分。
- **图像存储格式（Container）**：一个盒子，可存一种或多种像素格式，可有损/无损压缩，可附 Exif 元数据。
- **RAW**：相机直出的未处理传感器数据（全动态范围 12/14 位），需 raw 转换器处理成可视图像。
- **DNG**：Adobe 的通用 RAW 格式，tag 定义在 TIFF/TIFF-EP 中。
- **Exif**：Exchangeable image file format，记录相机属性与拍摄数据的元数据，可嵌入 JPEG/TIFF。

## 工作机制

1. **采集**：传感器（覆 Bayer CFA）输出每像素单色的 12/14 位 raw 数据。
2. **存 RAW**：相机将未处理数据 + 拍摄参数（Exif）打包为 RAW（厂商私有格式或 DNG）。
3. **处理**：raw 转换器（如 libraw/dcraw）解码，经去马赛克/白平衡/色彩校正等处理。
4. **编码存储**：按目标格式（JPEG 有损、PNG 无损、TIFF 可两者）压缩编码，可嵌入 Exif。

## 示例或代码

常见像素排列（8bit）：

```text
RGB888    : RGBRGBRGB...
ARGB8888  : ARGBARGB...
AYUV      : VUYAVUYA...   (YUV4:4:4, packed)
UYVY      : UYVYUYVY...   (YUV4:2:2, packed)
NV12      : YYY...UVUV    (YUV4:2:0, U 与 V 顺序 NV12/NV21 相反)
```

常见工具：`libtiff`（解析 TIFF）、`libraw`（解码 DNG）、`ExifTool`（读写 Exif）、`FFmpeg`（图像/视频编解码转换）。

## 常见误区

- **"RAW 就是无损的"**：RAW 是"未处理"，不等于无损；部分 RAW 支持非线性量化（有损压缩可见退化小）。
- **"所有 RAW 都一样"**：各家厂商 RAW 格式不同（NEF/CR2/ARW…），无统一标准，DNG 是 Adobe 提出的通用方案。
- **"Bayer 是格式"**：Bayer 是传感器滤色阵列（2×2 的 R/G/B/G2），不是存储格式。
- **"Exif 只在 JPEG 里"**：Exif 可嵌入 JPEG/TIFF/RIFF 等，也可嵌入 RAW。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| image-format-definition | wiki-image-file-format | 文件格式定义 + 有损/无损压缩 |
| raw-definition / raw-sensor-data / raw-cfa | wiki-raw-image-format | RAW 未处理数据 + 12/14 位全动态范围 + Bayer CFA |

## 待验证项

无。

## 关联知识

- [[demosaic]] —— RAW 数据需经去马赛克才能变成全彩图像。
- [[android-camera-architecture]] —— Camera 流水线输出 raw 帧，raw 域处理与格式相关。

## 详细章节

### 像素排列格式

- **planar**：同类的像素排列在一起。比如 YUV，先排完所有 Y，再排 U，最后排 V。
- **packed**：每个单元的像素排一块。比如 YUV，按 YUVYUVYUV 顺序存储整张照片。
- 通过 FOURCC 区分（统一编码，有时加位宽）；排列格式有大小端区别。

#### 8bit 像素排列

- **RGB888 / ARGB8888**：RGBRGB... / ARGBARGB...，具体存储顺序有差异。
- **AYUV**：VUYAVUYA...，YUV4:4:4 packed，每像素 4 字节。
- **UYVY**：UYVYUYVY...，YUV4:2:2，两个小端字节（第一个 LSB=U、MSB=Y，第二个 LSB=V、MSB=Y）。
- **NV12**：YYY...UVUV，YUV4:2:0，UV 数组 LSB=U、MSB=V；NV21 的 U/V 顺序相反。

#### 10bit 像素排列

一个字节存不下，一般占 2 字节，低位补 0（使不支持 16bit 的设备直接截断成 10bit 只损失少量细节）；需关注大小端字节序。

### 图像存储格式

图像存储格式是一个容器（Container）：可存一种或几种像素格式（如 BMP 存 RGB888/RGBA8888），可有损/无损压缩（文件头定义压缩算法），可附 Exif 信息（如 JPEG/TIFF）。

- **无损压缩**：BMP、PNM（PPM/PGM/PBM）、PNG。
- **有损压缩**：JPEG、JPEG2000、GIF。
- **可有损可无损**：TIFF、DNG。

### Exif

可交换图像文件格式（Exchangeable image file format），为数码相机照片设定，记录相机属性与拍摄数据；可附加在 JPEG、TIFF、RIFF 等文件。Exif 信息以 0xFFE1 开头标记，后两字节为长度，最大 64KB。常用读取软件：ExifTool。

### RAW、TIFF、DNG

- **RAW**：包含创建可视图像必需的传感器数据（一般存 Bayer Pattern 与拍摄参数，参数以 Exif 嵌入）；RAW 格式无统一标准，各厂商自定义（3FR/DCR/KDC/IIQ/CR2/ERF/MEF/MOS/NEF/ORF/PEF/RW2/ARW/SRF/SR2），多基于 TIFF。
- **DNG**：Adobe 的通用 RAW 格式，tag 定义在 TIFF/TIFF-EP 中，DNG 标准定义数据组织方式、颜色空间转换等；手机 RAW 常以 DNG 存储。
- **TIFF 结构**：图像文件头（IFH，8 字节，指向第一个 IFD）、图像文件目录（IFD，含图像信息与指向实际图像数据的指针）、目录项；一个 TIFF/DNG 可存多个指向实际图像的指针（不同分辨率），部分 RAW 内置预览小 JPEG。

### 图像编解码工具

- **FFmpeg**：各种图像与视频编解码及转换工具。
- **libtiff**：解析 TIFF；**libraw**：解码 DNG 与后续处理。

## 参考

- https://en.wikipedia.org/wiki/Image_file_format
- https://en.wikipedia.org/wiki/Raw_image_format
- https://en.wikipedia.org/wiki/Exif
- https://en.wikipedia.org/wiki/Digital_Negative
