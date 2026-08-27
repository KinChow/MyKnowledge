# C++并发编程及CUDA

## 并发和并行

* 并发是逻辑上的同时发生 （Simultaneous）
    * 能处理多个同时性活动的能力，并发事件之间不一定要同一时刻发生。
* 并行是是物理上的同时发生
    * 是指同时发生的两个并发事件，具有并发的含义，而并发则不一定并行。



## 进程与线程

### 进程、线程、协程

* 进程是对运行时程序的封装，是系统进行资源调度和分配的的基本单位，实现了操作系统的并发。
*  线程是进程的子任务，是CPU调度和分派的基本单位，用于保证程序的实时性，实现进程内部的并发；
    *  线程是操作系统可识别的最小执行和调度单位。
    *  每个线程都独自占用一个虚拟处理器：独自的寄存器组，指令计数器和处理器状态。
    *  每个线程完成不同的任务，但是共享同一地址空间（也就是同样的动态内存，映射文件，目标代码等等），打开的文件队列和其他内核资源。
* 协程，又称微线程，是一种用户态的轻量级线程，协程的调度完全由用户控制（也就是在用户态执行）。
    * 协程拥有自己的寄存器上下文和栈。
    * 协程调度切换时，将寄存器上下文和栈保存到线程的堆区，在切回来的时候，恢复先前保存的寄存器上下文和栈，直接操作栈则基本没有内核切换的开销，可以不加锁的访问全局变量
    * 上下文的切换快



### 多线程的优缺点

*   优点
    * 程序响应更快（如UI界面）
    * 资源利用效率
    *   多核系统下能大幅提升性能
*   缺点
    *   资源消耗（thread 是系统资源）
    *   切换开销
    *  复杂度（设计、开发、测试）
* 库
    * posix thread (pthread)
    * C++11 thread




### C++ thread

C++11标准库的线程封装类
C++11开始提供了对多线程的支持。标准库提供了std::thread类来创建和管理线程，std::mutex 用于互斥锁，std::future类模板来获取异步操作的结果，等等。



#### 线程创建

一个线程对象关联着一个执行线程，或者说它拥有（own）一个线程实体。std::thread 不支持拷贝，但支持移动，这意味着我们可以将一个执行线程从一个线程对象移动到另一个线程对象

```c++
std::thread t2(std::move(t1));
```





#### 线程执行体

std:thread的执行体并不要求必须是普通的函数，可以是任何可调用（Callable）的对象

* lambda表达式
* 重载了operator()的类的对象
* 使用std::bind表达式绑定对象和其非静态成员函数
* 使用lambda表达式调用对象的非静态成员函数



#### 线程管理函数

在任何一个时间点上，线程是可结合的（joinable），或者是分离的 （detached）。一个可结合的线程能够被其他线程收回其资源和杀死；在被其他线程回收之前，它的存储器资源（如栈）是不释放的。相反，一个分离的线程是不能被其他线程回收或杀死的，它的存储器资源在它终止时由系统自动释放。

为了防止忘记调用join，可以使用RAII技法管理线程回收

为了防止忘记调用join 或 detach，我们可以使用 RAII技法管理线程的回收：

```c++
class thread_guard
{
	std::thread &t_;
public:
    explicit thread_guard(std:thread &t) : t_(t) {}
    thread_guard(const thread_guard &) = delete;
    thread_guard &operator= (const thread guard&) = delete;
    ~thread_guard()
    { 
        if (t_.joinable()) {
            t_.join();
        }
    }
};
```



std::this_thread命名空间中也定义了一系列函数用于管理当前线程。
* yield
    * 建议线程调度者执行其他线程，相当于主动让出剩下的执行时间，具体调度算法取决于实现。
* get_id
    * 获取当前线程的线程id。
* sleep_for
    * 指定的一段时间内停止当前线程的执行。
* sleep_until
    * 停止当前线程的执行直到指定的时间点。



## C++ mutex与死锁，使用RAII管理多线程资源

### 为什么要有互斥锁

共享空间

* 代码段
* 数据段
* 进程空间
* 打开的文件



线程有共享空间

*  对共享资源的访问会造成竞争问题
*  确定不会造成写数据时的冲突



### 互斥（Mutex: Mutual Exclusion）

* std::mutex
    * 最简单的互斥对象。
* std::timed_mutex
    * 带有超时机制的互斥对象，允许等待一段时间或直到某个时间点仍未能获得互斥对象的所有权时放弃等待。
* std: recursive_mutex
    * 允许被同一个线程递归的Lock和Unlock。
* std::recursive_timed_mutex
* std::shared_timed_mutex（C++14）
    * 允许多个线程共享所有权的互斥对象，如读写锁。



