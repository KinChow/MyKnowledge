# OpenCL优化指导

## 避免GPU/CPU ping-pong

避免ping-poing，GPU与CPU运行时并行最好

* 如果可能的话，在调用`clFinish()`之前先将所有内核排队

* 在一个或多个`clEnguqueNDRange()`调用后调用`clFlush()`；在检查最终结果之前，调用`clFinish()`。

  * 避免无休止地调用`clEnqueueNDRange()`，这最终会导致OOM

  * 目前，不支持自动冲洗

* 如果您只想在管道中间检查结果，调用`clWaitForEvent()`
* 不要让应用程序处理器等待结果
* 确保应用程序处理器在需要GPU结果之前有其他操作要处理
* 确保应用程序处理器在执行时不需要与OpenCL内核交互



## 找到瓶颈

主机应用程序或内核执行

* 避免内存拷贝
* 避免cache flush



哪个pipe重要？

* 其他pipe的操作很少或没有运行时间成本



保存操作或保存寄存器

我们能处理多少寄存器压力，和隐藏延迟



使用cache的程度如何？

* 指令在LS管道自旋等待数据吗？



如果带宽有限，合并kernel

* 避免重新加载数据



如果寄存器数量有限，拆分kernel

* 编译器更容易做好工作



如果加载/存储能力有限，减少加载/存储

* 计算负责的表达式，而不是使用查找表



如果算术能力有限，少做算术计算

* 表格函数
* 使用多项式近似，而不是特殊函数





## 最小化数据访问

每个线程可用的缓存空间很少，所以要小心使用

* 读和写都是通过L1缓存



通常缓存使用

* 尽可能使用最小数据大小
* 设计访问模式时，最大限度提高空间和时间位置



GPGPU会加重使用外部内存

* 更倾斜使用大量连续读和写
* 显著提升DDR内存性能





## 最小化数据共享

在Mali，local和global内存区域之间没有物理差异

* 两者都映射到系统RAW，因此具有相同的底层性能



共享资源很昂贵

* 工作项内的数据共享都是免费的：只是寄存器访问
* 工作组内的数据共享相对不免费：大概率在L1缓存使用加载/存储指令
* 跨工作组的数据共享更不免费：可能在L2缓存使用加载/存储指令



Mali的L1原子实现是在L1内存系统

* 原子在L1内存中命中是单周期的
* 原子在L1中缺失需要再L2获取





## 通用指导

* 尽可能使用`clFlush()`而不是`clFinish()`
* 使用`clWaitForEvents()`或回调进行同步
* 不要使用任何带有阻塞调用的`clEnqueueMap()`操作
* 使用`CL_MEM_ALLOC_HOST_PTR`避免复制`clAllocBuffer()`的内存
* 在CPU和GPU之间进行更好的并行化
* 确保每个核心上都有足够的线程
* 避免使用`cl_arm_import_memory`扩展从外部存储器复制内存





## Tyrm/Natt 指导

* 使用整型乘法需要注意，可能会类型溢出
  * 尽量使用浮点类型
* 线程数量
  * 寄存器数量 >= 32，最大1024线程
  * 寄存器数量 > 32 & <= 64，最大512线程
* local workgroup size至少一个warp大小
* 在加载/存储单元使用texture unit
* 使用点乘扩展





## 编译器优化

编译选项

* `-cl-arm-non-uniform-work-group-size`：允许执行非统一的工作组
  * 对于CL 1.2，当global work size不是local work group size的倍数时非常有用
* `-cl-fast-relaxed-math`：启动`-cl-finite-math-only`和`-cl-unsafe-math-optimizations`
  * 优化零操作
  * `power()`性能提升
* `-cl-unsafe-math-optimizations`：启动所有不安全的浮点优化
* `-fkernel-unroller[=<arg>]`