---
aliases:
- Binary Search Tree
- BST
- 二叉查找树
- 排序二叉树
confidentiality: public
domain: computer-science
evidence:
- claim: 二叉搜索树（BST，又称有序/排序二叉树）是一种有根二叉树：每个内部节点的键大于其左子树中的所有键、小于其右子树中的所有键；BST 上操作的时间复杂度与树高成线性关系。
  claim_id: bst-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-6c9f3729e870
    exact: |-
      Binary search tree, also called an ordered or sorted binary tree, is a rooted binary tree data structure with the key of each internal node being greater than all the keys in the respective node's left subtree and less than the ones in its right subtree.
  - evidence_id: evidence-25a94489f8e2
    exact: |-
      The time complexity of operations on the binary search tree is linear with respect to the height of the tree.
  targets:
  - evidence_id: evidence-6c9f3729e870
    source_id: wiki-binary-search-tree
  - evidence_id: evidence-25a94489f8e2
    source_id: wiki-binary-search-tree
- claim: BST 支持以二分查找方式快速查找、添加和删除数据项；由于每次比较都跳过剩余树的大约一半，查找性能正比于二分对数。
  claim_id: bst-binary-search
  support: direct
  supporting_quotes:
  - evidence_id: evidence-8fd0ef8100e7
    exact: |-
      Binary search trees allow binary search for fast lookup, addition, and removal of data items. Since the nodes in a BST are laid out so that each comparison skips about half of the remaining tree, the lookup performance is proportional to that of binary logarithm.
  targets:
  - evidence_id: evidence-8fd0ef8100e7
    source_id: wiki-binary-search-tree
- claim: BST 是 1960 年代为高效存储带标签数据的问题设计的，归于 Conway Berners-Lee 与 David
    Wheeler 名下。
  claim_id: bst-history
  support: direct
  supporting_quotes:
  - evidence_id: evidence-3aa8c8e52e3e
    exact: |-
      BSTs were devised in the 1960s for the problem of efficient storage of labeled data and are attributed to Conway Berners-Lee and David Wheeler.
  targets:
  - evidence_id: evidence-3aa8c8e52e3e
    source_id: wiki-binary-search-tree
- claim: BST 的性能依赖节点插入顺序，任意插入可能导致退化；最坏情况下连续操作会使 BST 退化为单链表状（不平衡树）结构，最坏复杂度与链表相同；若干 BST 变体可以提供有保证的最坏情况性能。
  claim_id: bst-degeneracy
  support: direct
  supporting_quotes:
  - evidence_id: evidence-30007c0cb00e
    exact: |-
      The performance of a binary search tree is dependent on the order of insertion of the nodes into the tree since arbitrary insertions may lead to degeneracy; several variations of the binary search tree can be built with guaranteed worst-case performance.
  - evidence_id: evidence-54af1c56b7d6
    exact: |-
      In worst case, successive operations in the binary search tree may lead to degeneracy and form a singly linked list (or "unbalanced tree") like structure, thus has the same worst-case complexity as a linked list.
  targets:
  - evidence_id: evidence-30007c0cb00e
    source_id: wiki-binary-search-tree
  - evidence_id: evidence-54af1c56b7d6
    source_id: wiki-binary-search-tree
- claim: BST 也是构造 set、multiset、关联数组等抽象数据结构的基础数据结构。
  claim_id: bst-abstract-ds
  support: direct
  supporting_quotes:
  - evidence_id: evidence-d5faef464cb6
    exact: |-
      Binary search trees are also a fundamental data structure used in construction of abstract data structures such as sets, multisets, and associative arrays.
  targets:
  - evidence_id: evidence-d5faef464cb6
    source_id: wiki-binary-search-tree
- claim: 删除只有一个孩子的节点：修改 Z 的父节点使其指向该孩子节点，孩子随之顶替 Z 在树中的位置。
  claim_id: bst-delete-one-child
  support: direct
  supporting_quotes:
  - evidence_id: evidence-af0e76f257a0
    exact: |-
      If Z has only one child, the child node of Z gets elevated by modifying the parent node of Z to point to the child node, consequently taking Z's position in the tree, as shown in (b) and (c).
  targets:
  - evidence_id: evidence-af0e76f257a0
    source_id: wiki-binary-search-tree
