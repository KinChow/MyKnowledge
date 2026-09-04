---
aliases:
- Android Camera
- Camera HAL
- Camera HAL3
- CamX-CHI
confidentiality: public
domain: computer-science
evidence:
- claim: Camera HAL3 将 camera 子系统建模为流水线：每个 capture request 按 1:1 转换为一个 frame。
  claim_id: hal3-pipeline
  support: direct
  supporting_quotes:
  - evidence_id: evidence-fe448cb00526
    exact: "The API models the camera subsystem as a pipeline that converts incoming requests for frame captures into frames, on a 1:1 basis."
  targets:
  - evidence_id: evidence-fe448cb00526
    source_id: aosp-camera-hal3
- claim: Camera HAL 接口随 Android 演进：Android 8.0 引入 Treble，将 Camera HAL API 切换到由 HIDL 定义的稳定接口；从 Android 13 起 Camera HAL 接口开发改用 AIDL。
  claim_id: hal-interface-evolution
  support: direct
  supporting_quotes:
  - evidence_id: evidence-cf017f340ff1
    exact: "Starting with Android 13, camera HAL interface development uses AIDL. Android 8.0 introduced Treble, switching the Camera HAL API to a stable interface defined by the HAL interface description language (HIDL)."
  targets:
  - evidence_id: evidence-cf017f340ff1
    source_id: aosp-camera-hal3
- claim: Camera HAL 位于 camera driver 与更高层 framework 之间：向上连接 Camera 2 框架 API，向下定义必须实现以让应用正确操作相机硬件的接口。
  claim_id: hal-layer
  support: direct
  supporting_quotes:
  - evidence_id: evidence-d937f440c251
    exact: "The HAL sits between the camera driver and the higher-level Android framework and defines an interface that you must implement so apps can correctly operate the camera hardware."
  - evidence_id: evidence-8a33cfacf842
    exact: "Android's camera hardware abstraction layer (HAL) connects the higher-level camera framework APIs in Camera 2 to your underlying camera driver and hardware."
  targets:
  - evidence_id: evidence-d937f440c251
    source_id: aosp-camera-architecture
  - evidence_id: evidence-8a33cfacf842
    source_id: aosp-camera-architecture
- claim: Android 9 引入多摄像头 API 支持：由两个或多个指向同方向的物理摄像头设备组成逻辑摄像头设备，对应用呈现为单个 CameraDevice/CaptureSession。
  claim_id: multi-camera
  support: direct
  supporting_quotes:
  - evidence_id: evidence-260cce4b839f
    exact: "Android 9 introduced API support for multi-camera devices through a new logical camera device composed of two or more physical camera devices pointing in the same direction. The logical camera device is exposed as a single CameraDevice/CaptureSession to an app allowing for interaction with HAL-integrated multi-camera features."
  targets:
  - evidence_id: evidence-260cce4b839f
    source_id: aosp-camera-multi-camera
- claim: Camera metadata 分三类：static 是相机子系统的静态属性、可在配置输出管线或提交请求前查询；dynamic 随每帧生成并含实际使用的参数与时间戳；control 大多数设置预期可每帧修改而不引入明显卡顿或延迟。
  claim_id: metadata-types
  support: direct
  supporting_quotes:
  - evidence_id: evidence-ec5493ad2bf0
    exact: "Most of this information is a static property of the camera subsystem and can therefore be queried before configuring any output pipelines or submitting any requests."
  - evidence_id: evidence-ccd5ac3651b7
    exact: "the new camera API adds a substantial amount of dynamic metadata to each captured frame. This includes the requested and actual parameters used for the capture, as well as additional per-frame metadata such as timestamps and statistics generator output."
  - evidence_id: evidence-5fc4b7551293
    exact: "For most settings, the expectation is that they can be changed every frame, without introducing significant stutter or delay to the output frame stream."
  targets:
  - evidence_id: evidence-ec5493ad2bf0
    source_id: aosp-camera-metadata
  - evidence_id: evidence-ccd5ac3651b7
    source_id: aosp-camera-metadata
  - evidence_id: evidence-5fc4b7551293
    source_id: aosp-camera-metadata
