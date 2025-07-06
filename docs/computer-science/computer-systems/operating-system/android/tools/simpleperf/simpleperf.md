# Simpleperf

## 概述

Simpleperf是Android平台的一个本地层性能分析工具，分析Android应用在CPU执行流程，帮忙找到Java、Kotlin或C/C++编写的应用热点（占用应用大部分执行时间的部分原生代码）。

Simpleperf的命令与Linux的perf工具类似，支持Android特有的改进。



## 使用

Simpleperf具有三个主要的功能：stat、record和report。

* stat命令给出了在一个时间段内被分析的进程中发生了多少事件的摘要。
* record命令在一段时间内记录剖析进程的样本。
* report命令读取perf.data文件及所有被剖析进程用到的共享库，并输出一份报告，展示时间消耗在了哪里。



### stat

```shell
# simpleperf stat [options] [command [command-args]]
simpleperf stat -p 进程号 --duration 检测进程的持续时间(秒)
```



### record

```shell
# simpleperf record [options] [command [command-args]]
simpleperf record -p 进程号 -o 输出文件(默认perf.data) --duration 监测进程的持续时间(秒)
```



如果出现`Access to kernel symbol addresses is restricted`的警告，需要使用一下命令来取消

```shell
echo 0 > /proc/sys/kernel/kptr_restrict
```



### report

```shell
# simpleperf report [options]
simpleperf report --dsos 选定动态共享对象(so库)  -f 记录文件(默认perf.data) --sort 用于排序和打印报告的键 -n
```

如果使用report命令进行查找的时候，发现so现实的symbol都是地址，而不是函数内容。这多数是因为在安卓编译的时候，设备上使用的so库已经被strip过，也就是说，已经抛离了.symbol段的内容。

那么，我们需要将带有symbol信息的so下载到设备上。同时需要将so放置到perf.data中记录的相同的路径(否则，Simpleperf无法找到它)。

如果找不到路径，可以在perf.data文件中直接搜索需要选定的so库的名称，即可查看到路径。





## 原理

现代的CPU具有一个硬件组件，称为性能监控单元（PMU）。PMU具有一些硬件计数器，计数一些诸如经历了多少次CPU周期，执行了多少条指令，或发生了多少次缓存未命中等的事件。

Linux内核将这些硬件计数器包装到硬件perf事件（hardware perf events）中。此外，Linux内核还提供了独立于硬件的软件事件和跟踪点事件。Linux内核通过perf_event_open系统调用将这些都暴露给了用户空间。



### stat

* 给定用户选项，Simpleperf通过对Linux内核进行系统调用来启用分析；
* Linux内核在调度到被分析进程时启用计数器；
* 分析之后，Simpleperf从内核读取计数器，并报告计数器摘要。



### record

* 给定用户选项，Simpleperf通过对Linux内核进行系统调用来启用分析；
* 在Simpleperf和Linux内核之间创建映射缓冲区；
* Linux内核在调度到被分析进程时启用计数器；
* 每次给定数量的事件发生时，Linux内核将样本转储到映射缓冲区；
* Simpleperf从映射缓冲区读取样本并生成perf.data。



## 参考

https://developer.android.com/ndk/guides/simpleperf?hl=zh-cn

https://blog.csdn.net/qq_38410730/article/details/103481429

https://blog.csdn.net/chaihuasong/article/details/110475287

https://android.googlesource.com/platform/system/extras/+/master/simpleperf/doc/README.md



