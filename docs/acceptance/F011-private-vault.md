# F011 Private Vaults 子仓库（0..N）验收

- Feature：F011
- 相关规范：SEC、SYS、SRC、ARC、OPS、WEB
- 相关 ADR：ADR-0002、ADR-0003、ADR-0009
- 实现设计：[Private Vault 子仓库](../technical-design/private-vault-submodule.md)
- 状态：Implemented（2026-08-27；4 个 Registry 基础场景通过；完整 Vault/Projection/Backup 验收仍待补齐）
- 实现证据：`tools/vault_registry.py`、`tools/paths.py`、`tools/cli.py`、`tests/test_vault_registry.py`
- 当前边界：当前实现只读 manifest 解析、路径隔离、Git worktree 检查、owner-aware 对象扫描、local projection 合并和 backup state 派生；跨 Vault 引用、逐 Vault 写入与恢复演练尚未完成。

## 本轮证据（2026-08-30）

- AC-F011-002/004/011/014：`VaultRegistry.local_projection()` 生成 `local-projection/v1`，按 `(vault_id, object_type, object_id)` 稳定排序合并同名对象；`scope=private` 只返回 internal vault，故障 vault 仅保留 `{vault_id,state,reason}` 诊断，不伪装为空仓。证据：`tests/test_vault_registry.py::test_local_projection_merges_same_ids_with_owner_and_private_scope`、`test_local_projection_keeps_unavailable_vault_diagnostic`。

- `tests/test_vault_registry.py::test_available_scopes_include_private_when_private_vault_is_ready` 验证 `VaultCheckReport.available_scopes` 按可用 owner 派生 `public`、`local`、`private`；private vault 缺失时只保留 `public/local`，不会把不可用仓库伪装为 private 可用。

- AC-F011-001/003：`tests/test_vault_registry.py::VaultRegistryTests::test_same_object_id_across_vaults_is_not_a_conflict` 验证两个可用 Vault 各自拥有同名 Wiki 时不冲突且各计数为 1；`test_duplicate_object_id_inside_one_vault_is_reported_without_paths` 验证同 Vault 重复 ID 返回 `duplicate_object_id`。
- SEC/owner 边界：冲突项只包含 `{vault_id, object_type, object_id}`，测试确认报告不包含 workspace 物理路径。

## Private API owner 增量证据（2026-08-27）

- AC-F011-001/006/010：`tests/test_api.py::test_private_vault_read_and_backlinks_are_owner_scoped` 使用两个独立 Git vault 创建同名 Wiki；显式 `vault_id=private` 读取 private 正文和 backlinks，响应仅返回 owner-relative path，public 路由仍读取 public 正文，不按全局 object ID 猜测。

## AC-F011-019 Private owner API 路由

- Given：多个可用 vault 存在同名 object ID；When：使用 capability 调用 read/backlinks 并显式指定 `vault_id`；Then：API 通过 Registry owner root 定位对象，只返回指定 vault 的正文、backlinks 和 vault-relative path；当前状态：通过上述测试。

对象实际合并 projection、跨 Vault 引用阻断、private/public confidentiality 传染和恢复仍待后续验收。

## 本轮 Registry 引用与保密等级证据（2026-08-27）

## 冲突 projection 增量证据（2026-08-30）

- `VaultRegistry.local_projection()` 现在读取 `check()` 的冲突 owner triple；同一 Vault 内重复 `(object_type, object_id)` 不进入 local/private projection，只在 `vault-check/v1` 保留 `duplicate_object_id` 诊断。`tests/test_vault_registry.py::VaultRegistryTests::test_local_projection_excludes_same_vault_conflicts` 验证两个路径同名对象不会被排序选择或覆盖。

- AC-F011-010：`tests/test_vault_registry.py::VaultRegistryTests::test_reference_rejects_cross_vault_even_when_target_exists` 验证目标 vault 可用且对象 ID 合法时，owner=`public` 指向 `private` 仍返回 `cross_vault_reference`，不会按全局 ID 猜测 owner。
- AC-F011-010/012：`VaultRegistry.effective_confidentiality` 对 owner 与 upstream 取最高等级；public 上游包含 internal 时结果为 `internal`，全 public 保持 `public`。该结果仅用于派生门禁，不改变 canonical 事实。
- 边界：本轮未实现跨 vault copy/move、private projection 合并和恢复演练，F011 仍为 Implemented（部分）。

## 跨 Vault copy/move 增量证据（2026-08-30）

