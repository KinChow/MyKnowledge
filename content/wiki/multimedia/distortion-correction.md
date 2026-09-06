---
aliases:
- 畸变矫正
- Distortion Correction
- 光学畸变
- 桶形畸变
- 枕形畸变
confidentiality: public
domain: multimedia
evidence:
- claim: 几何光学中，畸变是偏离直线投影（rectilinear projection）的偏差——即场景中的直线在图像中不再保持为直线。
  claim_id: distortion-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-1614c99b9d35
    exact: In geometric optics, distortion is a deviation from rectilinear projection;
      a projection in which straight lines in a scene remain straight in an image.
  targets:
  - evidence_id: evidence-1614c99b9d35
    source_id: web-multimedia-distortion-correction
id: distortion-correction
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-multimedia-distortion-correction
status: published
tags:
- camera
- lens
- isp
- distortion
- calibration
- multimedia
title: 畸变矫正
updated_at: '2026-09-06'
---

# 畸变矫正

## 一句话结论

光学畸变（Optical Distortion）是偏离直线投影（rectilinear projection）的偏差：理想情况下场景中的直线在图像中仍为直线，畸变让直线变弯（桶形/枕形/胡须形）。它不同于球差、彗差、色差、场曲、像散——那些只影响清晰度而不改变形状结构。畸变主要由镜头折射与镜组设计引起，用**径向畸变模型（Brown-Conrady 多项式或 division model）+ 切向畸变**建模，通过**棋盘格标定**求内参/畸变系数，再经**重映射（undistort）**矫正；ISP 中畸变矫正常与暗角矫正、去马赛克等 raw 域处理协同，评测用 TV 畸变系数等客观指标。

## 核心概念

- **直线投影（Rectilinear projection）**：场景中直线在图像中仍为直线的理想投影。
- **畸变（Distortion）**：偏离直线投影的几何像差，改变物体在图像中的形状结构。
- **径向畸变**：沿半径方向的比例变化——桶形（向外鼓起）、枕形（向内收拢）、胡须形（先桶后枕的复合）。
- **切向畸变**：镜头与 sensor 不平行导致的偏心（decentering）畸变。
- **Brown-Conrady 模型**：径向偶次多项式 + 切向项，标定常用。
- **Division model**：单参数/多参数除法模型，对径向畸变更精确。
- **标定**：棋盘格角点提取 → 相机内参/畸变系数估计（如 OpenCV calibrateCamera）。
- **矫正**：由畸变系数生成映射表（LUT/remap），逐像素重采样。

## 工作机制

1. **成因**：镜头折射、镜组设计与装配误差使光线偏离理想直线投影；径向畸变源于对称镜头的对称性畸变，切向畸变源于光轴与 sensor 不垂直。
2. **建模**：畸变图像坐标 (x_d, y_d) 与理想坐标 (x_u, y_u) 满足多项式/除法关系，用标定求系数。
3. **标定**：拍摄多角度棋盘格，检测角点，最小化重投影误差求出内参矩阵 K 与畸变系数（k1,k2,p1,p2,k3 等）。
4. **矫正**：对每个输出像素，用畸变模型反查输入像素位置，经插值得到无畸变图像；ISP 常预生成 LUT 逐帧查表。

## 示例或代码

```python
import cv2
import numpy as np

# 1) 棋盘格角点检测
ret, corners = cv2.findChessboardCorners(gray, (cols, rows), None)
# 2) 多张棋盘格标定 -> 内参 mtx + 畸变系数 dist
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
# 3) 畸变矫正（直接）或生成映射表（高效）
dst = cv2.undistort(img, mtx, dist)
mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, mtx, (w, h), cv2.CV_32FC1)
dst2 = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)
```

径向畸变模型（Brown-Conrady，k 为径向系数，p 为切向系数）示意：

```text
x_u = x_d + x_d*(k1*r^2 + k2*r^4 + k3*r^6) + [2*p1*x_d*y_d + p2*(r^2 + 2*x_d^2)]
y_u = y_d + y_d*(k1*r^2 + k2*r^4 + k3*r^6) + [p1*(r^2 + 2*y_d^2) + 2*p2*x_d*y_d]
```

## 常见误区

- **"畸变只是边缘变弯"**：畸变是整幅图像的比例随半径变化（中心比例 1、边缘比例 ≠1），不只是"弯"。
- **"畸变和暗角是一回事"**：畸变是几何形状变化，暗角（vignetting）是亮度/饱和度降低，二者成因与矫正都不同。
- **"只要径向模型就够"**：镜头与 sensor 不平行还有切向（偏心）畸变，高精度场景需要完整 Brown-Conrady 模型。
- **"矫正后图像无损"**：重映射伴随插值（双线性/双三次），会引入轻微模糊或过冲，分辨率与边缘都会受影响。
- **"畸变系数是固定的"**：随焦距/对焦距离/模组批次变化，变焦镜头需多组系数（zoom-dependent calibration）。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| distortion-definition | web-multimedia-distortion-correction | 畸变 = 偏离直线投影的几何像差 |

