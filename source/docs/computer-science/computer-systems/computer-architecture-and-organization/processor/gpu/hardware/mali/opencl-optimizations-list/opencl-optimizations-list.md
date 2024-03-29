# OpenCL优化列表

## 一般优化

Arm建议进行一般优化，如处理大量数据、使用正确的数据类型以及编译一次内核。



#### 选择最佳处理器

* GPU专为并行处理而设计。
* 应用处理器专为高速串行计算而没计。
* 所有应用程序都包含执行控制功食的部分和执行计算的其他部分。为获得最佳性能，请使用最佳处理器执行任务：
  * 控制和串行功能最好在使用传统语言的应用程序处理器上执行。
  * 在Mali GPU上使用OpenCL实现可并行计算功能。



#### 在应用程序开始时编译一次内核

* 确保在应用程序启动时编译一次内核。这可以显著降低固定开销。



#### 将许多工作项目入队

* 要最大限度地利用所有处理器或着色器核心，必须将许多工作项排队。



#### 处理大量数据

* 您必须处理相对大量的数据才能获得 OpenCL 的优势。这是因为启动 OpenCL 任务的固定开销。不同数据集大小是否有收益取决于运行 OpenCL 代码的处理器。
* 例如，在 GPU 上对单个 640x480 图像执行简单的图像处理可能不是很快，而处理 1920x1080 图像可能收益更大。尝试使用小图像对 GPU 进行基准测试只能测量驱动程序的启动时间。
* 不要通过小数据集的性能来估计更大数据集的性能。应用程序以不同的数据集大小运行基准测试。



### 在 128 位或 16 字节边界上对齐数据

* 在 128 位或 16 字节边界上对齐数据。这可以提高加载和保存数据的速度。如果可以，请在 64 字节边界上对齐数据。这可确保数据均匀地放入 Mali GPU 上的cache中。



### 使用正确的数据类型

* 检查每个变量以查看其需要的范围。
* 使用较小的数据类型有几个优点：
  * 每个周期可以用较小的变量执行更多的操作。
  * 可以在单个循环周期内加载或存储更多内容。
  * 如果将数据存储在较小的容器中，则其可缓存性更高。
* 如果精度并不重要，尽量使用`short`、`ushort`或 `char`来代替 ，而不是`int`。
* 例如，如果对两个相对较小的数字进行相加，则可能不需要`int`. 但是，需要检查是否可能发生溢出。
* 如果需要额外范围就使用`float`。例如，如果需要非常小的或非常大的数字。



### 使用最切合实际的数据类型

* 将图像和其他数据存储为图像或缓冲区：
  * 如果算法可以矢量化，使用缓冲区。
  * 如果算法需要插值或自动边缘clamp，使用图像。



### 不要将缓冲区合并作为优化

* 将多个缓冲区合并为单个缓冲区作为优化不太可能提供性能优势。
* 例如，如果有两个输入缓冲区，您可以将它们合并为一个缓冲区，并使用偏移量来计算数据地址。然而，这意味着每个内核都必须执行偏移计算。
* 最好使用两个缓冲区，并将地址作为一对内核参数传递给内核。



### 使用异步操作

* 尽可能将控制线程和 OpenCL 线程之间使用异步操作。例如：
  * 不要让应用程序处理器等待结果。
  * 确保应用程序处理器在需要 OpenCL 线程的结果之前还有其他操作需要处理。
  * 确保应用程序处理器在执行时不与 OpenCL 内核交互。



### 避免在处理过程中应用处理器和 GPU 交互

* 尽可能先将所有内核放入队列，在最后调用 `clFinish()`。
* 一次或多次调用`clEnqueueNDRange()`后调用`clFlush()` ，并在检查最终结果之前调用`clFinish()`。



### 避免在提交线程中阻塞调用

* 避免 `clFinish()`或`clWaitForEvent()`或提交线程中的任何其他阻塞调用。
* 如果可能，如果要在计算过程中检查结果，请等待异步回调。
* 如果在提交线程中使用阻塞操作，请尝试双缓冲。



### 批处理内核提交

