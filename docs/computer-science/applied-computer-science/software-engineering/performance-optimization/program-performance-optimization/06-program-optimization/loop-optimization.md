# 循环级优化

## 循环不变量外提

### 基本概念

循环不变量是指在循环迭代空间内值不发生变化的变量。由于循环不变量的值在循环的迭代空间内不发生变化，因此可将其外提到循环外仅计算一次，避免其在循环体内重复计算。



#### 合法性

* 变换不能影响源程序的语义



#### 优点

* 削弱计算强度



#### 例子

优化前

```c++
for (int i = 0; i < m; i++) {
    for (int j = 0; j < n; j++) {
        a[i][j] = b[j] / (t * t);
    }
}
```



优化后

```c++
auto tmp = 1 / (t * t);
for (int i = 0; i < m; i++) {
    for (int j = 0; j < n; j++) {
        a[i][j] = b[j] * tmp;
    }
}
```



### 编译器中的循环不变量外提

#### LLVM

| 选项          | 功能                                                   |
| ------------- | ------------------------------------------------------ |
| `-Rpass=licm` | 执行循环不变代码移动，尝试从循环体中删除尽可能多的代码 |



## 循环展开和压紧

### 基础概念

* 循环展开：英文称loop unrolling，是一种牺牲程序的尺寸来加快程序的执行速度的优化方法，可以由程序员完成，也可由编译器自动优化完成。
  它通过将循环体内的代码复制多次的操作，进而减少循环分支指令执行的次数，增大处理器指令调度的空间，获得更多的指令级并行。
* 循环压紧：是指调整复制后的语句执行，将原来一条语句复制得到的多条语句合并到一起。



#### 优点

* 减少循环分支指令执行的次数；
* 获得了更多的指令级并行；
* 增加了寄存器的重用。



#### 例子

优化前

```c++
for (int i = 0; i < m; i++) {
    for (int j = 0; j < n; j++) {
        a[i][j] = b[i][j] + c[i][j] * d[i][j];
    }
}
```



优化后

```c++
for (int i = 0; i < m; i++) {
    int j = 0;
    for (; j < n - 3; j += 4) {
        a[i][j] = b[i][j] + c[i][j] * d[i][j];
        a[i][j + 1] = b[i][j + 1] + c[i][j + 1] * d[i][j + 1];
        a[i][j + 2] = b[i][j + 2] + c[i][j + 2] * d[i][j + 2];
        a[i][j + 3] = b[i][j + 3] + c[i][j + 3] * d[i][j + 3];
    }
    for (; j < n; j++) {
        a[i][j] = b[i][j] + c[i][j] * d[i][j];
    }
}
```



### 循环展开的合法性

* 循环展开需要在不影响原程序语义的情况下进行。



#### 例子

优化前

```c++
for (i = 0; i < m; i++) {
    for (j = 0; j < n; j++) {
        a[i + 1][j - 1] = a[i][j] + 3;
    }
}
```



优化后

```c++
for (i = 0; i < m; i += 2) {
    for (j = 0; j < n; j++) {
        a[i + 1][j - 1] = a[i][j] + 3;
        a[i + 2][j - 1] = a[i + 1][j] + 3;
    }
}
```



### 循环完全展开

* 循环完全展开：按照迭代次数对循环进行展开，该方法对循环嵌套的最内层循环或者向量化后的循环加速效果更明显。要注意的是并不是循环展开的次数越多获得的程序性能越高，过度地进行循环展开可能会增加寄存器的压力，可能会引起指令缓存区的溢出。



#### 例子

优化前

```c++
for (i = 0; i < 4; i++) {
    a[i] = a[i] + 3;
}
```



优化后

```c++
for (i = 0; i < 4; i++) {
    a[i] = a[i] + 3;
    a[i + 1] = a[i + 1] + 3;
    a[i + 2] = a[i + 2] + 3;
    a[i + 3] = a[i + 3] + 3;
}
```



### 尾循环处理

* 当迭代次数不能被循环展开次数整除的情况下，需要在进行循环展开的同时考虑尾循环的处理。



#### 例子

优化前

```c++
for (int j = 0; j < n; j++) {
    a[j] = b[j] + c[j] * d[j];
}
```



优化后

