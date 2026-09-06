---
aliases:
- 图像防抖
- Image Stabilization
- OIS
- EIS
- 防抖
confidentiality: public
domain: multimedia
evidence:
- claim: 图像防抖是一组在曝光期间减少相机或其他成像设备运动导致模糊的技术。
  claim_id: image-stabilization-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-1d64ca8df123
    exact: Image stabilization (IS) is a family of techniques that reduce blurring associated with the motion of a camera or other imaging device during exposure.
  targets:
  - evidence_id: evidence-1d64ca8df123
    source_id: wikipedia-image-stabilization-v2
id: image-stabilization
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- wikipedia-image-stabilization-v2
- working-multimedia-image-stabilization
status: published
tags:
- camera
- isp
- stabilization
- ois
- eis
- multimedia
title: 图像防抖
updated_at: '2026-09-04'
---

# 图像防抖

## 一句话结论

图像防抖（Image Stabilization）是一组在曝光期间减少相机/成像设备运动导致模糊的技术。抖动会导致模糊、倾斜、果冻效应、运动模糊、视频抖动等。分**光学防抖（OIS）**（镜头/sensor 位移补偿，陀螺仪检测 + 马达/霍尔反馈）与**电子防抖（EIS）**（算法处理：果冻效应消除、运动模糊去卷积、多帧短曝光、视频帧匹配如光流/SIFT）。目标是更智能、更便携、更低成本的防抖效果。

## 核心概念

- **防抖**：减少曝光期间运动导致的模糊（Image Stabilization）。
- **OIS（光学防抖）**：镜头移动/sensor 移动/两者；陀螺仪检测 + OIS 马达（X/Y）+ 霍尔传感器反馈。
- **EIS（电子防抖）**：算法后处理——果冻效应消除、运动模糊去除、视频帧匹配。
- **果冻效应**：卷帘快门（逐行曝光）与全局快门差异导致。
- **运动模糊**：由点扩散函数（PSF）导致的图像衰退。
- **视频帧匹配**：灰度投影/块匹配/位平面/特征点/光流/SIFT。

## 工作机制

1. **检测**：陀螺仪（机械/激光/MEMS）检测运动；人眼机制类比（内耳前庭检测 → 大脑处理 → 眼球/摇头抵抗）。
2. **OIS 补偿**：OIS 控制器 + 马达（X/Y 轴）+ 霍尔传感器反馈，移动镜头或 sensor 抵消抖动。
3. **EIS 后处理**：果冻效应消除（卷帘 vs 全局快门）、运动模糊去卷积（盲目解卷积）、多帧短曝光、视频帧匹配（光流/特征点/SIFT）消除视频抖动。

## 示例或代码

```text
OIS 组件（手机）：
  OIS 陀螺仪 → OIS 控制器 → OIS 马达（X/Y 轴）+ 霍尔传感器（X/Y）

视频帧匹配法：
  灰度投影 / 块匹配 / 位平面匹配 / 特征点匹配 / 光流 / SIFT

视频帧匹配影响因素：
  LOF（缺乏特征）/ RP（重复模式）/ 低信噪比 / 运动物体 /
  透视远近 / 光照突变 / 运动模糊 / 大面积阴影
```

## 常见误区

- **"EIS 能替代 OIS"**：OIS 物理补偿（低光长曝光有效），EIS 算法后处理（裁剪/变形），两者互补。
- **"果冻效应是算法能全消的"**：果冻效应源于卷帘快门逐行曝光，只能缓解（缩短曝光/算法矫正），不能完全消除。
- **"运动模糊去卷积容易"**：盲目解卷积存在 PSF 不可预知、忽视噪声、计算时间长等问题。
- **"防抖只靠 OIS 马达"**：需要陀螺仪检测 + 马达补偿 + 霍尔传感器闭环反馈。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| image-stabilization-definition | wikipedia-image-stabilization-v2 | 防抖 = 减少曝光期间运动导致的模糊 |

## 待验证项

无。

## 关联知识

- [[time-domain-noise-reduction]] —— 视频降噪与防抖（帧间处理）相关。
- [[image-quality-assessment]] —— 稳定性（防抖 ΔX/ΔY 等）是质量评价维度。
- [[auto-exposure]] —— 曝光时间与防抖耦合（长曝光需防抖）。

## 详细章节

### 需求

- 三脚支架 / 单脚支架 / 外置器械 / 无需器械

目标：更智能、更便携、更低成本的专业防抖效果。

### 抖动导致的问题

- 模糊 / 倾斜 / 摇摆 / 头尾分离 / 眩晕感 / 果冻效应 / 运动模糊 / 视频抖动

### 图像防抖分类

- **光学防抖（OIS）**：镜头移动 / sensor 移动 / 两者一起移动。
- **电子防抖（EIS）**。
- 视频后处理过滤器 / 外置的防抖支架 / 防抖 CCD。

#### 光学防抖技术

- **人眼防抖机制**：内耳前庭（检测）→ 大脑（处理）→ 眼球转动或摇头（抵抗）。
- **外置稳像设备**：陀螺仪（检测）+ 支架物理移动（抵抗）；优点可调幅度大、无需相机支持，缺点使用不方便。
- **单反相机**：sensor 防抖（传感器位移补偿）；镜头防抖（凹片镜移动实现光路折射转变，优势"所见即所得"）。
- **手机 OIS**：OIS 陀螺仪、OIS 控制器、OIS 马达（X 轴/Y 轴）、霍尔传感器（X 轴/Y 轴）。
- **常见陀螺仪**：机械陀螺仪、激光陀螺仪、MEMS 陀螺仪。

#### 电子防抖技术

**果冻效应消除原理**：果冻效应源于卷帘快门（逐行曝光）与全局快门的对比。

**运动模糊消除原理**：运动模糊的实质是由点扩散函数所导致的图像衰退。

**盲目解卷积法**：存在的问题——PSF 函数存在不可预知性、忽视了噪声、计算时间长。

**多帧短曝光法**：用多帧短曝光合成，减少单帧运动模糊。

**视频抖动消除原理**：常见视频帧匹配法——灰度投影法、块匹配法、位平面匹配法、特征点匹配法、光流法、SIFT 匹配法。

**影响因素**：缺乏特征（LOF）、重复模式（RP）、低信噪比（Low SNR）、存在运动物体、透视角度造成同一物体远近运动量不同、光照突然变化、运动模糊、大面积阴影。

## 参考

- OIS/EIS 防抖技术综述：https://en.wikipedia.org/wiki/Image_stabilization
- 果冻效应与卷帘快门：https://en.wikipedia.org/wiki/Rolling_shutter
