# Kirin 9000S

## info

```
CL_PLATFORM_NAME: HUAWEI
CL_PLATFORM_VENDOR: HUAWEI
CL_PLATFORM_VERSION: OpenCL 3.0
CL_PLATFORM_PROFILE: EMBEDDED_PROFILE
CL_PLATFORM_EXTENSION: cl_khr_global_int32_base_atomics cl_khr_global_int32_extended_atomics cl_khr_local_int32_base_atomics cl_khr_local_int32_extended_atomics cl_khr_byte_addressable_store cl_khr_3d_image_writes cl_khr_int64_base_atomics cl_khr_int64_extended_atomics cl_khr_fp16 cl_khr_icd cl_khr_egl_image cl_khr_image2d_from_buffer cl_khr_depth_images cl_khr_subgroups cl_khr_il_program cl_khr_priority_hints cl_khr_throttle_hints cl_arm_printf cl_arm_non_uniform_work_group_size cl_arm_import_memory_dma_buf cles_khr_int64
CL_DEVICE_TYPE: GPU
CL_DEVICE_VENDOR_ID: 268439552
CL_DEVICE_MAX_COMPUTE_UNITS: 4
CL_DEVICE_MAX_WORK_ITEM_DIMENSIONS: 3
CL_DEVICE_MAX_WORK_ITEM_SIZES: [512, 512, 512]
CL_DEVICE_MAX_WORK_GROUP_SIZE: 512
CL_DEVICE_PREFERRED_VECTOR_WIDTH_CHAR: 16
CL_DEVICE_PREFERRED_VECTOR_WIDTH_SHORT: 8
CL_DEVICE_PREFERRED_VECTOR_WIDTH_INT: 4
CL_DEVICE_PREFERRED_VECTOR_WIDTH_LONG: 2
CL_DEVICE_PREFERRED_VECTOR_WIDTH_FLOAT: 4
CL_DEVICE_PREFERRED_VECTOR_WIDTH_DOUBLE: 0
CL_DEVICE_MAX_CLOCK_FREQUENCY: 0
CL_DEVICE_ADDRESS_BITS: 64
CL_DEVICE_MAX_MEM_ALLOC_SIZE: 1073741824
CL_DEVICE_IMAGE_SUPPORT: 1
CL_DEVICE_MAX_READ_IMAGE_ARGS: 16
CL_DEVICE_MAX_WRITE_IMAGE_ARGS: 16
CL_DEVICE_IMAGE2D_MAX_WIDTH: 16384
CL_DEVICE_IMAGE2D_MAX_HEIGHT: 16384
CL_DEVICE_IMAGE3D_MAX_WIDTH: 16384
CL_DEVICE_IMAGE3D_MAX_HEIGHT: 16384
CL_DEVICE_IMAGE3D_MAX_DEPTH: 2048
CL_DEVICE_MAX_SAMPLERS: 16
CL_DEVICE_MAX_PARAMETER_SIZE: 1024
CL_DEVICE_GLOBAL_MEM_CACHELINE_SIZE: 64
CL_DEVICE_GLOBAL_MEM_CACHE_SIZE: 262144
CL_DEVICE_GLOBAL_MEM_SIZE: 4294967296
CL_DEVICE_MAX_CONSTANT_BUFFER_SIZE: 65536
CL_DEVICE_MAX_CONSTANT_ARGS: 128
CL_DEVICE_LOCAL_MEM_SIZE: 32512
CL_DEVICE_PROFILING_TIMER_RESOLUTION: 1000
CL_DEVICE_ENDIAN_LITTLE: 1
CL_DEVICE_NAME: Maleoon 910
CL_DEVICE_VENDOR: HUAWEI
CL_DRIVER_VERSION: 3.0
CL_DEVICE_PROFILE: EMBEDDED_PROFILE
CL_DEVICE_VERSION: OpenCL 3.0
CL_DEVICE_EXTENSIONS: cl_khr_global_int32_base_atomics cl_khr_global_int32_extended_atomics cl_khr_local_int32_base_atomics cl_khr_local_int32_extended_atomics cl_khr_byte_addressable_store cl_khr_3d_image_writes cl_khr_int64_base_atomics cl_khr_int64_extended_atomics cl_khr_fp16 cl_khr_icd cl_khr_egl_image cl_khr_image2d_from_buffer cl_khr_depth_images cl_khr_subgroups cl_khr_il_program cl_khr_priority_hints cl_khr_throttle_hints cl_arm_printf cl_arm_non_uniform_work_group_size cl_arm_import_memory_dma_buf cles_khr_int64
```



## clpeak

    Platform: HUAWEI
    Device: Maleoon 910
    Driver version  : 3.0 (Android)
    Compute units   : 4
    Clock frequency : 0 MHz
    
    Global memory bandwidth (GBPS)
      float   : 32.15
      float2  : 42.77
      float4  : 45.70
      float8  : 23.84
      float16 : 12.32
    
    Single-precision compute (GFLOPS)
      float   : 396.68
      float2  : 408.83
      float4  : 511.05
      float8  : 401.00
      float16 : 383.11
    
    Half-precision compute (GFLOPS)
      half   : 593.50
      half2  : 741.84
      half4  : 850.03
      half8  : 726.74
      half16 : 691.57
    
    No double precision support! Skipped
    
    Integer compute (GIOPS)
      int   : 170.31
      int2  : 177.98
      int4  : 179.60
      int8  : 181.28
      int16 : 181.36
    
    Integer compute Fast 24bit (GIOPS)
      int   : 361.67
      int2  : 390.02
      int4  : 480.25
      int8  : 394.05
      int16 : 375.55
    
    Transfer bandwidth (GBPS)
      enqueueWriteBuffer              : 2.71
      enqueueReadBuffer               : 2.72
      enqueueWriteBuffer non-blocking : 3.11
      enqueueReadBuffer non-blocking  : 3.14
      enqueueMapBuffer(for read)      : 6.44
        memcpy from mapped ptr        : 2.86
      enqueueUnmap(after write)       : 22.21
        memcpy to mapped ptr          : 0.86
    
    Kernel launch latency : 422.99 us