```c++
int j = 0;
for (; j < n - 3; j += 4) {
    a[j] = b[j] + c[j] * d[j];
    a[j + 1] = b[j + 1] + c[j + 1] * d[j + 1];
    a[j + 2] = b[j + 2] + c[j + 2] * d[j + 2];
    a[j + 3] = b[j + 3] + c[j + 3] * d[j + 3];
}
for (; j < n; j++) {
    a[j] = b[j] + c[j] * d[j];
}
```



### 编译器循环展开

#### LLVM

| 选项                        | 功能                               |
| --------------------------- | ---------------------------------- |
| `-funroll-loops`            | 打开循环展开                       |
| `-no-unroll-loops`          | 关闭循环展开                       |
| `-mllvm -unroll-max-count`  | 为部分和运行时展开设置最大展开计数 |
| `-mllvm -unroll-count`      | 确定展开次数                       |
| `-mllvm -unroll-runtime`    | 使用运行时行程计数展开循环         |
| `-mllvm -unroll-threshold`  | 设定循环展开的成本限值             |
| `-mllvm -unroll-remainder`  | 允许循环展开后有尾循环             |
| `-Rpass=loop-unroll`        | 显示循环展开的优化信息             |
| `-Rpass-missed=loop-unroll` | 显示循环展开失败的信息             |



### pragma指令循环展开

```c++
#pragma clang loop unroll(enable)
for (i = 0; i < N; i++) {
    sum = sum + a[i] + b[i];
}
```



```c++
#pragma clang loop unroll(full)
for (i = 0; i < N; i++) {
    sum = sum + a[i] + b[i];
}
```



```c++
#pragma clang loop unroll_count(8)
for (i = 0; i < N; i++) {
    sum = sum + a[i] + b[i];
}
```



### 向量化程序循环展开

* 可以针对向量化指令的程序进行循环展开，以进一步挖掘数据级的并行性，提高程序执行的性能。



## 循环合并

### 基础概念

循环合并，Loop Fusion，是将具有相同迭代空间的两个循环合成一个循环的过程，属于语句层次的循环变换。



#### 优点

*  减小循环的迭代开销
* 增强数据重用，寄存器重用
* 减小并行化的启动开销，消除合并前多个循环间的线程同步开销
* 增加循环优化的范围



#### 例子

优化前

```c++
for (int i = 0; i < n; i++) {
    x[i] = a[i] + b[i];
}
for (int i = 0; i < n; i++) {
    y[i] = a[i] - b[i];
}
```



优化后

```c++
for (int i = 0; i < n; i++) {
    x[i] = a[i] + b[i];
	y[i] = a[i] - b[i];
}
```



### 循环合并的合法性

并不是所有循环都可以进行合并，循环合并需要满足合法性要求，有些情况下循环合并会导致结果错误。满足合法性要求的循环合并可以减小循环的迭代开销以及并行化的启动和通信开销，还可能增强寄存器的重用。 

* 不能违反原来的依赖关系圈。如果两个循环之间存在一条循环无关的依赖路径，这条路径包含一个未与它们合并的循环语句，则它们不能披合并。
* 不能产生新的依赖。如果两个循环之间存在一个阻止合并的依赖，则它们不能被合并。



#### 错误例子

优化前

```c++
for (int i = 0; i < n; i++) {
    a[i] = b[i] + c;
}
for (int i = 0; i < n; i++) {
    d[i] = a[i + 1] + e;
}
```



优化后

```c++
for (int i = 0; i < n; i++) {
    a[i] = b[i] + c;
    d[i] = a[i + 1] + e;
}
```



### 循环合并的有利性

循环合并的一个重要应用场景为并行化，但并不是所有循环合并都可以给并行化带来收益，有以下两种情况：

* 分离限制：当一个并行循环和一个串行循环合并时，结果必然是串行执行的。
* 阻止并行性的依赖限制，当两个都可并行的循环存在一个阻止并行的依赖，进行循环合并后该依赖被合并后的循环携带。



#### 分离限制例子

优化前

```c++
for (i = 1; i < N; i++) {
    a[i] = b[i] + 1; // 并行循环
}
for (i = 1; i < N; i++) {
    c[i] = a[i] + c[i - 1]; // 串行循环
}
```



优化后

```c++
for (i = 1; i < N; i++) {
    a[i] = b[i] + 1;
    c[i] = a[i] + c[i - 1]; // 串行循环
}
```



