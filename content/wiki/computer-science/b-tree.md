---
aliases:
- B-Tree
- B 树索引
- 多路平衡搜索树
confidentiality: public
domain: computer-science
evidence:
- claim: B 树是特化的 m 路搜索树，为优化数据访问而设计，尤其面向基于磁盘的存储系统；m 阶 B
    树每个节点最多 m 个孩子、m−1 个键；m 的取值由磁盘块大小与键大小决定。
  claim_id: bt-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-66214b606544
    exact: |-
      A B-Tree is a specialized m-way tree designed to optimize data access, especially on disk-based storage systems.
  - evidence_id: evidence-8ae77e263dd5
    exact: |-
      In a B-Tree of order m, each node can have up to m children and m-1 keys, allowing it to efficiently manage large datasets.
  - evidence_id: evidence-9816f0e07ebc
    exact: |-
      The value of m is decided based on disk block and key sizes.
  targets:
  - evidence_id: evidence-66214b606544
    source_id: web-computer-science-b-tree
  - evidence_id: evidence-8ae77e263dd5
    source_id: web-computer-science-b-tree
  - evidence_id: evidence-9816f0e07ebc
    source_id: web-computer-science-b-tree
- claim: B 树单个节点能存大量键（包括大键值），显著降低树高，从而减少代价高昂的磁盘操作。
  claim_id: bt-height-advantage
  support: direct
  supporting_quotes:
  - evidence_id: evidence-b1b915105f64
    exact: |-
      One of the standout features of a B-Tree is its ability to store a significant number of keys within a single node, including large key values.
  - evidence_id: evidence-d8f1cb6c82c0
    exact: |-
      It significantly reduces the tree’s height, hence reducing costly disk operations.
  targets:
  - evidence_id: evidence-b1b915105f64
    source_id: web-computer-science-b-tree
  - evidence_id: evidence-d8f1cb6c82c0
    source_id: web-computer-science-b-tree
- claim: B 树（m 阶）性质：所有叶节点在同一层（同深度）；节点内多个键按升序存储；非叶节点（除根）至少有 m/2 个孩子；所有节点（除根）至少有 m/2−1 个键；有 n−1 个键的非叶节点应有 n 个非空孩子。
  claim_id: bt-properties
  support: direct
  supporting_quotes:
  - evidence_id: evidence-76dc09ac3b6d
    exact: |-
      - All leaf nodes of a B tree are at the same level, i.e. they have the same depth (height of the tree).
  - evidence_id: evidence-64ae9b2b952f
    exact: |-
      - The keys of each node of a B tree (in case of multiple keys), should be stored in the ascending order.
  - evidence_id: evidence-929c66dfcdfe
    exact: |-
      - In a B tree , all non-leaf nodes (except root node) should have at leastm/2 children.
  - evidence_id: evidence-00006726c56b
    exact: |-
      - All nodes (except root node) should have at least m/2 - 1 keys.
  - evidence_id: evidence-c030dbd0c441
    exact: |-
      A non-leaf node with n-1 key values should have n non NULL children.
  targets:
  - evidence_id: evidence-76dc09ac3b6d
    source_id: web-computer-science-b-tree
  - evidence_id: evidence-64ae9b2b952f
    source_id: web-computer-science-b-tree
  - evidence_id: evidence-929c66dfcdfe
    source_id: web-computer-science-b-tree
  - evidence_id: evidence-00006726c56b
    source_id: web-computer-science-b-tree
  - evidence_id: evidence-c030dbd0c441
    source_id: web-computer-science-b-tree
- claim: M 路树可能平衡也可能倾斜，而 B 树总是自平衡的。
  claim_id: bt-self-balanced
  support: direct
  supporting_quotes:
  - evidence_id: evidence-a2c2600534ba
    exact: |-
      While M-way trees can be either balanced or skewed, B-Trees are always self-balanced.
  targets:
  - evidence_id: evidence-a2c2600534ba
    source_id: web-computer-science-b-tree
- claim: B 树的查找与二叉搜索树的查找类似，从根开始递归向下遍历。
  claim_id: bt-search
  support: direct
  supporting_quotes:
  - evidence_id: evidence-c36ad82f4456
    exact: |-
      Search is similar to the search in Binary Search Tree.
  - evidence_id: evidence-6c2e5c8c86d0
    exact: |-
      Start from the root and recursively traverse down.
  targets:
  - evidence_id: evidence-c36ad82f4456
    source_id: web-computer-science-b-tree
  - evidence_id: evidence-6c2e5c8c86d0
    source_id: web-computer-science-b-tree
