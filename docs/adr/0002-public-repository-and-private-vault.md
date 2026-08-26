# ADR-0002：公开仓库与 Private Vaults（0..N）

- 状态：Accepted
- 日期：2026-08-26
- 相关规范：SYS、SEC、SRC、ARC
- 相关 Feature：F007、F011、F012

## 背景

MyKnowledge 的公开仓库用于发布个人知识 Wiki，但 Source、归档快照、题目解析和验证报告可能包含内部资料。Git 历史、CI 日志、构建缓存和静态资源都可能造成泄漏；仅在 `dist/` 扫描或依赖作者自觉删除文件都不够。

同时，内部资料仍然需要完整的 source-first、snapshot、claim 验证、检索和私有发布流程。把内部内容复制到另一套数据库会产生 ID、hash、状态和备份分叉，不能满足一次性交付和可恢复要求。

## 候选方案

### A. 所有内容留在公开仓库，以加密文件或 `.gitignore` 隔离

实现最简单，但密文、文件名、提交时间、误提交历史和 CI 解密过程仍可能泄漏；一旦明文进入 Git 历史，后续删除无法可靠修复。不能作为默认方案。

### B. 独立私有 Git 仓库，按可插拔 Vault 挂载（选定）

public repo 和每个 private repo 各自拥有完整 Git 历史和对象目录。运行时由 Vault Registry 合并 `public + 0..N` 个 vault 的对象空间；对象 ID 和 snapshot 都按 owner `vault_id` 解析，完整键分别是 `(vault_id, object_type, object_id)` 和 `(vault_id, snapshot_sha256)`，未挂载的 private 对象表示 `unavailable`。每个外部仓库都是独立 owner，可以单独挂载、检查、备份和恢复；一个 vault 的故障不应拖垮与其无关的 vault。本地私有 workspace 可以管理任意数量的并列仓库；必要时再由该私有 workspace 使用 Git submodule 固定各 private repo 的 commit。

### C. 在公开仓库提交 private repo 的 Git submodule 指针

submodule 本身不包含正文，但会暴露私有仓库 URL、仓库名、commit 时间和拓扑，公共克隆还会产生“子模块不存在”的噪声。只有用户明确接受元数据泄漏时才允许采用，并且指针只能出现在私有 workspace 或单独的私有发布分支；public main 默认不携带该指针。

### D. 外部知识库或加密云盘作为 canonical store

能减少本地磁盘管理，但无法保证离线复核、内容寻址和 Git review；服务可用性、权限和导出格式也会成为新的硬依赖。可以作为备份目标，不能作为第一事实源。

## 决策

采用方案 B，并保留方案 C 作为私有 workspace 的可选挂载方式：

1. public repo 只存 `confidentiality: public` 对象、公共投影和不含私有路径/URL 的 schema/policy。每个 private repo 都是独立的私有 Git 仓库，目录结构与 public vault 对齐：`sources/`、`wiki/`、`practice/`、`archive/`、`queries/`。
2. `config/vaults.example.yaml` 只描述 public vault 和可复制的字段模板。真实挂载路径、每个 vault 的 private remote、备份目标和 credential helper 写入被 `.gitignore` 忽略的 `config/vaults.local.yaml`，或写入私有 workspace 配置；不得把绝对路径、私有 URL、访问令牌写入 public repo。当前每个 private vault 的 Git remote 与加密备份目标尚未决定，必须逐 vault 显式保持 `null`/`unconfigured`，不能用假地址表示“已配置”。
3. 推荐的本地布局是私有 workspace superproject 管理一个 public repo 和任意数量的并列 private repo：

   ```text
   MyKnowledge-workspace/       # 私有、不发布
   ├── public/                  # public repo
   └── vaults/
       ├── team-internal/      # private repo，或其 submodule checkout
       ├── personal-private/   # 可选的第二个 private repo
       └── research-private/   # 可选的第三个 private repo
   ```

   如果需要固定 private repo 版本，submodule 指针只提交到该私有 superproject。public repo 不提交任何 private submodule 指针，避免仓库身份和路径泄漏。
