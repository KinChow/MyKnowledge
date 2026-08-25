# ADR-0002：公开仓库与 Private Vault

- 状态：Accepted
- 日期：2026-08-25
- 相关规范：SEC、SYS
- 相关 Feature：F007、F011

## 背景

当前仓库是公开仓库，Source、Wiki、题目和归档都可能随 Git 发布。

## 决策

统一在 Source、Wiki、Question 上声明 confidentiality，非公开对象不得进入公开构建。第一阶段只实现 Private Vault 契约，不挂载私有存储。

## 后果

公开仓库的 leak gate 必须覆盖所有输入和生成物，而不能只扫描 dist。

## 重新评估条件

出现第一份非公开资料，或私有数据需要本地完整工作流时启动 Private Vault 实现。
