# ARM体系结构与现代处理器设计

* ARM体系结构简介
    *   ARM基本简介
    *   ARM体系结构介绍
    *   ARM处理器模式
    *   ARM指令集
    *   ARM处理器寄存器
* ARM周边组件简介
    *   中断
    *   cache
    *   Memory model
    *   总线协议
    *   MMU
* ARM处理器核典型结构
* ARM多核处理器系统设计



## ARM体系结构简介

### ARM基本简介

ARM（Advanced RISC Machines）

* 一家公司
* —种微处理器架构
    * A (Application)
        * 针对高性能计算
        * 支持MMU
        * 支持A64/A32/T32指令集
        *  手机、Sever
    *   R (Real-time)
        *   针对实时操作处理
        * 支持MPU
        * 支持A32和T32指令集
        *   嵌入式实时处理系统
        *   电子制动系统，工业控制领域
    * M (Microcontroller)
        *  针对低功耗、低成本系统
        *   支持T32变种的指令集  
        * iot



### ARM体系结构介绍

体系结构（Architecture）：为了给不同的处理器提供更通用的编程模型，定义不同的Architecture，符合相同Architecture的处理器具有相同的编程模型，ARM已经定义的Architecture有ARMv4、ARMv5、ARMv6M、ARMv7M、ARMv7AR、ARMv8、ARMv8.1、ARMv8.2、ARMv9...



#### 计算机体系结构（Computer Architecture）

*   ISA(Instruction Set Architecture)
    *  软件与硬件的接口
    *   寄存器
    * Memory模型、页表管理、寻址模式
    *  异常模型
    *   指令集
*  微架构
*  逻辑实现



#### 现代计算机系统的抽象层次

| 类型 | 层次                  | 开发者     |
| ---- | --------------------- | ---------- |
| 软件 | 应用                  | 程序员     |
| 软件 | 算法                  | 程序员     |
| 软件 | 编程语言              | 程序员     |
| 软件 | 操作系统/虚拟机       | 程序员     |
|      | 指令集体系结构（ISA） | 架构师     |
| 硬件 | 微架构                | 电子工程师 |
| 硬件 | RTL                   | 电子工程师 |
| 硬件 | 电路                  | 电子工程师 |
| 硬件 | 设备器件              | 电子工程师 |



#### ARM体系结构定义了ARM处理器的基本特征

* The programmers model（编程模型，处理器模式）
* The instruction set（指令集）
* System configuration（系统配置）
* Exception handling（中断处理）
* The menory model（存储模型）
不同版本的体系结构定义了不同的系统特性和系统行力：
* 采用几级cache, cache的大小寄存器的功能定义
* 定义一些扩展功能：浮点运算硬件支持、SIMD支持



#### 结构演进



#### 路标



### ARM处理器模式

  AArch64支持4个异常等级，2种安全状态

* EL0~EL3：EL0特权等级最低，EL3特权等级最高
* 安全与非安全
* EL2与EL3是可选的：若不需要安全和虚拟化可以不实现EL2与EL3



AArch32的异常模型类似于ARMv7-A



ARMv8-A支持2种执行状态：

* AArch32
    * 兼容ARMv7-A架构
    * 13个32-Bit的通用寄存器、1个32-Bit PC寄存器、1个32-Bit LR寄存器
    * 32个64-bit的向量SIMD和标量浮点寄存器
    * 支持A32与T32指令集
    * 传统的ARM异常模型（USER/SYS/FIQ/IRQ/SVC/UND）
    * 虚拟地址储存在32-Bit寄存器
* AArch64
    * 31个64-Bit通用寄存器（X0~X30），X30被用作LR寄存器
    * 1个64-Bit的PC/SP/ELR寄存器
    * 32个128-bit的向量SIMD和标量浮点寄存器支持A64指令集
    * 新的异常模型（EL0~EL3）
    * 虛拟地址储存在64-Bit寄存器



执行状态只有在异常进入或退出的时候才能改变

*  移动到低的EL，执行状态可以维持或切换到AArch32
*  移动到高的EL，执行状态可以维持或切换到AArch64
*  异常进入时，EL可以维持或升高
* 异常退出时，EL可以维持或降低



### ARM指令集

