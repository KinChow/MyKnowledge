# F012 备份、恢复和可观测性验收

- Feature：F012
- 相关规范：SEC、OPS
- 状态：Implemented（2026-08-27；基础状态/manifest 已实现，完整恢复验收待补齐）
- 实现证据：`tools/backup.py`、`tools/vault_registry.py`、`tools/cli.py`
- 当前边界：已实现 durable manifest 生成与离线 hash 校验；当前未实现外部 target 传输、空仓恢复演练、durable record 全量校验和持久 verified 状态派生。

## 本轮证据（2026-08-28）

- AC-F012-005/006：`tests/test_vault_registry.py::VaultRegistryTests::test_backup_manifest_verification_detects_tampering` 验证生成的 `backup-manifest/v1` 自身 hash 可校验，内容被篡改后返回 `backup_state: failed` 与 `hash_mismatch`。
- AC-F012-008：同一测试验证 manifest 验证结果包含 owner `vault_id`、manifest hash 和仓库相对路径；校验过程不上传、不修改 Vault 文件。

该证据不代表外部备份已配置、空仓恢复已完成或 Vault 可持久标记为 verified；未配置目标仍必须报告 `backup_not_configured`。

## 外部 target manifest 导出增量证据（2026-08-30）

- `BackupManager.export_manifest()` 将已校验的 owner manifest 原子复制到用户显式指定的外部 target；target 位于仓库内会被拒绝，输出不含 remote、凭据或正文。
- `tests/test_vault_registry.py::test_backup_manifest_can_be_exported_without_claiming_verified_target` 验证导出结果为 `state: exported`、`backup_state: configured`，不会因存在外部副本直接派生 `verified`。完整内容传输和隔离恢复仍需单独演练。

## Entries 增量证据（2026-08-30）

- `tests/test_vault_registry.py::VaultRegistryTests::test_backup_manifest_must_live_under_declared_owner` 验证备份 manifest 必须位于声明 Vault 的 `audit/backup/` 下，复制到外部路径后返回 `manifest_owner_mismatch`，不会跨 Vault 复用校验结果。

- AC-F012-005/008：`BackupManager.create_manifest` 为 public owner 记录 sources/wiki/archive/audit 文件的相对路径、sha256 和 size；`verify_manifest` 逐项重算并在缺失或 hash 变化时返回 `failed`。
- 备份 manifest 不包含绝对路径、token、remote URL 或私有 Vault 内容；外部 target 未配置时仍保持 `unconfigured`。

## 本轮状态派生证据（2026-08-27）

- `tests/test_vault_registry.py::VaultRegistryTests::test_backup_not_configured_warning_has_safe_next_action` 验证未配置 private target 时逐 Vault 报告 `backup_not_configured` 和脱敏 `next_action`，不泄露 workspace path，也不把状态提升为 verified。

- `tests/test_vault_registry.py::VaultRegistryTests::test_backup_status_derives_failed_from_corrupt_latest_manifest` 验证已配置 target 的最近 durable manifest 被篡改或结构损坏时，`backup_status` 派生为 `failed/manifest_invalid`。
- 状态边界：只有 target 配置仍为 `configured`；本轮不会因 manifest 存在而伪造 `verified`，完整 entries、audit chain 与隔离恢复仍须通过 `verify_manifest`/恢复演练。

- `tests/test_vault_registry.py::VaultRegistryTests::test_valid_manifest_alone_does_not_claim_verified_target` 进一步验证：即使 manifest 本身校验通过，未完成恢复演练时状态仍为 `configured`，不会把单次校验结果冒充完整备份准出。

## Symlink/hard-link 恢复边界证据（2026-08-27）

- `tests/test_vault_registry.py::VaultRegistryTests::test_backup_rejects_hardlink_entries` 验证 owner Vault 中 hard-link 条目在 manifest 生成阶段返回 `entry_hardlink`，不把 Vault 外部 inode 纳入备份。
- manifest 校验和恢复阶段同时拒绝 symlink/hard-link；路径 containment 之外不依赖文件名判断安全性。

