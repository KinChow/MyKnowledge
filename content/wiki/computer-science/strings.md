---
aliases:
- 字符串
- String
- 字符串数据结构
confidentiality: public
domain: computer-science
evidence:
- claim: 字符串传统上是字符序列，可作为字面量常量或某种变量；后者允许元素被修改与长度改变，也可能在创建后固定。字符串常实现为字节（或字）的数组数据结构，用某种字符编码存储字符元素序列。
  claim_id: string-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-1447528d9989
    exact: In computer programming, a string is traditionally a sequence of characters,
      either as a literal constant or as some kind of variable. The latter may allow
      its elements to be mutated and the length changed, or it may be fixed (after
      creation). A string is often implemented as an array data structure of bytes
      (or words) that stores a sequence of elements, typically characters, using some
      character encoding.
  targets:
  - evidence_id: evidence-1447528d9989
    source_id: web-computer-science-strings
- claim: 字符串通常实现为字节、字符或码元（code unit）数组，以便快速访问单个单元或子串；少数语言（如 Haskell）用链表实现。
  claim_id: string-representation
  support: direct
  supporting_quotes:
  - evidence_id: evidence-812fbabfc66a
    exact: Strings are typically implemented as arrays of bytes, characters, or code
      units, to allow fast access to individual units or substrings, including characters
      when they have a fixed length. A few languages such as Haskell implement them
      as linked lists instead.
  targets:
  - evidence_id: evidence-812fbabfc66a
    source_id: web-computer-science-strings
- claim: 许多高级语言把字符串作为原始数据类型（如 JavaScript、PHP），多数其他语言则作为复合数据类型，部分语言在书写字面量时提供专门支持（如
    Java 与 C#）。
  claim_id: string-types
  support: direct
  supporting_quotes:
  - evidence_id: evidence-18083865b0a7
    exact: Many high-level languages provide strings as a primitive data type, such
      as JavaScript and PHP, while most others provide them as a composite data type,
      some with special language support in writing literals, for example, Java and
      C#.
  targets:
  - evidence_id: evidence-18083865b0a7
    source_id: web-computer-science-strings
- claim: 文本编辑器的核心数据结构是管理代表当前文件状态的字符串；除单个连续字符数组外，常用 gap buffer、行链表、piece table 或 rope
    等替代表示，使插入、删除与撤销等操作更高效。
  claim_id: string-editor-repr
  support: direct
  supporting_quotes:
  - evidence_id: evidence-0ba90d1d9d6c
    exact: The core data structure in a text editor is the one that manages the string
      (sequence of characters) that represents the current state of the file being
      edited. While that state could be stored in a single long consecutive array
      of characters, a typical text editor instead uses an alternative representation
      as its sequence data structure—a gap buffer, a linked list of lines, a piece
      table, or a rope—which makes certain string operations, such as insertions,
      deletions, and undoing previous edits, more efficient.
  targets:
  - evidence_id: evidence-0ba90d1d9d6c
    source_id: web-computer-science-strings
id: strings
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-strings
status: published
tags:
- string
- data-structure
- algorithm
- text
title: 字符串数据结构
updated_at: '2026-09-06'
---

# 字符串数据结构

## 一句话结论

字符串（string）是**字符的有序序列**，可作为字面量常量或变量；它在底层常实现为字节/字符/码元的**数组**（用某种字符编码存储），因此“随机访问快、插入删除慢”。不同语言把字符串建模为原始类型（JavaScript、PHP）或复合类型（Java、C#、C++ 的 `std::string`）；是否可修改（可变/不可变）与存储表示（定长、空终止、长度前缀、rope 等）决定了典型操作的复杂度。围绕字符串的经典问题（子串查找 KMP、编辑距离等）构成算法与数据结构的重要分支。

## 核心概念

