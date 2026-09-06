---
aliases:
- OpenCV
- Open Source Computer Vision Library
- 计算机视觉库
confidentiality: public
domain: multimedia
evidence:
- claim: OpenCV（Open Source Computer Vision Library）是一个开源的计算机视觉与机器学习软件库，包含超过 2500 个优化算法，涵盖经典与前沿的计算机视觉和机器学习方法。
  claim_id: opencv-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-7e6069f3047b
    exact: |-
      OpenCV documentation#
      OpenCV (Open Source Computer Vision Library) is an open-source computer vision and machine learning software library. It has more than 2,500 optimised algorithms, a comprehensive mix of both classic and state-of-the-art computer vision and machine learning methods.
  targets:
  - evidence_id: evidence-7e6069f3047b
    source_id: web-multimedia-opencv
id: opencv
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-multimedia-opencv
- working-multimedia-opencv
status: published
tags:
- opencv
- computer-vision
- library
- image
- multimedia
title: OpenCV
updated_at: '2026-09-05'
---

# OpenCV

## 一句话结论

OpenCV（Open Source Computer Vision Library）是一个开源的计算机视觉与机器学习软件库，提供 C++/Python/Java 等多语言接口，包含超过 2500 个优化算法，覆盖图像处理、视频分析、特征提取、目标检测、机器学习与深度学习推理等能力。它既是科研与工程的标准工具，也是很多相机/ISP 算法的原型验证平台。功能按模块组织：核心数据结构（core）、图像处理（imgproc）、编解码（imgcodecs）、视频 I/O（videoio）、GUI（highgui）、视频分析（video）、标定与三维重建（calib3d）、特征（feature2d）、检测（objdetect）、深度学习（dnn）等。

## 核心概念

- **OpenCV**：开源计算机视觉与机器学习库，2500+ 优化算法，多语言接口。
- **core**：核心数据结构（Mat/Point/Rect/Scalar）、内存与并行（TBB/OpenCL/CUDA）。
- **imgproc**：图像处理主力——滤波、形态学、几何变换、直方图、边缘检测、阈值、颜色空间转换、轮廓分析。
- **imgcodecs / videoio**：图像与视频的编解码、读写（imread/imwrite、VideoCapture/VideoWriter）。
- **highgui**：高层 GUI——窗口显示、鼠标/键盘事件、滑块，见 [[highgui]]。
- **feature2d / objdetect / dnn / ml**：特征检测、目标检测、深度学习推理、经典机器学习。

## 工作机制

1. **数据表示**：图像以 Mat 数据结构承载（多通道、多种位深），所有模块围绕 Mat 运算。
2. **模块分工**：读入（imgcodecs/videoio）→ 处理（imgproc/feature2d/dnn 等）→ 显示/输出（highgui/imgcodecs）。
3. **加速**：核心运算支持 TBB/OpenCL/CUDA 并行与异构调度；gapi 可把运算组织成有向图做流水线优化。
4. **部署形态**：既可编译为 C++ 库，也可通过 Python/Java 绑定快速原型验证。

## 示例或代码

```python
import cv2

img = cv2.imread("photo.png")          # 读图（BGR）
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 颜色空间转换（imgproc）
edges = cv2.Canny(gray, 50, 150)       # 边缘检测（imgproc）
cv2.imshow("edges", edges)             # 显示（highgui）
cv2.waitKey(0)

cap = cv2.VideoCapture(0)              # 打开相机（videoio）
```

## 常见误区

- **"OpenCV 只能做图像处理"**：它同时覆盖视频分析、特征、标定、机器学习、深度学习推理等。
- **"所有功能都在一个库里"**：功能按模块划分，导入/链接时按需使用（如 dnn 才加载深度学习）。
- **"OpenCV 只能 C++"**：提供 C++/Python/Java 等多语言绑定，适合快速原型验证。
- **"OpenCV 会做自动颜色空间转换"**：默认约定（如 imread 返回 BGR）与常规 RGB 不同，转换需显式调用 cvtColor。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| opencv-definition | web-multimedia-opencv | OpenCV 是开源计算机视觉与机器学习库，2500+ 算法 |

## 待验证项

- 各模块功能与默认颜色空间约定（BGR 等）来自内部工作笔记（working-multimedia-opencv）与官方文档，具体接口行为以官方文档为准。

## 关联知识

- [[highgui]] —— OpenCV 高层 GUI 与媒体 I/O 模块。
- [[image-scaling]] —— 常见图像处理算子可用 OpenCV imgproc 实现。
- [[isp-system]] —— OpenCV 常作为相机/ISP 算法的原型验证平台。

## 详细章节

OpenCV（Open Source Computer Vision Library）是一个开源的计算机视觉与图像处理库，提供 C++/Python/Java 等多语言接口，覆盖图像处理、视频分析、特征提取、目标检测、机器学习与深度学习推理等能力。它既是科研与工程的标准工具，也是很多相机/ISP 算法的原型验证平台。

#### modules

OpenCV 按功能划分为多个模块（module）：

- **core**：核心数据结构（Mat、Point、Rect、Scalar）、基本运算、内存与并行（TBB/OpenCL/CUDA）。
- **imgproc**：图像处理主力模块——滤波（高斯/双边/中值）、形态学、几何变换（缩放/旋转/仿射）、直方图、边缘检测（Canny/Sobel）、阈值、颜色空间转换（cvtColor）、轮廓分析等。
- **imgcodecs**：图像编解码（imread/imwrite），支持 PNG/JPEG/BMP/WebP 等格式。
- **videoio**：视频与相机输入输出（VideoCapture/VideoWriter），统一摄像头/视频文件/流媒体。
- **highgui**：高层 GUI——窗口显示、鼠标/键盘事件、滑块，见 [[highgui]]。
- **video**：视频分析与运动分析——光流、背景减除、跟踪（KLT/Tracker）、帧差。
- **calib3d**：相机标定与三维重建——棋盘格标定、相机内参/畸变、PnP、对极几何、立体匹配。
- **feature2d**：特征点检测与描述——SIFT、SURF、ORB、AKAZE、特征匹配。
- **objdetect**：目标检测——Haar 级联人脸检测、HOG 行人检测、QR 码/ArUco 检测（较新的 YOLO 类通常走 dnn）。
- **dnn**：深度学习推理——加载 Caffe/TensorFlow/PyTorch/ONNX 模型，在 OpenCV 内做前向推理。
- **ml**：经典机器学习——SVM、决策树、随机森林、KNN、EM 等。
- **flann**：高维最近邻快速搜索库（特征匹配加速）。
- **photo**：计算摄影——去噪（fastNlMeansDenoising）、HDR 合成与色调映射、修复（inpaint）、无缝拼接（seamlessClone）。
- **stitching**：图像拼接——多图配准、融合，生成全景图。
- **gapi**：Graph API——把 OpenCV 运算组织成有向图并做流水线/异构（CPU/GPU）调度优化。

## 参考

- OpenCV 官方文档：https://docs.opencv.org/
- 模块索引：https://docs.opencv.org/4.x/
