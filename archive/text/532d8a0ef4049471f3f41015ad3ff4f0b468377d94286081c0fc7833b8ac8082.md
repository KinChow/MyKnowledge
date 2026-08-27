# cache优化

## 软件预取

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
    "prfm PLDL1KEEP, [%0，#(%1)]"
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




## 热点汇聚

### 数据汇聚



### 指令汇聚

```c++
#define unlikely(x) __builtin_expect(!!(x), 0)
#define likely(x) __builtin_expect(!!(x), 1)
```

这里的`__builtin_expect()`函数是`gcc`的内建函数，编译器在编译过程中，会将可能性更大的代码紧跟着后面的代码，将可能性较小的分支挪到代码末尾，这样在就指令预取时就可以将更可能执行的指令预取到cache中。这样添加了指令cache的命中率，减少了指令跳转带来的性能上的下降。