- **字符串**：字符序列，字面量常量或变量；后者可能可变、也可能创建后固定（不可变）。
- **字符编码**：底层以字节/码元存储，用 ASCII、UTF-8、UTF-16 等编码把字符映射为字节序列。
- **存储表示**：连续数组（随机访问快）、空终止（C 风格）、长度前缀、dope vector、rope/链表（编辑友好）。
- **可变性（immutability）**：不可变字符串（Java、Python、C#）在“修改”时产生新对象；可变字符串（C++ `std::string`、JavaScript 字符缓冲）可就地修改。
- **字符串算法**：子串查找（朴素/KMP/BM）、编辑距离、LCP/LCS、模式匹配（正则）、哈希（Rabin-Karp）等。
- **文本编辑器结构**：gap buffer、行链表、piece table、rope——为插入/删除/撤销优化。

## 工作机制

1. **存储布局**：字符串常为数组——字节数组（C/C++、UTF-8）、字符数组、或码元（code unit）数组，从而能快速访问单个单元/子串；少数语言（Haskell）用链表。
2. **长度表示**：空终止（C，需遍历求长、易越界）、长度前缀（Pascal 风格、`std::string` 等，O(1) 求长）、或记录+容量（dope vector/胖指针）。
3. **编码与索引**：定长字符可直接按下标索引；变长编码（UTF-8）下“第 N 个字符”需要扫描或额外索引结构。
4. **可变与不可变**：不可变实现（如 Java `String`）修改时新建对象（多次拼接低效，常需 `StringBuilder`）；可变实现就地扩展，但并发/别名场景需注意。
5. **编辑场景**：文本编辑器用 gap buffer / piece table / rope 等结构，把“在中间插入/删除”从 O(n) 降到更优复杂度，并天然支持撤销。

## 示例或代码

```c
// C：空终止字符串（char 数组 + '\0'），求长需遍历 O(n)
char s[] = "hello";
size_t n = strlen(s);          // O(n)

// C++：std::string，长度前缀、可变、O(1) 求长
#include <string>
std::string s = "hello";
size_t n = s.size();           // O(1)
s += ", world";                // 就地扩展（可能重新分配）
```

```java
// Java：String 不可变，拼接产生新对象
String s = "hello";
String t = s + " world";       // 新建 String；循环拼接应用 StringBuilder
```

```python
# Python：str 不可变；切片/查找
s = "hello"
print(s[0], s[1:3], s.find("ll"))   # 'h' 'el' 2
```

**KMP 子串查找**（示意，朴素匹配为 O(n·m)，KMP 用前缀函数把主串指针不回退到 O(n+m)）：

```
text    = "ABC ABCDAB ABCDABCDABDE"
pattern = "ABCDABD"
前缀表（部分匹配表）驱动 pattern 指针回溯而非 text 指针回退 → O(n+m)
```

## 常见误区

- **“字符串就是字符数组”**：是常见实现，但字符串是抽象数据类型；实现可能是链表、rope、长度前缀等，且往往带编码/长度/容量元数据。
- **“字符串可随意拼接很快”**：不可变字符串在循环中 `+` 拼接会反复复制（O(n²)）；应使用 StringBuilder / `join` 等。
- **“‘修改字符串’都能就地完成”**：Java/Python/C# 的字符串不可变，“修改”实际是创建新对象；C/C++ 可变才可就地改。
- **“空终止字符串没问题”**：C 风格空终止串求长 O(n)、缓冲区越界风险高，是现代语言普遍改长度前缀表示的原因之一。
- **“变长编码按下标索引一定 O(1)”**：UTF-8 下按“字符序号”索引不是天然 O(1)，需按字节索引或额外结构。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| string-definition | web-computer-science-strings | 字符串定义：字符序列、可变/固定、字节数组+编码 |
| string-representation | web-computer-science-strings | 数组实现（快速访问）；Haskell 用链表 |
| string-types | web-computer-science-strings | 原始类型 vs 复合类型（JS/PHP vs Java/C#） |
| string-editor-repr | web-computer-science-strings | 文本编辑器用 gap buffer/rope 等替代表示 |

