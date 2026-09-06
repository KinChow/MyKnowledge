---
aliases: []
confidentiality: public
domain: computer-science
evidence:
- claim: 对电池供电设备或大型长时间计算而言，直接功耗和间接功耗都是计算效率需要关注的指标。
  claim_id: computer-performance-and-power-consumption-power
  support: direct
  supporting_quotes:
  - evidence_id: evidence-8ee402064328
    exact: 'For computers whose power is supplied by a battery (e.g. laptops and smartphones),
      or for very long/large calculations (e.g. supercomputers), other measures of
      interest are:


      Direct power consumption: power needed directly to operate the computer.

      Indirect power consumption: power needed for cooling, lighting, etc.'
  targets:
  - evidence_id: evidence-8ee402064328
    source_id: wikipedia-algorithmic-efficiency-power-v2
id: computer-performance-and-power-consumption
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- wikipedia-algorithmic-efficiency-power-v2
- working-computer-science-computer-performance-and-power-consumption
status: published
tags:
- performance
- power
- cpu
- benchmark
title: 计算机性能和功耗
updated_at: '2026-09-06'
---
# 计算机性能和功耗

## 一句话结论

计算机性能可由**响应时间/执行时间**或**吞吐率/带宽**衡量，CPU 执行时间 = 指令数 × CPI × 时钟周期时间；而提高性能（增加晶体管密度、提高主频）会增加**功耗**与散热负担，功耗 ≈ 1/2 × 负载电容 × 电压² × 开关频率 × 晶体管数量。

## 核心概念

- **响应时间 / 执行时间**：执行程序要花多少时间（让计算机跑得更快）。
- **吞吐率 / 带宽**：一定时间范围内能处理多少事情——处理的数据或执行的程序指令（让计算机搬得更多）。
- 性能的定义：响应时间的倒数。
- SPEC：CPU 基准测试程序。
- 计时：CPU 时钟；`time` 命令统计 real / user / sys time。
- 功耗公式：功耗 ≈ 1/2 × 负载电容 × 电压的平方 × 开关频率 × 晶体管数量。

## 工作机制

- 程序实际花费的 CPU 执行时间 = user time + sys time。
- 程序的 CPU 执行时间 = CPU 时钟周期数 × 时钟周期时间；CPU 时钟周期数 = 指令数 × 每条指令平均时钟周期数（CPI）。
- 提高性能可从**指令数**、**CPI** 和 **CPU 主频**入手。
- CPU 是超大规模集成电路，由晶体管组成；计算即晶体管开关不断开合组合成各种运算。增加同样面积里的晶体管数量（提高密度）或让开关更快（提高主频）都会增加功耗，带来耗电与散热问题；CPU 面积变大时晶体管间距变大、电传输时间变长，运算速度下降；CPU 里能放下的晶体管数量和开关频率是有限的。

## 示例或代码

```shell
# linux 统计程序的时间
time
```

- real time：运行程序，整个过程中流逝的时间。
- user time：用户态运行指令的时间。
- sys time：内核里运行指令的时间。

## 常见误区

- **“user time 就是全部 CPU 时间”**：程序实际花费的 CPU 执行时间 = user time + sys time。
- **“提高主频没有代价”**：提高主频（开关频率）会增大功耗，带来耗电与散热问题。
- **“响应时间和吞吐率是一回事”**：响应时间关注单次执行快慢，吞吐率关注单位时间内的处理量。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| computer-performance-and-power-consumption-power | wikipedia-algorithmic-efficiency-power-v2 | 对电池供电设备或大型长时间计算，直接功耗与间接功耗都是需要关注的指标 |

## 待验证项

无。

## 关联知识

- [[cpu-and-memory]] —— 流水线、缓存与性能优化。
- [[cpu-cache-optimization]] —— 缓存命中率对性能的影响。
- [[cpu-history]] —— CPU 发展历史。
- [[soc]] —— 移动 SoC 的能效权衡。

## 详细章节

### 计算机性能和功耗

#### 性能

* 响应时间或者执行时间
  * 让计算机跑得更快
  * 响应时间指的是执行程序要花多少时间

* 吞吐率或者带宽
  * 让计算机搬得更多
  * 吞吐率在一定时间范围内到底能处理多少事情，处理的数据或者执行的程序指令



性能的定义：响应时间的倒数



SPEC提供CPU的基准测试程序



计算机的计时单位 

CPU时钟



统计时间 

程序运行结束的时间减去程序运行开始的时间

Wall clock time (elapsed time)

```shell
# linux 统计程序的时间
time 
```

* real time：运行程序，整个过程中流逝的时间
* user time：用户态运行指令的时间
* sys time：内核里运行指令的时间



程序实际花费CPU的执行时间 = user time + sys time



程序的CPU执行时间 = CPU时钟周期数 * 时钟周期时间



CPU时钟周期数 = 指令数 * 每条指令平均时钟周期数



#### 功耗

程序CPU的执行时间 = 指令数 * CPI * clock cycle time

要想提高计算机的性能，可以从**指令数**、**CPI**和**CPU主频**入手。

CPU又叫做超大规模集成电路。这些电路是由一个个晶体管组成的。CPU计算时，实际上就是让晶体管的开关不断去打开和关闭来组合成各种运算和功能。

要想计算得快，一方面我们可以在CPU同样的面积里面增加晶体管数量，也就是增加密度。另一方面，让晶体管的打开和关闭速度更快一点，也就是提高主频。而这两者都会增加功耗带来耗电和散热的问题。

CPU的面积变大晶体管之间的距离也会变大电传输的时间就变长，运算速度自然下降

在CPU里面能够放下晶体管的数量和晶体管开关的频率是有限的

功耗 ～= 1/2 * 负载电容 * 电压的平方 * 开关频率 * 晶体管数量
