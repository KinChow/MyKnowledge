---
aliases:
- Queue
- 队列数据结构
- FIFO 队列
confidentiality: public
domain: computer-science
evidence:
- claim: 队列是计算机科学中的抽象数据类型，作为实体的有序集合；按约定，添加元素的一端称为
    back、tail 或 rear，移除元素的一端称为 head 或 front。
  claim_id: q-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-321ef16388c5
    exact: |-
      In computer science, a queue is an abstract data type that serves as an ordered collection of entities.
  - evidence_id: evidence-0b3f314368e0
    exact: |-
      By convention, the end of the queue where elements are added is called the back, tail, or rear of the queue. The end of the queue where elements are removed is called the head or front of the queue.
  targets:
  - evidence_id: evidence-321ef16388c5
    source_id: wiki-queue-adt
  - evidence_id: evidence-0b3f314368e0
    source_id: wiki-queue-adt
- claim: 队列支持两个主要操作：enqueue 在队尾添加一个元素；dequeue 从队首移除一个元素；此外常允许
    peek 或 front 操作，返回下一个将出队元素的值而不真正出队。
  claim_id: q-ops
  support: direct
  supporting_quotes:
  - evidence_id: evidence-5fbba192da65
    exact: |-
      Enqueue, which adds one element to the rear of the queue
  - evidence_id: evidence-63df362c3908
    exact: |-
      Dequeue, which removes one element from the front of the queue.
  - evidence_id: evidence-8bb17fb652f7
    exact: |-
      Other operations may also be allowed, often including a peek or front operation that returns the value of the next element to be dequeued without dequeuing it.
  targets:
  - evidence_id: evidence-5fbba192da65
    source_id: wiki-queue-adt
  - evidence_id: evidence-63df362c3908
    source_id: wiki-queue-adt
  - evidence_id: evidence-8bb17fb652f7
    source_id: wiki-queue-adt
- claim: 队列的操作使其成为先进先出（FIFO）数据结构：最先加入队列的元素最先被移除；这也等价于要求新元素加入后，必须先移除所有先于它的元素才能移除它。
  claim_id: q-fifo-wiki
  support: direct
  supporting_quotes:
  - evidence_id: evidence-3612bdfaecca
    exact: |-
      make it a first-in-first-out (FIFO) data structure as the first element added to the queue is the first one removed.
  - evidence_id: evidence-8d8f51a56142
    exact: |-
      This is equivalent to the requirement that once a new element is added, all elements that were added before have to be removed before the new element can be removed.
  targets:
  - evidence_id: evidence-3612bdfaecca
    source_id: wiki-queue-adt
  - evidence_id: evidence-8d8f51a56142
    source_id: wiki-queue-adt
- claim: 队列是线性数据结构，更抽象地说是一种顺序集合。
  claim_id: q-linear
  support: direct
  supporting_quotes:
  - evidence_id: evidence-2ae223870aea
    exact: |-
      A queue is an example of a linear data structure, or more abstractly a sequential collection.
  targets:
  - evidence_id: evidence-2ae223870aea
    source_id: wiki-queue-adt
- claim: 队列可以实现为循环缓冲区（circular buffer）和链表。
  claim_id: q-impl
  support: direct
  supporting_quotes:
  - evidence_id: evidence-2bcf59757f6a
    exact: |-
      A queue may be implemented as circular buffers and linked lists, or by using both the stack pointer and the base pointer.
  targets:
  - evidence_id: evidence-2bcf59757f6a
    source_id: wiki-queue-adt
- claim: 有界队列是限制为固定数量条目的队列。
  claim_id: q-bounded
  support: direct
  supporting_quotes:
  - evidence_id: evidence-4db305b3ca1c
    exact: |-
      A bounded queue is a queue limited to a fixed number of items.
  targets:
  - evidence_id: evidence-4db305b3ca1c
    source_id: wiki-queue-adt
