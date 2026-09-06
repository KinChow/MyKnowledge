---
aliases:
- 闪光灯
- Flash
- 氙灯
confidentiality: public
domain: multimedia
evidence:
- claim: 闪光灯是摄影时所使用的人造光源，按下快门后（通常 1/1000 到 1/200 秒之间）照亮场景。
  claim_id: flash-definition
  support: personal
  supporting_quotes:
  - evidence_id: evidence-852cd706ccab
    exact: 闪光灯是在摄影时所使用的人造光源。当接下照相机的快门之后，通常在1/1000到1/200秒之间，照亮场景。
  targets:
  - evidence_id: evidence-852cd706ccab
    source_id: working-multimedia-flash
id: flash
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- working-multimedia-flash
status: published
tags:
- camera
- flash
- photography
- multimedia
title: 闪光灯
updated_at: '2026-09-04'
---

# 闪光灯

## 一句话结论

闪光灯是摄影时所使用的人造光源，按下快门后（通常 1/1000 到 1/200 秒）照亮场景，用于暗光瞬间照明或亮光场合局部补光。类型上 Xenon（氙灯）强度/显色/灵活性最高但体积价格差，LED 持续光灵活便宜（主流：蓝 LED+荧光粉合成白光）。关键参数指导数 GN = 光圈 × 距离；同步方式有高速/慢速同步、前帘/后帘同步，后帘同步适合夜景人像定格运动主体。

## 核心概念

- **闪光灯**：摄影用人造光源；暗光瞬间照明 + 亮光局部补光。
- **类型**：Xenon（强度/CRI/灵活性高、价格尺寸差）vs LED（持续光、便宜，蓝 LED+荧光粉为主流）。
- **GN 指数**：GuideNumber = FNumber × Distance，衡量闪光强度。
- **同步**：高速同步（<1/250s）、慢速同步（慢快门+闪光补光）；前帘/后帘同步。
- **常见问题**：反光、Flash AE 过/欠曝、Flash AWB 色偏、能量不足远景不亮、运动模糊。

## 工作机制

1. **触发**：按下快门，闪光灯在 1/1000~1/200 秒间照亮场景。
2. **同步**：闪光与快门幕帘同步——高速同步（快门开启期间保持同步）、慢速同步（慢快门+近景补光）；前帘同步（前帘打开瞬间闪）、后帘同步（后帘关闭瞬间闪，夜景人像定格主体）。
3. **曝光控制**：按 GN = FNumber × Distance 计算/校准闪光量，配合 Flash AE/AWB。

## 示例或代码

```text
GN = FNumber × Distance
（闪光指数 = 光圈 × 距离；已知 GN 可推算合适光圈/距离组合）

快门工作过程：
  快门触发 → 后幕帘开启 → 前幕帘开启（曝光开始）→ 后幕帘关闭（曝光结束）→ 前幕帘关闭

前帘同步：前帘打开瞬间闪光 → 曝光 → 后帘关闭
后帘同步：后帘关闭瞬间闪光（运动物体定格，夜景人像常用）
```

## 常见误区

- **"闪光灯只是补光"**：也用于亮光场合局部补光、逆光近景补光、慢速同步创造动感。
- **"LED 闪光灯没氙灯好"**：LED 持续光灵活、便宜、可做补光灯，主流方案是蓝 LED+荧光粉合成白光；氙灯强度/CRI 高但体积价格差。
- **"前后帘同步没区别"**：拍静止物体无区别；拍运动物体（夜景人像）后帘同步能把主体定格在画面中。
- **"闪光灯不会出错"**：会带来反光、Flash AE 过/欠曝、Flash AWB 色偏、能量不足远景不亮、曝光时间过长运动模糊等问题。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| flash-definition | working-multimedia-flash | 闪光灯是摄影用人造光源 |

## 待验证项

无。

## 关联知识

- [[auto-exposure]] —— Flash AE 与自动曝光联动。
- [[auto-white-balance]] —— Flash AWB 与闪光灯色温相关。
- [[overview-of-3a]] —— 闪光是曝光控制的一部分。

## 详细章节

### 闪光灯的作用

闪光灯是在摄影时所使用的人造光源。当按下照相机的快门之后，通常在 1/1000 到 1/200 秒之间照亮场景。闪光灯多用于光线较暗的场合瞬间照明，也用于光线较亮的场合给被拍摄对象局部补光。

### 闪光灯的类型

| 类型 | Xenon | LED | Dual LED |
| --- | --- | --- | --- |
| Intensity | 10 | 1 | 1 |
| Duration（持续时间） | 1（10ms 以下） | 10 | 10 |
| CRI | 10 | 5 | 8 |
| flexibility | 10 | 5 | 8 |
| speed | 10 | 10 | 10 |
| Price/Size | 1 | 10 | 10 |

（数值为相对评分：10 为优。）

### 闪光灯的原理

#### 类型

1. Three color LED combined to generate white light
2. Blue LED + phosphor combined to generate white light（主流方案）

$$
GuideNumber(GN) = FNumber * Distance
$$

#### 快门工作过程

1. 当快门被触发后
2. 后幕帘开启
3. 前幕帘开启——曝光开始
4. 后幕帘关闭——曝光结束
5. 前幕帘关闭

#### 高速同步与慢速同步

- **高速同步**：相机使用较快快门速度时（一般 <1/250s），闪光灯参与曝光并在快门开启期间与快门保持同步速度。
- **慢速同步**：相机使用较慢快门速度时，闪光灯参与曝光并成功在快门完全开启期间触发闪光。目的是在较慢环境下拍摄时，用慢速快门保障整幅画面充足曝光，并利用闪光灯对有效照射范围内近景补光，获得远景和逆光近景亮度均衡的效果，或拍摄运动物体的动感特效。

#### 前帘同步与后帘同步

- **前帘同步**：在前帘打开的瞬间闪光灯发出光线，感光元件进行曝光，然后后帘关闭曝光结束。
- **后帘同步**：在后帘关闭的瞬间闪光灯发出光线，感光元件进行曝光，然后后帘关闭曝光结束。拍静止物体时两者没有区别，但拍运动物体区别大；拍夜景人像时常用后帘同步，最终将人定格在画面中。

#### 闪光灯的常见问题

- 物体反光
- Flash AE 造成的过/欠曝
- Flash AWB 造成的色偏
- 能量不够造成的远景不亮
- 曝光时间太长造成运动模糊

## 参考

- 氙灯 vs LED 闪光灯对比：https://en.wikipedia.org/wiki/Flash_(photography)
- 闪光灯同步（前帘/后帘/高速同步）：https://en.wikipedia.org/wiki/Flash_synchronization
