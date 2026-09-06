---
aliases:
- ARM
- ARM 架构
- ARM ISA
- ARM instruction set
confidentiality: public
domain: computer-science
evidence:
- claim: ARM（小写 stylised 为 arm）是 RISC 指令集架构家族，Arm Holdings 设计指令集并授权给其他公司构建物理设备。
  claim_id: arm-isa-family
  support: direct
  supporting_quotes:
  - evidence_id: evidence-c6331b5d1245
    exact: ARM (stylised in lowercase as arm) is a family of RISC instruction set
      architectures for computer processors. Arm Holdings develops the instruction
      set architecture and licenses them to other companies, who build the physical
      devices that use the instruction set.
  targets:
  - evidence_id: evidence-c6331b5d1245
    source_id: web-computer-science-arm-instruction-sets
- claim: ARM 架构是 load-store 架构，采用统一 16×32 位寄存器堆，固定 32 位指令宽度以简化译码与流水线（以代码密度为代价）；后来
    Thumb 指令集补充 16 位指令提高代码密度。
  claim_id: arm-risc-design
  support: direct
  supporting_quotes:
  - evidence_id: evidence-58dcc8093664
    exact: The ARM architecture is a load–store architecture. Uniform 16 × 32-bit
      register file (including the program counter, stack pointer and the link register).
      Fixed instruction width of 32 bits to ease decoding and pipelining, at the cost
      of decreased code density. Later, the Thumb instruction set added 16-bit instructions
      and increased code density.
  targets:
  - evidence_id: evidence-58dcc8093664
    source_id: web-computer-science-arm-instruction-sets
- claim: 自 ARM7TDMI（1994 年发布）起，处理器具备 Thumb 压缩指令集状态——ARM 指令集子集的紧凑 16 位编码。
  claim_id: arm-thumb
  support: direct
  supporting_quotes:
  - evidence_id: evidence-e8d2d7132c1c
    exact: To improve compiled code density, processors since the ARM7TDMI (released
      in 1994) have featured the Thumb compressed instruction set, which have their
      own state. When in this state, the processor executes the Thumb instruction
      set, a compact 16-bit encoding for a subset of the ARM instruction set.
  targets:
  - evidence_id: evidence-e8d2d7132c1c
    source_id: web-computer-science-arm-instruction-sets
id: arm-instruction-sets
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-arm-instruction-sets
status: published
tags:
- arm
- risc
- instruction-set
- isa
- architecture
title: ARM 指令集
updated_at: '2026-09-06'
---

# ARM 指令集

## 一句话结论

ARM（小写 stylised 为 arm）是 RISC 指令集架构（ISA）家族，由 Arm Holdings 设计并以 IP 授权模式提供给其他厂商实现。它的核心设计是 load-store 架构、统一 16×32 位寄存器堆、固定 32 位指令宽度、多数指令单周期执行；为弥补精简设计带来的代码密度下降，后期引入 Thumb（16 位压缩指令集）与 Thumb-2，并从 ARMv8 起扩展为 64 位 AArch64。指令集以条件执行、谓词化等特性著称，是手机/嵌入式/服务器/PC（Apple Silicon、Windows on ARM）最主流的处理器架构之一。

## 核心概念

- **RISC（Reduced Instruction Set Computer）**：精简指令集——指令规整、定宽、译码简单、多为单周期，与 CISC（如 x86）相对。
- **Load-store 架构**：只有 load/store 指令访问内存，运算指令只操作寄存器；ALU 指令不能直接读写内存。
- **统一寄存器堆**：ARM（AArch32）有 16 个 32 位通用寄存器（R0–R14，其中 R13=SP、R14=LR，R15=PC 在部分模式下特殊处理）。
- **条件执行（predication）**：大多数 ARM 指令可带条件码（EQ/NE/GT/LT 等），不满足条件则指令不执行，减少分支跳转。
- **Thumb / Thumb-2**：16 位压缩编码（后扩展为 16/32 位混合的 Thumb-2），提高代码密度，常用于存储受限的嵌入式系统。
- **AArch64 / ARMv8-A 起**：新增 64 位执行状态，31 个 64 位通用寄存器（X0–X30），是 Apple Silicon、服务器（如 AWS Graviton）采用的主要状态。

## 工作机制

1. **取指-译码-执行流水线**：ARM 核心按流水线取指固定宽度指令（AArch32 为 32 位），译码后访问统一寄存器堆执行，多数指令单周期完成。
2. **Load-store 数据流**：内存中的数据必须先经 load 指令读入寄存器，运算在寄存器间进行，结果经 store 写回内存——运算指令不直接访问内存。
3. **条件执行减少分支**：指令的高 4 位为条件码，条件不成立时指令被丢弃（不改变架构状态），从而在短分支处替代真正的跳转，减少流水线冲刷。
4. **Thumb 译码映射**：Thumb 状态使用 16 位编码（Thumb-2 混合 32 位），多数 Thumb 指令直接映射到普通 ARM 指令，编译后代码更紧凑，解码器把 Thumb 指令映射回内部操作。