ISA: instruction set architecture -> 指令，集合，架构

ISA在软件和硬件人员之间提供了一个抽象层

* 处理器设计者：依据ISA来设计处理器
* 处理器使用者（写编译器的厉害程序员）：依据ISA可以知道软件抽象对应使用哪些指令，遵循哪些规范



#### ISA需要能说明白什么东西？

* 寄存器结构  
* 寻址模式
* 操作数的类型和大小
* 操作指令类型
* ISA的编码长度
* 载入存储体系



#### 优秀的ISA需要具有的特征

*  可持续用于很多机器上 （protability）
* 可以适用于多个领域 （generality）
* 对上层提供方便的功能 （convenient functionality）
* 可以由下层有效的实现 （efficient implementation）



#### 指令集基本分类

*   数据处理指令
    *   算术和逻辑运算
    *   移动和移位操作
    *   条件指令乘除指令
*   内存访问指令
*   Barrier指令
*   跳转类指令
*  系统指令
*  调试及其他指令



##### 数据处理指令

* 一旦数据放到register 中后，有很多的指令可以处理它
    *   可以是多个register之间的处理，也可以是一个register和一个立即数
    *   这些指令不会去访问内存
*   算术和逻辑运算指令包括：
    *   Arithmetic operations（ADD,SUB等）
    *   Logical operations（AND, BIC,EOR等）
    *   Data move（MOV）
    *   Comparison（CMP等）
* 移位指令：
    * LSL： 逻辑左移
    * LSR： 逻辑右移
    * ASR：算术右移
    * ROR：向右旋转
*   条件指令：
    * EQ/NE/LS等
    * CSEL



```c++
ADD W0, W1, W2, ISL #3 // WO = W1 + (W2 < 3) 
SUB w2, w1, #1 // r=r- 1 
ADD w1, w1, #2 // r=г + 2 
BIC X0, X0, X1
MOV X0, X1 // Сору X1 tо Х0
CMP W3, W4 // Set flags based on W3 - W4 
CMP w0, #0 // if (1 = 0)
CSEL w2, w1, w2, EQ // select between the two results
```



##### 内存访问指令

* AArch64是一个 load - store 体系
* 通过load store指令来让内存和registers之间的数据传输
    *   指定地址，数据大小（size），源或者目的寄存器
*  允许非对齐操作
    * 只有normal memory的时候允许
    *   可以配置成产生fault
    *   不支持exclusive accesses, load acquire, store release
*   Register load/store
    *   `LDR Rn, {addr)`
    *   `STR Rn, {addr}`
* PRFM：预取指令



```c++
LDR X0, [X1] // 从X1 中的地址加载
LDR X0, [X1, #8] // 从地址 X1+8 加载
LDR X0, [XL, X2] // 从地址 X1+X2 加载
LDR X0, [X1, X2, LSL, #3] // 从地址 X1+(X2<<3)加载
LDR X0, [X1, W2, SXTW] // 以地址 X1 + sign_extend(W2)加载
LDR X0, [X1, W2, SXTW, #3] // 从地址 X1 + (sign_extend(W2)<<3)加载
```





##### barrier

* DMB
    * 数据Memory屏障
    * 仅当所有在它前面的存储器访问操作都执行完毕后，才提交（commit）在它后面的存储器访问操作
* DSB
    * 数据同步屏障，比DMB严格
    * 仅当所有在它前面的存储器访问操作都执行完毕后，才执行在它后面的指令
* ISB
    * 指令同步屏障，最严格
    * 清洗流水线，以保证所有它前面的指令都执行完毕之后，才执行它后面的指令





##### control flow指令

* Branch instructions
    *   `B offset`（程序相关分支向前或向后128MB，有条件的比如B.EQ是1MB范围）
    *  `BL offset`（和B类似，但是返回地址存储在X30中，并提示分支预测逻辑这是一个函数调用）
    *  `BR Xm`（绝对跳转到Xm）
    *  `BLR Xm`（和BR类似，返回地址存储在X30中，提示分支预测逻辑这是一个函数调用）
    *   `RET`（作为BR，提示分支预测逻辑这是一个函数返回，默认返回X30中地址）
