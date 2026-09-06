---
aliases:
- Red-Black Tree
- RBT
confidentiality: public
domain: computer-science
evidence:
- claim: 红黑树是一种自平衡二叉搜索树，高度上限为 O(logN)，查找、插入、删除都能在 O(logN)
    时间内高效完成；而普通二叉搜索树最坏可能退化到 O(N)。
  claim_id: rb-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-fe34e8b4d9cb
    exact: |-
      A Red-Black Tree is a self-balancing binary search tree with a height limit of O(logN), enabling efficient search, insertion, and deletion operations in O(logN) time, unlike standard binary search trees which can take O(N) time.
  targets:
  - evidence_id: evidence-fe34e8b4d9cb
    source_id: web-computer-science-red-black-tree
- claim: 红黑树有五条性质：每个节点非红即黑；根节点恒为黑色；红节点不能有红子节点（红节点不能相邻）；从任一节点到其后代叶子的每条路径必须含相同数量的黑节点；所有叶子（NIL 节点）都是黑色。
  claim_id: rb-properties
  support: direct
  supporting_quotes:
  - evidence_id: evidence-70d3bddd4fb5
    exact: |-
      Node Color: Each node is either red or black.
  - evidence_id: evidence-0d5d6b70154b
    exact: |-
      Root Property: The root of the tree is always black.
  - evidence_id: evidence-96b26ae2b99c
    exact: |-
      Red Node Property: Red nodes cannot have red children (Red nodes cannot be adjacent).
  - evidence_id: evidence-0cb659e294c6
    exact: |-
      Black Node Property: Every path from a node to its descendant leaves must have the same number of black nodes.
  - evidence_id: evidence-53b7c761e0ab
    exact: |-
      Leaf Property: All leaves (NIL nodes) are black.
  targets:
  - evidence_id: evidence-70d3bddd4fb5
    source_id: web-computer-science-red-black-tree
  - evidence_id: evidence-0d5d6b70154b
    source_id: web-computer-science-red-black-tree
  - evidence_id: evidence-96b26ae2b99c
    source_id: web-computer-science-red-black-tree
  - evidence_id: evidence-0cb659e294c6
    source_id: web-computer-science-red-black-tree
  - evidence_id: evidence-53b7c761e0ab
    source_id: web-computer-science-red-black-tree
- claim: 这些性质（无连续红节点、黑高相同）保证红黑树最长路径不超过最短路径的两倍，从而维持树的平衡与高效性能。
  claim_id: rb-height-guarantee
  support: direct
  supporting_quotes:
  - evidence_id: evidence-9ab60d16945e
    exact: |-
      These properties (no two consecutive reds and same black height) ensure that the longest path from the root to any leaf is no more than twice as long as the shortest path, maintaining the tree's balance and efficient performance.
  targets:
  - evidence_id: evidence-9ab60d16945e
    source_id: web-computer-science-red-black-tree
- claim: 红黑树插入新节点分两步：先按 BST 规则插入，再修复红黑性质违规。
  claim_id: rb-insertion
  support: direct
  supporting_quotes:
  - evidence_id: evidence-6acfc182afc6
    exact: |-
      Insertion: Inserting a new node involves a two-step process: BST insertion, followed by fixing Red-Black property violations.
  targets:
  - evidence_id: evidence-6acfc182afc6
    source_id: web-computer-science-red-black-tree
- claim: 插入修复情形一（叔节点为红）：把父节点与叔节点改黑、祖父节点改红，然后向上继续修复。
  claim_id: rb-insert-case1
  support: direct
  supporting_quotes:
  - evidence_id: evidence-cbddd783092e
    exact: |-
      Case 1 (Uncle is Red): Recolor parent and uncle to black, grandparent to red. Then, move up the tree.
  targets:
  - evidence_id: evidence-cbddd783092e
    source_id: web-computer-science-red-black-tree
