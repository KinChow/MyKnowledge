---
aliases:
- Stack
- 栈数据结构
- LIFO
confidentiality: public
domain: computer-science
evidence:
- claim: 栈中元素加入或移除的次序称为后进先出（Last In, First Out，LIFO）。
  claim_id: stk-lifo
  support: direct
  supporting_quotes:
  - evidence_id: evidence-d286628a0b15
    exact: |-
      The order in which elements are added to or removed from a stack is described as last in, first out, referred to by the acronym LIFO.
  targets:
  - evidence_id: evidence-d286628a0b15
    source_id: wiki-stack-adt
- claim: 如同实物堆叠：从栈顶取元素容易，但访问栈中更深的元素可能需要先移除上面的多个元素。
  claim_id: stk-top-access
  support: direct
  supporting_quotes:
  - evidence_id: evidence-d10e607c26e6
    exact: |-
      As with a stack of physical objects, this structure makes it easy to take an item off the top of the stack, but accessing a datum deeper in the stack may require removing multiple other items first.
  targets:
  - evidence_id: evidence-d10e607c26e6
    source_id: wiki-stack-adt
- claim: peek 操作可以在不修改栈的情况下返回最后加入元素的值（栈顶项）。
  claim_id: stk-peek
  support: direct
  supporting_quotes:
  - evidence_id: evidence-4593be24621b
    exact: |-
      Additionally, a peek operation can, without modifying the stack, return the value of the last element added (the item at the top of the stack).
  targets:
  - evidence_id: evidence-4593be24621b
    source_id: wiki-stack-adt
- claim: 栈被视为顺序集合：一端——栈顶（top）——是 push 和 pop 操作唯一可以发生的位置；另一端（栈底，bottom）固定。
  claim_id: stk-one-end
  support: direct
  supporting_quotes:
  - evidence_id: evidence-13a035e39fcd
    exact: |-
      Considered a sequential collection, a stack has one end which is the only position at which the push and pop operations may occur, the top of the stack, and is fixed at the other end, the bottom.
  targets:
  - evidence_id: evidence-13a035e39fcd
    source_id: wiki-stack-adt
- claim: 栈可实现为有界容量：若栈已满且没有足够空间接受另一个元素，栈处于栈溢出（stack overflow）状态。
  claim_id: stk-overflow
  support: direct
  supporting_quotes:
  - evidence_id: evidence-4dc02e593e5a
    exact: |-
      A stack may be implemented to have a bounded capacity. If the stack is full and does not contain enough space to accept another element, the stack is in a state of stack overflow.
  targets:
  - evidence_id: evidence-4dc02e593e5a
    source_id: wiki-stack-adt
- claim: 栈可以轻易地用数组或链表实现——它只是 list 的特例；把一个结构标识为栈的不是实现而是接口：用户只被允许对底层数组或链表做
    push/pop；例如可以用指向栈顶元素的单链表实现栈。
  claim_id: stk-impl
  support: direct
  supporting_quotes:
  - evidence_id: evidence-322b64c2a9f2
    exact: |-
      A stack can be easily implemented either through an array or a linked list, as it is merely a special case of a list. In either case, what identifies the data structure as a stack is not the implementation but the interface: the user is only allowed to pop or push items onto the array or linked list, with few other helper operations.
  - evidence_id: evidence-78c22ee5ee5f
    exact: |-
      A stack may be implemented as, for example, a singly linked list with a pointer to the top element.
  targets:
  - evidence_id: evidence-322b64c2a9f2
    source_id: wiki-stack-adt
  - evidence_id: evidence-78c22ee5ee5f
    source_id: wiki-stack-adt
- claim: push 在检查溢出后添加元素并递增 top 索引；pop 在检查下溢后递减 top
    索引，并返回之前位于栈顶的元素。
  claim_id: stk-push-pop
  support: direct
  supporting_quotes:
  - evidence_id: evidence-1fae9bf0b3f4
    exact: |-
      The push operation adds an element and increments the top index, after checking for overflow:
  - evidence_id: evidence-57bb10891387
    exact: |-
      Similarly, pop decrements the top index after checking for underflow, and returns the item that was previously the top one:
  targets:
  - evidence_id: evidence-1fae9bf0b3f4
    source_id: wiki-stack-adt
  - evidence_id: evidence-57bb10891387
    source_id: wiki-stack-adt
- claim: 栈用于表达式求值与语法解析：逆波兰表示法的计算器用栈保存值；表达式可用前缀/后缀/中缀表示，相互转换可用栈完成；许多编译器在翻译为低级代码前用栈解析语法。
  claim_id: stk-expr
  support: direct
  supporting_quotes:
  - evidence_id: evidence-63eafcee671c
    exact: |-
      Calculators that employ reverse Polish notation use a stack structure to hold values. Expressions can be represented in prefix, postfix or infix notations and conversion from one form to another may be accomplished using a stack. Many compilers use a stack to parse syntax before translation into low-level code.
  targets:
  - evidence_id: evidence-63eafcee671c
    source_id: wiki-stack-adt
