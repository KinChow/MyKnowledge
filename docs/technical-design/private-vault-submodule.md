# Private Vaults 子仓库（0..N）实现设计

- 状态：Implemented（2026-08-27；只读 Vault Registry 基础能力已落地）
- 相关 Feature：F011、F007、F012
- 相关规范：SYS、SEC、SRC、ARC、WIKI、OPS
- 相关 ADR：ADR-0002、ADR-0003、ADR-0006、ADR-0009
- 相关验收：[F011](../acceptance/F011-private-vault.md)、[F007](../acceptance/F007-static-wiki-publishing.md)

## 1. 目标与非目标

### 目标

- 用一个 public vault 加 `0..N` 个独立私有 Git vault 保存 internal source、wiki、practice、snapshot 和 local index；
- 在同一套 schema、ID、hash、evidence 和 operation 契约下合并全部已声明 vault；
- 支持每个 private vault 独立的挂载、版本、脏工作树、冲突、备份和恢复状态；
- 支持一个 vault 不可用时其他 vault 仍可查询，并对引用故障 vault 的对象给出可解释 `unavailable` 降级；
- 支持 internal 内容确认后私有发布，并强制显示 `publication_warning: internal`；告警确认并入 `operation-confirmation/v1`（`scope: publish_private`）的 `warning_code` + `warning_text_sha256` 必填字段，不再是独立事件类型；
- 让 public projection、Pagefind、外部快照服务和 public LLM 永远看不到 internal 正文；
- 对多个 Git submodule、工作树异常、同 Vault ID 冲突、禁止跨 Vault 内容引用和中途失败提供可恢复处理。

### 非目标

- 多用户权限系统、服务端 ACL 或在线协作；
- 在 public repo 中加密存储 internal 正文；
- 自动 commit、push、reset、submodule update 或删除用户数据；
- 将 private vault 的内容复制到第二套数据库作为事实源。

## 2.1 本轮成熟方案调查（2026-08-27）

- Git worktree/submodule：复用 Git 的 `rev-parse --show-toplevel`、HEAD 和独立工作树边界；Registry 只读检查，不执行 update、reset 或 push。
- YAML manifest：复用 PyYAML safe loader 和版本化 manifest；路径经过 realpath、workspace containment 和不重叠检查，不把绝对路径写入共享报告。
- 最小权限原则：采用显式声明而非自动扫描 `../vaults`；不存在的 optional vault 只影响自身状态。

本轮结论：`tools/vault_registry.py` 先交付只读 `VaultCheckReport` 与 `vault check`，对象合并、跨 Vault 写锁、备份恢复和 projection generator 作为后续增量，不伪造 F011 Accepted。

本轮增量调查（2026-08-30）：Git worktree/submodule 的 owner 边界继续作为挂载基线；参考 Git object namespace 和显式 registry 的做法，在每个可用 Vault 内扫描 `wiki/` 与 `sources/` 的稳定 ID。跨 Vault 相同 `(object_type, object_id)` 不冲突；同一 Vault 重复 ID 形成阻断级 `duplicate_object_id`。扫描报告只输出 ObjectRef 与计数，不输出物理路径，降低 public/共享日志泄漏风险。

`VaultRegistry.object_index()` 现按 `(vault_id, object_type, object_id)` 输出可供 local projection/index 使用的 owner-aware 索引；冲突键标记 `availability: conflict`，不可用 Vault 不被伪装为空仓或被其他 owner 替代。

本轮 API owner 调查（2026-08-27）：Git 独立 worktree/submodule owner root（GPL-2.0，<https://git-scm.com/docs/git-worktree>）与 PyYAML safe loader（MIT，<https://github.com/yaml/pyyaml>）继续作为成熟隔离方案；替代方案是按全局 `object_id` 搜索或按 manifest 顺序猜测 owner，会在同名对象时泄漏/读错内容，明确排除。API 只接受显式 `vault_id`，通过 Registry realpath 解析 owner，返回 vault-relative path；private 内容不进入 public projection。新增 `VaultRegistry.validate_reference` 复用该 owner 边界并对跨 vault 目标 fail-closed；`effective_confidentiality` 复用最高等级传染规则。离线模式仅依赖本地 manifest/checkout，不上传正文；manifest 字段变化会使报告 hash 改变并要求重新校验。

### 本轮 local projection 合并调查（2026-08-30）

- Git worktree/submodule（Git 2.45.2，GPL-2.0，<https://git-scm.com/docs/git-worktree>、<https://git-scm.com/book/en/v2/Git-Tools-Submodules>）：复用独立 checkout、HEAD 和 owner 根；限制是 Git 不定义跨仓库知识对象的合并语义，因此不能直接把路径或全局 ID 当作 owner。

本轮冲突投影调查（2026-08-30）：Git index/merge 的 unresolved conflict 采用 fail-closed，必须先解决冲突才能生成可消费树；本项目复用该边界，在 `local-projection/v1` 中跳过同一 Vault 重复 owner triple，仅在 `vault check` 保留冲突诊断。替代方案是按路径排序或多数版本选择一个，会静默改变知识事实；不采用。跨 Vault 同名对象仍按 owner triple 独立保留。

本轮跨 Vault copy/move 调查（2026-08-30）：Git `mv`（Git 2.45.2，GPL-2.0，<https://git-scm.com/docs/git-mv>）保证单一工作树内移动成功后再更新 index，但不提供跨独立仓库事务或 owner 语义；git-annex（10.x，GPL-3.0，<https://git-annex.branchable.com/>）以 repository owner 和内容可用性分离传输/路径，适合离线内容复制但会引入远端配置和更复杂的对象协议。采用 `tools.vault_transfer.VaultTransfer` 的本地受控方案：显式 source/target Vault 与相对路径、source hash precondition、目标不存在、internal 内容不得降级到 public、`VaultLockGroup` 按稳定 Vault ID 顺序获取双锁；copy 只写目标，move 在目标 hash 验证后删除源，任一失败只清理本次目标文件并保留源。直接使用 `shutil.copy` 或按全局 `object_id` 猜 owner 会绕过确认、锁和 confidentiality，明确排除。离线运行不访问网络；操作记录只保留 operation/hash/owner 元数据，不写 private 路径到 durable audit，升级需重跑跨 Vault failure-injection 测试。

