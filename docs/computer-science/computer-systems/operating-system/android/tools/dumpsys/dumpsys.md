# dumpsys

## meminfo

### 使用

```shell
adb shell dumpsys meminfo [pkg/pid]
```

* native heap：malloc和new没释放
* stack（栈上内存）：相机退出线程没有join，以及对应的局部变量，函数调用栈
* GL mtrack：申请的OpenCL或OpenGL资源未释放，GPU驱动内存
* EGL mtrack：主要没有释放ION内存
* .so mmap：相机退出so没有dlclose
* unknown：已知有mmap使用映射的匿名内存，全局变量，so的dlopen



### 相机

常驻内存是相机拍照录像处理完后，退出桌面静止5分钟后，占用的内存



## 参考

https://developer.android.com/tools/dumpsys?hl=zh-cn

