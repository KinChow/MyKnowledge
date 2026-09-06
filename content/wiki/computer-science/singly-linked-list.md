---
aliases:
- Singly Linked List
- 单链表
- 单向链表
confidentiality: public
domain: computer-science
evidence:
- claim: 链表是计算机科学中的基础数据结构：相比数组主要优势是高效的插入与删除；与数组一样也用于实现栈、队列、双端队列等其他数据结构。
  claim_id: sll-fundamental
  support: direct
  supporting_quotes:
  - evidence_id: evidence-d38ddbbef35a
    exact: |-
      A linked list is a fundamental data structure in computer science. It mainly allows efficient insertion and deletion operations compared to arrays. Like arrays, it is also used to implement other data structures like stack, queue and deque.
  targets:
  - evidence_id: evidence-d38ddbbef35a
    source_id: web-computer-science-singly-linked-list
- claim: 链表是线性数据结构：各元素不必存放在连续位置；元素称为节点，彼此用链接相连。
  claim_id: sll-non-contiguous
  support: direct
  supporting_quotes:
  - evidence_id: evidence-2e3920cc1316
    exact: |-
      A linked list is a type of linear data structure individual items are not necessarily at contiguous locations. The individual items are called nodes and connected with each other using links.
  targets:
  - evidence_id: evidence-2e3920cc1316
    source_id: web-computer-science-singly-linked-list
- claim: 单链表中每个节点包含两样东西——数据与连接到另一节点的链接；每个节点只持有一个指向下一个节点的链接。
  claim_id: sll-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-5fa7b97efee5
    exact: |-
      - A node contains two things first is data and second is a link that connects it with another node.
  - evidence_id: evidence-6f9055c4a223
    exact: |-
      In its most basic form, each node contains data, and a reference (in other words, a link) to the next node in the sequence. This structure allows for efficient insertion or removal of elements from any position in the sequence during iteration.
  targets:
  - evidence_id: evidence-5fa7b97efee5
    source_id: web-computer-science-singly-linked-list
  - evidence_id: evidence-6f9055c4a223
    source_id: wiki-linked-list
- claim: 第一个节点称为头节点（head node），借助 head 与 next 链接可以遍历整条链表。
  claim_id: sll-head
  support: direct
  supporting_quotes:
  - evidence_id: evidence-a5a4fd131352
    exact: |-
      - The first node is called the head node and we can traverse the whole list using this head and next links.
  targets:
  - evidence_id: evidence-a5a4fd131352
    source_id: web-computer-science-singly-linked-list
- claim: 链表插入/删除高效、访问顺序、非连续存储；数组则插删低效、随机访问、连续存储；且数组的缓存局部性更好。
  claim_id: sll-vs-array
  support: direct
  supporting_quotes:
  - evidence_id: evidence-55fba6124609
    exact: |-
      - Insertion/Deletion: Efficient
  - evidence_id: evidence-f7b8487bda5d
    exact: |-
      - Access: Sequential
  - evidence_id: evidence-f1ce9379114f
    exact: |-
      - Data Structure: Non-contiguous
  - evidence_id: evidence-368650b1ce09
    exact: |-
      - Data Structure: Contiguous
  - evidence_id: evidence-a88953d73441
    exact: |-
      - Access: Random
  - evidence_id: evidence-71294d476f8f
    exact: |-
      - Insertion/Deletion: Inefficient
  - evidence_id: evidence-5f4608cd28e0
    exact: |-
      Arrays have better cache locality compared to linked lists.
  targets:
  - evidence_id: evidence-55fba6124609
    source_id: web-computer-science-singly-linked-list
  - evidence_id: evidence-f7b8487bda5d
    source_id: web-computer-science-singly-linked-list
  - evidence_id: evidence-f1ce9379114f
    source_id: web-computer-science-singly-linked-list
  - evidence_id: evidence-368650b1ce09
    source_id: web-computer-science-singly-linked-list
  - evidence_id: evidence-a88953d73441
    source_id: web-computer-science-singly-linked-list
  - evidence_id: evidence-71294d476f8f
    source_id: web-computer-science-singly-linked-list
  - evidence_id: evidence-5f4608cd28e0
    source_id: wiki-linked-list
- claim: 访问单链表中元素需要从头遍历到目标节点——内存中没有对特定节点的直接访问；这使访问时间与节点数成线性关系，且无法随机访问。
  claim_id: sll-linear-access
  support: direct
  supporting_quotes:
  - evidence_id: evidence-e1c0317667fd
    exact: |-
      A drawback of linked lists is that data access time is linear with respect to the number of nodes in the list.
  - evidence_id: evidence-debf304f8906
    exact: |-
      Because nodes are serially linked, accessing any node requires that the prior node be accessed beforehand (which introduces difficulties in pipelining). Faster access, such as random access (direct access), is not possible.
  targets:
  - evidence_id: evidence-e1c0317667fd
    source_id: wiki-linked-list
  - evidence_id: evidence-debf304f8906
    source_id: wiki-linked-list