#### 阻止并行性的依赖限制

优化前

```c++
for (i = 1; i < N; i++) {
    a[i + 1] = b[i] + 1;
}
for (i = 1; i < N; i++) {
    c[i] = a[i] + 1;
}
```



优化后

```c++
for (i = 1; i < N; i++) {
    a[i + 1] = b[i] + 1;
    c[i] = a[i] + 1; // 依赖a
}
```



### 编译器中的循环合并

#### LLVM

LLVM中进行循环合并需要满足以下条件：

* 两个循环必须相邻，即两个循环之间不能有语句。
* 两个循环必须有相同的迭代次数。
* 循环必须是等价的控制流，如果一个循环执行，另一个循环也保证执行。
* 循环之间不能有负距离依赖关系，比如两个循环，当第二个循环的迭代次数为m时，使用第一个循环在未来m+n次迭代时计算的值（其中n>0）。



| 选项                               | 功能                                |
| ---------------------------------- | ----------------------------------- |
| `-fproactive-loop-fusion-analysis` | 打开循环合并分析                    |
| `-proactive-loop-fusion`           | 打开循环合并优化                    |
| `-loop-fusion`                     | 通过opt工具对中间码进行循环合并优化 |



## 循环分布

### 基础概念

循环分布（Loop Distribute）是指将一个循环分解为多个循环，且每个循环都有与原循环相同的迭代空间，但只包含原循环的语句子集，常用于分解出可向量化或者可并行化的循环，进而将可向量化部分的代码转为向量执行。



#### 优点

- 将一个串行循环转变为多个并行循环
- 实现循环的部分并行化
- 增加循环优化的范围



#### 缺点

- 减小并行性粒度
- 增加额外的通信和同步开销



#### 例子

优化前

```c++
for (i = 1; i < N; i++) {
    a[i] = i;
    b[i] = b[i] + 2;
    c[i] = c[i - 1] + 3;
}
```



优化后

```c++
for (i = 1; i < N; i++) {
    a[i] = i;
    b[i] = b[i] + 2;
}
for (i = 1; i < N; i++) {
    c[i] = c[i - 1] + 3;
}
```



### 与循环交换优化的配合

若循环不是紧嵌套循环导致无法进行后续优化操作时，可以使用循环分布将循环体变换为紧嵌套循环。



#### 例子

优化前

```c++
for (i = 1; i < N; i++) {
    for (j = 1; j < N; j++) {
        A[i][j] = D; // S1语句
        for (k = 1; k < N; k++) {
        	A[i][j]= A[i][j] + B[i][k] * C[k][j]; // S2语句
        }
    }
}
```



优化后

```c++
for (i = 1; i < N; i++) {
    for (j = 1; j < N; j++) {
        A[i][j] = D; // S1语句
    }
}
for (i = 1; i < N; i++) {
    for (j = 1; j < N; j++) {
        for (k = 1; k < N; k++) {
        	A[i][j]= A[i][j] + B[i][k] * C[k][j]; // S2语句
        }
    }
}
```





### 与循环合并优化的配合

#### 例子

优化前

```c++
for(i = 1; i < N; i++){
    A[i] = B[i] + 1; // S1语句
    C[i] = A[i] + C[i-1]; // S2语句
    D[i] = A[i] + x; // S3语句
}
```



循环分布优化

```c++
for(i = 1; i < N; i++){
    A[i] = B[i] + 1; // S1语句
}
for(i = 1; i < N; i++){
    C[i] = A[i] + C[i-1]; // S2语句
}
for(i = 1; i < N; i++){
    D[i] = A[i] + x; // S3语句
}
```



循环合并优化

```c++
for(i = 1; i < N; i++){
    A[i] = B[i] + 1; // S1语句
    D[i] = A[i] + x; // S3语句
}
for(i = 1; i < N; i++){
    C[i] = A[i] + C[i-1]; // S2语句
}
```



### 编译器中的循环分布

#### LLVM

| 选项                              | 功能                       |
| --------------------------------- | -------------------------- |
| `-mllvm -enable-loop-distribute`  | 打开循环分布优化           |
| `-Rpass=loop-distribute`          | 提供循环分布优化成功的信息 |
| `-Rpass-missed=loop-distribute`   | 提供循环分布优化失败的信息 |
| `-Rpass-analysis=loop-distribute` | 提供循环分布优化失败的分析 |