本轮 staging 故障恢复调查（2026-08-27）：Restic 0.17.x restore（BSD-2-Clause，<https://restic.readthedocs.io/en/stable/050_restore.html>）和 Borg 1.4 extract/check（BSD-3-Clause，<https://borgbackup.readthedocs.io/en/stable/usage/extract.html>）都把目标写入与源 snapshot 保留分开，失败不会删除来源；Git worktree（GPL-2.0，<https://git-scm.com/docs/git-worktree>）为独立 checkout 提供 owner 边界，但不提供跨仓库原子事务。替代方案是写入目标后立即删除源或依赖调用者清理，故障会留下丢失或双份状态。MyKnowledge 保留“目标原子写入并校验 hash，最后删除源”的顺序，并用故障注入验证源删除失败时目标回滚、源保留、双 Vault 锁释放；离线行为、operation 格式与 confidentiality 规则不变。
- Backstage Software Catalog（v1.32.0，Apache-2.0，<https://backstage.io/docs/features/software-catalog/descriptor-format>）：复用显式实体 ref/owner manifest、稳定排序和缺失实体可诊断的思路；限制是 Catalog 面向服务元数据，不提供 Markdown 正文保密或 public projection，因此只借用 manifest 形状，不引入其运行时。
- 替代方案：按 `object_id` 做全局字典覆盖，或把 private 内容复制到 public projection 后再过滤。两者在同名对象、Vault 故障和日志导出时都会读错 owner 或产生泄漏，明确排除。

本轮结论：新增离线、可重建的 `local-projection/v1` 生成器。每条记录始终带 `{vault_id, object_type, object_id}`，同名对象并存；可用 Vault 才提供正文和 content hash，不可用 Vault 只保留 Vault 级状态元数据。该生成器只为 `local`/显式 `private` 查询服务，public projection 仍由 public allowlist 生成器独立负责，绝不读取 private 正文。输出不含物理路径、remote、凭据或 private lineage。

### Manifest path security 增量调查（2026-08-30）

- Git worktree/submodule（Git 2.45.2，GPL-2.0，<https://git-scm.com/docs/git-worktree>）以真实 checkout root 作为 owner 边界；Python `pathlib.Path.resolve()` 可发现最终 realpath，但单独使用会把中间 symlink 静默跟随。
- 替代方案是只做最终 `relative_to(workspace)` 检查，或依赖 manifest 路径字符串判断安全；这两者都允许 `workspace/link/private` 通过并把 private checkout 伪装成声明路径。
- 本项目在 resolve 前逐组件拒绝 symlink（`path_symlink`），再执行 workspace containment、路径不重叠和 Git owner 检查。该检查纯离线，不改变 manifest 数据格式；升级 pathlib/Git 版本需重跑 symlink、overlap 和 direct/superproject 回归。

本轮 projection CLI 调查（2026-08-27）：Backstage Software Catalog descriptor（Apache-2.0，<https://backstage.io/docs/features/software-catalog/descriptor-format>）与 Click/Typer command groups（BSD-3-Clause/MIT）均采用稳定 manifest schema 和薄 CLI 编排；替代方案是 CLI 直接扫描 Vault 并自行序列化，会产生第二套 owner/冲突规则。新增 `python -m tools.cli local-projection` 仅调用 `VaultRegistry.write_local_projection()`，保持原子写入、owner 三元组和不可用诊断边界；离线不联网，升级只需重跑 projection/CLI parity 测试。

本轮 public projection 隔离调查（2026-08-27）：Git worktree/submodule 的独立 owner root（GPL-2.0，<https://git-scm.com/docs/git-worktree>）与 Backstage Catalog 的显式实体 owner/ref（Apache-2.0，<https://backstage.io/docs/features/software-catalog/descriptor-format>）都要求消费方从声明的仓库根和 owner 元数据读取；替代方案是从 workspace 父目录递归扫描所有 `vaults/*`，会把 private 正文和同名对象带入 public manifest。`PublicProjectionGenerator` 继续只扫描当前 public `wiki/` root，public allowlist/confirmation 由 public validator 判定；私有 checkout 仅由 Vault Registry 的 local/private projection 消费。该边界离线可重放、不读取相邻 private path，升级不改变 manifest schema。

## 2. 当前基线与目录

当前仓库是 `public` vault。每个 private repo 与 public repo 使用相同的对象目录和 schema 版本，但拥有独立 Git 历史：

```text
MyKnowledge-workspace/                 # 仅本机私有 workspace
├── public/                            # public repo checkout（当前仓库）
│   ├── sources/ wiki/ practice/       # practice 为 F008 预留
│   ├── archive/text/ archive/manifest.jsonl
│   └── config/vaults.example.yaml
└── vaults/
    ├── team-internal/                 # private repo checkout 或 submodule
    │   ├── sources/ wiki/ practice/   # practice 为 F008 预留
    │   ├── archive/text/ archive/raw/
    │   └── .git/
    ├── personal-private/              # 可选的第二个 private repo
    └── research-private/              # 可选的第三个 private repo
```

应用根目录仍可以直接运行 public repo。挂载配置是被忽略的本地 overlay：

```text
config/vaults.example.yaml       # 可提交，只含 public 示例和字段说明
config/vaults.local.yaml         # 不提交，含 private path/remote/ref/backup 配置
```

