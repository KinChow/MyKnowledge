---
archive_policy: text-only
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-be0d6e5cee68
  position:
    end: 344
    start: 92
    type: TextPositionSelector
  selector:
    exact: 标准库算子在性能上"不足"的真正原因不是单次计算慢，而是**每个 PyTorch 算子都会单独启动一个 CUDA kernel，数据被迫在 HBM
      里反复进出**（无内核融合）；Triton 是 OpenAI 开发的、介于 CUDA（逐线程）与高层框架（整操作）之间的 GPU 内核 DSL，让你**以"线程块"为单位思考**：把一个计算任务拆成多个块，每个块把数据装入共享内存、做计算（矩阵乘法等"大块"运算可当原子操作）、再写回全局内存，而
      warp 调度、线程粗化、寄存器分配等底层细节交给编译器。
    prefix: '# Triton 与 Kernel 编写


      ## 一句话结论


      '
    suffix: 课程从"为什么写 kernel"（基准测试/性能分析/内核融合）
    type: TextQuoteSelector
  snapshot_sha256: sha256:9994be737d497c4d1cf5a67351ded8330c3dafe70be871e973885764b65fcaf4
extractor: personal-note/1
id: working-computer-science-llm-triton-kernels
media_type: text/markdown
origin: personal
read_status: retrieved
retrieval:
  acquisition: personal-note
schema_version: source/v1
snapshot_sha256: sha256:9994be737d497c4d1cf5a67351ded8330c3dafe70be871e973885764b65fcaf4
source_type: personal-note
vault_id: public
---
---
domain: computer-science
title: Triton 与 Kernel 编写
---

# Triton 与 Kernel 编写

## 一句话结论

标准库算子在性能上"不足"的真正原因不是单次计算慢，而是**每个 PyTorch 算子都会单独启动一个 CUDA kernel，数据被迫在 HBM 里反复进出**（无内核融合）；Triton 是 OpenAI 开发的、介于 CUDA（逐线程）与高层框架（整操作）之间的 GPU 内核 DSL，让你**以"线程块"为单位思考**：把一个计算任务拆成多个块，每个块把数据装入共享内存、做计算（矩阵乘法等"大块"运算可当原子操作）、再写回全局内存，而 warp 调度、线程粗化、寄存器分配等底层细节交给编译器。课程从"为什么写 kernel"（基准测试/性能分析/内核融合）讲到"怎么写 kernel"（逐元素 → 行规约 → 行求和 → 矩阵乘法分块），并预告掌握这些就具备了实现 FlashAttention 所需的全部要素。

## 核心概念

- **内存层级与带宽-容量反比**：寄存器 → L1 缓存/共享内存（同一块物理内存，共享内存可控、L1 不可控）→ 全芯片共享的 L2 → HBM。"大容量内存速度慢，而且离得远；而像寄存器这样又快又大的内存……它们是本地的快速的但容量小"。
- **线程 / 线程块（CTA）/ 网格**：编程模型把内核启动视为"一个由线程和线程块组成的网格"，线程块会被调度到某个 SM 上执行。线程块存在的意义是让一组线程共享一块 SM 本地内存。
- **Warp 与锁步执行**：线程块内线程被分组为 warp，每 warp 32 个线程，同一条指令以锁步方式执行；"控制分歧"（warp 内线程走不同分支）会被串行化，因此要避免分支。
- **Warp 调度与延迟隐藏（计算/内存搬运重叠）**：SM 可同时运行多个 warp，从一个 warp 切换到另一个是"零开销"的；当一个 warp 从 HBM 读数据（约 100 个时钟周期）时，"你会立即切换到另一个可以实际执行一些张量运算的Warp"——这是内存搬运与计算重叠的主要机制。
- **占用率（occupancy）**：SM 寄存器数量固定，每线程用寄存器越多、可驻留线程越少，占用率越低。占用率"不一定越大越好"，因为线程少但每线程工作多（线程粗化）可能有益。
- **线程粗化（thread coarsening）**：让一个线程处理多个元素（如"八个"）以削减线程数量，编译器会自动对轻量任务做此优化（在 PTX 中可见）。
- **Bank 冲突（共享内存）**：共享内存被分成 32 个 Bank、每 Bank 宽 4 字节，每时钟周期每个 Bank 只能被一个线程访问；多个线程同时访问同一 Bank 须排队（如 32 路冲突是最坏情况），这就是 Bank 冲突。
- **内存合并（memory coalescing）**：一个 warp 的 32 个线程访问 HBM 时，若访问同一缓存行会被合并成一次 128 字节（转录误写为"228字节"）事务；按列访问会取回大量用不到的内存。
- **内核融合（kernel fusion）**：把多个逐元素操作（如 GELU 公式里的若干子运算）合并进单个 kernel，只读一次 HBM、每元素写一次 HBM，避免 kernel 之间数据必须回到 HBM 的多次往返。
- **Triton 的块编程模型**：不写"每个线程做什么"，而是写"每个块做什么"——块把数据加载到共享内存、操作、写回全局内存；"这些块其实是一个中间点，它介于思考单个元素在做什么和思考整体操作之间"。Triton 不是函数式的：无返回值，须显式分配输出张量并用 `tl.load`/`tl.store` 读写。
- **PTX**：Triton/CUDA 编译产出的 GPU 中间汇编语言，线程级视角；`LDGLOBAL` 从 HBM 加载到寄存器、`STGLOBAL` 写回 HBM，块索引 `CTAX`、线程索引 `TX` 区分线程。
- **tile（分块）**：数据放不进一个块（共享内存）时，把一行/一个输出分块拆成多个 tile 循环处理并累加；矩阵乘法的经典分块思想是"从全局来看它像朴素方法，从局部来看它又像理想化方法"。
- **算术强度（arithmetic intensity）**：操作数除以传输字节数，越高越好；朴素矩阵乘为常数，理想共享内存方案可达 N 量级，分块方案提升到"分块大小的量级"。