## 空仓恢复增量证据（2026-08-30）

- `tests/test_vault_registry.py::VaultRegistryTests::test_verified_manifest_restores_to_empty_checkout` 现验证成功隔离恢复写入 owner-scoped `backup-restore-record/v1` 后，`vault check/status` 才派生 `backup_state: verified`；`test_restore_marker_tampering_does_not_derive_verified` 验证 marker 篡改回到 `configured`。

- AC-F012-002/005/007：`tests/test_vault_registry.py::VaultRegistryTests::test_verified_manifest_restores_to_empty_checkout` 验证已校验 manifest 可恢复到显式空 checkout；`test_restore_requires_empty_target` 验证非空目标返回 `restore_target_not_empty`，不会覆盖用户文件。
- 恢复过程只复制 manifest 已列出的 owner entries，路径穿越、缺失文件或 hash 异常会失败并清理已创建文件；不修改 public/其他 Vault。

## 恢复中途失败清理增量证据（2026-08-27）

- `tests/test_vault_registry.py::VaultRegistryTests::test_restore_cleans_partial_checkout_after_write_failure` 注入第二个 entry 写入失败，验证已写文件及其空父目录均被清理，目标 checkout 不留下半恢复内容。

## Durable operation 校验增量证据（2026-08-30）

- AC-F012-006：`tests/test_write_operation.py::WriteOperationTests::test_tampered_durable_audit_blocks_apply` 验证 durable operation audit 的单条 `record_sha256` 不匹配时写入被阻断；顺序与删除证据仍由 Git 历史提供，不引入自建链。

- AC-F012-006：`VaultLock.recover` 的恢复测试验证陈旧 owner sidecar 清理前先获取内核锁，并追加 `record_type: lock-recovery`、`record_sha256` 的 durable record；活锁不会被删除。

- AC-F012-006/008：`tests/test_vault_registry.py::VaultRegistryTests::test_backup_rejects_manifest_with_rehashed_tampered_durable_record` 验证同时篡改 durable operation、entry hash 和 manifest hash 仍被 `durable_record_hash_mismatch` 阻断；release confirmation entries 还必须通过 `event_sha256` 校验。

## Practice owner 增量证据（2026-08-27）

- AC-F012-005/007/008：`BackupManager.create_manifest` 和 `verify_manifest` 按 owner vault 记录 `practice/questions`、`practice/reviews` 的相对路径与 sha256；`tests/test_vault_registry.py::VaultRegistryTests::test_practice_entries_are_owner_scoped_and_restored` 验证空 checkout 恢复，`test_private_manifest_does_not_read_public_or_escape_owner` 验证 private manifest 不读取 public 内容或越过 owner 边界。

## AC-F012-001 逐 Vault 状态

- Given：多个 private Vault 的 remote/backup 状态不同；
- When：执行 `vault check`；
- Then：逐 Vault 输出 `backup_state`、最近结果、未配置告警和受影响对象；
- 失败时不变量：不能用全局状态掩盖单 Vault 风险。
- 自动化级别：Integration。
- 对应测试：`tests/test_vault_registry.py::VaultRegistryTests::test_public_only_fallback_is_available`
- 当前状态：部分通过（状态输出已实现）。

## AC-F012-002 空仓恢复演练

- Given：某 Vault 已配置并标记可备份；
- When：恢复到空 checkout；
- Then：object ID、snapshot hash、evidence binding 和 projection 可重建；
- 失败时不变量：不修改 public 或其他 Vault。
- 自动化级别：Recovery/Integration。

## AC-F012-003 操作可观测性

- Given：挂载、索引、发布、恢复或失败操作；
- When：查看报告；
- Then：可按 operation_id/vault_id/hash 定位阶段、错误和恢复建议；
- 失败时不变量：日志不包含凭据、private path、selector exact 或敏感正文。
- 自动化级别：Integration/Security。