* Conditional Branch
    * `CBZ Xn,label` 当Xn=0的时候跳转到label(+/-1 MB range)
    * `CBNZ Wn, label` 当Xn！=0的时候跳转到label(+/-1 MB range)





##### system control指令

三个异常处理指令

* `SVC #imm16` （enter EL1，允许调用kernel）
* `HVC #imm16` （enter EL2，允许调用hypervisor）
* `SMC #imm16` （enter EL3，允许调用最高安全等级）
* 要从异常中返回，使用ERET





##### 调试指令及其他指令

* `BRK #imm16`
    * 进入monitor mode debug
    * 如果monitor mode debug没有使能，则指令UNDEF
* `HLT #imm16`
    * 如果halt mode debug没有使能，则指令UNDEF
* `Breakpoint`：通常用作debug用途
* `NOP`：单纯空执行指令
*  `YIELD`：指示这个线程重要性不高，提高SMI,SMP系统的整体性能
*   `WFE`：wait for event
*   `WFI`：wait for interrupt
*   `SEV`：send evnet
*   `SEVL`：send event local
* 其他浮点，NEON，加密指令等



### ARM处理器寄存器

#### AArch64通用寄存器（GPR）

31个64-Bit通用寄存器

* 32-Bit格式：W0~W30-Xn［31:0］
* 64-Bit格式：X0 ~ X30



32个128-Bit SIMD/浮点寄存器

* 128-Bit格式：Qn
*   64-Bit格式：Dn
*   32-Bit格式：Sn
*  16-Bit格式：Hn
* 8-Bit格式：Bn



程序调用标准

* X0-X7：参数/结果寄存器，被调用的子程序返回前无需恢复
*   XR（X8）：间接结果末知寄存器
*   X9-X15： 临时寄存器，如果使用需要保存现场、返回时需要恢复现场
*   IP0/IP1：内部程序调用临时寄存器；如果使用需要保存现场、返回时需要恢复现场
*   PR：平台寄存器
*   X19-X28：被保存的寄存器。被调用者（函数内部在起始地方保存寄存器，在结束时，恢复寄存器
* FP：帧指针，保存函数栈的基地址
* LR：链接寄存器，执行链接操作的时候存储返回地址



子程序调用

* 参数通过X0～X7传递
* 返回值通过X1～X1
* 必须预留：X19～X29
* 可以占用：X0～X18
* 返回地址：X30(LR)



#### AArch64特殊寄存器（SPR）

* 零寄存器：XZR/WZR
    * 读0，与无效
* PC寄存器
    * 非通用寄存器，指示系统运作所处的PC指针
* Link寄存器
    * X30:
        * 由分支链接指令（BL/BLR）更新
        * RET指令从子程序返
    * ELR_ELn:
        * 异常入口更新
        * ERET指令从异常返回，保存异常的返回地址
*  栈指针寄存器：
    * SP_ELn
    * 非通用寄存器
    * 栈指针必须128-Bit对齐
*  程序状态寄存器：SPSR （saved process status register）



| 处理器状态 PSTATE | Description                                           |
| ----------------- | ----------------------------------------------------- |
| Field             | ALU条件标志：负、零、进位、溢出                       |
| N,Z,C and V       | 当前执行状态：AArch64/AArch32                         |
| nRW               | 异常掩码：Debug、SError、IRQ、FIQ                     |
| DAIF              | SP寄存器选择：EL0只能使用SP_EL0，在其他EL可以选择使用 |
| SP                | SP_EL0还是SP_ELX                                      |
| EL                | 当前的EL等级：EL0~EL3                                 |
| IL                | 非法执行状态                                          |
| SS                | 软件单步调试                                          |



#### 系统配置寄存器

* AArch64系统配置通过系统寄存器控制
* 寄存器的名称告诉你可以从中访问的最低的异常级别
    * TTBR0_EL1：能够被EL1、EL2和EL3访问
    * TTBR0_EL2：能够被EL2和EL3访问
* 使用MSR和MSR访问寄存器



```c++
MRS Xt, <system register> // Move <system_register> to Xt

MSR <system register>, Xt // Move Xt to <system register>
```



#### 系统寄存器

* CTLR_ELn (System Control Register)
    *   Controls architectural features, for example MMU, caches and alignment checking