- `tests/test_vault_transfer.py::test_private_to_public_transfer_is_blocked_before_write` 验证 internal 内容迁移到 public Vault 时返回 `confidentiality_downgrade`，public 目标不会创建。
- `tests/test_vault_transfer.py::test_cross_vault_copy_and_move_use_explicit_owner_and_locks` 验证 public → private 的 copy/move 必须先 Preview/确认，Apply 使用双 Vault 稳定排序锁、源 hash 复查和目标 hash 校验；copy 保留源，move 在目标成功后删除源。
- CLI 入口 `python -m tools.cli transfer preview|apply` 只委托 `VaultTransfer`，不直接写 Markdown。完整跨 Vault staging 失败恢复和 private projection 重建仍待补，F011 仍为 Implemented（部分）。

## Staging failure recovery 增量证据（2026-08-27）

- `VaultTransfer.apply()` 保持“目标写入并 hash 校验后才删除源”的顺序；源删除失败时清理本次目标文件并释放双 Vault 锁，源内容保持不变。
- `tests/test_vault_transfer.py::test_cross_vault_move_rolls_back_target_when_source_delete_fails` 注入源删除异常，验证返回 `apply_failed`、目标不存在且 public/private lock owner 文件均已释放。

## Local projection materialization 增量证据（2026-08-27）

- `VaultRegistry.write_local_projection()` 将 `local-projection/v1` 以 0600 权限原子写入 `queries/local/manifest.json`，保留 owner 三元组、不可用 Vault 诊断和 `projection_sha256`。
- `tests/test_vault_registry.py::VaultRegistryTests::test_local_projection_can_be_materialized_atomically` 验证输出可解析、hash 一致且不会暴露物理路径。

## Owner-aware object index 增量证据（2026-08-27）

- `tests/test_vault_registry.py::VaultRegistryTests::test_object_index_keeps_same_ids_separate_by_owner` 验证两个 Vault 的同名 Wiki 以 `(vault_id, object_type, object_id)` 分别保留，索引值只含 owner/status 元数据，不暴露物理路径。
- 同 Vault 重复 ID 由 `check()` 先报告冲突，`object_index()` 对冲突键标记 `availability: conflict`，不会静默覆盖。

## Public projection 权限一致性增量证据（2026-08-27）

- `tests/test_vault_registry.py::VaultRegistryTests::test_private_public_projection_permission_is_rejected` 与 `test_internal_public_projection_permission_is_rejected` 验证 private 或 internal vault 声明 `allow_public_projection: true` 时，Registry 返回 `public_projection_confidentiality`；不会把保密内容交给 public generator。

## AC-F011-001 多个私有仓库挂载和合并

- Given：public repo 与两个或更多独立 private Git repo（例如 `team-internal`、`personal-private`）均通过 manifest 声明，schema、vault confidentiality 和 `vault_id` 正确；
- When：执行 `vault check` 和对象索引构建；
- Then：全部可用 vault 的 source/wiki/archive 可按 `(vault_id, object_type, object_id)` 合并，private source/wiki/archive 进入 `queries/local` 并保留 owner `vault_id`，public projection 仍只包含 public 对象；每个 vault 都有独立状态报告；
- 失败时不变量：不把任一 private 正文、路径、remote 或凭据写入 public 生成物；不同 vault 的同名对象不能按 manifest 顺序覆盖或隐式选择 owner；
- 自动化级别：Integration。
- 对应测试：`tests/test_vault_registry.py::VaultRegistryTests::test_multiple_vaults_and_unavailable_isolated`
- 当前状态：部分通过（Registry 隔离已通过，对象合并待实现）。

## AC-F011-002 单个 Vault 不可用时的隔离降级

- Given：manifest 同时声明 `team-internal` 和 `personal-private`，其中一个目录不存在、submodule 未初始化或 Git worktree 不可读，另一个可用；
- When：执行查询、校验和 public/private projection；
- Then：仅故障 vault 的对象标记 `availability: unavailable`，引用它的 Wiki 保留引用并标记 `validation_state: unavailable` + `upstream_unavailable`；不引用故障 vault 的对象仍可查询、索引和发布到其允许的 projection；public build 仍可完成 public 对象；
- 失败时不变量：不得把 unavailable 当成 source missing，不得自动删除、降级或改写 Wiki，也不得把其他 vault 一并标记 unavailable；
- 自动化级别：Integration。

## AC-F011-003 同 Vault ID 冲突阻断

- Given：同一 vault 出现重复 `(object_type, object_id)`，或同一 object 的 evidence binding 不可解释；另有两个 private vault 各自拥有相同 ID；
- When：构建合并对象空间或执行写入 preview；
- Then：同 Vault 重复键报告 `vault_id`、路径和 hash，冲突对象不进入合并 projection，阻断相关校验、索引和 apply；不同 vault 的同名对象分别进入 local projection 并保留 owner；无关对象仍可处理；
- 失败时不变量：不得在同一 vault 内覆盖或静默选择多数版本，也不得把不同 vault 的独立知识对象误合并；
- 自动化级别：Unit/Integration。

