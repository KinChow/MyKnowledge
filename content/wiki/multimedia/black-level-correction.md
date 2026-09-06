---
aliases:
- 黑电平校正
- Black Level Correction
- BLC
- 线性化
confidentiality: public
domain: multimedia
evidence:
- claim: 黑电平（Black Level / Optical Black）是图像数据中黑色数据（0）对应的图像传感器采集电平值；sensor 预留未曝光像素行以实时测量黑电平。
  claim_id: black-level-definition
  support: personal
  supporting_quotes:
  - evidence_id: evidence-8490e5fbc009
    exact: |-
      黑电平（Black Level / Optical Black）：黑电平是图像数据中黑色数据（0）对应图像传感器采集的电平值。

      一般sensor上会预留了一些完全没有曝光的像素，在上下两端都有一些未曝光的像素行，通过读取这些像素值的大小，可以实时得到黑电平。
  targets:
  - evidence_id: evidence-8490e5fbc009
    source_id: working-multimedia-black-level-correction
id: black-level-correction
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- working-multimedia-black-level-correction
status: published
tags:
- camera
- isp
- black-level
- raw
- multimedia
title: 黑电平与线性化
updated_at: '2026-09-04'
---

# 黑电平与线性化

## 一句话结论

黑电平（Black Level / Optical Black）是图像数据中黑色（0）对应的图像传感器采集电平值，源于 AD 前的固定偏移与 sensor 暗电流。sensor 预留未曝光像素行（光学黑 OB）实时测量它，ISP 在 raw 域最前端减去黑电平（Raw = SensorOutput - OpticalBlackLevel + pedestal），否则干扰信息会破坏 AWB 与后续处理。黑电平随温度/gain 漂移，扣除不当会导致暗部偏色。线性化则是把 sensor 的非线性输出在校正前转为线性，供后端乘法类算法（LSC/CCM）使用。

## 核心概念

- **黑电平（OB）**：图像数据黑色（0）对应的 sensor 采集电平；sensor 上下预留未曝光像素行实时测量。
- **成因**：固定偏移（AD 前加偏置保暗部细节）+ 暗电流（无光照也有输出，随曝光/gain/温度变化）。
- **扣除公式**：Raw = SensorOutput - OpticalBlackLevel + pedestal；在 ISP 最前端去除。
- **扣除方法**：中值 / 全局均值（常用）/ 局部均值 / 自定义；分块双线性插值。
- **线性化**：把 sensor 非线性输出转为线性（P_out = P_in + F(x,y)，分 region/section 查表插值）。

## 工作机制

1. **测量**：sensor 预留未曝光像素行（光学黑 OB），读取其值得到当前黑电平。
2. **扣除**：ISP 最前端按公式 Raw = SensorOutput - OpticalBlackLevel + pedestal 减去黑电平。
3. **线性化**：非线性 sensor 输出经校正曲线（region/section 查表 + 双线性插值）转为线性，供后端 LSC/CCM 等乘法模块使用。
4. **漂移处理**：黑电平随温度/gain 漂移，可分级（不同 gain 用不同值）或按漂移曲线校正。

## 示例或代码

```text
黑电平扣除：
  Raw = SensorOutput - OpticalBlackLevel + pedestal
  （去掉 pedestal 基底即可）

线性化：
  P_out(x, y) = P_in(x, y) + F(x, y)
  （每通道一条校正曲线；Gr/Gb 共用一条）
  步骤：分 region → 每 region 分 section（暗/亮区 section 最多）→
        查表得 section 端点校正值 → 双线性插值 → 施加
```

## 常见误区

- **"黑电平是显示黑位"**：这里指 sensor 光学黑（未曝光像素的电平），不是视频信号的黑位（那是另一种 black level）。
- **"黑电平固定不变"**：随温度、gain、位置变化；增益增大时暗电流增强，需不同 gain 减不同值。
- **"多扣一点黑电平无所谓"**：多扣会导致 AWB 暗区偏绿、破坏噪声形态；分通道扣除会致不同色温偏色不同。
- **"扣除后就不用管"**：扣除过少画面灰蒙、对比度低；过多画面暗沉、黑色偏色且白平衡无法校正。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| black-level-definition | working-multimedia-black-level-correction | 黑电平 = 图像黑色对应的 sensor 采集电平 |

## 待验证项

无。

## 关联知识

- [[auto-white-balance]] —— 黑电平扣除残留会导致 AWB 暗区偏色。
- [[basic-of-color]] —— 色彩链前端的 raw 域处理。
- [[demosaic]] —— 黑电平校正/线性化位于去马赛克前的 raw 域。

## 详细章节

### 黑电平的定义

黑电平（Black Level / Optical Black）：黑电平是图像数据中黑色数据（0）对应图像传感器采集的电平值。一般 sensor 上会预留一些完全没有曝光的像素（上下两端未曝光像素行），通过读取这些像素值的大小，可以实时得到黑电平。

