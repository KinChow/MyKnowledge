---
aliases: []
confidentiality: public
domain: computer-science
evidence:
- claim: To perform more fine-grained optimization of in-memory algorithms, we have
    to start taking into account the many specific details of the CPU cache system.
  claim_id: cpu-cache-optimization-audit-1
  support: direct
  supporting_quotes:
  - evidence_id: evidence-9b7a55f92851
    exact: To perform more fine-grained optimization of in-memory algorithms, we have
      to start taking into account the many specific details of the CPU cache system.
  targets:
  - evidence_id: evidence-9b7a55f92851
    source_id: algorithmica-cpu-cache
id: cpu-cache-optimization
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- algorithmica-cpu-cache
- algorithmica-cache-latency
- working-computer-science-cpu-cache-optimization
status: published
tags:
- architecture
- cpu
- cache
- performance
title: cache优化
updated_at: '2026-09-06'
---
# cache优化

## 一句话结论

当硬件预取无法取得较低的 cache miss 时，可通过**软件预取**（GCC `__builtin_prefetch`、ARM `prfm` 汇编）与**热点汇聚**（数据/指令布局、`likely`/`unlikely` 提示编译器）把后续可能用到的数据提前调入 cache，提升 cache 命中率、减少 CPU 等待内存的时间，进而提升运行效率。

## 核心概念

- **软件预取**：在程序中显式插入预取指令/内置函数，把后续可能用到的数据提前加载到 cache。
- **`__builtin_prefetch(addr, rw, locality)`**：`addr` 为预取地址；`rw` 指示读/写，0 为读、1 为写；`locality` 表示局部性，0 表示数据读取后不再使用，3 表示很可能再次被访问，1/2 介于两者之间。
- **ARM `prfm` 指令**：`PREM prop, [Xn|SP{, #pimm}]`；`prop` 由 `<type>`（PLD 数据预加载 / PLI 指令预取 / PST 数据预存储）、`<target>`（L1/L2/L3）、`<policy>`（KEEP 使用后保存 / STRM 流式淘汰）三部分组成。
- **热点汇聚**：数据汇聚与指令汇聚——把热点代码/数据聚拢以提高 cache 命中率。

## 工作机制

- 软件预取将后续可能使用到的数据提前加载到 cache，提升 cache 命中率，减少 CPU 等待数据从内存加载的时间。
- 内置函数不满足需求时，可用内联汇编调用 `prfm`：以 `ptr` 为基地址、`128` 为立即数偏移量，偏移 128 字节作为预取地址，预取一个 cache line 的数据。
- `__builtin_expect()` 是 GCC 内建函数：编译时把可能性更大的代码紧跟在判断之后，将可能性较小的分支挪到代码末尾，使指令预取时更可能把"更可能执行"的指令预取进 cache，提高指令 cache 命中率、减少指令跳转带来的性能下降。

## 示例或代码

```c++
__builtin_prefetch (const void *addr, int rw, int locality)
```

内联汇编软件预取：

```c++
__asm__ volatile(
    "prfm PLDL1KEEP, [%0,#(%1)]"
    ::"r"(ptr), "i"(128)
);
```

`likely`/`unlikely` 定义：

```c++
#define unlikely(x) __builtin_expect(!!(x), 0)
#define likely(x) __builtin_expect(!!(x), 1)
```

## 常见误区

- **“locality 数值越大表示越早丢弃”**：`locality` 0 表示数据读取后不再使用，3 表示很可能再次被访问，数值越大越应被保留。
- **“软件预取一定比硬件预取好”**：软件预取是在硬件预取无法取得较低 cache miss 的情况下的补充手段。
- **“prfm 只针对数据读”**：`<type>` 还有 PLI（指令预取）与 PST（数据预存储）等类型。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| cpu-cache-optimization-audit-1 | algorithmica-cpu-cache | 做内存内算法的细粒度优化必须考虑 CPU 缓存系统的具体细节 |

## 待验证项

无。

## 关联知识

- [[cpu-and-memory]] —— 缓存结构、地址映射、替换策略与虚拟内存。
- [[computer-performance-and-power-consumption]] —— 性能度量与访存延迟。
- [[algorithm-optimization]] —— 算法层面的优化手段。

## 详细章节

### cache优化

#### 软件预取

在硬件预取无法取得较低的Cache-miss的情况下，可以尝试软件预取将后续可能使用到的数据提前加载到cache中，进而提升cache命中率，减少CPU等待数据从内存中加载的时间，进而提升软件的运行效率。
在GCC編译器下，可以调用内置的预取函数完成预取：

```c++
__builtin_prefetch (const void *addr, int rw, int locality)
```

* 参数`addr`表示要进行预取的地址；

* `rw`和`locality`都是可选的参数。

  * `rw`用于指示读/写，0为读，1为写。

  * `locality`表示局部性，0表示数据读取后不再使用，3表示数据将很可能被再次访问，数值1/2介于两者之间。



如果内置的函数无法满足需求，可以使用内联汇编，调用相应的汇编指令进行软件预取。

```c++
__asm__ volatile(
    "prfm PLDL1KEEP, [%0,#(%1)]"
    ::"r"(ptr), "i"(128)
);
```

代码中参数`ptr`用于基地址，`128`为立即数偏移量，表示以`ptr`中的数值作为基地址，偏移128字节作为预取的地址，预取一个cacheLine的数据。



汇编指令的格式如下：

```c++
PREM prop, [Xn|SP{, #pimm}]
```

prop由`<type>`、`<target>`、`<policy>`三部分组成。

* `<type>`：

  * PLD：数据预加载；

  * PLI：指令预取；

  * PST；数据预存储

* `<target>`：

  * L1、L2、L3分别表示对三个不同的cache层级进行操作。

* `<policy>`：

  * KEEP：数据预取使用后保存一定时间；

  * STRM：流式或非临时预取，数据使用后将淘汰；
  * `XnlSP`为基地址
  * `#pimn`为可选的偏移量





#### 热点汇聚

##### 数据汇聚



##### 指令汇聚

```c++
#define unlikely(x) __builtin_expect(!!(x), 0)
#define likely(x) __builtin_expect(!!(x), 1)
```

这里的`__builtin_expect()`函数是`gcc`的内建函数，编译器在编译过程中，会将可能性更大的代码紧跟着后面的代码，将可能性较小的分支挪到代码末尾，这样在就指令预取时就可以将更可能执行的指令预取到cache中。这样添加了指令cache的命中率，减少了指令跳转带来的性能上的下降。
