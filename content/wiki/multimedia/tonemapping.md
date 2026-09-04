---
aliases:
- 色调映射
- Tone Mapping
- 色调映射算子
confidentiality: public
domain: multimedia
evidence:
- claim: 色调映射（Tone mapping）是把一组颜色映射到另一组，在动态范围更有限的媒介上近似显示 HDR 图像外观的技术。
  claim_id: tone-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-0682d4015b96
    exact: "Tone mapping is a technique used in image processing and computer graphics to map one set of colors to another to approximate the appearance of high-dynamic-range (HDR) images in a medium that has a more limited dynamic range."
  targets:
  - evidence_id: evidence-0682d4015b96
    source_id: wiki-tone-mapping
- claim: 局部（空间变化）色调映射算子的非线性函数参数随像素局部特征逐像素变化；比全局算子复杂，可能产生 halo（光晕）与振铃伪影，但能提供最佳性能——因为人眼主要对局部对比敏感。
  claim_id: tone-local-ops
  support: direct
  supporting_quotes:
  - evidence_id: evidence-cb52956d0035
    exact: "Local (or spatially varying) operators: the parameters of the non-linear function change in each pixel, according to features extracted from the surrounding parameters. In other words, the effect of the algorithm changes in each pixel according to the local features of the image. Those algorithms are more complicated than the global ones; they can show artifacts (e.g. halo effect and ringing); and the output can look unrealistic, but they can (if used correctly) provide the best performance, since human vision is mainly sensitive to local contrast."
  targets:
  - evidence_id: evidence-cb52956d0035
    source_id: wiki-tone-mapping
- claim: 全局色调映射的简单例子是 Reinhard 算子 Vout = Vin/(Vin+1)，其中 Vin 为原像素亮度，Vout 为映射后像素亮度。
  claim_id: tone-reinhard
  support: direct
  supporting_quotes:
  - evidence_id: evidence-5f91df4675bb
    exact: "A simple example of global tone mapping filter is Vout = Vin/(Vin+1) (Reinhard), where Vin is the luminance of the original pixel and Vout is the luminance of the filtered pixel."
  targets:
  - evidence_id: evidence-5f91df4675bb
    source_id: wiki-tone-mapping
id: tonemapping
kind: knowledge
publication_scope: public
related: []
sources:
- wiki-tone-mapping
status: published
tags:
- camera
- isp
- tone-mapping
- hdr
- multimedia
title: 色调映射（Tone Mapping）
updated_at: '2026-09-04'
---

# 色调映射（Tone Mapping）

## 一句话结论

色调映射（Tone mapping）是在动态范围更有限的媒介（屏幕/打印）上近似显示高动态范围（HDR）图像的技术：把场景辐射的大动态范围强对比压缩到可显示范围，同时尽量保留细节与颜色。算子分**全局**（所有像素同一映射函数，如 Reinhard `Vout=Vin/(Vin+1)`）与**局部**（逐像素按局部特征变化，对比保留更好但可能产生 halo/振铃伪影）两类。

## 核心概念

- **动态范围**：图像亮度最大值与最小值之比；显示设备（CRT/LCD/打印）动态范围有限，无法直接显示自然场景/HDR 全范围。
- **全局色调映射（空域不变）**：只考虑像素亮度值、不考虑位置，所有像素用同一映射函数。
- **局部色调映射（空域相关）**：针对图像不同区域做不同变换，考虑像素空间位置。
- **常见伪影**：Halo（光晕）、振铃、卡通感、饱和度降低、局部对比缺失。

## 工作机制

1. **输入**：HDR 图像（高动态范围亮度）。
2. **映射**：全局算子对整幅图用同一非线性函数压缩动态范围；局部算子逐像素（或逐区域）按局部特征/对比度调整映射。
3. **输出**：压缩到显示设备动态范围（如 8bit SDR），尽量保留细节与颜色外观。

全局算子示例（Reinhard）：

