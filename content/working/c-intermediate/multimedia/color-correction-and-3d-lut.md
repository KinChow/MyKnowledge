---
domain: multimedia
legacy_first_commit_at: '2025-07-06T20:30:14+08:00'
legacy_path: docs/computer-science/applied-computer-science/multimedia/camera/algorithm/image-processing/color-reconstruction/color-correction-and-3d-lut.md
snapshot_sha256: sha256:6dda8274d2d6f61d16cf1725e71dcbef13efe47bb9bc33e09077ac065a15453c
title: 色彩矫正与3D LUT
---
# 色彩矫正与3D LUT

## 背景与实质

图像传感器的光谱响应与标准人眼（CIE 色彩匹配函数）并不一致，且镜头、滤光片会引入光谱选择性衰减，导致相机拍出的颜色偏离场景真实颜色。色彩校正（Color Correction）的实质是用一个颜色变换矩阵把"传感器响应空间"映射到"标准 RGB 空间"，补偿传感器与人眼/标准空间的差异，使颜色在统计意义上准确。它解决的是"相机看到的不等于人眼看到的"这一根本问题，是相机 ISP 色彩链路中承上（AWB 之后）启下（色域映射/gamma 之前）的关键模块。

## 颜色矫正的主要方法：CCM

颜色校正矩阵（Color Correction Matrix，CCM）是一个 3×3 矩阵，作用在每个像素的 RGB 向量上：

$$
\begin{bmatrix} R' \\ G' \\ B' \end{bmatrix}
=
\begin{bmatrix}
m_{00} & m_{01} & m_{02} \\
m_{10} & m_{11} & m_{12} \\
m_{20} & m_{21} & m_{22}
\end{bmatrix}
\begin{bmatrix} R \\ G \\ B \end{bmatrix}
$$

要点：

- **标定**：拍摄标准色卡（如 Macbeth ColorChecker，24 色），用标准光源（D65、A 光等）照射，记录各色块实测 RGB 与标准 RGB，用最小二乘拟合得到 CCM。
- **按光源分组**：不同色温下传感器响应差异大，通常按 AWB 估计的色温区间准备多组 CCM，插值使用（色温越高，矩阵偏冷）。
- **对角线主导**：CCM 对角元素接近 1 保证基本色调，非对角元素负责通道串扰校正；矩阵行和需保持灰平衡（灰输入 → 灰输出）。
- **权衡**：追求色准（接近参考）可能损失饱和度或引入噪声放大；弱光下常采用"去饱和 CCM"抑制色噪。CCM 本质是全局线性变换，无法表达复杂的、非线性的颜色风格，这是 3D LUT 的用武之地。

## 颜色矫正的补充和风格化：3D LUT

3D LUT（三维查找表）把 RGB 输入空间采样成三维网格（如 17³、33³、65³ 个节点），每个节点存一个输出 RGB 值，输入像素通过三线性插值从相邻节点得到输出。相比 CCM：

- **非线性表达**：3D LUT 可表达任意非线性颜色映射（曲线、色相偏移、分区调色），CCM 只能做线性变换。
- **风格化**：电影风格（LUT 调色）、肤色美化、特定场景色彩增强（食物/风景）都通过 3D LUT 实现。
- **色域映射**：把广色域（如 Display P3/Adobe RGB）映射到 sRGB 时，3D LUT 可同时做压缩与色调映射。
- **工程实践**：ISP 通常 CCM 负责"准"（校正到标准空间），3D LUT 负责"美"（风格化），两者串联；LUT 网格越大精度越高但存储/带宽越大，需在精度与成本间权衡。

## 参考

- 色彩校正矩阵与相机标定：https://en.wikipedia.org/wiki/Color_mapping / https://en.wikipedia.org/wiki/ICC_profile
- 3D LUT 与色彩分级：https://en.wikipedia.org/wiki/3D_lookup_table / https://en.wikipedia.org/wiki/Color_grading
- Macbeth ColorChecker：https://en.wikipedia.org/wiki/ColorChecker
