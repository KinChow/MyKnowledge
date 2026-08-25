# 写操作与锁实现设计

- 状态：Draft
- 相关 Feature：F004
- 相关规范：OPS、SEC
- 相关 ADR：ADR-0006
- 相关验收：[F004](../acceptance/F004-write-operation.md)

## 目标与非目标

目标是实现 Preview → 用户确认 → Apply、幂等、仓库级锁、原子落盘、rename/move 和废弃操作。本阶段不实现 Agent Skill UI。

## 核心流程

生成规范化 operation → 保存 Preview → 用户确认 → 获取写锁 → 校验输入和前置 hash → 写临时文件 → 原子替换 → 更新 operation 状态。

## 失败处理

任何前置条件失败都不写入目标对象；中途失败必须可恢复，不能留下可发布半成品；重复 operation 返回既有结果。

## 测试策略

覆盖未确认 Apply、重复 Apply、hash 冲突、并发写入、进程中断、移动和废弃。

## 未决问题

锁文件格式、跨进程超时和恢复命令在代码实现前确定。
