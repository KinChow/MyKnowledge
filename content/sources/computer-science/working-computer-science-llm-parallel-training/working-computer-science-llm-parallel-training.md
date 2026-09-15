---
archive_policy: text-only
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-6030298a92a1
  position:
    end: 185
    start: 84
    type: TextPositionSelector
  selector:
    exact: 多卡并行的根本动机只有两个：一是参数、激活值、梯度、优化器状态放不进单卡 HBM（例如 B200 只有 192GB 内存，装不下 1 万亿参数的模型），二是即便放得下也希望通过拆开所有东西来训练得更快。
    prefix: '--


      # 并行训练（DP/TP/PP）


      ## 一句话结论


      '
    suffix: 三种经典并行方式按不同维度切分模型：**数据并行（DP）** 只
    type: TextQuoteSelector
  snapshot_sha256: sha256:3fcca5da298116e817b48f096393f30d198e47b12674ee9e345845e074d82521
extractor: personal-note/1
id: working-computer-science-llm-parallel-training
media_type: text/markdown
origin: personal
read_status: retrieved
retrieval:
  acquisition: personal-note
schema_version: source/v1
snapshot_sha256: sha256:3fcca5da298116e817b48f096393f30d198e47b12674ee9e345845e074d82521
source_type: personal-note
vault_id: public
---
---
domain: computer-science
title: 并行训练（DP/TP/PP）
---

# 并行训练（DP/TP/PP）

## 一句话结论

多卡并行的根本动机只有两个：一是参数、激活值、梯度、优化器状态放不进单卡 HBM（例如 B200 只有 192GB 内存，装不下 1 万亿参数的模型），二是即便放得下也希望通过拆开所有东西来训练得更快。三种经典并行方式按不同维度切分模型：**数据并行（DP）** 只切数据、每卡持有完整模型、反向传播后用 AllReduce 对梯度取平均；**张量并行（TP）** 切每一层权重矩阵（列切分）、每层都要通信激活值，因此只能用在 NVLink 等高速互联域内；**流水线并行（PP）** 按网络深度切层并把整批数据拆成微批次，能容忍慢得多的互联，但会产生流水线气泡。三者的共同权衡始终是算力/显存容量与通信带宽之间的取舍——从单卡到千卡，本质都是把数据搬到计算单元附近并避免通信成为瓶颈。

## 核心概念

- **多卡 = 更大的内存层次结构**：单卡内部是 SM→L2/寄存器→HBM 的分层，多卡只是把这个结构延伸到 GPU 之外。课程指出，数据可能"你这里需要的数据可能远在另一个GPU上"，必须想办法把它搬运过来，但核心原则不变——"但核心原则其实是一样的,因为关键就在于如何协调计算过程,尽量避免数据传输成为瓶颈"。多卡教学的目标是"而本周我们要讨论如何利用多个GPU,让你的代码运行得更快"。
- **rank / world size**：分布式编程的标准术语，每个 rank 对应一个特定设备（这里一个 GPU 就是一个 rank），world size 对应设备数量；例如四个 rank 的 world size 是四。
- **集合通信原语（collective）**：broadcast / scatter / gather / reduce 只是热身，真正驱动语言模型分布式训练的是 **allgather、reduce_scatter、allreduce**；all-to-all 对 MoE 重要。这些原语的历史可追溯到 80 年代，并非为训练语言模型发明。
- **数据并行（DDP）**：把 batch 按 world size 切成本地 batch，每卡独立前向/反向，之后对全参数梯度做 AllReduce 取平均，再各自更新参数。它是标准训练加上一步梯度同步。
- **张量并行（TP）**：不切数据、切每一层本身，每个计算节点获得每一层参数的一部分。按列切权重矩阵称为**列张量并行**；前向传播对每层激活做 AllGather，反向传播做 ReduceScatter。
- **流水线并行（PP）**：沿网络深度方向切分，每个节点拿到网络层的一个子集；把整批数据拆成很多个微批次（microbatch），用 receive/send 点对点操作在节点间传递中间激活。朴素版本会产生**流水线气泡**。
- **有效带宽**：通信基准中用发送的总字节数除以总时长衡量，"带宽的计算方式就是用发送的字节数除以总时长"；AllReduce 的有效带宽约 400GB/s，且与 GPU 数量、拓扑结构无关。
- **网络拓扑层次**：单节点内 NVLink/NVSwitch，跨节点 InfiniBand（或以太网），节点越多、层数越深速度越慢；RDMA 允许 GPU 直读直写另一 GPU 内存、完全绕过 CPU。