- claim: HAL 是给硬件厂商实现的标准接口抽象层，允许厂商实现底层设备特定功能而不影响更高层代码；HIDL 用于 HAL client 与 HAL service 之间的通信。
  claim_id: hal-and-hidl
  support: direct
  supporting_quotes:
  - evidence_id: evidence-d8e44be806f4
    exact: "A hardware abstraction layer (HAL) is type of abstraction layer with a standard interface for hardware vendors to implement. A HAL allows hardware vendors to implement lower-level, device-specific features without affecting or modifying code in higher-level layers."
  - evidence_id: evidence-ffb3b59c768e
    exact: "HIDL enables communication between HAL clients and HAL services."
  targets:
  - evidence_id: evidence-d8e44be806f4
    source_id: aosp-hal-architecture
  - evidence_id: evidence-ffb3b59c768e
    source_id: aosp-hal-architecture
- claim: VTS（Vendor Test Suite）中大多数测试是检查 HAL 实现的 GTest 风格测试。
  claim_id: vts-tests-hal
  support: direct
  supporting_quotes:
  - evidence_id: evidence-21f66837f09c
    exact: "Most tests in VTS are GTest-style tests that check the HAL implementation."
  targets:
  - evidence_id: evidence-21f66837f09c
    source_id: aosp-vts
- claim: Linux 媒体框架把硬件设备建模为通过 pad 连接的 entity 图（media controller），entity 是基本媒体硬件构建块，可对应 CMOS sensor、SoC 图像处理流水线、DMA 通道等。
  claim_id: v4l2-media-controller
  support: direct
  supporting_quotes:
  - evidence_id: evidence-d3551866bc58
    exact: "hardware devices are modelled as an oriented graph of building blocks called entities connected through pads."
  - evidence_id: evidence-0267a563245f
    exact: "An entity is a basic media hardware building block. It can correspond to a large variety of logical blocks such as physical hardware devices (CMOS sensor for instance), logical hardware devices (a building block in a System-on-Chip image processing pipeline), DMA channels or physical connectors."
  targets:
  - evidence_id: evidence-d3551866bc58
    source_id: kernel-v4l2-mc
  - evidence_id: evidence-0267a563245f
    source_id: kernel-v4l2-mc
id: android-camera-architecture
kind: knowledge
publication_scope: public
related: []
sources:
- aosp-camera-architecture
- aosp-camera-hal3
- aosp-camera-metadata
- aosp-camera-multi-camera
- aosp-hal-architecture
- aosp-vts
- kernel-v4l2-mc
status: published
tags:
- android
- camera
- hal
- v4l2
- mobile
title: Android Camera 架构：分层、接口与数据流
updated_at: '2026-09-04'
---

# Android Camera 架构：分层、接口与数据流

## 一句话结论

Android Camera 是分层架构：App 通过 Camera2 API 与框架交互，向下依次是 Camera framework（App 进程内客户端）、Camera service（系统进程）、Camera provider/HAL（vendor 进程，Android 8.0/Treble 起为 HIDL 接口、Android 13 起为 AIDL 接口）、Kernel 驱动（V4L2/media controller）与硬件（Sensor/ISP）。核心是 HAL3 把每个 capture request 按 1:1 转成 frame 的流水线，配合 static/control/dynamic 三类 metadata；多摄通过"逻辑摄像头设备"对应用透明呈现为单个 CameraDevice。

## 核心概念

- **Camera HAL3**：把 camera 子系统建模为 request→frame 的 1:1 流水线；request 封装该帧捕获与处理的全部配置（分辨率/像素格式、手动 sensor/lens/flash 控制、3A 模式、RAW→YUV 处理等）。
- **分层**：App → Framework（App 进程）→ Service（系统进程）→ Provider/HAL（vendor 进程）→ Driver（Kernel）→ Hardware。
- **接口演进**：Android 8.0 Treble 引入 HIDL 稳定接口；Android 13 起新特性仅走 AIDL Camera HAL。
- **metadata 三分类**：static（特性，配置前查询）、control（每帧可改的设置）、dynamic（每帧结果，含实际参数与时间戳）。
- **逻辑摄像头设备**（Android 9）：多个同方向物理摄像头组成一个逻辑设备，对应用是单个 CameraDevice/CaptureSession。
- **VTS**：验证 HAL 实现等 vendor 侧（GTest 风格为主）。
- **V4L2/media controller**：Linux 通用视频框架，把硬件建模为 entity/pad 图，暴露硬件拓扑给用户空间。

## 工作机制

请求从 App 到硬件的流转：