- claim: B 树用于大型数据库中访问磁盘上的数据；借助索引特性可实现多级索引；多数服务器也采用 B 树方案；CAD 系统用它组织和检索几何数据。
  claim_id: bt-applications
  support: direct
  supporting_quotes:
  - evidence_id: evidence-8214458f5d1a
    exact: |-
      It is used in large databases to access data stored on the disk
  - evidence_id: evidence-2759f2b8a2fa
    exact: |-
      With the indexing feature, multilevel indexing can be achieved.
  - evidence_id: evidence-b73b4224b61e
    exact: |-
      Most of the servers also use the B-tree approach.
  - evidence_id: evidence-1c09cbbe9339
    exact: |-
      B-Trees are used in CAD systems to organize and search geometric data.
  targets:
  - evidence_id: evidence-8214458f5d1a
    source_id: web-computer-science-b-tree
  - evidence_id: evidence-2759f2b8a2fa
    source_id: web-computer-science-b-tree
  - evidence_id: evidence-b73b4224b61e
    source_id: web-computer-science-b-tree
  - evidence_id: evidence-1c09cbbe9339
    source_id: web-computer-science-b-tree
- claim: B 树对插入、删除、查找等基本操作有保证的 O(log n) 时间复杂度，适合大数据集与实时应用；B 树自平衡；高并发、高吞吐；存储利用率高。
  claim_id: bt-advantages
  support: direct
  supporting_quotes:
  - evidence_id: evidence-5363f1317e57
    exact: |-
      B-Trees have a guaranteed time complexity of O(log n) for basic operations like insertion, deletion, and searching, which makes them suitable for large data sets and real-time applications.
  - evidence_id: evidence-106c338287c4
    exact: |-
      B-Trees are self-balancing.
  - evidence_id: evidence-2f0c8558da51
    exact: |-
      High-concurrency and high-throughput.
  - evidence_id: evidence-8c0c9f65c122
    exact: |-
      Efficient storage utilization.
  targets:
  - evidence_id: evidence-5363f1317e57
    source_id: web-computer-science-b-tree
  - evidence_id: evidence-106c338287c4
    source_id: web-computer-science-b-tree
  - evidence_id: evidence-2f0c8558da51
    source_id: web-computer-science-b-tree
  - evidence_id: evidence-8c0c9f65c122
    source_id: web-computer-science-b-tree
- claim: B 树是基于磁盘的数据结构，磁盘占用可能较高；且并非在所有场景下都是最优选择。
  claim_id: bt-disadvantages
  support: direct
  supporting_quotes:
  - evidence_id: evidence-ecdd8791e2b1
    exact: |-
      B-Trees are based on disk-based data structures and can have a high disk usage.
  - evidence_id: evidence-613b328ca2f2
    exact: |-
      Not the best for all cases.
  targets:
  - evidence_id: evidence-ecdd8791e2b1
    source_id: web-computer-science-b-tree
  - evidence_id: evidence-613b328ca2f2
    source_id: web-computer-science-b-tree
id: b-tree
kind: reference
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-b-tree
- working-computer-science-b-tree
status: published
tags:
- data-structure
- tree
- disk-index
title: B 树
updated_at: '2026-09-05'
---
# B 树

## 一句话结论

B 树是一种**自平衡的多路（m 路）搜索树**，为磁盘存储优化而生：每个节点存多达 m−1 个键、m 个子指针（m 按磁盘块大小选取），一次 I/O 换取一批键的比较，显著压低树高、减少昂贵的磁盘操作。所有叶节点同层、节点半满的约束保证基本操作稳定 O(log n)——它是数据库索引与文件系统的标准底座。

## 核心概念

- **阶（order m）**：节点最多 m 个孩子、m−1 个键；m 由磁盘块与键大小决定，让一个节点恰好填满一个磁盘页。
- **矮胖树形**：单节点存大量键 → 树高显著降低 → 磁盘 I/O 次数减少。
- **半满约束**：除根外节点至少 m/2 个孩子（m/2−1 个键），防止稀疏退化。
- **全叶同层**：所有叶节点深度相同，天然保持平衡。

