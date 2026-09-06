---
aliases:
- NPU
- 神经处理单元
- AI 加速器
- 深度学习处理器
- Neural Processing Unit
confidentiality: public
domain: computer-science
evidence:
- claim: NPU（神经处理单元，又称 AI 加速器或深度学习处理器）是一类专用硬件加速器或计算机系统，用于加速人工智能与机器学习应用（包括人工神经网络与计算机视觉）；NPU
    可以独立存在、作为 CPU 的一部分或作为 GPU 的一部分。
  claim_id: npu-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-1954a2deedbb
    exact: A neural processing unit (NPU), also known as an AI accelerator or deep
      learning processor, is a class of specialized hardware accelerator or computer
      system designed to accelerate artificial intelligence and machine learning applications,
      including artificial neural networks and computer vision. NPU can be standalone,
      a part of a CPU or a part of a GPU.
  targets:
  - evidence_id: evidence-1954a2deedbb
    source_id: web-computer-science-npu
- claim: NPU 的用途要么是高效执行已训练好的 AI 模型（如 LLM 的推理 inference），要么是训练 AI 模型；NPU 在速度或功耗上可能更高效。
  claim_id: npu-purpose
  support: direct
  supporting_quotes:
  - evidence_id: evidence-5df13bc15608
    exact: Their purpose is either to efficiently execute already trained AI models
      like LLMs (inference) or to train AI models. NPUs can be more efficient in terms
      of speed or power consumption.
  targets:
  - evidence_id: evidence-5df13bc15608
    source_id: web-computer-science-npu
- claim: 自 2010 年代末起，Nvidia、AMD 等公司的 GPU 常包含 AI 专用硬件——面向低精度矩阵乘法的专用功能单元；这些 GPU 常作为
    AI 加速器用于训练与推理。
  claim_id: npu-gpu-trend
  support: direct
  supporting_quotes:
  - evidence_id: evidence-e867730dc7d6
    exact: Since the late 2010s, graphics processing units designed by companies such
      as Nvidia and AMD often include AI-specific hardware in the form of dedicated
      functional units for low-precision matrix-multiplication operations. These GPUs
      are commonly used as AI accelerators, both for training and inference.
  targets:
  - evidence_id: evidence-e867730dc7d6
    source_id: web-computer-science-npu
id: npu-overview
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-npu
status: published
tags:
- npu
- ai
- accelerator
- hardware
- deep-learning
title: NPU 神经处理单元
updated_at: '2026-09-06'
---

# NPU 神经处理单元

## 一句话结论

NPU（Neural Processing Unit，神经处理单元，又称 AI 加速器 / 深度学习处理器）是一类**专用硬件加速器**，用于加速人工智能与机器学习应用——包括人工神经网络与计算机视觉；它可以独立存在、集成进 CPU 或集成进 GPU。NPU 的职责是高效执行已训练模型（推理 inference）或训练模型，在速度与功耗上通常优于通用处理器；其与 CPU/GPU 的核心差异在于：CPU 是少而复杂的通用控制核心，GPU 是多而并行的矩阵吞吐核心，而 NPU 为 AI 运算（低精度矩阵乘法、卷积、激活）做**领域专用**的极致优化（DSA），即“为特定算法定制架构”。

## 核心概念

- **NPU / AI 加速器 / 深度学习处理器**：面向 AI/ML 应用的专用硬件加速器，可独立、或在 CPU/GPU 内实现。
- **训练 vs 推理**：训练（training）是反向传播更新权重；推理（inference）是前向计算使用已训练模型（如 LLM 生成）。
- **DSA（Domain-Specific Architecture）**：针对特定领域（如 AI）定制的数据通路/存储/指令，换取能效与吞吐，是 AI 芯片的主流路线（相对通用 ISA 的取舍）。
- **低精度矩阵运算**：AI 推理常用 INT8/INT4/FP16 等低精度矩阵乘法，NPU/张量核心据此做专用功能单元。
- **部署形态**：云（数据中心/服务）、边（边缘网关）、端（手机/IoT），对应不同算力与功耗约束。

## 工作机制

1. **数据流**：输入特征图/权重按 NPU 的张量指令载入片上 SRAM → 乘加阵列（MAC array）逐层计算 → 激活/池化/归一化等算子流水执行 → 输出写回。计算以矩阵乘法与卷积为核心。
2. **与 CPU 协作**：NPU 作为加速器，由 CPU（或 DSP）负责任务调度、内存搬运、控制流；NPU 专注批量张量计算（SIMD/脉动阵列）。
3. **与 GPU 的区别**：GPU 用大量通用 SIMT 核心做图形/通用并行计算；NPU 去掉与 AI 无关的图形管线，用更专用的乘加阵列与低精度支持换取更高能效。
4. **软件栈**：上层库/框架（TensorFlow、PyTorch）→ 厂商 API（AMD Ryzen AI、Intel OpenVINO、Apple CoreML、Qualcomm SNPE、NVIDIA CUDA）→ NPU 驱动/编译器（把 ONNX 等模型格式映射为 NPU 指令）。

## 示例或代码

