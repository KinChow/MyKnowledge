# IPS

## 需求

* 跨平台：支持海思、高通、MTK平台
* 跨操作系统：支持OS解耦
* 特性与软件框架解耦：易扩展业务，提高开发效率
* 特性可裁剪：通过裁剪，快速在高中低平台配置特性列表
* 决策机制：可配置算法全场景地图
* 资源调度：最大硬件资源利用率
* 自动化维测框架：减少维测成本



## 架构

* 作为目标平台的一个node/filter存在
* 需要实现目标平台node/filter所需要的接口
* camera3内的pipeline由HAL控制



### 特性层

主要用于接收处理系统外部（Camera3、CameraKit、HMS等）请求。

请求分为两类：

* 能力查询请求
* 图像处理请求



### 平台层

* 创建管理pipeline：根据特性层提供的pipeline的描述信息，找到对应的算法插件，创建pipeline

* 资源管理和调度：根据各个请求的优先级和资源的冲突情况，高效灵活的调度算法运行



### 硬件抽象层

对底层的硬件（ISP、IVP、NPU）进行抽象，以便更好的移植



### 公共能力

提供基础能力，如数据管理、内存管理、维测信息等



## 代码结构

### adapter（适配层）

包含Session、FilterBridge、DatabaseProxy



### algo_plugin（算法插件）

包含感知引擎和处理引擎所需的算法



### feature（特性层）

包含决策引擎、感知引擎



### platform（平台层）

管道机制、维测、调度、server



### common（公共库）

Database、Dmap、Message、内存池等



### app_manager（三方自动使能）

支持通过配置文件，自动向目标三方应用使能底层算法





## 对外接口

### 模块

#### Server

* QueryCapability

* CreateSession

开机创建



#### Session

* LoadRequest
* GetFilterBridge

根据外部系统的请求创建，一个cameraID对应一个Session



#### FilterBridge

* Configure
* TransformFrame

一个Session可以创建多个FilterBridge，FilterBridge负责真正的图像处理



### 套件

#### FrameCallback

通过调用callback，查看每帧处理情况



#### FrameAllocator

内存分配，每个node的内存是在每个node传递还是创建



#### Device

查询算法能力，根据不同sensor组建不同通路



#### EventCallback

通过调用callback，查看事件处理情况



## 内部接口

### 感知引擎



### 决策引擎



### 处理引擎



### 调度机制

#### 特性级调度

部分特性（如BestShot）有响应时间限制，需要高优先级快速响应。



#### 算法级调度

算法开放给第三方应用，和自研相机可能存在资源冲突，通过scheduler按优先级运行

