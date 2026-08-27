# F004 写操作验收

- Feature：F004
- 相关规范：OPS、SEC
- 状态：Implemented（2026-08-28；确认事件绑定、并发一致性、真实 projection 重建已补齐；跨 Vault staging 与领域 writer 统一迁移仍待后续验收）
- 实现证据：`tools/write_operation.py`、`tools/operation_store.py`（`validate_apply_confirmation`）、`tools/vault_lock.py`、`tests/test_write_operation.py`（31 项）
- 当前边界：Source/Evidence 既有 writer 尚未统一迁移到通用 writer；跨 Vault apply/恢复、SQLite index 生产重建仍需后续验收。

## Rename source precondition 增量证据（2026-08-27）

- `WriteOperation.rename()` 记录源文件 `source_before_hash`；Apply 在锁内先校验源 hash，再写目标和删除源。
- `tests/test_write_operation.py::WriteOperationTests::test_rename_source_drift_blocks_without_deleting_source` 验证 Preview 后源文件被用户修改时返回 `hash_mismatch`，源内容保留且目标不存在。

## 路径竞态增量证据（2026-08-30）

- `tests/test_write_operation.py::WriteOperationTests::test_apply_path_race_returns_structured_failure` 在 Preview 后把父目录替换为 symlink，验证 Apply 回滚、返回 `expired/apply_failed` 与 `path_symlink` 诊断，且 symlink 指向目录没有被写入。
- 本轮增量：已增加 Vault fencing sidecar 与提交点校验；多 Vault 锁排序、projection/index 恢复和 retire 领域状态仍需后续验收。

## 本轮证据（2026-08-29）

- AC-F004-010：`tests/test_write_operation.py::WriteOperationTests::test_fencing_token_rejects_replaced_owner` 验证 owner sidecar 被替换后 `assert_owner()` 返回 `LockBusyError`，旧持有者不能继续提交。
- AC-F004-005：全量 `tests/test_write_operation.py` 仍通过多文件失败回滚，fencing 检查位于每次文件替换之前。
- AC-F004-007/009：`tests/test_write_operation.py::WriteOperationTests::test_tampered_durable_audit_blocks_apply` 验证篡改 `audit/operations` 后 Apply 在写入前返回 `hash_mismatch`，目标文件保持不存在。

- AC-F004-010：`tests/test_write_operation.py::WriteOperationTests::test_stale_lock_recovery_requires_free_kernel_lock_and_writes_audit` 验证释放内核锁后恢复 orphan owner sidecar 并写入 `lock-recovery` 审计；`test_stale_lock_recovery_does_not_break_live_lock` 验证活锁返回 `lock_busy`。

- AC-F004-008：`tests/test_write_operation.py::WriteOperationTests::test_multi_vault_lock_group_orders_and_releases_all` 验证多 Vault 去重并按稳定顺序获取/逆序释放；`test_multi_vault_lock_group_releases_acquired_locks_on_failure` 验证第二把锁失败时第一把锁立即释放，不留下 owner sidecar。

## AC-F004-001 未确认不得 Apply

- Given：存在 Preview 但没有用户确认；
- When：执行 Apply；
- Then：操作被拒绝且目标文件不变；
- 自动化级别：Integration。
- 对应测试：`tests/test_write_operation.py::WriteOperationTests::test_preview_is_read_only_and_apply_requires_confirmation`
- 当前状态：通过。

## AC-F004-002 重复 Apply 幂等

- Given：同一 operation 已成功 Apply；
- When：重复执行 Apply；
- Then：返回原结果，不产生重复对象或损坏索引；
- 自动化级别：Integration。
- 对应测试：`tests/test_write_operation.py::WriteOperationTests::test_apply_is_idempotent`
- 当前状态：通过。

## AC-F004-003 并发写入保持一致

- Given：两个写操作同时获取仓库写锁；
- When：并发执行；
- Then：只有一个持有锁，另一个可重试或明确失败，仓库不出现半成品；
- 自动化级别：Integration。
- 对应测试：`tests/test_write_operation.py::ConcurrentApplyTests::test_two_concurrent_applies_produce_single_consistent_result`
- 当前状态：通过。

## AC-F004-004 blocked 与 hash 失效

