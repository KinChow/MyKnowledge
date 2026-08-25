# 规范到验收追踪矩阵

本文是索引，不是新的规范来源。完整约束以
[系统设计规范](./myknowledge-system-design.md) 为准。

## ID 约定

| 前缀 | 范围 |
| --- | --- |
| SYS | 系统不变量 |
| SRC / ARC | Source 与原文归档 |
| WIKI / EVD | Wiki、Claim、Evidence |
| VAL | 确定性和 LLM 验证 |
| OPS | 写操作协议 |
| IDX / API / WEB | 索引、后端和公开站 |
| QST / SKILL / MIG / SEC | 题目、Agent、迁移和保密 |

## P0 基线

| 规范 ID | Feature | ADR | 实现设计 | 验收 | 测试 | 状态 |
| --- | --- | --- | --- | --- | --- | --- |
| SRC-001 | F001 | ADR-0001 | source-ingestion | AC-F001-001/002 | 待实现 | Designed |
| ARC-001 | F001 | ADR-0003 | source-ingestion | AC-F001-003 | 待实现 | Designed |
| WIKI-001 | F002 | ADR-0001 | wiki-claim-validation | AC-F002-001 | 待实现 | Designed |
| EVD-001 | F003 | ADR-0001/0005 | wiki-claim-validation | AC-F003-001/002 | 待实现 | Designed |
| VAL-001 | F003 | ADR-0005 | wiki-claim-validation | AC-F003-003 | 待实现 | Designed |
| OPS-001 | F004 | ADR-0006 | write-operation-and-locking | AC-F004-001/002 | 待实现 | Designed |

## 完整性要求

- 每条 `必须` 级规范至少映射一个 Feature 和一个验收场景。
- 每个 P0 Feature 必须有 Technical Design 和 Acceptance。
- 每个验收场景必须关联自动化测试或明确的人工验证方式。
- 本矩阵中的状态不能替代验收证据。
