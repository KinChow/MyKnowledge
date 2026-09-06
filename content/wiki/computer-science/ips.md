---
aliases: []
confidentiality: public
domain: computer-science
evidence:
- claim: camera3 内的 pipeline 由 HAL 控制。
  claim_id: ips-camera3-hal
  support: personal
  supporting_quotes:
  - evidence_id: evidence-62605ca2a77d
    exact: camera3内的pipeline由HAL控制
  targets:
  - evidence_id: evidence-62605ca2a77d
    source_id: working-computer-science-ips
id: ips
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- working-computer-science-ips
status: published
tags:
- camera
- image-processing
- isp
- architecture
title: IPS
updated_at: '2026-09-06'
---
# IPS

## 一句话结论

IPS（图像处理系统）是一套跨平台、跨操作系统的相机图像处理软件框架：以目标平台的 node/filter 形态存在，按"特性层 / 平台层 / 硬件抽象层 / 公共能力"分层，满足特性可裁剪、可配置决策机制与资源调度等需求，并通过 Server / Session / FilterBridge 对外提供图像处理能力。

## 核心概念

- **架构定位**：作为目标平台的一个 node/filter 存在，需要实现目标平台 node/filter 所需的接口；camera3 内的 pipeline 由 HAL 控制。
- **特性层**：主要用于接收处理系统外部（Camera3、CameraKit、HMS 等）请求，请求分为能力查询请求与图像处理请求两类。
- **平台层**：创建管理 pipeline（根据特性层提供的 pipeline 描述信息找到对应算法插件并创建）；资源管理和调度（根据各请求的优先级和资源冲突情况，高效灵活地调度算法运行）。
- **硬件抽象层**：对底层的硬件（ISP、IVP、NPU）进行抽象，以便更好地移植。
- **公共能力**：提供数据管理、内存管理、维测信息等基础能力。

## 工作机制

- **需求约束**：跨平台（支持海思、高通、MTK 平台）；跨操作系统（支持 OS 解耦）；特性与软件框架解耦（易扩展业务、提高开发效率）；特性可裁剪（通过裁剪快速在高中低平台配置特性列表）；决策机制（可配置算法全场景地图）；资源调度（最大硬件资源利用率）；自动化维测框架（减少维测成本）。
- **对外调用链**：Server（`QueryCapability` / `CreateSession`，开机创建）→ Session（`LoadRequest` / `GetFilterBridge`，根据外部系统请求创建，一个 cameraID 对应一个 Session）→ FilterBridge（`Configure` / `TransformFrame`，一个 Session 可创建多个，负责真正的图像处理）。
- **套件**：FrameCallback 通过回调查看每帧处理情况；EventCallback 查看事件处理情况；FrameAllocator 负责内存分配（决定每个 node 的内存是在 node 间传递还是创建）；Device 查询算法能力，根据不同 sensor 组建不同通路。
- **调度机制**：特性级调度（部分特性如 BestShot 有响应时间限制，需要高优先级快速响应）；算法级调度（算法开放给第三方应用，与自研相机可能存在资源冲突，通过 scheduler 按优先级运行）。

## 示例或代码

代码结构划分：

- **adapter（适配层）**：包含 Session、FilterBridge、DatabaseProxy。
- **algo_plugin（算法插件）**：包含感知引擎和处理引擎所需的算法。
- **feature（特性层）**：包含决策引擎、感知引擎。
- **platform（平台层）**：管道机制、维测、调度、server。
- **common（公共库）**：Database、Dmap、Message、内存池等。
- **app_manager（三方自动使能）**：支持通过配置文件，自动向目标三方应用使能底层算法。

## 常见误区

- **把特性逻辑与软件框架耦合**：需求明确要求"特性与软件框架解耦"，耦合会降低业务扩展性与开发效率，也不利于特性裁剪。
- **忽略请求优先级与资源冲突**：平台层按各请求的优先级和资源冲突情况调度算法运行，调度不当则无法实现最大硬件资源利用率。
- **忽略目标平台 node/filter 约束**：IPS 作为目标平台的 node/filter 存在，需实现对应接口；camera3 内的 pipeline 由 HAL 控制。

## 证据映射

| claim_id | 来源 | 要点 |
| --- | --- | --- |
| ips-camera3-hal | working-computer-science-ips | camera3 内的 pipeline 由 HAL 控制（personal 笔记） |

## 待验证项

- [ ] 本页正文（需求、架构、代码结构、对外/内部接口）来自个人笔记迁移，仅 camera3 pipeline 由 HAL 控制一条 claim 有证据锚定（support: personal）；
- [ ] 待补充外部权威来源（如 Android Camera HAL / ISP 相关文档）以升级证据。

## 关联知识

- [[android-camera-architecture]] —— Android Camera 架构：分层、接口与数据流
- [[isp-system]] —— ISP（图像信号处理）系统
- [[huawei-camera]] —— 华为相机系统

## 详细章节

### IPS

#### 需求

* 跨平台：支持海思、高通、MTK平台
* 跨操作系统：支持OS解耦
* 特性与软件框架解耦：易扩展业务，提高开发效率
* 特性可裁剪：通过裁剪，快速在高中低平台配置特性列表
* 决策机制：可配置算法全场景地图
* 资源调度：最大硬件资源利用率
* 自动化维测框架：减少维测成本



#### 架构

* 作为目标平台的一个node/filter存在
* 需要实现目标平台node/filter所需要的接口
* camera3内的pipeline由HAL控制



##### 特性层

主要用于接收处理系统外部（Camera3、CameraKit、HMS等）请求。

请求分为两类：

* 能力查询请求
* 图像处理请求



##### 平台层

* 创建管理pipeline：根据特性层提供的pipeline的描述信息，找到对应的算法插件，创建pipeline

* 资源管理和调度：根据各个请求的优先级和资源的冲突情况，高效灵活的调度算法运行



##### 硬件抽象层

对底层的硬件（ISP、IVP、NPU）进行抽象，以便更好的移植



##### 公共能力

提供基础能力，如数据管理、内存管理、维测信息等



#### 代码结构

##### adapter（适配层）

包含Session、FilterBridge、DatabaseProxy



##### algo_plugin（算法插件）

包含感知引擎和处理引擎所需的算法



##### feature（特性层）

包含决策引擎、感知引擎



##### platform（平台层）

管道机制、维测、调度、server



##### common（公共库）

Database、Dmap、Message、内存池等



##### app_manager（三方自动使能）

支持通过配置文件，自动向目标三方应用使能底层算法





#### 对外接口

##### 模块

###### Server

* QueryCapability

* CreateSession

开机创建



###### Session

* LoadRequest
* GetFilterBridge

根据外部系统的请求创建，一个cameraID对应一个Session



###### FilterBridge

* Configure
* TransformFrame

一个Session可以创建多个FilterBridge，FilterBridge负责真正的图像处理



##### 套件

###### FrameCallback

通过调用callback，查看每帧处理情况



###### FrameAllocator

内存分配，每个node的内存是在每个node传递还是创建



###### Device

查询算法能力，根据不同sensor组建不同通路



###### EventCallback

通过调用callback，查看事件处理情况



#### 内部接口

##### 感知引擎



##### 决策引擎



##### 处理引擎



##### 调度机制

###### 特性级调度

部分特性（如BestShot）有响应时间限制，需要高优先级快速响应。



###### 算法级调度

算法开放给第三方应用，和自研相机可能存在资源冲突，通过scheduler按优先级运行

