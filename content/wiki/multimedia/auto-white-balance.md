---
aliases:
- 自动白平衡
- AWB
- Auto White Balance
confidentiality: public
domain: multimedia
evidence:
- claim: |-
    In photography and image processing, color balance is the global adjustment of the intensities of the colors (typically red, green, and blue primary colors). An important goal of this adjustment is to render specific colors – particularly neutral colors like white or grey – correctly. Hence, the general method is sometimes called gray balance, neutral balance, or white balance. Color balance changes the overall mixture of colors in an image and is used for color correction.
  claim_id: auto-white-balance-audit-1
  support: direct
  supporting_quotes:
  - evidence_id: evidence-33a2fc20ca9d
    exact: |-
      In photography and image processing, color balance is the global adjustment of the intensities of the colors (typically red, green, and blue primary colors). An important goal of this adjustment is to render specific colors – particularly neutral colors like white or grey – correctly. Hence, the general method is sometimes called gray balance, neutral balance, or white balance. Color balance changes the overall mixture of colors in an image and is used for color correction.
  targets:
  - evidence_id: evidence-33a2fc20ca9d
    source_id: web-multimedia-auto-white-balance
id: auto-white-balance
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-multimedia-auto-white-balance
- working-multimedia-auto-white-balance
status: published
tags:
- camera
- isp
- white-balance
- color
- 3a
- multimedia
title: 自动白平衡（AWB）
updated_at: '2026-09-04'
---

# 自动白平衡（AWB）

## 一句话结论

自动白平衡（Auto White Balance，AWB）模拟人眼的色彩恒常性：图像传感器只记录物体反射的光谱能量，不具备人脑"无论光源色温如何都把白色认知为白色"的能力。AWB 通过调整 R/G/B 通道增益（输出 Rgain、Bgain，G 通道作参考），使灰卡在任意色温光源下都呈现 R=G=B，从而恢复物体真实颜色。核心假设是"图像像素的 R/G 与 B/G 比值能反映光源色温"；经典算法有灰度世界、完美反射、动态阈值、白点法及机器学习方法。

## 核心概念

- **色彩恒常性（Color Constancy）**：人脑能把不同色温光源下的"白色"认知为白色；AWB 目标即模拟它。
- **色温（Color Temperature）**：用开尔文（K）描述光源光谱：低色温偏暖（红黄，2700K 白炽灯），高色温偏冷（蓝，6500K 阴天）；D65（6500K）是参考白点。
- **白平衡校正**：调整 Rgain/Bgain 使灰卡 R=G=B；公式 R_out=R_in×Rgain、B_out=B_in×Bgain。
- **AWB 流程**：标定（建立色温→增益表）→ 统计（M×N 块的 R/G、B/G、白点）→ 校正（估计色温查表施加增益）。

## 工作机制

1. **标定**：产线用标准光源（D65、A 光）照射灰卡，统计各色温下 sensor 的 R/G、B/G 比值，建立"色温→增益"标定表。
2. **统计**：从当前帧（raw 域，BLC/DPC 后）选统计区域，分成 M×N 块，统计每块 R/G、B/G 均值、白点个数、亮度直方图。
3. **校正**：由统计结果估计光源色温，查标定表得 Rgain/Bgain，对整帧施加增益；校正后接色彩校正（CCM）与 gamma。

## 示例或代码

```text
白平衡公式：
  R_out = R_in × Rgain
  G_out = G_in            （G 通道作参考，不动）
  B_out = B_in × Bgain

灰度世界法：
  假设 R/G/B 三通道均值相等（场景平均反射率中性）
  若 R 均值偏高 → 降低 Rgain

完美反射法：
  假设最亮像素（高光）应为白色
  取亮度最高像素统计 R/G、B/G 作为光源估计
```

## 常见误区

- **"白平衡是调色温设置"**：AWB 是根据场景估计光源色温并补偿，不是用户手动改色温；且方向要小心——画面偏黄应提高 K（加蓝补偿）、偏蓝应降低 K（加红补偿）。
- **"灰度世界法万能"**：场景本身大面积偏色（蓝天、黄叶）时会误判，破坏真实色彩。
- **"白点检测只看亮度"**：完美反射法对无真正高光点或高噪声场景失效，需结合饱和度等做白点检测（动态阈值法）。
- **"AWB 增益可以随便跳"**：逐帧剧烈跳变会导致画面闪烁，需时间域平滑。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| auto-white-balance-audit-1 | web-multimedia-auto-white-balance | 色彩平衡/白平衡定义：全局调整 RGB 强度，使中性色正确呈现 |

## 待验证项

无。

## 关联知识

- [[overview-of-3a]] —— AWB 是相机 3A（AE/AF/AWB）之一。
- [[black-level-correction]] —— AWB 依赖黑电平扣除正确，暗部色偏与 BLC 残留相关。
- [[demosaic]] —— AWB 在去马赛克之后的 raw 域色彩链中。

