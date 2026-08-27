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

本轮 bundle 增量：在 manifest 副本之外增加无压缩 `manifest.json + payload/<relative-path>` 离线 bundle，逐项复用 manifest hash 校验和 owner/path/symlink/hardlink 门禁。bundle 验证不读取 canonical checkout，也不改变 Vault 状态；未来恢复入口必须从 bundle 重建空 checkout 后再生成本地 restore marker。

当前已实现 `restore_bundle`：先验证 bundle，再要求空 target，按 manifest 相对路径原子写入并在 target 内记录 `backup-restore-record/v1`。任一条目失败会清理已写文件和空目录；恢复结果是可审计证据，不自动修改源 Vault 的 `backup_state`。

本轮 bundle owner 调查（2026-08-30）：Git bundle 的 ref/owner 必须是可解析的稳定标识，SQLite backup 的数据库名不能替代 Vault owner；替代方案是只验证 payload hash 而忽略 `vault_id`，会让恢复审计无法判断目标归属。`verify_bundle()` 现在要求 `vault_id` 为 `safe_id` 且 `entries` 为列表，非法 owner 元数据在读取 payload 前 fail-closed。

本轮跨 Vault 恢复调查（2026-08-30）：Restic stable restore 文档（项目版本 0.17.x，BSD-2-Clause，<https://restic.readthedocs.io/en/stable/050_restore.html>）将 snapshot/repository 身份与显式 `--target` 分离，目标路径本身不承担来源归属；Borg 1.4 文档（BSD-3-Clause，<https://borgbackup.readthedocs.io/en/stable/usage/usage.html>）同样以 archive/repository 元数据选择恢复来源。两者均支持离线校验/恢复，但不会替 MyKnowledge 判定 Vault confidentiality 或跨 Vault 引用政策。采用：新增 `restore_bundle_to_vault(bundle, target, target_vault_id)`，在创建目标前用 `safe_id` 校验显式目标 ID，并要求其与 manifest `vault_id` 完全相等；错配返回 `cross_vault_restore`，不创建或修改目标。直接复用成熟方案的“来源元数据 + 显式目标”边界，MyKnowledge 保留 owner ObjectRef、private/public confidentiality、空目标和 restore marker 门禁。离线时只读取 bundle manifest/payload；升级影响限于 manifest/schema 与 owner 校验，不执行 checkout/reset/commit/push，也不保存 URL、凭据或正文之外的敏感信息。

本轮恢复后集合校验调查（2026-08-30）：Borg `check` 1.4.5（BSD-3-Clause，<https://borgbackup.readthedocs.io/en/stable/usage/check.html>）区分 repository 与 archive 完整性检查；Restic 的 repository check/restore 文档（BSD-2-Clause，<https://restic.readthedocs.io/en/stable/050_restore.html>）要求恢复目标显式指定并可再次验证。替代方案是只相信复制函数返回成功，无法发现目标中额外文件、owner marker 被替换或恢复后的 entry hash 漂移。采用 `verify_restored_bundle()`：逐项复核 manifest hash、拒绝 symlink/hard-link/缺失或额外文件，并要求与 manifest owner/hash 匹配且 `record_sha256` 有效的 restore marker；`restore_bundle()` 只有通过该复核才返回 restored，失败清理整个空目标。该校验离线运行，不扫描其他 Vault，不改变 public projection。

每个 Vault 独立维护 `private_git_remote`、`encrypted_backup_target` 和派生 `backup_state`：`unconfigured`、`configured`、`verified`、`failed`。`unconfigured` 只表示没有任何 target；只配置一个 target 也可以进入 `verified`，但必须明确报告没有第二份冗余。`configured` 表示至少一个 target 和 opaque credential reference 可解析但尚未完成验证；target 身份变化或验证过期回到 `configured`。上传、完整性或恢复失败进入 `failed`；修正 target 后重新验证才能回到 `verified`。`verified` 只能由**所有已配置 target** 的最近一次备份、manifest integrity check、Git 历史可解析和隔离空仓恢复演练共同产生；全局汇总不能覆盖单 Vault 状态。当前所有 private target 保持 `null`/`unconfigured`；public 条目的置空字段不触发 private backup 告警。

## 备份内容与恢复

备份 manifest 的 canonical schema version 是 `backup-manifest/v1`，至少包含 Vault ID、规范化相对仓库标识、expected HEAD、分支/submodule commit、schema/policy version、object ObjectRef、object ID、content/evidence hash、snapshot owner key、snapshot hash、archive record hash、evidence binding hash、人工审计确认 hash、`operation-confirmation/v1`/`public-release-confirmation/v1` event hash（适用时）、operation record hash、生成器版本和 manifest 自身 `manifest_sha256`。owner Vault 的 durable manifest 固定在 `audit/backup/<backup_id>.json`；外部 target 只保存副本。`target_identity_opaque` 和 `encryption.key_ref_opaque` 只能是不可逆引用，不能写 remote URL、密钥或 token。它必须明确列出 LFS 对象（如启用）和每个 blob 的校验结果；public backup 不包含 private 正文、路径、remote、凭据或 private ID。workspace shared blob cache 若启用，必须在每个 owner Vault 的 manifest 中列出并在备份中可重建，不能只备份共享缓存。恢复到空 checkout 后必须先校验 manifest/hash、文件类型、symlink/hard-link 和 Git/LFS 完整性，再逐条校验 durable record 的 `record_sha256` 与 target owner（顺序与篡改证据来自 Git 历史，不再验证自建 hash chain），之后才能生成 private/local projection；失败返回 `hash_mismatch`，不修改 public 或其他 Vault。未验证 Vault 的 purge、覆盖式恢复和清理默认阻断。

恢复成功的判定不是“文件复制完成”，而是：在隔离的空 checkout 中重新运行 Vault Registry、object/snapshot index、deterministic validation 和 projection，得到与 manifest 相同的 owner/hash 集合；durable `audit/operations/`、`audit/validation/` 和（若为 public-owned）`release/public-confirmations/` 必须可解析。临时 `state/` 丢失只允许重新生成，不能使备份从未验证变为 verified。备份工具默认不执行 checkout reset、hook、commit 或 push，所有恢复目标由用户显式提供。

## 告警与审计

`vault check`、private publish preview、会话结束检查和高风险操作都按 Vault 输出 `backup_not_configured` 或恢复失败原因。审计记录包含 `operation_id`、Vault ID 集合、HEAD、输入 hash、阶段、耗时、错误 code、结果、恢复建议和 `record_sha256`，不包含凭据、private path、selector exact 或敏感正文。每个 operation/validation/publish record 使用固定文件名和 append-only 规则，记录 owner `vault_id`、target ObjectRef、policy/schema/tool version 和相关 hash；public-safe event 另按 event schema 校验，不能从普通日志推导确认。

## 测试与演练

测试覆盖多 Vault 独立状态、备份目标缺失、备份校验失败、空仓恢复、损坏 snapshot、丢失/篡改 audit 或 confirmation record、audit sequence gap/previous hash mismatch、部分多 Vault Apply、旧 projection 保留和日志脱敏。恢复演练报告记录时间、工具版本、输入 manifest hash、校验结果、恢复后 object/snapshot/evidence/attestation hash 集合、audit chain 验证结果和人工复核人；缺少任一 durable record 必须保持 `failed`/`unconfigured`。`BackupManager.status` 对已配置 Vault 的最近 durable manifest 做 schema/self-hash/entries 结构检查；损坏派生为 `failed`，manifest 存在本身不会提升为 `verified`。
