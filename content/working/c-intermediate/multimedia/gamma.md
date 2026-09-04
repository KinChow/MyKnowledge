---
domain: multimedia
legacy_first_commit_at: '2025-07-06T20:30:14+08:00'
legacy_path: docs/computer-science/applied-computer-science/multimedia/camera/algorithm/image-processing/image-reconstruction/gamma.md
snapshot_sha256: sha256:de8d58f0618fb72b8747ee52cd348af656c59f567870a5829eb723a442bd62d5
title: gamma
---
# gamma

## 什么是Gamma

Gamma：一种数学变换。

Gamma矫正：

输入亮度与输出亮度的非线性变换，一般写作：
$$
L_{out} = L_{in}^{1/\gamma}
$$
或显示侧 $V_{out} = V_{in}^{\gamma}$（编码/解码的 gamma 互为倒数）。常见的 gamma 值：sRGB 编码约 1/2.2（解码 2.2），BT.709 编码约 0.45（解码 2.4 近似）。

## Gamma与人的视觉非线性

韦伯理论（韦伯-费希纳定律）：

即感觉的差别阈限随原来刺激量的变化而变化，而且表现为一定的规律性——人眼对亮度的感知近似对数/幂函数：暗部对亮度差异更敏感，亮部差异不易察觉。因此把更多编码比特分配给暗部（而非线性平均分配），可以在有限位深下让人眼感知的量化误差更均匀，这就是 gamma 编码的生理基础。

### Gamma与系统

存储、传输、显示图像的带宽有限。

通过Gamma矫正，将更多的存储分配给暗区，配合人眼的非线性。

Gamma的效果由Encoding及Display共同决定。

- **编码侧（Encoding）**：相机/内容侧对线性场景光做幂次压缩（如 1/2.2），把暗部细节用更多码值保存，减少暗部量化带（banding）。
- **传输/存储**：在 8bit/10bit 有限位深下，gamma 编码使暗部量化更密、亮部更疏，匹配人眼灵敏度。
- **显示侧（Display）**：显示器按解码 gamma（约 2.2）展开，恢复近似线性亮度。
- **端到端**：编码与解码 gamma 需匹配（系统 gamma 近似 1），否则画面偏亮/偏暗或对比度异常；ICC/色彩管理正是为了协调各环节 gamma 与色域。

## 参考
- Gamma 校正与人眼视觉：https://en.wikipedia.org/wiki/Gamma_correction
- 韦伯定律：https://en.wikipedia.org/wiki/Weber%E2%80%93Fechner_law
- sRGB 传输函数：https://en.wikipedia.org/wiki/SRGB
