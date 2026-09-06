---
aliases:
- 迭代器
- Iterator Pattern
confidentiality: public
domain: computer-science
evidence:
- claim: 迭代器模式是一种设计模式，用迭代器来遍历容器并访问容器的元素。
  claim_id: iterator-pattern-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-05b5c0c26a06
    exact: the iterator pattern is a design pattern in which an iterator is used to
      traverse a container and access the container's elements
  targets:
  - evidence_id: evidence-05b5c0c26a06
    source_id: web-computer-science-iterator-pattern
id: iterator-pattern
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-iterator-pattern
status: published
tags:
- design-pattern
- behavioral
- iterator
title: 迭代器模式
updated_at: '2026-09-06'
---
# 迭代器模式

## 一句话结论

迭代器模式用一个**迭代器（Iterator）对象**来遍历容器（聚合对象）并访问其元素，核心思想是——**"顺序访问聚合对象的元素，同时不暴露其底层表示"**。它把"访问与遍历"从容器中独立出来，使算法与容器解耦：不同的迭代器可用不同方式遍历同一聚合，新增遍历方式也无需改动聚合本身。

## 核心概念

- **定义**：迭代器模式是一种设计模式，用一个迭代器遍历容器并访问其元素。
- **算法与容器解耦**：迭代器模式把算法与容器解耦；当然有些算法必然与容器相关、无法解耦。
- **本质（GoF 定义）**："提供一种方式，顺序访问聚合对象的元素而不暴露其底层表示。"
- **通用算法**：如 `searchForElement()` 可用指定类型的迭代器通用实现，从而在任何支持该迭代器的容器上使用。
- **可扩展遍历**：不同迭代器可不同方式访问/遍历聚合；定义新迭代器即可独立新增访问与遍历操作。

## 工作机制

- 聚合（Aggregate）提供创建迭代器的接口（如 `createIterator()`）；迭代器维护遍历游标与"是否还有下一个"的判定。
- 客户端通过迭代器接口 `hasNext()` / `next()` 顺序访问元素，不接触聚合内部结构。
- 算法（如查找）只依赖迭代器接口，因而可在任何支持该迭代器的容器上复用。
- 若在聚合接口中定义访问/遍历操作，会把聚合绑死在特定遍历方式上，无法在不改接口的前提下新增操作——这正是模式要解决的问题。
- 内建语言支持：很多语言（如 C++ STL、Java、Python `__iter__`）原生提供迭代器机制。

## 示例或代码

Python 示意（自定义迭代器遍历自定义聚合，不暴露内部列表）：

```python
class Words:                       # Aggregate 聚合
    def __init__(self, words):
        self._words = words
    def __iter__(self):            # 创建迭代器
        return WordsIterator(self)

class WordsIterator:               # Iterator 迭代器
    def __init__(self, agg):
        self._agg = agg
        self._i = 0
    def __iter__(self):
        return self
    def __next__(self):            # 顺序访问，不暴露底层表示
        if self._i >= len(self._agg._words):
            raise StopIteration
        w = self._agg._words[self._i]
        self._i += 1
        return w

for w in Words(["hello", "world"]):
    print(w)
```

通用算法示例：`searchForElement()` 若基于迭代器实现，可在数组、链表、树等所有支持该迭代器的容器上复用。

## 常见误区

- **把迭代器与"聚合内部结构"耦合**：迭代器的意义正在于隐藏表示；暴露实现细节就违背了模式意图。
- **在遍历过程中修改聚合**：多数迭代器实现为"fail-fast"或行为未定义，需谨慎。
- **误以为迭代器只适用于数组/列表**：树、图、数据库游标、生成器等都适用。
- **忽略"算法与容器解耦"的边界**：有些算法天然容器相关，无法一概解耦。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| iterator-pattern-definition | web-computer-science-iterator-pattern | 迭代器用于遍历容器并访问元素，算法与容器解耦，不暴露底层表示 |

## 待验证项

无。英文定义直接来自 Wikipedia《Iterator pattern》条目，已锚定原文逐字引文。

## 关联知识

- [[arrays]] / [[linked-list]] 等数据结构 —— 迭代器为各种聚合提供统一遍历接口。
- [[object-oriented]] —— 接口抽象与封装是迭代器模式的实现基础。
- [[software-design]] —— 行为型模式在 23 种 GoF 模式中的定位。
- [[compilation-principle]] —— 语法树遍历可借助迭代器（亦见访问者/解释器模式）。

## 详细章节

### 定义

在面向对象编程中，迭代器模式是一种设计模式：用**迭代器**遍历容器（集合/聚合）并访问容器元素。迭代器模式把**算法与容器解耦**；在有些情况下算法必然与容器相关，因而无法解耦。

例如，假设算法 `searchForElement()` 可基于指定类型的迭代器通用实现，而非作为容器特有算法——这让它可以用于任何支持所需迭代器类型的容器。迭代器模式的本质（GoF）："提供一种方式，顺序访问聚合对象的元素而不暴露其底层表示。"

迭代器模式是 23 个著名 GoF 设计模式之一。它解决的问题：在聚合接口中定义访问与遍历操作是不灵活的，因为这会把聚合"绑死"在特定访问/遍历方式上，并使得后续新增操作不得不修改聚合接口。

### 参与者

- **Iterator（迭代器）**：定义访问与遍历元素的接口（如 `hasNext()`、`next()`、`current()`）。
- **ConcreteIterator（具体迭代器）**：实现迭代器接口，维护遍历当前位置；在聚合对象上遍历。
- **Aggregate（聚合）**：定义创建迭代器对象的接口（如 `createIterator()`）。
- **ConcreteAggregate（具体聚合）**：实现创建迭代器的接口，返回适合自身的具体迭代器实例。

### 结构

- 聚合对象提供工厂式接口创建迭代器；迭代器持有对聚合（或其底层结构）的引用与游标。
- 客户端只依赖迭代器接口完成遍历，不直接操作聚合内部。
- 不同的迭代器实现可对同一聚合提供不同遍历方式（正序、逆序、跳步、树先序等）。
- 新增遍历方式 = 新增迭代器类，无需改动聚合。

### 适用场景

- 需要以统一接口遍历多种异构聚合，且希望隐藏它们的内部结构。
- 需要为同一聚合提供多种遍历方式。
- 希望写出与具体容器无关的通用算法（查找、过滤、统计）。
- 需要在不修改聚合的前提下扩展遍历能力。

### 优缺点

优点：

- 客户端无需知道聚合内部表示，符合封装原则。
- 支持多种遍历方式，且可独立扩展。
- 算法与容器解耦，提高复用性。
- 简化聚合的接口（遍历逻辑外置）。

缺点：

- 引入额外的迭代器类。
- 某些遍历（尤其随机访问）在迭代器抽象下性能受限。
- 并发/遍历中修改聚合需要额外处理。

### 与相关模式关系

- **与组合模式**：组合结构的遍历常借助迭代器（递归遍历）。
- **与访问者模式**：访问者遍历对象结构时可用迭代器获取元素。
- **与解释器模式**：解释器遍历语法树时也常配合迭代器/递归。
- **与工厂方法**：聚合通过工厂方法（`createIterator`）创建迭代器。

## 参考

https://en.wikipedia.org/wiki/Iterator_pattern
