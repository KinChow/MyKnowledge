---
aliases:
- Doubly Linked List
- 双链表
- 双向链表
confidentiality: public
domain: computer-science
evidence:
- claim: 双链表是一种特殊的链表：每个节点既包含指向后继节点的指针，也包含指向前驱节点的指针。
  claim_id: dll-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-4f94beda7fef
    exact: |-
      A doubly linked list is a special type of linked list in which each node contains a pointer to the previous node as well as the next node in the structure.
  - evidence_id: evidence-b70e16480b71
    exact: |-
      In a doubly linked list, each node contains, besides the link to the next node, a second link field pointing to the previous node in the sequence.
  targets:
  - evidence_id: evidence-4f94beda7fef
    source_id: web-computer-science-doubly-linked-list
  - evidence_id: evidence-b70e16480b71
    source_id: wiki-linked-list
- claim: 双链表的特性：动态大小——节点可按需增删；双向导航——每个节点含前后两个指针，可向前也可向后遍历；内存开销——每个节点除数据外还要存前驱、后继两个指针。
  claim_id: dll-characteristics
  support: direct
  supporting_quotes:
  - evidence_id: evidence-76a39ee4b694
    exact: |-
      Dynamic size: The size of a doubly linked list can change dynamically, meaning that nodes can be added or removed as needed.
  - evidence_id: evidence-94a4ee85614c
    exact: |-
      Two-way navigation: In a doubly linked list, each node contains pointers to both the previous and next elements, allowing for navigation in both forward and backward directions.
  - evidence_id: evidence-98f0126ae9e7
    exact: |-
      Memory overhead: Each node in a doubly linked list requires memory for two pointers (previous and next), in addition to the memory required for the data stored in the node. This
  targets:
  - evidence_id: evidence-76a39ee4b694
    source_id: web-computer-science-doubly-linked-list
  - evidence_id: evidence-94a4ee85614c
    source_id: web-computer-science-doubly-linked-list
  - evidence_id: evidence-98f0126ae9e7
    source_id: web-computer-science-doubly-linked-list
- claim: 双链表每个节点空间开销更大（除非用 XOR 链接），基本操作也更昂贵；但它支持双向快速顺序访问，往往更易操纵。
  claim_id: dll-tradeoff
  support: direct
  supporting_quotes:
  - evidence_id: evidence-9ef0e141f101
    exact: |-
      Double-linked lists require more space per node (unless one uses XOR-linking), and their elementary operations are more expensive; but they are often easier to manipulate because they allow fast and easy sequential access to the list in both directions.
  targets:
  - evidence_id: evidence-9ef0e141f101
    source_id: wiki-linked-list
- claim: 在双链表中，仅凭节点地址就能用常数次操作插入或删除该节点；在单链表中做同样的事必须持有指向该节点的指针的地址（整表句柄或前驱节点的链接域）。有些算法本身就需要双向访问。
  claim_id: dll-constant-ops
  support: direct
  supporting_quotes:
  - evidence_id: evidence-8c7e9f4376d8
    exact: |-
      In a doubly linked list, one can insert or delete a node in a constant number of operations given only that node's address. To do the same in a singly linked list, one must have the address of the pointer to that node, which is either the handle for the whole list (in case of the first node) or the link field in the previous node.
  - evidence_id: evidence-5d91e2bb22e8
    exact: |-
      Some algorithms require access in both directions.
  targets:
  - evidence_id: evidence-8c7e9f4376d8
    source_id: wiki-linked-list
  - evidence_id: evidence-5d91e2bb22e8
    source_id: wiki-linked-list
- claim: 双链表可用于实现哈希表——按键高效存取数据的结构。
  claim_id: dll-apps
  support: direct
  supporting_quotes:
  - evidence_id: evidence-d1c33c347368
    exact: |-
      Implementing a Hash Table: Doubly linked lists can be used to implement hash tables, which are used to store and retrieve data efficiently based on a key.
  targets:
  - evidence_id: evidence-d1c33c347368
    source_id: web-computer-science-doubly-linked-list