- **典型 NPU 产品形态**：
  - 独立 AI ASIC：Google TPU、华为昇腾（Ascend）310/910、寒武纪思元；
  - 集成进 SoC：Apple Neural Engine（A 系列/M 系列）、Qualcomm Hexagon NPU、联发科 APU、华为达芬奇（DaVinci）架构（见 [[davinci]]）；
  - GPU 内张量核心：NVIDIA Tensor Core、AMD Matrix Core。

- **软件接口示例**（概念示意，非真实 API）：

```python
import onnxruntime as ort
# 把 ONNX 格式的已训练模型交给 NPU/加速器执行（推理）
session = ort.InferenceSession("model.onnx", providers=["CPUExecutionProvider"])
output = session.run(None, {"input": input_tensor})
```

## 常见误区

- **“NPU 就是 GPU”**：GPU 是通用并行处理器（图形+计算），NPU 是 AI 领域专用加速器；现代 GPU 常内置类 NPU 的张量单元，但两者定位不同（见 [[gpu-overview]]）。
- **“NPU 能跑所有 AI 任务”**：NPU 对特定算子/精度优化；控制流复杂、算子不匹配的模型可能效率低下甚至回退到 CPU/GPU。
- **“有 NPU 就不需要 CPU/GPU”**：NPU 是加速器，仍需 CPU 调度、GPU 承担图形与部分通用并行计算，三者异构协作。
- **“NPU 只做推理”**：NPU 既能推理也能训练（如昇腾 910、TPU 用于训练），只是多数端侧 NPU 面向推理优化。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| npu-definition | web-computer-science-npu | NPU 定义与三种存在形态（独立/CPU 内/GPU 内） |
| npu-purpose | web-computer-science-npu | 推理/训练两用途，速度与功耗优势 |
| npu-gpu-trend | web-computer-science-npu | GPU 内置低精度矩阵专用单元成为 AI 加速器 |

## 待验证项

- 各厂商 NPU 的具体架构细节（乘加阵列规模、片上存储、编译器模型）属于实现层面，本文不逐一代入；可结合 [[davinci]]（华为达芬奇）等具体架构页面深化。
- “NPU 典型产品形态”表格为本人综合的常识性罗列，建议按具体芯片官方资料复核。

## 关联知识

- [[cpu-and-memory]] —— 通用处理器与内存体系（NPU 依赖 CPU 调度）。
- [[gpu-overview]] —— GPU 通用并行架构与 NPU 的差异。
- [[davinci]] —— 华为达芬奇 AI 计算架构（NPU 具体实现之一）。
- [[soc]] —— NPU 作为 SoC 组成单元的集成形态。
- [[computer-hardware]] —— 硬件整体构成（NPU 在其中的位置）。

## 详细章节

### 什么是 AI 芯片

AI 芯片泛指为人工智能计算优化的处理器。其主流路线是 **DSA（Domain-Specific Architecture，领域专用架构）**——针对 AI 计算的特点定制数据通路、存储层次与指令，从而在能效/吞吐上大幅优于通用处理器。好处是特定算法（矩阵乘法、卷积）跑得又快又省电；代价是通用性下降、适配新模型需要编译器/驱动支持。

AI 芯片需要完成两类任务：

- **训练**：利用大量数据与反向传播算法迭代更新模型参数（权重），计算量大、精度要求高（多为 FP32/BF16）。
- **推理**：使用已训练好的模型对新输入做前向计算（如 LLM 生成、图像识别），对时延与功耗敏感，常用低精度（INT8/INT4/FP16）加速。

### 部署方式

- **云（Cloud）**：数据中心以 Web 服务形式提供 AI 能力（大模型 API、云推理），算力强、可扩展。
- **边（Edge）**：靠近数据源的网关/服务器，权衡算力与网络延迟。
- **端（Device）**：手机与 IoT 应用系统，算力受限但低延迟、隐私好、可离线。

### 技术路线

- **GPU**：通用并行图形/计算单元（CUDA/OpenCL），叠加 AI 专用张量单元后广泛用于训练与推理。
- **FPGA**：可重构硬件，灵活但开发复杂、能效相对 ASIC 低，适合原型与多变场景。
- **ASIC（NPU 属于此类）**：为 AI 定制的专用集成电路（如 TPU、昇腾、苹果 Neural Engine），能效最高，但一旦流片功能固定、迭代成本高。

### 应用场景

- **计算中心**：云端训练与大规模推理（大模型、推荐系统）。
- **自动驾驶**：车载 NPU 实时处理视觉/传感器数据（多路摄像头、激光雷达）。
- **安防应用**：视频结构化、人脸识别、行为分析。
- **IoT AI 应用**：语音唤醒、关键字识别、智能家居等低功耗场景。

### NPU 与 CPU/GPU 的关系

- **CPU**：少而复杂、擅长控制流与通用逻辑（延迟敏感）。
- **GPU**：多而并行、擅长大规模并行通用计算（吞吐敏感），并内置张量核心做 AI 加速。
- **NPU**：面向 AI 的领域专用加速器，用更专门的乘加阵列/低精度支持，在特定 AI 任务上能效最高。

三者通常异构共存于同一系统/SoC：CPU 调度、GPU 图形与通用并行、NPU 专攻 AI。

## 参考

- [Wikipedia: Neural processing unit](https://en.wikipedia.org/wiki/Neural_processing_unit)
- [Wikipedia: AI accelerator](https://en.wikipedia.org/wiki/AI_accelerator)