#### GCC

| 选项                     | 功能             |
| ------------------------ | ---------------- |
| `-ftree-loop-distribute` | 打开循环分布优化 |



### pragma指令循环分布

```c++
#pragma clang loop distribute(enable) 
for (i = 0; i < N; ++i) {
    A[i + 1] = A[i] + B[i]; // S1
    C[i] = D[i] * E[i]; // S2
}
```





## 循环分段

### 基础概念

循环分段是将单层循环变换为两层嵌套循环，内层循环遍历的是迭代次数为strip的连续区域（或叫条带循环），外层循环的步进单位为strip，这个strip就是分段因子，分段因子需要根据硬件情况选取。如果原循环是可并行化的循环，则分段后依然可以实施并行化变换。通常采用循环分段技术实现外层的并行化以及内层的向量化，以达到利用系统多层次并行资源的目的。

由于循环分段语句并没有改变循环的迭代次序，因此循环分段总是合法的。如果原循环是可并行化的循环，则分段后依然可以实施并行化变换。通常情况下，采用循环分段技术实现外层的并行化以及内层的向量化，达到利用系统多层次并行资源的目的。



#### 优点

- 充分利用多个处理器资源
- 将可用的并行性转换成更适合硬件的形式



#### 例子1

优化前

```c++
for (int i = 0; i < n; i++) {
    x[i] = a[i] + b[i];
}
```



优化后

```c++
for(i = 0; i < N; i += k){    // 并行执行
    for(j = i; j <= i + k - 1; j++) {
    	A[j] = B[j] + C[j];    // 向量执行
    }
}
```



#### 例子2

优化前

```c++
for (int i = 0; i < n; i++) {
    x[i] = a[i] + b[i];
}
```



优化后

```c++
constexpr int K = 32;
int i = 0
for (; i < n - K + 1; i += K) {
    for (int j = i; j < i + K - 1; j += 4) {
        ymm0 = _mm_load_ps(B + j);
		ymm1 = _mm_load_ps(C + j);
		ymm2 = _mm_add_ps(ymm0, ymm1);
		_mm_storeu_ps(A + j, ymm2);
    }
}
for (; i < n; i++) {
    x[i] = a[i] + b[i];
}
```



#### 不适用例子

在内层循环中每次迭代调用的数组`A[i][j]`的数量都不同，找到一个有效的平衡点很难，通常宁愿选择一个较小的分段大小，而不是把并行循环平均分到处理其中，这样当负担较重的处理器还在执行时，执行结束较早的处理器可以承担一些过剩的工作。

```c++
for(i = 1; i < SIZE; i++){
    for(j = 1; j < i; j++) {
    	A[i][j] = A[i][j - 1] + B[i];
    }
}
```





## 循环交换

### 基础概念

当一个循环体中包含一个以上的循环，且循环语句之间不包含其它语句，则称这个循环为**紧嵌套循环**，交换紧嵌套中两个循环的嵌套顺序是提高程序性能最有效的变换之一。实际上，**循环交换**是一个重排序变换，仅改变了参数化迭代的执行顺序，但是并没有删除任何语句或产生任何新的语句，所以循环交换的合法性需要通过循环的依赖关系进行判定。

循环交换增强数据局部性方面有所帮助，而且在程序的提高向量化和并行化的效果。



#### 优点

- 增强数据局部性
- 增强向量化和并行化的识别



#### 例子

优化前

```c++
for (j = 0; j < N; j++) {
    for (k = 0; k < N; k++) {
        for (i = 0; i < N; i++) {
            a[i][j] = a[i][j] + b[i][k] * c[k][j];
        }
    }
}
```



优化后

```c++
for (j = 0; j < N; j++) {
    for (i = 0; i < N; i++) {
        for (k = 0; k < N; k++) {
            a[i][j] = a[i][j] + b[i][k] * c[k][j];
        }
    }
}
```



### 循环交换的有利性

#### 例子1

最内层的循环存在循环携带依赖，而导致循环无法进行并行化，向量化的效果变差。如果交换这两个循环，依赖关系就变为由外层循环携带，而内层循环不携带依赖，就可以进行并行化，或者把可向量化的循环移动到最内层而提高向量化效果。



优化前

