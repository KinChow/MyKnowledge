---
aliases:
- AVL Tree
- Adelson-Velsky and Landis Tree
- 平衡二叉搜索树
confidentiality: public
domain: computer-science
evidence:
- claim: AVL 树是一种自平衡二叉搜索树，任意节点的两棵子树高度差不超过 1；一旦超过 1，就通过再平衡恢复该性质。
  claim_id: avl-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-0e522fe6aa29
    exact: In an AVL tree, the heights of the two child subtrees of any node differ
      by not more than one; if at any time they differ by more than one, rebalancing
      is done to restore this property.
  targets:
  - evidence_id: evidence-0e522fe6aa29
    source_id: wiki-avl-tree
- claim: AVL 树的查找、插入和删除在平均与最坏情况下均为 O(log n)，其中 n 是操作前树中的节点数。
  claim_id: avl-operation-complexity
  support: direct
  supporting_quotes:
  - evidence_id: evidence-6487166eddd5
    exact: Lookup, insertion, and deletion all take O(log n) time in both the average
      and worst cases, where n is the number of nodes in the tree prior to the operation.
  targets:
  - evidence_id: evidence-6487166eddd5
    source_id: wiki-avl-tree
- claim: AVL 树以两位苏联发明者 Georgy Adelson-Velsky 和 Evgenii Landis 命名，他们在 1962 年的论文
    "An algorithm for the organization of information" 中发表该结构；它是最早被发明的自平衡二叉搜索树数据结构。
  claim_id: avl-history
  support: direct
  supporting_quotes:
  - evidence_id: evidence-6d8546da2df8
    exact: 'The AVL tree is named after its two Soviet inventors, Georgy Adelson-Velsky
      and Evgenii Landis, who published it in their 1962 paper "An algorithm for the
      organization of information". It is the first self-balancing binary search tree
      data structure to be invented.'
  targets:
  - evidence_id: evidence-6d8546da2df8
    source_id: wiki-avl-tree
- claim: AVL 树节点的平衡因子是该节点左子树高度与右子树高度之差。
  claim_id: avl-balance-factor
  support: direct
  supporting_quotes:
  - evidence_id: evidence-6e44ce038439
    exact: Balance factor of a node in an AVL tree is the difference between the height
      of the left subtree and that of the right subtree of that node.
  targets:
  - evidence_id: evidence-6e44ce038439
    source_id: programiz-avl-tree-v2
- claim: AVL 树的自平衡性质由平衡因子维护，平衡因子的取值必须始终为 -1、0 或 +1。
  claim_id: avl-balance-invariant
  support: direct
  supporting_quotes:
  - evidence_id: evidence-74bd0caab81a
    exact: The self balancing property of an avl tree is maintained by the balance
      factor. The value of balance factor should always be -1, 0 or +1.
  targets:
  - evidence_id: evidence-74bd0caab81a
    source_id: programiz-avl-tree-v2
- claim: 旋转操作交换子树中节点的位置。
  claim_id: avl-rotation
  support: direct
  supporting_quotes:
  - evidence_id: evidence-83331771a789
    exact: In rotation operation, the positions of the nodes of a subtree are interchanged.
  targets:
  - evidence_id: evidence-83331771a789
    source_id: programiz-avl-tree-v2
- claim: AVL 失衡的四种情形及其旋转为：Right Right 用单旋 rotate_Left；Left Left 用单旋 rotate_Right（镜像）；Right
    Left 用双旋 rotate_RightLeft；Left Right 用双旋 rotate_LeftRight（镜像）。
  claim_id: avl-four-cases
  support: direct
  supporting_quotes:
  - evidence_id: evidence-fb396c902653
    exact: |-
      Right Right: X is rebalanced with a simple rotation rotate_Left. Left Left: X is rebalanced with a simple rotation rotate_Right (mirror-image). Right Left: X is rebalanced with a double rotation rotate_RightLeft. Left Right: X is rebalanced with a double rotation rotate_LeftRight (mirror-image).
  targets:
  - evidence_id: evidence-fb396c902653
    source_id: wiki-avl-tree
- claim: 删除操作中，单次删除使 AVL 子树高度至多下降 1，节点临时平衡因子范围是 -2 到 +2；保持在 -1 到 +1 内可按 AVL
    规则调整，变为 ±2 则子树失衡、需要旋转。
  claim_id: avl-delete-rebalance
  support: direct
  supporting_quotes:
  - evidence_id: evidence-ed8598496e30
    exact: Since with a single deletion the height of an AVL subtree cannot decrease
      by more than one, the temporary balance factor of a node will be in the range
      from −2 to +2. If the balance factor remains in the range from −1 to +1 it can
      be adjusted in accord with the AVL rules. If it becomes ±2 then the subtree
      is unbalanced and needs to be rotated.
  targets:
  - evidence_id: evidence-ed8598496e30
    source_id: wiki-avl-tree
