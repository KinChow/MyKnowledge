---
aliases:
- 深度图
- Depth Map
- 深度图与应用
- 视差图
- 深度相机
confidentiality: public
domain: multimedia
evidence:
- claim: 在 3D 计算机图形与计算机视觉中，深度图是包含场景物体表面到某视点距离信息的图像或图像通道。
  claim_id: depth-map-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-16a3dfa68192
    exact: a depth map is an image or image channel that contains information relating to the distance of the surfaces of scene objects from a viewpoint
  targets:
  - evidence_id: evidence-16a3dfa68192
    source_id: web-multimedia-depth-map-and-application
id: depth-map-and-application
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-multimedia-depth-map-and-application
status: published
tags:
- camera
- depth
- 3d
- tof
- stereo
- multimedia
title: 深度图与应用
updated_at: '2026-09-06'
---

# 深度图与应用

## 一句话结论

深度图（Depth Map）是 3D 计算机图形与计算机视觉中的**图像或图像通道**，包含场景物体表面到某一视点的距离信息；相关术语有深度缓冲（depth buffer）、Z-buffer、Z-buffering、Z-depth（"Z"约定为相机视轴方向）。深度图可通过 **ToF/结构光/双目立体/单目估计/激光雷达**等方式获得，也可由 3D 扫描仪生成或从多幅图像重建。典型可视化约定"近暗远亮"或"近焦平面暗、离焦平面远更亮"。在相机领域深度图驱动**背景虚化（人像散景）、人像分割、自动对焦辅助、AR 遮挡、3D 重建、SLAM、自动驾驶感知**等应用，与视差图（disparity）通过基线×焦距换算。

## 核心概念

- **深度图（Depth Map）**：记录场景物体表面到视点距离的图像/通道。
- **深度缓冲 / Z-buffer / Z-depth**：相关概念，Z 指相机视轴方向（相机 Z 轴），非场景绝对 Z 轴。
- **视差图（Disparity map）**：双目中左右视图同名点视差，深度 = 基线 × 焦距 / 视差。
- **获取方式**：ToF（飞行时间）、结构光（散斑/条纹）、双目立体匹配、单目深度估计（学习）、激光雷达（LiDAR）。
- **应用**：背景虚化、人像分割、自动对焦、AR/VR、SLAM、3D 重建、自动驾驶、安全监控。

## 工作机制

1. **ToF**：发射调制光/脉冲，测量光往返时间 t，深度 d = c·t/2；也有间接 ToF（相位差）。
2. **结构光**：投射已知散斑/条纹，观察其形变反推深度（如早期 iPhone/Primesense）。
3. **双目立体**：两摄像头同时成像，立体匹配求视差，深度 = f·B/d（f 焦距、B 基线、d 视差）。
4. **单目估计**：用深度学习从单张图回归深度，绝对尺度不确定。
5. **LiDAR**：激光逐点测距，生成稀疏/稠密深度点云。

## 示例或代码

```text
深度可视化约定：
  按到相机距离  ：near 暗、far 亮（近暗远亮）
  按到焦平面距离：近焦平面暗，越远越亮（前后都更亮）
双目深度公式：
  depth = (focal_length * baseline) / disparity
```

```python
import cv2
# 双目立体匹配 -> 视差图（再换算深度）
stereo = cv2.StereoSGBM_create(
    minDisparity=0, numDisparities=64, blockSize=11)
disparity = stereo.compute(imgL, imgR).astype(np.float32) / 16.0
depth = (f * b) / (disparity + 1e-6)  # f 焦距、b 基线、单位一致
```

## 常见误区

- **"深度图就是视差图"**：视差是双目同名点位移，深度是物理距离；二者通过基线×焦距换算，且深度图还可以来自 ToF/结构光等非双目方式。
- **"深度图是普通灰度照片"**：灰度是数据可视化，像素值是距离而非亮度。
- **"手机背景虚化靠光学景深"**：手机多用深度图/AI 人像分割做合成散景，不是真正的浅景深。
- **"深度图总是准确的"**：深度有噪声、遮挡、边缘不连续、低纹理区域失效，单目深度还无绝对尺度。
- **"深度图和 Z-buffer 完全一样"**：Z-buffer 是渲染流水线的深度缓冲，深度图是数据/图像，概念相关但用途不同。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| depth-map-definition | web-multimedia-depth-map-and-application | 深度图 = 含表面到视点距离信息的图像/通道 |

