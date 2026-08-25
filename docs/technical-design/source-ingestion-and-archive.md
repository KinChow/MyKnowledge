# Source 导入与归档实现设计

- 状态：Draft
- 相关 Feature：F001
- 相关规范：SRC、ARC、SEC
- 相关 ADR：ADR-0001、ADR-0003
- 相关验收：[F001](../acceptance/F001-source-ingestion.md)

## 目标与非目标

目标是实现 URL、local-file 和 personal-note 三类来源的统一导入、来源完备性校验、文本归档和 hash 生成。本阶段不实现批量历史迁移和 Private Vault。

## 模块边界

- `source_parser`：解析输入和 front matter；
- `archive_source`：抓取、快照、压缩和 hash；
- `source_validator`：确定性规则校验；
- `operation_store`：保存 preview/apply 状态。

## 流程与失败处理

解析来源 → 获取正文 → 保存 text 快照 → 按需保存 raw → 计算 hash → schema 校验 → 生成 Preview。

抓取失败、来源不完整或 raw 的 LFS 前置检查失败时，不得产生可发布 Source；允许的 text-only 降级必须记录原因。

## 测试策略

覆盖三类来源、抓取失败、重复导入、空正文、locator、hash 稳定性和 raw LFS 检查。

## 未决问题

离线 HTML/PDF 副本是否统一通过 `local-file` 通道导入，需要在实现前确认并写回系统规范。