## 工作机制

### 1. 硬件与拓扑：数据走多远的层次结构

课程给出一个通用层次：局部层面靠近 SM 的是单个节点、单个 GPU（L2/寄存器最快，HBM 次之——"但在本节课中,HBM将被视为快的"）；再往外是单节点多 GPU（NVLink + NVSwitch 连接）；最外是多节点多 GPU，只能使用 InfiniBand 或以太网，"具体用哪个取决于你现有的网络配置"。

- 节点内的 GPU 通过 NVLink 连到 NVSwitch，从编程角度看，"你可以把每个Gpu都看作是连接到了其他任何一个Gpu"，硬件负责把数据搬到交换机、交换机负责路由。
- 集群规模增长到一定程度后，"你就无法再使用NVSwitch和NVLink了"，必须把节点放进由 InfiniBand 连接的 Pod 中；这时 GPU 不再直连，必须经过 PCIe 再走 InfiniBand 线，速度慢得多。
- 拓扑是分层的：NVSwitch（域内 8~72 卡）→ InfiniBand Pod → 以太网（"在以太网中你必须经过PCIe总线"，而且还要穿过 CPU），越往外越慢——"你拥有的节点越多速度就会越慢"。
- RDMA（远程直接内存访问）是理想目标：课程先定义"因此有一种叫做远程直接内存访问"，再说明它允许一个 GPU 直接写入或读取另一个 GPU 的内存，并且"整个过程完全不需要用到CPU"。NVLink/NVSwitch 和 InfiniBand 都支持 RDMA，标准以太网不支持；但 RoCE（基于融合以太网的 RDMA）能让以太网绕过 CPU 传输数据，是对 InfiniBand 的回应，且 InfiniBand 非常昂贵。课程提到 Meta 在融合以太网上训练 LLM 的论文，措辞是"LMA可能是在融合以太网上训练的"（也可能不是）。
- 大规模硬件例子：B200/B300 的 **NVL72** 由 9 个托盘（每个托盘 8 个 GPU）组成，共 72 个 GPU 全部通过 NVSwitch 连到同一个 NVLink 域，可获得"最多72个GPU的极快互联"。

### 2. 集合通信原语：从热身到核心

- **broadcast**：rank0 上有一个张量（如 0123），广播结束后"每个rank上都会拥有相同的张量"；一般只用于初始化场景（加载初始检查点后广播给所有 rank），只做一次。
- **scatter**：rank0 上的大张量被切成与 world size 一样多的分片分发到各 rank，"把一个地方的大张量分散到多个不同的地方去"，让各 GPU 在不同部分上做本地计算。
- **gather**：scatter 的逆操作，把所有数据块拼接到同一个 rank（如 rank0）。
- **reduce**：与函数式编程的 reduce 相同，对分散在各 rank 的数据应用求和/最大值/最小值等结合、交换操作，结果放到 rank0。
- **allgather**：对每个 rank 都做 gather，"all的意思就是对所有rank的输出都执行这个操作"。训练中常见模式是每个 rank 都持有部分参数，需要做 all-gather 才能得到完整参数用于完整的前向传播。
- **reduce_scatter**：先对每个维度分别做 reduce，再把结果分散出去。反向传播后"每个gpu都会处理不同的数据"，需要把来自不同分片的梯度加起来，然后把这些存储重新分配出去。
- **allreduce**：最容易理解的操作——"然后你在所有节点上复制它们"（先在例子中做求和）。它是数据并行（DDP）的核心：先对梯度求和，再把完整参数复制到所有 rank。
- **all-to-all**：最通用的操作，可指定每个 rank 如何向另一个 rank 发送某条特定消息；在训练 MoE 时有用，因为"每个rank既负责一部分数据的分片"（也拥有一组专家子集，动态路由后变成全对全通信）。若各 rank 发送的字节数平衡，all-to-all 可看作矩阵转置。
- **关键分解**："AllReduce等于ReduceGatter加上AllGather"。基础版本用整体 allreduce 就足够；但 FSDP/ZeRO 这类高级功能需要把 allreduce 拆成 reduce_scatter + allgather，从而更精细地管理通信。