- claim: 栈的另一个重要应用是回溯：把最后正确的点压入栈，走错路径时从栈中弹出即可回到该点。
  claim_id: stk-backtrack
  support: direct
  supporting_quotes:
  - evidence_id: evidence-4fe264776635
    exact: |-
      Another important application of stacks is backtracking.
  - evidence_id: evidence-a7ae1699eb8d
    exact: |-
      This can be achieved through the use of stacks, as a last correct point can be pushed onto the stack, and popped from the stack in case of an incorrect path.
  targets:
  - evidence_id: evidence-4fe264776635
    source_id: wiki-stack-adt
  - evidence_id: evidence-a7ae1699eb8d
    source_id: wiki-stack-adt
- claim: 不少小型微处理器直接在硬件中实现栈，一些微控制器有不可直接访问的定深栈。
  claim_id: stk-hardware
  support: direct
  supporting_quotes:
  - evidence_id: evidence-def936ce83dc
    exact: |-
      There is also a number of small microprocessors that implement a stack directly in hardware, and some microcontrollers have a fixed-depth stack that is not directly accessible.
  targets:
  - evidence_id: evidence-def936ce83dc
    source_id: wiki-stack-adt
id: stack
kind: reference
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- wiki-stack-adt
- web-computer-science-stack
- working-computer-science-stack
status: published
tags:
- data-structure
- stack
- lifo
title: 栈
updated_at: '2026-09-05'
---
# 栈

## 一句话结论

栈是一种**后进先出（LIFO）的顺序集合**：所有 push/pop 只发生在同一端——栈顶（top），另一端栈底固定。它是"最后发生的事最先处理"的抽象：函数调用、表达式求值、回溯、撤销操作都靠它。实现上只需数组或链表；**标识栈的不是实现而是接口**。

## 核心概念

- **LIFO**：最后进入的元素最先被移除。
- **栈顶（top）/ 栈底（bottom）**：操作端与固定端。
- **溢出 / 下溢**：有界栈满时 push 报 overflow；空栈时 pop 报 underflow。
- **peek/top**：只读栈顶不移除。

## 工作机制

### 核心操作

| 操作 | 语义 |
| --- | --- |
| push(x) | 检查溢出后写入元素、递增 top 索引 |
| pop() | 检查下溢后递减 top 索引，返回原栈顶元素 |
| peek() | 不修改栈，返回最后加入元素的值 |

### 实现

- **数组**：top 索引 + 定长数组（有界栈）。
- **单链表**：指向栈顶元素的指针做头插入/头删除。
- 要点：栈的本质是**接口约束**（只许 push/pop/peek），底层数组或链表只是载体。

### 复杂度

| 操作 | 复杂度 |
| --- | --- |
| push / pop / peek | O(1) |
| 深处访问 | O(n)（需先弹出上层元素） |

## 常见误区

- **"栈和内存栈是一回事"**：ADT 意义的栈是接口约束；硬件/调用栈只是它的实例（调用栈还带帧语义）。
- **"数组实现栈必然溢出"**：只有有界栈才可能溢出；动态数组可自动扩容。
- **"栈只能后进先出所以用途窄"**：恰恰相反——凡是"嵌套/回退"语义（调用、括号匹配、DFS、撤销）都天然是栈问题。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| stk-lifo / stk-top-access / stk-peek / stk-one-end | wiki-stack-adt（Wikipedia） | LIFO 定义、栈顶语义、peek |
| stk-overflow / stk-impl / stk-push-pop | wiki-stack-adt | 溢出、数组/链表实现、push/pop 步骤 |
| stk-expr / stk-backtrack / stk-hardware | wiki-stack-adt | 表达式求值、回溯、硬件栈 |

## 待验证项

无。

## 关联知识

- [[queue]] —— 对偶结构：队列 FIFO、栈 LIFO。
- [[binary-tree]] —— DFS（前/中/后序）的递归栈本质。
- [[cpp-class-and-raii]] —— 调用栈与对象生命周期。
- [[data-structure-optimization]] —— 深度优先场景选型。

## 详细章节

### 定义

栈中元素加入或移除的次序是后进先出（LIFO）——名称源于盘子叠放的生活类比。它是顺序集合：栈顶是 push/pop 唯一可发生的位置，栈底固定。如同实物堆叠，取栈顶容易，访问更深的元素可能要先移除其上的多个元素。

### 应用

- **表达式求值与语法解析**：逆波兰计算器用栈存值；前/中/后缀表示转换用栈；编译器翻译前用栈解析语法（多数语言是上下文无关语言，可用栈式机器解析）。
- **回溯**：迷宫寻路等场景，把最后正确点压栈、失败时弹栈回退。
- **硬件栈**：许多小型微处理器直接在硬件实现栈；部分微控制器有不可直接访问的定深栈。
- 函数调用栈（编译期内存管理）、撤销操作、DFS。

## 参考

- https://en.wikipedia.org/wiki/Stack_(abstract_data_type)
- https://www.geeksforgeeks.org/dsa/stack-data-structure/
