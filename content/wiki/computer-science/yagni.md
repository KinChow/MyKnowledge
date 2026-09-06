---
aliases:
- you-arent-gonna-need-it
confidentiality: public
domain: computer-science
evidence:
- claim: YAGNI（You aren't gonna need it）源自极限编程（XP），主张程序员在确认必要之前不应添加功能。
  claim_id: yagni-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-ab404e6b660d
    exact: '"You aren''t gonna need it" (YAGNI) is a principle which arose from extreme
      programming (XP) that states a programmer should not add functionality until
      deemed necessary.'
  targets:
  - evidence_id: evidence-ab404e6b660d
    source_id: web-computer-science-yagni
id: yagni
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-yagni
status: published
tags:
- yagni
- design-principle
- extreme-programming
- agile
title: YAGNI原则
updated_at: '2026-09-06'
---
# YAGNI原则

## 一句话结论

YAGNI（You Aren't Gonna Need It，你不会需要它的）是源自极限编程（eXtreme Programming，XP）的一条原则：**程序员在真正需要某项功能之前，不应该去实现它**。XP 联合创始人 Ron Jeffries 将其概括为："总是等到你真正需要的时候才去实现，永远不要仅仅因为预见到将来可能需要就去实现。" 它要求只关注当前正在处理的故事（story），而不是想象中的未来需求。

## 核心概念

- **YAGNI 的定义**：不应在"确认必要"之前添加功能——不要实现当前用不到的东西。
- **出处**：源于极限编程（XP），是该方法论最著名的口号之一。
- **核心哲学**（Ron Jeffries）：Always implement things when you actually need them, never when you just foresee that you need them（总是等到真正需要时才实现，不要因为预见到需要就去实现）。
- **DTSTTCPW**：do the simplest thing that could possibly work（做能工作的最简单的事），YAGNI 是这条 XP 实践背后的原则。
- **配套实践**：持续重构（continuous refactoring）、持续自动化单元测试、持续集成——YAGNI 必须与它们配合使用。

## 工作机制

- **需求驱动实现**：只实现"当前故事"需要的功能，不为想象中的未来需求预写代码。
- **与 DTSTTCPW 协同**：YAGNI 是"做最简单可行之事"的支撑原则——既然不需要，就不去实现。
- **风险**：若脱离持续重构等配套实践单独使用，可能导致代码混乱与大规模返工，即所谓技术债（technical debt）。
- **依赖配套**：YAGNI 对配套实践的依赖是 XP 原始定义的一部分——它不是"不写代码"的借口，而是"在正确的时机写正确的代码"。

## 示例或代码

**YAGNI 反例**：为"将来可能支持多种数据库"提前抽象出完整的 ORM 适配层、插件注册表，而当前只用一个数据库。这些代码当下无人使用，还增加了维护成本。

**YAGNI 做法**：先针对当前数据库写直接可用的代码；当真的出现第二个数据库需求时，再用重构（而不是预先设计）引入抽象。

```text
# 不 YAGNI：为不存在的未来需求预埋
abstract class Storage { ... }          # 只有一个实现时就是过度设计
class ConfigurablePluginManager { ... } # 当前没有插件需求

# YAGNI：只实现现在需要的能力
class UserRepository { save(u); find(id); }  # 等真有多存储需求再重构抽象
```

**与其他实践配合**：YAGNI + 持续重构 + 持续集成——先写最简单的实现，靠重构演进设计，而不是一开始就设计得面面俱到。

## 常见误区

- **把 YAGNI 当成"不写文档/不做设计"**：YAGNI 针对的是"功能实现"，不是取消必要设计；它强调实现的时机而非否定思考。
- **以为 YAGNI 可以脱离重构单独使用**：没有持续重构配套，YAGNI 可能导致代码混乱与大量返工（技术债）。
- **把 YAGNI 与"不做任何预测"混为一谈**：XP 允许为当前故事做设计，只是不为"想象中的未来故事"实现功能。
- **与 DRY/KISS 的关系被误解**：YAGNI 与 [[dry]]、[[kiss]] 存在张力——DRY 鼓励抽象（但不能过早）、KISS 鼓励简单（不做多余设计），三者在"时机与权衡"上互补。
- **把 YAGNI 用于逃避必要的基础设施**：当前故事确实需要的能力（如基本的错误处理）仍要实现，YAGNI 不豁免真正的需求。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| yagni-definition | web-computer-science-yagni | YAGNI 源自 XP，主张确认必要之前不添加功能 |

## 待验证项

无。

## 关联知识

- [[dry]] —— 不要重复自己：抽象时机的对立面（不能为猜测的未来需求过早抽象）。
- [[kiss]] —— 保持简单：从"简单性"角度支持"不实现不需要的东西"。
- [[solid]] —— 面向对象设计原则。
- [[software-design]] —— 软件设计总览。
- [[refactoring-concepts-and-principles]] —— 重构：YAGNI 的配套实践，让设计随真实需求演进。
- [[four-rules-of-simple-design]] —— 简单设计四原则。

## 详细章节

### YAGNI原则

#### 定义

"You aren't gonna need it"（YAGNI）是一条源自极限编程（XP）的原则：程序员在真正需要之前，不应添加功能。短语的其他形式包括 "You aren't going to need it" 与 "You ain't gonna need it"。

XP 联合创始人 Ron Jeffries 对该哲学的解释是：

> Always implement things when you actually need them, never when you just foresee that you [will] need them.

即：总是等到你真正需要它们的时候才去实现，永远不要仅仅因为你预见到将来可能需要就去实现。这条口号提醒我们：始终只处理我们手中的故事（story），而不是处理我们"以为将来会需要"的东西。

#### 与 XP 实践的关系

YAGNI 是 XP 实践"do the simplest thing that could possibly work"（DTSTTCPW，做能工作的最简单的事）背后的原则。它应当与若干其他实践组合使用：

- 持续重构（continuous refactoring）
- 持续自动化单元测试（continuous automated unit testing）
- 持续集成（continuous integration）

如果脱离持续重构单独使用，YAGNI 可能导致代码混乱与大规模返工，也就是所谓的技术债（technical debt）。YAGNI 对配套实践的依赖，本身就是 XP 原始定义的一部分——它不是"只写最少的代码"这种孤立的偷懒法则，而是"在持续重构与测试保障下，只实现当下需要的能力"这一完整工作流的一环。

#### 实践意义

- 避免为想象中的未来需求预写功能，减少当下无用的代码量与维护面。
- 让设计通过"当前真实需求 + 持续重构"逐步演进，而不是一开始就假设未来。
- 与 DRY（不要重复自己）、KISS（保持简单）一起，构成一组互相制衡的设计原则：三者都关注"避免不必要的复杂度"，但切入点不同——DRY 关注知识的单一权威表示、KISS 关注简单性本身、YAGNI 关注实现时机。

## 参考

- Wikipedia — You aren't gonna need it: https://en.wikipedia.org/wiki/You_aren%27t_gonna_need_it
- Ron Jeffries, Ann Anderson, Chet Hendrickson — Extreme Programming Installed (2001)
- Martin Fowler, Kent Beck — Refactoring: Improving the Design of Existing Code (1999)