- claim: 插入修复情形二（叔节点为黑）：若新节点是右孩子，先对父节点做左旋；若是左孩子，对祖父节点做右旋并重新着色。
  claim_id: rb-insert-case2
  support: direct
  supporting_quotes:
  - evidence_id: evidence-60331b073563
    exact: |-
      Case 2 (Uncle is Black): If node is a right child, perform a left rotation on the parent. If the node is a left child, perform a right rotation on the grandparent and recolor.
  targets:
  - evidence_id: evidence-60331b073563
    source_id: web-computer-science-red-black-tree
- claim: 红黑树的查找与普通 BST 的查找方式相同。
  claim_id: rb-search
  support: direct
  supporting_quotes:
  - evidence_id: evidence-c83b40239805
    exact: |-
      Searching: Searching in Red-Black Trees mirrors BST searching.
  targets:
  - evidence_id: evidence-c83b40239805
    source_id: web-computer-science-red-black-tree
- claim: 红黑树删除按标准 BST 规则移除节点；若删除的是黑节点，可能出现 "double black" 状态，需要专门修复。
  claim_id: rb-deletion
  support: direct
  supporting_quotes:
  - evidence_id: evidence-6724bb114559
    exact: |-
      Remove the node using standard BST rules.
  - evidence_id: evidence-0c72d8fee0ea
    exact: |-
      If a black node is deleted, a "double black" condition might arise, which requires specific fixes.
  targets:
  - evidence_id: evidence-6724bb114559
    source_id: web-computer-science-red-black-tree
  - evidence_id: evidence-0c72d8fee0ea
    source_id: web-computer-science-red-black-tree
- claim: 左旋是在节点 x 处向左转动树，把它的右孩子 y 提升到 x 原来的位置。
  claim_id: rb-rotation-left
  support: direct
  supporting_quotes:
  - evidence_id: evidence-61a045cc5983
    exact: |-
      Left Rotation: A left rotation at node x pivots the tree to the left, promoting its right child y to x's former position.
  targets:
  - evidence_id: evidence-61a045cc5983
    source_id: web-computer-science-red-black-tree
- claim: 右旋是在节点 x 处向右转动树，把它的左孩子 y 提升到 x 原来的位置。
  claim_id: rb-rotation-right
  support: direct
  supporting_quotes:
  - evidence_id: evidence-d9751cdd107c
    exact: |-
      Right Rotation: A right rotation at node x pivots the tree to the right, promoting its left child y to x’s former position.
  targets:
  - evidence_id: evidence-d9751cdd107c
    source_id: web-computer-science-red-black-tree
- claim: 红黑树因自平衡而在查找、插入、删除上有最坏 O(log n) 的高效率；插入、删除与平衡规则直观，相对容易实现；适合实现 map、set 与优先队列。
  claim_id: rb-advantages
  support: direct
  supporting_quotes:
  - evidence_id: evidence-46854131a1bf
    exact: |-
      Because of their self-balancing property, they offer high efficiency in searching, insertion, and deletion, with a worst-case time complexity of O(log n).
  - evidence_id: evidence-adb4ade9ca09
    exact: |-
      Red-Black Trees have straightforward rules for insertion, deletion, and balance, making them relatively easy to implement.
  - evidence_id: evidence-0420728272cc
    exact: |-
      Suitable for use in maps, sets, and priority queues.
  targets:
  - evidence_id: evidence-46854131a1bf
    source_id: web-computer-science-red-black-tree
  - evidence_id: evidence-adb4ade9ca09
    source_id: web-computer-science-red-black-tree
  - evidence_id: evidence-0420728272cc
    source_id: web-computer-science-red-black-tree