*   ACTLR_ELn (Auxiliary Control Register)
    * Controls processor specific features
* SCR_EL3 (Secure Configuration Register)
    *   Controls secure state and trapping of exceptions to EL3
*   HCR_EL2 (Hypervisor Configuration Register)
    *   Controls virtualization settings, and trapping of exceptions to EL2
*   MIDR_EL1 (Main ID Register)
    *   The type of processor the code is running on (e.g. part number and revision)
*   MPIDR_EL1 (Multiprocessor Affinity Register)
    *   The core and cluster IDs, in multi-core/cluster systems
*   CTR_EL0 (Cache Type register)
    *   Information about the integrated caches (e.g. the size)



## ARM周边组件简介

### 中断

####  为什么要有中断

*   中断：一种通知交互机制
*  轮询 VS中断



#### 中断类型

* 同步异常（可能是操作系统正常运行的一部分）
    * 系统调用：SVC、HVC、SMC
    * SP和PC未对齐
    * 未分配的指令
    * 页表翻译中止
    * Debug
* 异步异常
    * IRQ
    * FIQ（FIQ优先级高于IRQ）
    * SError
        *   Bus Error: Decode Error, Slave Error, Data Poision
        *   Internal Cache Error: ECC Fault
        * nSEI、nREI输入有效



#### 异常处理寄存器

* ESR_ELn包含了异常原因及相关信息
    * 只能记录同步异常和SError的信息，不包含IRQ和FIQ
    * EC (Exception Class)
    * IL (Instruction Length)
    * ISS (Instruction Specific Syndrome)
* FAR_ELn
    * 记录了产生异常的虚拟地址
* ELR_ELn
    * 存储异常的返回地址，用于ERET返回时写入PC



#### 异常执行与退出

* 当异常进入
    * PSTATE值保存到SPSR_ELn中
    * PC返回地址存入ELR_ELn
    * 配置PSTATE的值
        * 修改EL等级
        * 选择SP
        * 屏蔽中断
    * 用异常原因更新ESR_ELn
    * 跳转异常向量表VBAR_Eln
    * 执行异常服务程序
* 当异常返回
    * 从SPSR_ELn中恢复PSTATE
    * 从ELR_ELn中恢复PC



#### 异常向量表

* 每个EL都有自己的异常向量表，除了EL0
* 异常向量表入口虚拟地址寄存器
    * VBAR_EL3、VBAR_EL2、VBAR_EL1
* 异常向量表入口只有32条指令



### cache

* 性能要求越来越高，CPU运算速率越来越高，内存读写速度匹配不上
* 性能要求越来越高，多核的实现成为必然
* Memory的访问延时要求越来越低
    * 通用寄存器、cache、ddr



#### 如何工作

* 时间局部性：将最近被访问的信息项放在离处理器较近的地方。
* 空间局部性：将包括临近存储字的数据块一起移到离处理器较近的存储器。
* 缓存工作的原理，就是“引用的局部性〞



#### 地址映射

一般来说，主存容量远大于Cache的容量。因此，当要把数据从主存调入Cache 时，就有个如何放置的问题。这就是映射规则所要解决的。映射规则有以下三种。

* 直接相连
* 全相连
* 组相连



#### Coherence and Consistency

内存系统行为的2个不同的方面：

* Coherence：定义一次读操作可以返回哪些位，什么值
* Consistency： 确定读取何时返回写入值





### Memory model

Sequential Consistency Memory Model

Weakly-ordered Memory Model

为了提升访存性能，X86和ARM都没有采用Sequential Consistency Memory Model

添加Data Memory Barrier指令来保证读取flag与读取data之间的顺序。



#### 类型

* Normal
    * 代码、数据
    * 重排序（不保证访问顺序，有保序需求要使用Barrier）
    * 合井
    * 投机访问（分支预测、数据乱序加载、投机的Cacheline Fill）
    * 不限制对空间的重复访问，多次读取返回相同的值，多次写最后一次写生效
    * Normal和Device之间的访问也不保证顺序
