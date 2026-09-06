---
aliases:
- Generic Tree
- N-ary Tree
- 多叉树
- N 叉树
confidentiality: public
domain: computer-science
evidence:
- claim: 通用树是节点的集合：每个节点由数据记录和指向其孩子的引用列表组成（不允许重复引用）；与链表不同，每个节点存储多个节点的地址，每个节点存其孩子地址，首节点地址存在单独的 root 指针里。
  claim_id: gt-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-f9bac1c8c445
    exact: |-
      Generic trees are a collection of nodes where each node is a data structure that consists of records and a list of references to its children(duplicate references are not allowed).
  - evidence_id: evidence-46c603cf9e8c
    exact: |-
      Unlike the linked list, each node stores the address of multiple nodes.
  - evidence_id: evidence-62968fd58026
    exact: |-
      Every node stores address of its children and the very first node's address will be stored in a separate pointer called root.
  targets:
  - evidence_id: evidence-f9bac1c8c445
    source_id: web-computer-science-generic-tree
  - evidence_id: evidence-46c603cf9e8c
    source_id: web-computer-science-generic-tree
  - evidence_id: evidence-62968fd58026
    source_id: web-computer-science-generic-tree
- claim: 通用树是 N 叉树，性质为：每个节点可有多个孩子；且每个节点的孩子数量事先未知。
  claim_id: gt-properties
  support: direct
  supporting_quotes:
  - evidence_id: evidence-5263a6f6a6ac
    exact: |-
      The Generic trees are the N-ary trees which have the following properties:
  - evidence_id: evidence-fa4db717e798
    exact: |-
      Many children at every node.
  - evidence_id: evidence-58d6bbdb5a2e
    exact: |-
      The number of nodes for each node is not known in advance.
  targets:
  - evidence_id: evidence-5263a6f6a6ac
    source_id: web-computer-science-generic-tree
  - evidence_id: evidence-fa4db717e798
    source_id: web-computer-science-generic-tree
  - evidence_id: evidence-58d6bbdb5a2e
    source_id: web-computer-science-generic-tree
- claim: 为每个节点预分配固定数量孩子指针的朴素表示有两大缺点：多数情况下指针用不到造成大量内存浪费；孩子数量事先未知导致容量难以确定。
  claim_id: gt-naive-drawback
  support: direct
  supporting_quotes:
  - evidence_id: evidence-5e89cf9c3624
    exact: |-
      Memory Wastage - All the pointers are not required in all the cases. Hence, there is lot of memory wastage.
  - evidence_id: evidence-519b571cd237
    exact: |-
      Unknown number of children - The number of children for each node is not known in advance.
  targets:
  - evidence_id: evidence-5e89cf9c3624
    source_id: web-computer-science-generic-tree
  - evidence_id: evidence-519b571cd237
    source_id: web-computer-science-generic-tree
- claim: 用链表存孩子地址无法随机访问任意孩子的地址（访问代价高）；用数组可随机访问，但只能存固定数量的孩子地址。
  claim_id: gt-array-vs-list
  support: direct
  supporting_quotes:
  - evidence_id: evidence-83dfa21cbba1
    exact: |-
      In Linked list, we can not randomly access any child's address. So it will be expensive.
  - evidence_id: evidence-befe247be0b1
    exact: |-
      In array, we can randomly access the address of any child, but we can store only fixed number of children's addresses in it.
  targets:
  - evidence_id: evidence-83dfa21cbba1
    source_id: web-computer-science-generic-tree
  - evidence_id: evidence-befe247be0b1
    source_id: web-computer-science-generic-tree
- claim: 更好的做法是用动态数组存孩子地址：既能随机访问任意孩子的地址，容量又不固定。
  claim_id: gt-dynamic-array
  support: direct
  supporting_quotes:
  - evidence_id: evidence-18a3b8828169
    exact: |-
      We can use Dynamic Arrays for storing the address of children. We can randomly access any child's address and the size of the vector is also not fixed.
  targets:
  - evidence_id: evidence-18a3b8828169
    source_id: web-computer-science-generic-tree
- claim: first child/next sibling（左孩子/右兄弟）表示法：把同一父节点的孩子们（兄弟）从左到右链接起来，并移除父节点指向除第一个孩子之外其他孩子的链接。
  claim_id: gt-sibling-repr
  support: direct
  supporting_quotes:
  - evidence_id: evidence-e5dcfc7cecfe
    exact: |-
      In the first child/next sibling representation, the steps taken are:
  - evidence_id: evidence-dc543a38b4da
    exact: |-
      At each node-link the children of the same parent(siblings) from left to right.
  - evidence_id: evidence-9b50296a1951
    exact: |-
      Remove the links from parent to all children except the first child.
  targets:
  - evidence_id: evidence-e5dcfc7cecfe
    source_id: web-computer-science-generic-tree
  - evidence_id: evidence-dc543a38b4da
    source_id: web-computer-science-generic-tree
  - evidence_id: evidence-9b50296a1951
    source_id: web-computer-science-generic-tree
