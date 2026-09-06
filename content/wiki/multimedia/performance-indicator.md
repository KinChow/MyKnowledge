---
aliases:
- 性能指标
- 相机性能
- 关键性能指标
- Camera 性能评测
confidentiality: public
domain: multimedia
evidence:
- claim: Profilers provide a summary of execution statistics and/or events. They give an overview of the overall performance of the program, often broken down to the functions, loops or even user-specified sections.
  claim_id: performance-indicator-audit-1
  support: direct
  supporting_quotes:
  - evidence_id: evidence-f6c8afdf6614
    exact: |-
      Profilers provide a summary of execution statistics and/or events. They give an overview of the overall performance of the program, often broken down to the functions, loops or even user-specified sections.
  targets:
  - evidence_id: evidence-f6c8afdf6614
    source_id: osti-profiling-tracing
id: performance-indicator
kind: reference
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- osti-profiling-tracing
- working-multimedia-performance-indicator
status: published
tags:
- camera
- performance
- benchmark
- multimedia
title: 关键指标
updated_at: '2026-09-05'
---
# 关键指标

## 详细章节

### 关键指标

#### 性能分类

##### 空载性能和负载性能

按照 camera 在运行时手机系统所处环境的复杂度，将性能分为空载性能和负载性能。

* 空载性能：camera 运行在一个干净的环境，开机静置半小时后，衡量 camera 性能指标。
* 负载性能：camera 运行在一个复杂的环境，模拟用户真实使用场景，启动相机之前启动 TOP15 个三方应用软件（如微信、微博、qq、王者荣耀、支付宝等），rom 空间强制填充在剩余 10%，camera 运行时确保后台有其他应用与 camera 竞争资源，在这种情况下衡量 camera 性能指标。

##### 场景性能

###### 启动

评估指标：

* 启动时延：从点击相机图标手抬起的时刻为开始时刻，相机出现真实取景界面的第二帧为结束时刻，差值为启动时延。

评估场景：

* 热启动：
  * 前置动作：点击 launcher 界面的相机图标，再点击 home 键退出。
  * 再次点击 launcher 界面的相机图标，该启动时延为热启动时间。

* 冷启动：
  * 前置动作：在后台进程中杀死 camera 应用。
  * 点击 launcher 界面的相机图标，该启动时延为冷启动时间。

* 首次启动：
  * 前置动作：手机重启。
  * 手机开机后，点击 launcher 界面的相机图标，该启动时延为首次启动时间。

###### 拍照

评估指标：

* shutter lag：打开相机，对准秒表（粗测）或者跑马灯（精测），点击拍照并查看生成的图片。点击拍照抬手时预览界面的秒表或者跑马灯时刻为开始时刻，图片中秒表或跑马灯时刻为结束时刻，差值为 shutter lag 性能。
* 连拍速度：打开相机，对准秒表，然后长按拍照按钮，连续拍摄 100 张照片，连拍速度 = 总照片数 / (最后一张照片结束时刻 - 第一张照片开始时刻)。
* 连拍数量：打开相机，然后长按拍照按钮，连续拍摄 10s，连拍数量为总照片数。
* shot2see：打开相机，对焦后点击拍照到生成照片。点击拍照键的抬手时刻为开始时刻，照片在缩略图内开始生成的时刻为结束时刻，差值为 shot2see 性能。
* see2review：打开相机，对焦后点击拍照到生成照片，点击缩略图直到照片完全显示出来。点击缩略图抬手时刻为开始时刻，照片完全显示出来为结束时刻，差值为 see2review 性能。
* shot2shot：打开相机，对准秒表对焦完成后，不断点击拍照按钮，持续 15s 以上，查看 15s 内拍照多少照片，shot2shot = 15s / 总照片数。
* shot2preview：打开相机，对焦后点击拍照后到预览画面重新恢复。点击拍照抬手时刻为开始时刻，预览重新恢复为结束时刻，差值为 shot2preview 性能。
* gallery2preview：打开相机，对焦后点击拍照后，通过缩略图进入图库预览，然后按返回键回到 camera 预览界面。点击返回键抬手时刻为开始时刻，预览第二帧出现为结束时刻，差值为 gallery2preview。
* Preview response time：
* Preview frozen time：
* AE 收敛时间：打开相机，用黑卡完全遮挡摄像头，快速将黑卡移开，直到画面亮度稳定。移开黑卡时刻为开始时刻，画面亮度稳定为结束时刻，差值为 AE 收敛时间。

评估场景：

* 拍照模式
  * 拍照
  * 人像
  * 大光圈
* 镜头
  * 主摄
  * 广角
  * 长焦
* 场景
  * 高亮
  * 中亮
  * 低亮
  * HDR 场景
  * 有人
  * 运动
    * 亮度
      * 600lux
      * 100lux
      * 20lux
    * 运动速度
      * 0.5m/s~2.5m/s

###### 对焦

评估指标：

* 对焦时延
  * 自动对焦性能：点击 launcher 界面的相机图标，打开相机，自动对焦到 xx m 远的目标，等待对焦完成。从点击相机图标手抬起的时刻为开始时刻，预览界面停止拉伸为结束时刻，差值为自动对焦性能。
  * 触控对焦性能：点击 launcher 界面的相机图标，打开相机，触控对焦，等待摄像头对焦完成。触控对焦抬手时刻为开始时刻，预览界面停止拉伸为结束时刻，差值为触控对焦性能。

评估场景：

* 镜头
  * 主摄
  * 广角
  * 长焦
  * 前置
* 场景
  * 棋盘格
  * 枯叶
  * 文字

###### 录像

评估指标：

* 时延
  * 录像启动：打开相机，选择录像模式，点击录像按钮到开始录像。点击录像按钮的抬手时刻为开始时刻，录像时间显示为 00:01 为结束时刻，差值为录像启动时延。
  * 录像停止
* 流畅性
  * 录像预览帧率
  * 录像帧率

评估场景：

* 分辨率
  * 4k
  * 1080p
* 帧率
  * 30fps
  * 60fps

###### 镜头切换

评估指标：

* 变焦跟手时延
* 镜头切换时延：打开相机，点击前后摄像头切换按钮，直到预览画面切换。点击切换摄像头抬手时刻为开始时刻，预览画面出现第二帧为结束时刻，差值为镜头切换时延。
* 变焦帧率/帧间隔

评估场景：

* 切换方式
  * 点击切换
  * 双指变焦
* 镜头
  * 主摄
  * 广角
  * 长焦
  * 前置

###### 模式切换

评估指标：

* 模式切换时延

评估场景：

* 拍照录像模式切换
* 拍照人像模式间切换
* 前后置切换

#### 来源说明

本文为相机性能评测的内部方法论（启动/拍照/对焦/录像/切换时延等指标口径），来源于团队评测规范，无单一外部文献来源；指标定义以本仓库为准。