## 待验证项

- KMP 与编辑距离等算法描述为本文综合的算法常识，未逐字锚定到外部来源；可后续从算法教材/权威页补锚。
- 各语言字符串实现细节（是否可变、存储布局）以具体语言规范为准，本文为概述。

## 关联知识

- [[arrays]] —— 字符串底层最常见的实现结构（数组）。
- [[singly-linked-list]] —— 链表实现字符串（Haskell 等）与编辑场景的替代结构。
- [[stack]] / [[queue]] —— 其它线性表结构（字符串属于线性结构分支）。
- [[b-tree]] —— 存储与索引中与字符串相关的排序/检索（Trie/B+ 树可延伸）。
- [[gpu-overview]] / [[npu-overview]] —— 文本/AI 任务中字符串处理的算力背景。

## 详细章节

### 字符串是什么

在计算机编程中，字符串传统上是**字符序列**，要么作为字面量常量，要么作为某种变量。后者可能允许元素被修改、长度被改变，也可能在创建后固定。字符串常实现为**字节（或字）的数组**，用某种**字符编码**存储字符元素序列；更广义地，字符串也可以指字符以外的数据序列（列表）。

### 用途与表示

字符串通常由字符组成，常用于存储人类可读数据（如单词、句子）。

- **实现形态**：字符串通常实现为字节、字符或码元（code unit）数组，以便快速访问单个单元或子串（字符定长时含字符本身）；少数语言（如 Haskell）用链表实现。
- **数据类型**：许多高级语言把字符串作为原始数据类型（如 JavaScript、PHP），多数其他语言则作为复合数据类型，部分在书写字面量时提供专门支持（如 Java、C#）。

### 常见表示方式

- **Dope vector**：记录字符串起点、长度等元数据的描述符（胖指针），支持 O(1) 长度与子串切片。
- **空终止（Null-terminated）**：C 风格，以 `\0` 结尾，求长需遍历，易越界。
- **字节/位终止（Byte-/bit-terminated）**：用特殊字节/位标记结束，减少浪费。
- **长度前缀（Length-prefixed）**：显式记录长度，O(1) 求长，是 C++ `std::string` 等现代实现的常见方式。
- **记录（Records）**：把字符串建模为带长度/容量/引用计数的结构（如 `std::string` 的 SSO 小字符串优化）。

### 字符串算法

围绕字符串存在丰富的算法与数据结构：

- **子串查找**：朴素 O(n·m)；KMP（前缀函数，主串指针不回退）、BM（坏字符/好后缀）、Rabin-Karp（滚动哈希）等。
- **编辑距离 / LCS**：动态规划求两串相似度（Levenshtein 距离、最长公共子序列）。
- **Trie / 后缀结构**：前缀树（Trie）、后缀数组/后缀树，用于词典、自动补全、子串统计。
- **正则表达式**：基于自动机的模式匹配。
- **哈希与比较**：字符串哈希（滚动哈希）把子串比较近似降到 O(1)。

### 文本编辑器中的字符串结构

文本编辑器的核心数据结构是管理“当前文件状态”的字符串。虽然该状态可存为单个连续字符数组，典型编辑器却使用替代表示——**gap buffer**（插入点附近留空隙）、**行链表**、**piece table**（只记录片段引用）、或 **rope**（平衡树/树形字符串）——使插入、删除与撤销历史等操作更高效，避免中间插入 O(n) 复制整串。

## 参考

- [Wikipedia: String (computer science)](https://en.wikipedia.org/wiki/String_(computer_science))
- [Wikipedia: Knuth–Morris–Pratt algorithm](https://en.wikipedia.org/wiki/Knuth%E2%80%93Morris%E2%80%93Pratt_algorithm)
- [Wikipedia: Rope (data structure)](https://en.wikipedia.org/wiki/Rope_(data_structure))