* Device
    * 外设使用，访问可能有副作用
    * 限制对空间的访问顺序，但ARMv8定义了一个Device属性，可以不保序限制对空间的操作是否可以合并，但ARMv8定义了一个Device属性可以merge
    * 对空间的多次访问行为可能不一致，例如FIFO类型的外设、读/写清之类的寄存器访问可能产生副作用，因为对处理器可执行的优化有更多限制
    * 不允许投机访问
* 其他的属性
    * Cacheable
    * Shareable
    * 访问权限
    * 执行权限



#### 设备类型和ordering

Device-nGnRnE、Device-nGnRE、Device-nGRE、Device-GRE

* Gathering（G/nG）：确定多个访问是香可以在总线出口上Merge成一个传输
* Reordering（R/nR）：确定对同一个device操作是否可以乱序
* EWA（E/nE）：确定对memory的访问是否可以Bufferable
Device-nGnRnE是最严格的Device属性



#### 弱保序模型

* 程序并非按照顺序进行最后的执行，软件必须要显示的插入保序操作来保证顺序
* ARMv8-A采用弱序内存模型，指令可乱序执行，提升性能
* 有什么样的指令来保证顺序
    *   FENCE instructions （barrier等）
    *   Atomic指令



| 乱序源              | 原因                                                         |
| ------------------- | ------------------------------------------------------------ |
| 多流水线技术        | 每个核，每个周期可以同时执行多条指令=>具体先后顺序的指令，可能同时执行 |
| 乱序执行            | 对于没有依赖的指令，处理器支持乱序执行                       |
| 分支预测Speculation | 遇到条件分支指令时，预测分支结果，执行后续指令               |
| Speculative loads   | 预取数据                                                     |
| Load and store优化  | 合并Load/Store，批量读写                                     |
| 外部存储系统        | 控制路支持同时处理多个master的请求                           |
| 多核的Cache一致性   | 硬件支持的cache一致性，能在核间迁移cache line。不同的核看到的Cached更新顺序可能不一致。 |
| 编译器优化          | 编译器对指令重排序，可能把内存访问操作提前                   |



### 总线协议

* 随着SOC系统复杂性增加，模块间的交互变得错综复杂，软件控制也很困难
*   AMBA协议定义了在设计高性能嵌入式微控制器的片上通信标准
*   AMBA通过使用APB/AHB/AXI/CHI等协议的规范对SOC的公共通路进行定义，让SOC的模块设计更加清晰简答，重用性强



#### AMBA协议的演进

* 1995 - AMBA1.0 APB外设总线及ASB系统总线发布。
* 1999- AMBA2.0 AHB总线发布，APB 总线升级为同步总线。
* 2003-AMBA3.0 AXI高性能互联协议发布，APB总线扩展，AHB Lite协议发布。
* 2010-AMBA4.0 AXI4扩展总线发布，无缝对接AXI3。
* 2013-AMBA5.0 CHI高速一致性协议正式发布，目前已扩展到Issue E。



#### 基本结构

*   RING（环形总线）：
    *  由多个节点单向或双向环形互联而成，主要完成的功能是保证芯片系统内部所有设备之间的各传输通道按照一定的顺序正确且高效地互联互访；
*   MESH（网形总线）：
    *  由多个节点多方向网形互联而成，点与点之间通过共享总线进行互联；能支持大规模的节点的连接和提供强大的带宽；但是两两模块交互走的路径很多，路由不固化则路径太灵活设计复杂，路由固化则有可能会有同路径流量的冲突，造成性能下降；



### MMU

#### 为什么需要memory管理

* 典型系统的memory map被划分成多个逻辑区域，虚拟内存可以运行比实际物理内存大的应用程序。还会有一个交换分区（通常是硬盘）
* 每个逻辑区域可能需要不同的Memory属性
    * 访问权限
        *   Read/Write
        *   User/Privileged
    *  Memory类型
        * Cacheing/Buffering
        *   Normal/Device
* 安全隔离
    * 应用程序不用关注实际的物理memory空间



#### 虚拟内存

* 每个系统都会有一份硬件物理地址映射
* 虚拟地址空间被软件所定义
    * 页表定义了虚拟地址和物理地址间的映射
* 虚拟地址给OS更多的灵活性来进行Memory管理
    * 多个不连续的物理Memory块可以呈现出一个虚拟地址空间



