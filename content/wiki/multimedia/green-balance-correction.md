---
aliases:
- 绿平衡校正
- Green Balance Correction
- Gr/Gb 平衡
confidentiality: public
domain: multimedia
evidence:
- claim: |-
    The filter pattern is half green, one quarter red and one quarter blue, hence is also called BGGR, RGBG, GRBG, or RGGB.
  claim_id: green-balance-correction-audit-1
  support: direct
  supporting_quotes:
  - evidence_id: evidence-429e23e81582
    exact: |-
      The filter pattern is half green, one quarter red and one quarter blue, hence is also called BGGR, RGBG, GRBG, or RGGB.
  targets:
  - evidence_id: evidence-429e23e81582
    source_id: wiki-bayer-filter
id: green-balance-correction
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- wiki-bayer-filter
- working-multimedia-green-balance-correction
status: published
tags:
- camera
- isp
- green-balance
- bayer
- multimedia
title: 绿平衡校正
updated_at: '2026-09-04'
---

# 绿平衡校正

## 一句话结论

Bayer 阵列中绿色像素分为 Gr（红行）与 Gb（蓝行），因半导体制造工艺限制与微透镜差异，Gr 与 Gb 的 gain 不一致（Bayer 阵半绿、四分之一红、四分之一蓝）。偏差导致平坦区经去马赛克后出现规律的亮暗相间纹理——**迷宫格（Maze pattern）**，并使中性灰偏色、影响 AWB/CCM。绿平衡校正（GBC）通过对 G 通道做增益调整（静态 OTP 标定或动态统计 Gr/Gb 差值）消除偏差；需权衡增益强度与噪声/细节。

## 核心概念

- **Gr/Gb**：Bayer 阵列中红行的绿色像素（Gr）与蓝行的绿色像素（Gb）。
- **成因**：半导体制造工艺限制（微透镜/光刻差异）+ 微透镜偏移/形状差异 → Gr/Gb 进光量不同。
- **迷宫格（Maze pattern）**：Gr/Gb 增益不一致时，平坦区去马赛克后出现亮暗相间棋盘纹理。
- **静态校正**：产线标定 Gr/Gb 增益差写 OTP，补偿固定工艺偏差。
- **动态校正**：统计平坦区 Gr/Gb 均值差值，超阈值（可动态）时校正 G 分量。

## 工作机制

1. **统计**：在平坦区域分别计算 Gr 与 Gb 平均值。
2. **比较**：取 Gr/Gb 平均值的差值 diff。
3. **判定**：diff 与阈值（可随亮度/ISO 动态）比较——False 无需校正，True 校正 G 分量。
4. **权衡**：校正强度过大放大噪声/损失细节；不同亮度/ISO 下 Gr/Gb 偏差不同需分档。

## 示例或代码

```text
动态绿平衡校正：
  1. 计算 Gr 平均值、Gb 平均值
  2. diff = Gr均值 - Gb均值
  3. if diff < 阈值:  无需校正
     else:            校正 G 分量（按 diff 调整增益）
  （阈值可随亮度/ISO 动态变化）
```

## 常见误区

- **"Gr/Gb 偏差是固定工艺误差"**：还随亮度、ISO、温度变化，需动态/分档校正。
- **"校正强度越大越好"**：增益过大会放大噪声或损失细节，需权衡。
- **"平坦区才需要"**：迷宫格只出现在平坦区，统计也应只在平坦区做，避免纹理/边缘误统计。
- **"静态校正够用"**：静态 OTP 只补偿固定偏差，无法处理动态偏差，使用较少。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| green-balance-correction-audit-1 | wiki-bayer-filter | Bayer 阵半绿/四分之一红/四分之一蓝 |

## 待验证项

无。

## 关联知识

- [[demosaic]] —— 迷宫格是去马赛克后暴露的 Gr/Gb 偏差。
- [[black-level-correction]] —— raw 域前端的通道一致性处理。
- [[auto-white-balance]] —— Gr/Gb 偏差影响中性灰与 AWB。

## 详细章节

### 绿平衡背景

Bayer 阵列中绿色像素分为 Gr（处于红行）与 Gb（处于蓝行）。由于：

- 半导体制造工艺限制（不同行/列的微透镜与光刻差异）
- 微透镜（微透镜偏移/形状差异导致 Gr 与 Gb 的进光量不同）

导致 Gr 和 Gb 两个绿色分量存在偏差（gain 不一致），进而破坏灰度均衡。

### 影响

迷宫格（Maze pattern / 棋盘格伪彩）出现在平坦区域：当 Gr 与 Gb 增益不一致时，平坦区经去马赛克后会出现规律的亮暗相间纹理（迷宫格），同时也会使中性灰偏色、影响后续 AWB/CCM 的准确性。

### 绿平衡难点

绿平衡、噪声、细节：

- 校正本身是对 G 通道做增益调整，强度过大会放大噪声或损失细节；
- 不同亮度/ISO 下 Gr/Gb 偏差不同，需要分级（按亮度/增益分档）处理；
- 与降噪、细节增强的相互作用需要权衡。

### 绿平衡校正方法

#### 静态校正

根据 sensor 模组决定，使用较少：产线对每个模组标定固定的 Gr/Gb 增益差并写 OTP，只补偿固定的工艺偏差，无法处理随亮度/温度/增益变化的动态偏差，因此实际使用较少。

#### 动态校正

根据图像中像素之间的差值等关系动态决定：在平坦区域统计 Gr 与 Gb 的均值，用其差值动态调整 G 通道增益。

优化：阈值可以是动态的（随亮度/ISO 变化）。

1. 分别计算 Gr 和 Gb 平均值
2. 取 Gr 和 Gb 平均值的差值 diff
3. diff < 阈值
   - 如果为 False，无需校正处理
   - 如果为 True，校正 G 分量

即只有当 Gr/Gb 偏差超过阈值（可动态）时才施加校正，避免对正常场景过度调整，也避免在纹理/边缘区域误统计。

## 参考

- Gr/Gb 差异与迷宫格伪彩：成像系统绿平衡资料
- Bayer 模式与绿色通道：https://en.wikipedia.org/wiki/Bayer_filter
