# F004 写操作验收

- Feature：F004
- 相关规范：OPS、SEC
- 状态：Implemented（2026-08-27；7 个通用 writer 测试通过；完整领域 writer 验收仍待后续补齐）
- 实现证据：`tools/write_operation.py`、`tests/test_write_operation.py`、`tools/operation_store.py`、`tools/vault_lock.py`
- 当前边界：Source/Evidence 既有 writer 尚未统一迁移到通用 writer；多 Vault fencing、projection/index 恢复和 retire 领域状态仍需后续验收。
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

## AC-F004-004 blocked 与 hash 失效

- Given：Preview 缺少来源、Vault/provider 不可用，或 Apply 前输入/registry hash 发生变化；
- When：执行 Apply；
- Then：操作进入 `blocked` 或 `expired`，目标文件、索引和旧 projection 保持不变，并返回可执行的 `next_action`；
- 失败时不变量：不得留下可自动续写的半成品或把 blocked 当作成功；
- 自动化级别：Unit/Integration。

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
