# 备份、恢复与可观测性实现设计

- 状态：Implemented（2026-08-27；逐 Vault 状态与 durable manifest 基础能力已落地）
- 相关 Feature：F012
- 相关规范：SEC、OPS、ARC
- 相关 ADR：ADR-0002、ADR-0003、ADR-0006
- 相关验收：[F012](../acceptance/F012-backup-and-observability.md)

## 逐 Vault 备份状态

本轮成熟方案调查（2026-08-30）：Git-based backup/restore（<https://git-scm.com/docs>，GPL-2.0 文档/实现）复用 HEAD/worktree 可验证提交；SQLite backup API/WAL（<https://sqlite.org/backup.html>，public domain）复用一致性快照思想；替代方案是 rsync 文件复制（GPL-3.0），但缺少 owner record/hash manifest 和 Git 历史语义，本轮不采用。`tools/backup.py` 现在为 public owner 生成 sources/wiki/archive/audit 的相对路径 hash entries，并逐项离线重算；恢复时要求显式空 target、先验证 manifest 再原子写入并在失败时清理 staging。不自动上传、checkout、reset、commit 或 push，真实外部 target 仍保持未配置边界。

本轮 durable record 校验调查（2026-08-27）：Git 的对象哈希/提交历史（GPL-2.0）作为删除与重排证据，SQLite WAL/backup API（Public Domain）作为一致性快照参考；替代方案是只相信 manifest entry hash，攻击者可同步修改 manifest 后伪造记录，因此不采用。`verify_manifest` 对 `audit/operations/*.json` 重算 `record_sha256`，对 `release/public-confirmations/*.json` 重算并验证 `event_sha256`；记录本身无效时即使 manifest entry hash 被重写也返回失败。该校验离线运行，不保存 URL、凭据或正文摘要之外的敏感数据。

本轮外部 target 调查（2026-08-30）：Git bundle v2（Git 2.45.2，GPL-2.0，<https://git-scm.com/docs/git-bundle>）适合已提交对象，但不能覆盖未提交 canonical 文件与本地 audit；SQLite backup/WAL（Public Domain，<https://sqlite.org/backup.html>）提供一致性快照思路。故本轮采用显式 target 的 manifest 副本导出作为可验证传输阶段，target 只接收 `backup-manifest/v1` 和 hash，不把副本存在误报为完整备份；导出后仍必须在隔离空 checkout 执行恢复并生成 owner marker 才能派生 `verified`。替代方案是直接复制目录并把 `configured` 改成 `verified`，明确排除。

每个 Vault 独立维护 `private_git_remote`、`encrypted_backup_target` 和派生 `backup_state`：`unconfigured`、`configured`、`verified`、`failed`。`unconfigured` 只表示没有任何 target；只配置一个 target 也可以进入 `verified`，但必须明确报告没有第二份冗余。`configured` 表示至少一个 target 和 opaque credential reference 可解析但尚未完成验证；target 身份变化或验证过期回到 `configured`。上传、完整性或恢复失败进入 `failed`；修正 target 后重新验证才能回到 `verified`。`verified` 只能由**所有已配置 target** 的最近一次备份、manifest integrity check、Git 历史可解析和隔离空仓恢复演练共同产生；全局汇总不能覆盖单 Vault 状态。当前所有 private target 保持 `null`/`unconfigured`；public 条目的置空字段不触发 private backup 告警。

## 备份内容与恢复

备份 manifest 的 canonical schema version 是 `backup-manifest/v1`，至少包含 Vault ID、规范化相对仓库标识、expected HEAD、分支/submodule commit、schema/policy version、object ObjectRef、object ID、content/evidence hash、snapshot owner key、snapshot hash、archive record hash、evidence binding hash、人工审计确认 hash、`operation-confirmation/v1`/`public-release-confirmation/v1` event hash（适用时）、operation record hash、生成器版本和 manifest 自身 `manifest_sha256`。owner Vault 的 durable manifest 固定在 `audit/backup/<backup_id>.json`；外部 target 只保存副本。`target_identity_opaque` 和 `encryption.key_ref_opaque` 只能是不可逆引用，不能写 remote URL、密钥或 token。它必须明确列出 LFS 对象（如启用）和每个 blob 的校验结果；public backup 不包含 private 正文、路径、remote、凭据或 private ID。workspace shared blob cache 若启用，必须在每个 owner Vault 的 manifest 中列出并在备份中可重建，不能只备份共享缓存。恢复到空 checkout 后必须先校验 manifest/hash、文件类型、symlink/hard-link 和 Git/LFS 完整性，再逐条校验 durable record 的 `record_sha256` 与 target owner（顺序与篡改证据来自 Git 历史，不再验证自建 hash chain），之后才能生成 private/local projection；失败返回 `hash_mismatch`，不修改 public 或其他 Vault。未验证 Vault 的 purge、覆盖式恢复和清理默认阻断。

恢复成功的判定不是“文件复制完成”，而是：在隔离的空 checkout 中重新运行 Vault Registry、object/snapshot index、deterministic validation 和 projection，得到与 manifest 相同的 owner/hash 集合；durable `audit/operations/`、`audit/validation/` 和（若为 public-owned）`release/public-confirmations/` 必须可解析。临时 `state/` 丢失只允许重新生成，不能使备份从未验证变为 verified。备份工具默认不执行 checkout reset、hook、commit 或 push，所有恢复目标由用户显式提供。

## 告警与审计

`vault check`、private publish preview、会话结束检查和高风险操作都按 Vault 输出 `backup_not_configured` 或恢复失败原因。审计记录包含 `operation_id`、Vault ID 集合、HEAD、输入 hash、阶段、耗时、错误 code、结果、恢复建议和 `record_sha256`，不包含凭据、private path、selector exact 或敏感正文。每个 operation/validation/publish record 使用固定文件名和 append-only 规则，记录 owner `vault_id`、target ObjectRef、policy/schema/tool version 和相关 hash；public-safe event 另按 event schema 校验，不能从普通日志推导确认。

## 测试与演练

测试覆盖多 Vault 独立状态、备份目标缺失、备份校验失败、空仓恢复、损坏 snapshot、丢失/篡改 audit 或 confirmation record、audit sequence gap/previous hash mismatch、部分多 Vault Apply、旧 projection 保留和日志脱敏。恢复演练报告记录时间、工具版本、输入 manifest hash、校验结果、恢复后 object/snapshot/evidence/attestation hash 集合、audit chain 验证结果和人工复核人；缺少任一 durable record 必须保持 `failed`/`unconfigured`。`BackupManager.status` 对已配置 Vault 的最近 durable manifest 做 schema/self-hash/entries 结构检查；损坏派生为 `failed`，manifest 存在本身不会提升为 `verified`。
