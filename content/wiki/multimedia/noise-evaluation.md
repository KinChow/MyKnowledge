---
aliases:
- 噪声评价
- 图像噪声评价
- Noise Evaluation
- 信噪比
- SNR
confidentiality: public
domain: multimedia
evidence:
- claim: 降噪是从信号中去除噪声的过程，相关技术既用于音频，也用于图像。
  claim_id: noise-reduction-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-42fbc162a23a
    exact: Noise reduction is the process of removing noise from a signal. Noise reduction techniques exist for audio and images.
  targets:
  - evidence_id: evidence-42fbc162a23a
    source_id: wikipedia-noise-reduction-v2
id: noise-evaluation
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- wikipedia-noise-reduction-v2
- working-multimedia-noise-evaluation
status: published
tags:
- camera
- isp
- noise
- denoise
- multimedia
title: 图像噪声评价
updated_at: '2026-09-05'
---

# 图像噪声评价

## 一句话结论

图像噪声是数字图像在获取、传输、处理过程中引入的随机扰动，可沿多个维度分类（来源、频率、色彩、时态、与信号关系、概率分布）。RAW 域在噪声模型最简单（高斯-泊松近似）时降噪最有效；一旦经过 Lens shading、Gamma、demosaic、CCM 等模块，噪声会变成非线性、空间相关、彩噪饱和的结构性噪声，难以建模。噪声评价常用 SNR、MSE/PSNR、SSIM 等指标，但这些指标均与主观视觉不完全一致（SNR/PSNR 高≠图像质量好）；可视化噪声（Visual Noise）按人眼空间频率响应加权，更贴近实际感知。

## 核心概念

- **噪声**：图像中与真实信号无关/相关的随机扰动，统计学上用标准差衡量。
- **噪声分类**：按频率（高/中/低频）、色彩空间（luma/chroma）、时态（FPN/时间噪声）、与信号关系（加性/乘性）、概率密度（高斯/泊松/椒盐/瑞利/伽马/指数/均匀）。
- **RAW 降噪意义**：RAW 域噪声近似高斯-泊松模型，可按亮度分段降噪或归一化噪声，利于保护细节。
- **SNR（信噪比）**：均匀区域均值/标准差，只反映总噪声量，不反映人眼感知。
- **MSE/PSNR**：均方误差/峰值信噪比；PSNR 通常 >30dB 才算可接受，但高 PSNR 不代表主观质量好。
- **SSIM（结构相似性）**：从亮度、对比度、结构三方面度量，更贴近人眼，但仍有 PSNR 的同类问题。
- **Visual Noise（VN）**：按可见性加权噪声，模拟人眼对空间频率的响应，亮度/彩噪分开赋权。

## 工作机制

1. **噪声建模**：RAW 域中高斯噪声可看作加性（不随光强变化）、泊松噪声可看作乘性（与光强成正比），模型简单可估计（noise profile）。
2. **越晚处理越难**：Lens shading（径向乘性 gain → radial noise）→ Gamma（按亮度非线性）→ demosaic（插值成结构性噪声）→ CCM（3×3 矩阵增强相关性、放大彩噪饱和度），噪声模型逐步复杂化，RAW 降噪之后需更复杂的去噪算法。
3. **评价**：SNR 用均匀区域均值/标准差；MSE/PSNR 基于像素误差；SSIM 综合亮度/对比度/结构；VN 按人眼可见性加权。

## 示例或代码

```text
SNR  = mean(region) / std(region)          # 区域均值 / 区域标准差
MSE  = (1/(M*N)) * Σ (x(i,j) - y(i,j))^2   # 均方误差
PSNR = 10 * log10(MAX^2 / MSE)             # 峰值信噪比，>30dB 通常可接受
SSIM = 亮度项 × 对比度项 × 结构项            # 结构相似性
```

## 常见误区