### 死锁

对多个互斥对象进行加锁，有可能会发生死锁

解决办法
* 能否只用1个锁
* 加锁顺序一致
* 使用 std::lock(mtx1, mtx2)同时加锁



### 使用RAII管理互斥对象

C++通常使用RAll（Resource Acquisition Is Initialization）来自动管理资源。如果可能应总是使用标准库提供的互斥对象管理类模板。

* std: lock_guard
    * 严格基于作用域（scope-based）的锁管理类模板，构造时是否加锁是可选的（不加锁时假定当前线程已经获得锁的所有权），析构时自动释放锁，所有权不可转移，对象生存期内不允许手动加锁和释放锁。
* std::unique_lock
    * 更加灵活的锁管理类模板，构造时是否加锁是可选的，在对象析构时如果持有锁会自动释放锁，所有权可以转移。对象生命期内允许手动加锁和释放锁。
* std::shared_lock(C++14)
    * 用于管理可转移和共享所有权的互斥对象。



### 互斥对象管理类模板的加锁策略

策略

* （默认）
    * 无
    * 请求锁，阻塞当前线程直到成功获得锁。
* std: defer_lock
    * std: defer_lock_t
    * 不请求锁。
* std::try_to_lock
    * std::try_to_lock_t
    * 尝试请求锁，但不阻塞线程，锁不可用时也会立即返回。
* std::adopt_lock
    * std::adopt_lock_t
    * 假定当前线程已经获得互斥对象的所有权，所以不再请求锁。



### 条件变量（condition variable）

条件变量是一种同步原语（Synchronization Primitive）用于多线程之间的通信，它可以阻塞一个或同时阻塞多个线程直到：

*  收到来自其他线程的通知
*   超时
*   发生虚假唤醒（Spurious Wakeup）



#### C++11为条件变量提供了两个类

*  std::condltion_Variable：必须与std:unique_lock配合使用
*   std::condition_varable_any：更加通用的条件变量，可以与任意类型的配合使用，相比前者使用时会有额外的开销
二者具有相同的成员函数



#### 条件变量为什么叫条件变量？

* 条件变量存在虚假唤醒的情况，因此在线程被唤醒后需要检查条件是否满足
* 无论是notify_one或notfiy_all都是类似于发出脉冲信号，如果对wait调用发生在notify之后是不会被唤醒的，所以接收者在使用wait等待之前也需要检查条件（标识）是否满足，另一个线程（通知者）在notify前需要修改相应标识供接收者检查
* 二者在线程要等待条件变量前都必须要获得相应的锁



#### 成员函数

* notify_one
    * 通知—个等待线程
* notify_all
    * 通知全部等待线程
* wait
    * 阻塞当前线程直到被唤醒
* wait_for
    * 阻塞当前线程直到被唤醒或超过指定的等待时间（长度）
* wait_until
    * 阻塞当前线程直到被唤醒或到达指定的时间（点）



### 原子操作 atomic

原子操作（atomic operation） 意为”不可被中断的一个或一系列操作”。在新标准C++11，引入了原子操作的概念，并通过头文件 atomich提供了多种原子操作数据类型，例如 atomic_int, atomic_foat等等，如果在多线程中对这些类型的共享资源进行操作，编译器将保证这些操作都是原子性的，即确保任意时刻只有一个线程对这个资源进行访问。它的实现更接近底层，因而效率比互斥对象高。

基本类型 std::atomic，扩展实现 std::atomic_char, std::atomic_int, std::atomic_uint等。
* atomic_store
    * 保存非原干数据到原子数据结构
* atomic_load
    * 读取原子结构中的数据
* atomic_exchange
    * 保存非原干数据到原子数据结构，返回原来保存的数据
* atomic_fetch_add
    * 对原于结构中的数据做加操作
* atomic_fetch_sub/atomic_fetch_sub_explicit
    * 对原子结构中的数据做减操作
* atomic_fetch_and
    * 对原于结构中的数据逻辑与
* atomic fetch_or
    * 对原子结构中的数据逻辑或
* atomic_fetch_xor
    * 对原子结构中的数据逻辑异或



#### volatile与atomic

对 volatile 变量的访问，编译器不能做任何假设和推理，每次都必须按部就班地与内存进行交互（到内存中读取，而不是复用寄存器中的值）。

* volatile 不能解决多线程中的问题。
按照 Hans Boehm & Nick Maclaren 的总结，volatile 只在三种场合下是合适的。
*   和信号处理（signal handler）相关的场合；
*   和内存映射硬件（memory mapped hardware） 相关的场合；
*   和非本地跳转（setjmp 和 longjmp）相关的场合。



### 内存屏障与内存模型 Memory barrier & memory order