* 从版本 r17p0 开始，OpenCL 驱动程序会对内核进行批处理，这些内核会一起刷新提交给硬件。批处理内核可以显着降低运行时开销和缓存维护成本。例如，当应用程序在独立内核中访问通过`clImportMemoryARM`创建的缓冲区的多个子缓冲区时，这种优化非常有用。
* 应用程序应该以尽可能大的组刷新内核。不过，当 GPU 空闲时，要达到最佳性能，应用程序需要尽早刷新初始批次的内核，以便 GPU 执行与其他内核的排队重叠。



## 内核优化

实验工作组的大小和形状，最大限度地减少线程收敛



### 查询可用于在设备上执行内核的可能工作组大小

```c
clGetKernelWorkgroupInfo(kernel, dev, CL_KERNEL_WORK_GROUP_SIZE, sizeof(size_t)... );
```



### 为了获得最佳性能，请使用 4 到 64 之间（含 4 和 64）以及 4 的倍数的工作组大小

* 如果使用屏障，则工作组规模越小越好。
* 选择工作组大小时，请考虑数据的内存访问模式。
* 找到最佳工作组大小可能违反直觉，因此请测试不同的选项，看看哪一个最快。



### 如果全局工作大小不能被 4 整除，请在边缘使用填充或使用不均匀的工作组大小

* 为了确保全局工作大小可以被 4 整除，请添加更多虚拟线程。
* 或者，您可以让应用程序处理器计算边缘。
* 您可以使用非统一的工作组大小，但这并不能保证比其他选项更好的性能。



### 如果您不确定工作组大小最佳，请将 local_work_size 定义为 NULL

* 驱动程序选择它认为最佳的工作组大小。驱动程序通常选择工作组大小为64。
* 性能可能不是最佳的。



### 如果要设置本地工作大小，请将 reqd_work_group_size 限定符设置为内核函数

* 这在编译时为驱动程序提供了寄存器使用和调整作业大小的信息，以正确适应着色器核心。



### 试验工作组规模

* 如果可以的话，尝试不同的大小，看看是否有任何一个可以带来性能优势。尺寸为 2 的倍数更有可能表现更好。

* 如果您的内核对工作组大小没有偏好，您可以传递`NULL`给`clEnqueueNDRangeKernel()`.



### 如果可能，使用 128 或 256 的工作组大小

* 最大工作组大小通常为 256，但这不适用于所有内核，并且驱动程序建议使用其他大小。工作组大小 64 是保证可用于所有内核的最小大小。
* 如果可能，请使用 128 或 256 的工作组大小。这样可以最佳地利用 Mali GPU 硬件。如果最大工作组大小低于 128，则您的内核可能过于复杂。



### 尝试工作组的形状

* 工作组的形状会影响应用程序的性能。例如，32 x 4 的工作组可能是最佳的大小和形状。
* 尝试不同的形状和尺寸，找到最适合您的应用的组合。



### 检查同步要求

* 一些内核需要工作组来同步工作组内携带屏障的工作项。这些通常需要特定的工作组规模。
* 在不需要工作项之间同步的情况下，工作组大小的选择取决于设备的最有效大小。
* 可以传入`NULL`以使 OpenCL 选择有效的大小。



### 考虑组合多个内核

* 如果有多个按顺序工作的内核，请考虑将它们组合成一个内核。如果组合内核，请注意它们之间的依赖关系。

* 但是，如果数据依赖性不断扩大，请勿组合内核。例如：

  - 如果有两个内核，A和B。

  - 内核 B 的输入由内核 A 的输出。

  - 如果内核 A 与内核 B 合并形成内核 C，则只能向内核 C 输入常量数据，加上之前输入到内核 A 的数据。

  - 内核 C 无法使用内核 A *n -1*的输出，因为不能保证内核 A *n* -1 已被执行。这是因为工作项的执行顺序无法保证。

* 通常这意味着内核 A 和内核 B 的坐标系相同。

* 如果组合内核需要屏障，那么最好将它们分开。



### 避免拆分内核

* 避免分裂内核。如果需要拆分内核，请将其拆分为尽可能少的内核。
* 如果拆分内核能够去除屏障，有时会带来好处。
* 如果您的内核遭受寄存器压力，则拆分内核可能会很有用。



### 检查内核是否很小

* 如果内核很小，请使用单一维度的数据并确保工作组大小是 2 的幂。