- **"SNR 高图像质量就好"**：SNR 只反映总噪声量，不描述人眼感知方式；同样的 SNR 视觉表现可能不同，且过度涂抹会导致 SNR 高但质量差。
- **"PSNR 高就是好图"**：PSNR 公式未体现像素值范围（8bit 与 12bit 的相同 MSE 不可比），也不反映人眼感知，仍需人眼辅助判断。
- **"降噪越晚做越好"**：RAW 域噪声模型最简单，越往后 Gamma/demosaic/CCM 会把噪声复杂化，更难处理。
- **"SSIM 能完全替代 PSNR"**：SSIM 更贴近人眼，但仍具有 PSNR 类似的"指标高不等于主观好"问题。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| noise-reduction-definition | wikipedia-noise-reduction-v2 | 降噪是从信号中去除噪声的过程，用于音频与图像 |

## 待验证项

- 噪声分类、RAW 降噪意义、SNR/MSE/PSNR/SSIM 评价等具体内容来自内部工作笔记（working-multimedia-noise-evaluation），无公开权威来源，待人工复核。

## 关联知识

- [[time-domain-noise-reduction]] —— 时域降噪利用噪声帧间随机性。
- [[frequency-domain-noise-reduction]] —— 频域降噪。
- [[gamma]] —— Gamma 会把噪声非线性化。
- [[isp-system]] —— 降噪模块在 ISP 流水线中的位置。
- [[sensor]] —— RAW 噪声的来源（光电转换、暗电流、增益）。

## 详细章节

### 噪声的分类与特性

#### 噪声来源

- 图像获取
  - 对于数字图像传感器，一般会经历如下三个过程：
    - 光电转换
    - 电能-势能转换
    - 数模转换
- 图像信号传输
  - 数字图像在传输记录过程中会受到多种噪声的污染。另外，在图像处理的某些环节当输入的对象并不如预想时也会在结果图像中引入噪声。
- 从统计学上来说，噪声可以用标准差衡量。

ISO/灵敏度的调节可以看做调整放大器的增益，增益大的结果就是放大了信号，也放大了噪声，这也是高ISO情況下噪声明显增加的原因。

#### 噪声分类

- 频率
  - 高频：边缘和细节
  - 中频
  - 低频：大量平坦区域
- 色彩空间
  - luma noise亮度噪声
  - chroma noise彩色噪声
- 时态
  - Fix pattern noise 与时间无关，表现上看就是噪声幅度不随时间变化。
  - Temporal noise是随时间变化，在低光下录制的视频中不断变化的细小信号就是temporal noise。
  - 也有一种分法是将图像的行或者列存在一条条的噪声看作fix pattern noise。
  - 去除temporal noise的方法就是多帧平均加运动检测，temporal noise视觉上是一种高频噪声。
- 噪声和信号的关系
  - 加性噪声和图像信号强度是不相关的，如图像在传输过程中引进的"信道噪声"、电视摄像机扫描图像的噪声。这类带有噪声的图像g可看成为理想无噪声图像f与噪声n之和。
  - 乘性噪声和图像信号是相关的，往往随图像信号的变化而变化，如入射到相机的光子在硅层内被转换成光电子，由于光信号的量子特性，相机捕获到的信号存在一定的不确定性产生的散粒噪声。
- 概率密度函数
  - 高斯噪声：电子噪声，在放大器或检测器中产生
  - 泊松噪声（光子噪声）
  - 脉冲噪声（椒盐噪声）：随机改变一些像素值，由图像传感器、传输信道、解码处理等产生的黑白相间亮暗点噪声
  - 瑞利噪声：出现在雷达测距图像
  - 伽马噪声：出现在激光图像
  - 指数分布噪声
  - 均匀分布噪声

#### RAW降噪的意义

高斯噪音可以看作加性噪声，泊松噪声可以看作乘性噪声：

- 高斯噪声不随光强增大变化
- 泊松噪声与光强成正比

参考noise profile在raw domain设计降噪算法会容易一些，在不同的亮度进行不同程度的降噪，或者归一化噪声，有利于保护细节。

传统Raw域降噪模块后有多个模块会对噪音产生影响，如果不及早处理，会使噪音复杂化，更难处理：

