# 写操作与锁实现设计

- 状态：Implemented（2026-08-27；通用 writer 与基础验收已落地）
- 相关 Feature：F004
- 相关规范：OPS、SEC
- 相关 ADR：ADR-0006
- 相关验收：[F004](../acceptance/F004-write-operation.md)

## 本轮 commit intent 完整性调查（2026-08-27）

- `filelock` 3.x（MIT，<https://github.com/tox-dev/filelock>）适合进程间互斥，但不提供多文件提交或崩溃恢复语义；SQLite transaction/WAL（Public Domain，<https://sqlite.org/lang_transaction.html>）可提供 durable commit，但本项目 canonical Markdown 仍需文件级原子替换。
- Dendron 的 vault rename/link 重构经验（GPL-3.0，<https://github.com/dendronhq/dendron>）强调可重放的路径映射；Git/Git LFS（GPL-2.0，<https://git-scm.com/docs>）能恢复对象历史，却不会验证本地 operation intent 是否被篡改。替代方案是只检查 intent schema 或文件最终 hash，无法证明恢复目标对应原始 preview。
- 采用 `commit-intent/v1` 自哈希：写入前将 operation、vault、每个文件的 before/after hash 纳入 canonical `intent_sha256`；`recover()` 先重算并校验该 hash，再比较文件状态。intent 缺失、篡改或 operation/vault 不匹配均返回 `recovery_invalid`，不更新 durable operation 为 applied。校验离线，不改变 canonical 数据格式；升级需保留旧 intent 的显式兼容策略，不静默迁移。

## 目标与非目标

本轮 rename precondition 调查（2026-08-27）：Git `mv`/index（GPL-2.0，<https://git-scm.com/docs/git-mv>）要求工作树内容与索引状态一致后再更新路径；Dendron vault rename（AGPL-3.0，<https://github.com/dendronhq/dendron>）保留稳定路径映射。替代方案是只绑定目标文件 hash，无法发现源文件在确认前被用户修改。`WriteOperation.rename()` 现在记录 `source_before_hash`，Apply 在锁内校验该 hash，漂移时返回 `hash_mismatch` 并保留源、拒绝创建目标；离线无网络，不改变其他 operation 格式。

目标是实现 Preview → 用户确认 → Apply、幂等、逐 Vault 排他锁、原子落盘、rename/move 和废弃操作。Agent Skill 只调用本设计定义的 operation API，不拥有第二套写入规则。不可重建的确认、发布和验证摘要写入 owner vault 的 `audit/`；`state/` 只保存可清理的运行态。

## 本轮成熟方案调查（2026-08-27）

- `filelock` v3.32.4（MIT，https://github.com/tox-dev/py-filelock）：复用跨平台排他锁和进程退出自动释放；MyKnowledge 额外保留 vault/token/audit 语义。
- SQLite WAL/transaction（https://sqlite.org/wal.html）：复用原子提交与恢复思想；当前 operation metadata 仍以 JSON durable record 保存，避免引入不必要的数据库迁移。
- Dendron vault refactor（https://github.com/dendronhq/dendron）：借鉴 vault 内路径重构和链接迁移边界；实际 source/wiki 状态和 evidence 门禁仍由 MyKnowledge 领域服务负责。

本轮结论：通用 writer 复用 `filelock`、`atomic_write`（临时文件、fsync、rename）和现有 `OperationStore`，不复制 Source/Wiki 校验逻辑；所有目标路径先做仓库根目录约束，领域 writer 后续通过同一接口接入。

本轮增量：借鉴数据库 fencing token/lease 的成熟边界，在 filelock 之外为每个 Vault 写入 `state/locks/<vault_id>.owner` sidecar（随机 `lock_token` + operation_id），每次文件替换前重新校验。token 不匹配即中止，sidecar 只由当前 owner 清理；这保留 filelock 的内核互斥，同时覆盖陈旧进程继续提交的风险。sidecar 是临时状态，不进入 audit、projection 或 public 输出。

本轮再次复用 Git 提交哈希作为历史链，同时对每个 `audit/operations/<operation_id>.json` 做单条 `record_sha256` 自校验；Apply 前先校验 durable audit，再校验输入 hash，避免被篡改的 state/audit 驱动写入。该校验不引入自建 previous-record 链。