- claim: 左孩子/右兄弟表示法的优点：内存高效（不需要额外链接）；可按二叉树处理——任何通用树都能转成这种二叉表示，用 firstChild/nextSibling 取代左右指针；许多算法因它就是二叉树而更容易表达；每个节点定长，无需辅助数组或向量。
  claim_id: gt-sibling-advantages
  support: direct
  supporting_quotes:
  - evidence_id: evidence-24f1ad12af22
    exact: |-
      Memory efficient - No extra links are required, hence a lot of memory is saved.
  - evidence_id: evidence-e4d90aa02a5b
    exact: |-
      Treated as binary trees - Since we are able to convert any generic tree to binary representation, we can treat all generic trees with a first child/next sibling representation as binary trees.
  - evidence_id: evidence-f08329fa0d14
    exact: |-
      Many algorithms can be expressed more easily because it is just a binary tree.
  - evidence_id: evidence-8266d22eb01e
    exact: |-
      Each node is of fixed size ,so no auxiliary array or vector is required.
  targets:
  - evidence_id: evidence-24f1ad12af22
    source_id: web-computer-science-generic-tree
  - evidence_id: evidence-e4d90aa02a5b
    source_id: web-computer-science-generic-tree
  - evidence_id: evidence-f08329fa0d14
    source_id: web-computer-science-generic-tree
  - evidence_id: evidence-8266d22eb01e
    source_id: web-computer-science-generic-tree
id: generic-tree
kind: reference
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-generic-tree
- working-computer-science-generic-tree
status: published
tags:
- data-structure
- tree
title: 通用树
updated_at: '2026-09-05'
---
# 通用树

## 一句话结论

通用树（Generic Tree / N 叉树）是**每个节点可有任意多个孩子、且孩子数事先未知**的树结构：与链表不同，每个节点要存多个孩子的地址。核心工程问题是**孩子指针怎么存**——固定指针槽浪费内存，动态数组（`vector<Node*>`）是直接解，**左孩子/右兄弟表示法**则是把它转化为二叉树的经典方案。

## 核心概念

- **N 叉性质**：每节点多孩子 + 孩子数事先未知——这两条共同决定了"固定槽位表示必然有缺陷"。
- **孩子存储三方案**：固定指针槽 → 数组/链表 → 动态数组；以及结构级的左孩子/右兄弟表示。
- **左孩子/右兄弟**：每个节点只存 `firstChild` 与 `nextSibling` 两个指针，任意通用树可转化为二叉树形态。
- **root 指针**：与链表一致，首节点地址存于独立的 root 指针。

## 工作机制

### 表示法一：固定指针槽（朴素）

按最坏情形（设最多 k 个孩子）给每个节点预分配 k 个指针。缺点：多数节点孩子远少于 k，指针大量闲置浪费内存；且孩子数事先未知，k 难以确定。

### 表示法二：数组 vs 链表存孩子地址

- **链表**：可以动态增长，但无法随机访问某个孩子的地址，按位置取孩子代价高。
- **数组**：可随机访问孩子，但容量固定，退化回"孩子数未知"的矛盾。

### 表示法三：动态数组（推荐）

`vector<Node*> children`：既保留随机访问能力，容量又不固定，直接化解矛盾。

### 表示法四：左孩子/右兄弟（结构级方案）

1. 同一父节点的孩子们（兄弟）从左到右用 `nextSibling` 链接。
2. 父节点只保留指向**第一个孩子**的链接，移除到其余孩子的链接。

效果：节点定长（两个指针）、无内存浪费，且整棵树成为形态上的二叉树——`firstChild` 相当于左指针、`nextSibling` 相当于右指针，二叉树上的算法（遍历、递归）都可以直接套用。

## 示例或代码

左孩子/右兄弟节点定义：

```c
struct Node {
    int key;
    struct Node *firstChild;   // 第一个孩子
    struct Node *nextSibling;  // 下一个兄弟
};
```

## 常见误区

- **"通用树就是二叉树"**：二叉树是通用树的特例（度 ≤ 2）；左孩子/右兄弟只是把通用树**表示成**二叉树形态，逻辑结构仍是 N 叉。
- **"数组表示一定比链表好"**：数组给随机访问但锁死容量；链表反之。动态数组才是两者折中。
- **"固定指针槽简单所以常用"**：孩子数未知时 k 无法选，内存浪费比例可达数倍，工程上基本不用。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| gt-definition / gt-properties | web-computer-science-generic-tree | 定义 + N 叉两性质 |
| gt-naive-drawback / gt-array-vs-list / gt-dynamic-array | web-computer-science-generic-tree | 三种孩子存储方案的取舍 |
| gt-sibling-repr / gt-sibling-advantages | web-computer-science-generic-tree | 左孩子/右兄弟的做法与四条优点 |

## 待验证项

- 层序遍历与"父数组表示法求树高"两个主题在源中仅存标题，未收录正文；需要时另行补源。

## 关联知识

- [[binary-tree]] —— 左孩子/右兄弟表示的目标形态；二叉树算法可直接套用。
- [[b-tree]] —— 多路平衡树的特例：孩子数有上下界约束的通用树。
- [[singly-linked-list]] —— 兄弟链本质是单链表；nextSibling 即 next 指针。

## 详细章节

### 定义与性质

通用树是节点的集合：每个节点由数据记录与指向其孩子的引用列表组成（不允许重复引用）。不同于链表（每节点只存一个后继地址），通用树每个节点存储多个孩子的地址，首节点地址存在单独的 root 指针中。它是 N 叉树：每节点可有多个孩子，且孩子数量事先未知。

### 左孩子/右兄弟表示法

- 同一父节点的兄弟从左到右成链。
- 父节点仅链接第一个孩子。
- 结果：无多余链接、节点定长、可用二叉树算法遍历全部元素（从父节点的 firstChild 出发沿兄弟链走完整层）。

### 应用场景

- 文件系统目录树（任意深度、任意扇出）。
- DOM / UI 控件树、组织架构树。
- 编译器 AST（节点扇出不定的语法树）。

## 参考

- https://www.geeksforgeeks.org/dsa/generic-treesn-array-trees/