## 工作机制

1. **为什么要手写 kernel**：先用基准测试和性能分析确认瓶颈。GELU 例子中，直接实现 ≈3.75ms（"直接实现大概花了3.75毫秒"），内置实现与 torch.compile 版本都快得多。原因是直接实现由计算图里的每个基本操作各启动一个 kernel（Binary Functor、UnaryAddAtoms 等），"每个操作都会从 HBM 中反复读写数据"——"这里没有做核融合所以速度很慢"；内置实现是"一个 GELU 的 CUA 核函数……直接实现了 GELU 这个操作"；编译版本"基本上GELU里的所有操作都被融合到了一个核函数里……所以你只需要从HBM读取一次数据"。
2. **基准测试规范**：永远做热身（避免惰性编译/首次开销计入）、多次计时取平均（或看分布如 95 分位数）、用 CUDA 事件（record 开始/结束）并同步等待全部线程完成，因为 GPU 操作是异步的。矩阵乘法运行时间随规模立方增长，但在维度约 2000 之前存在平台期——GPU 为较大矩阵乘法设计，小矩阵效率极低。
3. **Triton 编程骨架**：先在 Python 侧分配输出张量（Triton 无返回值），把张量切成块（如 8000 元素、块大小 1024 → 8 块），用 `kernel[grid](...)` 的方括号语法指定网格形状，网格有多少块就调用多少次 kernel；每个块用 `pid` 计算自己负责的数据区间（`pid * BLOCK_SIZE`），用 `tl.arange(0, BLOCK_SIZE)` 生成块内索引，用 mask 处理"元素总数不能被块大小整除"的尾部，`tl.load` 读入、计算、`tl.store` 写回。
4. **编译与 PTX**：Triton 代码被编译成 PTX 中间语言，PTX 是线程级代码（线程块概念已被抽象掉），且已体现线程粗化（一个线程处理多个元素）；PTX 里仍有很多细节未指定（在哪个 SM 上执行、warp 调度），由硬件在运行时决定。遇到 TMA 加载指令会阻塞若干周期，warp 调度器切换其他 warp 执行，加载完成后切回。
5. **Softmax（行规约，行能放一块）**：把每一行当作一个块（块数=行数，块大小=列数向上取 2 的幂），因为 softmax 是"逐形操作"不是逐元素操作；被 mask 的位置置为负无穷（对应 softmax 的 0 值）；然后 `tl.max` 减去最大值（数值稳定性）→ `tl.exp` → `tl.sum` → 除法。此时"你几乎就可以像写普通PyTorch那样来写"。
6. **行求和（行放不下一块）**：当列数大于块大小，把行拆成多个 tile，在 kernel 内加 for 循环遍历 tile，"每次跳跃的时候我都会去调用一下……先拿到那个特定tile的偏移量，然后从HBM里把数据加载出来，再把它加到累加结果里面去"，累加器存放在寄存器或共享内存（块大小足够大就必须放共享内存），最后做小规约求和写回。从这里开始"它就不太像PyTorch了"。
7. **矩阵乘法分块内核**：朴素方法每个元素做一次点积，读取次数 M×K×N 量级、算术强度是常数；理想化方法把整个 A、B 装入共享内存，读取次数降到二次方量级、算术强度达 N 量级，但 A、B 通常太大放不下。实际做法是分块：C 被切成多个分块，每个分块对应一个线程块，块内沿 K 循环加载 A 行分块和 B 列分块到共享内存、做矩阵乘法（"只要数据在共享内存里操作起来就跟PyTorch一样"）、累加到部分和，扫完所有行列后把输出分块写回 HBM。算术强度提升到分块大小量级。额外好处是内核融合：在写回前直接对每个元素应用激活函数（"这就是内核融合 明白吗"）。
8. **索引/步长**：张量在内存中线性化存储，用行步长×行索引 + 列步长×列索引把多维索引映射到线性地址。

