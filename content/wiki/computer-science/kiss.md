---
aliases:
- keep-it-simple-stupid
confidentiality: public
domain: computer-science
evidence:
- claim: KISS（Keep it simple, stupid）是设计原则，1960 年由美国海军首次提出，其含义是简单性应当成为设计目标。
  claim_id: kiss-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-38397a5e1e8d
    exact: KISS ("Keep it simple, stupid") is a design principle first noted by the
      U.S. Navy in 1960. First seen partly in American English by at least 1938, KISS
      implies that simplicity should be a design goal.
  targets:
  - evidence_id: evidence-38397a5e1e8d
    source_id: web-computer-science-kiss
id: kiss
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-kiss
status: published
tags:
- kiss
- design-principle
- simplicity
- software-engineering
title: KISS原则
updated_at: '2026-09-06'
---
# KISS原则

## 一句话结论

KISS（Keep It Simple, Stupid，保持简单、直接）是一条设计原则，核心含义是**简单性应当成为设计目标**：系统应该尽可能简单，避免不必要的复杂性。它最初由美国海军在 1960 年提出，并因洛克希德"臭鼬工厂"总工程师 Kelly Johnson 而广为流传——好的设计应能在最朴素的条件下被理解、维护和修复。

## 核心概念

- **KISS 的定义**：Keep It Simple, Stupid——让简单成为设计目标；系统能简单就尽量简单。
- **起源**：1960 年美国海军首次记载；1938 年已有 "Keep it Short and Simple" 的变体。
- **Kelly Johnson 的版本**：臭鼬工厂总工程师，把原则解释为"设计出来的东西要能被一线人员在有限工具下维修"。
- **"stupid" 的含义**：不是贬低使用者，而是指"故障方式"与"可用维修手段"之间的关系——设计要简单到愚蠢条件下也能处理。
- **反例**：Heath Robinson 机关与 Rube Goldberg 机器——用过于复杂的方案解决简单问题的幽默反例，即"非 KISS"。

## 工作机制

- **以简单为设计目标**：在做每个设计决策时，优先选择更简单的方案，除非有明确的理由需要复杂度。
- **约束条件下的简单**：Kelly Johnson 用"一把工具修好战斗机"的故事说明——设计复杂度必须与可用的维修/维护能力匹配。
- **识别非 KISS**：当一个简单任务被包装成多层次的复杂机制时，就是"非 KISS"信号。
- **广泛适用**：美国军方（海军、空军）与软件开发领域都广泛使用该原则；在软件中体现为减少不必要的抽象、层级与"聪明"技巧。

## 示例或代码

**起源故事**：Kelly Johnson 递给设计团队一小把工具，挑战他们——设计的喷气式飞机必须让普通机械师在战地条件下、只用这些工具就能维修。因此"stupid"指的是"故障方式"与"可用的维修手段"之间的关系：设计必须简单到如此朴素的条件也能处理。

**软件中的 KISS 示例**：

```cpp
// 非 KISS：为了"扩展性"引入多余层级
class CommentServiceProxyFactoryAdapter { /* ... */ };

// KISS：直接、可读
void publish_comment(const Comment& c) {
    db.save(c);
    notify(c);
}
```

**非 KISS 反例**：Heath Robinson 机关 / Rube Goldberg 机器——用极度复杂的机械解决一个简单动作，是"非 KISS"的幽默象征。

## 常见误区

- **把 KISS 等同于"禁止任何复杂度"**：KISS 是"让简单成为目标"，不是"永远选最简单"；有明确理由时复杂度是允许的。
- **把 KISS 当成"代码少"**：简单不等于行数少，而是结构可理解、可维护；过度压缩的"聪明代码"反而违背 KISS。
- **忽视上下文约束**：KISS 强调设计与"可用的理解/维修手段"匹配；脱离使用场景谈简单没有意义。
- **把"stupid"当贬义**：它描述的是故障环境与维修手段的朴素性，不是使用者愚蠢。
- **为"可能的需要"提前加复杂度**：这与 [[yagni]] 相关——不要为尚未出现的需求预埋复杂机制。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| kiss-definition | web-computer-science-kiss | KISS 由美国海军 1960 年首次记载，含义是简单性应当成为设计目标 |

## 待验证项

无。

## 关联知识

- [[yagni]] —— 不要实现不需要的功能：从"需求"角度避免不必要的复杂度。
- [[dry]] —— 不要重复自己：与 KISS 同属设计原则，但关注"知识唯一表示"。
- [[solid]] —— 面向对象设计原则。
- [[lod]] —— 最少知识原则（降低耦合）。
- [[software-design]] —— 软件设计总览。
- [[refactoring-concepts-and-principles]] —— 重构：让设计保持简单的手段。
- [[four-rules-of-simple-design]] —— 简单设计四原则。

## 详细章节

### KISS原则

#### 定义

KISS（Keep It Simple, Stupid）是一条设计原则，1960 年由美国海军首次记载；早在 1938 年，美式英语中已有 "Keep it Short and Simple" 的变体。KISS 的含义是：简单性应当成为设计目标。

短语的其他变体（通常是对更直白的 "stupid" 的委婉说法）包括："keep it simple, silly"（保持简单，傻瓜）、"keep it simple and straightforward"（保持简单直接）、"keep it simple, soldier"（保持简单，士兵）、"keep it simple, sweetie"（保持简单，甜心）等。

#### 起源

"Keep it simple, stupid" 这一缩略词据传由 Kelly Johnson 首创。他是洛克希德臭鼬工厂（Lockheed Skunk Works，洛克希德 U-2 与 SR-71 黑鸟侦察机等的制造者）的总工程师。不过 "Keep it Short and Simple" 的变体在 1938 年的《Minneapolis Star》上已有记载。

关于该原则最经典的例子是：Johnson 递给设计团队一小把工具，要求他们设计的喷气式飞机必须能在战地条件下、由普通机械师仅用这些工具完成维修。因此，"stupid" 指的是"事物的故障方式"与"可用于修复它的手段"之间的关系——设计必须简单到在最朴素的条件（包括最朴素的人员与工具）下也能被处理。

该缩略词被美国军方（尤其是海军与空军）广泛使用，也流行于软件开发领域。它在 1970 年前后已广泛使用。

#### 变体与反例

该原则很可能起源于类似的最小化概念。Heath Robinson 机关与 Rube Goldberg 机器——故意用过度复杂的方案解决简单任务或问题的装置——是"非 KISS"方案的幽默例证。

#### 软件中的使用

在软件开发中，KISS 意味着：优先选择最简单的可行方案；不为猜测中的未来需求预埋复杂度（与 YAGNI 呼应）；让代码结构清晰、直接、可维护。它常与其他简单性导向的原则（简单设计四原则、YAGNI、DRY）一起指导日常编码决策。

## 参考

- Wikipedia — KISS principle: https://en.wikipedia.org/wiki/KISS_principle
- Ben R. Rich — Clarence Leonard (Kelly) Johnson 1910–1990: A Biographical Memoir, National Academies Press, 1995