## 详细章节

### 真假颜色

人眼具有色彩恒常性：无论光源色温如何变化，人脑都能把"白色"认知为白色。而图像传感器不具备这种能力——它只是记录物体反射的光谱能量，因此在不同色温光源下拍摄同一物体，得到的 RGB 值会明显不同。AWB 的目标就是模拟人眼的色彩恒常性，让图像中的白色在各种光源下都还原为白色，从而恢复物体真实的颜色。

### 色温基础

色温用开尔文（K）描述光源的光谱特性：色温越低，光源越偏暖（红黄），如日出日落约 2000-3500K、白炽灯约 2700K；色温越高，光源越偏冷（蓝），如阴天约 6500K、阴影约 7500K。标准光源 D65 约 6500K（正午日光）是图像与显示系统的参考白点。

### 白平衡基础

白平衡通过调整 R/G/B 三个通道的增益，使灰卡（中性灰）在图像中呈现为 R=G=B。其核心假设是：图像中像素的 R/G 与 B/G 比值能反映光源色温。ISP 的 AWB 模块一般输出 Rgain、Bgain 两个增益（G 通道通常作为参考通道不动），施加在 raw 数据上以纠正偏色。

白平衡校正公式：
$$
R_{out} = R_{in} \times Rgain, \quad G_{out} = G_{in}, \quad B_{out} = B_{in} \times Bgain
$$

### 白平衡基本流程

#### 标定

在产线或实验室用标准光源（D65、A 光等）照射灰卡，统计各色温下 sensor 输出的 R/G、B/G 比值，建立"色温 → 增益"的标定表（或拟合曲线），存为 AWB 参数。这是后续所有 AWB 算法的基础数据。

#### 统计

从当前帧（raw 域，一般在 BLC/DPC 之后）选取统计区域，将图像分成 M×N 块，统计每块的 R/G、B/G 均值、白点个数、亮度直方图等，作为光源估计的输入。

#### 校正

根据统计结果估计当前光源色温，查标定表得到 Rgain/Bgain，对整帧施加增益完成白平衡。校正后通常接色彩校正（CCM）与 gamma，最终还原真实色彩。

### 典型白平衡算法

#### 灰度世界法

假设场景中所有颜色的平均反射率是中性的（灰），即 R/G/B 三个通道的均值相等。取整幅图像各通道均值，若 R 均值偏高则降低 Rgain。优点：实现简单、对多彩场景效果好；缺点：当场景本身大面积偏色（如大片蓝天、黄叶）时会误判，破坏真实色彩。

#### 完美反射法

假设图像中最亮的像素（接近镜面高光）能反映光源颜色，即"最亮点应为白色"。取亮度最高的若干像素，统计其 R/G、B/G 作为光源估计。优点：对高光场景有效；缺点：当图像没有真正的高光点时失效，对噪声敏感。

#### 动态阈值法

综合灰度世界与完美反射：先做白点检测——把同时满足亮度高、饱和度低的像素判为白点候选，再对白点集合做统计估计光源。是目前手机 ISP 中较常用的方法，通过调节白点判定阈值可适应不同场景。

#### 白点法

与完美反射类似但更严格：限定一个色温范围（如 2500K-7500K）内的白点才参与统计，超出范围的低色温/高色温像素剔除，避免路灯、夕阳等极端光源干扰估计。

#### 特殊类型算法

针对特定场景的改进：如对肤色区域单独加权（肤色是用户最敏感的颜色）、对多光源场景做分区白平衡、对运动场景做时间滤波防止增益抖动。

#### 基于机器学习算法

用神经网络直接回归光源估计：输入整帧或缩略图，输出色温或 Rgain/Bgain。相比传统方法对复杂/多光源场景鲁棒性更好，但需要大量标注数据，且存在泛化风险，通常作为传统方法的补充或融合。

### 自动白平衡优化与思考

- **分区与局部 AWB**：整图单一增益在画面存在多个光源（室内暖光 + 窗外冷光）时会顾此失彼，可对图像分区估计增益并平滑过渡。
- **时间稳定性**：AWB 增益逐帧剧烈跳变会导致画面闪烁，需对增益做时间域平滑，但也要避免对真实光源切换反应过慢。
- **与曝光/噪声的耦合**：高 ISO 下噪声增大，白点检测易误判；暗区色偏严重（与黑电平扣除残留相关），需与 BLC、降噪模块联合调试。
- **先验与场景识别**：结合场景识别（夜景/逆光/多光源）选择更合适的算法分支，是当前手机 AWB 的主流工程实践。

## 参考

- 色彩恒常性（Color Constancy）：https://en.wikipedia.org/wiki/Color_constancy
- 色温与白平衡：https://en.wikipedia.org/wiki/Color_temperature / https://en.wikipedia.org/wiki/White_balance
- 灰度世界与完美反射等经典 AWB 算法综述：https://en.wikipedia.org/wiki/Color_balance
