---
aliases:
- Binary Tree
- 二叉树遍历
confidentiality: public
domain: computer-science
evidence:
- claim: 二叉树是每个父节点至多有两个孩子的树数据结构；每个节点由三部分组成，其中两部分是左孩子的地址与右孩子的地址。
  claim_id: bintree-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-fc3cd706c50d
    exact: |-
      A binary tree is a tree data structure in which each parent node can have at most two children. Each node of a binary tree consists of three items:
  - evidence_id: evidence-99ac291d5c8f
    exact: |-
      address of left child
  - evidence_id: evidence-445127cc9c8d
    exact: |-
      address of right child
  targets:
  - evidence_id: evidence-fc3cd706c50d
    source_id: programiz-binary-tree-v2
  - evidence_id: evidence-99ac291d5c8f
    source_id: programiz-binary-tree-v2
  - evidence_id: evidence-445127cc9c8d
    source_id: programiz-binary-tree-v2
- claim: 满二叉树（Full）是一种特殊的二叉树：每个父节点/内部节点要么有两个孩子，要么没有孩子。
  claim_id: bintree-full
  support: direct
  supporting_quotes:
  - evidence_id: evidence-c07bf1606108
    exact: |-
      A full Binary tree is a special type of binary tree in which every parent node/internal node has either two or no children.
  targets:
  - evidence_id: evidence-c07bf1606108
    source_id: programiz-binary-tree-v2
- claim: 完美二叉树（Perfect）：每个内部节点恰有两个孩子，且所有叶节点在同一层。
  claim_id: bintree-perfect
  support: direct
  supporting_quotes:
  - evidence_id: evidence-4715bfc4048b
    exact: |-
      A perfect binary tree is a type of binary tree in which every internal node has exactly two child nodes and all the leaf nodes are at the same level.
  targets:
  - evidence_id: evidence-4715bfc4048b
    source_id: programiz-binary-tree-v2
- claim: 完全二叉树（Complete）与满二叉树相似但有两点不同：每一层必须被完全填满；所有叶元素倾向左侧；最后一个叶元素可能没有右兄弟（不必是满二叉树）。
  claim_id: bintree-complete
  support: direct
  supporting_quotes:
  - evidence_id: evidence-10b8acb00371
    exact: |-
      A complete binary tree is just like a full binary tree, but with two major differences
  - evidence_id: evidence-1a26cf6fb16b
    exact: |-
      Every level must be completely filled
  - evidence_id: evidence-4e2930adcd59
    exact: |-
      All the leaf elements must lean towards the left.
  - evidence_id: evidence-696f990f0af4
    exact: |-
      The last leaf element might not have a right sibling i.e. a complete binary tree doesn't have to be a full binary tree.
  targets:
  - evidence_id: evidence-10b8acb00371
    source_id: programiz-binary-tree-v2
  - evidence_id: evidence-1a26cf6fb16b
    source_id: programiz-binary-tree-v2
  - evidence_id: evidence-4e2930adcd59
    source_id: programiz-binary-tree-v2
  - evidence_id: evidence-696f990f0af4
    source_id: programiz-binary-tree-v2
- claim: 退化树/病态树是每个节点只有一个孩子（左或右）的树；歪斜树是被左节点或右节点主导的退化树，分左歪斜与右歪斜两类。
  claim_id: bintree-degenerate
  support: direct
  supporting_quotes:
  - evidence_id: evidence-b0ed47f947f1
    exact: |-
      A degenerate or pathological tree is the tree having a single child either left or right.
  - evidence_id: evidence-4e587942c165
    exact: |-
      A skewed binary tree is a pathological/degenerate tree in which the tree is either dominated by the left nodes or the right nodes.
  targets:
  - evidence_id: evidence-b0ed47f947f1
    source_id: programiz-binary-tree-v2
  - evidence_id: evidence-4e587942c165
    source_id: programiz-binary-tree-v2
- claim: 平衡二叉树：每个节点的左子树与右子树高度差为 0 或 1。
  claim_id: bintree-balanced
  support: direct
  supporting_quotes:
  - evidence_id: evidence-1717ba8ee2fd
    exact: |-
      It is a type of binary tree in which the difference between the height of the left and the right subtree for each node is either 0 or 1.
  targets:
  - evidence_id: evidence-1717ba8ee2fd
    source_id: programiz-binary-tree-v2
- claim: 二叉树的节点用包含一个数据部分和两个指向同类型结构指针的结构体表示。
  claim_id: bintree-repr
  support: direct
  supporting_quotes:
  - evidence_id: evidence-b182c79f5138
    exact: |-
      A node of a binary tree is represented by a structure containing a data part and two pointers to other structures of the same type.
  targets:
  - evidence_id: evidence-b182c79f5138
    source_id: programiz-binary-tree-v2
