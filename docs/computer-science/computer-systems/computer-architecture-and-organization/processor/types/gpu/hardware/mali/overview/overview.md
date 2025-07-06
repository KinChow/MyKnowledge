# Mali GPU 概述

## 概述

ARM的Mali GPU系列是为移动设备设计的高效能图形处理单元（GPU），它们广泛应用于智能手机、平板电脑、电视等设备中。Mali GPU的设计注重能效比，以满足移动设备对电池寿命和性能的需求。



## 架构

### Utgard

##### 时间线

2005 年，Falanx 宣布了他们的 Utgard GPU 架构，即 Mali-200 GPU。 Arm 随后推出了 Mali-300、Mali-400、Mali-450 和 Mali-470。 Utgard 是一个非统一的 GPU（离散像素和顶点着色器）。

##### 特点

* 可编程流水线

* 主要专注于图形加速，支持OpenGL ES 2.0，但不支持OpenCL。



### Midgard

#### 1st Gen

##### 时间线

2010 年 11 月 10 日，Arm 宣布推出 Midgard 第一代 GPU 架构，包括 Mali-T604 以及后来于 2011 年推出的 Mali-T658 GPU。

##### 特点

* Midgard 使用分层平铺系统。

* 支持OpenGL ES 3.1，OpenCL 1.1。



#### 2nd Gen

##### 时间线

2012 年 8 月 6 日，Arm 宣布推出 Midgard 第二代 GPU 架构，其中包括 Mali-T678 GPU。

##### 特点

* Midgard 第二代引入了前向像素消除。
* 支持OpenGL ES 3.1，OpenCL 1.1。



#### 3rd Gen

##### 时间线

2013 年 10 月 29 日，Arm 发布了 Midgard 第三代 GPU 架构，包括 Mali-T760 GPU。

##### 特点

* 支持Vulkan 1.0，OpenGL ES 3.2，OpenCL 1.2。



#### 4th Gen

##### 时间线

2014年10月27日，Arm 发布了Midgard第四代GPU架构，包括Mali-T860、Mali-T830、Mali-T820。他们的旗舰产品 Mali-T880 GPU 于 2015 年 2 月 3 日发布。

##### 特点

- Mali-T880 多达16个内核，具有 256KB – 2MB 二级缓存。
- 支持Vulkan 1.0，OpenGL ES 3.2，OpenCL 1.2。



### Bifrost

#### 1st Gen

##### 时间线

2016 年 5 月 27 日，Arm 发布了 Bifrost GPU 架构，包括 Mali-G71 GPU。

##### 特点

- 具有四向量化的统一着色器。
- 标量ISA。
- 条款执行。
- 完全缓存一致性。
- Mali-G71 多达32个内核，具有 128KB – 2MB 二级缓存。
- Arm 声称 Mali-G71 的性能密度比 Mali-T880 高 40%，能效高 20%。
- 支持Vulkan 1.3，OpenGL ES 3.2，OpenCL 2.0。



#### 2nd Gen

##### 时间线

2017 年 5 月 29 日，Arm 发布了 Bifrost 第二代 GPU 架构，包括 Mali-G72 GPU。

##### 特点

- 算术优化和增加缓存。
- Mali-G72 多达32个内核，具有 128KB – 2MB 二级缓存。
- Arm 声称 Mali-G72 的性能密度比 Mali-G71 高20%，能效高25%。
- 支持Vulkan 1.3，OpenGL ES 3.2，OpenCL 2.0。



#### 3rd Gen

##### 时间线

2018 年 5 月 31 日，Arm 发布了 Bifrost 第四代 GPU 架构，包括 Mali-G76 GPU。

##### 特点

- 每个引擎 8 个执行通道（之前为 4 个）。像素和纹素吞吐量加倍。
- Mali-G76 多达20个内核，具有 512KB – 4MB 二级缓存。
- Arm 声称 Mali-G76 的性能密度比 Mali-G72 高30%，能效高 0%。
- 支持Vulkan 1.3，OpenGL ES 3.2，OpenCL 2.0。



### Valhall