## 示例或代码

```asm
@ ARM 条件执行示例：if (r0 < 0) r1 = r2 + r3;
    CMP   r0, #0        @ 比较 r0 与 0，设置条件码（N）
    ADDLT r1, r2, r3    @ 若 r0<0（LT=有符号小于），r1 = r2 + r3；否则本条不执行
```

```asm
@ Load-store 示例：*(int*)p = a + b;
    LDR   r0, =p        @ 加载 p 地址
    LDR   r2, [r0]      @ load：把内存读到寄存器（运算前必须先 load）
    ADD   r1, r2, r3    @ 运算只在寄存器间进行
    STR   r1, [r0]      @ store：把结果写回内存
```

## 常见误区

- **“ARM 只有 32 位”**：ARMv8-A 起同时支持 AArch32 与 AArch64（64 位），现代服务器、PC、旗舰手机均运行 64 位状态。
- **“RISC 就一定更快”**：RISC 靠简单指令+流水线换取高频/低功耗，但指令条数更多；与 x86 的对比必须结合微架构、功耗、应用场景，而非指令集本身（见 [[isa-and-microarchitecture]]）。
- **“条件执行是冗余优化”**：在短代码段条件执行比分支跳转更高效（省去跳转与流水线冲刷），但过长的谓词化指令反而降低性能，现代编译器会权衡。
- **“Thumb 只是‘更小更慢’的指令集”**：Thumb-2 在保持较高代码密度的同时性能接近 ARM 状态，是嵌入式与移动端默认选择之一。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| arm-isa-family | web-computer-science-arm-instruction-sets | ARM 是 RISC ISA 家族，Arm 授权给厂商实现 |
| arm-risc-design | web-computer-science-arm-instruction-sets | load-store、统一 16×32 寄存器、32 位定宽、单周期、Thumb 补 16 位 |
| arm-thumb | web-computer-science-arm-instruction-sets | Thumb 压缩指令集：16 位编码、映射到 ARM 指令 |

## 待验证项

- 条件执行、AArch64 寄存器布局等细节目前由本文综合表述，暂未锚定到权威文档（后续可从 Arm ARM 或 Arm Architecture Reference Manual 补锚）。
- Thumb-2 混合 16/32 位编码的机制描述为常识性概括，建议对照 [[arm-neon]] 等实操页面复核。

## 关联知识

- [[isa-and-microarchitecture]] —— ISA 与微架构的区分（指令集 vs 实现）。
- [[arm-neon]] —— ARM 的 SIMD 扩展（NEON），属 ARM 指令集的向量部分。
- [[cpu-and-memory]] —— CPU 与内存交互机制（load-store 的上层）。
- [[von-neumann-architecture]] —— 经典体系结构（指令/数据同存储）。
- [[gpu-overview]] —— 与 RISC CPU 不同的并行处理器设计。

## 详细章节

### ARM 是什么

ARM（stylised 为小写 arm）是 RISC 指令集架构家族。Arm Holdings 设计指令集架构并授权给其他公司，由这些公司构建使用该指令集的物理设备；Arm 也设计并授权实现这些指令集架构的内核（core）。

### RISC 设计要点（经典 ARM 指令集）

- **Load-store 架构**：只有 load/store 指令访问内存，运算在寄存器间完成。
- **统一 16×32 位寄存器堆**：包含程序计数器、栈指针与链接寄存器。
- **固定 32 位指令宽度**：便于译码与流水线，代价是代码密度较低。
- **多数指令单周期执行**：简化控制逻辑，有利于提高主频与能效。

### Thumb 压缩指令集

为改善编译代码密度，自 ARM7TDMI（1994 年发布）起处理器提供 Thumb 压缩指令集状态。在该状态下处理器执行 Thumb 指令集——ARM 指令集子集的紧凑 16 位编码。多数 Thumb 指令直接映射到普通 ARM 指令；空间节省来自将部分操作数隐含、并限制比 ARM 指令集状态更少的可能性组合。

### 条件执行与分支

ARM 的分支采用条件码与 compare-and-branch 机制：多数指令可带条件码，条件不成立时指令被丢弃，从而在短代码段替代真正的分支跳转，减少流水线冲刷。

## 参考

- [Wikipedia: ARM architecture family](https://en.wikipedia.org/wiki/ARM_architecture_family)
- [Arm Architecture Reference Manual（A-profile）](https://developer.arm.com/documentation/ddi0487/latest)
