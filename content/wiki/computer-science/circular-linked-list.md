---
aliases:
- Circular Linked List
- 循环链表
- 环形链表
confidentiality: public
domain: computer-science
evidence:
- claim: 循环链表是一种最后一个节点指回第一个节点、形成闭环的数据结构。
  claim_id: cll-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-c128c6562a10
    exact: |-
      A circular linked list is a data structure where the last node points back to the first node, forming a closed loop.
  targets:
  - evidence_id: evidence-c128c6562a10
    source_id: web-computer-science-circular-linked-list
- claim: 结构上所有节点连成一个圆，可以连续遍历而不会遇到 NULL；与普通链表的差别在于：普通链表尾节点指向
    NULL，循环链表尾节点指向第一个节点。
  claim_id: cll-structure
  support: direct
  supporting_quotes:
  - evidence_id: evidence-6c211b3f2ae0
    exact: |-
      Structure: All nodes are connected in a circle, enabling continuous traversal without encountering NULL .
  - evidence_id: evidence-a2708ecb9988
    exact: |-
      Difference from Regular Linked List: In a regular linked list, the last node points to NULL , whereas in a circular linked list, it points to the first node.
  targets:
  - evidence_id: evidence-6c211b3f2ae0
    source_id: web-computer-science-circular-linked-list
  - evidence_id: evidence-a2708ecb9988
    source_id: web-computer-science-circular-linked-list
- claim: 循环链表的用途：适合调度、播放列表管理等需要平滑且重复轮转的任务场景。
  claim_id: cll-uses
  support: direct
  supporting_quotes:
  - evidence_id: evidence-ef7973630fcb
    exact: |-
      Uses: Ideal for tasks like scheduling and managing playlists, where smooth and repeated.
  targets:
  - evidence_id: evidence-ef7973630fcb
    source_id: web-computer-science-circular-linked-list
- claim: 循环链表分两类：循环单链表——每个节点只有 next 指针，尾节点 next 指回首节点成环，只能单向移动；循环双链表——每个节点有
    prev 与 next 两个指针，除尾节点存首节点地址外，首节点也存尾节点地址。
  claim_id: cll-types
  support: direct
  supporting_quotes:
  - evidence_id: evidence-8a313224ebde
    exact: |-
      In Circular Singly Linked List, each node has just one pointer called the "next" pointer. The next pointer of the last node points back to the first node and this results in forming a circle. In this type of Linked list, we can only move through the list in one direction.
  - evidence_id: evidence-a1fc70db70fb
    exact: |-
      In circular doubly linked list, each node has two pointers prev and next, similar to doubly linked list.
  - evidence_id: evidence-40a2f4b646a1
    exact: |-
      Here, in addition to the last node storing the address of the first node, the first node will also store the address of the last node.
  targets:
  - evidence_id: evidence-8a313224ebde
    source_id: web-computer-science-circular-linked-list
  - evidence_id: evidence-a1fc70db70fb
    source_id: web-computer-science-circular-linked-list
  - evidence_id: evidence-40a2f4b646a1
    source_id: web-computer-science-circular-linked-list
- claim: 在 Wikipedia 的表述中：循环链表所有节点连成连续的环、不使用 null；对有头有尾的列表（如队列）只需存尾节点引用——尾节点之后的下一个节点就是首节点；从尾部加入、从头部移除都是常数时间。循环链表可以用单链或双链实现。
  claim_id: cll-wiki-structure
  support: direct
  supporting_quotes:
  - evidence_id: evidence-662ca96b80b6
    exact: |-
      In a circularly linked list, all nodes are linked in a continuous circle, without using null. For lists with a front and a back (such as a queue), one stores a reference to the last node in the list. The next node after the last node is the first node. Elements can be added to the back of the list and removed from the front in constant time.
  - evidence_id: evidence-3ac0049e1914
    exact: |-
      Circularly linked lists can be either singly or doubly linked.
  targets:
  - evidence_id: evidence-662ca96b80b6
    source_id: wiki-linked-list
  - evidence_id: evidence-3ac0049e1914
    source_id: wiki-linked-list
