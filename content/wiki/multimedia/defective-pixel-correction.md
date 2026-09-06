---
aliases:
- 坏点矫正
- Defective Pixel Correction
- DPC
- 坏点
confidentiality: public
domain: multimedia
evidence:
- claim: 在数字相机中，坏点不能正确感知光照；液晶显示器中的坏点则不能正确再现光照。
  claim_id: defective-pixel-camera-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-94447c9e16dd
    exact: In these devices, defective pixels fail to sense light levels correctly, whereas defective pixels in LCDs fail to reproduce light levels correctly.
  targets:
  - evidence_id: evidence-94447c9e16dd
    source_id: wikipedia-defective-pixel-camera-v2
id: defective-pixel-correction
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- wikipedia-defective-pixel-camera-v2
- working-multimedia-defective-pixel-correction
status: published
tags:
- camera
- isp
- defective-pixel
- raw
- multimedia
title: 坏点矫正
updated_at: '2026-09-04'
---

# 坏点矫正

## 一句话结论

坏点（Defective Pixel）是图像传感器像素阵列工艺缺陷导致的异常像素，不能正确感知光照（坏点在 LCD 中则不能正确再现光照）。坏点按是否变化分**静态/动态**、按亮度分 hot/dead/stuck/blinky 等、按相邻数量分单/双/多坏点。坏点矫正（DPC）在 RAW 域实现：静态矫正用产线标定坏点表（OTP），动态矫正实时检测（Pinto/Kakarala 算法）与校正（中值滤波/梯度均值），需在插值滤波前进行，避免影响周围像素。

## 核心概念

- **坏点**：像素阵列工艺缺陷导致不能正确感知光照的像素；计量单位 ppm。
- **分类**：静态（工艺/制造产生、不随增益时间变）/动态（随增益温度变）；hot/dead/stuck/blinky/stuck-to-neighbor/phase-detection；单/双/多坏点。
- **影响**：影响插值滤波、边缘伪彩、像素闪烁——需在插值前矫正。
- **静态矫正**：产线标定坏点表写 OTP，坐标匹配后校正。
- **动态矫正**：实时检测（Pinto：中心与邻域作差；Kakarala：最大/最小/均值判定）+ 校正（中值滤波/梯度均值）。

## 工作机制

1. **检测**：坏点比周围点更亮或更暗——Pinto 算法把中心 P5 与邻域 P1~P8 作差，全正或全负判为坏点；Kakarala 用最大/最小/均值差判定。
2. **校正**：中值滤波用周围像素中值替代；梯度均值按边缘方向（水平/垂直/45°/135°）选方向均值，平坦区用全部邻域均值。
3. **静态标定**：产线标定坏点坐标写 OTP，运行时坐标匹配判定 + 校正。

## 示例或代码

```c
// Kakarala 坏点检测
bool IsDefectivePixel(P1..P9) {
    P_high = max(P1..P9);
    P_low  = min(P1..P9);
    P_avg  = (sum(P1..P9) - P5 - P_high - P_low) / 6;
    P_diff = P_high - P_low;
    if (P5 < P_avg - P_diff || P5 > P_avg + P_diff) return true;
    return false;
}
// 梯度均值校正：选最小梯度方向做均值
if 水平梯度最小: P5_out = (P4+P6)/2;      // 垂直方向像素平均
else if 垂直梯度最小: P5_out = (P2+P8)/2;
else if 135°: P5_out = (P1+P9)/2;
else if 45°:  P5_out = (P3+P7)/2;
else:         P5_out = 周围8像素平均;
```

## 常见误区

- **"坏点矫正只用静态表"**：静态坏点表成本高（每 sensor 不同、存储大），动态检测校正更灵活（实时、数量不限）。
- **"中值滤波随便用"**：坏点校正需在插值滤波前；对高噪声场景会把噪声当坏点，需按 ISO 调试。
- **"高亮孤立点也是坏点"**：LED 点阵灯、交通灯等高亮孤立点可能被误判为坏点。
- **"相位像素是坏点"**：PDAF 的相位检测像素（遮挡半边）在图像上表现为坏点，但分布规律、位置静态，需单独处理。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| defective-pixel-camera-definition | wikipedia-defective-pixel-camera-v2 | 相机坏点不能正确感知光照 |

## 待验证项

无。

## 关联知识

- [[black-level-correction]] —— 与 DPC 同属 raw 域最前端处理。
- [[demosaic]] —— 坏点矫正需在插值滤波（去马赛克）之前。
- [[android-camera-architecture]] —— raw 域处理链（BLC/DPC/去马赛克）。

## 详细章节

### 坏点的定义