- claim: 与 AVL 树等更简单的平衡树相比，红黑树的插入与删除规则更复杂；维护红黑性质在插入/删除操作中带来少量额外开销。
  claim_id: rb-disadvantages
  support: direct
  supporting_quotes:
  - evidence_id: evidence-8c7950f5de01
    exact: |-
      Red-Black Trees have more intricate insertion and deletion rules compared to simpler balanced trees like AVL trees.
  - evidence_id: evidence-f63611b667a8
    exact: |-
      Maintaining the Red-Black Tree properties introduces a minor overhead during insertion and deletion operations.
  targets:
  - evidence_id: evidence-8c7950f5de01
    source_id: web-computer-science-red-black-tree
  - evidence_id: evidence-f63611b667a8
    source_id: web-computer-science-red-black-tree
- claim: 红黑树支撑 C++ 的 map/set 与 Java 的 TreeMap 等高性能容器；在操作系统中支撑高效进程调度（如 Linux CFS）与虚拟内存映射；在 XFS、Ext4 等文件系统中组织目录结构并跟踪磁盘块。
  claim_id: rb-applications
  support: direct
  supporting_quotes:
  - evidence_id: evidence-f5427bc1aaa0
    exact: |-
      Powers high-performance containers such as map and set in C++ and TreeMap in Java.
  - evidence_id: evidence-f362a701ea73
    exact: |-
      In operating systems, it enables efficient process scheduling (e.g., Linux CFS) and virtual memory mapping.
  - evidence_id: evidence-4bfb3ccb8bd6
    exact: |-
      It organizes directory structures and tracks disk blocks in file systems like XFS and Ext4.
  targets:
  - evidence_id: evidence-f5427bc1aaa0
    source_id: web-computer-science-red-black-tree
  - evidence_id: evidence-f362a701ea73
    source_id: web-computer-science-red-black-tree
  - evidence_id: evidence-4bfb3ccb8bd6
    source_id: web-computer-science-red-black-tree
id: red-black-tree
kind: reference
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-red-black-tree
- working-computer-science-red-black-tree
status: published
tags:
- data-structure
- tree
- self-balancing
- binary-search-tree
title: 红黑树
updated_at: '2026-09-05'
---
# 红黑树

## 一句话结论

红黑树是一种**自平衡二叉搜索树**：每个节点多存一位颜色（红/黑），靠五条性质（根黑、红不相邻、黑高一致、NIL 黑）把最长路径压到最短路径的两倍以内，使查找、插入、删除在最坏情况下也是 O(log n)。相比 AVL 树平衡更宽松、旋转更少，是 C++ `std::map`/`std::set`、Java `TreeMap`、Linux CFS 的底层结构。

## 核心概念

- **颜色位**：每个节点附加红/黑一位属性，插入与删除时用它维持平衡。
- **五条性质**：节点非红即黑；根恒黑；红节点不能相邻；任一节点到其后代叶子的每条路径黑节点数相同；叶子（NIL）全黑。
- **高度保证**：最长路径 ≤ 2 × 最短路径 ⇒ 树高 ≤ 2·log(N+1)，基本操作最坏 O(log n)。
- **双黑（double black）**：删除黑节点后出现的"亏一个黑"状态，删除修复的核心难点。

## 工作机制

### 查找

与普通 BST 完全相同：从根开始，等于命中、小于走左、大于走右，直到命中或到达 NIL。

### 插入

1. 按 BST 规则插入；新节点**初始染红**（不破坏黑高，只可能违反"红不相邻"）。
2. 若父节点为黑，无需修复；若父为红，按叔节点颜色修复：
   - **叔为红**：父、叔改黑，祖父改红，问题上移两层继续。
   - **叔为黑**：先按新节点是内/外孩子旋转一次（右孩子→对父左旋；左孩子→对祖父右旋），再重新着色收尾。

### 删除

1. 按标准 BST 规则移除节点。
2. 若移除的是黑节点，路径上"亏一个黑"，产生 **double black**；按兄弟颜色与兄弟孩子颜色分类：兄红→旋转+重着色后转为兄黑情形；兄黑且无红侄→把黑推给父节点向上传播；兄有红侄→按远/近红侄旋转修复。

### 旋转