这里有两种等价部署形态：直接在当前 `MyKnowledge` checkout 中以 `public` vault 启动，并由 local manifest 指向外部 `vaults/*`；或者使用上面的私有 workspace superproject，把当前 checkout 放到 `public/` 后统一管理多个子仓库。后者只是管理层级，不改变 object ID、hash、发布和保密契约，也不是把 private 仓库复制进 public repo。

不把任一 `../vaults/*` 路径、私有 remote、用户名或 token 写入 public 生成物。private workspace 若需要固定子仓库版本，可以在 workspace superproject 中提交各 submodule 指针；public repo 不提交这些指针。

## 3. Vault manifest

启动时加载并规范化 manifest。路径先解析为绝对路径供本次进程使用，绝不写回对象、日志或 public artifact：

```yaml
schema_version: 1
layout: direct-checkout              # or superproject
workspace_root: null                 # resolved by the rules below
public_vault_id: public
vaults:
  - id: public
    path: .                          # current public checkout in direct mode
    type: git-checkout
    confidentiality: public
    required: true
    allow_public_projection: true
    expected_branch: main
    expected_commit: null
    provider_policy: public_allowed
    private_git_remote: null
    encrypted_backup_target: null
    backup_state: unconfigured
  - id: team-internal
    path: null                      # 仅在被忽略的 local manifest 中填写
    type: git-submodule
    confidentiality: internal
    required: false
    expected_branch: main
    expected_commit: null
    allow_public_projection: false
    provider_policy: internal_allowed
    private_git_remote: null
    encrypted_backup_target: null
    backup_state: unconfigured
  - id: personal-private
    path: null
    type: git-checkout
    confidentiality: internal
    required: false
    expected_branch: main
    expected_commit: null
    allow_public_projection: false
    provider_policy: internal_allowed
    private_git_remote: null
    encrypted_backup_target: null
    backup_state: unconfigured
```

每个 vault 的 `path`、remote、备份目标和 credential helper 都属于私有 workspace 的本地配置，不提交到 public repo；示例中的 private `path: null` 代表必须在 local manifest 中显式填写。`type` 只能是 `git-checkout`（独立 checkout）或 `git-submodule`（由私有 superproject 挂载）；submodule 的 `.git` 文件必须解析到该私有 superproject，不能指向 public repo。当前每个 private vault 都明确采用 `private_git_remote: null`、`encrypted_backup_target: null`、`backup_state: unconfigured`；这表示它只有本地 Git 工作副本，没有已验证的远端或备份链路。工具必须逐 vault 报告 `backup_not_configured`，不得自动猜测托管位置、自动 push，或把本地副本描述为“已备份”。普通读取、查询和可逆编辑可以继续；对某 vault 的 `purge`、覆盖式恢复等不可逆操作在该 vault `backup_state != verified` 时阻断，除非未来策略显式提供并记录风险确认。`backup_state` 只能取 `unconfigured`、`configured`、`verified`、`failed`，由检查/恢复报告派生，不能由作者手写。

路径解析算法固定为：

1. `layout: superproject` 时，`workspace_root` 必须是私有 superproject 根；`public.path` 通常为 `public`，其他 vault 为 `vaults/<id>` 或其明确相对路径。
2. `layout: direct-checkout` 且不挂载外部 vault 时，若 `workspace_root` 为 `null`，Registry 以当前 public Git worktree 根为 root，`public.path: .` 是唯一特殊值；只要挂载外部 private checkout，local manifest 就必须显式填写同时包含 public 与这些 checkout 的 `workspace_root`，并把 `public.path` 改为该 root 下的相对路径。
3. 所有路径先 `realpath` 再校验，必须位于 workspace root、彼此互不重叠；拒绝 `..`、绝对路径、跳出 root 的 symlink/hard-link，以及通过 Git submodule gitfile 指向 public repo 的路径。解析后的绝对路径只存在于本机诊断内存，不写入对象、日志或 public artifact。

这套规则消除了“`path: .` 到底指向 public checkout 还是 superproject 根”的歧义。启动时必须把规范化后的 `layout`、workspace root hash（不含路径正文）和每个 vault 的相对 path hash 纳入 `VaultCheckReport`，供 operation precondition 使用。

为保持 manifest 结构统一，`public` 示例也保留这三个字段并置为 `null`/`unconfigured`；它们在 public vault 上不代表 private remote，也不触发 private 数据备份告警。`backup_not_configured` 只针对包含 private 数据的 vault 以及涉及该 vault 的高风险操作。

状态语义按 vault 独立计算：`unconfigured` 表示该 vault 没有任何已配置的 backup target（remote 和 encrypted target 都为 `null`）；`configured` 表示至少一个 target 已填写、credential helper 只以 opaque reference 解析成功，但尚未完成最近一次完整验证；`verified` 表示**所有已配置 target** 的最近一次 manifest 完整性检查、audit chain 校验和隔离空仓恢复均通过；`failed` 表示最近一次上传、完整性、审计链或恢复尝试失败。只配置一个 target 仍可进入 `verified`，但报告必须列出未配置的另一个 target，不得声称双目标冗余。target 身份变化或验证过期回到 `configured` 并要求重新演练；任何失败回到 `failed`；删除所有 target 回到 `unconfigured`。状态只由检查/恢复报告派生，不能由作者手写为 `verified`。全局报告只做汇总（例如 `backup_summary.unverified_vault_ids`），不能用一个全局 `verified` 覆盖某个 vault 的失败状态。

durable backup manifest 固定写入 owner Vault 的 `audit/backup/<backup_id>.json`，外部 target 只保存该 manifest 的副本和其声明的 entries/LFS 对象；`state/` 中的临时报告不能替代它。manifest 的 `target_identity_opaque`、`encryption.key_ref_opaque` 和 credential helper 只保存不可逆引用，不保存 remote URL、密钥或 token。shared snapshot blob cache 即使按 `snapshot_sha256` 物理去重，也必须在每个 owner 的 manifest 中列出 `(vault_id, snapshot_sha256)`、恢复路径、权限和 hash，不能作为某个 Vault 唯一的备份对象。

