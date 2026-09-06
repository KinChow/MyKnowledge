---
aliases:
- 享元模式
- Flyweight Pattern
- 轻量级模式
confidentiality: public
domain: computer-science
evidence:
- claim: 享元模式指通过与其他相似对象共享部分数据来最小化内存占用的对象。
  claim_id: flyweight-pattern-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-cf5b706ff406
    exact: flyweight software design pattern refers to an object that minimizes memory
      usage by sharing some of its data with other similar objects. The flyweight
      pattern is one of twenty-three GoF design patter
  targets:
  - evidence_id: evidence-cf5b706ff406
    source_id: web-computer-science-flyweight-pattern
id: flyweight-pattern
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-flyweight-pattern
status: published
tags:
- design-pattern
- structural
- flyweight
title: 享元模式
updated_at: '2026-09-06'
---
# 享元模式

## 一句话结论

享元模式（Flyweight Pattern）通过**共享不可变的内在状态（intrinsic state）**，让大量相似对象复用同一份数据，从而**最小化内存占用**——它把对象状态拆成可共享的内在状态与调用时传入的外在状态（extrinsic state），是典型的"以共享换内存"的结构型优化模式。

## 核心概念

- **Flyweight（享元）**：可共享的对象，只保存内在状态。
- **内在状态（intrinsic state）**：对象间相同、可共享、不变的部分，存储在享元内部。
- **外在状态（extrinsic state）**：随使用场景变化、由客户端在调用时传入的部分，不存于享元。
- **FlyweightFactory（享元工厂）**：缓存并复用享元对象，按 key 返回已存在的实例。
- **共享的意义**：大量对象只需少数几个享元实例 + 各自的外在状态。

## 工作机制

1. 把对象状态拆分为内在状态（共享）与外在状态（不共享）。
2. `FlyweightFactory` 维护一个享元池：客户端请求时先查池，命中则复用，未命中则创建并放入池。
3. 客户端调用享元操作时，把外在状态作为参数传入，与内在状态共同参与运算。
4. 结果：N 个"逻辑对象"只需要少量物理对象，内存显著下降。

关键点：享元必须是**可安全共享**的——内在状态不可变，外在状态不存储在享元内部，否则共享会引入数据竞争或串扰。

## 示例或代码

以文本编辑器中的字符渲染为例（共享字形，避免每个字符都建独立对象）：

```java
import java.util.*;

// Flyweight：只含内在状态（字形数据）
class Glyph {
    private final char symbol;
    private final byte[] bitmap;
    Glyph(char symbol) { this.symbol = symbol; this.bitmap = render(symbol); }
    private byte[] render(char c) { /* 生成字形位图 */ return new byte[16]; }
    void draw(int x, int y, int fontSize) {
        // 用内在状态 symbol/bitmap + 外在状态 x/y/fontSize 完成绘制
    }
}

// FlyweightFactory：享元工厂，按字符共享
class GlyphFactory {
    private final Map<Character, Glyph> pool = new HashMap<>();
    Glyph get(char c) {
        return pool.computeIfAbsent(c, Glyph::new); // 复用或创建
    }
}

// 客户端：只保存外在状态（位置），复用享元
GlyphFactory factory = new GlyphFactory();
for (int i = 0; i < 10000; i++) {
    Glyph g = factory.get(text.charAt(i % 26)); // 最多 26 个享元实例
    g.draw(i, 0, 12);                           // 位置作为外在状态传入
}
```

## 常见误区

- **把享元当成简单的对象池**：对象池关注"复用减少创建开销"；享元关注"共享数据减少内存"，且严格区分内在/外在状态。
- **忽视内在状态不可变性**：共享对象若被修改会污染所有使用者；内在状态必须不可变。
- **把外在状态塞进享元**：那会破坏共享，令模式失效。
- **以为享元只为性能**：它本质是结构型模式，以"共享"实现复用与内存优化；过度使用会引入工厂与状态拆分复杂度。
- **与单例混淆**：单例全局唯一一份；享元是"同类共享多份"，由工厂管理。

## 证据映射

| claim_id | 来源 | 要点 |
| --- | --- | --- |
| flyweight-pattern-definition | web-computer-science-flyweight-pattern | 享元对象通过共享部分数据最小化内存占用，是 GoF 二十三种模式之一 |

## 待验证项

无。定义已由 web 源（Wikipedia Flyweight pattern 条目）锚定。

## 关联知识

- [[software-design]] —— 设计模式分类：享元属于结构型模式。
- [[object-oriented]] —— 值语义与共享引用是理解内在/外在状态的基础。
- [[data-structure-optimization]] —— 共享数据结构（如字符串驻留）与享元思想一致。
- [[flyweight-pattern]] 相关——与"池化""缓存"思想相关。
- [[cache-optimization]] —— 内存占用与缓存命中优化的背景。
- [[class-diagram]] —— 用 UML 类图表达 FlyweightFactory/Flyweight/Client 关系。

## 详细章节

### 定义

享元模式（Flyweight Pattern）是 GoF 二十三种设计模式之一，属于结构型模式。它指一个**通过与其他相似对象共享部分数据来最小化内存占用**的对象。在其他语境中，共享数据结构的思想也被称为"哈希共构"（hash consing）。该概念由 Paul Calder 与 Mark Linton 于 1990 年提出，最初用于在所见即所得文档编辑器中高效处理字形信息。

### 参与者

- **Flyweight**：声明享元的接口，通过它可接收并作用于外在状态。
- **ConcreteFlyweight**：实现享元接口，存储内在状态（必须可共享）。
- **UnsharedConcreteFlyweight**：不共享的享元（如组合结构中的根节点），并非所有享元都必须共享。
- **FlyweightFactory**：创建并管理享元对象，保证共享；请求不存在的 key 时创建，否则返回缓存实例。
- **Client**：维护对享元的引用，并计算/存储外在状态。

### 结构

```
Client → FlyweightFactory ──► Flyweight (interface)
              │                     ↑
        (pool: Map<key, Flyweight>) ConcreteFlyweight
```

### 适用场景

- 应用中存在大量相似对象，导致内存占用过高。
- 对象的大多数状态可提取为共享的内在状态。
- 内在状态可移除后，剩余的外在状态可由客户端计算并传入。
- 性能优化（内存）优先于可读性/简单性的场景。

### 优点与缺点

优点：

- 大幅减少对象数量，降低内存占用。
- 减少创建开销，提高运行效率。
- 内在状态集中管理，便于统一维护。

缺点：

- 拆分内在/外在状态增加设计与编码复杂度。
- 需要管理工厂与共享池，逻辑变复杂。
- 共享对象若被错误修改，会引入难以排查的串扰/并发问题。

### 与相关模式的关系

- **与组合（Composite）**：组合模式可用享元共享组合结构中的叶子节点。
- **与单例（Singleton）**：享元工厂可配合单例；享元本身非单例，而是"按 key 共享"。
- **与缓存/池化思想**：共享复用同一内存优化目标，但享元强调状态拆分。
- **与策略（Strategy）**：享元常被用来共享策略对象以减少对象数量。

## 参考
- https://en.wikipedia.org/wiki/Flyweight_pattern