id: doubly-linked-list
kind: reference
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- wiki-linked-list
- web-computer-science-doubly-linked-list
- working-computer-science-doubly-linked-list
status: published
tags:
- data-structure
- linked-list
title: 双链表
updated_at: '2026-09-05'
---
# 双链表

## 一句话结论

双链表在单链表基础上给每个节点加了 **prev 指针**：前后两个方向都能遍历。换来的是**已知节点地址即可 O(1) 删除/插入**（单链表做不到）与便捷的反向扫描；代价是每节点多一个指针的内存开销与更复杂的基本操作。LRU 缓存、文本编辑器、浏览器历史都靠它。

## 核心概念

- **prev + next**：每节点两个链接，分别指向前驱与后继。
- **双向导航**：正向与反向遍历都可行。
- **对称删除**：删除任意节点不需要其前驱信息——prev 指针就是前驱。
- **内存开销**：每节点多存一个指针（除非用 XOR 链接技巧）。

## 工作机制

### 结构

```text
None ← [prev|data|next] ⇄ [prev|data|next] ⇄ [prev|data|next] → None
```

### 与单链表的关键差异

| 能力 | 单链表 | 双链表 |
| --- | --- | --- |
| 仅凭节点地址删除该节点 | 不行（需前驱指针地址） | **可以，常数次操作** |
| 反向遍历 | 不支持 | 支持 |
| 每节点指针数 | 1 | 2 |
| 尾节点操作 | 需从头找 | 若维护 tail 则 O(1) |

### 复杂度

| 操作 | 复杂度 |
| --- | --- |
| 已知节点的前插/删除 | O(1) |
| 查找 | O(n) |
| 头尾插入（维护 head/tail） | O(1) |

## 常见误区

- **"双链表全面优于单链表"**：每节点多一倍指针开销、插入删除要维护两条链、不支持尾共享（tail-sharing），不能用作持久化结构。
- **"双向 = 查找更快"**：查找仍是 O(n)；双向只是导航能力，不是搜索加速。
- **"XOR 链接是常规手段"**：它省掉一个指针但调试困难、与 GC/并发不兼容，工程上罕见。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| dll-definition | web-computer-science-doubly-linked-list + wiki-linked-list | prev+next 定义 |
| dll-characteristics | web-computer-science-doubly-linked-list | 动态大小、双向导航、内存开销 |
| dll-tradeoff / dll-constant-ops | wiki-linked-list（Wikipedia） | 空间/操作代价、常数次删除、双向算法需求 |
| dll-apps | web-computer-science-doubly-linked-list | 哈希表实现 |

## 待验证项

无。

## 关联知识

- [[singly-linked-list]] —— 单指针的前身，对比理解 prev 的价值。
- [[doubly-circular-linked-list]] —— 双链 + 环形：首尾互指。
- [[queue]] —— deque 的双向链表实现。
- [[data-structure-optimization]] —— LRU 等需要 O(1) 双向摘除的场景。

## 详细章节

### 定义与特性

双链表的每个节点除指向后继的链接外，还有第二个链接域指向前驱（两个链接可称为 forward/backwards 或 next/prev）。三大特性：动态大小（节点按需增删）、双向导航（前驱后继指针支持前后两个方向遍历）、内存开销（每节点存两个指针）。

### 工程取舍

- 更多空间与更贵的基本操作，但双向顺序访问使其更易操纵。
- 已知节点地址即可常数次操作完成插入/删除；单链表必须持有"指向该节点指针"的地址（表句柄或前驱链接域）。
- 某些算法天然需要双向访问。

### 应用

- 哈希表的桶内拉链（配合 O(1) 删除）。
- LRU 缓存：哈希表 + 双链表是标准组合。
- 浏览器前进/后退历史、文本编辑器的撤销/重做链、deque 实现。

## 参考

- https://en.wikipedia.org/wiki/Linked_list
- https://en.wikipedia.org/wiki/Doubly_linked_list
- https://www.geeksforgeeks.org/dsa/doubly-linked-list-tutorial/