每个 vault 在加载时必须通过：

1. 路径存在、是目录、不是 symlink 跳出 workspace；
2. Git worktree 可读，`git rev-parse --show-toplevel` 与 manifest 目录一致；
3. `HEAD`、branch/submodule 状态和 schema version 满足 policy；
4. vault 的所有对象有效 confidentiality 不得高于 vault 等级；允许 public projection 的 vault 出现 internal 声明立即失败；
5. `vault_id` 符合稳定标识符规则、除唯一 `public` 外不重复；对象 ID、文件路径和 archive owner key 在本 vault 内唯一；
6. 各 vault 的 realpath 不重叠，不能把 public checkout、另一个 vault 或 workspace 元数据目录作为子路径。

`expected_commit` 缺省时只记录实际 HEAD，不自动拉取；指定后不匹配将 Vault 状态标记为 `revision_mismatch`（诊断 code 同名），该 vault 查询可读但写入、验证和发布阻断，其他 vault 不受影响，等待用户显式选择 checkout/修改 manifest。

`required` 只表示命令的就绪门槛，不改变对象隔离：`required: true` 的 vault 不可用时，`vault check` 和明确依赖它的发布/恢复命令返回 blocked；不依赖它且没有跨 vault 引用的 public-only 读取或构建仍可继续。`required: false` 的 vault 不可用时默认产生 warning，并只阻断引用该 vault 的对象。任何命令都必须在结果中列出被跳过的 vault 和原因，不能用“部分成功”掩盖缺失数据。

### 3.1 Vault Registry 与 Projection Generator 契约

Registry 不把目录扫描结果当成配置。每次启动先解析唯一的 `vaults.local.yaml`，再输出不可变的 `VaultCheckReport`（canonical schema version `vault-check/v1`）；没有 local manifest 时只生成一个 `public` 条目，不自动发现 `../vaults`、Git submodule 或同名目录。local manifest 的 canonical schema 是 `vault-manifest/v1`（字段和枚举见 `config/schemas.yaml`），解析后的绝对路径只留在进程内。

```python
class VaultCheckReport(TypedDict):
    schema_version: Literal["vault-check/v1"]
    generated_from: str                 # public/workspace HEAD or tree hash
    vaults: list[VaultStatus]            # stable vault_id order, never collapsed
    conflicts: list[Conflict]
    affected_object_refs: list[ObjectRef]
    backup_summary: dict                 # unverified_vault_ids, states, no paths
    available_scopes: list[Literal["public", "local", "private"]]
    report_sha256: str
```

`VaultStatus` 至少包含 `vault_id`、state/reason、HEAD/expected revision 的摘要 hash、object count（不可用时为 `null`）、dirty/conflict flags、`backup_state` 和受影响 ObjectRef 数量；绝对 path、remote、submodule gitfile、credential helper 和 private object 标题只能在本机授权诊断中显示，不能进入共享 report。列表按 UTF-8 字节序的 `vault_id` 排序后再 hash。Registry 必须扫描所有声明条目，即使第一个 private vault 失败；单条失败只影响该 vault 和引用它的对象。

`generate_public_projection` 是独立的 public-only generator，不从 `queries/local` 过滤，也不接受任意 `vault_ids` 参数：

```python
class PublicProjectionGenerator(Protocol):
    def preview(self, registry: VaultCheckReport) -> PublicProjectionPreview: ...
    def apply(self, operation_id: str, confirmation: PublicConfirmation) -> PublicProjectionManifest: ...
```

实现步骤固定为：

1. 只打开 `vault_id == public`、`allow_public_projection == true` 且 state 为 `available` 的 checkout；private checkout 即使已挂载也不是 public generator 的输入。
2. 重新计算 public Wiki 的 semantic/content/evidence/validation/attestation 和 effective confidentiality；作者手写的 `public_publishable`、`public_release`、`vault_id` 一律忽略或报告 `derived_field_mismatch`。
3. 仅保留 `status: published`、`publication_scope: public`、`effective_confidentiality: public`、`validation_state: pass`、`evidence_state: supported|corroborated` 且当前人工 confirmation/hash 全部匹配的对象。每个对象生成 public-safe body、附件清单、Wiki-to-Wiki object-ID links、`release_input_sha256`、输入 leak 摘要和 `public_confirmation_path`。
4. 生成前执行对象/路径/附件/active-content 校验；生成后由 `prepare-content`、graph、Pagefind 和最终 dist leak gate 再验证。任一 registry conflict、cross-vault reference、attestation 缺失、confirmation 失效或 leak finding 都使该 item 不进入 manifest；若命令要求全局一致性则整个 operation blocked，默认不把 private 缺失伪装成“没有页面”。
5. 输出 `queries/public/manifest.json` 及其 `manifest_sha256`。manifest 只含 public-safe 字段；private lineage 只在 generator 所属 private audit 中保留不可逆 commitment，不能写 `source_vault_ids`、private ID、snapshot exact 或路径。

Generator 的 preview 必须返回被纳入/排除的 ObjectRef、每个排除原因、registry report hash、输入 leak 摘要和人工确认 nonce；apply 再读取 registry report/hash，避免在挂载集合变化后复用旧 preview。它不执行 commit/push、不会自动初始化 submodule，也不会为了生成 public 页面读取 private 正文。

## 4. 对象空间与引用解析

### 4.1 合并规则

`VaultRegistry` 先按稳定 `vault_id` 排序，再逐 vault 扫描对象并建立：

```text
object_index[(vault_id, object_type, object_id)] =
  {
    vault_id,
    object_type,
    object_id,
    path,
    confidentiality,
    content_sha256,
    availability,
    availability_reason,
    state: available | unavailable | conflict | invalid
  }
snapshot_index[(vault_id, snapshot_sha256)] =
  {
    vault_id,
    snapshot_sha256,
    archive_path,
    media_type,
    availability,
    availability_reason,
    confidentiality,
    owner_object_ref,
    physical_blob_key: snapshot_sha256,
    deduplicated: true | false
  }
```

