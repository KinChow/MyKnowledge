---
aliases: []
confidentiality: public
domain: computer-science
evidence:
- claim: dumpsys 是运行在 Android 设备上的工具，用于提供系统服务信息。
  claim_id: dumpsys-audit-1
  support: direct
  supporting_quotes:
  - evidence_id: evidence-e9bbe59eef86
    exact: dumpsys is a tool that runs on Android devices and provides information
      about system services.
  targets:
  - evidence_id: evidence-e9bbe59eef86
    source_id: android-dumpsys-v2
id: dumpsys
kind: reference
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- android-dumpsys-v2
- working-computer-science-dumpsys
status: published
tags:
- android
- debugging
- memory-analysis
title: dumpsys
updated_at: '2026-09-06'
---
# dumpsys

## 详细章节

### dumpsys

#### meminfo

##### 使用

```shell
adb shell dumpsys meminfo [pkg/pid]
```

* native heap：malloc和new没释放
* stack（栈上内存）：相机退出线程没有join，以及对应的局部变量，函数调用栈
* GL mtrack：申请的OpenCL或OpenGL资源未释放，GPU驱动内存
* EGL mtrack：主要没有释放ION内存
* .so mmap：相机退出so没有dlclose
* unknown：已知有mmap使用映射的匿名内存，全局变量，so的dlopen



##### 相机

常驻内存是相机拍照录像处理完后，退出桌面静止5分钟后，占用的内存



#### 参考

https://developer.android.com/tools/dumpsys?hl=zh-cn