### 3. NCCL 与 torch.distributed 编程

- 最底层是 NVIDIA 集合通信库（NCCL），它负责把集合操作（如 AllReduce、Reduce、Broadcast）转换成实际在 GPU 之间发送的底层数据包；NCCL 会探测硬件拓扑、找出不同 GPU 之间的路径，再启动 GPU 通信内核（"所有在GPU上运行的东西"其实都是内核，包括通信内核）。
- PyTorch 的 `torch.distributed` 为集合操作提供简洁接口，不需要显式考虑 NCCL；GPU 用 NCCL 后端，CPU 用 Gloo 后端（"并行处理其实已经存在很长时间了"，CPU 上也能做集合操作）。主节点地址/端口配置只是元数据协调，实际数据传输走 NCCL，"否则速度会变得非常非常慢"。
- 编程要点：`spawn` 把函数复制运行 world size 次、每个进程一个 rank；`barrier` 是同步屏障，但加入更多屏障的缺点是"你最终可能会进行一些不必要的等待"；AllReduce 支持异步（`async=True`），典型做法是"让计算和通信重叠在一起进行"。

### 4. 通信基准与有效带宽

- 对一亿个元素执行 AllReduce，先预热（CUDA Synchronize + Barrier，因为存在两种异步形式："也就是Cua内核和各个进程"），再计时。每个 rank 会报告不同的测量值，要报告单一数字可取平均值。
- 有效带宽 = 发送的总字节数 ÷ 总时长。对 AllReduce，字节数为 大小 × 2 × (WorldSize−1)，"因为你需要同时进行发送和规约"（因子 2），并迭代 WorldSize−1 步；总时长为单个 rank 的挂钟时间 × WorldSize。
- 结果约 400GB/s。随 world size 增大，(WorldSize−1)/WorldSize 趋近 1，有效带宽趋近两倍的数据大小除以持续时间——"注意这个结果与WorldSize无关"，也与拓扑结构无关（"而拓扑结构是NCCL会去处理的事情"，由它决定以环形还是树形拓扑传消息）。
- ReduceScatter 与 AllReduce 带宽相似（约 400GB/s 量级）；AllReduce 移动两倍数据量、耗时也是两倍，二者相互抵消。

### 5. 数据并行（DP/DDP）

- 把 batch（如 128×d 的矩阵）按 world size 切成四块，"每个Rank都会分到一块数据"，本地 batch size = batch size / world size，"也就是Batch Size除以World Size"，"这样每块GPU看到的就是32个数据点"。
- 每卡实例化同一份 MLP（每层是一个 d×d 矩阵），对本地数据做前向、反向。因为每卡数据不同、梯度也不同，于是关键步骤是"我们要在所有Worker之间同步T度"。
- 对全部参数梯度做全局规约取平均，AllReduce 完成后"每个Rank就都拿到了完全相同的T度"，然后各自更新参数。课程强调："实际上这就是标准训练和DDP之间"唯一的区别，且只需改动一行代码——在反向传播之后插入这一步，"就是通过All Reduce来平均所有T度"。
- 每个 rank 更新参数时"就好像它拥有全部数据一样"，但实际上它只处理了一部分数据。DDP 非常模块化，不关心前向传播长什么样，因此对 Transformer 同样适用。
- 约束：batch size 至少得是 world size 才有意义，且通常是其倍数更简单；不是倍数可用 0 填充解决。