id: binary-tree
kind: reference
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- programiz-binary-tree-v2
- working-computer-science-binary-tree
status: published
tags:
- data-structure
- tree
- binary-tree
title: 二叉树
updated_at: '2026-09-05'
---
# 二叉树

## 一句话结论

二叉树是**每个节点至多两个孩子**（左孩子、右孩子）的树结构：它把"树"的层级关系压缩到两个指针，既能表示任意层级数据，又派生出 BST/AVL/红黑树/堆等高效变体。按形状约束从松到紧分：满、完美、完全、平衡——这些约束直接决定各变体的性能保证。

## 核心概念

- **节点三要素**：数据项 + 左孩子地址 + 右孩子地址。
- **形状谱系**：退化/歪斜（最坏，退化为链表）→ 完全 → 满 → 完美（最紧）。
- **遍历三序**：前序（根左右）、中序（左根右）、后序（左右根）——递归定义天然适配二叉结构。
- **高度差约束**：平衡二叉树要求每节点左右子树高度差 ≤ 1（AVL 的核心思想来源）。

## 工作机制

### 六种形态

| 类型 | 约束 |
| --- | --- |
| 满（Full） | 每个内部节点要么两个孩子要么没有 |
| 完美（Perfect） | 内部节点恰两个孩子 + 所有叶同层 |
| 完全（Complete） | 每层填满、叶元素靠左；最后一个叶可能没有右兄弟 |
| 退化（Degenerate） | 每个节点只有一个孩子 |
| 歪斜（Skewed） | 左/右节点主导的退化树 |
| 平衡（Balanced） | 每节点左右子树高度差为 0 或 1 |

### 表示

节点用"数据 + 两个指针"的结构体表示：

```c
struct node {
    int data;
    struct node *left;
    struct node *right;
};
```

### 遍历

三种深度优先遍历（递归定义）：

```text
前序 PreOrder:  根 → 左子树 → 右子树
中序 InOrder:   左子树 → 根 → 右子树   （BST 上得到升序序列）
后序 PostOrder: 左子树 → 右子树 → 根
```

## 常见误区

- **"满二叉树 = 完美二叉树"**：中文语境常混用，英文定义上 Perfect 严格于 Full——完美树每层全满，满树只约束"0 或 2 个孩子"。
- **"完全二叉树必须对称"**：不必，完全二叉树只要求逐层从左到右填充（堆的数组表示正依赖此性质）。
- **"退化树还是二叉树"**：是，但性能退化为 O(n) 链表——这正是 BST 需要自平衡（AVL/红黑树）的原因。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| bintree-definition / bintree-repr | programiz-binary-tree-v2 | 定义、节点三要素、结构体表示 |
| bintree-full / bintree-perfect / bintree-complete | programiz-binary-tree-v2 | 满/完美/完全二叉树 |
| bintree-degenerate / bintree-balanced | programiz-binary-tree-v2 | 退化/歪斜/平衡 |

## 待验证项

无。

## 关联知识

- [[binary-search-tree]] —— 有序约束的二叉树，是搜索树的基类概念。
- [[avl-tree]] / [[red-black-tree]] —— 平衡约束的工程实现。
- [[generic-tree]] —— 二叉树是通用树的孩子数受限特例；左孩子/右兄弟表示把通用树转成二叉形态。
- [[data-structure-optimization]] —— 堆（完全二叉树）的数组表示。

## 详细章节

### 定义

二叉树是树数据结构：每个父节点至多两个孩子。每个节点由三部分组成——数据项、左孩子地址、右孩子地址。

### 六种类型

1. **满二叉树（Full）**：每个父节点/内部节点要么有两个孩子，要么没有孩子。
2. **完美二叉树（Perfect）**：每个内部节点恰有两个孩子，所有叶节点在同一层。
3. **完全二叉树（Complete）**：类似满二叉树但有两点差异——每层必须完全填满；所有叶元素倾向左侧。最后一个叶元素可能没有右兄弟，即完全二叉树不必是满二叉树。
4. **退化树（Degenerate/Pathological）**：每个节点只有一个孩子（左或右）。
5. **歪斜树（Skewed）**：被左节点或右节点主导的退化树，分左歪斜与右歪斜。
6. **平衡二叉树（Balanced）**：每个节点左右子树高度差为 0 或 1。

### 应用场景

- 表达式树（编译器语法树）。
- 堆：用数组表示的完全二叉树，支撑优先队列。
- 搜索与排序：BST 及其自平衡变体（见 [[binary-search-tree]]、[[avl-tree]]）。
- 哈夫曼编码树（压缩）。

## 参考

- https://www.programiz.com/dsa/binary-tree