- Lens shading correction 对噪声的影响
  - 因为lens shading correction 是在图像上乘以一个gain，远离中心的地方gain越大，因此会导致由图像中心到边缘形成沿径向增强的噪声图像，也被称作radial noise。
- Gamma 对噪声的影响
  - Gamma可以近似理解为不同的亮度值乘以的gain不一样，亮度越小的地方乘以的gain越大，亮度越大的地方乘以的gain越小，因此gamma之后的噪声又形成了一个非线性变化。
- demosaic 对噪声的影响
  - 由于demosaic对原始信号进行了插值操作，会导致图像的噪声变为结构性噪声。
- CCM 对噪声的影响
  - 无论是色彩管理还是RGB到sRGB色域空间的转换，一般情况下是一个3×3的矩阵，这一步又增强了噪声的相关性，而且还会增强视觉的彩色噪声的饱和度，使噪声的视觉效果变得更糟糕。

总结：在RAW降噪前，是高斯-泊松噪声，后面噪声模型不确定，无法建模，导致了后面需要更复杂的去噪算法。

#### 噪声的评价

##### SNR（信噪比 SIGNAL-NOISE RATIO）

- 使用图像中均匀区域的标准偏差作为噪声的度量，通过将区域的平均值除以标准偏差来计算信噪比（SNR）。方法比较简单：
  - 首先，在图像中选取一块区域（可以是整个图像，也可以是某一个均匀的图像区块）
  - 其次，计算所选区域的均值和标准差；最后，均值与标准差的比值就认为是信噪比
- SNR的缺陷
  - SNR仅反映总噪声量，但没有描述人类观察者实际感知噪声的方式。
  - 一般会出现两种问题：
    - SNR并不能代表真实的视觉噪声，有些同样的SNR，但是视觉表现出来就不同。
    - SNR好并不能代表最终图像质量好，有时会过度涂抹；SNR虽高，但是图像质量并不好。
  - 可视噪声值易于理解：值越高，观察者将看到的噪声越多。
  - SNR和Visual Noise之间的主要区别在于，VN将根据可见性对噪声进行加权，模拟人类视觉系统对空间频率的响应：看不到的噪音不会被考虑在内。因为不同频率噪声对人眼的视觉影响完全不一样，并且人眼对彩噪和亮度噪声的感觉也完全不一样，所以亮度和颜色分开计算，赋予不同的权重。

目前，用得比较多的评价方式是MSE（Mean-Squared Error，均方误差）和PSNR（Peak Signal-to-Noise Ratio，峰值信噪比）。

- MSE
  - 计算公式：$MSE = \frac{1}{MN}\sum_{i=1}^{M}\sum_{j=1}^{N}(x(i,j)-y(i,j))^2$
  - 公式里没有表现出像素值范围对结果的影响，同样的均方误差8-bit的图像和12-bit的图像显然没有可比性。
- PSNR
  - 计算公式：$PSNR = 10\log_{10}\left(\frac{MAX^2}{MSE}\right)$
  - 通常PSNR值越高表示品质越好，一般而言，当PSNR<30dB时，代表以人的肉眼看起来是不能容忍的范围。因此大部分PSNR值都要>30dB。但PSNR高，并不代表图像质量一定好，有时候还是必须要靠人的肉眼去辅助判断图像的质量才较为正确。

##### SSIM（结构相似性）

结构相似性，是一种衡量两幅图像相似度的指标。SSIM使用的两张图像中，一张为未经压缩的无失真图像，另一张为失真后的图像。也是视频质量评价的一种优秀算法。不过依然具有PSNR的问题。

## 参考

- Noise reduction：https://en.wikipedia.org/wiki/Noise_reduction
- Signal-to-noise ratio：https://en.wikipedia.org/wiki/Signal-to-noise_ratio
- Peak signal-to-noise ratio：https://en.wikipedia.org/wiki/Peak_signal-to-noise_ratio
- Structural similarity：https://en.wikipedia.org/wiki/Structural_similarity