### 使用足够数量的并发线程

* 使用足够数量的并发线程来隐藏指令的执行延迟。

* 着色器核心执行的并发线程数取决于内核使用的活动寄存器的数量。寄存器数量越多，并发线程数越少。

* 使用的寄存器数量由编译器根据内核的复杂性以及内核同时拥有多少个活动变量来确定。

* 减少寄存器数量：

  - 尝试减少内核中活动变量的数量。

  - 使用较大的 NDRange，因此工作项较多。

* 对此进行试验以找到适合您的应用程序的方法。您可以使用离线编译器为您的内核生成统计信息来协助完成此操作。



### 优化应用程序的内存访问模式

* 使用具有线性访问和高局部性的数据结构。这些提高了缓存能力，从而提高了性能。



### 根据您的平台调整 cl_arm_thread_limit_hint 的值

* 如果您使用扩展 `cl_arm_thread_limit_hint`，则最佳值因平台而异。根据您的平台调整最佳值。



## 代码优化

### 使用矢量加载和保存

* 要在单个操作中加载尽可能多的数据，请使用矢量加载。这些功能能够一次加载 128 位。对保存数据执行相同的操作。

* 例如，如果要加载 char 值，请使用内置函数`vload16()`一次加载 16 个字节。
* 不要尝试在单次加载中加载超过 128 位。这会降低性能。



### 每个负载执行尽可能多的操作

* 对每个加载的数据元素执行多次计算的操作通常适合在 OpenCL 中进行编程：

  - 尝试重用已加载的数据。

  - 每次加载时使用尽可能多的算术指令。



### 避免与 float 和 int 之间的转换

* float与int之间的转换很昂贵，尽量避免转换。



### 实验一下你的算法执行速度有多快

* 有许多变量决定应用程序的性能。变量之间的一些相互作用可能非常复杂，很难预测它们如何影响性能。

* 试验您的 OpenCL 内核，看看它们的运行速度有多快：

  - 数据类型
    - 尽可能使用最小的数据类型进行计算。例如，如果数据不超过 16 位，则不要使用 32 位类型。

  - 加载存储类型
    - 尝试更改每个工作项处理的数据量。
  - 资料整理
    - 更改数据排列以最大限度地利用处理器缓存。

  - 最大化加载的数据
  - 始终在单个操作中加载尽可能多的数据。使用 128 位宽向量加载来加载每次加载尽可能多的数据项。



### 使用移位而不是除法

* 如果除以 2 的幂，请使用移位而不是除法。
  * 这仅适用于整数。
  * 这仅适用于二的幂。
  * 除法和移位使用不同的负数舍入方法。



### 对标量数据使用矢量加载和保存

* 即使不将数据作为向量处理，也可以对数据数组使用向量加载`VLOAD`指令。这能够使用单个指令加载多个数据元素。128 位矢量加载所需的时间与加载单个字符所需的时间相同。多次加载单个字符可能会导致缓存抖动，从而降低性能。
* 保存数据时，请执行相同的操作。



### 使用内置函数的精确版本

* 通常，内置函数的`half_`或版本不提供额外的性能。`native_`以下函数是例外：

  - `native_sin()`

  - `native_cos()`

  - `native_tan()`

  - `native_divide()`

  - `native_exp()`

  - `native_sqrt()`

  - `half_sqrt()`



### 使用 _sat() 函数代替 min() 或 max()

`_sat()`如果值对于表示来说太高或太低，函数会自动采用最大值或最小值。不需要添加额外的 `min()`代码 `max()`。



### 避免编写使用许多实时变量的内核

* 避免编写使用许多实时变量的内核。使用太多实时变量会影响性能并限制最大工作组大小。



### 不计算内核中的常量

- 使用常量定义。
- 如果这些值仅在运行时已知，则在主机应用程序中计算它们，并将它们作为参数传递给内核。例如，`height-1`。



### 使用离线编译器生成统计数据

* 使用`mali_clcc`离线编译器生成内核统计信息，并检查算术指令和负载之间的比率。



### 使用内置函数

* 许多内置功能都是作为快速硬件指令实现的，使用它们可以获得高性能。



### 谨慎使用缓存

