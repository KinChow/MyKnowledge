---
aliases: []
confidentiality: public
domain: computer-science
evidence:
- claim: 该扩展通过 `clImportMemoryARM` 支持把外部内存直接导入 OpenCL。
  claim_id: cl-mem-claim-1
  support: direct
  supporting_quotes:
  - evidence_id: evidence-e481cd1b0c45
    exact: "This extension adds a new function that allows for direct memory import
      into\n    OpenCL via the clImportMemoryARM function."
  targets:
  - evidence_id: evidence-e481cd1b0c45
    source_id: web-computer-science-cl-mem
- claim: 如果暴露了 `cl_arm_import_memory_host` 扩展字符串，就可以导入普通用户态分配的内存，例如 `malloc`。
  claim_id: cl-mem-claim-3
  support: direct
  supporting_quotes:
  - evidence_id: evidence-19828ea5873f
    exact: "If the extension string cl_arm_import_memory_host is exposed then importing\n
      \     from normal userspace allocations (such as those created via malloc) is\n
      \     supported."
  targets:
  - evidence_id: evidence-19828ea5873f
    source_id: web-computer-science-cl-mem
- claim: 如果暴露了 `cl_arm_import_memory_protected` 扩展字符串，就可以使用 `CL_IMPORT_TYPE_PROTECTED_ARM`
    导入受保护内存。
  claim_id: cl-mem-claim-4
  support: direct
  supporting_quotes:
  - evidence_id: evidence-bab64f7cf6c5
    exact: "If the extension string cl_arm_import_memory_protected is exposed then\n
      \     using CL_IMPORT_TYPE_PROTECTED_ARM in the list of <properties> is\n      allowed."
  targets:
  - evidence_id: evidence-bab64f7cf6c5
    source_id: web-computer-science-cl-mem
id: cl-mem
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-cl-mem
- working-computer-science-cl-mem
status: published
tags:
- opencl
- memory
- gpu
- mali
- adreno
title: cl_mem
updated_at: '2026-09-06'
---
# cl_mem


## 一句话结论

OpenCL 内存（cl_mem）的分配方式决定性能：粗粒度共享（CL_MEM_ALLOC_HOST_PTR + Map/UnMap）、细粒度共享（SVM/内存一致性平台）、以及 ARM/Qualcomm 的导入扩展（clImportMemoryARM、CL_MEM_EXT_HOST_PTR_QCOM）等，各有性能、适用范围与限制，应根据平台与共享粒度选择。

## 核心概念

- **CL_MEM_ALLOC_HOST_PTR**：clCreateBuffer 申请的内存分配在同一内存空间，GPU/CPU 均可访问；粗粒度共享，需 Map/UnMap 控制访问归属权。
- **SVM（clEnqueueSVMMap）**：细粒度共享；内存一致性平台上无需 Map/UnMap，性能最好；OpenCL 2.0+。
- **clImportMemoryARM**：把外部内存直接导入 OpenCL（CL_IMPORT_TYPE_HOST_ARM 导入 malloc 内存；CL_IMPORT_TYPE_PROTECTED_ARM 导入 dma_buf/ION 内存）；免 Map/UnMap；仅 Mali GPU，接口调用轻量耗时。
- **CL_MEM_EXT_HOST_PTR_QCOM**：Adreno GPU 访问 ION 内存，本质映射到已申请内存，内存申请耗时最小。
- **CL_MEM_USE_HOST_PTR**：兼容性最强但性能最差（两块物理空间 + 驱动层隐式同步）。

## 工作机制

1. CL_MEM_ALLOC_HOST_PTR 分配在同一内存空间；UnMap 需与 CPU 同步后才可被 CPU 访问，对性能有影响。
2. SVM 在内存一致性平台上无需 Map/UnMap，细粒度共享仍有较好性能；非一致性平台仍需 Map/UnMap。
3. clImportMemoryARM 把外部内存直接导入 OpenCL，支持 GPU 侧访问 malloc 或 dma_buf/ION 内存，免 Map/UnMap 操作。
4. CL_MEM_USE_HOST_PTR 分配在物理上两块空间，驱动层完成隐式同步，占用带宽。

## 示例或代码

（各方案的对比表格见 ## 详细章节。）

## 常见误区

- 误以为 CL_MEM_USE_HOST_PTR 性能好——实际性能最差，仅作兼容性补充。
- 误以为所有平台都适配 clImportMemoryARM——它只适用于 Mali GPU，且芯片供应商可能未适配。
- 误以为 SVM 在所有平台都无需 Map/UnMap——非一致性平台仍需 Map/UnMap。

## 证据映射

