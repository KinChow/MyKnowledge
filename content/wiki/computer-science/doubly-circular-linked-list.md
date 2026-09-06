---
aliases:
- Doubly Circular Linked List
- Circular Doubly Linked List
- 双向循环链表
- 循环双链表
confidentiality: public
domain: computer-science
evidence:
- claim: 双向循环链表的底座仍是循环链表的定义——最后一个节点指回第一个节点，形成闭环。
  claim_id: dcll-base
  support: direct
  supporting_quotes:
  - evidence_id: evidence-355e5aff8fbb
    exact: |-
      A circular linked list is a data structure where the last node points back to the first node, forming a closed loop.
  - evidence_id: evidence-3ac0049e1914
    exact: |-
      Circularly linked lists can be either singly or doubly linked.
  targets:
  - evidence_id: evidence-355e5aff8fbb
    source_id: web-computer-science-doubly-circular-linked-list
  - evidence_id: evidence-3ac0049e1914
    source_id: wiki-linked-list
- claim: 循环双链表中每个节点有 prev 与 next 两个指针，类似双链表；除尾节点存首节点地址外，首节点也会存尾节点地址——两个方向都成环。
  claim_id: dcll-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-b089d48016e4
    exact: |-
      In circular doubly linked list, each node has two pointers prev and next, similar to doubly linked list.
  - evidence_id: evidence-0348bb935fa5
    exact: |-
      Here, in addition to the last node storing the address of the first node, the first node will also store the address of the last node.
  targets:
  - evidence_id: evidence-b089d48016e4
    source_id: web-computer-science-doubly-circular-linked-list
  - evidence_id: evidence-0348bb935fa5
    source_id: web-computer-science-doubly-circular-linked-list
- claim: 双链表的通用优点适用于双向循环形态：空间与基本操作开销更大，但支持双向快速顺序访问、往往更易操纵；已知节点地址即可常数次插入/删除。
  claim_id: dcll-tradeoffs
  support: direct
  supporting_quotes:
  - evidence_id: evidence-9ef0e141f101
    exact: |-
      Double-linked lists require more space per node (unless one uses XOR-linking), and their elementary operations are more expensive; but they are often easier to manipulate because they allow fast and easy sequential access to the list in both directions.
  - evidence_id: evidence-8c7e9f4376d8
    exact: |-
      In a doubly linked list, one can insert or delete a node in a constant number of operations given only that node's address. To do the same in a singly linked list, one must have the address of the pointer to that node, which is either the handle for the whole list (in case of the first node) or the link field in the previous node.
  targets:
  - evidence_id: evidence-9ef0e141f101
    source_id: wiki-linked-list
  - evidence_id: evidence-8c7e9f4376d8
    source_id: wiki-linked-list
- claim: 循环链表的句柄优点同样适用于双向循环形态：指向任一节点的指针可作为整条链的句柄；持尾节点指针即能轻易访问首节点——需要访问两端的队列类应用只需一个指针管理。
  claim_id: dcll-handle
  support: direct
  supporting_quotes:
  - evidence_id: evidence-d0a6e5f269a8
    exact: |-
      With a circular list, a pointer to the last node gives easy access also to the first node, by following one link. Thus, in applications that require access to both ends of the list (e.g., in the implementation of a queue), a circular structure allows one to handle the structure by a single pointer, instead of two.
  targets:
  - evidence_id: evidence-d0a6e5f269a8
    source_id: wiki-linked-list
id: doubly-circular-linked-list
kind: reference
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- wiki-linked-list
- web-computer-science-doubly-circular-linked-list
- working-computer-science-doubly-circular-linked-list
status: published
tags:
- data-structure
- linked-list
title: 双向循环链表
updated_at: '2026-09-05'
---
# 双向循环链表

## 一句话结论

双向循环链表（Circular Doubly Linked List）是链表家族的"满配形态"：**prev/next 双指针 + 首尾互指成环**。任意节点出发都能双向走完整圈；持一个节点指针即可管理整条链。它是 Linux 内核 `list_head`、LRU 缓存等高频 O(1) 摘除场景的标准底座。

## 核心概念

- **双指针成环**：每个节点有 prev 与 next，与双链表相同。
- **首尾互指**：尾节点存首节点地址，首节点也存尾节点地址——两个方向都是环。
- **单指针句柄**：指向任一节点的指针即可代表整条链表。
- **无 null**：任何 next/prev 都不为空，遍历以"回到出发点"终止。

## 工作机制

### 结构

```text
   ┌──────────────────────────────┐
   ↓                              │
⇄ [A] ⇄ [B] ⇄ [C] ⇄ [D] ──────────┘
   ↑                              │
   └──────────────────────────────┘
（A.prev = D，D.next = A：首尾互指）
```

### 与其他链表的组合关系

| | 单向 | 双向 |
| --- | --- | --- |
| 线性（NULL 结尾） | [[singly-linked-list]] | [[doubly-linked-list]] |
| 环形 | [[circular-linked-list]] | **本页** |

### 复杂度

| 操作 | 复杂度 |
| --- | --- |
| 已知节点的前插/后插/删除 | O(1) |
| 从任一节点双向遍历 | O(n) |
| 维护单指针句柄的头尾操作 | O(1) |

## 常见误区

- **"循环双链表需要 head 指针"**：不需要——任意一个节点指针就是句柄；实践中常用一个哨兵（dummy）节点统一插入/删除边界。
- **"遍历用 `while (p != NULL)`"**：环里没有 NULL，会死循环；正确终止条件是"回到出发点"。
- **"指针多只是浪费"**：prev 指针买来的是 O(1) 双向摘除——这正是 LRU/内核链表选它的原因。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| dcll-base | web-computer-science-doubly-circular-linked-list + wiki-linked-list | 闭环定义；循环链表可单链可双链 |
| dcll-definition | web-computer-science-doubly-circular-linked-list | prev/next 双指针；首尾互指 |
| dcll-tradeoffs / dcll-handle | wiki-linked-list（Wikipedia） | 双链取舍、常数次操作、单指针句柄 |

## 待验证项

- 哨兵节点（sentinel）在该形态下的标准写法与 Linux `list_head` 案例未收录公开源，待补。

## 关联知识

- [[doubly-linked-list]] —— 去掉环形即得线性双链表。
- [[circular-linked-list]] —— 去掉 prev 即得循环单链表。
- [[singly-linked-list]] —— 最基础的形态。
- [[data-structure-optimization]] —— LRU/内核对象链的选型依据。

## 详细章节

### 定义

双向循环链表 = 循环 + 双向：每个节点有 prev 与 next 两个指针（同双链表），且首尾互指——尾节点存首节点地址，首节点也存尾节点地址。循环链表本就可由单链或双链实现，本页是双链实现。

### 取舍

继承双链表的优点与代价：每节点空间更大、基本操作更贵，但可双向快速顺序访问、更易操纵；已知节点地址即可常数次插入/删除。再叠加环形句柄优点：任一节点指针即可管理整条链，两端访问只需一个指针。

### 应用

- 队列/ deque：持一个句柄指针，两端 O(1)。
- 轮转调度：沿环循环遍历不终止。
- 需要任意位置 O(1) 摘除的链式容器（配合外部索引）。

## 参考

- https://en.wikipedia.org/wiki/Linked_list#Circularly_linked_list
- https://www.geeksforgeeks.org/dsa/circular-linked-list/
