---
aliases:
- 计算机硬件
- Computer Hardware
- PC 硬件
confidentiality: public
domain: computer-science
evidence:
- claim: 计算机硬件包括计算机的物理部件，如 CPU、RAM、主板、数据存储、显卡、声卡与机箱，以及显示器、鼠标、键盘、音箱等外部设备。
  claim_id: hardware-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-2754e1ca4120
    exact: Computer hardware includes the physical parts of a computer, such as the
      central processing unit (CPU), random access memory (RAM), motherboard, computer
      data storage, graphics card, sound card, and computer case. It includes external
      devices such as a monitor, mouse, keyboard, and speakers.
  targets:
  - evidence_id: evidence-2754e1ca4120
    source_id: web-computer-science-computer-hardware
- claim: CPU 执行计算机所需的大部分计算任务；它从 RAM 取指令、译码并执行，然后返回结果供其他部件进一步处理（即指令周期）。
  claim_id: hardware-cpu
  support: direct
  supporting_quotes:
  - evidence_id: evidence-84a42a7dca80
    exact: At least one CPU (central processing unit), which performs the majority
      of computational tasks required for a computer to operate. Often described informally
      as the brain of the computer, the CPU fetches program instructions from random-access
      memory (RAM), decodes and executes them, then returns results for further processing
      by other components. This process is known as the instruction cycle.
  targets:
  - evidence_id: evidence-84a42a7dca80
    source_id: web-computer-science-computer-hardware
- claim: 大多数个人电脑电源单元符合 ATX 标准，把电源插座提供的 120–277V 交流电转换为更低电压（典型 12V、5V 或 3.3V）的直流电。
  claim_id: hardware-power
  support: direct
  supporting_quotes:
  - evidence_id: evidence-9da6093a732a
    exact: 'Most personal computer power supply units meet the ATX standard and convert
      from alternating current (AC) at between 120 and 277 volts provided from a power
      outlet to direct current (DC) at a much lower voltage: typically 12, 5, or 3.3
      volts.'
  targets:
  - evidence_id: evidence-9da6093a732a
    source_id: web-computer-science-computer-hardware
- claim: 内部总线用地址、数据、控制等多条通信线连接 CPU 与主存；21 世纪高速串行总线（如 PCI Express、USB）取代了并行总线；多处理器系统中传统上由北桥协调
    CPU、内存与高速外设，南桥负责较慢的 I/O 设备。
  claim_id: hardware-bus-chipset
  support: direct
  supporting_quotes:
  - evidence_id: evidence-06bce453287a
    exact: The internal bus connects the CPU to main memory via multiple communication
      lines—typically 50 to 100—divided into address, data, and control buses, each
      handling specific types of signals. Historically, parallel buses were dominant,
      but in the twenty-first century, high-speed serial buses (often using serializer/deserializer
      (SerDes) technology) have largely replaced them, enabling greater data throughput
      over fewer physical connections. Examples include PCI Express and USB. In systems
      with multiple processors, an interconnect bus is used, traditionally coordinated
      by a northbridge chip, which links the CPU, memory, and high-speed peripherals
      such as PCI. The southbridge handles communication with slower I/O devices such
      as storage.
  targets:
  - evidence_id: evidence-06bce453287a
    source_id: web-computer-science-computer-hardware
id: computer-hardware
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-computer-hardware
status: published
tags:
- hardware
- cpu
- memory
- motherboard
- bus
- power-supply
title: 计算机硬件
updated_at: '2026-09-06'
---

# 计算机硬件

## 一句话结论

计算机硬件是计算机的物理部件总和，包括 CPU（中央处理器）、内存（RAM）、主板、数据存储、显卡、声卡、机箱等内部部件，以及显示器、鼠标、键盘、音箱等外部设备。系统按“CPU ↔ 总线 ↔ 内存/外设”的结构运转：CPU 取指-译码-执行（指令周期），芯片组（北桥/南桥）协调数据传输流向，总线是实际传输数据的高速公路，电源把交流电转为各部件所需的低压直流电。理解硬件组成与各部件职责，是理解整机性能与体系结构（[[von-neumann-architecture]]）的基础。

## 核心概念