### 6. 张量并行（TP，列切分）

- 思路与 DP 相反："每个计算节点都会获得每一层的一部分参数"（不是切数据，而是切每一层本身）。
- 假设每个节点拥有全部数据；为每个节点定义局部维度，权重矩阵维度变为 总维度数 × 局部维度数。对一个层参数矩阵按列切分，"这种方式也被称为列张量并行"（按行切分也存在，课程未展开）。
- 前向：每层用局部权重切片算部分激活，非线性是逐元素操作可独立应用，然后"我需要把所有激活值都汇集到所有节点上"，用 allgather 把各节点局部激活收集、拼接成完整 X（batch×总维度），再进入下一层。
- 反向：拥有激活值后"并且需要执行Reduce Scatter操作"，将梯度分散到各个节点——前向 AllGather / 反向 ReduceScatter 是对偶的。这些并行逻辑不会由 `loss.backward()` 自动执行（因为里面没有并行逻辑），需要显式管理，这是课程从 0 开始构建的刻意设计。
- 代价：TP 通信量特别大，"因为每一层你都需要发送所有这些激活值"，而这些激活值本身相当大，因此只在节点内部 NVLink/高带宽连接内做，"所以一般来说张量并行是在一个节点内部通过NVlink"，"而你不会在NVlink域之外做张量并行"。

### 7. 流水线并行（PP）

- 沿网络深度切分，"每个节点都会拿到网络层的一个子集"；每层的参数矩阵仍是 总维度数 × 总维度数，但只持有局部层数的参数。"所以这是一种非常自然的深度网络划分方式"。
- 除了切层，"还会把整个批次数据拆分成很多个微批次"。每个微批次：从前一个节点 receive，只对自己负责的层做前向，再把结果 send 给下一节点——使用 receive/send 两个点对点操作。
- 问题：朴素版本产生**流水线气泡**——"你其实就是在那里等着其他张量处理完"，效率非常低。微批次的意义是把数据拆成更小的单元，让每个节点快速处理完并马上传给下一个节点，"这样一来就能减少流水线气泡的数量"。
- 朴素版本还没处理**通信与计算的重叠**（把 receive/send 变成异步版本并管理），课程明确"通信和计算之间的重叠在流水线并行中显得尤其关键"；数据并行里也能做——反向传播中梯度一算完就开始发送，这是作业要探索的内容。

### 8. 并行方式选择：显存/算力/通信权衡

- 选哪种并行"这在很大程度上是取决于你的硬件配置的"：TP 通信量大→NVLink 域内；PP 通信量小→"这种并行方式通常能容忍速度慢得多的互联设备"（所以去中心化训练用 PP，"因为你的节点或GPU实际上分布在地球两端"）；DP 可扩展但受**临界批量大小**限制——batch 太大"实际上它并不会给你带来什么帮助"，白白浪费算力，此时最好改用张量并行。
- 常见组合：节点内部张量并行 + 流水线数据并行或 FSDP + 必要时再加流水线并行。
- 总结：DP/TP 需要非常快的网络连接（"它们需要非常快的网络连接"），PP 对网络要求低、但"你必须花很大力气去减少这些流水线气泡"。高层面是重新计算 vs 存储在内存里的取舍（类似激活检查点），"你可以把数据存储在不同的GPU上"；数据并行在某种意义上做冗余工作（"因为每个进程实际上都在更新自己的参数"），好处是"你不需要移动优化器的状态"。

## 示例或代码