## AC-F011-004 相同 snapshot 跨 Vault 去重

- Given：两个 private vault 保存内容完全相同且 hash 相同的不可变 snapshot；
- When：构建 snapshot index 和 `queries/local` projection；
- Then：底层内容可以按 `snapshot_sha256` 去重，但索引保留两个 owner `vault_id`、相对路径和可用性，引用与备份仍可追溯到各自 vault；
- 失败时不变量：同 snapshot 去重不得合并 object ID、丢失 owner、改变 confidentiality 或绕过任一 vault 的备份和发布策略；
- 自动化级别：Unit/Integration。

## AC-F011-005 Internal private publish 告警和目标选择

- Given：internal Wiki 已通过 deterministic/LLM 或 exemption 验证，且请求 `publication_scope: private`；manifest 中存在多个 private vault；
- When：执行 `publish_private` Preview/Apply；
- Then：Preview 要求并明确显示实际 `target_vault`（且必须等于对象 owner）、有效保密等级、hash、告警文本和 `requires_warning_ack`；Apply 只有在目标 vault 可用、publish confirmation 与 warning ack 均存在时成功，并生成该 owner vault 的 `private_publishable`；未指定、指定不存在或与 owner 不同的目标必须 blocked，不能默认使用名为 `internal` 的 vault；跨 Vault 需要另行 copy/move operation；
- 失败时不变量：缺少任一确认不得改变 status、projection 或索引；
- 自动化级别：Integration/Manual confirmation。

## AC-F011-006 Internal 不进入 public projection

- Given：两个或更多 private vault 存在已发布 internal Wiki、source、snapshot 和验证报告；
- When：生成 public manifest、Astro dist、Pagefind、graph、sitemap 和 source map；
- Then：所有 private vault 的 internal 正文、标题、ID、URL、数量、`vault_id` 和关系均不出现；public allowlist 只能接受 `vault_id: public`；
- 失败时不变量：leak gate 命中即阻断，旧 public dist 保持不变；
- 自动化级别：Security/Integration。

## AC-F011-007 外部服务边界

- Given：internal source 需要归档或 LLM 验证；
- When：选择 Wayback/public provider 或 internal_allowed provider；
- Then：Wayback/public provider 被拒绝，internal_allowed provider 可在 policy 允许时使用；无合规 provider 时状态为 `validation_state: unavailable` 并保持 draft/review；
- 失败时不变量：不得把 internal 正文发送到公开服务或日志；
- 自动化级别：Integration。

## AC-F011-008 Submodule 和 revision 独立恢复

- Given：多个 private repo 以 submodule 挂载，其中任一 vault 出现未初始化、HEAD 不匹配、dirty worktree 或仓库损坏；
- When：执行 vault check、只读查询和 apply；
- Then：按 `vault_id` 输出明确原因和恢复建议；只读能力只对受影响对象降级，覆盖/发布只对受影响 vault 阻断，工具不自动 reset/push；恢复该 vault 到期望 commit 后重新 check 可解除对应阻断；
- 失败时不变量：不丢失用户修改、不删除旧索引或备份；
- 自动化级别：Integration/Manual recovery。

## AC-F011-009 Private backup restore

- Given：选定的 private vault `backup_state: verified`，且该 vault 的 private Git remote 或加密备份包含 vault manifest、object hash 和 snapshot；其他 vault 可以处于任意状态；
- When：恢复该 vault 到空 private checkout；
- Then：该 vault 的 object/snapshot hash、ID 索引和 evidence binding 与备份一致，private projection 可重建；其他 vault、public repo 和 public projection 不被改写；
- 失败时不变量：恢复失败不影响无关 vault、public repo 和 public projection；
- 自动化级别：Recovery/Integration。

## AC-F011-010 跨 Vault 内容引用阻断

- Given：public vault 或某 private vault 的 Wiki 引用只能在另一个 Vault 解析的 source ID，且目标 vault 已挂载或未挂载；
- When：执行 public projection 和 leak gate；
- Then：写入/校验阶段直接拒绝并报告带 `source_vault_id`/`target_vault_id` 的 `cross_vault_reference`；public-to-private 和 private-to-private 内容引用不能进入 canonical projection。若历史坏数据已存在，public 对象不生成 catalog、HTML、graph 或 Pagefind 文档；
- 失败时不变量：不能通过把引用改成 missing、删除 ID、暴露 private ID 或改指向另一个 vault 来绕过保密边界；public release 的 `source_vault_ids` 只保留 lineage，不放宽该规则；
- 自动化级别：Security/Integration。

## AC-F011-011 Remote/backup 尚未配置的逐 Vault 告警