```c++
for(i = 1;i < N;i++)
    for(j = 1;j < N;j++)
        A[i][j + 1] = A[i][j] + 2;
```



优化后

```c++
for(j = 1;j < N;j++)
    for(i = 1;i < N;i++)
        A[i][j + 1] = A[i][j] + 2;
```



#### 例子2

内层循环每一次迭代都需要进行存储和读取操作，共需`M*N`次，寄存器重用较少。进行循环交换后，仍然需要`M*N`次的存储操作，但读取操作的次数减少到了N次，即第一行的每个值都放在寄存器里被重用了M次。循环交换还可以提高寄存器的重用能力，把携带依赖的循环放在最内层的位置，使可以被重用的值保留在寄存器中。



优化前

```c++
for (j = 1; j < N; j++)
   for (i = 1; i < M; i++)
        A[i][j] = A[i - 1][j];	
```



优化后

```c++
for (i = 1; i < M; i++)
    for (j = 1; j < N; j++)
        A[i][j] = A[i - 1][j];
```



### 循环交换的合法性

重排序某个依赖端点的循环交换是不合法的，即不要引起依赖关系的反转。



#### 错误例子

优化前

```c++
for(j = 1; j < N; j++)
    for(i = 1; i < N; i++)
    	A[i][j + 1] = A[i + 1][j] + 2;
```



优化后

```c++
for(i = 1; i < N; i++)
    for(j = 1; j < N; j++)
    	A[i][j + 1] = A[i + 1][j] + 2;
```





### 编译器中的循环交换

| 编译器 | 选项                             |
| ------ | -------------------------------- |
| LLVM   | `-mllvm -enable-loopinterchange` |
| GCC    | `-floop-interchange`             |





## 循环分块

### 基础概念

**循环分块是指通过增加循环嵌套的维度来提升数据局部性的循环变换技术，是对多重循环的迭代空间进行重新划分的过程**，循环分块前后要保证迭代空间相同。循环分块是循环交换和循环分段的结合。可以提高程序的局部性，增加数据重用来提升程序的性能。

在计算机存取数据，需要从主存将数据取到寄存器中，这一过程为了是数据存取更有效率，在主存和寄存器中会存在一个高速缓存Cache，缓存常用的数据，但存储量很少，通常当某个数据现在被用过以后，后面还会被用，但是按循环默认的执行方式，可能到下次再被用到的时候就已经从高速缓存行Cache中被消除了，于是重排循环，减少内层循环的迭代量，使得一个cache line在被消除之前会被再次使用。

* **时间局部性**：如果程序中的某条指令或某个数据被访问过，不久以后该指令或该数据可能再次被访问。

* **空间局部性**：一旦程序访问了某个存储单元，在不久之后，其附近的存储单元也将被访问。

C语言访存数据是行优先的原则，设置S长度与硬件平台高速缓存行相匹配，将控制这些分段上进行迭代的循环移动最外层的位置，这样单次迭代数据量得到了大幅度的减少，减少了从主存取数的时间，进而提升了性能。



#### 例子

优化前

```c++
for (j = 0;j < M; j++) {
    for (i = 0; i < N; i++) {
        b[i] += a[i][j];
    }
}
```



循环分段

```c++
step = 4;
for (j = 0; j < M; j++) {
    for (i = 0; i < N; i += step) {
        for (k = i; k < min(i + step, N); k++) {
            b[k] += a[k][j];
        }
    }
}
```



循环交换

```c++
step = 4;
for (i = 0; i < N; i += step) {
    for (j = 0; j < M; j++) {
        for (k = i; k < min(i + step, N); k++) {
            b[k] += a[k][j];
        }
    }
}
```



### 三层嵌套循环

#### 例子

优化前

```c++
for (i = 0; i < I; i++) {
    for (j = 0; j < J; j++) {
        for (k = 0; k < K; k++) {
            c[i][j] = a[i][k] * b[k][j];
        }
    }
}
```



第一次循环分块

```c++
for (k = 0; k < K; k += s) {
    for (i = 0; i < I; i++) {
    	for (j = 0; j < J; j++) {
        	for (k_ = k; k_ < min(k + s, K); k_++) {
            	c[i][j] = a[i][k_] * b[k_][j];
            }
        }
    }
}
```



第二次循环分块