### 黑电平的成因

- **固定偏移**：CCD/CMOS 传感器采集信息经转换生成 RAW 数据。以 8bit 为例有效值 0~255；AD 芯片精度可能无法转换很小电压，sensor 厂家在 AD 输入前加固定偏移量，使输出像素值在 5（非固定）~255 之间，目的是保留暗部细节（ISP 后面有 LSC、AWB、Gamma 等增益模块，亮区一点损失可接受）。
- **暗电流**：sensor 电路本身存在暗电流，无光照时也有输出电压；暗电流跟曝光时间和 gain 有关，不同位置不同。gain 增大时暗电流增强，因此很多 ISP 会在不同 gain 下减不同的黑电平值。

**温度影响**：环境温度升高，OB 偏移加大，去除 OB 需考虑温度影响（考验各家 sensor 设计/工艺/算法）；不考虑温度时 OB 波动大、RGB 分布不均会导致偏色。

### 黑电平的消除

BLC 各通道均需校正，常用方法：中值、全局均值（几乎各家常用）、局部均值、自定义。

**使用场景**：
1. 图像平面趋于平整 → 推荐全局均值
2. 图像出现明显突出山峰（峰值）→ 推荐中值
3. 某个角的值较高（电源等原因）→ 推荐局部计算

**全局均值**：sensor 预留未曝光像素行，读取像素值实时得到黑电平（sensor 厂家称 optical black level）。RAW 数据在 ISP 处理时需减去黑电平才是真正的 RAW 数据：
$$
Raw = SensorOutput - OpticalBlackLevel + pedestal
$$
- Black level correction 基本在 ISP 做，去掉 pedestal 基底即可
- optical black level：固定数值，对 RGB 各通道可一样也可不一样；可根据增益不同选不同数值
- 利用黑电平随温度和 gain 的漂移曲线，用一次函数校正（不同 sensor 漂移曲线不同，未作通用方案）

**双线性插值计算 BLC 减去的数值**：将图像分块，根据块内四个顶点的黑电平偏移值，计算块网格各点像素位置的黑电平偏移值。

**高通平台**：ISP pipeline 两个地方去 black level——
- black level correction：整体清晰度好（raw 域降噪程度少）
- ABF 后的 BLS 部分：整体噪声更好（满足 raw 域降噪算法，降噪更多）

高通思路：ABF 中前期在 black level 少扣一点基底留给 ABF，根据噪声分布做双边滤波优化暗区 RGB 分布不均、减少偏色，之后在 BLS 模块把剩余基底扣掉。

### 黑电平的影响

高倍 gain 下，画面既有亮区又有暗区时，OB 平均值可能没变但波动（方差）变大（尤其暗区，噪声影响变大）。各家 sensor 用均值扣除 OB，会导致暗部区域偏紫——因为 OB 方差加大，按均值扣除会有残余且 RGB 分量不平衡，再受白平衡（Rgain/Bgain）影响。

sensor 输出 raw 数据附加的黑电平值需在 ISP 最前端去干净，否则干扰后端各模块，尤其导致 AWB 不准、画面偏绿或偏红：
- ISP 多扣一点 OB：AWB 暗区偏绿、噪声形态被破坏
- ISP 分通道扣 OB：不同色温下偏色情况不同

**校正失效影响**：
- 彩色图像：扣除过少 → 画面灰蒙蒙、对比度低；扣除过多 → 画面暗沉、细节损失、黑色偏色且白平衡无法校正
- 黑白图像：扣除过少 → 灰蒙、对比度低；扣除过多 → 暗沉、动态范围降低、细节损失、黑色偏色

### 线性化背景

目前 sensor 输出图像大部分是非线性的，但后端很多算法模块用乘法（如镜头暗角矫正、色彩校正），所以 ISP 通路开端需将非线性转换为线性。

### 线性化定义

对传感器的非线性校正：数学模型中 sensor 输出值和光强在整个有效范围内呈线性正比关系，但物理上只有中间区域是线性的。

### 线性化方法

在原像素上加减值，每个颜色通道有一条校正曲线（Gr 和 Gb 共用一条）：
$$
P_{out}(x, y) = P_{in}(x, y) + F(x,y)
$$

**步骤**：
1. 线性化校正曲线把有效像素范围分为多个 regions
2. 每个 region 划分不同 sections；最暗区和最亮区 sensor 随光强变化曲线变化最大，划分 section 最多
3. 根据输入像素值判断当前像素在第几个 region、当前 region 第几个 section
4. 查表得到当前 section 左右端点对应的校正值
5. 用双线性插值根据当前 section 端点的校正值，计算当前像素的校正值
6. 将校正值作用到输入像素值上，得到输出像素

## 参考

- https://zhuanlan.zhihu.com/p/194206599
- https://blog.csdn.net/xiaoyouck/article/details/72824534
- https://deepinout.com/qcom-camera-tuning/qcom-camera-tuning-black-level-analysis.html