- **CPU（中央处理器）**：计算机的“大脑”，执行大部分计算任务；从内存取指、译码、执行，结果交回其他部件（指令周期）。
- **内存（RAM）**：随机存取存储器，存放正在执行的程序与数据，断电丢失；CPU 直接经总线访问。
- **主板与芯片组**：主板承载 CPU、内存、扩展槽与 I/O 接口；芯片组（传统分北桥/南桥）控制数据“从哪到哪”的流转。
- **总线**：CPU 与内存/外设之间的数据传输“高速公路”，分地址/数据/控制三类信号线；现代多为高速串行总线（PCIe、USB）。
- **北桥 / 南桥**：北桥连接 CPU、内存、显卡等高速部件（现已多集成进 CPU）；南桥连接硬盘、键盘、鼠标等较慢 I/O 设备。
- **电源（PSU）**：ATX 标准，把 120–277V 交流电转换为 12V/5V/3.3V 直流电供各部件。
- **显卡（GPU）**：负责图形渲染与大规模并行计算，可独立（扩展卡）或集成进 CPU/主板（见 [[gpu-overview]]）。

## 工作机制

1. **指令周期（CPU 核心运转）**：CPU 从 RAM 取指令 → 译码 → 执行 → 将结果交回其他部件继续处理；内存是程序与数据的所在地（冯·诺依曼结构，见 [[von-neumann-architecture]]）。
2. **总线传输**：CPU 与主存之间由内部总线连接，通信线（约 50–100 条）分为地址总线（选地址）、数据总线（传数据）、控制总线（传控制信号）。21 世纪高速串行总线（PCIe、USB，基于 SerDes 技术）已取代多数并行总线，用更少物理连接获得更高吞吐。
3. **芯片组协调**：传统上北桥连接 CPU、内存与高速外设（如 PCI 显卡），南桥连接较慢 I/O（存储、键鼠）；现代北桥功能多已并入 CPU（所以主板上“看不到北桥”），芯片组以单芯片（PCH）形式存在。
4. **供电与散热**：电源按 ATX 标准把交流电转为 12V/5V/3.3V 直流电；CPU/GPU 功耗高，用散热器+风扇或液冷散热。
5. **I/O 扩展**：扩展卡（显卡、声卡、网卡）插入主板扩展槽，通过扩展总线为系统增加功能；现代显卡常集成在 CPU/主板中。

## 示例或代码

- **整机数据流示例**（文字说明）：

```
用户按键盘（南桥→USB 控制器）→ 键盘输入经中断/轮询进入内存
→ CPU 取指令执行应用程序 → 图形计算经显卡渲染
→ 帧缓冲经显示输出接口（HDMI/DP）送显示器
电源（ATX PSU）为所有部件提供 12V/5V/3.3V 直流电
```

- **部件与总线速率的直观对比**（示例性数量级，具体因代际而异）：

| 部件 | 连接 | 说明 |
| --- | --- | --- |
| CPU ↔ 内存 | 内存控制器（北桥内/CPU 内） | 延迟最低，带宽最高 |
| CPU ↔ 显卡 | PCIe x16 | 高速串行总线 |
| CPU ↔ 硬盘 | NVMe/SATA（经南桥/PCH） | 存储 I/O |
| 键鼠/外设 | USB/PS2（经南桥/PCH） | 慢速 I/O |

## 常见误区

- **“内存越大电脑一定越快”**：内存容量只决定能否装下更多程序/数据；性能还受内存带宽、延迟、CPU 与总线能力影响（见 [[cpu-and-memory]]）。
- **“主板上的北桥还在”**：现代架构北桥功能（内存控制器、PCIe 控制器）已集成进 CPU，主板上通常只看到单芯片（南桥/PCH）。
- **“显卡只用于玩游戏”**：GPU 承担大规模并行计算（AI、科学计算、渲染），也是通用加速器（见 [[gpu-overview]]）。
- **“电源越大越好”**：电源按额定功率与 80 Plus 效率选型，功率过大浪费、不足导致不稳定；更重要的是各路 12V 供电与接口匹配。
- **“总线是单条线路”**：总线是分组的多条通信线（地址/数据/控制），并已从并行演进到高速串行。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| hardware-definition | web-computer-science-computer-hardware | 硬件的内部/外部部件清单 |
| hardware-cpu | web-computer-science-computer-hardware | CPU 取指-译码-执行（指令周期） |
| hardware-power | web-computer-science-computer-hardware | ATX 电源 交流→直流 12/5/3.3V |
| hardware-bus-chipset | web-computer-science-computer-hardware | 地址/数据/控制总线、北桥/南桥分工 |