**课程中的具体数字（可审计）：**
- B200 有 192GB 内存；1 万亿参数模型放不进单卡。
- NVLink 5 总带宽约每秒 1.8TB；B200 的 HBM 带宽（"HBM对于B200来说带宽是每秒8TB"），约慢 4 倍；HBM 又比共享内存/L2 缓存慢得多。
- NVL72 = 9 个托盘 × 每个托盘 8 个 GPU = 72 个 GPU，全部接入同一个 NVSwitch/NVLink 域。
- 数据并行示例：batch size 128、维度 d，world size 4 → 本地 batch size 32。
- 基准：对一亿元素 AllReduce，有效带宽约 400GB/s；ReduceScatter 也约 400GB/s 量级。

**伪代码（基于课程描述整理，非引文）：**

数据并行（DDP）训练循环：
```
x_local = x[start:end]            # 按 world size 切本地 batch
for epoch:
    for batch:
        loss = forward(x_local)   # 每卡独立前向（持完整模型）
        loss.backward()           # 每卡独立反向 → 本地梯度
        allreduce(grads, op=SUM)  # 所有 worker 间梯度求和/平均 ← 唯一新增步骤
        grads /= world_size
        optimizer.step()          # 每卡用相同梯度各自更新
```

张量并行（列切分，单层前向）：
```
W_local = W[:, local_start:local_end]        # 每节点持权重矩阵的一列块
z_local = X @ W_local                        # 局部矩阵乘
Y_local = nonlin(z_local)                    # 逐元素非线性，可独立做
X_next = allgather(Y_local, dim=-1)          # 汇集所有节点局部激活 → 拼接成完整 X
# 反向：对梯度执行 reduce_scatter 分回各节点
```

流水线并行（节点 p 处理第 p 段层）：
```
for microbatch in microbatches:              # 把整批拆成微批次
    x = recv(from=p-1)                       # 从上一节点接收
    for layer in my_layers:                  # 只算分配给自己的层
        x = layer(x)
    send(x, to=p+1)                          # 发给下一节点
# 理想实现把 recv/send 变异步，让通信与计算重叠，减少气泡
```

## 常见误区

- **误区：AllReduce 是一个不可拆的整体操作。** 澄清：AllReduce = ReduceScatter + AllGather，课程用代码验证了这一点；FSDP/ZeRO 正是靠拆开它来精细管理通信与显存。
- **误区：GPU 越多通信就越快、有效带宽越高。** 澄清：课程测得有效带宽"注意这个结果与WorldSize无关"，也跟拓扑结构无关，约 400GB/s 是硬件/库层面的稳定值；增加 GPU 并不改变每字节搬移的有效带宽。
- **误区：张量并行可以随便跨节点做。** 澄清：TP 每层都要发激活值、通信量极大，只在 NVLink/高带宽域内做——"所以一般来说张量并行是在一个节点内部通过NVlink"，"而你不会在NVlink域之外做张量并行"。
- **误区：并行卡越多训练越快，可以无限加。** 澄清：数据并行受临界批量大小限制，batch 太大"实际上它并不会给你带来什么帮助"，白白浪费算力，此时应转向张量并行。
- **误区：集合通信的 broadcasting 就是 numpy 的 broadcasting。** 澄清：课程明确二者概念上相近（都是把一个东西分发到多个上），但具体实现是用于集合通信的，会有点不一样。
- **误区：DDP 能解决模型放不进显存的问题。** 澄清：DDP 的 AllReduce 需要把所有模型参数放在内存里；参数放不进内存是 FSDP/ZeRO（下一节内容）解决的问题，而不是 DDP。
- **误区：只要调用 `loss.backward()` 就能做并行。** 澄清：TP 的前向 AllGather/反向 ReduceScatter 不会自动执行（因为里面没有并行逻辑），课程从 0 显式管理；实际应用中 PyTorch 已自动实现。

## 待验证项

