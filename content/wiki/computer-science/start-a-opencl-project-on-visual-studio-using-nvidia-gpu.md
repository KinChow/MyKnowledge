---
aliases: []
confidentiality: public
domain: computer-science
evidence:
- claim: OpenCL API 的设备信息定义包含 `CL_DEVICE_MAX_WORK_ITEM_SIZES` 属性。
  claim_id: start-a-opencl-project-on-visual-studio-using-nvidia-gpu-audit-1
  support: direct
  supporting_quotes:
  - evidence_id: evidence-dd2feaa2ad18
    exact: <enum value="0x1005"        name="CL_DEVICE_MAX_WORK_ITEM_SIZES"/>
  targets:
  - evidence_id: evidence-dd2feaa2ad18
    source_id: khronos-opencl-api-v2
id: start-a-opencl-project-on-visual-studio-using-nvidia-gpu
kind: reference
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- khronos-opencl-api-v2
- working-computer-science-start-a-opencl-project-on-visual-studio-using-nvidia-gpu
status: published
tags:
- opencl
- visual-studio
- nvidia
- cuda
title: Start a OpenCL project on Visual Studio using Nvidia GPU
updated_at: '2026-09-06'
---
# Start a OpenCL project on Visual Studio using Nvidia GPU

## 详细章节

### Start a OpenCL project on Visual Studio using Nvidia GPU

#### cuda

下载地址：https://developer.nvidia.com/cuda-downloads



#### Visual Studio配置

项目->属性

配置属性->C/C++->常规->附加包含目录

`C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.7\include`

配置属性->链接器->常规->附加包含目录

x86：`C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.7\lib\Win32`

x64：`C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.7\lib\x64`

配置属性->链接器->输入->附加依赖项

`OpenCL.lib`
