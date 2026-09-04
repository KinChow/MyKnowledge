---
domain: multimedia
legacy_first_commit_at: '2025-07-06T20:30:14+08:00'
legacy_path: docs/computer-science/applied-computer-science/multimedia/camera/software/opencv/OpenCV.md
snapshot_sha256: sha256:742b7bdd4712bae62e6b63b8026e61795e8684b1e3e5a38e273e78b1172750e9
title: OpenCV
---
# OpenCV

OpenCV（Open Source Computer Vision Library）是一个开源的计算机视觉与图像处理库，提供 C++/Python/Java 等多语言接口，覆盖图像处理、视频分析、特征提取、目标检测、机器学习与深度学习推理等能力。它既是科研与工程的标准工具，也是很多相机/ISP 算法的原型验证平台。

## modules

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