```c++
for (j = 0; j < J; j += s) {
	for (k = 0; k < K; k += s) {
    	for (i = 0; i < I; i++) {
    		for (j_ = j; j_ < min(j + s, J); j_++) {
        		for (k_ = k; k_ < min(k + s, K); k_++) {
            		c[i][j_] = a[i][k_] * b[k_][j_];
                }
            }
        }
    }
}
```



第三次循环分块

```c++
for (i = 0; i < I; i += s) {
	for (j = 0; j < J; j += s) {
		for (k = 0; k < K; k += s) {
    		for (i_ = i; i_ < min(i + s, I); i_++) {
    			for (j_ = j; j_ < min(j + s, J); j_++) {
        			for (k_ = k; k_ < min(k + s, K); k_++) {
            			c[i_][j_] = a[i_][k_] * b[k_][j_];
                    }
                }
            }
        }
    }
}
```







## 循环分裂

### 基础概念

循环分裂是对循环的迭代次数进行拆分，将循环的迭代次数拆成两段或者多段，但是拆分后的循环不存在主体循环之说，也就是拆分成迭代次数都比较多的两个或者多个循环。



#### 例子

优化前

```c++
for (i = 0; i < N; i++) {
    a[i] = a[i] + a[M];
}
```



优化后

```c++
for (i = 0; i < M; i++) {
    a[i] = a[i] + a[M];
}
for (i = M + 1; i < N; i++) {
    a[i] = a[i] + a[M];
}
```





## 循环倾斜

### 基础概念

循环倾斜是一种改变迭代空间形式的变换，用于挖掘循环中的并行潜能的优化方式，可以把存在的并行性用传统的并行循环的形式表示出来。



#### 例子

优化前

```c++
for (i = 1; i < 4; i++) {
    for (j = 1; j < 4; j++) {
        a[i][j] = a[i][j - 1] + a[i - 1][j];
    }
}
```



循环倾斜

```c++
for (i = 1; i < 4; i++) {
    for (j = i + 1; j < i + 4; j++) {
        a[i][j - i] = a[i][j - i - 1] + a[i - 1][j - i];
    }
}
```



循环交换

```c++
for (j = 2; j < 8; j++) {
    for (i = max(1, j - 4); i < min(j - 1, 4); i++) {
        a[i][j - i] = a[i][j - i - 1] + a[i - 1][j - i];
    }
}
```





## 参考

* [自编教材分享：第六章—程序编写优化（四）](https://www.bilibili.com/video/BV1rh411A79q/?share_source=copy_web&vd_source=0137e09b2de139e28a9cbd41a02033fe)
* [循环优化（一）：循环展开和压紧](https://www.bilibili.com/video/BV1HB4y1x7zv/?share_source=copy_web&vd_source=0137e09b2de139e28a9cbd41a02033fe)
* [循环优化（二）：循环合并](https://www.bilibili.com/video/BV1CD4y1B7H2/?share_source=copy_web&vd_source=0137e09b2de139e28a9cbd41a02033fe)

* [循环优化（三）：循环分布](https://www.bilibili.com/video/BV1Z8411t7dC/?share_source=copy_web&vd_source=0137e09b2de139e28a9cbd41a02033fe)
* [循环优化（四）：循环交换](https://www.bilibili.com/video/BV13d4y1C7ca/?share_source=copy_web&vd_source=0137e09b2de139e28a9cbd41a02033fe)
* [循环优化（五）：循环不变量外提](https://www.bilibili.com/video/BV1Ud4y1b7Zc/?share_source=copy_web&vd_source=0137e09b2de139e28a9cbd41a02033fe)
* [循环优化（六）：循环分段](https://www.bilibili.com/video/BV1Zs4y1s7zn/?share_source=copy_web&vd_source=0137e09b2de139e28a9cbd41a02033fe)
* [循环优化（七）：循环分块](https://www.bilibili.com/video/BV1gv4y1Y7ed/?share_source=copy_web&vd_source=0137e09b2de139e28a9cbd41a02033fe)
* [循环优化（八）：循环分裂](https://www.bilibili.com/video/BV1mb411f7wK/?share_source=copy_web&vd_source=0137e09b2de139e28a9cbd41a02033fe)
* [循环优化（九）：循环倾斜](https://www.bilibili.com/video/BV1uV4y1f7cJ/?share_source=copy_web&vd_source=0137e09b2de139e28a9cbd41a02033fe)