#### 1st Gen

##### 时间线

2019 年 5 月 27 日，Arm 宣布推出 Valhall GPU 架构，包括 Mali-G77 GPU 和 10 月份的 Mali-G57 GPU。

##### 特点

- 新型超标量引擎
- 简化的标量 ISA
- 新的动态调度
- Mali-G77 多达16个内核，具有 512KB – 2MB 二级缓存
- Arm 声称 Mali-G77 的性能密度比 Mali-G76 高30%，能效高30%



#### 2nd Gen

##### 时间线

2020 年 5 月 26 日，Arm 宣布推出 Valhall 第二代 GPU 架构，包括 Mali-G78。

##### 特点

- 异步时钟域
- 新的 FMA 单元并提高 Tiler 吞吐量
- Mali-G78 多达24个内核，具有 512KB – 2MB 二级缓存
- Arm 帧缓冲区压缩 (AFBC)
- Arm 声称 Mali-G78 的性能密度比 Mali-G77 高 15%，能效高 10%



#### 3rd Gen

##### 时间线

2021 年 5 月 25 日，Arm 宣布推出 Valhall 第三代 GPU 架构（作为 TCS21 的一部分），包括 Mali-G710、Mali-G510 和 Mali-G310 GPU。

##### 特点

* 更大的着色器核心（是 Valhall 第二代的 2 倍）。

- 新的 GPU 前端、命令流前端 (CSF) 取代了作业管理器。
- Mali-G710 多达16个内核，具有 512KB – 2MB 二级缓存。
- Arm 声称 Mali-G710 的性能密度比 Mali-G78 高20%，能效高20%。
- 支持Vulkan 1.3，OpenGL ES 3.2，OpenCL 2.0。



#### 4th Gen

##### 时间线

2022 年 6 月 28 日，Arm 宣布推出 Valhall 第四代 GPU 架构（作为 TCS22 的一部分），包括 Immortalis-G715、Mali-G715 和 Mali-G615 GPU。

##### 特点

- 光线追踪支持（基于硬件）。
- 可变速率着色。
- 新的执行引擎，具有双倍的 FMA 块、矩阵乘法指令支持和 PPA 改进。
- 手臂固定速率压缩 (AFRC)。
- Arm 声称 Immortalis-G715 比 Mali-G710 性能提高15%，能效提高15% 。
- 支持Vulkan 1.3，OpenGL ES 3.2，OpenCL 2.0。



#### 5th Gen

##### 时间线

2023 年 5 月 29 日，Arm 宣布推出第五代 Arm GPU 架构（作为 TCS23 的一部分），包括 Immortalis-G720、Mali-G720 和 Mali-G620 GPU。

##### 特点

- 延迟顶点着色 (DVS) 管道。
- Arm 声称，与 Immortalis-G715 相比，Immortalis-G720 的性能提高了15%，并且使用的内存带宽减少了40%。
- 支持Vulkan 1.3，OpenGL ES 3.2，OpenCL 3.0。



## 实现

### HiSilicon

| Soc名称                      | Mali型号                      |
| ---------------------------- | ----------------------------- |
| Kirin 620                    | Mali-450 MP4 @ 533 MHz        |
| Kirin 650/655/658/659        | Mali-T830 MP2 @ 900 MHz       |
| Kirin 710                    | Mali-G51 MP4 @ 1000 MHz       |
| Kirin 810                    | Mali-G52 MP6 @ 820 MHz        |
| Kirin 820                    | Mali-G57 MP6 @??? MHz         |
| Kirin 910/910T               | Mali-450 MP4 @ 533/700 MHz    |
| Kirin 920/925/928            | Mali-T628 MP4 @ 600/600/? MHz |
| Kirin 930/935                | Mali-T628 MP4 @ 600/680 MHz   |
| Kirin 950/955                | Mali-T880 MP4 @ 900 MHz       |
| Kirin 960                    | Mali-G71 MP8 @ 1037 MHz       |
| Kirin 970                    | Mali-G72 MP12 @ 746 MHz       |
| Kirin 980                    | Mali-G76 MP10 @ 720 MHz       |
| Kirin 985                    | Mali-G77 MP8 @??? MHz         |
| Kirin 990/990 5G             | Mali-G76 MP16 @ 600 MHz       |
| Kirin 9000 5G/Kirin 9000E 5G | Mali-G78 MP24/22 @ 759 MHz    |