- claim: 删除有两个孩子的节点：用 Z 的中序后继 Y 顶替 Z。若 Y 是 Z 的右孩子，Y 顶替 Z 且 Y
    的右孩子保持不变；若 Y 在 Z 的右子树内但不是右孩子，Y 先被自己的右孩子替换，然后再顶替 Z
    的位置；也可以改用中序前驱。
  claim_id: bst-delete-two-children
  support: direct
  supporting_quotes:
  - evidence_id: evidence-ff0802491fcb
    exact: |-
      If Z has both left and right children, the in-order successor of Z, say Y, displaces Z by following the two cases:
  - evidence_id: evidence-2b52cbf6cd14
    exact: |-
      If Y is Z's right child, Y displaces Z and Y's right child remain unchanged.
  - evidence_id: evidence-c6bb2944b119
    exact: |-
      If Y lies within Z's right subtree but is not Z's right child, Y first gets replaced by its own right child, and then it displaces Z's position in the tree.
  - evidence_id: evidence-aadcbd15a301
    exact: |-
      Alternatively, the in-order predecessor can also be used.
  targets:
  - evidence_id: evidence-ff0802491fcb
    source_id: wiki-binary-search-tree
  - evidence_id: evidence-2b52cbf6cd14
    source_id: wiki-binary-search-tree
  - evidence_id: evidence-c6bb2944b119
    source_id: wiki-binary-search-tree
  - evidence_id: evidence-aadcbd15a301
    source_id: wiki-binary-search-tree
- claim: BST 的三种遍历：中序遍历先访问左子树、再根、后右子树，按非降键序访问所有节点；前序遍历先访问根；后序遍历最后访问根。
  claim_id: bst-traversal
  support: direct
  supporting_quotes:
  - evidence_id: evidence-b2b0afcf337e
    exact: |-
      Inorder tree walk: Nodes from the left subtree get visited first, followed by the root node and right subtree. Such a traversal visits all the nodes in the order of non-decreasing key sequence.
  - evidence_id: evidence-c1634aa0ad23
    exact: |-
      Preorder tree walk: The root node gets visited first, followed by left and right subtrees.
  - evidence_id: evidence-8d3abacce66c
    exact: |-
      Postorder tree walk: Nodes from the left subtree get visited first, followed by the right subtree, and finally, the root.
  targets:
  - evidence_id: evidence-b2b0afcf337e
    source_id: wiki-binary-search-tree
  - evidence_id: evidence-c1634aa0ad23
    source_id: wiki-binary-search-tree
  - evidence_id: evidence-8d3abacce66c
    source_id: wiki-binary-search-tree
- claim: 自平衡二叉搜索树有多种，包括 T-tree、treap、红黑树、B 树、2–3 树与伸展树。
  claim_id: bst-balanced-types
  support: direct
  supporting_quotes:
  - evidence_id: evidence-109717c4bbe1
    exact: |-
      There are several self-balanced binary search trees, including T-tree, treap, red-black tree, B-tree, 2–3 tree, and Splay tree.
  targets:
  - evidence_id: evidence-109717c4bbe1
    source_id: wiki-binary-search-tree
- claim: BST 用于 tree sort 等排序算法（所有元素一次插入后按中序遍历），也用于 quicksort；还用节点的键作为优先级来实现优先队列。
  claim_id: bst-applications
  support: direct
  supporting_quotes:
  - evidence_id: evidence-1a2ba9876653
    exact: |-
      Binary search trees are used in sorting algorithms such as tree sort, where all the elements are inserted at once and the tree is traversed at an in-order fashion. BSTs are also used in quicksort.
  - evidence_id: evidence-4e4f979c165d
    exact: |-
      Binary search trees are used in implementing priority queues, using the node's key as priorities.
  targets:
  - evidence_id: evidence-1a2ba9876653
    source_id: wiki-binary-search-tree
  - evidence_id: evidence-4e4f979c165d
    source_id: wiki-binary-search-tree
id: binary-search-tree
kind: reference
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- wiki-binary-search-tree
- web-computer-science-binary-search-tree
- working-computer-science-binary-search-tree
status: published
tags:
- data-structure
- tree
- binary-search-tree
title: 二叉搜索树
updated_at: '2026-09-05'
---
# 二叉搜索树