图像传感器的形成光线采集点（像素点）的阵列工艺存在缺陷，光信号进行转化为电信号的过程中出现错误，会造成图像上的部分像素信息有误，导致图像中的像素值不准确，这些有缺陷的像素点称为坏点。坏点的计量单位是 ppm（parts per million），例如有 100ppm，对于一个 5 百万像素的 sensor 就有 500 个坏点。

### 坏点的成因

- **工艺缺陷**：sensor 生产时引入的缺陷（如灰尘导致某像素电路损坏）；组装过程的缺陷（模组组装、电路焊接过程的损伤）。
- **使用缺陷**：使用过程中的损伤（跌落、碰撞造成物理损坏）；使用时间过长（老化后器件变差）；使用环境（温度、湿度、光照造成器件能力波动）。

### 坏点的分类

- **根据坏点是否变化**：
  - 静态坏点：不会随着时间、增益等改变，从 sensor 制造时因为工艺等产生。亮点（亮度明显大于入射光比例，随曝光时间显著增加）；暗点（无论什么入射光下，值接近 0）。
  - 动态坏点：因为增益、温度等引起，会随时间变化而改变。
- **根据坏点的亮度**：hot pixel（比周围点亮很多）、dead pixel（值接近 0）、stuck pixel（值接近 255）、blinky pixel（随机值）、stuck to neighbor pixel（值受相邻像素通道影响）、phase detection pixel（PDAF sensor 专有）。
- **根据单通道相邻坏点数量**：单坏点（单通道只有一个坏点）、双坏点（相邻两个坏点）、多坏点（大于两个坏点）。

### 坏点的影响

- 后续进行插值和滤波处理时，会影响到周围的像素值，因此需要在插值和滤波之前对坏点进行矫正。
- 会造成图像的边缘出现伪彩色，不仅影响清晰度，还影响边缘的色彩。
- 会造成图像部分像素闪烁的现象。

### 坏点的消除

坏点矫正是在 RAW 域实现的，分为静态坏点矫正和动态坏点矫正两个独立过程。

#### 静态坏点矫正

一般在 sensor 或模组产线上进行标定，并将坏点位置写在 OTP（One Time Programmable）里面。静态坏点矫正是基于已有的静态坏点表，比较当前点的坐标是否与静态坏点表中的某个坐标一致，若一致则判定为坏点，然后再计算矫正结果对其进行矫正。

静态坏点的实用性不强：每个 sensor 的坏点都不相同，需要厂家给出每个 sensor 的静态坏点表，出于成本考虑厂家一般不会提供；一些低成本 sensor 坏点很多，用户需要保存大量坏点表，对存储空间是很大开销。

**相位像素**：部分像素遮左半边、部分遮挡右半边，用来快速聚焦。由于遮挡会造成亮度差异，在图像上表现为坏点。特点：分布很规律、位置总是静态不变、位置和 sensor 型号有关（同型号位置相同）。

#### 动态坏点矫正

动态坏点矫正可以实时检测和校正 sensor 的亮点与暗点，校正的坏点个数不受限制；相对静态坏点校正具有更大的灵活性和不确定性。分两个步骤：坏点检测与坏点校正。

**坏点检测**：坏点比周围点更亮或更暗，利用这个特点可以检测坏点。

**Pinto 算法**：将中心像素 P5 与周围像素 P1~P8 分别作差，根据结果正负判断——如果结果全为正值或负值，则该点为坏点；反之，如果结果有正有负，则视为正常像素点。

**Kakarala 算法**：用最大/最小/均值差判定（见"示例或代码"）。

**坏点校正**：
- **中值滤波**：使用周围像素点 P1~P8 的中值进行替代。
- **梯度均值**：根据边缘情况（各个方向计算梯度，选择最小值），选择进行均值滤波的像素点；如果是平坦区域，则根据周围所有像素进行均值。P 为 R、G、B 三个通道（见"示例或代码"）。

### 消除算法评价指标

- 不能损失原有图像细节
- 尽量消除所有坏点
- 不能引起 artifact

### 可能造成的问题

- **noise 的影响**：高噪声情况下可能把噪声当成坏点，所以坏点矫正调试时根据 ISO 进行调试。
- **高亮的孤立点**：例如 LED 点阵灯、交通灯等，可能被当成坏点。
- **分辨率卡等**：比较密集的条纹不能模糊。

## 参考

- https://www.qinxing.xyz/posts/506138d8/
- https://zhuanlan.zhihu.com/p/116873535
- https://bbs.huaweicloud.com/blogs/345231
- https://blog.51cto.com/u_15202985/6009981
- http://www.notedeep.com/page/18332
- Pinto V, Shaposhnik D. Dynamic identification and correction of defective pixels: U.S. Patent 8,098,304[P].2012-1-17.
- Baharav I, Kakarala R, Zhang X,et al. Bad pixel detection and correction in an image sensing device: U.S.Patent 6,737,625[P]. 2004-5-18.