## 待验证项

- 各深度获取方式的具体参数（ToF 波长、双目基线、公式约定）来自公开资料，待按硬件规格复核。
- 手机人像虚化中深度图与语义分割的混合策略以各厂商实现为准。

## 关联知识

- [[isp-system]] —— 深度图是主 pipeline 之外的能力，可联动 3A。
- [[auto-focus]] —— 深度信息辅助对焦（人脸/主体距离）。
- [[prospects-of-computational-photography]] —— 计算摄影（光场/散景/3D）依赖深度。
- [[camera-competitive-product-analysis]] —— 深度相关（虚化/AR）是竞品卖点对比项。
- [[image-quality-assessment]] —— 深度质量（边缘/噪声/遮挡）评测维度。

## 详细章节

### 定义

在 3D 计算机图形与计算机视觉中，深度图是图像或图像通道，包含场景物体表面到某视点的距离信息。该术语与深度缓冲（depth buffer）、Z-buffer、Z-buffering、Z-depth 相关（可能同义/类比）。这些术语中的"Z"指相机视轴方向的约定（相机 Z 轴方向），而不是场景的绝对 Z 轴。

### 可视化

两种常用可视化：

- **按到相机距离**：近的表面更暗，更远的表面更亮。
- **按到名义焦平面距离**：离焦平面近的表面更暗，离焦平面远的表面更亮（靠近和远离视点的都更亮）。

### 获取方式

#### ToF（飞行时间）

发射调制光或光脉冲，测量光到物体表面再返回的时间，直接换算距离 d = c·t/2；间接 ToF 通过测量反射光与发射光之间的相位差求距离。代表：手机上 ToF 传感器、工业 ToF 相机。优点：实时、相对不受纹理影响；缺点：受环境光/多径/运动模糊影响。

#### 结构光

向场景投射已知图案（散斑/正弦条纹），从图案变形反推深度。代表：早期消费级 3D 传感器（Primesense/Kinect v1）。适合中近距离、弱光环境较好；室外阳光受限。

#### 双目立体

两个相机（固定基线）同时拍摄，立体匹配在左右图找同名点得到视差，depth = f·B/d。被动、成本低、可做远距离；低纹理/重复纹理区域匹配失败，遮挡区有孔洞。代表：Mobileye、双目 ADAS、手机双摄测距。

#### 单目深度估计

用深度学习从单张图像回归深度图；绝对尺度不确定，通常与语义分割/运动恢复结合。

#### LiDAR / 激光雷达

主动逐点测距，生成稀疏或稠密点云，再投影为深度图；精度高、测距远，用于自动驾驶、测绘（如 iPhone Pro LiDAR）。

### 应用

- **3A 联动**：深度辅助自动对焦（主体距离）、人脸/人像区域检测。
- **背景虚化（散景）**：按深度对背景做不同程度模糊，模拟浅景深（手机人像模式）。
- **人像/主体分割**：深度 + 语义分割抠出主体做特效。
- **AR/VR**：遮挡处理（虚拟物体被真实物体遮挡）、场景几何理解。
- **3D 重建与测量**：深度图转点云/网格，建模与测量。
- **SLAM/机器人**：相机位姿估计与环境建图。
- **自动驾驶**：障碍物测距、可行驶区域、目标检测融合。

### 深度图在相机/ISP 中的角色

深度获取常作为独立的深度相机/模组（ToF/双目/结构光）与主摄协同；深度图可与 ISP 输出的彩色图对齐（标定与配准），用于后续计算摄影与 3A 决策。深度质量（边缘精度、噪声、遮挡、时域稳定性）需要专门的评测（见 [[image-quality-assessment]]）。

## 参考

- Depth map：https://en.wikipedia.org/wiki/Depth_map
- 双目立体视觉：https://en.wikipedia.org/wiki/Computer_stereo_vision
- Time-of-flight camera：https://en.wikipedia.org/wiki/Time-of-flight_camera