```text
Vout = Vin / (Vin + 1)     （Vin 原亮度 ∈ [0,∞)，Vout 映射到 [0,1)）
```

## 示例或代码

按算法类别：

```text
全局（空域不变）:
  - 基于 S 方程（S 曲线压缩暗/亮区，保留中间调细节）
  - 基于平均对数压缩
  - 基于直方图均衡（累积直方图 → 均衡函数 → 亮度映射）

局部（空域相关）:
  - 基于分层模型（分解 base 层 + detail 层，压缩 base、保留 detail）
  - 基于梯度域（衰减大梯度、保留小梯度）
  - 基于摄影法（分区块，过亮区块变暗、过暗区块变亮，源自遮光-曝光）
```

## 常见误区

- **"色调映射 = 亮度增强"**：色调映射是动态范围压缩，把 HDR 压到显示范围，不是简单调亮。
- **"局部算子总比全局好"**：局部算子对比保留好，但会产生 halo/振铃/卡通感，需权衡。
- **"HDR 图直接存成 JPEG 就行"**：JPEG 等 SDR 格式动态范围有限，需先色调映射。
- **"饱和度损失是不可避免的"**：饱和度降低源于 S 曲线压缩，可用分层模型（只映射亮度、保持色彩）缓解。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| tone-definition | wiki-tone-mapping | 色调映射定义 |
| tone-local-ops | wiki-tone-mapping | 局部算子 + halo/振铃 + 人眼局部对比 |
| tone-reinhard | wiki-tone-mapping | Reinhard 全局算子公式 |

## 待验证项

无。

## 关联知识

- [[hdr]] —— 色调映射处理的是 HDR 合成后的高动态范围图像。

## 详细章节

### 算法分类

- **全局色调映射算法（空域不变）**：只考虑像素亮度值、不考虑位置，所有像素用一样映射函数。常用：基于 S 方程、基于平均对数压缩、基于直方图均衡化。优点：计算量小、实现简单、效率高；缺点：在色度、明度及细节上有损失。
  - **基于 S 方程**：用 S 曲线变换压缩输入，压缩暗区与亮区动态范围，保留中间亮度细节。
  - **基于直方图均衡化**：把原始灰度直方图从集中区间变成全范围均匀分布；步骤为计算亮度累积直方图 → 得到均衡函数 → 修整 → 亮度映射。
- **局部色调映射算法（空域相关）**：针对图像不同区域做不同变换，调整某点灰度时把该点空间位置也考虑在内。常用：基于分层模型、基于梯度域、基于摄影法。
  - **基于分层模型**：图像分解为基本层（大尺度变化）与细节层（可见性信息），压缩基本层、保留细节层。
  - **基于梯度域**：在亮度梯度域上衰减大梯度、保留或适当增强小梯度，压缩动态范围并保留细节；图像更锐利，但可能压平整体对比、暗物体周围产生光晕。
  - **基于摄影法**：分区块的色调映射，过亮区块变暗、过暗区块变亮，源自摄影遮光-曝光概念。

### 问题与解法

- **饱和度降低**：基于 S 方程的映射导致饱和度降低；解决：分层模型把图像分为色彩与亮度两部分，色彩不变、只映射亮度。
- **局部对比度缺失**：分层模型导致局部对比度缺失；解决：基于双边滤波的色调映射。
- **Halo（光晕）**：暗/亮区域交界处出现颜色反差（光晕）；双边滤波会加剧；解决：基于加权最小二乘滤波器的色调映射。

## 参考

- https://en.wikipedia.org/wiki/Tone_mapping
- Reinhard E, et al. Photographic Tone Reproduction for Digital Images[C]. SIGGRAPH, 2002.
- Fattal R, et al. Gradient Domain High Dynamic Range Compression[C]. SIGGRAPH, 2002.
- Farbman Z, et al. Edge-Preserving Decompositions for Multi-Scale Tone and Detail Manipulation[C]. SIGGRAPH, 2008.