#### MMU

*   虚拟地址到物理地址的转换、权限保护、访问属性等
*   PTW (Page Table Walk)
* TLB (Translation Look-aside Buffers)
    * 页表Cache
    *  减少页表转换时间
*   按页大小管理内存
    * 4K/16K/64K



#### 单级页表与多级页表的比较

*  单级页表占用连续内存比多级页表大
    *  假设页表粒度4KB，虚拟地址48-Bit， 每个页表Entry 8Bytes
    *  单级页表的Entry数：2^36
    * 4级页表，每级用9-Bit索引：`(2^9)+m*(2^9)+n*(2^9)+k*(2^9)`
    *  单机页表中即使没用到的页表也会占用1个Entry。但某个进程实际使用的页只占其中的一小部分，其分布是稀疏的，因此非常适合使用多级页表这种稀疏的级联数组
*  多级页表访问内存的数量增多，增加转换延迟
    *   TLB
        *   只会缓存最后一级的转换
    *   Large Page/Huge Page
        *  使用2MB/1GB的大页，减少内存访问次数
        *  TLB中缓存的页表粒度增大，miss率降低。
        *  内存碎片较多，内存浪费严重
    *   Paging Structure Caches
        *  两个连续的页，只有最后一级的转换不同
        *   缓存前几级转换



#### 内核/用户态的页表隔离

* `TTBR1_EL1`：内核态程序的页表基地址
*   `TTBR0_EL1`：用户态程序的页表基地址
*   `TCR_EL1`
    *   T0SZ/T1SZ: TTBR1/TTBR0虚拟地址范围 -2^（64-TnSZ）
    *   IPS：物理地址的大小
    *   TG1/TG0：页表的粒度



#### TLBI

* 当页表重新映射有修改时，需要将TLB中缓存的页表手动无效化掉
*   `TLBI <operation> {, <Xt>}`: `<operation> = < type> < level> {IS}`
*   Type
    * ALL: ALL TLB Entries
    *   VMALL: ALL TLB Entries (Stage1, Current Guest OS)
    *   VMALLS12: ALL TLB Entries (Stage1&2, Current Guest OS)
    *   ASID: Entries that match ASID in Xt
    *   VA: Entry for virtual address and ASID in Xt
    *   VAA: Entry for virtual address in Xt, with Any ASID
*   Level
    * `En=ELn`虚拟地址空间
*   IS: Inner-Shareable



## ARM处理器核典型结构

### Flynn分类法

* SISD
    * 串行処理器
* SIMD
    * 向量处理器
    * 参媒体指令扩展 （SSE、MMX、AVX）
    * GPU(SIMT)
* MISD
    * 无商业实现
* MIMD
    * 多核处理器



### 架构并行分类

* 指令级并行
    * 流水线
    * 超标量、乱序执行
    * 投机、分支预测
    * VLIW/EPIC
* 数据级并行
    * SIMD
* 线程级并行
    * MIMD
    * 并发多线程
    * Cache一致性
    * 同步



### 基本流程

1. 指令预取
2. 译码
3. 执行
4. 存取



### 流水线

* 性能
    * 对延迟没有收益
    * 对带宽收益很大
* 举例
    * Single Cycle Computer  
        * 45ns/Cycle x 1 CPl x 100 inst =4500ns   
    * Ideal Pipelined Computer  
        * 10ns/Cycle x (1CPU x100 inst + 4 cycle drain) = 1040 ns
* 对资源reuse



#### 流水线设计的困难

* 在流水线中我们希望当前每个时钟周期都有一条指令进入流水线可以执行。但在某些情况下，下一条指令无法按照预期开始执行，这种情况就被称为冒险
*  流水线限制：Hazards（冒险）阻止下一条指令在指定的时钟周期执行
    *  结构冒险：如果一条指令需要的硬件部分还在为之前的指令工作，无法为这条指令提供服务，那就导致结构冒险
        * HW cannot support this combination of instructions
    * 数据冒险：如果一条指令需要某数据而该数据正在被之前的指令操作，那这条指令就无法执行，导致了数据冒险
        * Instruction depends on result of prior instruction still in the pipeline
    * 控制冒险：如果现在要执行哪条指令，是由之前指令的运行结果决定，而现在那条之前指令的结果还没产生，就导致了控制冒险。
        * Caused by delay between the fetching of instructions and decisions about changes in control flow



