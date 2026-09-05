---
aliases: []
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
kind: reference
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- wiki-bayer-filter
- working-multimedia-green-balance-correction
status: published
tags:
- needs-fact-check
- web-source-added
- working-migration
title: 绿平衡校正
updated_at: '2026-09-05'
---
# 绿平衡校正

## 来源与迁移记录

### 迁移与校验记录

- 原始位置：`content/working/c-intermediate/multimedia/green-balance-correction.md`
- 原文快照：`working-multimedia-green-balance-correction`（personal-note；用于保留作者原始整理，不等同于外部权威来源）
- 外部链接：1 条；链接仅作为待补来源线索，尚未自动认定为事实依据。
- 当前状态：`draft`；事实正确性、来源逐条对应和必要的权威来源补齐待人工审查。

### 来源补充
- 来源隔离：当前绑定中的 `web-multimedia-green-balance-correction` 经正文检查确认是错误页/残留文本，已移除当前引用；Source 文件和历史审计记录保留。

- 已联网读取：`https://en.wikipedia.org/wiki/Bayer_filter`；来源正文已保存为不可变 Source 快照。

## 详细章节

### 绿平衡校正

#### 绿平衡背景

Bayer 阵列中绿色像素分为 Gr（处于红行）与 Gb（处于蓝行）。由于：

*   半导体制造工艺限制（不同行/列的微透镜与光刻差异）
*  微透镜（微透镜偏移/形状差异导致 Gr 与 Gb 的进光量不同）

导致 Gr 和 Gb 两个绿色分量存在偏差（gain 不一致），进而破坏灰度均衡。

#### 影响

迷宫格（Maze pattern / 棋盘格伪彩）出现在平坦区域：当 Gr 与 Gb 增益不一致时，平坦区经去马赛克后会出现规律的亮暗相间纹理（迷宫格），同时也会使中性灰偏色、影响后续 AWB/CCM 的准确性。

#### 绿平衡难点

绿平衡、噪声、细节：

- 校正本身是对 G 通道做增益调整，强度过大会放大噪声或损失细节；
- 不同亮度/ISO 下 Gr/Gb 偏差不同，需要分级（按亮度/增益分档）处理；
- 与降噪、细节增强的相互作用需要权衡。

#### 绿平衡校正方法

##### 静态校正

根据sensor模组决定，使用较少：产线对每个模组标定固定的 Gr/Gb 增益差并写 OTP，只补偿固定的工艺偏差，无法处理随亮度/温度/增益变化的动态偏差，因此实际使用较少。

##### 动态校正

根据图像中像素之间的差值等关系动态决定：在平坦区域统计 Gr 与 Gb 的均值，用其差值动态调整 G 通道增益。

优化：阈值可以是动态的（随亮度/ISO 变化）。

1. 分别计算Gr和Gb平均值
2. 取Gr和Gb平均值的差值diff
3. diff < 阈值
    * 如果为False，无需校正处理
    * 如果为True，校正G分量

即只有当 Gr/Gb 偏差超过阈值（可动态）时才施加校正，避免对正常场景过度调整，也避免在纹理/边缘区域误统计。

#### 参考
- Gr/Gb 差异与迷宫格伪彩：成像系统绿平衡资料
- Bayer 模式与绿色通道：https://en.wikipedia.org/wiki/Bayer_filter