## 示例或代码

> 课程以口述+演示方式讲解，转录中无完整代码文本。以下按转录描述的结构用标准 Triton API 重建，ASR 词汇（如 `tl.arange` 被转写为 "range zero block size"）已对照语义还原。

**逐元素内核（向量乘，对应转录："一个八纤维的向量"→ 8000 元素、块大小 1024 → 8 个块）**

```python
n, BLOCK_SIZE = 8000, 1024          # 8000 个元素 / 1024 → 8 个块
x = torch.randn(n, device="cuda")
y = torch.empty_like(x)
num_blocks = n // BLOCK_SIZE

@triton.jit
def vector_kernel(x_ptr, y_ptr, n_elements, BLOCK_SIZE: tl.constexpr):
    pid = tl.program_id(axis=0)                    # "程序ID也就是P……用来标识块的"
    offsets = pid * BLOCK_SIZE + tl.arange(0, BLOCK_SIZE)  # 块内偏移
    mask = offsets < n_elements                    # 尾部掩码，"在Treaton代码里看到这种研码操作"
    x = tl.load(x_ptr + offsets, mask=mask)        # 从 HBM 读出、"指针运算"
    y = x * 2.0                                    # "接着做你正常的计算"
    tl.store(y_ptr + offsets, y, mask=mask)        # "最后再写回到HBM里"

vector_kernel[(num_blocks,)](x, y, n, BLOCK_SIZE)  # 方括号 = 网格形状
```

**Softmax（行规约，"每一行都当做一个块"）**

```python
m, n_cols = X.shape
BLOCK_SIZE = triton.next_power_of_2(n_cols)   # "为了求好运取下一个2的me"
num_blocks = m                                # 块数 = 行数，"每一行一个块"

@triton.jit
def softmax_kernel(x_ptr, y_ptr, row_stride, n_cols, BLOCK_SIZE: tl.constexpr):
    pid = tl.program_id(axis=0)
    row_start = x_ptr + pid * row_stride       # "行不长……告诉我向下移动多远"
    col_offsets = tl.arange(0, BLOCK_SIZE)
    mask = col_offsets < n_cols
    x = tl.load(row_start + col_offsets, mask=mask, other=float("-inf"))
    # "如果某个位置被掩码了我就把它设为负无穷……这部分其实就是softmax里相当于0值的"
    x = x - tl.max(x, axis=0)                  # "先减去最大值……数值稳定性"
    num = tl.exp(x)                            # "对每个元素分别进行指数运算"
    denom = tl.sum(num, axis=0)                # "对每一行求和并计算出一个规一化常数"
    y = num / denom
    tl.store(y_ptr + pid * row_stride + col_offsets, y, mask=mask)
```

**矩阵乘法（分块，"全局像朴素方法、局部像理想化方法"）**