## AC-F012-004 持久审计与临时状态分离

- Given：public release、private publish、验证和 purge 操作完成，或本机 `state/` 被清理；
- When：在干净 checkout 重新执行 check/projection；
- Then：owner vault 的 `audit/operations/`、`audit/validation/` 和 public-safe `release/public-confirmations/` 足以验证当前 hash/确认状态；临时 state 丢失只触发重新生成，不改变事实记录；
- 失败时不变量：不能用被忽略的 state 缓存或日志声称人工确认、验证或可恢复性存在；
- 自动化级别：Repository/Integration。

## AC-F012-005 备份 manifest 完整性

- Given：Vault 已配置备份目标，包含 snapshot、evidence、validation attestation、private publish 和 public-safe confirmation record；
- When：生成备份 manifest 并在空 checkout 恢复；
- Then：manifest 含 owner ObjectRef、HEAD/submodule/LFS、对象/快照/evidence/attestation/operation/confirmation hash 和自身 `manifest_sha256`；恢复后重新生成的 hash 集合一致；
- 失败时不变量：缺少任一 durable record、校验失败或备份只含临时 state 时不得标记 `verified`，不得修改其他 Vault；
- 自动化级别：Recovery/Integration/Security。

备份状态只允许 `unconfigured`、`configured`、`verified`、`failed`；shared snapshot blob cache 即使存在，也不能替代 owner Vault 的 manifest 或备份对象。

## AC-F012-006 Durable record 完整性由 record_sha256 与 Git 历史保证

- Given：owner Vault 的 operation/validation/release durable record 中，一条被篡改内容、一条被删除、一条被重复；
- When：执行 `vault check`、备份 manifest 生成或空仓恢复；
- Then：被篡改的记录因 `record_sha256` 自校验失败返回 `hash_mismatch`；删除与重排由 `git log` 暴露，不由自建 chain 检测；Vault 不得标记 `verified`，相关 publish/restore 阻断；
- 失败时不变量：不得为 durable record 引入 `sequence`/`previous_record_sha256`/`chain_scope` 自建哈希链——Git commit 已是哈希链，重复实现更弱且可能与 Git 历史不一致；不能依赖 state/log 掩盖篡改；锁恢复必须有 `lock-recovery` 记录；
- 自动化级别：Unit/Repository/Recovery/Security。

## AC-F012-007 Backup state transitions

- Given：某 private Vault 依次处于无 target、配置一个 target、完成验证、target 身份变化、验证过期和恢复失败；
- When：执行 backup、restore 和 `vault check`；
- Then：状态严格按 `unconfigured -> configured -> verified`，失败进入 `failed`，target 变化/过期回到 `configured`，删除所有 target 回到 `unconfigured`；`verified` 只允许在所有已配置 target 的 manifest integrity、audit chain 和隔离空仓恢复都通过后产生；
- 失败时不变量：不能因为 shared blob cache、最近一次成功上传或作者手写字段把 Vault 标为 `verified`，未验证 Vault 的 purge/覆盖式恢复仍被阻断；
- 自动化级别：Unit/Integration/Recovery。

## AC-F012-008 Durable backup manifest 与密钥引用

- Given：Vault 生成备份，包含 snapshot（可物理去重）、LFS、operation/validation/release audit 和加密 target；
- When：检查 `audit/backup/<backup_id>.json` 并恢复到空 checkout；
- Then：manifest 自身 hash、owner ObjectRef、snapshot/archive/LFS、audit chain heads、target kind 和恢复后 hash 集合均可校验；remote/加密配置只保存 opaque identity/key reference，不保存 URL、密钥或 token；每个 owner Vault 都有独立 manifest/恢复记录；
- 失败时不变量：缺少 durable manifest、owner 记录或 key reference 解析失败不得标记 `verified`，不能用共享 blob cache 替代 owner Vault 的备份；
- 自动化级别：Repository/Security/Recovery。
