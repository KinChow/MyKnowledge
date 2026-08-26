# 写操作与锁实现设计

- 状态：Draft
- 相关 Feature：F004
- 相关规范：OPS、SEC
- 相关 ADR：ADR-0006
- 相关验收：[F004](../acceptance/F004-write-operation.md)

## 目标与非目标

目标是实现 Preview → 用户确认 → Apply、幂等、逐 Vault 排他锁、原子落盘、rename/move 和废弃操作。Agent Skill 只调用本设计定义的 operation API，不拥有第二套写入规则。不可重建的确认、发布和验证摘要写入 owner vault 的 `audit/`；`state/` 只保存可清理的运行态。

## 核心流程

生成规范化 operation → 保存 Preview → 用户确认 → 获取写锁 → 校验输入和前置 hash → 在同一文件系统生成 canonical/projection staging → 最终校验 → 写 commit-intent 并 fsync → 原子提交 canonical 与 durable record → 原子替换 projection/index → 记录完成状态。

## 失败处理

任何前置条件失败都不写入目标对象；提交前中途失败必须可恢复，不能留下可发布半成品；重复 operation 返回既有结果。canonical 提交后若仅 projection/index 失败，保留旧 projection 并将 operation 标记 `applied_index_pending`，恢复器负责重建，不能声称完整链路已完成。缺少来源、Vault、provider 或 leak gate 时 operation 进入 `blocked`，不会留下可自动续写的半成品。

## 测试策略

覆盖未确认 Apply、重复 Apply、hash 冲突、并发写入、进程中断、移动和废弃。

## 锁、幂等和恢复契约

- 锁文件位于实际 Vault 的 `state/locks/<vault_id>.lock`，内容至少包含 `operation_id`、随机 `lock_token`、fencing token、持有进程 PID、进程启动时间、主机、创建时间和 `heartbeat_file`；锁主体在持有期间不可变，最新心跳写入同目录 sidecar（`*.lock.heartbeat`），用临时文件 + fsync + rename 原子替换，锁目录被 Git 忽略且不进入 projection。
- 获取锁使用原子 `O_CREAT|O_EXCL`；默认超时 15 分钟，持有者每 30 秒更新心跳。超时锁只能由同一主机上的显式 `lock recover --operation-id` 清理，并先检查 PID/进程启动时间，不能静默删除活锁。
- 每一个 commit-intent、canonical/projection/index 替换和释放动作前都要重新读取并比较 `lock_token` 与 `operation_id`；token 不匹配就中止，不能依赖 PID 或“锁文件仍存在”推断持有权。恢复旧锁必须追加 `record_type: lock-recovery` 的 durable audit record，并使旧 token 失效。
- 单 Vault operation 先生成 staging，再在锁内重新检查 registry hash、HEAD、输入 hash 和目标文件 hash；任一不匹配即 `expired`，不写入。
- staging 必须同时包含 canonical 文件、durable operation/attestation record 和待生成 projection；最终校验通过后写入 commit-intent，记录每个旧/新 hash、路径和恢复动作，并在替换前 fsync。
- 启动时扫描未完成 commit-intent：没有 commit marker 按 manifest 恢复旧文件，有 marker 则补建 projection/index 并追加完成 record；任何恢复动作都不执行 reset、push 或删除用户未列出的文件。
- 多 Vault operation 按排序后的 `vault_id` 获取全部锁；不提供跨仓库伪事务。部分 Apply 时保留 staging、成功 Vault 列表和恢复说明，由用户决定继续或补偿。
- staging 必须位于目标 Vault 同一文件系统；若无法保证同一文件系统，writer 必须拒绝原子 Apply，而不是退化为跨设备 copy-and-delete。
- Apply 成功后写入不可变 durable operation record（`audit/operations/`）；同一幂等键重复调用返回原结果，hash、目标或策略变化生成新 operation。
- projection/index 写入失败时保留旧生成物，返回 `applied_index_pending` 和明确的重建动作；在 pending 状态下对象不得获得新的 `public_publishable`。

确认事件只有两个版本化类型（3 → 2 合并）：

- **`operation-confirmation/v1`**，由 `scope` 区分用途。至少包含 `event_type`、`event_id`、`operation_id`、`target_ref`、`scope`、`actor_type`、`actor_id`、`decision`、`confirmed_at`、`precondition_hashes`、`diff_sha256` 和 `event_sha256`。
  - `scope: apply`：普通 source/wiki apply，要求 `actor_type: human`。
  - `scope: publish_private`：私有发布，额外必填 `content_sha256`、`evidence_sha256`、`target_vault`；有效保密等级为 `internal` 时同一事件还必须携带 `warning_code` 和 `warning_text_sha256`（原独立的告警确认事件已并入此处，告警仍必须展示且不可静默跳过）。
- **`public-release-confirmation/v1`**，保持独立类型。public release 是唯一不可撤销的对外行为，独立类型让"写错一个 scope 值就公开了 internal 内容"在 schema 层不可表达。它额外必填 `release_input_sha256`、`reviewed_content_sha256`、`reviewed_evidence_sha256`、`leak_gate_report_sha256`、`leak_gate_report_scope`、`reason` 和一次性 `confirmation_nonce`。

事件 hash 使用去掉自身字段后的 canonical JSON UTF-8 计算，在 Apply 前重新校验，任何输入变化都使事件失效。一次性 nonce 只用于 public release：apply 与私有发布的重放已由 hash 绑定挡住（输入一变事件就不再匹配），再叠一层 nonce 只增加状态而不增加保障。nonce 的消费结果写入 durable operation record。