```python
# A: M×K, B: K×N, C: M×N；每个线程块负责 C 的一个 BM×BN 分块

@triton.jit
def matmul_kernel(a_ptr, b_ptr, c_ptr,
                  M, N, K,
                  stride_am, stride_ak, stride_bk, stride_bn, stride_cm, stride_cn,
                  BLOCK_M: tl.constexpr, BLOCK_N: tl.constexpr, BLOCK_K: tl.constexpr):
    pid_m = tl.program_id(0)   # "你醒来时你就在DM行DN列的分块上"
    pid_n = tl.program_id(1)
    acc = tl.zeros((BLOCK_M, BLOCK_N), dtype=tl.float32)  # "设置这个累加器矩阵……位于共享内存中大小是M乘以N"
    offs_m = pid_m * BLOCK_M + tl.arange(0, BLOCK_M)
    offs_n = pid_n * BLOCK_N + tl.arange(0, BLOCK_N)
    offs_k = tl.arange(0, BLOCK_K)
    a_ptrs = a_ptr + offs_m[:, None] * stride_am + offs_k[None, :] * stride_ak
    b_ptrs = b_ptr + offs_k[:, None] * stride_bk + offs_n[None, :] * stride_bn
    for k in range(0, K, BLOCK_K):            # "我会沿着行的方向去便利这些行分块"
        a = tl.load(a_ptrs)                    # "加载A这个小矩阵……加载B这个小分块"
        b = tl.load(b_ptrs)
        acc += tl.dot(a, b)                    # "我直接说个Metmo它就会执行矩阵乘法"
        a_ptrs += BLOCK_K * stride_ak
        b_ptrs += BLOCK_K * stride_bk
    # 内核融合：写回前直接应用激活
    # "如果我想对每个元素单独应用一个非线性变换，我完全可以在这里就把它做完"
    tl.store(c_ptr + offs_m[:, None] * stride_cm + offs_n[None, :] * stride_cn, acc)
```

## 常见误区

- **误区：Triton/手写 kernel 一定比 PyTorch 内置实现快。** 澄清：本课 GELU 例子中，"实际上在这个例子里……Triton核函数并不更快"，编译出来的 Triton 内核"比内置的要慢一些"；"这些东西是会变化的，而且非常依赖于具体的硬件配置"，性能对比不是固定的。
- **误区：占用率越高越好。** 澄清：占用率是可衡量的指标，"但它不一定越大越好"，因为涉及权衡——线程更少但每线程承担工作量更多（线程粗化）"那实际上可能是有益的"。
- **误区：Triton 像 PyTorch 一样是函数式、有返回值。** 澄清："我们只考虑数据的移动，你必须显示的进行读写操作，所以没有返回值"——要在 Python 侧先分配输出张量，kernel 里用指针 + `tl.load`/`tl.store` 读写。
- **误区：能控制数据放在寄存器还是共享内存。** 澄清："你无法控制这点，硬件会自己判断数据应该放在哪里"；累加器的存放（寄存器或共享内存）由编译器决定，只有块大小足够大时才"必须放到共享内存里"。
- **误区：可以手动控制使用张量核心（Tensor Core）。** 澄清：无法控制，"硬件会自己判断数据应该放在哪里"，数据从 HBM 经共享内存到寄存器的搬运（TMA 加载）由硬件按步进行。
- **误区：想让线程数填满硬件，块数越多越好。** 澄清：SM 数量有限（转录举例 148 个），若块数不是 SM 数的整数倍（如启动 160 个块）会有"尾部效应"——最后一批块不足时"有一批SM正闲着没事干"，即低占用率；"一般来说让线城块的数量能够整除SM的数量可能是个好主意"。
- **误区：Triton 能比 CUDA 提供完全的硬件灵活性。** 澄清：想要充分利用最新硬件的每一个新特性时，"它可能无法提供完全的灵活性"，但入门通常足够强大。

## 待验证项

- **FlashAttention 未实际编写**：本课仅预告"你已经有了完成作业和实现 FlashAttention 所需要的所有要素"，并未给出 FlashAttention kernel 代码；如何把 softmax 分块 + 矩阵乘分块组合成 FlashAttention 需另寻资料验证。
- **Triton API 词形**：转录中 `tl.arange` 被转写为 "range zero block size"、"Metmo" 疑似 `tl.dot` 等，本文"示例或代码"为按语义重建，需对照 Triton 官方文档与课程讲义核实。
- **硬件数值**：转录口误较多——"B200系列每个SM最多65个寄存器"（B200 应为 65536 寄存器/SM）、"B200有6500个寄存器"、"每个线程最多可以使用155个寄存器"（常见限制为 255）、"最多不超过564个WARP"（应为 64 warp）、"228字节的事物"（应为 128 字节缓存行）、"148个" SM 等，均需对照硬件规格书验证。
- **GELU 基准数据**："直接实现大概花了3.75毫秒"及内置/编译版相对快慢，依赖具体硬件、PyTorch 与 Triton 版本，需实测复现。
- **kernel 命名与 tile 形状**：PyTorch 底层 kernel 名（CUBLAS、SM100/Blackwell、F32、64x64x16 vs 32x32x16 等）反映 tile 形状与架构，具体映射需在对应环境中验证。
- **内存搬运与计算重叠**：课程只覆盖了 warp 调度层面的延迟隐藏（加载阻塞时切换 warp），未展开显式双缓冲/流水线（pipelining）等更细粒度重叠技术。

