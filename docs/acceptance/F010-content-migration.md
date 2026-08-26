# F010 存量内容迁移和质量清理验收

- Feature：F010
- 相关规范：MIG、SRC、WIKI、EVD
- 状态：Implemented（2026-08-28；inventory 基础能力，Source-first 迁移尚未完成）
- 实现证据：`tools/inventory_legacy.py`、`tests/test_inventory.py`
- 当前边界：已生成只读 Source-first migration preview、草稿目标和 route map；尚未执行真实 source/wiki 写入、证据绑定、route 修复和 rollback 演练。

## 本轮证据（2026-08-28）

- AC-F010-001/002：`tests/test_migration.py::test_migration_preview_is_source_first_and_does_not_write` 验证 preview 同时生成 source/wiki 稳定目标、`pending_manual_review`、`evidence_state: pending` 和 `writes_applied: false`，且原 `docs/` 文件字节不变。
- AC-F010-003：`test_migration_preview_changes_with_input_tree` 验证输入正文变化会改变 preview hash，避免复用旧迁移结果。

当前证据只覆盖确定性 preview 和回滚前置边界；真实抽取、evidence replay、链接修复及发布切换仍待人工/集成验收。

## AC-F010-001 迁移清单与状态边界

- Given：现有 docs 内容；
- When：生成迁移清单；
- Then：每个文件有 source/wiki 目标、证据状态、目标 Vault、route、`body_sha256`、输入 tree hash、classifier/threshold 版本和 completed/pending 状态；
- 失败时不变量：没有来源的内容不得自动标记 published。
- 自动化级别：Repository/Integration（清单生成）；`content_verdict` 和最终发布为 Manual review。
- 对应测试：`tests/test_inventory.py::test_inventory_has_tree_hash_and_pending_boundaries`；当前状态：通过。

## AC-F010-002 代表性样本迁移

- Given：包含网络 URL、local-file HTML/PDF、个人笔记、无来源和冲突来源的样本；
- When：执行迁移；
- Then：统一进入 Source → snapshot → evidence → Wiki 流程，local-file 记录 file hash 和 extractor 信息；
- 失败时不变量：不改写原 public 内容，不绕过验证门禁。
- 自动化级别：Integration/Manual review。

## AC-F010-003 链接与回滚

- Given：存在 unresolved internal Markdown links；
- When：生成 route map 和修复报告；
- Then：每条链接标记已修复/待人工处理，迁移失败可保留旧 public dist 和 canonical 内容；
- 失败时不变量：不得删除无法解释的旧对象。
- 自动化级别：Repository/Integration。