- **左旋**：在 x 处左旋，右孩子 y 上提到 x 的原位；y 的左子树转交给 x 作右子树。
- **右旋**：在 x 处右旋，左孩子 y 上提到 x 的原位；y 的右子树转交给 x 作左子树。
- 旋转保持 BST 有序性与红黑性质，是最长/最短路径比 ≤ 2 的维护手段。

## 示例或代码

复杂度（n 为节点数）：

| 操作 | 平均 | 最坏 |
| --- | --- | --- |
| 查找 | O(log n) | O(log n) |
| 插入 | O(log n) | O(log n) |
| 删除 | O(log n) | O(log n) |

快速验证性质的反例：3 个节点连成一条链（任意染色）必违反红黑性质——说明纯链式退化在红黑树中不存在。

## 常见误区

- **"红黑树完全平衡"**：不是，它只保证最长路径 ≤ 2× 最短路径；AVL 才是严格高度差 ≤ 1。
- **"插入的新节点是黑色"**：新节点初始为红，染黑反而会破坏黑高一致。
- **"删除和插入一样简单"**：删除要处理 double black 状态，情形比插入多得多。
- **"红黑树比 AVL 全面更优"**：红黑树旋转次数上限更低、写放大更小；AVL 更严格平衡、查找更快。写密集选红黑树，查找密集选 AVL。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| rb-definition / rb-height-guarantee | web-computer-science-red-black-tree | 定义、O(logN)、最长 ≤ 2× 最短 |
| rb-properties | web-computer-science-red-black-tree | 五条红黑性质 |
| rb-insertion / rb-insert-case1 / rb-insert-case2 / rb-search / rb-deletion | web-computer-science-red-black-tree | 两步插入、叔红/叔黑修复、查找同 BST、双黑 |
| rb-rotation-left / rb-rotation-right | web-computer-science-red-black-tree | 左旋/右旋定义 |
| rb-advantages / rb-disadvantages / rb-applications | web-computer-science-red-black-tree | 优劣与工程应用（map/set/TreeMap/CFS/XFS） |

## 待验证项

- 删除修复"兄黑有红侄"的远/近孩子细分原文较简略，逐情形图示待补。
- 高度上界 h ≤ 2·log(N+1) 的推导在源中仅给结论，未收录证明。

## 关联知识

- [[binary-search-tree]] —— 红黑树是 BST 加颜色的自平衡变体，查找逻辑不变。
- [[avl-tree]] —— 另一自平衡 BST：AVL 更严格平衡、查找更快；红黑树写放大更小。
- [[binary-tree]] —— 树的基础概念（高度、遍历）。
- [[data-structure-optimization]] —— 有序映射场景选型（红黑树 vs 跳表 vs B 树）。

## 详细章节

### 定义

红黑树是自平衡二叉搜索树，高度上限 O(logN)，查找、插入、删除均为 O(logN)；区别于普通 BST 最坏 O(N) 的退化。每个节点额外存储一位颜色属性，红/黑两色在插入与删除时用于维持平衡。

### 五条性质

1. **节点颜色**：每个节点是红色或黑色。
2. **根性质**：根总是黑色。
3. **红节点性质**：红节点不能有红孩子（红不相邻）。
4. **黑节点性质**：从任一节点到其后代叶子的每条路径黑节点数相同。
5. **叶子性质**：所有叶子（NIL 哨兵）都是黑色。

推论：根到叶黑节点数（黑高）≥ 树高的一半；N 个节点的红黑树高 h ≤ 2·log(N+1)。

### 应用

- C++ `map`/`set`、Java `TreeMap`/`TreeSet` 等高性能有序容器。
- 操作系统：Linux CFS 进程调度、虚拟内存区域管理。
- 文件系统：XFS、Ext4 的目录结构与磁盘块跟踪。
- 网络路由的高速包过滤与路由表查找；键值存储的内存索引。

## 参考

- https://www.geeksforgeeks.org/dsa/introduction-to-red-black-tree/
- [[avl-tree]] —— 与红黑树的对照见该页"与红黑树比较"一节。