- claim: 存在多种高效的 FIFO 队列实现——高效指入队（en-queuing）与出队（de-queuing）都能以 O(1) 时间完成。
  claim_id: q-efficiency
  support: direct
  supporting_quotes:
  - evidence_id: evidence-55c74d7a1fd6
    exact: |-
      There are several efficient implementations of FIFO queues. An efficient implementation is one that can perform the operations—en-queuing and de-queuing—in O(1) time.
  targets:
  - evidence_id: evidence-55c74d7a1fd6
    source_id: wiki-queue-adt
- claim: 双向链表在两端插入和删除都是 O(1)，因此是队列的天然选择。
  claim_id: q-ll-impl
  support: direct
  supporting_quotes:
  - evidence_id: evidence-01e0dc35da5b
    exact: |-
      A doubly linked list has O(1) insertion and deletion at both ends, so it is a natural choice for queues.
  targets:
  - evidence_id: evidence-01e0dc35da5b
    source_id: wiki-queue-adt
- claim: 常规单链表只有一端能高效插入删除；稍加修改——除首节点指针外再保存一个指向最后节点的指针——就能用它实现高效队列。
  claim_id: q-sll-impl
  support: direct
  supporting_quotes:
  - evidence_id: evidence-98db9ed161b0
    exact: |-
      A regular singly linked list only has efficient insertion and deletion at one end. However, a small modification—keeping a pointer to the last node in addition to the first one—will enable it to implement an efficient queue.
  targets:
  - evidence_id: evidence-98db9ed161b0
    source_id: wiki-queue-adt
- claim: deque（双端队列）可以用改造过的动态数组实现。
  claim_id: q-deque-arr
  support: direct
  supporting_quotes:
  - evidence_id: evidence-a6281e47fc6b
    exact: |-
      A deque implemented using a modified dynamic array
  targets:
  - evidence_id: evidence-a6281e47fc6b
    source_id: wiki-queue-adt
- claim: FIFO 即先进先出：是一种最先进入的元素最先处理、最新的元素最后处理的数据处理方式；队列及其各类变体正是采用
    FIFO 方式处理数据的数据结构。
  claim_id: q-fifo
  support: direct
  supporting_quotes:
  - evidence_id: evidence-8ff2ed221c43
    exact: |-
      FIFO is an abbreviation for first in, first out. It is a method for handling data structures where the first element is processed first and the newest element is processed last.
  - evidence_id: evidence-9dee8b7f3fce
    exact: |-
      Certain data structures like Queue and other variants of Queue uses FIFO approach for processing data.
  targets:
  - evidence_id: evidence-8ff2ed221c43
    source_id: web-computer-science-queue
  - evidence_id: evidence-9dee8b7f3fce
    source_id: web-computer-science-queue
- claim: 磁盘控制器可用 FIFO 作为磁盘调度算法，决定磁盘 I/O 请求的服务顺序；通信网络的网桥、交换机和路由器用
    FIFO 暂存去往下一目的地的数据包。
  claim_id: q-fifo-usage
  support: direct
  supporting_quotes:
  - evidence_id: evidence-5a69eff1293e
    exact: |-
      Disk controllers can use the FIFO as a disk scheduling algorithm to determine the order in which to service disk I/O requests.
  - evidence_id: evidence-e63039c54202
    exact: |-
      Communication network bridges, switches and routers used in computer networks use FIFOs to hold data packets en route to their next destination.
  targets:
  - evidence_id: evidence-5a69eff1293e
    source_id: web-computer-science-queue
  - evidence_id: evidence-e63039c54202
    source_id: web-computer-science-queue
id: queue
kind: reference
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- wiki-queue-adt
- web-computer-science-queue
- working-computer-science-queue
status: published
tags:
- data-structure
- queue
- fifo
title: 队列
updated_at: '2026-09-05'
---
# 队列

## 一句话结论

队列是一种**先进先出（FIFO）的线性抽象数据类型**：入队（enqueue）发生在队尾（rear），出队（dequeue）发生在队首（front）——最先进入的元素最先离开。它是"单资源多消费者"场景的天然模型：任务调度、消息队列、BFS 层序遍历、磁盘 I/O 调度都靠它保序削峰。高效实现（循环缓冲区、带头尾指针的链表）能把入队出队都做到 O(1)。