1. **App 层**：通过 Camera2 API（`CameraManager` → `openCamera` → `createCaptureSession` → `CaptureRequest`）向框架发起预览/拍照/录像请求。
2. **Camera framework**（App 进程内）：封装 Camera2 API 实现细节，通过 AIDL 跨进程接口（`ICameraService` / `ICameraDeviceUser`）把请求发给 Camera service。
3. **Camera service**（系统进程）：维护请求处理逻辑，把请求下发到 Camera provider。
4. **Camera provider/HAL**（vendor 进程）：加载厂商实现的 HAL 模块（遵循 HAL3 标准接口），驱动底层硬件。
5. **Kernel 驱动**：视频采集设备走 V4L2；媒体框架用 media controller 以 entity/pad/link 图描述硬件拓扑。
6. **结果回传**：图像数据经 Buffer Queue 返回 App；每帧的 metadata（含实际使用的曝光/帧时长/灵敏度等）随结果返回。

## 示例或代码

Camera2 API 基本调用流程（Java 伪代码）：

```java
CameraManager manager = (CameraManager) getSystemService(CAMERA_SERVICE);
// static metadata：能力/规格，配置管线前即可查询
CameraCharacteristics chars = manager.getCameraCharacteristics(cameraId);
// 打开设备 -> 创建 capture session -> 构建 request（control 设置）
manager.openCamera(cameraId, stateCallback, handler);      // -> CameraDevice
device.createCaptureSession(outputSurfaces, sessionCb, handler); // -> CameraCaptureSession
CaptureRequest.Builder req = device.createCaptureRequest(TEMPLATE_PREVIEW);
req.addTarget(previewSurface);
session.setRepeatingRequest(req.build(), captureCb, handler); // dynamic 结果在回调中逐帧返回
```

## 常见误区

- **"framework 和 service 是同一个东西"**：framework 是运行在 App 进程内的客户端库，service 才是独立的系统进程。
- **"现在还在用 HIDL"**：Android 13+ 新增的 Camera 特性只通过 AIDL HAL 提供，HIDL 仅用于兼容旧设备。
- **"多摄就是多个 CameraDevice"**：逻辑摄像头设备把多个物理摄像头包装成单个 CameraDevice/CaptureSession 给应用。
- **"V4L2 是 Android 特有的"**：V4L2 与 media controller 是 Linux 内核通用视频框架，Android 只是其使用方之一。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| hal3-pipeline / hal-interface-evolution | aosp-camera-hal3 | HAL3 流水线 + Treble/AIDL 演进 |
| hal-layer | aosp-camera-architecture | HAL 位于 driver 与 framework 之间 |
| multi-camera | aosp-camera-multi-camera | Android 9 逻辑摄像头设备 |
| metadata-types | aosp-camera-metadata | static/control/dynamic 三分类 |
| hal-and-hidl | aosp-hal-architecture | HAL 抽象层 + HIDL 通信 |
| vts-tests-hal | aosp-vts | VTS 测试 HAL 实现 |
| v4l2-media-controller | kernel-v4l2-mc | media controller entity/pad 模型 |

## 待验证项

无。

## 关联知识

- [[adb]] —— Android 系统工具链（同一 Android 域）。
- [[architecture-and-organization]] —— ARM 处理器与微架构（Camera HAL 之上与之下都依赖处理器子系统）。

## 详细章节

> 说明：本页 evidence claims 均来自官方文档；以下厂商实现细节（高通 CamX-CHI / KMD / ISP 分块）来自厂商文档与社区资料整理，属描述性内容，不作 evidence claims。

### Camera App（应用层）

应用层处于整个框架的顶层，和用户直接交互，采纳用户直接或间接的需求（例如拍照、预览、录像等）。一旦接收到用户相关的 UI 操作，便会通过 Camera API v2 标准接口将需求发给 Camera framework，并等待 framework 回传处理结果，结果包括图像数据和整体相机系统状态参数。

Camera App 基本流程：

1. 获取 `CameraManager`
2. 打开 Camera 设备
3. 创建 Camera capture session
4. 发送图像请求到 Camera Framework
5. Camera Framework 返回 metadata，Buffer Queue 返回图像数据到 Camera App 的预览/拍照/录像

### Camera framework

位于 camera app 与 camera service 之间，作为 framework 的一部分运行在 App 进程中。它封装了 Camera API v2 接口的具体实现细节，只暴露接口给 app 调用；接收来自 app 的请求，同时维护请求在内部流转的业务逻辑，最终通过调用 Camera AIDL 跨进程接口将请求发送给 camera service，然后等待 camera service 结果回传，进而将最终结果发送至 app。

