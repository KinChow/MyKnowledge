# Systrace

## 简介

Systrace 是 Android4.1 中新增的性能数据采样和分析工具

* ﻿内核部分：Systrace 利用了 Linux Kernel 中的 ftrace 功能。
* ﻿数据输出：Android 定义了一个 Trace 类。应用程序可利用该类把统计信息输出给ftrace。同时，Android 还有一个 atrace 程序，它可以从 ftrace 中读取统计信息然后交给数据分析工具来处理。
* ﻿数据抓取&分析：Android 提供一个systrace.py（python 脚本文件，位于 Android SDK目录/platform-tools/systrace 中，其内部将调用 atrace 程序）用来配置数据采集的方式（如采集数据的标签、输出文件名等）和收集 ftrace 统计数据并生成一个结果网页文件供用户查看。

从本质上说，systrace 是对 Linux Kernel中 ftrace 的封装。应用进程需要利用 Android 提供的 Trace 类来使用 systrace



systrace官方介绍和使用：http://developer.android.com/topic/performance/tracing?hl=zh-cn



## 使用

### 数据输出：代码添加 Systrace

#### 应用内

```java
import android.os.Trace;
Trace.beginSection("TEST");
Trace.endSection();
```

添加systrace跟踪，然后通过python systrace.py --app=TEST 指定apk。



#### framework java层

```java
import android.os.Trace;
Trace.traceBegin(Trace.TRACE_TAG_VIEW, "performTraversals");
Trace.traceEnd(Trace.TRACE_TAG_VIEW);
```



#### framework native

```c++
#include <utils/Trace.h>
#define ATRACE_TAG ATRACE_TAG_INPUT
ATRACE_CALL();
std::string message = StringPrintf("time=%" PRId64 ")", eventTime);
ATRACE_NAME(message.c_str());
```



```c++
#include <cutils/trace.h>
#define ATRACE_TAG ATRACE_TAG_INPUT
ATRACE_BEGIN("TEST");
ATRACE_END();
```



#### 对具体数值进行跟踪

```c++
void InputDispatcher::traceInboundQueueLengthLocked()
{
    if (ATRACE_ENABLED()) {
    	ATRACE_INT("iq", mInboundQueue.count());
    }
}
```





### 抓取systrace

```shell
python systrace.py [options] [category1] [category2] .. [categoryN]
python systrace.py -o trace.html gfx input view wm am sm pm hal res sched freq
```





### systrace分析

* ﻿﻿chrome://tracing/
    * ﻿﻿传统的systrace分析工具
    * ﻿﻿方便查看线程运行状态
* https://ui.perfetto.dev/#!/record/instructions
    * ﻿﻿谷歌提供的新版解析工具，各有优劣
    * ﻿﻿界面友好，运行更流畅
    * ﻿﻿线程唤醒关系清晰



### 抓取配置

* -o < FILE >
    * 输出的目标文件
* -t N, -time=N
    * 执行时间，默认5s
* -b N, -buf-size=N
    * buffer大小（单位kB），用于限制trace总大小，默认无上限
* -k< KFUNCS>, -ktrace=< KFUNCS >
    * 追踪kernel函数，用逗号分隔
* -a < APP_NAME >, -app=< APP_NAME >
    * 追踪应用包名，用逗号分隔
* -from-file=< FROM_FILE >
    * 从文件中创建互动的systrace
* -e < DEVICE_SERIAL >, - serial=< DEVICE_SERIAL >
    * 指定设备
* -l, -list-categories
    * 列举可用的tags



## 线程的运行状态

查看线程状态，判断线程是运行还是不可运行可以再进一步做阻塞分析



线程状态

* 运行中（running）
    * 可以了解任务执行在哪个核上，大核还是小核，运行核的频点对不对，任务的优先级多少
* 可运行状态（runnable）
    * 可以运行但是当前没有能被CPU调度，等待被调度后运行
    * 如果runnable的时间越长表示CPU调度越忙，这个线程的任务不能及时处理。还可以看到被哪个线程唤醒，之后进入到running状态。
    * runnable很长的时候可以看下是不是CPU太满了*（跑的任务很多），或者一直频点不够
    * 一个任务在进入 Running 状态之前，会先进入 Runnable 状态进行等待，可以查看到
* 睡眠（sleeping）
    * 没有任务执行，等待被唤醒
* 不可中断的睡眠态 Block I/O（uninterruptible sleep - Block I/O）
    * 线程在I/O上被阻塞或等待磁盘操作完成。这个出现的时候可能是一些磁盘读写操作 I/O操作慢了
* 不可中断的睡眠态（uninterruptible sleep）
    * 内核中的一些阻塞，需要具体分析，大量长时间出现时非正常