- **ZeRO / FSDP 细节**：课程只明确 DDP 用整体 AllReduce、需要把所有模型参数放在内存里，并预告下一节讲 FSDP 和 ZeRO；ZeRO 对参数/梯度/优化器状态的具体分片方式、以及如何把 AllReduce 拆成 reduce_scatter+allgather 来精细管理，本课未展开，需 cs336-p08 或后续 source 补强。
- **NCCL 内部算法**：提到 NCCL 决定以环形还是树形拓扑传消息，但未给出 ring/tree 的具体算法、带宽模型以及多节点集群的优化细节；讲师对 NCCL 是否针对多节点集群优化的问题回答"我不太清楚它们具体在哪些地方做了优化"。
- **流水线 schedule 与通信计算重叠**：课程只展示最朴素版本，明确没有处理通信和计算的重叠，微批次/1F1B 等 schedule、异步 recv/send 的实现细节留待周三（Tuto）讲解，未在本课覆盖。
- **TP 的行切分**：课程仅详述列张量并行，提到按行切分也可行但未展开。
- **RDMA 与 RoCE 细节**：课程把 RDMA 定位为"更侧重于通信时实际发生的事情"的理想目标，RoCE 为对 InfiniBand 的回应；Meta 在融合以太网训练 LLM 只是可能（"LMA可能是在融合以太网上训练的"），具体实现/性能数据缺失。
- **TPU 编译路径**：课程提到 TPU 上定义模型和分片策略，然后"然后编译器实际上会帮你处理很多决策"，但未展开 GSPMD/分片标注细节，可作为独立 topic。
- **NVL72 与 4D 组合**：本课仅提及 NVL72 硬件形态与节点内部 TP + 数据/流水线并行的组合直觉，4D 组合（DP/PP/TP/EP）的完整拓扑映射需结合 cs336-p08。

## 关联知识

- **[[gpu-overview]]**：单 GPU 内部结构（HBM、L2 缓存、SM、共享内存）是理解多卡 = 更大内存层次结构的前提；本课把 HBM 视为快的（相对 GPU 间通信）来对比。
- **专家并行与 4D 组合（cs336-p08）**：本课只点出 all-to-all 对 MoE 的重要性（"每个rank既负责一部分数据的分片"，也拥有一组专家子集），并预告序列并行、专家并行与多种并行技术的组合；EP 细节见 cs336-p08 独立文档，本文不展开。
- **Transformer / MLP**：课程明确"MLP其实就是Transformer里真正的计算核心"，用 MLP 演示三种并行方式，"一些更大的模型只是需要更多的记账工作"；可关联 [[transformer]]。
- **激活检查点与内存优化**：结尾把重新计算 vs 存储在内存里的取舍与激活检查点类比，并延伸为"你可以把数据存储在不同的GPU上"，与显存优化的系列内容同源。
- **CS336 课程体系**：上一讲为单 GPU 内核优化（减少内存访问、融合、分块），本讲为多 GPU 并行，下一讲（周三 Tuto / cs336-p08）为 FSDP、ZeRO、序列/专家并行与组合。

## 详细章节

### 为什么需要多卡：容量与吞吐
### 通信硬件与网络拓扑（NVLink / NVSwitch / InfiniBand / 以太网 / RDMA）
### 集合通信原语（broadcast / scatter / gather / reduce → allgather / reduce_scatter / allreduce / all-to-all）
### NCCL 与 torch.distributed 编程
### 通信基准与有效带宽
### 数据并行（DP / DDP）
### 张量并行（TP，列切分）
### 流水线并行（PP，层切分 + 微批次 + 流水线气泡）
### 并行方式选择：显存 / 算力 / 通信权衡与规模化组合

## 参考

- cs336-p07 转录（Stanford CS336，视频 P7，并行计算：DP/TP/PP 与通信拓扑），来源文件：`content/sources/computer-science/cs336-2026/cs336-p07/cs336-p07.md`