对象 ID 在所属 Vault 内命名；完整对象引用键是 `(vault_id, object_type, object_id)`。两个 private Vault 可以拥有相同的 `wiki_id`/`source_id`，因为它们是独立知识对象且默认不会互相引用；只有同一 Vault 内的重复键才是阻断级冲突。合并查询必须始终返回 `vault_id`，不能按 manifest 顺序覆盖同名对象。相同 `snapshot_sha256` 跨 vault 出现不构成对象冲突：默认每个 Vault 的 `archive/manifest.jsonl` 都保留 owner record 和可恢复路径；启用 physical dedup 时，`physical_blob_key` 指向 workspace 的内容寻址缓存，但该缓存是派生物、不可单独作为备份，也不能绕过 owner 权限。去重只发生在不可变 snapshot 字节层；知识对象、source 语义、证据关系和发布状态仍按 owner 独立计算，不能因为文本相同就推断知识等价或自动合并。`snapshot_sha256` 单独不能授予读取权限，任何 resolver 必须同时收到 `vault_id`（或明确的 owner 集合）。

默认引用必须在同一 Vault 内解析：Wiki、Evidence 和 Source 的 owner `vault_id` 必须一致。canonical Markdown 只记录带字段类型约束的相对 owner ID（`sources` 只能是 source ID，`related` 只能是 wiki ID，`part_of` 只能是同类 source ID）；领域层解析后统一扩展为完整 `ObjectRef`，不写物理路径。规范化 evidence hash、验证报告和索引必须保存解析后的 `resolved_object_ref`，防止同名 ID 在不同 Vault 间替换。API、报告、索引和错误诊断必须使用完整 `ObjectRef`。若输入显式指定了不同 `source_vault_id`，或解析结果只能落到另一个 Vault，写入/校验立即报告 `cross_vault_reference` 并拒绝 operation；`source_vault_id`/`target_vault_id` 只用于拒绝诊断、public release lineage 和多 Vault operation，不表示允许建立跨库内容依赖。

Registry 的确定性合并步骤固定为：

1. 读取 manifest，拒绝重复 `vault_id`、缺少保密等级、未知 `type`/`provider_policy` 和除唯一 `public` 外的 public projection owner；
2. 按 Unicode/ASCII 稳定排序后的 `vault_id` 逐个检查路径、Git HEAD、schema、dirty 状态和备份状态；某一步失败只写入该 vault 的 `VaultStatus`，不短路扫描其他 vault；
3. 对可扫描 vault 建立临时 object/snapshot owner 表，只有同一 `(vault_id, object_type, object_id)` 重复时才生成 `conflict`；发现相同 snapshot hash 时合并内容地址但追加 owner；
4. 解析引用时校验 source/target owner `vault_id` 必须一致；发现 private-to-private 或 public-to-private 引用时拒绝 canonical operation 并保留诊断，不把它改写成 missing；
5. 先生成 local/private projection，再用只允许 `vault_id == public` 的独立 allowlist 生成 public projection。任何 registry error、冲突或跨 Vault public 引用都只能阻断受影响对象，除非命令明确要求全局一致性；
6. 输出 `VaultCheckReport`：包含逐 vault 状态、冲突清单、受影响对象集合、`backup_summary.unverified_vault_ids` 和可继续执行的 scope。报告 hash 作为后续 operation 的 precondition，防止在 vault 集合变化后复用旧 preview。

### 4.2 未挂载和不可读

manifest 中声明但当前不可访问的每个 private vault 生成独立的 `VaultStatus`（canonical schema version `vault-status/v1`）：

```yaml
vault_id: team-internal
state: unavailable       # unavailable | revision_mismatch | dirty | conflict | invalid | available
reason: submodule_uninitialized
checked_at: 2026-08-26T00:00:00Z
object_count: null
affects_object_ids: []
```

该 vault 的对象不能被扫描出正文，因此不会出现在 public catalog；如果已有历史对象记录指向它，查询结果保留引用元数据，派生 `availability: unavailable`、`validation_state: unavailable` 和阻断码 `upstream_unavailable`，而不是把 `evidence_state` 改成 `missing`。新的跨 Vault canonical 引用不能在不可用时创建。没有引用该 vault 的查询、索引和 private projection 仍可继续处理其他可用 vault。`required: true` 只改变需要该 vault 的命令退出门，不把整个 registry 的所有对象强行标记为 unavailable。

如果任一对象引用了另一个 private vault 解析的 source/wiki ID，合并器报告包含 `source_vault_id`、`target_vault_id` 和 `cross_vault_reference` 的诊断，并拒绝该 canonical operation；public 对象引用 private source 时同样拒绝，而不是等到 public projection 才过滤。历史诊断仍可读，不能通过删除 ID、把 unavailable 改成 missing 或把目标改到另一个 vault 来绕过保密边界。

状态转换：

```text
unmounted -> unavailable -> available (用户挂载并重新 check)
                         -> unavailable (再次失败)
revision_mismatch/dirty/conflict -> available (用户修复并重新 check)
```

恢复某个 vault 后重新读取相同 ID/hash，自动解除该 vault 的 `unavailable` 并使受影响验证报告按 hash 重新判断；不自动改写 Wiki 或发布状态，也不重建无关 vault 的状态。

### 4.3 权限传染

`effective_confidentiality = max(self, all upstream source/wiki)`；F008 题目若启用，再由其独立规则继承所属 Wiki。若 public wiki 引用任一 private vault 的 source，校验器必须拒绝其 `public_publishable`，并提示迁移到目标 private vault 或创建脱敏 public claim。private vault 未挂载时不能通过“删掉引用”来降级；多个 private vault 的等级和引用按各自 `vault_id` 传播。

## 5. 子仓库挂载、同步和恢复