## 关联知识

- [[llm-cuda-programming]]：本文档的 GPU 底层概念（warp、Bank 冲突、内存合并、占用率、线程块/网格）与 CUDA 视角互证；Triton 是这些概念之上的"块级"抽象。
- [[llm-compiler-optimization]]：独立文档。本课仅在 torch.compile 场景提到"运行一个编译器……结果底层实际上就只是一个单一的核函数……是一个用Triton编写的核函数"，全程未涉及 XLA；编译/融合的另一面见该文档。
- [[llm-transformer-architecture]]：GELU 激活函数在 Transformer FFN 中的角色；本文档用 GELU 举例说明内核融合的价值。
- [[llm-parallel-training]]：本课结尾预告"下次我们会聊更多关于GPU的内容，还会讲一讲多GPU编程"，即该文档内容。
- [[cs336]]：本文档源自 CS336 第 6 讲（GPU 与 Triton 内核），可与作业中手写 Triton kernel、基准测试要求相互印证。

## 详细章节

### GPU 内存层级与编程模型（回顾）

典型 GPU 结构 = 内存（HBM）+ GPU 芯片；每代 GPU 有 100-200 个流式多处理器（SM），每个 SM 有寄存器组（B200 转录称"6500个寄存器"、应为 65536）、L1 缓存与共享内存（"记住这两者是同一块物理内存，共享内存是你可以控制的，而LE缓存你控制不了"）、全芯片共享的 L2、以及 HBM。容量越大速度越慢：寄存器非常快，L1/共享内存稍慢，L2 更慢，HBM 最慢（"尽管每秒8TB的速度放在整个大局里来看其实也不算慢了"）。编程模型：每个线程在数据的一小部分上执行一段代码，线程组织成线程块（CTA，一组线程），线程块组成网格；启动内核 = 启动"由线程和线程块组成的网格"。线程块会被调度到某个 SM 上，从 HBM 读一批数据、处理（可能经共享内存在线程间通信）、写回——"这就是整个游戏的核心"，"事实上在Traten中我们将会看到这是目前编写内核的主要方式"。H100/B200 还有线程块组（线程块集群、分布式内存）、B200 有张量内存（用于张量核心，速度介于寄存器和共享内存之间），本课不深入。

### 为什么要手写 kernel：基准测试、性能分析、内核融合

先测量再优化（"你应该始终先测量一下实际情况……找出瓶颈到底在哪里，然后再开始编写内核"）。基准测试给总耗时，性能分析告诉你时间花在哪。规范做法：做热身、多次计时取平均、用 CUDA 事件（Record 开始/结束）+ 同步等待。矩阵乘法运行时间立方增长但在维度约 2000 前有平台期（GPU 为较大的矩阵乘法设计）。GELU 三路对比：直接实现（约 3.75ms，多个 kernel、多次 HBM 往返、"这里没有做核融合所以速度很慢"）vs 内置实现（单一 GELU CUDA kernel）vs torch.compile（生成单一 Triton kernel、"只需要从HBM读取一次数据然后每个元素写一次HBM"）。由此引出内核融合的价值与 Triton 作为融合后 kernel 的载体。

### Triton 语言模型：以"块"为单位编程

CUDA 的思维是"每个线程负责做什么"（靠近硬件、细粒度控制，但线程间通信/同步繁琐）；Triton 由 OpenAI 开发、现已相当标准，思维是"一个块到底在做什么"——块把数据加载到共享内存、操作、写回全局内存，介于"单个元素"和"整体操作"之间的中间点；"你基本上就是定义这些巨大的矩阵，然后说把它们相成，这就像是一种原子操作"。局限：想充分利用最新硬件每个新特性时可能缺乏完全灵活性，但入门足够。

### 第一个 Triton 内核：逐元素操作与 PTX