- claim: AVL 插入需要 0 到 3 次尾递归旋转、摊还 O(1) 时间；AVL 删除最坏需要 O(log n) 次旋转、平均 O(1)。
  claim_id: avl-rotation-cost
  support: direct
  supporting_quotes:
  - evidence_id: evidence-804dc90717c9
    exact: RB insertions and deletions and AVL insertions require from zero to three
      tail-recursive rotations and run in amortized O(1) time, thus equally constant
      on average. AVL deletions requiring O(log n) rotations in the worst case are
      also O(1) on average.
  targets:
  - evidence_id: evidence-804dc90717c9
    source_id: wiki-avl-tree
- claim: AVL 树常与红黑树比较：两者支持相同的操作集合、基本操作同为 O(log n)；在查找密集型应用中 AVL 树更快，因为它平衡得更严格。
  claim_id: avl-vs-red-black
  support: direct
  supporting_quotes:
  - evidence_id: evidence-b33ffb170466
    exact: AVL trees are often compared with red–black trees because both support
      the same set of operations and take O(log n) time for the basic operations.
      For lookup-intensive applications, AVL trees are faster than red–black trees
      because they are more strictly balanced.
  targets:
  - evidence_id: evidence-b33ffb170466
    source_id: wiki-avl-tree
- claim: 每个 AVL 树都可以染成红黑树，但存在不是 AVL 平衡的红黑树。
  claim_id: avl-rb-math
  support: direct
  supporting_quotes:
  - evidence_id: evidence-3529b2a123b1
    exact: Indeed, every AVL tree can be colored red–black, but there are RB trees
      which are not AVL balanced.
  targets:
  - evidence_id: evidence-3529b2a123b1
    source_id: wiki-avl-tree
- claim: AVL 树可用于数据库中大记录的索引和大型数据库中的检索。
  claim_id: avl-app-database
  support: direct
  supporting_quotes:
  - evidence_id: evidence-e31977e17e30
    exact: For indexing large records in databases
  - evidence_id: evidence-9a0d9ef9c838
    exact: For searching in large databases
  targets:
  - evidence_id: evidence-e31977e17e30
    source_id: programiz-avl-tree-v2
  - evidence_id: evidence-9a0d9ef9c838
    source_id: programiz-avl-tree-v2
id: avl-tree
kind: reference
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- wiki-avl-tree
- programiz-avl-tree-v2
- working-computer-science-avl-tree
status: published
tags:
- data-structure
- tree
- self-balancing
- binary-search-tree
title: AVL 树
updated_at: '2026-09-05'
---
# AVL 树

## 一句话结论

AVL 树是最早被发明的自平衡二叉搜索树（Adelson-Velsky 与 Landis，1962）：每个节点维护**平衡因子**（左子树高度 − 右子树高度），其值恒为 -1、0 或 +1；失衡时通过**旋转**恢复平衡，使查找、插入、删除在平均与最坏情况下都是 O(log n)。相比红黑树，AVL 平衡更严格、查找更快，适合查找密集型场景。

## 核心概念

- **平衡因子（Balance Factor）**：节点左子树高度与右子树高度之差，必须始终为 -1、0 或 +1；自平衡性质由它维护。
- **旋转（Rotation）**：交换子树中节点位置的操作，是恢复平衡的唯一手段；分单旋（左旋/右旋）与双旋（左右旋/右左旋）。
- **高度保证**：任意节点两棵子树高度差 ≤ 1，因此树高为 O(log n)，所有基本操作 O(log n)。
- **历史地位**：1962 年由 Adelson-Velsky 与 Landis 在论文 "An algorithm for the organization of information" 中提出，是最早的自平衡二叉搜索树。

## 工作机制

### 插入

1. 按 BST 规则将新节点作为叶节点插入。
2. 回溯（retracing）路径上的祖先节点，更新平衡因子。
3. 若某祖先平衡因子达到 ±2，按失衡情形旋转：
   - **Right Right** → 单旋 `rotate_Left`
   - **Left Left** → 单旋 `rotate_Right`
   - **Right Left** → 双旋 `rotate_RightLeft`
   - **Left Right** → 双旋 `rotate_LeftRight`
4. 旋转后子树高度恢复，回溯停止。插入共需 0~3 次尾递归旋转，摊还 O(1)。

### 删除