##### 结构冒险

* 指令和数据放在同一个存储器中，那么不能同时读存储器
*  如何去解决？
    *   Stall Pipeline（效率低下）
    *   Harvard Structure（指令数据分开的存储结构）
    *  变种：单独的指令高速缓存和数据高速缓存。（一级高速缓存采用）



##### 数据冒险

* Data Hazrds
    *   RAW(Read After Write)
    *   WAW(Write After Write)
    *   WAR(Write After Read)
*   WAW/WAR富险是由于寄存器数量有限造成的
    *   寄存器需要反复复用
*   乱序执行会额外产生WAW/WAR冒险
*  解决方法
    *   Data Forward
        *   RAW
    *   Registers Rename
        *   WAW
        *   WAR



##### 寄存器重命名

* Registers
    *   Architected Registers (Logoic Registers)
        *  ISA定义的寄存器
        *   软件可见
    *   Rename Registers (Physical Registers)
        *   处理器 实现寄存器重命名增加的寄存器
        *   软件不可见
*  为WAW/WAR的指令重新分配1个不同的寄存器
    *   动态地解决寄存器复用带来的数据冒险
*   需要记录Architected Registers与Rename Registers之间的映射关系



### ROB(Re-order Buffer)

* 指令按原始顺序存入ROB
    *  FIFO、环形队列
    *  每个表项包括PC、目标寄存器、目标寄存器的值等
*   指令乱序执行完后，将结果放在ROB
    *   向其他介于读操作数、执行、完成和提交的指令提供操作数
    * 将结果用ROB的编号来表示，以决定某个结果写入到FIFO哪个Entry中
*  指令提交
    * 将ROB中顶部（Oldest）的数值更新到寄存器中



### 超标量处理器

*   指令获取（Instruction Fetch）
    *   每个时钟周期从ICache或Memory中取出多条指令
    * 分支预测
* 指令译码（Instruction Decode）
    *  译码指令（OpCode、Source、Destination）
    *   数据相关性检查与处理
*   指令分发（Instruction Dispatch）
    * 根据指令类型将指令分发到相应的运算单元
    *   将指令缓存在保留站中等待执行
*   指令执行（Instruction Execution）
    * 乱序执行指令
    *   指令结果、需要更新的寄存器或Memory地址等信息写入 ROB(Re-Order Buffer)
*   指令提交（Instruction Commit）
    *  按照指令的原始顺序更新寄存器或Memory



#### 为什么需要超标量处理器

* 标量处理器的局限性
  * IPC(instructions per cycle)的上限为1
  * 将不同类型的指令放在同—条流水线中处理，运算单元效率低下
    *   不同的指令需要不同的运算单元（例如整型和浮点数运算）
    *   多周期的指令很难和单周期的指令很难统一到同—条流水线中（例如乘法除法指令）
  * 会引入不必要的流水线气泡
    *   指令在流水线中必须步调一致，而且不会打乱指令的原始顺序
    *   当有一条指令由于依赖相关性停顿时，所有的后续指令都要停顿，无论是否有相关。
* 超标量处理器如何解决
  * 多发射：一次执行多条指令
  * 多个运算单元并行工作
  * 乱序执行、顺序提交



### ARM处理器核典型结构-ARM Cortex A76（ARMv8.2-A）

13级流水，4发射、OoO、8个处理单元

AARS: https://www.androidauthority.com/cortex-a76-deep-dive-870896/



## ARM多核处理器系统设计



## 参考

* Computer Organization and Design: The Hardware Software Interface [ARM Edition]
* Computer Organization and Design: The Hardware Software Interface[RISC-V Edition]
* Computer Architecture:A Quantitative Approach [6th Edition]
* Computer Systems: A Programmer's Perspective [3rd Edition]



## 新技术

* 多核一致性的cache研究
*  片上总线的结构选择
*   近内存计算
*   如何在memoy/cache/latency中选择相关的架构
*   未来的计算架构
*   如何在PPA中寻找平衡（性能，功耗，面积）