## 工作机制

### 性质（m 阶 B 树）

1. 所有叶节点在同一层。
2. 节点内多个键按升序排列。
3. 非叶节点（除根）至少有 m/2 个孩子。
4. 所有节点（除根）至少有 m/2−1 个键。
5. 有 n−1 个键的非叶节点恰有 n 个非空孩子。

### 查找

与 BST 查找思想类似：从根开始递归向下。在每个非叶节点内（节点内键升序），若命中 k 返回该节点；否则选择**第一个大于 k 的键之前**的那个孩子分支继续；到达叶节点仍未找到则返回 NULL。节点内的键起到限定搜索范围的作用（分离值/separation values）。

### 插入与删除（概述）

插入总是落在叶节点；节点满则分裂（分裂向上传播，可致树高 +1）。删除若发生在内部节点需用前驱/后继键替换；节点低于半满则借键或与兄弟合并（可致树高 −1）。两者都只影响局部，这正是"全叶同层"能一直维持的原因。

## 示例或代码

复杂度（n 为键数）：

| 操作 | 复杂度 |
| --- | --- |
| 查找 | O(log n) |
| 插入 | O(log n) |
| 删除 | O(log n) |

高度界：完全满时 h_min = ⌈log_m(n+1)⌉ − 1；最稀疏时 h_max = ⌊log_t((n+1)/2)⌋（t 为最小孩子数）。树高为对数级且底数是 m——m 越大树越矮。

## 常见误区

- **"B 树的 B 是 Binary"**：不是，B 树是多路的（m-way）；二叉搜索树才是每个节点至多两个孩子。
- **"B 树和 B+ 树是一回事"**：B+ 树把数据全放叶层并用链表串联，内部节点只作索引；B 树的数据可出现在任意节点。数据库索引多用 B+ 树。
- **"节点越满越好"**：半满下限是性能保证——只有"至少半满"才能让树高维持对数下界、删除后不退化。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| bt-definition / bt-height-advantage | web-computer-science-b-tree | m 路定义、m−1 键/m 孩子、树高与磁盘 I/O |
| bt-properties | web-computer-science-b-tree | 五条阶约束性质 |
| bt-self-balanced / bt-search | web-computer-science-b-tree | 恒自平衡；查找同 BST 思想 |
| bt-applications / bt-advantages / bt-disadvantages | web-computer-science-b-tree | 数据库/多级索引/服务器/CAD；O(log n) 与高并发；磁盘占用 |

## 待验证项

- 插入分裂与删除合并的逐情形算法细节源中未展开，仅收录结论性描述；后续可补 CLRS 或 ODS 的 B 树章节作第二来源。

## 关联知识

- [[binary-search-tree]] —— B 树查找逻辑是其多路推广。
- [[avl-tree]] / [[red-black-tree]] —— 二叉自平衡树：内存场景；B 树：磁盘场景（扇出大、层少）。
- [[generic-tree]] —— B 树是孩子数有上下界约束的通用树。
- [[data-structure-optimization]] —— 外存索引选型（B/B+ 树 vs LSM）。

## 详细章节

### 定义与背景

B 树是特化的 m 路搜索树，为优化数据访问设计，尤其针对基于磁盘的存储系统。m 阶 B 树每个节点最多 m 个孩子、m−1 个键，使其能高效管理大数据集；m 的取值基于磁盘块与键的大小决定。单节点可存大量键，显著降低树高，从而减少昂贵的磁盘操作。

### 为什么需要 B 树

- **优于普通 M 路树**：M 路树可平衡可倾斜，B 树恒自平衡；层数更少、访问时间显著缩短，特别适合外存。
- **面向大数据集**：降低的树高与平衡结构使顺序访问更快、插入删除更简单，可在保持有序的同时高效管理数百万条记录。

### 应用

- 大型数据库访问磁盘数据；多级索引。
- 多数服务器采用 B 树方案。
- CAD 系统组织和检索几何数据；亦用于自然语言处理、计算机网络与密码学领域。

## 参考

- https://www.geeksforgeeks.org/dsa/introduction-of-b-tree-2/
- [[avl-tree]]、[[red-black-tree]] —— 内存自平衡树对照。
