# Snapdragon 8gen1+

## info

```
CL_PLATFORM_NAME: QUALCOMM Snapdragon(TM)
CL_PLATFORM_VENDOR: QUALCOMM
CL_PLATFORM_VERSION: OpenCL 3.0 QUALCOMM build: commit #16c1863 changeid #I6928db2619 Date: 01/19/23 Thu Local Branch:  Remote Branch:
CL_PLATFORM_PROFILE: FULL_PROFILE
CL_PLATFORM_EXTENSION:
CL_DEVICE_TYPE: GPU
CL_DEVICE_VENDOR_ID: 20803
CL_DEVICE_MAX_COMPUTE_UNITS: 4
CL_DEVICE_MAX_WORK_ITEM_DIMENSIONS: 3
CL_DEVICE_MAX_WORK_ITEM_SIZES: [1024, 1024, 1024]
CL_DEVICE_MAX_WORK_GROUP_SIZE: 1024
CL_DEVICE_PREFERRED_VECTOR_WIDTH_CHAR: 1
CL_DEVICE_PREFERRED_VECTOR_WIDTH_SHORT: 1
CL_DEVICE_PREFERRED_VECTOR_WIDTH_INT: 1
CL_DEVICE_PREFERRED_VECTOR_WIDTH_LONG: 1
CL_DEVICE_PREFERRED_VECTOR_WIDTH_FLOAT: 1
CL_DEVICE_PREFERRED_VECTOR_WIDTH_DOUBLE: 0
CL_DEVICE_MAX_CLOCK_FREQUENCY: 1
CL_DEVICE_ADDRESS_BITS: 64
CL_DEVICE_MAX_MEM_ALLOC_SIZE: 1073741824
CL_DEVICE_IMAGE_SUPPORT: 1
CL_DEVICE_MAX_READ_IMAGE_ARGS: 128
CL_DEVICE_MAX_WRITE_IMAGE_ARGS: 64
CL_DEVICE_IMAGE2D_MAX_WIDTH: 16384
CL_DEVICE_IMAGE2D_MAX_HEIGHT: 16384
CL_DEVICE_IMAGE3D_MAX_WIDTH: 16384
CL_DEVICE_IMAGE3D_MAX_HEIGHT: 16384
CL_DEVICE_IMAGE3D_MAX_DEPTH: 2048
CL_DEVICE_MAX_SAMPLERS: 16
CL_DEVICE_MAX_PARAMETER_SIZE: 1024
CL_DEVICE_GLOBAL_MEM_CACHELINE_SIZE: 64
CL_DEVICE_GLOBAL_MEM_CACHE_SIZE: 262144
CL_DEVICE_GLOBAL_MEM_SIZE: 5973733376
CL_DEVICE_MAX_CONSTANT_BUFFER_SIZE: 65536
CL_DEVICE_MAX_CONSTANT_ARGS: 8
CL_DEVICE_LOCAL_MEM_SIZE: 32768
CL_DEVICE_PROFILING_TIMER_RESOLUTION: 1000
CL_DEVICE_ENDIAN_LITTLE: 1
CL_DEVICE_NAME: QUALCOMM Adreno(TM)
CL_DEVICE_VENDOR: QUALCOMM
CL_DRIVER_VERSION: OpenCL 3.0 QUALCOMM build: commit #16c1863 changeid #I6928db2619 Date: 01/19/23 Thu Local Branch:  Remote Branch:  Compiler E031.38.11.12
CL_DEVICE_PROFILE: FULL_PROFILE
CL_DEVICE_VERSION: OpenCL 3.0 Adreno(TM) 730
CL_DEVICE_EXTENSIONS: cl_khr_3d_image_writes cl_khr_byte_addressable_store cl_khr_depth_images cl_khr_egl_event cl_khr_egl_image cl_khr_fp16 cl_khr_gl_sharing cl_khr_global_int32_base_atomics cl_khr_global_int32_extended_atomics cl_khr_image2d_from_buffer cl_khr_local_int32_base_atomics cl_khr_local_int32_extended_atomics cl_khr_mipmap_image cl_khr_srgb_image_writes cl_khr_subgroups cl_qcom_accelerated_image_ops cl_qcom_android_ahardwarebuffer_host_ptr cl_qcom_android_native_buffer_host_ptr cl_qcom_bitreverse cl_qcom_compressed_image cl_qcom_create_buffer_from_image cl_qcom_dmabuf_host_ptr cl_qcom_dot_product8 cl_qcom_ext_host_ptr cl_qcom_ext_host_ptr_iocoherent cl_qcom_extended_query_image_info cl_qcom_extract_image_plane cl_qcom_filter_bicubic cl_qcom_ion_host_ptr cl_qcom_ml_ops cl_qcom_other_image cl_qcom_perf_hint cl_qcom_priority_hint cl_qcom_protected_context cl_qcom_recordable_queues cl_qcom_reqd_sub_group_size cl_qcom_subgroup_shuffle cl_qcom_vector_image_ops
```



## clpeak

    Platform: QUALCOMM Snapdragon(TM)
    Device: QUALCOMM Adreno(TM)
    Driver version  : OpenCL 3.0 QUALCOMM build: commit #16c1863 changeid #I6928db2619 Date: 01/19/23 Thu Local Branch:  Remote Branch:  Compiler E031.38.11.12 (Android)  
    Compute units   : 4
    Clock frequency : 1 MHz
    
    Global memory bandwidth (GBPS)
      float   : 35.80
      float2  : 36.24
      float4  : 37.66
      float8  : 37.92
      float16 : 24.45
    
    Single-precision compute (GFLOPS)
      float   : 1444.46
      float2  : 1583.69
      float4  : 1464.04
      float8  : 1673.95
      float16 : 1673.69
    
    Half-precision compute (GFLOPS)
      half   : 2232.08
      half2  : 2734.89
      half4  : 3073.10
      half8  : 3192.57
      half16 : 3270.45
    
    No double precision support! Skipped
    
    Integer compute (GIOPS)
      int   : 433.33
      int2  : 379.57
      int4  : 417.71
      int8  : 379.56
      int16 : 352.62
    
    Integer compute Fast 24bit (GIOPS)
      int   : 1336.47
      int2  : 791.06
      int4  : 1241.94
      int8  : 1235.84
      int16 : 1194.04
    
    Transfer bandwidth (GBPS)
      enqueueWriteBuffer              : 13.69
      enqueueReadBuffer               : 15.10
      enqueueWriteBuffer non-blocking : 13.77
      enqueueReadBuffer non-blocking  : 13.49
      enqueueMapBuffer(for read)      : 8414.91
        memcpy from mapped ptr        : 13.05
      enqueueUnmap(after write)       : 5760.42
        memcpy to mapped ptr          : 13.65
    
    Kernel launch latency : 66.59 us