8000 元素、块大小 1024、8 个块。Python 侧先分配输出张量（无返回值），`kernel[grid](...)` 方括号指定网格形状。kernel 内：`pid`（program id）标识块 → `offsets = pid * BLOCK_SIZE + tl.arange(0, BLOCK_SIZE)` → 尾部 mask（"元素数量刚好能被块大小整除……但一般情况下并不是这样，所以你经常会在Treaton代码里看到这种研码操作"）→ `tl.load`（指针运算、按 mask 读取）→ 计算 → `tl.store`。把代码编译成 PTX 后看到的是线程级代码：`LDGLOBAL`（从 HBM 加载到寄存器）、`STGLOBAL`（写回 HBM）、块索引 `CTAX` 与线程索引 `TX` 区分线程、同一份代码被所有线程运行、通过 ID 区分彼此；PTX 中可见编译器对轻量任务做了线程粗化（"虽然这是一个线程，但它处理的不是一个元素而是多个元素"）。PTX 仍不指定 SM 与 warp 调度，这些由硬件决定；TMA 加载阻塞时 warp 调度器切换其他 warp，加载完成切回——即延迟隐藏。

### Softmax / 行规约：行放得进一块时

softmax 是"逐形操作"（对行聚合），不是逐元素操作，所以"把每一行都当做一个块来处理"，块与块之间不需要交互、不共享内存。数值稳定性流程：先减行最大值，再指数，再求和归一化。mask 位置置负无穷（softmax 中相当于 0）。块大小 = 列数向上取 2 的幂；块数 = 行数。"如果所有数据都能放进一个块，那么你几乎就可以像写普通PyTorch那样来写"。

### 行求和：数据放不下一块时的分块迭代

当行有 4000 列而块大小只有 128 时，把行拆成 4 个 tile，kernel 内 for 循环遍历 tile：算 tile 偏移 → 从 HBM 加载 → 加到累加器（寄存器或共享内存，块够大就必须放共享内存）→ 遍历完做小规约、求和写回。此时"它就不太像PyTorch了"。区分 block 与 tile：block 对应整行，tile 是块内部迭代处理的片断。

### 矩阵乘法：朴素 → 共享内存理想化 → 分块内核

朴素方法：每元素做一次点积，从 HBM 读取次数 M×K×N 量级，算术强度是常数，"这并不好"；且存在大量重复读取（算 C4、C5 都要重读 A4/A5/A6）。理想化方法：把整个 A、B 装入共享内存一次，读取次数降到二次方量级、"算术强度达到了N的量级……可以说是你能期望的理想情况了"，但 A、B 通常太大放不下。分块方法：C 切成多个分块、每分块对应一个线程块；块内沿 K 循环，把 A 行分块与 B 列分块加载到共享内存、`tl.dot` 做矩阵乘法并累加部分和，扫完所有行列后写回 HBM；"算术强度现在提升到了分块大小的量级"。涉及大量索引/步长计算（行步长×行索引 + 列步长×列索引，转置则反过来）。额外收益是内核融合：写回前直接应用逐元素激活（"这就是内核融合"）。

### 总结与展望

多层抽象：PyTorch → Triton → PTX，程序员可控制的粒度递增（PTX 甚至可直接编写并控制专门细节），但最终都受硬件约束（SM 数量、存储体数量、内存/寄存器大小有限），"当你带着你的大矩阵和Transformer模型过来时，你需要让它适应硬件的各种约束"，这就是基准测试和性能分析重要的原因。Triton 的价值是"思考线程块比思考单个线程要容易得多"，因为你不需要显式同步线程、不需要处理共享内存。难度递进的例子：逐元素 → 行规约 → 数据放不进一行时的规约（初级分块）→ 矩阵乘法（必须分块）。预告：掌握这些后具备实现 FlashAttention 的要素；下次课讲多 GPU 编程。Triton 的替代方案：PTX（极端情况）、Thunder Kittens、各种 DSL（特性各异，如擅长高维乘法或高维张量处理，不一定能直接比较高下）。

## 参考

- cs336-p06 转录（content/sources/computer-science/cs336-2026/cs336-p06/cs336-p06.md）
- 原始出处：Stanford CS336 "从零开始构建语言模型"第 6 讲（GPU 编程与 Triton 内核），视频 https://www.bilibili.com/video/BV1j9Kc6mEq4?p=6