应用只做只读检查和明确的用户确认，不自动执行有远程副作用的 Git 命令。建议流程：

```text
validate_vault_manifest
  -> inspect worktree / HEAD / submodule status
  -> build merged object index
  -> preview operation (显示 vault、hash、confidentiality)
  -> user confirms
  -> writer 在目标 vault 内原子写入
  -> 用户自行 commit/push
```

用户执行一个或多个 submodule clone/update 后，再运行 `vault check`；工具按 `vault_id` 分组报告当前路径（仅本机诊断）、HEAD、期望 ref、dirty files、schema、对象数量和可用性。dirty private worktree 不阻断只读查询，但阻断会覆盖该 vault 已有文件的 apply，除非 operation 明确列出该 vault 并得到确认。

恢复策略：

| 故障 | 读取行为 | 写入行为 | 恢复 |
| --- | --- | --- | --- |
| 某 vault 目录不存在 | public 和其他可用 vault 可读，该 vault 对象 unavailable | 该 vault 写入阻断；无关 vault 不受影响 | 挂载/修正该 vault 的 local manifest |
| 某 submodule 未初始化 | 同上，给出该 vault 的 `git submodule update --init` 建议 | 该 vault 阻断 | 用户执行命令后重新 check |
| 某 vault HEAD 与 expected_commit 不同 | 该 vault 可读但标记 revision mismatch，其他 vault 可用 | 该 vault 写入/发布阻断 | 用户选择更新 manifest 或 checkout |
| 某 vault dirty worktree | 该 vault 可读 | 覆盖该 vault 相关文件阻断 | 用户提交、清理或显式确认冲突处理 |
| 某 Git 仓库损坏 | 不读取该 vault 正文，其他 vault 正常 | 该 vault 阻断 | 若该 vault 已配置并验证，从其 remote/备份恢复；未配置时报告无恢复目标，工具不 reset |
| 同一 vault 内 ID 冲突 | 冲突对象不进入合并投影，无关对象仍可读；不同 vault 的同名对象保留各自 owner | 阻断所有引用冲突对象的 apply | rename/migrate 后重建索引 |
| 任意 vault remote/backup 未配置 | 本地 vault 可读，逐 vault 标记恢复能力 unavailable | 对受影响 vault 的 `purge` 和覆盖式恢复阻断 | 先为该 vault 配置目标、验证连通性并完成恢复演练 |

## 6. Private projection 与发布告警

### 6.1 Projection

`queries/local`（本地生成物）包含全部已挂载且允许本地读取的 private/public vault 的 source、wiki 和其他当前版本允许索引的 metadata/正文；每条记录保留 owner `vault_id`。无法读取的对象只保留 `availability`、`availability_reason`、owner 和 hash 元数据，不进入正文/FTS/RAG chunk；直接读取时返回结构化 `unavailable`，不伪造空正文。不再定义单独的 `queries/private` 目录，避免在不同文档中产生两套索引路径。`queries/public` 只由 `public_publishable` 计算，不能通过过滤 local index 反向生成，避免把任一 private vault 的 ID、数量或存在性泄漏到 public。

private/local projection 的每条记录必须包含：`vault_id`、`object_id`、`confidentiality`、`publication_scope`、`availability`、`evidence_state`、`validation_state`、`content_sha256` 和 `generated_from`。public projection 的 allowlist 必须同时满足 `vault_id == public`、`allow_public_projection == true`、有效保密等级为 `public` 以及全部 public 门禁；不能通过只排除某个名为 `internal` 的 ID 实现保密。public projection generator 只依赖 public-owned body、public-safe confirmation 文件和已提交的 attestation 摘要，不要求在 CI checkout 任一 private vault。

### 6.2 Internal private publish operation

发布请求不能只改 front matter。`publish_private` operation 的 preview 至少展示：

```yaml
operation: publish_private
target: wiki/example
target_vault: team-internal     # 必须是 manifest 中实际存在的 vault_id
effective_confidentiality: internal
wiki_content_sha256: "sha256:..."
wiki_evidence_sha256: "sha256:..."
upstream_snapshot_hashes: ["sha256:..."]
validation_state: pass
publication_warning:
  code: INTERNAL_CONTENT
  text: "该内容包含内部资料，只会进入私有投影，不得转发或公开发布。"
requires_confirmation: true
requires_warning_ack: true
```

Apply 必须要求同一 operation id 的 `operation-confirmation/v1`，且 `scope: publish_private`；有效保密等级为 `internal` 时该事件还必须携带 `warning_code` 与 `warning_text_sha256`。`target_vault` 必须明确、可用、满足 policy 并等于对象 owner `vault_id`；不能默认填入 `internal`。首次创建或跨 Vault 迁移时由 source/wiki write 或显式 copy/move operation 选择 owner，不能用 publish operation 隐式复制。持久事件写入目标 private vault 的 `audit/operations/<operation_id>.json`，并保存 `target_ref`、当前 content/evidence hash、confirmation event hash 和 `after_sha256`；完整临时响应可写入被忽略的 `state/operations/`，但不能只保留后者。页面、API、Agent 查询结果使用 `publication_warning: internal` 和醒目文案，并返回实际 `vault_id`；不把 warning 当成"已安全"的证明。

### 6.3 Public release 与人工审核

`public_release` 是独立 operation，输入可以是重新分类的 public copy 或人工脱敏后的新 Wiki。它默认是 `false`，且不是 Wiki Front Matter 的权威字段；projection generator 必须从 `release/public-confirmations/<event_id>.json` 与 public owner 的 `audit/operations/<operation_id>.json` 重新派生。人工查看固定 hash 的完整输入材料（正文、公开 metadata、lineage、evidence 绑定和输入 leak-gate 报告）后，才能创建匹配当前 hash 的 confirmation event。确认后构建器还会独立扫描最终 dist；最终扫描失败会阻断本次发布，但不要求把尚未生成的 dist 报告预先写入人工事件。人工开关不能由“人工脱敏已执行”、LLM verdict、自动 leak gate、Front Matter 或 manifest 字符串替代。缺少 durable event/operation、nonce 已消费、actor 非 human、owner 非 public 或任一 hash 不匹配时一律派生为 `false`；输入 hash 变化后旧事件保留但不能复用。

