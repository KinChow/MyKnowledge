---
aliases:
- 动作模式
- Command Pattern
confidentiality: public
domain: computer-science
evidence:
- claim: 命令模式是一种行为型设计模式，它用一个对象封装执行某个动作或稍后触发某事件所需的全部信息。
  claim_id: command-pattern-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-30fa1d2cc7b2
    exact: the command pattern is a behavioral design pattern in which an object is
      used to encapsulate all information needed to perform an action or trigger an
      event at a later time
  targets:
  - evidence_id: evidence-30fa1d2cc7b2
    source_id: web-computer-science-command-pattern
id: command-pattern
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-command-pattern
status: published
tags:
- design-pattern
- behavioral
- command
title: 命令模式
updated_at: '2026-09-06'
---
# 命令模式

## 一句话结论

命令模式把"一个动作或稍后触发的事件所需的全部信息"（方法名、拥有该方法的对象、方法参数）**封装进一个命令对象**，使请求的**发送者（调用者 Invoker）与接收者（Receiver）解耦**：调用者只面向命令接口，不关心命令如何执行；命令可以被存储、排队、延迟执行、撤销和重做。

## 核心概念

- **定义**：命令模式是一种行为型设计模式，用一个对象封装执行动作或稍后触发事件所需的全部信息（方法名、拥有方法的对象、方法参数值）。
- **四个角色**：命令（Command）、接收者（Receiver）、调用者（Invoker）、客户端（Client）。
- **封装请求**：把"请求"从"执行请求的类"中分离出来，类不再耦合于特定请求。
- **解耦调用者**：调用者只认识命令接口，不知道具体命令，也不关心请求如何被完成。
- **可配置/可延迟**：可在运行时配置对象以携带某个请求，命令可排队或稍后执行。

## 工作机制

- 客户端创建命令对象，把接收者（及参数）绑定进命令；命令调用接收者方法时由 `execute()` 触发。
- 调用者（Invoker）知道如何执行命令（并可选地记账），但只依赖命令接口，不依赖具体命令。
- 客户端决定把哪些命令交给哪个调用者、在何时执行。
- 执行时调用者调用命令的 `execute()`，命令内部调用接收者的方法完成实际工作。
- 由于请求被封装为对象，可被存储、参数化、排队、延迟、撤销/重做。

## 示例或代码

经典场景：文本编辑器的撤销/重做、GUI 按钮触发动作、任务队列。

Python 示意：

```python
class Light:                              # Receiver 接收者
    def on(self):
        print("Light ON")
    def off(self):
        print("Light OFF")

class Command:                            # Command 接口
    def execute(self): ...
    def undo(self): ...

class LightOnCommand(Command):            # ConcreteCommand
    def __init__(self, light: Light):
        self._light = light
    def execute(self):
        self._light.on()
    def undo(self):
        self._light.off()

class RemoteControl:                      # Invoker 调用者
    def __init__(self):
        self._history = []
    def set_command(self, cmd: Command):
        self._command = cmd
    def press(self):
        self._command.execute()
        self._history.append(self._command)
    def undo(self):
        if self._history:
            self._history.pop().undo()

# Client 组装
light = Light()
rc = RemoteControl()
rc.set_command(LightOnCommand(light))
rc.press()      # Light ON
rc.undo()       # Light OFF
```

## 常见误区

- **把命令模式等同于"回调"**：回调只是函数指针，命令对象还封装了接收者与参数、可支持撤销/排队等。
- **让调用者依赖具体命令**：这正是模式要避免的——调用者应只依赖命令接口。
- **在只有单个固定请求时强行使用**：没有"可配置/可延迟/可撤销"需求时，命令模式是过度设计。
- **忽略撤销/重做的契约**：若支持撤销，命令需同时维护可逆操作，否则撤销语义不完整。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| command-pattern-definition | web-computer-science-command-pattern | 命令对象封装动作/事件所需全部信息，调用者与接收者解耦、可配置可延迟 |

## 待验证项

无。英文定义直接来自 Wikipedia《Command pattern》条目，已锚定原文逐字引文。

## 关联知识

- [[memento-pattern]] —— 撤销/重做常与备忘录模式（保存状态快照）配合使用。
- [[observer-pattern]] —— 事件驱动系统中命令可作为通知/派发的内容。
- [[chain-of-responsibility-pattern]] —— 命令对象可作为责任链中被传递处理的请求载体。
- [[software-design]] —— 行为型模式在 23 种 GoF 模式中的定位。

## 详细章节

### 定义

在面向对象编程中，命令模式是一种行为型设计模式：用一个对象封装"执行某个动作或稍后触发某个事件所需的全部信息"。这些信息包括方法名、拥有该方法的对象以及方法参数的值。

命令模式的四个术语总是被同时提及：命令（Command）、接收者（Receiver）、调用者（Invoker）和客户端（Client）。命令对象认识接收者并调用接收者的方法；接收者方法的参数值存储在命令中；接收者对象通过聚合被存入命令对象。调用 `execute()` 时，接收者才真正完成工作。调用者知道如何执行命令，并可对命令执行做记账，但它不认识具体命令，只认识命令接口。

命令模式是 23 个著名 GoF 设计模式之一。它解决的典型问题：避免"调用者与特定请求耦合"（即避免硬编码请求）、允许用某个请求配置对象。把请求硬编码进类里是僵化的，因为它把类在编译期耦合到某个特定请求，无法在运行时指定请求。

### 参与者

- **Command（命令接口）**：声明执行操作的接口（通常为 `execute()`，可选 `undo()`）。
- **ConcreteCommand（具体命令）**：实现接口，绑定接收者对象与动作、参数；`execute()` 内调用接收者的方法。
- **Receiver（接收者）**：真正执行请求所对应业务逻辑的对象。
- **Invoker（调用者）**：持有命令对象、触发其执行，并可做执行记账；只依赖命令接口。
- **Client（客户端）**：创建具体命令、把接收者绑定进命令、把命令交给调用者，并决定执行时机。

### 结构

- 调用者聚合命令接口；命令聚合接收者。
- 客户端装配：决定给命令分配哪些接收者、给调用者分配哪些命令。
- 执行流程：客户端把命令交给调用者 → 调用者调用 `execute()` → 命令调用接收者的方法。
- 因请求被封装成对象，命令可在数据结构中存储、在队列中排队、延迟执行或合并成批。

### 适用场景

- 需要把请求参数化为对象：把动作作为可传递、可存储的实体。
- 需要支持撤销/重做、事务、日志、任务排队、宏命令等。
- 需要在不同时间调用同一请求（延迟执行）。
- 需要将"发起请求"与"执行请求"解耦，便于测试与替换。

### 优缺点

优点：

- 发送者与接收者完全解耦，调用者只依赖命令接口。
- 符合开闭原则：新增命令无需修改现有类。
- 请求可被存储、排队、延迟、撤销/重做、日志化。
- 便于实现宏命令（组合命令）。

缺点：

- 每类请求都要一个命令类，类数量膨胀。
- 命令对象会额外持有接收者与参数，增加一层间接。

### 与相关模式关系

- **与备忘录模式**：撤销（undo）可用备忘录保存状态快照实现"状态回滚"，命令模式则负责"操作回滚"。
- **与观察者模式**：命令可作为事件驱动系统中被派发/通知的内容。
- **与责任链模式**：命令对象是责任链中沿链传递、由某个处理器处理的"请求"。
- **与组合模式**：宏命令由多个子命令组合而成，是组合模式在命令上的应用。

## 参考

https://en.wikipedia.org/wiki/Command_pattern
