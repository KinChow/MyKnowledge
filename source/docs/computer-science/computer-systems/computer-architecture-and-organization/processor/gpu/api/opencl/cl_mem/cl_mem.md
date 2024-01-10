# cl_mem

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

