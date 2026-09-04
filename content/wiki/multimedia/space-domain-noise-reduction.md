---
aliases:
- 空域降噪
- 空间域降噪
- Spatial Domain Noise Reduction
confidentiality: public
domain: multimedia
evidence:
- claim: 选择图像降噪算法需权衡多个因素：可用算力与时间、是否接受牺牲一些真实细节来换取更多降噪、以及噪声与图像细节的特性。
  claim_id: noise-tradeoff
  support: direct
  supporting_quotes:
  - evidence_id: evidence-04c098537dac
    exact: "There are many noise reduction algorithms in image processing. In selecting a noise reduction algorithm, one must weigh several factors: the available computer power and time available; whether sacrificing some real detail is acceptable if it allows more noise to be removed; and the characteristics of the noise and the detail in the image, to better make those decisions."
  targets:
  - evidence_id: evidence-04c098537dac
    source_id: wiki-noise-reduction
- claim: 非局部均值基于图像中所有像素的非局部平均去除噪声：像素的权重由以其为中心的小块与被去噪像素小块之间的相似度决定。
  claim_id: noise-nlm
  support: direct
  supporting_quotes:
  - evidence_id: evidence-b1196b6868bf
    exact: "Another approach for removing noise is based on non-local averaging of all the pixels in an image. In particular, the amount of weighting for a pixel is based on the degree of similarity between a small patch centered on that pixel and the small patch centered on the pixel being de-noised."
  targets:
  - evidence_id: evidence-b1196b6868bf
    source_id: wiki-noise-reduction
- claim: 中值滤波是非线性滤波，设计得当能很好地保留图像细节。
  claim_id: noise-median
  support: direct
  supporting_quotes:
  - evidence_id: evidence-1f1b599dffe7
    exact: "A median filter is an example of a nonlinear filter and, if properly designed, is very good at preserving image detail."
  targets:
  - evidence_id: evidence-1f1b599dffe7
    source_id: wiki-noise-reduction
- claim: 非局部均值算法的计算复杂度是图像像素数的二次方，直接应用非常昂贵。
  claim_id: nlm-cost
  support: direct
  supporting_quotes:
  - evidence_id: evidence-5a2113b47195
    exact: "The computational complexity of the non-local means algorithm is quadratic in the number of pixels in the image, making it particularly expensive to apply directly."
  targets:
  - evidence_id: evidence-5a2113b47195
    source_id: wiki-non-local-means
id: space-domain-noise-reduction
kind: knowledge
publication_scope: public
related: []
sources:
- wiki-non-local-means
- wiki-noise-reduction
status: published
tags:
- camera
- isp
- noise-reduction
- image-processing
- multimedia
title: 空域降噪
updated_at: '2026-09-04'
---

# 空域降噪

## 一句话结论

空域降噪（Spatial Domain Noise Reduction）是在图像像素域内，通过分析窗口内中心像素与相邻像素在灰度空间的联系来降低噪声。核心是**相似性权重**的计算：均值/高斯滤波（局部线性）简单但模糊边缘，中值滤波（局部非线性）保边但对高斯噪声弱，双边滤波/引导滤波按像素相似性保边，非局部均值（NLM）用全图相似块加权、质量高但计算量是像素数的平方。选择算法需权衡算力、细节保留与噪声特性。

## 核心概念

- **空域滤波**：在像素域内，用窗口内邻域像素计算新中心像素值；重点在中心像素与相邻像素相似性权重的计算。
- **局部线性**：均值滤波、高斯滤波。
- **局部非线性**：中值滤波、双边滤波。
- **非局部**：非局部均值（NLM），用全图（或搜索窗内）相似块加权。
- **权衡**：算力/时间、是否接受牺牲细节换降噪、噪声与细节特性。

## 工作机制

1. **选窗口**：对当前像素选择邻域窗口（如 3×3、5×5）。
2. **算权重**：按算法计算窗口内各像素的权重——局部线性按距离/高斯权重，双边按"距离+像素相似度"，NLM 按块相似度。
3. **加权求和**：以权重对新像素值做加权平均（或取中值），得到降噪输出。
4. **权衡**：窗口越大越平滑但可能丢失信号细节，需按实际噪声/信号特性选择。

## 示例或代码

中值滤波（非线性，保边）：

```text
对每个像素：
  1. 取邻域像素
  2. 按强度排序
  3. 用排序后的中值替换原像素值
```

非局部均值（权重由块相似度决定）：

```text
u(p) = (1/C(p)) · Σ_q v(q)·f(p,q)
f(p,q) = exp(-|B(q)-B(p)|² / h²)      （B 为以 p/q 为中心的小块均值）
```

## 常见误区

- **"降噪越强越好"**：强降噪会牺牲细节、使边缘模糊——需在降噪与保细节间权衡。
- **"均值滤波就够了"**：均值/高斯是低通，平滑的同时模糊边缘；对椒盐噪声效果也差。
- **"中值滤波通用"**：中值对椒盐噪声有效、保边缘，但对高斯噪声表现差，会使小目标丢失。
- **"NLM 可以直接上手机"**：NLM 复杂度是像素数的平方，需搜索窗/积分图/FFT 等加速才能在实时场景用。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| noise-tradeoff / noise-nlm / noise-median | wiki-noise-reduction | 降噪权衡 + NLM + 中值滤波 |
| nlm-cost | wiki-non-local-means | NLM 二次方复杂度 |

## 待验证项

无。

## 关联知识

- [[demosaic]] —— 降噪通常放在去马赛克前后的 raw 域处理链。

## 详细章节

### 常用空域降噪方法

- **均值滤波**：窗口内像素均值替代原值；线性、加权系数为 1。优点：简单快速；缺点：模糊边缘细节、对椒盐噪声表现差。
- **中值滤波**：窗口内排序取中值。对斑点/椒盐噪声有效、能保存边缘；窗口越大越平滑但可能抹掉有用信号；对高斯噪声差、小目标易丢失。
- **高斯滤波**：权重与距离有关（高斯核）。
- **双边滤波**：权重与距离和像素相似度都有关（基于空间分布和像素相似度），比高斯更保边缘；对高频噪声去噪效果差。
- **引导滤波**：需引导图（可为输入图自身，此时成为保边滤波）；模型假设局部线性，输出与输入大体相似但纹理部分跟随引导图。
- **非局部均值（NLM）**：使用图像中所有像素，按某种相似度加权；滤波后清晰度高、不丢细节，但原始 NLM 计算量极大。改进：搜索窗代替全图、相似度阈值、用块显著特征（纹理）代替灰度欧氏距离。

### 渐进式降噪与自适应

- **渐进式图像降噪**：多次降噪 + 多次融合，在一定噪声范围内信噪比有提升。
- **自适应降噪**：在原有算法上增加设定条件，优化降噪执行范围，更好保留有效像素。手段：方向差分找噪声像素并差异化赋权、自适应最优窗口、不同频率用不同降噪强度。

## 参考

- https://en.wikipedia.org/wiki/Noise_reduction
- https://en.wikipedia.org/wiki/Non-local_means
- Buades A, Coll B, Morel J M. A Non-Local Algorithm for Image Denoising[C]. CVPR, 2005.
- Tomasi C, Manduchi R. Bilateral Filtering for Gray and Color Images[C]. ICCV, 1998.
- He K, Sun J, Tang X. Guided Image Filtering[J]. IEEE TPAMI, 2013.