## 核心概念

- **FIFO**：最先加入队列的元素最先被移除；新元素必须等它前面的元素全部移除后才能被移除。
- **rear / front**：添加端与移除端的约定名称（back/tail/rear 与 head/front）。
- **循环缓冲区（环形缓冲）**：数组首尾相接的队列实现，天然适配定长有界队列。
- **有界队列**：限制为固定数量条目的队列——生产者/消费者系统的背压基础。
- **peek/front**：只读下一个将出队的元素而不出队。

## 工作机制

### 核心操作

| 操作 | 语义 |
| --- | --- |
| enqueue() | 在队尾添加一个元素 |
| dequeue() | 从队首移除一个元素 |
| peek()/front() | 返回下一个将出队的元素，不移除 |

### 实现方式

- **循环缓冲区**：定长数组的经典实现，配头尾下标取模递增；对应有界队列。
- **双向链表**：两端插入删除均 O(1)，是队列的天然选择。
- **单链表 + 尾指针**：普通单链表只有一端高效；额外保存最后一个节点的指针即可高效实现队列。
- **改造的动态数组**：deque（双端队列）的实现方式之一。

### 复杂度

| 操作 | 平均 | 最坏 |
| --- | --- | --- |
| 查找 | O(n) | O(n) |
| 插入 | O(1) | O(1) |
| 删除 | O(1) | O(1) |
| 空间 | O(n) | O(n) |

## 常见误区

- **"队列就是数组"**：数组只是底层容器；线性数组实现的 front/rear 递增会产生假满（前面有空位却报满），工程上用循环缓冲区解决。
- **"优先队列也是 FIFO"**：不是——优先队列按优先级出队，与入队次序无关。
- **"deque 严格遵守 FIFO"**：双端队列两端皆可进出，FIFO 只是它的可选用法。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| q-definition / q-ops / q-fifo-wiki / q-linear | wiki-queue-adt（Wikipedia） | ADT 定义、rear/front、两大操作、FIFO 性质 |
| q-impl / q-bounded / q-efficiency / q-ll-impl / q-sll-impl / q-deque-arr | wiki-queue-adt（Wikipedia） | 实现方式与 O(1) 效率 |
| q-fifo / q-fifo-usage | web-computer-science-queue（FIFO 专题） | FIFO 定义、磁盘调度与网络设备应用 |

## 待验证项

- 变体分类（简单/循环/优先队列/双端）的详细描述目前主要来自内部工作笔记（personal source，不能作为公开 direct 证据）；正文仅保留与 Wikipedia 证据直接对应的部分，优先队列与双端队列的展开描述待补对应公开源。

## 关联知识

- [[stack]] —— 对偶结构：栈 LIFO、队列 FIFO。
- [[circular-linked-list]] —— 链表实现的循环队列形态。
- [[binary-tree]] —— BFS 层序遍历以队列为引擎。
- [[data-structure-optimization]] —— 消息队列/任务调度选型。

## 详细章节

### 定义

队列是计算机科学中的抽象数据类型：实体的有序集合，添加端称为 back/tail/rear，移除端称为 head/front。其两个主要操作是 enqueue（队尾添加）与 dequeue（队首移除）。队列的操作使其成为 FIFO 数据结构——最先加入的元素最先被移除；它也是线性数据结构（更抽象地说，顺序集合）。队列名源自现实中人们排队等候商品或服务的类比。

### 应用

- 单一资源多消费者的服务排队；快慢设备的速度同步（缓冲）。
- 磁盘控制器以 FIFO 作为磁盘调度算法决定 I/O 请求服务顺序。
- 网络网桥、交换机与路由器用 FIFO 暂存去往下一跳的数据包。
- BFS 层序遍历、消息队列、任务调度。

## 参考

- https://en.wikipedia.org/wiki/Queue_(abstract_data_type)
- https://www.geeksforgeeks.org/fifo-first-in-first-out-approach-in-programming/
