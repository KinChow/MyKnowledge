---
aliases:
- Gamma
- Gamma校正
- Gamma Correction
confidentiality: public
domain: multimedia
evidence:
- claim: Gamma 矫正是对输入亮度与输出亮度做非线性变换的数学变换。
  claim_id: gamma-definition
  support: personal
  supporting_quotes:
  - evidence_id: evidence-568bb0bf2131
    exact: 输入亮度与输出亮度的非线性变换
  targets:
  - evidence_id: evidence-568bb0bf2131
    source_id: working-multimedia-gamma
id: gamma
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- working-multimedia-gamma
status: published
tags:
- camera
- isp
- gamma
- color
- multimedia
title: Gamma 校正
updated_at: '2026-09-04'
---

# Gamma 校正

## 一句话结论

Gamma 是对输入亮度与输出亮度做非线性变换的数学变换（Gamma 矫正）：编码侧 L_out = L_in^(1/γ)，显示侧 V_out = V_in^γ（互为倒数）。其生理基础是韦伯-费希纳定律——人眼对亮度感知近似对数/幂函数，暗部对差异更敏感；因此在有限带宽/位深下把更多编码比特分配给暗区，让人眼感知的量化误差更均匀。Gamma 效果由 Encoding 与 Display 共同决定（sRGB 编码约 1/2.2，BT.709 编码约 0.45），端到端 gamma 需匹配否则画面偏亮/偏暗。

## 核心概念

- **Gamma 变换**：输入/输出亮度的非线性变换；编码 L_out = L_in^(1/γ)、显示 V_out = V_in^γ。
- **韦伯-费希纳定律**：人眼感知差别阈限随刺激量变化，暗部对差异更敏感——gamma 编码的生理基础。
- **编码侧（Encoding）**：对线性场景光做幂次压缩（1/2.2），暗部用更多码值，减少量化带（banding）。
- **显示侧（Display）**：按解码 gamma（约 2.2）展开，恢复近似线性亮度。
- **端到端**：编码/解码 gamma 需匹配（系统 gamma 近似 1），ICC/色彩管理协调各环节 gamma 与色域。

## 工作机制

1. **编码**：相机/内容侧对线性光做幂次压缩（如 sRGB 1/2.2），把更多存储/码值分配给暗部。
2. **传输/存储**：8bit/10bit 有限位深下，gamma 编码使暗部量化更密、亮部更疏，匹配人眼灵敏度。
3. **显示**：显示器按解码 gamma（约 2.2）展开，恢复近似线性亮度；端到端 gamma 匹配则系统 gamma ≈ 1。

## 示例或代码

```text
Gamma 变换：
  编码侧：L_out = L_in^(1/γ)     （如 sRGB 1/2.2）
  显示侧：V_out = V_in^γ          （如 2.2）

常见值：
  sRGB：编码 1/2.2，解码 2.2
  BT.709：编码约 0.45，解码 2.4 近似
```

## 常见误区

- **"gamma 只是亮度调节"**：gamma 是把编码比特分配给暗部（匹配人眼非线性），不是简单调亮/调暗。
- **"编码 gamma 和显示 gamma 一样就行"**：它们是倒数关系（编码 1/γ、解码 γ），端到端需匹配（系统 gamma≈1），否则偏亮/偏暗或对比度异常。
- **"8bit 线性编码够用"**：线性编码暗部量化粗糙会出现 banding；gamma 编码让暗部量化更密。
- **"gamma 只影响显示"**：gamma 效果由编码与显示共同决定，涉及相机/内容/传输/显示全链。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| gamma-definition | working-multimedia-gamma | Gamma 是亮度非线性变换 |

## 待验证项

无。

## 关联知识

- [[basic-of-color]] —— sRGB/BT.709 的 gamma 是色彩空间的一部分。
- [[hdr]] —— HDR 显示与 SDR gamma 曲线的差异。
- [[tonemapping]] —— 色调映射与 gamma 同属亮度/动态范围处理。

## 详细章节

### 什么是Gamma

Gamma：一种数学变换。Gamma 矫正：输入亮度与输出亮度的非线性变换，一般写作：
$$
L_{out} = L_{in}^{1/\gamma}
$$
或显示侧 $V_{out} = V_{in}^{\gamma}$（编码/解码的 gamma 互为倒数）。常见的 gamma 值：sRGB 编码约 1/2.2（解码 2.2），BT.709 编码约 0.45（解码 2.4 近似）。

### Gamma与人的视觉非线性

韦伯理论（韦伯-费希纳定律）：感觉的差别阈限随原来刺激量的变化而变化，而且表现为一定的规律性——人眼对亮度的感知近似对数/幂函数：暗部对亮度差异更敏感，亮部差异不易察觉。因此把更多编码比特分配给暗部（而非线性平均分配），可以在有限位深下让人眼感知的量化误差更均匀，这就是 gamma 编码的生理基础。

#### Gamma与系统

存储、传输、显示图像的带宽有限。通过 Gamma 矫正，将更多的存储分配给暗区，配合人眼的非线性。Gamma 的效果由 Encoding 及 Display 共同决定。

- **编码侧（Encoding）**：相机/内容侧对线性场景光做幂次压缩（如 1/2.2），把暗部细节用更多码值保存，减少暗部量化带（banding）。
- **传输/存储**：在 8bit/10bit 有限位深下，gamma 编码使暗部量化更密、亮部更疏，匹配人眼灵敏度。
- **显示侧（Display）**：显示器按解码 gamma（约 2.2）展开，恢复近似线性亮度。
- **端到端**：编码与解码 gamma 需匹配（系统 gamma 近似 1），否则画面偏亮/偏暗或对比度异常；ICC/色彩管理正是为了协调各环节 gamma 与色域。

## 参考

- Gamma 校正与人眼视觉：https://en.wikipedia.org/wiki/Gamma_correction
- 韦伯定律：https://en.wikipedia.org/wiki/Weber%E2%80%93Fechner_law
- sRGB 传输函数：https://en.wikipedia.org/wiki/SRGB