### Camera service

位于 Camera framework 与 Camera provider 之间，作为独立进程存在于 Android 系统中，在系统启动初期运行。它封装了 Camera AIDL 跨进程接口，提供给 framework 调用，接收来自 framework 的图像请求；内部维护请求在该层的处理逻辑，最终通过 Camera HAL 接口（Treble 起为 HIDL、Android 13 起为 AIDL）将请求下发到 Camera provider，并等待结果回传、将结果上传至 framework。

### Camera provider

始于 Google Treble 开源项目，基于接口与实现分离的设计原则，位于 Camera service 与 Camera driver 之间，作为独立进程在系统启动初期运行。它提供 Camera HAL 跨进程接口（Treble 起为 HIDL、Android 13 起为 AIDL）供 Camera service 调用，封装了接口的实现细节；接收来自 service 的图像请求，内部加载 Camera HAL Module（由 OEM/ODM 实现，遵循 Google 制定的标准 Camera HAL3 接口），通过该接口控制 Camera HAL 部分，最后等待结果回传，再通过 HAL 接口将结果发送至 Camera service。

### Camera HAL：高通 CamX-CHI（厂商实现）

该部分是高通对 Google Camera HAL3 接口的实现，以 so 库形式加载进 Camera Provider。旧架构采用 QCamera & MM-Camera，为了更好的灵活性和可扩展性，高通提出了 CamX-CHI 架构：

- **CamX**：负责基础服务代码的实现，不经常改动，对上实现 HAL3 接口，对下通过 V4L2 框架与 Kernel 通信，并通过 dlopen so 库与 CHI 交互。目录含 `core/`（核心实现，含 HAL3 入口 `hal/` 与 CHI 交互 `chi/`）、`csl/`（与 camera 驱动通信的统一控制接口）、`hwl/`（具有独立运算能力的硬件 node，受 CSL 管理）、`swl/`（依赖 CPU 实现的软件 node）。
- **CHI**：负责实现可扩展性和定制化需求，方便 OEM/ODM 添加自己的扩展功能。CHI 通过抽象出 **Usecase、Feature、Session、Pipeline、Node** 概念（Usecase 包含 Feature，Feature 包含 Session，Session 管理内部 Pipeline 的数据流转，Pipeline 通过 Link 连接各 Node），使厂商可以通过实现 Node 接口接入自己的算法，并通过 XML 文件（`topology/`）灵活配置 Usecase、Pipeline、Node 的结构关系。

### Camera driver：V4L2 与高通 KMD

Linux 为视频采集设备制定了标准的 V4L2 接口，并在内核中实现了其基础框架 V4L2 Core。用户空间进程可以通过 V4L2 接口调用相关设备功能而不用考虑实现细节。V4L2 提出总设备和子设备的概念，并通过 media controller 机制向用户空间暴露自己的硬件拓扑结构。视频采集设备驱动厂商按照 V4L2 Core 的要求开发驱动，只需实现相应的结构体和函数接口并调用注册函数注册自己。Linux 内核文档中的 Qualcomm Camera Subsystem（CamSS）驱动即实现 V4L2、media controller 与 V4L2 subdev 三类接口，按 CSIPHY/CSID/ISPIF/VFE 拆分为多个子设备，并暴露 `/dev/video*` 与 `/dev/v4l-subdev*` 设备节点。

在高通平台上，KMD 框架包含三部分：

- **CRM**：框架顶层管理者，创建 V4L2 主设备管理所有子设备，暴露设备节点 `video0` 给用户空间，内部维护整个底层驱动业务逻辑。
- **Camera Sync**：创建 V4L2 主设备，暴露设备节点 `video1`，主要用于向用户空间反馈图像数据处理状态。
- **子设备**：抽象成 `v4l2_subdev` 设备，暴露设备节点 `v4l2-subdev` 给用户空间进行更精细化的控制。

初始化过程中通过 media controller 机制，保持用户空间枚举底层硬件设备的能力。

V4L2 帧数据流基本流程：

1. 打开 video 设备
2. 查看并设置设备
3. 申请帧缓冲区
4. 开启数据流
5. 将帧缓冲区入队
6. 将帧缓冲区出队
7. 取出帧数据

### Camera hardware