- claim: 相比常规数组，链表的核心好处是插入或移除元素无需重新分配或重组整个结构——数据项不需要连续存储；而运行时重组数组代价高得多。
  claim_id: sll-benefit
  support: direct
  supporting_quotes:
  - evidence_id: evidence-816e76e0295f
    exact: |-
      The principal benefit of a linked list over a conventional array is that the list elements can be easily inserted or removed without reallocation or reorganization of the entire structure because the data items do not need to be stored contiguously in memory or on disk, while restructuring an array at run-time is a much more expensive operation.
  targets:
  - evidence_id: evidence-816e76e0295f
    source_id: wiki-linked-list
id: singly-linked-list
kind: reference
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- wiki-linked-list
- web-computer-science-singly-linked-list
- working-computer-science-singly-linked-list
status: published
tags:
- data-structure
- linked-list
title: 单链表
updated_at: '2026-09-05'
---
# 单链表

## 一句话结论

单链表是链表的最基本形态：**每个节点只持有一个 next 指针**指向后继，尾节点指向空。它用"非连续存储 + 顺序访问"换取**任意位置 O(1) 插入/删除**——是栈、队列、哈希表拉链等结构的实现基座；代价是无法随机访问、缓存局部性差。

## 核心概念

- **节点（node）**：数据 + 一个 next 链接。
- **head**：头节点引用——整条链表的唯一入口，遍历全靠它。
- **非连续存储**：节点散布在内存各处，靠指针维系顺序。
- **单向遍历**：只能从头到尾走，无法回头。

## 工作机制

### 结构

```text
head → [data|next] → [data|next] → [data|next] → None
```

### 复杂度

| 操作 | 复杂度 | 说明 |
| --- | --- | --- |
| 头部插入/删除 | O(1) | 改 head 指针 |
| 已知前驱的插入/删除 | O(1) | 改两条指针 |
| 查找/访问第 i 个 | O(n) | 必须从 head 顺序走 |
| 反向遍历 | 不支持 | 无 prev 指针（见 [[doubly-linked-list]]） |

### 与数组对比

| | 链表 | 数组 |
| --- | --- | --- |
| 存储 | 非连续 | 连续 |
| 插入/删除 | 高效 | 低效（搬移） |
| 访问 | 顺序 | 随机 |
| 缓存局部性 | 差 | 好 |

## 常见误区

- **"链表插入删除总是 O(1)"**：前提是已持有目标位置（前驱）指针；找到这个位置本身要 O(n)。
- **"链表省内存"**：每个节点多存一个指针，且分散分配导致碎片；小对象场景总内存可能比数组更高。
- **"用链表遍历和数组一样快"**：缓存局部性差使链表遍历在实践中明显慢于数组顺序扫描。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| sll-fundamental / sll-non-contiguous / sll-definition / sll-head | web-computer-science-singly-linked-list | 定义、节点构成、head 入口 |
| sll-vs-array | web-computer-science-singly-linked-list + wiki-linked-list | 插删高效/顺序访问/缓存对比 |
| sll-linear-access / sll-benefit | wiki-linked-list（Wikipedia） | 线性访问代价、非连续插入优势 |

## 待验证项

无。

## 关联知识

- [[doubly-linked-list]] —— 加 prev 指针的双向版本。
- [[circular-linked-list]] —— 尾节点回指头节点的环形版本。
- [[stack]] / [[queue]] —— 用单链表即可实现。
- [[arrays]] —— 对照结构：连续存储与随机访问。

## 详细章节

### 定义

单链表是一种链表：每个节点包含两样东西——数据与连接到另一节点的链接；每个节点只有一个链接指向下一个节点。链表整体是线性数据结构，元素不必连续存放，节点间用链接相连。第一个节点称为头节点，借助 head 与 next 链接可以遍历整条链表。

### 访问模型

节点串行链接：访问任何节点都必须先访问其前驱，因此无法随机访问，访问时间与节点数成线性——这也给流水线化带来困难。

### 应用

- 实现栈、队列、双端队列。
- 哈希表的冲突拉链。
- 任意位置的动态插入/删除场景（如内存管理空闲链表、多项式表示）。

## 参考

- https://en.wikipedia.org/wiki/Linked_list
- https://www.geeksforgeeks.org/dsa/singly-linked-list-tutorial/