- Given：两个 private vault 各自的 `private_git_remote: null`、`encrypted_backup_target: null`、`backup_state: unconfigured`，且状态可能不同；
- When：执行 `vault check`、private publish preview、会话结束检查或 `purge`/覆盖式恢复；
- Then：前 3 类操作逐一报告带 `vault_id` 的醒目 `backup_not_configured` 风险且不声称已备份；只要高风险操作涉及任一未验证 vault，就被阻断；普通读取和可逆编辑以及不相关 vault 的操作仍可用；
- 失败时不变量：不得生成假 remote、假备份时间或“可恢复”结论；
- 自动化级别：Integration/Manual。

## AC-F011-012 Public release 等待人工审核

- Given：public release 已生成脱敏/重新分类输出、当前 `release_input_sha256`、content/evidence hash、lineage、`source_vault_ids` 和 leak-gate 报告；
- When：执行 `public_release` preview；
- Then：Preview 生成 `public_release: false`，展示 diff、证据绑定、有效保密等级和报告 hash；只有人工通过独立 confirmation event（`actor_type: human`、一次性 nonce）将当前 `release_input_sha256` 绑定为 `true` 并完成 public confirmation 后才能 Apply 或进入 `queries/public`；public-safe 事件必须写入 `release/public-confirmations/`，公开投影仅保留不可逆的 `public_lineage_commitment` 和事件 hash；
- 失败时不变量：LLM、Agent、CI 或自动 leak gate 不得把 `public_release` 改为 `true`；
- 自动化级别：Integration/Manual review。

## AC-F011-013 Public release 人工开关保持关闭

- Given：操作生成 `public_release: false`；
- When：人工不确认或明确保持关闭；
- Then：不生成 public projection，操作可继续修改并重新 preview；
- 失败时不变量：false 不能进入 public 文件、Pagefind 或 sitemap；
- 自动化级别：Manual review/Integration。

## AC-F011-014 Public release 开关 hash 失效

- Given：人工已对当前 `release_input_sha256` 确认 `public_release: true`，但输出正文、metadata、evidence 或 leak-gate 报告 hash 在 Apply 前发生变化；
- When：执行 Apply；
- Then：Apply 被拒绝，`public_release` 自动重置为 `false`，必须对新 hash 重新人工确认后才能继续；
- 失败时不变量：不产生部分 public 文件、不复用旧批准；
- 自动化级别：Integration。

## AC-F011-015 零私有仓库兼容路径

- Given：local manifest 只声明 `public` vault，或当前 checkout 未使用外层 workspace superproject；
- When：执行 public-only 查询、索引和静态构建；
- Then：系统按单一 public vault 工作，不要求创建空 private 目录，不改变既有 public object ID、hash 或 projection；
- 失败时不变量：启用/禁用外挂 vault 只是 manifest 变化，不得复制 public 内容或生成第二套数据模型；
- 自动化级别：Integration。

## AC-F011-016 跨 Vault 写锁和 staging 失败

- Given：一次 operation 同时读取或写入多个明确的 `source_vault_ids`/`target_vault`；
- When：并发执行 preview/apply，或其中一个 vault 在 apply 阶段失败；
- Then：锁按稳定 `vault_id` 顺序获取；失败时保留 staging、已成功 vault 列表、precondition hash 和恢复说明，不自动回滚另一仓库的用户变更；
- 失败时不变量：不得死锁、静默覆盖、伪造全局事务成功或删除旧 projection；
- 自动化级别：Integration/Failure injection。

## AC-F011-017 Manifest 路径布局与隔离

- Given：分别使用 direct-checkout 和 superproject 两种布局，挂载两个或更多 private vault；另有重叠路径、symlink/hard-link、错误 submodule gitfile 和重复/非法 `vault_id` fixture；
- When：执行 `vault check` 和 projection；
- Then：只有解析到 workspace root 内、彼此不重叠且 Git owner 正确的路径可用；`public.path: .` 只在 direct mode 指向当前 public worktree 时有效；错误项按 vault 返回结构化原因；
- 失败时不变量：不能越界读取、把 private repo 当 public、按同名 ID 猜 owner 或把绝对路径写入任何 public artifact；
- 自动化级别：Security/Integration。

## AC-F011-018 Public release durable record

- Given：public-owned 脱敏 Wiki 已生成 release preview，且 `public_release: false`；
- When：人工确认并 Apply，随后清理临时 state 或修改任一输入 hash；
- Then：确认事件写入 `release/public-confirmations/<event_id>.json`，owner operation record 写入 `audit/operations/<operation_id>.json`；清理 state 不影响可回放，hash 变化使开关回到 false；
- 失败时不变量：不能仅修改 Front Matter 的 true、复用 nonce/旧 event、将 private lineage/ID/hash 写入 public-safe event，或在 record 缺失时发布；
- 自动化级别：Repository/Security/Manual review。