- 每个线程可用的缓存空间量很低，因此必须小心使用。
- 使用尽可能小的数据大小。
- 使用数据访问模式最大化空间局部性。
- 使用数据访问模式最大化时间局部性。



### 使用大量顺序读取和写入

* GPU 上的通用计算会大量使用外部内存。使用大量顺序读取和写入可显着提高内存性能。



## 执行优化

Arm 建议进行一些执行优化，例如优化通信代码以减少延迟。

Arm 还建议：

- 如果您从源代码构建，请将二进制文件缓存在存储设备上。

- 如果您知道应用程序初始化时所使用的内核，请`clCreateKernelsInProgram()`尽快调用以启动最终编译。

  这样做可以确保当您将来使用内核时，它们启动得更快，因为使用了现有的最终二进制文件。

- 如果您使用回调提示处理器继续处理内核执行产生的数据，请确保在刷新队列之前设置回调。

  如果您不这样做，回调可能会在较大一批工作结束时发生，晚于实际完成的工作。



## 减少串行计算的影响

### 使用内存映射而不是内存拷贝来传输数据



### 优化通讯代码

- 要减少延迟，请优化发送和接收数据的通信代码。



### 保持消息小

- 通过仅发送所需的数据来减少通信开销。



### 使用2的幂次大小的内存块进行通信

- 确保用于通信的内存块的大小是 2 的幂，这使得数据更易于缓存。



### 以较少的传输次数发送更多的数据



### 计算值，而不是从内存中读取值

- 简单的计算可能比从内存中读取速度更快



### 在应用处理器上进行串行计算

- 应用处理器针对低延迟任务进行了优化。



### 使用`clEnqueueFillBuffer()`填充缓冲区

- Mali OpenCL 驱动程序包含 `clEnqueueFillBuffer()`，使用它来代替在应用程序中手动实现缓冲区填充。



### 使用`clEnqueueFillImage()`填充图像

- Mali OpenCL 驱动程序包含 `clEnqueueFillImage()`，使用它来代替在应用程序中手动实现图像填充。



## Mali Midgard GPU 特定优化

### 确保内核同时退出

* 分支在 Mali Midgard GPU 上的计算成本很低。这意味着您可以在内核中使用循环，而不会影响性能。您的内核可以包含不同的代码段，但尽量确保内核同时退出。解决这个问题的方法是使用*桶算法*。



### 内核代码尽可能简单

* 这有助于自动矢量化过程。使用循环和分支可能会使自动矢量化变得更加困难。



### 在内核代码中使用向量运算

* 在内核代码中使用向量运算可以帮助编译器将它们映射到向量指令。



### 矢量化您的代码

* Mali Midgard GPU 使用向量执行计算。这些使您能够对每条指令执行多个操作。对代码进行矢量化可以充分利用 Mali Midgard GPU 硬件，因此请确保对代码进行矢量化以获得最佳性能。Mali Midgard GPU 包含 128 位宽向量寄存器。笔记Midgard 编译器可以自动向量化一些标量代码。



### 增量矢量化

* 以增量步骤进行矢量化。例如，开始一次处理一个像素，然后是两个，然后是四个。



### 避免处理单一值

* 避免编写对单字节或其他小值进行操作的内核。编写适用于向量的内核。



### 使用 128 位向量

* 128 位的向量大小是最佳的。大于 128 位的向量大小被分成 128 位部分并单独进行操作。例如，添加两个 256 位向量所需的时间是添加两个 128 位向量所需的时间的两倍。您可以使用小于 128 位的向量大小，不会出现问题。使用大于 128 位的向量的缺点是它们会增加代码大小。增加的代码大小会使用更多的指令缓存空间，这会降低性能。



## Mali Bifrost和Valhall GPU特定优化

### 确保`if`语句和循环中的线程都采用相同的分支方问

### 避免过度使用寄存器

### 向量化8位和16位操作

### 不需要向量化32位操作

### 使用128位加载或存储操作

### 如果四通道中的所有线程都从同一缓存线加载，则加载和存储操作会更快

### 尽可能使用32位算术代替64位

### 使用細粒度共享虚拟内存

### 尝试在执行引擎和负载存储单元的使用上取得良好的平衡



## 参考

https://developer.arm.com/documentation/100614/0314/OpenCL-optimizations-list