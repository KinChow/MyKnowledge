---
aliases: []
confidentiality: public
domain: computer-science
evidence:
- claim: OpenCL 设备枚举 CL_DEVICE_MAX_WORK_ITEM_SIZES 的值为 0x1005。
  claim_id: limitations-of-local-work-size-and-global-work-size-audit-1
  support: direct
  supporting_quotes:
  - evidence_id: evidence-dd2feaa2ad18
    exact: <enum value="0x1005"        name="CL_DEVICE_MAX_WORK_ITEM_SIZES"/>
  targets:
  - evidence_id: evidence-dd2feaa2ad18
    source_id: khronos-opencl-api-v2
id: limitations-of-local-work-size-and-global-work-size
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- khronos-opencl-api-v2
- web-computer-science-limitations-of-local-work-size-and-global-work-size
- working-computer-science-limitations-of-local-work-size-and-global-work-size
status: published
tags:
- opencl
- gpu
- work-group
- performance
title: Limitations of local work size and global work size
updated_at: '2026-09-06'
---
# Limitations of local work size and global work size


## 一句话结论

global work size 基本任意，而 local work size 受硬件约束；同时 global work size 每一维度必须是 local work size 对应维度的倍数。内核还受 CL_KERNEL_WORK_GROUP_SIZE（各维度乘积上限）限制，这源于线程间分配的硬件资源（本地内存、寄存器）有限。

## 核心概念

- **local work size**：每个维度受设备属性 `CL_DEVICE_MAX_WORK_ITEM_SIZES` 限制（如 [512, 512, 64] 表示 x/y 最大 512、z 最大 64）。
- **CL_KERNEL_WORK_GROUP_SIZE**：内核 local work size 所有维度乘积的最大值（如 256 时 local work size 最大为 [16, 16, 1]）。
- **CL_DEVICE_LOCAL_MEM_SIZE**：设备本地内存大小，同样约束并行线程数。
- 不指定 local work size 时由实现自动选择，但不保证最优。

## 工作机制

1. 设备属性 `CL_DEVICE_MAX_WORK_ITEM_SIZES` 给出各维度 local work size 上限；`CL_DEVICE_LOCAL_MEM_SIZE` 给出本地内存容量。
2. 内核的 `CL_KERNEL_WORK_GROUP_SIZE` 限制 local work size 各维度乘积。
3. 线程使用的本地内存与寄存器数量决定可并行执行的线程数量，硬件资源有限是其根本原因。
4. global work size 每维度需为 local work size 对应维度的倍数；不指定 local 大小时由驱动选择（可能非最优）。

## 示例或代码

- `CL_DEVICE_MAX_WORK_ITEM_SIZES = [512, 512, 64]` → local work size x/y 最大 512，z 最大 64。
- `CL_KERNEL_WORK_GROUP_SIZE = 256` → local work size 最大形如 [16, 16, 1]。

## 常见误区

- 误以为 global work size 有硬件上限——通常 global work size 可以是任意，限制主要在 local work size。
- 误以为 local work size 只受单一数值限制——它受各维度上限与乘积上限双重约束。
- 误以为不指定 local work size 会得到最优性能——驱动选择的 local work size 不保证最优。

## 证据映射

| claim_id | 来源 | 要点 |
| --- | --- | --- |
| limitations-of-local-work-size-and-global-work-size-audit-1 | khronos-opencl-api-v2 | OpenCL 设备信息含 CL_DEVICE_MAX_WORK_ITEM_SIZES（0x1005） |

## 待验证项

无。

## 关联知识

- [[overview-of-opencl]] —— OpenCL 概述与索引空间/工作项。
- [[opencl]] —— OpenCL 执行模型与 NDRange。
- [[opencl-optimizations-list]] —— 工作组大小选择相关优化。


## 详细章节

### Limitations of local work size and global work size

通常，global work size可以是任意，local work size受硬件设备所约束。在谈到local work size和global work size的限制时，一般是说local work size的限制。但是，global work size的每一个维度必须是local work size对应维度的倍数。



如果CL_DEVICE_MAX_WORK_ITEM_SIZES是[512, 512, 64]，这意味着local work size的x和y维度最大为512，z维度最大为64。

CL_DEVICE_MAX_WORK_ITEM_SIZES

CL_DEVICE_LOCAL_MEM_SIZE



对于内核local work size也有限制，CL_KERNEL_WORK_GROUP_SIZE为local work size所有维度乘积的最大值。例如CL_KERNEL_WORK_GROUP_SIZE是256，那么local work size最大为[16, 16, 1]。这是由于在线程之间分配的硬件资源有限，因此线程使用的本地内存和寄存器的数量将限制线程的数量并行执行。



可以不指定local work size，处理时会指定local work size，但是不保证是最优的