相机硬件处在整个相机体系的最底层，是相机系统的物理实现部分，包括镜头、感光器、ISP 三个最重要的模块，以及对焦马达（VCM）、闪光灯、滤光片、光圈等辅助模块。

- **镜头**：汇聚光线，利用光的折射性把射入的光线汇聚到感光器上。
- **感光器（Sensor）**：负责光电转换，通过内部感光元件将光信号转换为电子信号，再经数电转换模块转为数字信号，最后传给 ISP。
- **ISP**：负责对数字图像做算法处理，如白平衡、降噪、去马赛克等。

高通 ISP 典型分块（数据流 IFE → BPS → IPE → JPEG）：

- **IFE（Image Front End）**：Sensor 输出的数据首先到达 IFE，针对 preview/video 做颜色校正、下采样、去马赛克、3A 数据统计。
- **BPS（Bayer Processing Segment）**：用于拍照图像数据的坏点去除、相位对焦、去马赛克、下采样、HDR 处理以及 Bayer 混合降噪。
- **IPE（Image Processing Engine）**：由 NPS（噪声处理段）、PPS（像素处理段）两部分组成，承担硬件降噪（MFNR、MFSR）、图像裁剪、降噪、颜色处理、细节增强等工作。
- **JPEG**：拍照数据的存储通过该硬件模块进行 JPEG 编码。

其他硬件模块：**VCM**（音圈马达，驱动镜头对焦，部分方案亦控制光圈叶片）、**IR-cut**（红外截止滤光片，滤除红外线，只让可见光通过）、**MIPI CSI**（Sensor 与 SoC 之间的图像传输接口）、**I2C**（控制通路）。

### 多摄

Android 9（2018/8）通过新的逻辑摄像头设备（由两个或更多个指向同一方向的物理摄像头设备组成）引入对多摄像头设备的 API 支持。逻辑摄像头设备以单个 `CameraDevice`/`CaptureSession` 的形式提供给应用，从而允许与集成在 HAL 中的多摄像头功能交互；应用可以选择访问和控制底层物理摄像头的信息流、元数据和控件。

### CTS 与 VTS

- **CTS（Compatibility Test Suite）**：为了保证开发的应用在所有兼容 Android 的设备上正常运行并保证一致的用户体验，Google 制定 CTS 确保设备运行的 Android 系统全面兼容 Android 规范，并提供兼容性标准文档（Compatibility Definition Document, CDD）。设备厂商定制 Android 系统后必须通过最新 CTS 检测，并将测试报告提交给 Google 以获得认证（可在 Google Play 上架）。CTS 是通过命令行操作的工具。
- **VTS（Vendor Test Suite）**：由一套测试框架和测试用例组成，目的是提高 Android 系统（核心 HAL 和库）与底层系统软件（内核、模块、固件）的健壮性、可靠性与合规性。Google 发起 Project Treble 项目，而 Treble 中最重要的就是新增 Vendor Interface 概念及相应的 VTS 测试。

### meta 分类

- **control (request)**：应用查询出 static metadata 后据此对每帧做相应控制（如曝光、对焦、闪光灯等），每帧都可设定，随 capture request 提交并绑定对应的图像回调。
- **dynamic (result)**：HAL 收到 control 设置后执行捕获，每帧生成动态 metadata（实际使用的参数、统计结果等）并随帧结果返回。
- **static (characteristics)**：描述逻辑设备（logical device）的规格与提供什么功能，开机阶段能力上报。

### 参考

- https://source.android.com/docs/core/camera
- https://source.android.com/docs/core/camera/camera3
- https://source.android.com/docs/core/camera/camera3_metadata
- https://source.android.com/docs/core/camera/multi-camera
- https://source.android.com/docs/core/architecture/hal
- https://source.android.com/docs/core/tests/vts
- https://docs.kernel.org/driver-api/media/mc-core.html
- https://docs.kernel.org/admin-guide/media/qcom_camss.html —— Qualcomm Camera Subsystem 驱动（V4L2/subdev/media controller）
- https://www.cnblogs.com/schips/p/android_cam_x_software_stack.html —— CamX-CHI 架构梳理（厂商实现）
- https://developer.ridgerun.com/wiki/index.php/Qualcomm_Robotics_RB5/Capture_Subsystem/Hardware_Capture_Components —— 高通 ISP 分块 IFE/BPS/IPE
- https://cloud.tencent.com/developer/article/1821976 —— 高通 Camera 数字成像系统简介（ISP 与滤光片）
