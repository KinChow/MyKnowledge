---
domain: computer-science
legacy_first_commit_at: '2025-07-06T20:30:14+08:00'
legacy_path: docs/computer-science/computer-systems/computer-architecture-and-organization/processor/types/gpu/api/opencl/Start-a-OpenCL-project-on-Visual-Studio-using-Nvidia-GPU/Start-a-OpenCL-project-on-Visual-Studio-using-Nvidia-GPU.md
snapshot_sha256: sha256:923fa66765319904ec414347c4505c215e40c7695b512ffc375733415594ea5c
title: Start a OpenCL project on Visual Studio using Nvidia GPU
---
# Start a OpenCL project on Visual Studio using Nvidia GPU

## cuda

下载地址：https://developer.nvidia.com/cuda-downloads



## Visual Studio配置

项目->属性

配置属性->C/C++->常规->附加包含目录

`C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.7\include`

配置属性->链接器->常规->附加包含目录

x86：`C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.7\lib\Win32`

x64：`C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.7\lib\x64`

配置属性->链接器->输入->附加依赖项

`OpenCL.lib`