内存屏障（memory barrier）是一个CPU指命。基本上，它是这样一条指令

* 确保一些特定操作执行的顺序；
* 影响一些数据的可见性（可能是某些指令执行后的结果）。

编译器和CPU可以在保证输出结果一样的情况下对指令重排序，使性能得到优化。
插入一个内存屏障，相当于告诉CPU和编译器先于这个命令的必须先执行，后于这个命令的必须后执行。
内存屏障另一个作用是强制更新一次不同CPU的缓存。

读写锁 std::shared_mutex和std::shared_lock（C++14）
和一般的 std:mutex()一样提供lock()、try_lock()和 unlock()之外，std:shared mutex 还提供了lock_shared()、try_lock_shared()和 unlock_shared()三个操作。与 std::unique_lock 对应，标准库也提供std:shared_lock()容器。
它会在构造时，尝试以lock_shared()锁住传人的共享互斥量，并在销毁时，确保以 unlock_shared()的方式释放共享互斥量。同时，std::shared_lock也提供了lock()和 unlock()接口，用于以共享的方式锁住或者解锁构造时关联的共享互斥量。



### 信号量(Semaphore)

*   Semaphore是posix thread中的概念
*  C++11和 Boost.Thread 都没有提供Semaphore。原因简单来说，就是信号量太容易出错了（too error prone），通过组合互斥锁 （mutex）和条件变量 （condition variable）可以达到相同的效果，且更加安全。



### 避免死锁的进阶指导

*   尽量数据独立，线程间尽量少甚至没有共享数据
*   考虑能否使用数据副本
*  锁及共享数据操作尽量集中
*   避免嵌套锁
*   因为每个线程只持有一个锁，就不会产生死锁。
*   使用固定顺序加解锁
* 临界区尽量短，可控  
    * 谨慎调用第三方代码



### 推荐阅读材料（高阶学习材料）

* C++并发编程实践




## CUDA编程模型

### GPU与CPU硬件架构的对比

* CPU：更多资源用于缓存及流控制
* GPGPU： 更多资源用于数据计算
   *  适合具备可预测、针对数组的计算模式



### SIMD和SIMT

* SIMD: Single Instruction Multiple Data，—条指令处理多个数据
    * Intel mmx指令/sse指令
    * Arm Neon指令
* SIMD发生在ALU内部
* SIMT: Single Instruction Multi Threads，一条指令多条线程：
    *   应用于GPGPU
    *  每个thread拥有自己的状态寄存器
    *   每个线程有独立的访存地址
    *  每个thread可以有独立的执行路径
* SIMD运行的程序可以SIMT运行，反之不一定



### CUDA和GPGPU的软硬件对应方式

一个thread block的线程数量由程序员决定。但最后都会拆解成若干个warp（32个线程），最后在SM（streammultiprocessor）中以warp或者half- warp（nvidia的gpu都有）进行运行，同一个（half-）warp中的线程一定是齐头并进的

GPGPU和CPU运行的差异：控制流
* GPGPU：通过屏蔽的分别运行pathA和pathB
* CPU：只跑true的path，不会跑另一个分支



### GPGPU的warp scheduler: SM中的线程调度与执行

* Thread block内部线程组织为32-thread warps
    *   An implementation decision - not part of CUDA
*  Warp是SM调度的基本单位
    *  Warp就是一条32路SIMD指令
    *  Half-warp是warp的前一半或后一半
    *   访问存储器的基本单位



### 并行线程组织结构

* Thread：并行的基本单位
* Thread block：互相合作的线程组
* Cooperative Thread Array (CTA)
    * 允许彼此同步
    * 通过快速共享内存交换数据
    * 以1维、2维或3维组织
    * 最多包含512个线程
* Grid：一组thread block
    * 以1维、2维或3维组织
    * 共享全局内存
* Kernel：在GPU上执行的核心程序
    * one kernel <->one grid



### Block and Thread IDs

Blocks 和Threads 具有IDs

*   threadldx, blockldx
*   Block ID: 1D or 2D
*   Thread ID: 1D, 2D or 3D
*  由此决定相应处理数据



### 存储器模型与内存分配

* R/W per-thread registers
    * 1-cycle latency
* R/W per-thread local memory
    * Slow - register spilling to global memory
* R/W per-block shared memory
    * 1-cycle latency
    * But bank conflicts may drag down
* R/W per-grid global memory
    * ~500-cycle latency
    * But coalescing accessing could hide latency
* Read only per-grid constant and texture memories
    * ~500-cycle latency
    * But cached



### 开发流程

1. cpu原型实现
2. 将数据传给显存
3. 将数据结果传回内存
4. kernel函数
5. 调用kernel函数