- Given：Preview 缺少来源、Vault/provider 不可用，或 Apply 前输入/registry hash 发生变化；
- When：执行 Apply；
- Then：操作进入 `blocked` 或 `expired`，目标文件、索引和旧 projection 保持不变，并返回可执行的 `next_action`；
- 失败时不变量：不得留下可自动续写的半成品或把 blocked 当作成功；
- 自动化级别：Unit/Integration。
- 对应测试：`test_hash_change_blocks_without_overwrite`、`test_rename_source_drift_blocks_without_deleting_source`、`test_apply_path_race_returns_structured_failure`、`ApplyConfirmationTests::test_confirmation_wrong_hash_fails_closed_without_writes`
- 当前状态：通过。

## AC-F004-005 原子多文件 Apply 与恢复

- Given：rename/move/retire/purge 或多 Vault operation 在写临时文件或索引阶段中断；
- When：注入进程崩溃、跨设备 staging 或单 Vault Apply 失败；
- Then：同一文件系统内要么全部原子完成，要么旧文件/旧索引保持不变；跨 Vault 失败保留 staging、成功列表和恢复说明，不自动回滚用户变更；
- 失败时不变量：不产生半写文件、静默覆盖或伪造全局事务成功；
- 自动化级别：Failure injection/Integration。

## AC-F004-006 确认事件绑定

- Given：存在同一 operation 的 `operation-confirmation/v1` 事件与 precondition hashes；
- When：执行 Apply 或重复消费事件；
- Then：只有 `actor_type: human`、`scope` 合法且 hash 完全匹配时成功；事件只消费一次，hash 变化后必须重新 preview；
- 失败时不变量：Agent/LLM/CI 不能自行生成确认或把 `public_release` 改为 true；
- 自动化级别：Security/Integration。
- 对应测试：`ApplyConfirmationTests`（成功绑定/伪造 hash/agent actor/幂等消费）
- 当前状态：通过。

## AC-F004-007 Durable record 与一次性 nonce

- Given：Apply 使用 `operation-confirmation/v1` 与当前 precondition hashes；public release 另用带一次性 nonce 的 `public-release-confirmation/v1`；`state/` 可被清理；
- When：完成 Apply、重复消费事件，或删除临时 state 后重新检查；
- Then：owner vault 的 `audit/operations/<operation_id>.json` 保留结果、event hash 和 after hashes，public release 另存 nonce 的 `consumed_at`；重复消费返回原结果，不能再次写入；
- 失败时不变量：不能仅凭 state/log 声称已确认；不能复用 public release nonce；durable record 缺失时不得生成 publishable projection；apply 与私有发布不得引入一次性 nonce——hash 绑定已挡住重放；
- 自动化级别：Repository/Integration/Security。

## AC-F004-011 确认事件 3 → 2 合并后的边界

- Given：确认事件只有 `operation-confirmation/v1`（`scope: apply | publish_private`）与 `public-release-confirmation/v1`；分别构造：缺 `content_sha256`/`evidence_sha256`/`target_vault` 的 `scope: publish_private`、缺 `warning_code`/`warning_text_sha256` 的 internal 私有发布、`scope: public_release`、以及用 `operation-confirmation/v1` 冒充 public release；
- When：校验事件并执行 Apply / public release；
- Then：前两种按缺字段拒绝；`public_release` 不是合法 scope 值，词表校验直接拒绝；public release 只接受 `public-release-confirmation/v1`；
- 失败时不变量：**public release 不得被表达为 `operation-confirmation/v1` 的任何 scope 值**——它是唯一不可撤销的对外行为，独立事件类型使"写错一个 scope 值就公开了 internal 内容"在 schema 层不可表达；internal 告警确认虽已并入私有发布事件，仍必须展示且不可静默跳过；
- 自动化级别：Unit/Security。
- 对应测试：`ConfirmationBoundaryTests` + `tests/test_release_confirmation.py::test_public_release_rejects_operation_confirmation_masquerade`
- 当前状态：通过。

## AC-F004-008 多 Vault 锁顺序

- Given：operation 同时涉及两个或更多 Vault，另一个 operation 以不同输入顺序并发执行；
- When：获取锁并 Apply；
- Then：所有 operation 按排序后的 `vault_id` 获取 `state/locks/<vault_id>.lock`，不会死锁；失败保留 staging 和成功列表；
- 失败时不变量：不得静默覆盖、跨设备伪原子替换或伪造全局事务成功；
- 自动化级别：Integration/Failure injection。

## AC-F004-009 Canonical 提交与索引失败恢复

