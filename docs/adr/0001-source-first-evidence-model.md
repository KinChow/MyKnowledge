# ADR-0001：Source-first 与证据模型

- 状态：Accepted
- 日期：2026-08-25
- 相关规范：SYS、SRC、EVD
- 相关 Feature：F001、F002、F003

## 背景

知识内容需要可追溯，不能由模型直接生成无来源 Wiki。

## 候选方案

- 直接编辑 Wiki；
- 先保存 Source，再由 Claim/Evidence 映射生成 Wiki；
- 依赖外部搜索摘要作为来源。

## 决策

采用 Source-first：Source 保存来源和证据边界，Wiki 的可验证 Claim 显式绑定 Evidence，经过验证和用户确认后才可发布。

## 后果

写入链路更长，但内容可审计、可失效和可重验证。

## 重新评估条件

无法为主要知识类型稳定保存来源，或证据门禁严重阻碍个人笔记写入时重新评估。