## 一句话结论

二叉搜索树（BST）是一种**有序二叉树**：每个内部节点的键大于左子树所有键、小于右子树所有键。这条不变量让每次比较都能排除一半搜索空间，查找/插入/删除平均 Θ(log n)；但**性能依赖插入顺序**——有序插入会退化为链表（最坏 O(n)），因此工程上几乎都用它的自平衡变体（AVL、红黑树）。

## 核心概念

- **BST 不变量**：left < node < right（对整棵子树成立，不只是直接孩子）。
- **中序遍历 = 升序**：BST 最优雅的性质，tree sort 的原理。
- **退化问题**：插入顺序决定树形；退化后等价单链表。
- **自平衡家族**：AVL、红黑树、treap、伸展树、B 树等都是"加了平衡约束的 BST"。

## 工作机制

### 查找

从根开始：目标键等于当前键则命中；小于走左、大于走右；到达空引用则查找失败。每次比较跳过约一半剩余树。

### 插入

按查找路径下行，把新键挂到失败的空位上（总是作为叶插入），树形由插入顺序唯一决定。

### 删除（三情况）

| 情形 | 处理 |
| --- | --- |
| 叶节点 | 直接移除 |
| 只有一个孩子 | 修改 Z 的父节点指向该孩子，孩子顶替 Z 的位置 |
| 有两个孩子 | 用**中序后继** Y 顶替 Z：Y 是 Z 右孩子时直接顶替（Y 右孩子不变）；Y 在右子树更深处时先被自己的右孩子替换、再顶替 Z；也可改用中序前驱 |

### 复杂度

| 操作 | 平均 | 最坏 |
| --- | --- | --- |
| 查找 | Θ(log n) | O(n) |
| 插入 | Θ(log n) | O(n) |
| 删除 | Θ(log n) | O(n) |
| 空间 | Θ(n) | O(n) |

## 常见误区

- **"BST 有序性只看父子"**：不是——不变量要求整个左子树全部小于节点、整个右子树全部大于节点；只比直接孩子是常见 bug。
- **"BST 永远 O(log n)"**：平均才是 log n；顺序插入退化为 O(n) 链表。
- **"删除双孩子节点要重构子树"**：只需用中序前驱/后继的键替换，不需要旋转重构。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| bst-definition / bst-binary-search / bst-history | wiki-binary-search-tree（Wikipedia） | 定义不变量、二分性质、1960s 起源 |
| bst-degeneracy / bst-complexity | wiki-binary-search-tree | 插入顺序依赖与退化 |
| bst-delete-one-child / bst-delete-two-children / bst-traversal | wiki-binary-search-tree | 删除三情况与三序遍历 |
| bst-abstract-ds / bst-balanced-types / bst-applications | wiki-binary-search-tree | set/关联数组基础、自平衡家族、排序与优先队列 |

## 待验证项

无。

## 关联知识

- [[binary-tree]] —— BST 的基类结构：无平衡约束的形态。
- [[avl-tree]] —— 高度差 ≤ 1 的严格自平衡 BST，查找更快。
- [[red-black-tree]] —— 工程中最常用的自平衡 BST（map/set 底层）。
- [[b-tree]] —— BST 的多路推广，面向磁盘。

## 详细章节

### 定义与历史

BST 又称有序或排序二叉树：有根二叉树，每个内部节点的键大于其左子树所有键、小于其右子树所有键；操作时间复杂度与树高线性相关。它由 Conway Berners-Lee 与 David Wheeler 在 1960 年代为高效存储带标签数据的问题设计。

### 作为抽象数据结构的基座

BST 是构造 set、multiset、关联数组（映射）等抽象数据结构的基础数据结构。

### 应用

- **排序**：tree sort——所有元素一次插入，再中序遍历得到有序序列；BST 思想也用于 quicksort。
- **优先队列**：以节点键为优先级实现；入队用常规 BST 插入，出队按优先队列类型取最小/最大键。
- **关联容器**：C++ map/set、Java TreeMap 的底层（自平衡变体）。

## 参考

- https://en.wikipedia.org/wiki/Binary_search_tree
- https://www.geeksforgeeks.org/dsa/binary-search-tree-data-structure/