- claim: 用循环链表时，指向尾节点的指针沿一条链接即可轻松访问首节点；因此需要访问两端的应用（如队列实现）用环形结构只需一个指针管理，而非两个。它也适合表示天然循环的数据——多边形的顶点、按
    FIFO 使用与释放的缓冲池、按轮转（round-robin）分时的一组进程。
  claim_id: cll-apps
  support: direct
  supporting_quotes:
  - evidence_id: evidence-d0a6e5f269a8
    exact: |-
      With a circular list, a pointer to the last node gives easy access also to the first node, by following one link. Thus, in applications that require access to both ends of the list (e.g., in the implementation of a queue), a circular structure allows one to handle the structure by a single pointer, instead of two.
  - evidence_id: evidence-2a0d730d509f
    exact: |-
      A circularly linked list may be a natural option to represent arrays that are naturally circular, e.g. the corners of a polygon, a pool of buffers that are used and released in FIFO (first in, first out) order, or a set of processes that should be time-shared in round-robin order.
  targets:
  - evidence_id: evidence-d0a6e5f269a8
    source_id: wiki-linked-list
  - evidence_id: evidence-2a0d730d509f
    source_id: wiki-linked-list
id: circular-linked-list
kind: reference
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- wiki-linked-list
- web-computer-science-circular-linked-list
- working-computer-science-circular-linked-list
status: published
tags:
- data-structure
- linked-list
title: 循环链表
updated_at: '2026-09-05'
---
# 循环链表

## 一句话结论

循环链表把链表的尾部接到头部形成**闭环**：尾节点的 next 指回首节点，遍历永远不会碰到 NULL。它是"天然循环"问题的原生表示——**轮转调度（round-robin）、播放列表、循环缓冲**；只要维护一个尾节点指针，就能同时 O(1) 访问两端。

## 核心概念

- **闭环**：尾节点指向首节点，没有 null 终止。
- **循环单链表 / 循环双链表**：单链或双链都可循环化。
- **尾指针句柄**：一个指向尾节点的指针即可代表整条链表——沿一条链接就到首节点。
- **连续遍历**：任何节点出发都能走完整圈。

## 工作机制

### 结构

```text
→ [A] → [B] → [C] ─┐
↑──────────────────┘      （循环单链表）

⇄ [A] ⇄ [B] ⇄ [C] ⇄      （循环双链表：首尾互指）
```

### 两类实现

| | 循环单链表 | 循环双链表 |
| --- | --- | --- |
| 指针 | 只有 next | prev + next |
| 尾→首 | 尾节点 next 指向首节点 | 尾节点存首节点地址 |
| 首→尾 | 需绕一圈 | **首节点也存尾节点地址** |
| 方向 | 单向 | 双向 |

### 复杂度

| 操作 | 复杂度 |
| --- | --- |
| 尾部加入 + 头部移除（队列模式，持尾指针） | O(1) |
| 从任一节点遍历全表 | O(n) |
| 查找 | O(n) |

## 常见误区

- **"循环链表没有终止条件"**：遍历终止条件改为"回到出发点"（do-while：先走再判 `p != head`），用普通 `while (p != NULL)` 会死循环。
- **"循环链表和环形缓冲区（ring buffer）一样"**：环形缓冲是**定长数组**取模实现；循环链表是动态节点成环——语义相似，实现与性能特征不同。
- **"循环链表可以替代双向链表"**：循环≠双向；循环单链表依然只能单向走。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| cll-definition / cll-structure / cll-uses / cll-types | web-computer-science-circular-linked-list | 闭环定义、与普通链表差异、两类实现、用途 |
| cll-wiki-structure / cll-apps | wiki-linked-list（Wikipedia） | 无 null 连续环、尾指针句柄、队列 O(1)、天然循环应用 |

## 待验证项

无。

## 关联知识

- [[singly-linked-list]] / [[doubly-linked-list]] —— 两类基础链表，循环化后分别得到两类循环链表。
- [[doubly-circular-linked-list]] —— 循环双链表的专页。
- [[queue]] —— 循环单链表 + 尾指针即队列实现。
- [[arrays]] —— 循环缓冲区的数组版实现。

## 详细章节

### 定义

循环链表：最后一个节点指回第一个节点形成闭环；所有节点连成圆，可连续遍历而不遇到 NULL。与普通链表的本质差别仅在尾节点的指向——普通链表指向 NULL，循环链表指向首节点。

### 两类实现

1. **循环单链表**：每节点只有 next 指针，尾节点 next 指回首节点成环，只能单向移动。
2. **循环双链表**：每节点有 prev 与 next；除尾节点存首节点地址外，首节点也存尾节点地址——两端都是 O(1)。

### 应用

- 调度与播放列表管理（平滑、重复轮转）。
- 天然循环数据的表示：多边形顶点、FIFO 缓冲池、round-robin 进程分时。
- 队列实现：持一个尾指针即可同时访问两端。

## 参考

- https://en.wikipedia.org/wiki/Linked_list#Circularly_linked_list
- https://www.geeksforgeeks.org/dsa/circular-linked-list/