| claim_id | 来源 | 要点 |
| --- | --- | --- |
| cl-mem-claim-1 | web-computer-science-cl-mem | clImportMemoryARM 直接内存导入 OpenCL |
| cl-mem-claim-3 | web-computer-science-cl-mem | cl_arm_import_memory_host 暴露后可导入 malloc 等用户态分配 |
| cl-mem-claim-4 | web-computer-science-cl-mem | cl_arm_import_memory_protected 暴露后可用 CL_IMPORT_TYPE_PROTECTED_ARM |

## 待验证项

无。

## 关联知识

- [[opencl]] —— OpenCL 内存模型。
- [[optimizing-opencl-for-mali-gpus]] —— Mali 内存分配优化。
- [[overview-of-opencl]] —— OpenCL 概述。


## 详细章节

### cl_mem

#### 对比

OpenCL通过clCreateBuffer申请内存，不同配置属性会有不同性能。

| 描述                                                         | 优势                                                         | 限制                                                         | 适合场景                                                     |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| clCreateBuffer申请内存时配置属性CL_MEM_ALLOC_HOST_PTR，申请的内存分配在同一内存空间，可以被GPU和CPU访问 | 性能较好<br>OpenCL 1.0以上版本<br>适用Mali和Adreno GPU       | 仅支持GPU申请的内存可以被CPU访问，反之不行<br>需要使用Map和UnMap控制内存的访问归属权<br>UnMap需要与CPU同步后才可被CPU访问，对性能有影响 | 适合允许OpenCL接口申请内存，且粗粒度的内存共享               |
| clEnqueueSVMMap申请内存，且平台满足内存一致性                | 性能最好<br/>不需要调用Map和UnMap，在细粒度共享内存时依然有较好的性能<br/>适用Mali和Adreno GPU | 仅支持GPU申请的内存被CPU访问，反之不行<br/>内存一致性平台<br/>支持OpenCL 2.0以上版本 | 使用允许使用OpenCL接口申请内存，且细粒度的内存共享           |
| clEnqueueSVMMap申请内存，平台不满足内存一致性                | 性能最好<br/>适用Mali和Adreno GPU                            | 仅支持GPU申请的内存被CPU访问，反之不行<br>需要调用Map和UnMap<br>支持OpenCL 2.0以上版本 | 使用允许使用OpenCL接口申请内存，且细粒度的内存共享           |
| 基于CL_IMPORT_TYPE_HOST_ARM扩展，适用clImportMemoryARM导入CPU使用malloc申请的内存 | 性能较好<br/>支持GPU侧使用malloc申请的CPU内存<br/>不需要Map和UnMap操作 | clImportMemoryARM接口调用轻量耗时<br>只适用于Mali GPU<br>虽然是ARM定义的接口，芯片供应商可能没有适配该扩展 | 适合在Mali GPU侧访问malloc申请的内存，支持细粒度的内存共享   |
| 基于CL_IMPORT_TYPE_PROTECTED_ARM扩展，适用clImportMemoryARM导入CPU使用malloc申请的内存 | 性能较好<br>支持GPU侧使用dma_buf或ION申请的CPU内存<br>不需要Map和UnMap操作 | clImportMemoryARM接口调用轻量耗时<br>只适用于Mali GPU<br>虽然是ARM定义的接口，芯片供应商可能没有适配该扩展 | 适合在Mali GPU侧访问dma_buf或ION申请的内存，支持细粒度的内存共享 |
| 基于CL_MEM_EXT_HOST_PTR_QCOM扩展，适用clCreateBuffer申请内存 | 性能最好<br>内存申请耗时最小（本质是映射到已经申请好的内存） | 只适用于Adreno GPU<br>OpenCL 1.1以上版本，且支持cl_qcom_ion_host_ptr扩展 | 使用在Adreno GPU侧访问ION申请的内存，支持细粒度的内存共享    |
| clCreateBuffer申请内存时配置属性CL_MEM_USE_HOST_PTR，申请的内存分配在两块物理空间，但驱动层会完成隐式同步 | 兼容性强，OpenCL基础接口<br>支持GPU侧使用malloc申请的内存<br>支持Mali和Adreno GPU | 性能最差<br>clCreateBuffer执行时间长<br>隐式同步占用带宽<br>除非兼容性要求，否则不使用该方案 | 必要场景的补充                                               |



#### 参考

ARM：https://www.khronos.org/registry/cl/extensions/arm/cl_arm_import_memory.txt

Qualcomm：https://registry.khronos.org/OpenCL/extensions/qcom/cl_qcom_android_native_buffer_host_ptr.txt