- Given：单 Vault operation 已通过最终校验，但 projection/index 写入阶段被故障注入中断；或进程在 commit-intent 与 commit marker 之间退出；
- When：重启 writer/recovery 并执行同一 operation 的状态查询；
- Then：无 marker 时按 intent 恢复旧 canonical 文件，有 marker 时保留新 canonical 文件并重建 projection；在索引恢复前状态为 `applied_index_pending`，不生成新的 `public_publishable`，恢复完成后追加不可变 `applied` record；
- 失败时不变量：不能留下半写文件、静默覆盖用户修改、把旧 projection 当成新内容，或重复消费 confirmation nonce；
- 自动化级别：Failure injection/Recovery。

## AC-F004-010 陈旧锁恢复与 fencing token

- Given：writer 持有某 Vault 锁后进程挂起或退出，另一个进程执行显式 `lock recover`，旧进程随后尝试继续写入；
- When：恢复锁、重试 commit-intent/canonical/projection 替换和释放；
- Then：恢复动作先检查 PID/进程启动时间并写入 `lock-recovery` durable audit；新锁生成新的 `lock_token`，旧进程在任一提交点因 token 不匹配被拒绝；默认不按超时自动删除；
- 失败时不变量：不能出现双写、静默覆盖、误删新锁或把未审计的恢复当作成功；
- 自动化级别：Security/Integration/Failure injection。

## Commit-intent 恢复增量证据（2026-08-27）

- `test_failed_apply_keeps_intent_for_explicit_recovery` 验证多文件 apply 故障回滚后不会静默删除 commit-intent；旧 canonical 保持不变，显式 `recover()` 返回 `recovery_required`，等待人工/上层决定继续或重做。

- `test_commit_intent_is_removed_after_apply` 验证正常 Apply 在 durable applied record 写入后清理临时 intent。
- `test_recover_commit_intent_marks_fully_written_files_applied` 验证进程在文件写完但 applied record 尚未落盘时，恢复检查按 after hash 重建 applied 状态；hash 不完整时返回 `recovery_required`，不覆盖用户文件。
- 边界：projection/index 重建与跨 Vault staging 仍待后续验收，F004 仍为 Implemented（部分）。

## Projection/index pending 恢复增量证据（2026-08-30）

- `tests/test_write_operation.py::WriteOperationTests::test_projection_failure_keeps_canonical_and_recovers` 注入 projection rebuild 失败，验证 canonical 文件已原子完成、operation 状态为 `applied_index_pending`、返回 `projection_failed`/`recover_projection`，不会伪造完整 `applied`。
- 使用同一 operation 显式 `recover()` 重跑 rebuild 后，状态才变为 `applied`，commit-intent 被清理；无 rebuild hook 时返回 `projection_rebuilder_unavailable`，不猜测恢复结果。
- 该增量闭合 AC-F004-009 的通用 writer 状态边界；真实 public projection/index 生产重建和跨 Vault staging 仍为环境级 pending。

## Commit intent 完整性增量证据（2026-08-27）

- `commit-intent/v1` 现在包含 canonical `intent_sha256`，覆盖 operation、vault 及每个文件的 before/after hash；`WriteOperation.recover()` 在恢复前校验自哈希、operation_id 和 target vault。
- `tests/test_write_operation.py::WriteOperationTests::test_recover_rejects_tampered_commit_intent` 验证 intent 被篡改时返回 `recovery_invalid`，不会把未验证状态标记为 applied；`test_recover_commit_intent_marks_fully_written_files_applied` 验证完整 intent 仍可重放。

## Retire marker 增量证据（2026-08-27）

- `test_rename_and_retire_have_distinct_operation_types` 现在执行 retire Apply，并验证 owner Vault 生成 `audit/retire/<operation_id>.json`（`retire-marker/v1`、目标相对路径和内容 hash）。原文件保留，便于回放和恢复，不执行不可逆删除。
- 边界：purge、projection/index 消费 retired 状态及跨 Vault staging 仍待后续验收。

## Symlink/hard-link target 增量证据（2026-08-27）

- `tests/test_write_operation.py::WriteOperationTests::test_symlink_and_hardlink_targets_are_rejected` 验证 preview 阶段拒绝仓库内 symlink 和共享 inode hard-link；apply 阶段也会再次检查 hard-link，避免路径或 inode 竞态绕过原子写入边界。

## Purge 备份前置证据（2026-08-27）

- `test_purge_requires_verified_owner_backup` 验证未达到 owner Vault `backup_state=verified` 时，`purge()` 返回 `backup_not_verified`，目标文件保持不变。
- Apply 仅接受通过该前置创建的 `purge` operation；删除前仍在锁内复查 hash，失败回滚恢复原文件。外部 target 未配置时不会伪造 verified。