## 待验证项

- 径向/切向畸变的具体系数与 OpenCV 接口行为来自内部工作笔记（与公开资料一致，但 Brown-Conrady 细节待人工复核）。
- 桶形/枕形/胡须形畸变的 K1 符号约定（桶形负、枕形正）来自 Wikipedia 表述，待与具体标定库确认。

## 关联知识

- [[lens-vignetting-correction]] —— 与畸变同属镜头缺陷，但一个是几何、一个是亮度。
- [[optical-fundamentals]] —— 镜头折射与成像规律是畸变成因的基础。
- [[isp-system]] —— 畸变矫正位于主 pipeline 之外（或 raw 域前端）。
- [[image-quality-assessment]] —— 畸变是均匀性/几何评测维度（TV 畸变系数）。
- [[camera-competitive-product-analysis]] —— 畸变表现是竞品成像效果评测项。

## 详细章节

### 畸变概念

在几何光学中，畸变是偏离直线投影的偏差——直线投影要求场景中的直线在图像中仍是直线。畸变是光学像差的一种，与球差、彗差、色差、场曲、像散的区别在于：后者只影响图像清晰度而不改变物体的形状结构（直线仍是直线），而畸变会改变物体在图像中的结构形状（直线变弯），因此得名"畸变"。

畸变通常不会降低图像清晰度，但会破坏几何保真度，影响测量、拼接、三维重建、AR 等对几何精度敏感的应用，也需要在成像质量评测中单独衡量。

### 产生原因

- **镜头折射与镜组设计**：光线经不同厚度/曲率的透镜折射后，边缘放大率与中心放大率不一致，产生径向畸变。
- **装配与偏心**：镜组光轴与 sensor 平面不垂直、镜片偏心，产生切向（decentering）畸变。
- **焦距/对焦距离变化**：变焦镜头在不同焦距、不同对焦距离下畸变量不同。

### 径向畸变类型

径向畸变通常按对称镜头的对称性分为三类：

- **桶形畸变（Barrel）**：图像放大率随离光轴距离增大而减小，直线在中心处向外鼓起，像木桶。通常对应负的 K1 系数。
- **枕形畸变（Pincushion）**：图像放大率随离光轴距离增大而增大，不经过图像中心的直线向中心内弯，像垫枕。通常对应正的 K1 系数。凸（正）球面透镜倾向于枕形畸变。
- **胡须形畸变（Mustache/Complex）**：桶形与枕形的混合——靠近图像中心呈桶形，向边缘逐渐过渡为枕形，画面上半部分水平线看起来像胡须。其径向几何级数非单调，K 序列在某个半径处变号。

### 数学模型

#### Brown-Conrady 模型

标定中常用的模型，径向畸变用偶次多项式，另加切向项：

$$
\begin{aligned}
x_u &= x_d + x_d(k_1 r^2 + k_2 r^4 + k_3 r^6) + [2p_1 x_d y_d + p_2(r^2 + 2x_d^2)] \\
y_u &= y_d + y_d(k_1 r^2 + k_2 r^4 + k_3 r^6) + [p_1(r^2 + 2y_d^2) + 2p_2 x_d y_d]
\end{aligned}
$$

其中 r 为归一化半径，k1/k2/k3 为径向系数，p1/p2 为切向系数。

#### Division model

对径向畸变，除法模型通常比 Brown-Conrady 偶次多项式更精确：

$$
x_u = x_c + \frac{x_d - x_c}{1 + K_1 r^2 + K_2 r^4 + \cdots}, \quad
y_u = y_c + \frac{y_d - y_c}{1 + K_1 r^2 + K_2 r^4 + \cdots}
$$

### 标定流程

1. 打印棋盘格/圆点标定板，从多个角度拍摄（覆盖视场中心与边缘）。
2. 检测角点（findChessboardCorners）并亚像素细化。
3. 用多视角对应关系估计内参矩阵与畸变系数（calibrateCamera，最小化重投影误差）。
4. 验证：用重投影误差（reprojection error）评估标定质量。

### 矫正方法

- **直接 undistort**：每帧调用 OpenCV undistort（适合低帧率/离线）。
- **预生成 LUT + remap**：initUndistortRectifyMap 生成映射表，每帧 remap（适合实时 ISP/视频）。
- **ISP 内建畸变矫正**：硬件查表 + 双线性插值，与暗角矫正、色彩矫正等协同。

### 评测

- **TV 畸变（TV Distortion）**：畸变量/像高，衡量径向畸变大小。
- **几何保真评测**：拍摄直线/网格目标，测量边缘直线度与位置误差。
- **与竞品对比**：在 [[camera-competitive-product-analysis]] 中对比不同产品的广角畸变控制。

## 参考

- Distortion (optics)：https://en.wikipedia.org/wiki/Distortion_(optics)
- OpenCV Camera Calibration：https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html
