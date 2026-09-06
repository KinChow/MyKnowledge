---
aliases:
- 解释器
- Interpreter Pattern
confidentiality: public
domain: computer-science
evidence:
- claim: 解释器模式是一种设计模式，规定了如何对一种语言中的句子进行求值。
  claim_id: interpreter-pattern-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-5d69d4a730fc
    exact: the interpreter pattern is a design pattern that specifies how to evaluate
      sentences in a language
  targets:
  - evidence_id: evidence-5d69d4a730fc
    source_id: web-computer-science-interpreter-pattern
id: interpreter-pattern
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-interpreter-pattern
status: published
tags:
- design-pattern
- behavioral
- interpreter
title: 解释器模式
updated_at: '2026-09-06'
---
# 解释器模式

## 一句话结论

解释器模式**规定了如何对一种语言中的句子进行求值**：为语言中每个符号（终结符/非终结符）定义类，句子的**语法树（AST）是组合模式的一个实例**，通过递归调用 `interpret()` 完成求值。它适合"文法简单、求值频繁"的场景（如表达式计算、SQL 片段、通信协议描述），但文法复杂时应改用解析器生成器等方案。

## 核心概念

- **定义**：解释器模式是一种设计模式，规定如何对一种语言中的句子进行求值。
- **每个符号一个类**：为专用计算机语言中的每个符号（终结符 terminal / 非终结符 nonterminal）定义一个类。
- **语法树 = 组合模式实例**：句子在语言中的语法树是组合模式的一个实例，用于为客户端求值（解释）该句子。
- **AST 递归解释**：用表达式类层次表示文法，实现 `interpret()` 操作；对 AST 调用 `interpret()` 完成求值。
- **不负责建树**：解释器模式不描述如何构建语法树——可由客户端手工构建，或由解析器自动构建。

## 工作机制

- 定义简单语言的文法：建立 `Expression` 类层次并实现 `interpret()` 操作。
- 用 `Expression` 实例构成的抽象语法树（AST）表示语言中的一个句子。
- 通过调用 AST 上的 `interpret()` 来解释句子。
- 表达式对象被递归组合成复合/树状结构（即抽象语法树，见组合模式）。
- `TerminalExpression` 无子节点、直接解释；`NonTerminalExpression` 维护子表达式容器并把解释请求转发给子表达式。

## 示例或代码

经典场景：算术表达式求值、正则表达式解释、简单 DSL。以"数字 + 加号"迷你语言为例：

```python
# 迷你语言: number '+' number
class Expression:
    def interpret(self): ...

class Number(Expression):                 # TerminalExpression 终结符
    def __init__(self, value): self._v = value
    def interpret(self): return self._v

class Plus(Expression):                   # NonTerminalExpression 非终结符
    def __init__(self, left, right): self._l, self._r = left, right
    def interpret(self):                  # 递归解释
        return self._l.interpret() + self._r.interpret()

# 手动构建 AST（"1 + 2"）
ast = Plus(Number(1), Number(2))
print(ast.interpret())                    # 3
```

## 常见误区

- **文法复杂时硬用解释器**：文法庞大时类数量爆炸、难以维护，应使用解析器生成器/正规表达式库。
- **混淆"定义文法"与"构建语法树"**：解释器只管求值；AST 构建可由客户端或解析器完成。
- **忽略与组合模式的联系**：解释器的核心结构就是递归的组合模式，忘记这一点会写不出正确的递归解释。
- **把解释器当通用解析框架**：它更适用于小而简单的语言/表达式。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| interpreter-pattern-definition | web-computer-science-interpreter-pattern | 解释器规定如何对语言句子求值；每个符号一个类，语法树是组合模式的实例 |

## 待验证项

无。英文定义直接来自 Wikipedia《Interpreter pattern》条目，已锚定原文逐字引文。

## 关联知识

- [[compilation-principle]] —— 词法/语法分析、抽象语法树与求值，是解释器模式的工程化应用。
- [[composite-pattern]]（结构型） —— 语法树是组合模式实例，递归求值依赖组合结构。
- [[visitor-pattern]] —— 对 AST 的多种操作（解释、打印、变换）可基于访问者实现。
- [[software-design]] —— 行为型模式在 23 种 GoF 模式中的定位。

## 详细章节

### 定义

在计算机编程中，解释器模式是一种设计模式，它规定了如何对一种语言中的句子进行求值。基本思想是：为一种**专用计算机语言**中的每个符号（终结符或非终结符）定义一个类。语言中一个句子的**语法树**是**组合模式**的一个实例，用于为客户端求值（解释）该句子。

解释器模式是 23 个著名 GoF 设计模式之一。典型用途：SQL 等专用数据库查询语言；常用于描述通信协议的专用计算机语言；大多数通用编程语言实际上也内含若干专用语言。

### 参与者

- **AbstractExpression（抽象表达式）**：声明抽象的解释操作 `interpret(context)`。
- **TerminalExpression（终结符表达式）**：无子节点，直接解释（如数字、字面量）。
- **NonTerminalExpression（非终结符表达式）**：维护子表达式容器（`expressions`），把解释请求转发给子表达式（如加法、乘法）。
- **Context（上下文）**：解释所需的全局信息（符号表、环境）。
- **Client（客户端）**：构建（或获取）语法树并调用其 `interpret()`。

### 结构

- 表达式对象递归组合成树（AST），即组合模式的应用。
- `interpret()` 从根递归下推：非终结符转发给子表达式，终结符直接求值。
- 对象协作图：客户端向 AST 发解释请求 → 请求沿树向下转发到所有对象 → 终结符对象直接执行解释。
- 解释器模式**不描述如何构建 AST**——可由客户端手工构建或由解析器自动构建。

### 适用场景

- 需要解释一种简单、文法稳定的小型语言（表达式、配置、规则）。
- 该语言被频繁求值且易扩展文法。
- 语法树结构固定、解释逻辑可按语法节点自然分解。
- SQL 子集、查询过滤表达式、数学公式求值等。

### 优缺点

优点：

- 文法易于扩展：新增符号 = 新增表达式类。
- 求值逻辑按语法节点内聚，结构清晰、易于实现。
- 与组合模式天然契合，便于递归处理。

缺点：

- 文法复杂时类数量急剧膨胀，维护困难。
- 性能：递归解释开销大（可先用 AST 优化/编译）。
- 只适合"小而简单"的语言，大型语言应使用解析器生成器。

### 与相关模式关系

- **与组合模式**：解释器的语法树是组合模式的直接实例，递归结构是其基础。
- **与访问者模式**：可用访问者对同一 AST 实现多种操作（求值、打印、类型检查）。
- **与迭代器模式**：遍历 AST 节点可借助迭代器。
- **与工厂方法/建造者**：AST 的构建可由建造者或解析器（常配合工厂）完成。

## 参考

https://en.wikipedia.org/wiki/Interpreter_pattern