本轮陈旧锁恢复调查（2026-08-27）：filelock 3.32.4（MIT，<https://github.com/tox-dev/py-filelock>）的内核互斥与进程退出释放作为活锁判据；SQLite WAL（Public Domain，<https://sqlite.org/wal.html>）和 etcd lease/fencing（Apache-2.0，<https://github.com/etcd-io/etcd>）仅借鉴 fencing/恢复语义。替代方案是按 mtime/PID 直接删除 lock 文件，会与活进程竞态，明确排除。`VaultLock.recover` 先非阻塞获取 filelock，再写 `record_type: lock-recovery` durable audit 并删除 owner sidecar；活锁返回 `lock_busy`，不执行静默清理。

本轮多 Vault 锁调查（2026-08-27）：filelock 的每文件内核互斥与数据库/etcd 的全局锁排序、lease fencing 语义作为成熟基线；替代方案是按调用方输入顺序逐个获取锁，两个反向 operation 可能死锁，明确排除。`VaultLockGroup` 对 `vault_id` 去重后按 UTF-8 字典序获取，异常时逆序释放已取得锁；不提供跨仓库伪事务，部分 apply 仍由上层报告成功列表和补偿动作。

本轮 Vault 路径绑定调查（2026-08-30）：Git worktree 的 `rev-parse --show-toplevel`（GPL-2.0，<https://git-scm.com/docs/git-rev-parse>）作为 owner 根的权威解析；etcd fencing token（Apache-2.0，<https://etcd.io/docs/v3.5/learning/api_guarantees/>）仅借鉴“锁和资源必须绑定同一 owner”的语义。替代方案是只用 `vault_id` 选择锁、仍把相对路径拼到 public root，会导致 private operation 写错仓库，明确排除。本轮 writer 将路径 containment、before hash、commit-intent 和锁统一绑定到同一 `vault_id` 的 checkout root；public 行为保持兼容，跨 Vault 伪事务仍不提供。

本轮路径竞态调查（2026-08-30）：filelock 的持锁期间路径重检与 SQLite transaction 的 fail-closed rollback 作为成熟边界；替代方案是让预览时通过的路径在 Apply 时直接抛出异常，会把 symlink/越界竞态转成未结构化 500。Apply 现在在回滚后把 `OSError/ValueError` 统一归一为 `expired/apply_failed`，不写入竞态目标，也不吞掉具体诊断。

### Projection/index 提交边界调查（2026-08-30）

- SQLite FTS5 transaction/WAL（Public Domain，<https://sqlite.org/fts5.html>、<https://sqlite.org/wal.html>）和 Git index/working-tree recovery（GPL-2.0，<https://git-scm.com/docs/git-recover>）都把可恢复元数据与最终对象提交分开；适合借鉴“先提交 canonical，再重建派生索引”的顺序，但 Git/SQLite 都不会替本项目维护 Wiki/public confirmation 语义。
- 替代方案是把 canonical、projection、index 放在一个 Python `try` 中，任一派生写失败就回滚所有文件。该方案无法保留已完成的 canonical 提交，也会把可重建故障误报为全局失败；因此不采用。
- MyKnowledge 复用 FTS5 的可重建、hash-bound 派生索引原则：`WriteOperation` 通过可注入 `projection_rebuilder` 在 canonical 原子替换后执行。hook 失败写入 `applied_index_pending`，不生成新的 publishable projection；显式 `recover()` 重跑成功后才追加 durable `applied` 状态。hook 未配置时保持现有通用 writer 行为。
- 离线边界：该状态机不联网、不写 endpoint/key；升级 projection/index 实现必须回归 pending、恢复、幂等和旧 canonical 保持不变测试。commit-intent 仍保留至恢复完成，便于进程崩溃后的诊断。

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

`operation_id` 只有一套口径：`tools/common.py::new_operation_id` 生成 `op_<32 位 hex>`，`tools/common.py::safe_operation_id` 校验，两端同源。校验只约束前缀、字符集与长度上限——`operation_id` 会成为 `audit/operations/<operation_id>.json` 的文件名，要挡的是路径穿越与文件名注入，而不是复刻生成端位宽。此前各调用点各自 `removeprefix("op_")` 再套 `safe_id`（连字符词表）的写法，使 `release confirm` 对每一个真实 `op_<hex>` 都返回 `event_id_invalid`；不合法时统一返回 `operation_id_invalid`。

`release_confirmation.write_event()` 的返回状态区分三种情况，幂等命中不算失败：内容一致的重复提交返回 `already_applied` 并回带既有记录的 `event_sha256` 与路径（CLI 退出码 0）；同 `event_id`、不同内容返回 `event_id_conflict`；既有事件文件损坏不可读返回 `event_unreadable`，不得按幂等放行。把重复提交报成失败会诱导操作者删掉 append-only 确认记录重签，用删审计换一次“成功”。
