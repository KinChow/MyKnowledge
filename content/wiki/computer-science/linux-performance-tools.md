---
aliases: []
confidentiality: public
domain: computer-science
evidence:
- claim: 'linux 自身有很多性能分析工具。并且提供了详细的输出格式。熟练掌握这些工具可以帮助我们更快的发现性能瓶颈，为性能调优提供思路。

    load average：平均负载

    PID：进程号

    USER：进程所有者的名字。

    PRI：进程优先级

    NI nice：级别

    SIZE：进程使用的内存（代码、数据和栈），kb 单位

    RSS：物理 RAM 使用量，kb 单位

    SHARE：和其它进程共享的内存，kb 单位

    STAT 进程状态 S 睡眠，R=运行，T=停止或跟踪，D=不可中断的睡眠，Z=僵尸。

    %CPU CPU 使用量。'
  claim_id: linux-performance-tools-audit-1
  support: direct
  supporting_quotes:
  - evidence_id: evidence-15ffe98b6e3c
    exact: 'linux 自身有很多性能分析工具。并且提供了详细的输出格式。熟练掌握这些工具可以帮助我们更快的发现性能瓶颈，为性能调优提供思路。

      load average：平均负载

      PID：进程号

      USER：进程所有者的名字。

      PRI：进程优先级

      NI nice：级别

      SIZE：进程使用的内存（代码、数据和栈），kb 单位

      RSS：物理 RAM 使用量，kb 单位

      SHARE：和其它进程共享的内存，kb 单位

      STAT 进程状态 S 睡眠，R=运行，T=停止或跟踪，D=不可中断的睡眠，Z=僵尸。

      %CPU CPU 使用量。'
  targets:
  - evidence_id: evidence-15ffe98b6e3c
    source_id: web-computer-science-linux-performance-tools
id: linux-performance-tools
kind: reference
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-linux-performance-tools
- working-computer-science-linux-performance-tools
status: published
tags:
- linux
- performance
- tools
- profiling
title: linux性能分析工具
updated_at: '2026-09-06'
---
# linux性能分析工具

## 详细章节

### linux性能分析工具

#### 工具

##### 列表

| 常用工具  | 功能                                      |
| --------- | ----------------------------------------- |
| top       | 展示所有进程信息                          |
| vmstat    | 展示详细的系统，硬件，信息                |
| lscpu     | cpu 信息查看                              |
| sysstat   | 工具集，包括 sar，mpstat，iostat，pidstat |
| ps        | 显示进程信息                              |
| free      | 显示内存使用情况                          |
| strace    | 拦截进程的系统调用                        |
| netstat   | 统计网络信息                              |
| sysbench  | 进程模拟工具                              |
| stress-ng | 模拟 cpu 压力                             |
| iozone    | IO 测试工具                               |







#### 参考

https://testerhome.com/topics/21513/show_wechat