状态机如下：

```text
prepared -> public_release: false -> human sets true -> apply -> public projection
                         |                         |
                         +-- output hash changed -> false
```

`public_release` operation 的审核记录至少包含：

```yaml
public_release: false
public_release_actor: null
public_release_at: null
release_input_sha256: null
reviewed_content_sha256: null
reviewed_evidence_sha256: null
leak_gate_report_sha256: null
leak_gate_report_scope: input-item
public_confirmation_sha256: null
public_lineage_commitment: null     # sha256 of the lineage record path; no key material
actor_type: null                   # only human may approve public release
source_vault_ids: [team-internal, research-private]
operation_id: "op_..."
```

上面的 `source_vault_ids` 只存在私有 operation/audit record；生成 public-safe event 或 projection 时必须删除该字段并重新跑 allowlist/leak gate。`public_confirmation_sha256` 始终等于 public-safe event 的 `event_sha256`，不能填另一份未落盘的摘要。

`public-release-confirmation/v1` 是 append-only 事件，至少包含 `event_id`、`operation_id`、`target_ref`（必须是 public-owned object）、`actor_type: human`、符合安全 pseudonym 格式的 `actor_id`、`decision: approve`、`release_input_sha256`、`reviewed_content_sha256`、`reviewed_evidence_sha256`、`leak_gate_report_sha256`、`confirmed_at`、不含 URL/路径/private lineage 的短 `reason`、`confirmation_nonce` 和 `event_sha256`；若出现 `target_vault` 必须为 `public`。nonce 必须由 preview 生成并且只允许消费一次；消费结果（operation、nonce、event hash、`consumed_at`）必须写入 durable operation record，不能只依赖可清理的 state。事件文件不能由 Agent/LLM/CI 自动创建。public-safe 事件可以提交到 public repo，但必须经过同一人工作流的人工 code review/commit，不能把“对象字段被改成 true”视为确认事件。该约束是流程门禁，不是密码学身份认证；非交互/CI 进程必须被 confirm 命令阻断。

只有明确的人类操作者可以为当前 `release_input_sha256` 产生可派生为 true 的 confirmation；Agent、LLM、CI 和 leak gate 只能生成待审材料。最简单的实现是由人工执行一次 `public-release confirm --operation-id ...`（或等价 UI 操作），writer 在同一个 apply 中写入 `actor_type: human`、确认时间、确认事件 hash 和 `public_confirmation_sha256`，projection 再根据 durable record 派生 `public_release`。Apply 前重新比较 release/content/evidence/leak-gate hash，并要求该事件仍匹配；任一 hash 变化时自动重置为 `false`，不得部分发布。完整审核记录写入源 private vault 的 `audit/operations/<operation_id>.json`；public-owned 的脱敏确认事件写入 public repo 的 `release/public-confirmations/<event_id>.json`，字段只包含 operation/release hash、人工 actor、时间、理由摘要、event hash 和 decision，不包含 private ID、路径或正文。public artifact 只保留 `public_lineage_commitment` 和 `public_confirmation_sha256`。

审核前的准备仍必须：

1. 证明输出已成为 `vault_id: public` 的独立对象，`sources`/evidence/Markdown links 不含任何 private ID，且每个 claim 重新绑定 public-owned source/snapshot；private lineage 只保存在审计记录和不可逆 commitment 中；
2. 重新计算 effective confidentiality、evidence bindings、content/evidence hash；
3. 重新执行 deterministic/LLM validation 和 public leak gate；
4. 保存原对象与输出对象的 lineage 以及 `source_vault_ids`，但 public artifact 不暴露 private ID、路径或正文；
5. 生成 `public_release: false`，展示 diff、证据、保密等级、leak-gate 报告和已知风险；
6. 人工通过交互式 `public-release confirm --operation-id ...` 消费一次性 nonce；writer 将 event 和 operation durable record 写入 owner Vault 后重新派生当前 `public_release`，只有派生为 `true` 才可进入 `queries/public`。

## 7. Internal LLM provider 边界

Provider 由 Codex/Claude Code 加载的 MyKnowledge Skill 在运行时提供。用户无需为具体 endpoint、模型版本或密钥读取方式做设计决策；这些属于 Skill 的 provider/runtime adapter 实现细节，不写入 Vault manifest、Git、public artifact 或普通审计日志。按 ADR-0010，LLM 规范审计是可选层，因此不做 capability 协商；runtime 只需保证不把 internal 正文交给不满足保密要求的 provider。

任一 internal source 没有满足保密要求的 provider 时，只将引用它的对象记为 `validation_state: not_run` + `not_run_reason: provider_unavailable`，不影响不引用它的其他 vault，也不自动降级到 public provider。这不阻断发布：确定性校验通过并取得人工审计确认后仍可发布，页面显示"未做语义审计"。请求日志只保存不含秘密的 opaque provider identity、输入 hash、vault_id 集合、耗时和结果状态；禁止记录 endpoint、密钥、Authorization header、完整请求正文或响应正文。

## 8. 接口契约

领域层提供只读接口，供 CLI/FastAPI/Skill 共用：

```python
class VaultRegistry:
    def check(self) -> VaultCheckReport: ...
    def resolve(self, vault_id: str, object_type: str, object_id: str) -> ObjectRef: ...
    def resolve_snapshot(self, vault_id: str, sha256: str) -> SnapshotRef: ...
    def projection(
        self,
        scope: Literal["public", "private", "local"],
        vault_ids: Sequence[str] | None = None,
    ) -> Projection: ...
```