### MediaTek

| Soc名称                                                     | Mali型号                                                     |
| ----------------------------------------------------------- | ------------------------------------------------------------ |
| MSD6683                                                     | Mali-470 MP3                                                 |
| MT5595, MT5890                                              | Mali-T624 MP3                                                |
| MT5596, MT5891                                              | Mali-T860 MP2[[79\]](https://en.wikipedia.org/wiki/Mali_(processor)#cite_note-79) |
| MT6571, MT6572, MT6572M                                     | Mali-400 MP1 @ ?/500/400 MHz                                 |
| MT6580                                                      | Mali-400 MP1 @ 500 MHz                                       |
| MT6582/MT6582M                                              | Mali-400 MP2 @ 500/416 MHz                                   |
| MT6588, MT6591, MT6592, MT6592M, MT8127                     | Mali-450 MP4 @ 600/700/600/600 MHz[[80\]](https://en.wikipedia.org/wiki/Mali_(processor)#cite_note-80) |
| MT6735, MT6735M, MT6735P                                    | Mali-T720 MP2 @ 600/500/400 MHz                              |
| MT6737, MT6737T                                             | Mali-T720 MP2 @ 550/600 MHz                                  |
| MT8735                                                      | Mali-T720 MP2 @ 450 MHz                                      |
| MT6753                                                      | Mali-T720 MP3 @ 700 MHz[[81\]](https://en.wikipedia.org/wiki/Mali_(processor)#cite_note-81) |
| MT6732, MT6732M, MT6752, MT6752M                            | Mali-T760 MP2 @ 500/500/700/700 MHz[[82\]](https://en.wikipedia.org/wiki/Mali_(processor)#cite_note-82) |
| MT6750                                                      | Mali-T860 MP2 @ 520 MHz                                      |
| MT6755 (Helio P10/P15/P18)                                  | Mali-T860 MP2 @ 700/650/800 MHz                              |
| MT6757 (Helio P20, P25)                                     | Mali-T880 MP2 @ 900 MHz/1.0 GHz[[83\]](https://en.wikipedia.org/wiki/Mali_(processor)#cite_note-83) |
| MT6797 (Helio X20/X23/X25/X27)                              | Mali-T880 MP4 @ 780/850/875 MHz                              |
| MT6763T (Helio P23), MT6758 (Helio P30)                     | Mali-G71 MP2 @ 770/950 MHz[[84\]](https://en.wikipedia.org/wiki/Mali_(processor)#cite_note-84)[[85\]](https://en.wikipedia.org/wiki/Mali_(processor)#cite_note-85) |
| MT6771 (Helio P60, P70)                                     | Mali-G72 MP3 @ 800/900 MHz[[86\]](https://en.wikipedia.org/wiki/Mali_(processor)#cite_note-86)[[87\]](https://en.wikipedia.org/wiki/Mali_(processor)#cite_note-87) |
| MT6768 (Helio P65), MT6769 (Helio G70/G80/G85/G88)          | Mali-G52 MC2 @ 820/950/1000 MHz                              |
| MT6785 (Helio G90/G90T/G95)                                 | Mali-G76 MC4 @ 720/800/900 MHz                               |
| MT6781 (Helio G96 , G99), MT6833 (Dimensity 700, 810, 6020) | Mali-G57 MC2 @ 850/950 MHz                                   |
| MT6853 (Dimensity 720, 800U)                                | Mali-G57 MC3 @ 850 MHz                                       |
| MT6873 (Dimensity 800)                                      | Mali-G57 MC4 @ 650 MHz                                       |
| MT6875 (Dimensity 820), MT6883Z (Dimensity 1000C)           | Mali-G57 MC5 @ 900 MHz                                       |
| MT6877/MT6877T (Dimensity 900/920/1080/7050)                | Mali-G68 MC4 @ 900 MHz                                       |
| MT6885Z (Dimensity 1000L)                                   | Mali-G77 MC7 @ 695 MHz                                       |
| MT6889 (Dimensity 1000/1000+)                               | Mali-G77 MC9 @ 850 MHz                                       |
| MT6891/MT6893 (Dimensity 1100/1200/1300/8020/8050)          | Mali-G77 MC9 @ 850 MHz                                       |
| MT8192 (Kompanio 820)                                       | Mali-G57 MC5 GPU @ ??? MHz                                   |
| MT8195/MT8195T (Kompanio 1200/1380)                         | Mali-G57 MC5 GPU @ ??? MHz                                   |
| MT8791 (Kompanio 900T)                                      | Mali-G68 MP4 GPU @ 900 MHz                                   |
| MT8797 (Kompanio 1300T)                                     | Mali-G77 MP9 @ 850 MHz                                       |
| MT6895/MT6886 (Dimensity 7200/8000/8100/8200)               | Mali-G610 MC6 @ ??? MHz                                      |
| MT6983 (Dimensity 9000/9000+)                               | Mali-G710 MP10 @ 850 MHz                                     |
| MT6985 (Dimensity 9200/9200+)                               | Immortalis-G715 MP11 @ ??? MHz                               |



### Sansung

| Soc名称                                                      | Mali型号                                        |
| ------------------------------------------------------------ | ----------------------------------------------- |
| Exynos 3 Quad (3470), Exynos 4 Dual, Quad (4210, 4212 and 4412) | Mali-400 MP4                                    |
| Exynos 5 Dual (5250) | Mali-T604 MP4                                   |
| Exynos 5 Hexa (5260) | Mali-T624 MP3                                   |
| Exynos 5 Octa (5420, 5422, 5430 and 5800) | Mali-T628 MP6                                   |
| Exynos 5 Hexa (7872)                                         | Mali-G71 MP1 @ 1.2 GHz                          |
| Exynos 7 Octa (5433/7410) | Mali-T760 MP6                                   |
| Exynos 7 Octa (7420) | Mali-T760 MP8 @ 772 MHz                         |
| Exynos 7 Quad (7570), Exynos 3 Quad (3475) | Mali-T720 MP1                                   |
| Exynos 7 Octa (7580) | Mali-T720 MP2                                   |
| Exynos 7 Octa (7870) | Mali-T830 MP1 @ 1000 MHz                        |
| Exynos 7 Octa (7880) | Mali-T830 MP3 @ 950 MHz                         |
| Exynos 7 Series 7885 | Mali-G71 MP2 @ 1300 MHz                         |
| Exynos 850           | Mali-G52 MP1                                    |
| Exynos 8 Octa 880    | Mali-G76 MP5 @ ???MHz                           |
| Exynos 8 Octa (8890) | Mali-T880 MP10 (Lite) / Mali-T880 MP12 @650 MHz |
| Exynos 9 Octa (8895) | Mali-G71 MP20 @ 546 MHz                         |
| Exynos 7 Series 9610 | Mali-G72 MP3                                    |
| Exynos 9 Series 9810 | Mali-G72 MP18 @ 572 MHz                         |
| Exynos 9 Series 9820/9825 | Mali-G76 MP12 @ 702/??? MHz                     |
| Exynos 9 Series 980  | Mali-G76 MP5 @ ? MHz                            |
| Exynos 9 Series 990  | Mali-G77 MP11 @ 800 MHz                         |
| Exynos 1330          | Mali G68 MP2 @ ??? MHz                          |
| Exynos 1280          | Mali-G68 MP4 @ 1000 MHz                         |
| Exynos 1380          | Mali-G68 MP5 @ 950 MHz                          |
| Exynos 1080          | Mali-G78 MP10 @ ?? MHz                          |
| Exynos 2100          | Mali-G78 MP14 @ ?? MHz                          |





## 参考

https://en.wikipedia.org/wiki/Mali_(processor)