## Private Vault 路径绑定增量证据（2026-08-30）

- `WriteOperation.preview/apply/recover/rename/retire/purge` 现在将文件路径和 `vault_id` 绑定到同一 owner checkout；private operation 不再把相对路径解析到 public root。
- `tests/test_write_operation.py::test_private_vault_write_uses_owner_checkout_root` 验证 private 文件只写入 private checkout，public checkout 不出现同名目标；现有 public 故障注入和回滚测试仍保持通过。

## 确认事件与验收补齐（2026-08-28）

- AC-F004-006：`OperationStore.validate_apply_confirmation`（`tools/operation_store.py`）实现 `operation-confirmation/v1` 严格校验——`actor_type` 必须为 `human`、scope ∈ {apply, publish_private}、`input_hash`/`diff_hash` 与当前 operation 完全绑定、`event_sha256` canonical 复核；`WriteOperation.apply(confirmation=...)`、Skill `write_apply` 与 API `/api/operation/{id}/apply` 均透传消费。`ApplyConfirmationTests` 验证成功路径（durable audit 记录事件 hash）、伪造 hash fail-closed 不写目标、agent actor 拒绝；重复消费由状态机幂等返回原结果。
- AC-F004-011：`ConfirmationBoundaryTests` 验证 `public_release` 不是合法 scope（schema 层不可冒充）；`publish_private` 缺 `content_sha256`/`evidence_sha256`/`target_vault` 时拒绝；`tests/test_release_confirmation.py::test_public_release_rejects_operation_confirmation_masquerade` 验证 public release 只接受 `public-release-confirmation/v1`。
- AC-F004-003：`ConcurrentApplyTests` 以双进程并发 apply 同一目标，验证恰好一个 `applied`、其余为结构化 `expired/blocked`（无 `apply_failed` 半成品），目标文件为单一完整内容。
- AC-F004-009（真实重建）：`WriteOperation` 对 public vault 默认挂接 `public_projection_rebuilder`（真实调用 `PublicProjectionGenerator`）；`RealProjectionRebuildTests` 验证 apply 后 manifest 落盘、注入写入障碍后进入 `applied_index_pending`、清除障碍后显式 `recover()` 完成重建并落 `applied`。SQLite index 生产重建留待 F005 接线。
- 边界：本地交互通道（CLI/本地 API）的裸 `confirmed` 标志仍表示"操作者在场确认"；非交互 Agent 通道建议随 apply 提供 `confirmation` 事件作为人工确认凭据。跨 Vault staging、Source/Evidence writer 统一迁移仍待验收。

## 真实 checkout 端到端演练证据（2026-08-28，commit eb5c214）

在真实 MyKnowledge checkout 上执行完整链路（sandbox 文件 `wiki/f004-drill.md`，演练后 rename 至 gitignore 的 `state/` 清理）：

- Preview：`op_26e72ba31676404d90e0c46d5a729a4f` → `previewed`；
- 伪造 `input_hash` → `blocked/confirmation_hash_mismatch`，目标文件未创建；`actor_type: agent` → `blocked/confirmation_actor_invalid`；
- 携带 human 确认事件 apply → `applied`，durable audit（`audit/operations/op_26e72...json`）记录 `event_sha256: sha256:7126a1d3...b2`；
- 重复 apply → 与首次结果逐字段相等（幂等）；
- public projection 真实重建：`queries/public/manifest.json` 由手写 `bootstrap-empty-v1` 占位符替换为生成器输出（`sha256:3c7ed791...a4`），items 为空（当前无已发布 wiki，符合预期）；
- 清理 rename 同链路 apply 成功，`wiki/` 无残留。
- 剩余 `Accepted` 阻断不变：跨 Vault staging、领域 writer 统一迁移、SQLite index 生产重建（F005）。

## 复审修复（2026-08-28）

- F-1（状态翻转缺陷）：applied 之后的 commit-intent 清理失败不再把 operation 翻回 `expired/apply_failed`，改为保持 `applied` 并在结果暴露 `warnings: [intent_cleanup_failed]`（`WriteOperation._finalize` / `_cleanup_intent_after_applied`）。对应测试：`ReviewFixTests::test_intent_cleanup_failure_keeps_applied_state_with_warning`。
- F-2（契约收紧）：`operation-confirmation/v1` 的 `event_sha256` 必填且必须匹配 canonical hash，durable audit 中的确认事件始终可独立复核。对应测试：`ReviewFixTests::test_confirmation_without_event_sha256_is_rejected`。