`VaultCheckReport` 必须包含每个 vault 的独立状态、错误和 `backup_state`，并提供按对象聚合的影响集合；全局结果只能是汇总，不能抹平单 vault 状态。`ObjectRef` 必须包含 `vault_id`，对象 `availability` 只表示 `available`、`unavailable`、`conflict`、`invalid`，具体原因放在 `availability_reason`（如 `revision_mismatch`、`dirty`、`path_unresolved`）；snapshot resolver 也必须按 owner vault 解析，不能仅凭 hash 在多个 owner 中猜测。Skill/CLI/FastAPI 不允许自行拼接路径；所有写操作必须把明确的 `vault_id` 和 precondition hashes 交给 writer。涉及多个 vault 的 public release lineage 或 registry operation 必须声明 source/target vault 及失败后的 staging 处理，但不得创建 private-to-private 内容引用。

`scope: public` 忽略调用方传入的 private `vault_ids`，始终使用唯一 public allowlist；`scope: private` 必须显式限定一个或多个 internal vault，`scope: local` 才允许缺省为全部当前可用 vault。限定 scope 不能绕过冲突、保密传染或 unavailable 状态，只能减少本次读取范围。

## 9. 安全和路径边界

- 拒绝 `..` 穿越、绝对路径、符号链接跳出 vault、hard-link 指向 vault 外文件和 archive path 重定向；
- 任一 private path、remote URL、submodule gitfile 和 private object ID 不进入 public generated JSON、sitemap、HTML、日志和错误页面；
- public CI 不 checkout private submodule，不读取 private credentials；
- public leak gate 在输入、staging 和 dist 三处扫描；命中 internal front matter、内网域名、private path 或 private hash 均失败；
- 归档原文只存 private vault，Wayback 和 public archive provider 明确拒绝 internal；
- 所有写入 preview 显示目标 vault 和 confidentiality 来源，避免用户误以为写入 public。

## 10. 幂等、并发和失败恢复

operation key = `sha256(canonical_json({kind, target_ref, input_hash, target_vault, source_vault_ids: sorted(...), policy_version}))`。同一 key 重试返回原结果；hash 变化生成新 operation。每个 vault 各自持有写锁；涉及多个 vault 的 operation 按稳定 `vault_id` 升序获取锁，避免死锁。跨 vault 操作不做伪事务：先在 staging 生成并校验全部相关 manifest，再由用户确认，任何一边 apply 失败都保留 staging、已成功 vault 列表和恢复说明，不自动回滚另一仓库的用户变更。

索引和 projection 采用临时目录 + fsync + 原子 rename。失败时保留上一版本及其 manifest/hash；不得删除旧 dist、旧 local index 或 private backup。

## 11. 可观测性

记录 `operation_id`、`vault_id`（跨 vault 操作记录排序后的 ID 集合）、HEAD、schema version、输入 hash、对象 ID、availability、阶段、耗时和错误 code。日志禁止正文、selector exact、内网 URL、凭据和 private path；诊断界面可在本机授权后显示完整路径，不写入共享 artifact。指标至少包含：按 vault 的挂载成功率、unavailable 对象数、ID 冲突数、相同 snapshot hash 去重数、private publish warning 次数、public leak gate 失败数、每个 vault 的 `backup_state`、备份最近成功时间（未配置时为 `null`）和恢复演练最近结果。

## 12. 测试策略

- manifest schema、vault 等级和 `allow_public_projection` 位置校验；
- 无 private vault 时 public-only 兼容路径，以及直接 checkout 与私有 workspace superproject 两种目录布局；
- 两个或更多 private vault 同时挂载，按 ID 合并和独立状态报告；
- 任意两个 vault 同 ID、相同 snapshot hash 去重、private-to-private 引用拒绝和 unavailable 语义；
- 一个 vault 不可用时另一个 vault 仍可查询和生成不相关 projection；
- 每个 submodule 未初始化、HEAD 不匹配、dirty worktree、损坏仓库和独立恢复；
- 路径穿越、symlink/hard-link、private URL/path/ID 泄漏扫描；
- 按 vault policy 的 internal provider 选择、public provider 拒绝和 provider unavailable；
- private publish 必须 confirmation + warning ack，缺一阻断；
- public release 重新 hash/验证，经过人工审核且不能从 internal 直接投影；
- public release 的人工开关、操作者、时间、理由和 hash 绑定记录可回放；
- 每个 vault remote/backup 未配置时产生带 `vault_id` 的 `backup_not_configured` 告警，只有相关 vault 配置并验证后才可通过恢复验收；
- 幂等 apply、按稳定 vault ID 排序的并发锁、跨 vault staging 失败和旧索引保留；
- 从备份恢复后 object/snapshot hash 与原 manifest 一致。

## 13. 迁移与回滚

先创建空 private repos 和 manifest example，再为每个目标 vault 迁移一份 internal fixture；验证各自 private projection、告警和 leak gate 后再导入真实资料。迁移不移动 public 文件，不改旧 ID；发现同一 vault 内冲突或显式跨 Vault 内容引用时暂停受影响对象并生成诊断清单，其他不相关对象仍可迁移。回滚只需卸载指定 vault 或恢复其已知 commit，public repo 及其他 private vault 的 schema 和 projection 不回退。

## 14. 部署参数与后续决策

- private Git remote：每个 private vault 均为 `null`（TBD，尚未选择托管位置）；
- encrypted backup target：每个 private vault 均为 `null`（TBD，尚未选择备份位置/工具）；
- 在上述参数按 vault 确定前，各 vault 的 `backup_state` 保持 `unconfigured`，不声称备份链路就绪；启用某个 vault 的门槛是为该 vault 配置、完成最小权限校验、一次备份和一次空仓恢复演练；
- 审核界面的视觉形态可以后续调整，但人工开关、操作者、hash 绑定、public confirmation 和 hash 变化自动重置属于本设计的必需实现。