1. 按 BST 规则删除节点。
2. 回溯更新平衡因子：单次删除使子树高度至多下降 1，临时平衡因子范围为 -2..+2；变为 ±2 则旋转。
3. 与插入不同，旋转后子树高度可能下降（BF(Z) ≠ 0 的情形），失衡可能向上传播到根，最坏需 O(log n) 次旋转（平均 O(1)）。

## 示例或代码

复杂度（n 为节点数）：

| 操作 | 平均 | 最坏 |
| --- | --- | --- |
| 空间 | O(n) | O(n) |
| 查找 | O(log n) | O(log n) |
| 插入 | O(log n) | O(log n) |
| 删除 | O(log n) | O(log n) |

旋转成本：插入 0~3 次尾递归旋转（摊还 O(1)）；删除最坏 O(log n) 次（平均 O(1)）。

## 常见误区

- **"AVL 每次插入都要旋转"**：插入摊还 O(1) 次旋转（0~3 次封顶），多数插入不触发旋转，只更新平衡因子。
- **"AVL 全面优于红黑树"**：AVL 更严格平衡带来更快查找，但删除最坏需 O(log n) 次旋转；写密集/删除密集场景红黑树（如 Linux 内核、C++ std::map）更常用。
- **"平衡因子是右减左"**：方向是约定问题（左减右或右减左均可），关键是整棵树统一，本文采用左减右。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| avl-definition / avl-operation-complexity / avl-history | wiki-avl-tree（Wikipedia） | 定义、O(log n) 复杂度、1962 起源 |
| avl-balance-factor / avl-balance-invariant / avl-rotation / avl-app-database | programiz-avl-tree-v2 | 平衡因子定义与不变量、旋转、数据库应用 |
| avl-four-cases / avl-delete-rebalance / avl-rotation-cost | wiki-avl-tree（Wikipedia） | 四种失衡旋转、删除回溯、旋转摊还成本 |
| avl-vs-red-black / avl-rb-math | wiki-avl-tree（Wikipedia） | 与红黑树比较与数学关系 |

## 待验证项

- 删除回溯中"旋转后子树高度下降、失衡向上传播"的逐层细节（Wikipedia 原文含图示引用，本页文字未完整收录）。

## 关联知识

- [[binary-search-tree]] —— AVL 是 BST 的自平衡特化；退化 BST 是 AVL 要解决的核心问题。
- [[red-black-tree]] —— 同为自平衡 BST，平衡更宽松、写放大更小；每个 AVL 都可染成红黑树。
- [[binary-tree]] —— 树结构基础：高度、深度、遍历。
- [[data-structure-optimization]] —— 从性能视角选择数据结构时 AVL/RB 的取舍。

## 详细章节

### 定义与性质

AVL 树是一种自平衡二叉搜索树：任意节点的两棵子树高度差不超过 1，一旦超过就通过再平衡恢复。该性质保证树高为 O(log n)，因此查找、插入、删除在平均与最坏情况下都是 O(log n)。

它以发明者 Georgy Adelson-Velsky 与 Evgenii Landis 命名，1962 年发表于论文 "An algorithm for the organization of information"，是最早的自平衡二叉搜索树数据结构。

### 平衡因子

平衡因子 = 左子树高度 − 右子树高度。AVL 树的自平衡性质由平衡因子维护，其值必须始终为 -1、0 或 +1。插入或删除使某节点平衡因子越出该范围（到达 ±2）时，以该节点为根的子树失衡，需要旋转。

### 旋转

旋转交换子树中节点的位置，不破坏 BST 的有序性。四种失衡情形：

| 情形 | 判定（X 失衡，Z 为较高子树根） | 修复 |
| --- | --- | --- |
| Right Right | 右子树的右子树过高 | 单旋 rotate_Left |
| Left Left | 左子树的左子树过高 | 单旋 rotate_Right（镜像） |
| Right Left | 右子树的左子树过高 | 双旋 rotate_RightLeft |
| Left Right | 左子树的右子树过高 | 双旋 rotate_LeftRight（镜像） |

即 C == B（子方向与平衡方向同侧）用单旋，C != B 用双旋。

### 与红黑树比较

- 两者支持相同操作集合，基本操作同为 O(log n)。
- AVL 平衡更严格（高度差 ≤ 1 vs 红黑树高度差可达 2 倍），查找密集型应用中更快。
- 数学关系：每个 AVL 树都可染成红黑树，反之不然（存在不是 AVL 平衡的红黑树）。
- 旋转成本：AVL 插入 0~3 次尾递归旋转（摊还 O(1)），删除最坏 O(log n) 次（平均 O(1)）。

### 应用

- 数据库中大记录的索引。
- 大型数据库中的检索。

## 参考

- https://en.wikipedia.org/wiki/AVL_tree
- https://www.programiz.com/dsa/avl-tree