4. 启动时读取 Vault Registry，验证每个 vault 的 `id`、Git worktree、expected branch/commit、schema version、confidentiality、provider policy 和独立备份状态。`public` 是保留 ID；外部 vault ID 必须稳定且全局唯一。对象 ID 只需在所属 Vault 内唯一，完整引用按 `(vault_id, object_type, object_id)` 解析；不同 private Vault 的同名知识对象保持独立，不把物理路径写入 Source/Wiki。
5. 任一 private vault 未挂载、分支不匹配或工作树不可读时，只将该 vault 标记为对应 `VaultState`，其对象使用 `availability: unavailable` + `availability_reason`；其他 vault 仍可查询和生成不依赖故障 vault 的投影。历史上引用故障 vault 的 Wiki 保留引用元数据，派生 `validation_state: unavailable`，并保留最近一次可计算的 `evidence_state`（从未成功计算时才为 `unresolved`）；新的跨 Vault 内容引用在写入/校验阶段直接拒绝。
6. internal 内容确认后可以在其实际目标 private vault 的 projection 进入 `published`，但 Apply 前必须展示不可忽略的 internal 告警，并在 `operation-confirmation/v1`（`scope: publish_private`）中保存 `warning_code`、`warning_text_sha256`、当前 wiki/evidence/source hash、操作者、时间和 `target_vault`。告警是用户可见的安全信号，不是可被静默跳过的提示。
7. internal 内容永远不自动进入 public projection。对外发布必须是单独的 `public_release` operation，默认 `public_release: false`；经过人工脱敏或重新分类、全量 evidence 复核和 public leak gate 后，只有人工为当前 hash 创建新的 public confirmation，projection 根据 durable event/operation record 派生 `public_release: true` 才能发布。不能仅修改 `publication_scope` 绕过有效保密等级传染；自动化、LLM 或 Agent 不能产生该人工事件或直接写入该派生字段。
8. internal source 不发送到 Wayback 或 public LLM provider；只能发送给 Skill runtime 按 capability 声明为 `internal_allowed` 的 provider。endpoint、模型版本和密钥由运行时 Skill 管理，不进入 manifest、Git 或普通审计日志。Skill 未提供合规 provider 时保持 draft/review/unavailable，不使用公开 provider 兜底。
9. 每个 private vault 独立保存 `private_git_remote: null`、`encrypted_backup_target: null` 和 `backup_state: unconfigured`，不使用全局单一备份状态。未配置时仍可进行本地读取和普通可逆写入，但工具必须逐 vault 告警；对受影响 vault 的不可逆 `purge`、覆盖式恢复和清理默认阻断，直到该 vault 目标配置并完成一次恢复演练。多 vault 操作只要涉及任一未验证 vault 就必须汇总告警并阻断高风险步骤。目标启用后，备份 manifest 只记录 object ID、snapshot hash、vault ID 和版本，不把内部正文复制到 public backup。

## 关键不变量

- 任一 `allow_public_projection: true` 的 vault 出现 `confidentiality: internal`、内网 URL、private path 或 private object ID 即阻断提交和构建；当前只有 `vault_id: public` 允许进入 public projection。
- 任一 private vault 的卸载不能破坏 public repo 或其他可用 vault 的可读性，也不能把该 vault 的对象误判成不存在。
- `private_publishable` 仅在 `status: published + publication_scope: private`、验证通过、显式确认和告警确认同时存在时成立；不引入额外的私有发布 status。
- `backup_state: unconfigured` 必须可见且不能被解释为已备份；没有经过验证的恢复链路不得作为“可恢复”发布条件。
- 任何 public projection 都不包含 source/archive/practice answer/validation report 的正文或可推断 private 对象存在性的信息。
- `public_release` 只有在当前输出 hash 绑定的人工开关为 `true` 时才可 Apply；默认 false，hash 变化自动重置为 false，不得进入 public projection。
- Canonical Source/Wiki 只能引用同一 owner Vault；跨 Vault copy/move 生成新 owner 对象，原始 `source_vault_ids` 只进入私有 lineage/audit，不成为内容引用。
- private vault 的 Git 状态异常不允许静默覆盖、自动 reset 或自动 push；恢复必须由用户确认。

## 后果

优点：内部内容仍使用同一套 schema、hash、验证和查询契约；public repo 的泄漏面更小；每个 private repo 在各自远端/备份目标配置后可独立备份、审查和回滚；未挂载及未配置备份场景都有明确降级语义，单仓库故障不会扩大影响面。

代价：需要维护 Vault Registry、跨仓库 ID 检查、私有 workspace 和按 vault 聚合的索引/备份状态；用户必须理解 public/private 发布是两个不同操作并明确选择目标 vault；多个 Git submodule 的 clone/update 失败需要逐一诊断。

## 重新评估条件

出现多用户协作、需要服务端权限继承、private vault 规模超过本地 Git/备份边界，或需要跨仓库事务提交时，重新评估 Git vault 是否仍是合适的 canonical store。