## 待验证项

- “北桥功能已集成进 CPU”为对现代平台的常识性表述（与 legacy 提纲一致），具体平台（Intel/AMD）的芯片组分工差异可在实操时对照平台白皮书复核。
- 部件-总线速率的示例数量级为说明性数据，非基准测量，引用时注意上下文。

## 关联知识

- [[cpu-and-memory]] —— CPU 与内存机制深入。
- [[von-neumann-architecture]] —— 程序/数据同存储的经典体系结构。
- [[gpu-overview]] —— 显卡/GPU 的架构与渲染管线。
- [[computer-performance-and-power-consumption]] —— 硬件性能与功耗权衡。
- [[npu-overview]] —— 现代 SoC 中的 AI 加速硬件。

## 详细章节

### CPU 中央处理器

CPU 是计算机中执行大部分计算任务的部件。它从随机存取存储器（RAM）取出程序指令，译码并执行，然后把结果交回其他部件继续处理——这个过程称为指令周期。CPU 常被非正式地描述为“计算机的大脑”。现代 CPU 是基于金属氧化物半导体（MOS）集成电路、采用光刻等先进制造工艺制造的微处理器，通常用散热器+风扇或液冷系统散热。许多当代 CPU 还集成了片内 GPU，省去了基础场景对独立显卡的需求。

### 内存

内存（RAM，随机存取存储器）存放正在运行的程序与数据，CPU 通过总线直接读写。它是“冯·诺依曼”结构的核心——程序与数据同处存储（见 [[von-neumann-architecture]]）。内存特性（容量、带宽、延迟）直接影响整机性能，详见 [[cpu-and-memory]]。

### 主板

主板是承载 CPU、内存、扩展槽与各类接口的印刷电路板。主板的核心价值在于**芯片组与总线**：

- **芯片组**控制数据传输的流转，也就是“数据从哪里到哪里”的问题；
- **总线**是实际传输数据的高速公路，总线速度决定数据能传输得多快。

主板芯片组传统上分为南桥与北桥：

- **南桥**：控制鼠标、键盘以及硬盘等外部输入输出设备与 CPU 之间的通信（较慢的 I/O）。
- **北桥**：连接 CPU 与内存、显卡之间的通信（高速部件）。现代北桥的功能已移植到 CPU 内部，所以主板上已看不到北桥芯片。

### 总线

内部总线用多条通信线（通常 50–100 条）把 CPU 连接到主存，分为**地址总线、数据总线、控制总线**，各处理特定类型的信号。历史上并行总线占主导；进入 21 世纪后，高速串行总线（常基于串行器/解串器 SerDes 技术）大规模取代并行总线，用更少的物理连接获得更高数据吞吐，例如 PCI Express 与 USB。在多处理器系统中使用互连总线，传统上由**北桥芯片**协调，连接 CPU、内存与 PCI 等高速外设；**南桥**负责与存储等较慢 I/O 设备通信。

### 电源

大多数个人电脑的电源单元（PSU）符合 ATX 标准，把电源插座提供的 120–277V 交流电（AC）转换为低得多的电压——典型为 12V、5V 或 3.3V——的直流电（DC），为 CPU、内存、主板、显卡、硬盘等部件供电。

### 显卡

显卡（GPU，图形处理器）负责图形渲染与大规模并行计算。在硬件上它可以是独立扩展卡，也可以是集成在 CPU/主板中的片内 GPU。显卡的并行架构、渲染管线与与 CPU 的差异详见 [[gpu-overview]]。

### 输入/输出设备

显示器、鼠标、键盘、音箱等外部设备通过主板接口（USB、HDMI、DP 等）与主机交互，属于计算机硬件的外部部分。扩展卡（如独立显卡、声卡、网卡）插入主板扩展槽，通过扩展总线为系统增加功能。

## 参考

- [Wikipedia: Computer hardware](https://en.wikipedia.org/wiki/Computer_hardware)
- [Wikipedia: Northbridge](https://en.wikipedia.org/wiki/Northbridge_(computing))
- [Wikipedia: Southbridge](https://en.wikipedia.org/wiki/Southbridge_(computing))
