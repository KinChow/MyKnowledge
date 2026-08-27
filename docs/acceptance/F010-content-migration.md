# F010 存量内容迁移和质量清理验收

- Feature：F010
- 相关规范：MIG、SRC、WIKI、EVD
- 状态：Implemented（2026-08-28；inventory 基础能力，Source-first 迁移尚未完成）
- 实现证据：`tools/inventory_legacy.py`、`tools/migrate_legacy.py`、`tests/test_inventory.py`、`tests/test_migration.py`
- 当前边界：已生成只读 Source-first migration preview、草稿目标和 route map；尚未执行真实 source/wiki 写入、证据绑定、route 修复和 rollback 演练。

## 本轮证据（2026-08-28）

- AC-F010-001/002：`tests/test_migration.py::test_migration_preview_is_source_first_and_does_not_write` 验证 preview 同时生成 source/wiki 稳定目标、`pending_manual_review`、`evidence_state: pending` 和 `writes_applied: false`，且原 `docs/` 文件字节不变。
- AC-F010-003：`test_migration_preview_changes_with_input_tree` 验证输入正文变化会改变 preview hash，避免复用旧迁移结果。

## 代表性样本增量证据（2026-08-27）

- AC-F010-002/003：`tests/test_migration.py::test_representative_sample_applies_source_then_draft_wiki` 验证样本先经 local-file Source preview/apply，再由 WriteOperation 写入 `status: draft` Wiki；`test_sample_apply_missing_item_is_fail_closed` 验证未知输入不会写入。原 `docs/guide.md` 保持不变，迁移结果不含绝对路径。

当前证据只覆盖确定性 preview 和回滚前置边界；真实抽取、evidence replay、链接修复及发布切换仍待人工/集成验收。

本轮链接修复增量：`tests/test_migration.py::test_sample_apply_repairs_only_inventory_links_and_reports_unresolved` 验证已知 legacy link 重写到稳定 route，unresolved link 进入报告，外部 URL 保持不变；修复只发生在 draft Wiki。

## 多媒体输入增量证据（2026-08-27）

- inventory 现纳入 `.md/.html/.htm/.txt/.pdf`，记录 `media_type`、输入字节 hash/长度和建议 extractor；PDF 不按文本解码，避免二进制污染 inventory。
- `apply_sample` 根据媒体类型复用 `TextExtractor`：HTML 走 Trafilatura、PDF 走 pypdf、文本走 UTF-8；extractor 缺失或失败时由 Source preview 返回结构化 blocked，不绕过 Source 门禁。
- 边界：Office/Docling、全量 evidence replay 和最终发布切换仍待后续验收。

## DOCX 抽取边界增量证据（2026-08-27）

- `tests/ingest/test_extractor.py::ExtractorTests::test_docx_extractor_does_not_fallback_to_binary_text` 验证 DOCX 不会按 UTF-8 fallback；Docling 缺失时明确返回 `extractor_unavailable:docling`。
- inventory 已记录 DOCX 的 `media_type` 与 `docling` extractor，依赖安装后才允许进入结构化抽取；当前环境未将 Docling 作为强制运行依赖。

CLI 增量证据：`tests/test_migration.py::test_migrate_cli_applies_confirmed_sample` 验证 CLI 复用同一 preview/confirm/apply 实现并返回结构化 `applied`。

## 幂等性增量证据（2026-08-27）

- `tests/test_migration.py::test_reapplying_sample_is_idempotent_and_does_not_duplicate_objects` 验证同一输入重复确认迁移时，Source/Wiki 文件字节保持一致且不会生成重复对象；输入 tree hash 变化仍会生成不同 preview hash。该证据不替代跨 Vault rollback 演练。

## 批量迁移增量证据（2026-08-30）

- `tests/test_migration.py::test_batch_requires_confirmation_then_applies_each_item_and_replays` 验证批量入口在未确认时不写入；确认后逐项通过 Source-first writer，两个样本均完成，并以 `migration-batch/v1` durable record 重放而不重复写入。
- `tests/test_migration.py::test_batch_unknown_item_is_fail_closed_without_writes` 验证批次包含未知 legacy path 时在任何写入前返回 `legacy_item_not_found`。
- `tests/test_migration.py::test_migrate_cli_batch_uses_confirmation_gate` 验证 `tools.cli migrate --apply-batch` 与领域批量服务共享确认门，未确认不写入，确认后完成迁移。
- 该证据闭合 AC-F010-001/002 的批次编排子场景；全量抽取、evidence replay、最终 projection 切换和 rollback 演练仍待完成，F010 仍为 Implemented（部分）。

## Preview hash confirmation 增量证据（2026-08-27）

- `apply_batch(..., expected_preview_sha256=...)` 在确认写入前重新生成 inventory/route plan；hash 与用户预览不一致时返回 `input_changed`，不调用 Source/Wiki writer，也不产生半成品。
- `tests/test_migration.py::test_batch_preview_hash_binding_blocks_changed_input_without_writes` 覆盖 preview 后修改 legacy 输入的 fail-closed 门禁。

## 受控 rollback 增量证据（2026-08-27）

- `rollback_sample()` 只从自校验 migration record 定位 Source/Wiki 生成物，保存完成时 `output_hashes`，并通过 `WriteOperation` 的 preview/confirmation/before-hash/lock 路径执行 purge；不直接删除目录或执行 Git reset。
- `tests/test_migration.py::test_rollback_sample_requires_confirmation_and_preserves_legacy_and_snapshot` 验证未确认不写、确认后仅移除生成的 Source/Wiki，原 `docs/` 与 content-addressed archive 保留，rollback record 可重放。
- `tests/test_migration.py::test_rollback_sample_blocks_output_drift_without_deleting_user_change` 验证迁移后用户编辑导致 `migration_output_changed`，文件保持不变。
- `tests/test_migration.py::test_migrate_cli_rollback_uses_confirmation_and_preserves_legacy` 验证 CLI rollback 复用同一确认门，未确认不删除，确认后只移除迁移产物且保留 legacy 输入。
- 该证据闭合 AC-F010-003 的单样本 rollback 子场景；全量迁移、最终 projection 切换和跨批次环境演练仍待完成。

- 本轮 durable replay：首次 sample apply 成功后写入 owner-local `audit/migrations/<migration_key>.json`（`migration-record/v1`）；相同 `legacy_path + body_sha256 + migration_version` 再次执行直接返回 `replayed: true`，不重复调用 Source/Wiki writer。`tests/test_migration.py::test_reapplying_sample_is_idempotent_and_does_not_duplicate_objects` 同时验证记录只生成一份。输入 hash 变化会使用新 key 并重新走门禁。
- replay 完整性增量：迁移记录带 `record_sha256` 并原子落盘；`tests/test_migration.py::test_tampered_migration_record_is_not_replayed` 篡改结果后验证不会返回 `replayed: true`，而是重新经过 Source-first 流程。

## 稳定 ID 冲突增量证据（2026-08-27）

- `tests/test_migration.py::test_migration_preview_blocks_normalized_id_collision_before_writes` 验证规范化路径产生相同 Wiki ID 时，preview 输出 `stable_id_collision` 并将冲突项标为 blocked；确认 apply 在任何 Source/Wiki 写入前拒绝，不按输入顺序覆盖对象。

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
- 对应测试：`tests/test_migration.py::test_sample_apply_repairs_only_inventory_links_and_reports_unresolved`；已知链接会重写，unresolved 链接保留并记录，原 `docs/` 不变。
