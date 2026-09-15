# ADR-0019：门禁收敛 = git 作为审批，只保留能捕获真实缺陷的门禁

- 状态：Accepted
- 日期：2026-09-14
- 相关规范：OPS、VAL、SEC、WIKI、CHN
- 相关 Feature：F003、F004、F007、F011、F012
- 相关 ADR：ADR-0006、ADR-0010、ADR-0015、ADR-0017
- 取代目标：标记 **ADR-0006**（Preview/Apply 写协议）为 Superseded —— 该协议已在代码中完全删除（`tools/write_operation.py` / `operation_store.py` / `vault_lock.py` 及其 CLI/API 入口与测试，2026-09-15）。**ADR-0010 / ADR-0014 / ADR-0015 本次不标 Superseded**：它们的实现仍在运行（`audit` / `confirm` / `release` / `override` 命令与 `release_confirmation.py` / `release_input.py`；`tools/layers.py` 的分域约束；`tools/validation/override.py`），标为 Superseded 会与代码相反。待"命令面收敛"在该三份 ADR 覆盖的范围内落地后再标。

## 背景

现有审批体系由四类 hash 绑定的人工确认事件 + 一套 operation 状态机构成：

| 确认机制 | 产生者 | 绑定对象 |
| --- | --- | --- |
| `--confirm` 布尔开关 | 各 apply CLI | 无 |
| `operation-confirmation/v1`（scope=apply/publish_private） | `cli confirm-apply` | input_hash + diff_hash |
| `operation-confirmation/v1`（scope=publish，人工审计确认） | `cli confirm` | content_sha256 + evidence_sha256 + deterministic_report_sha256 |
| `public-release-confirmation/v1` | `cli release confirm` | release_input_sha256 + nonce + leak_gate_report_sha256 |
| `validation-override/v1`（审计复议） | `cli override` | report_sha256 + 当前内容 hash |

配套：operation 状态机 4 态（`previewed`/`expired`/`applied_index_pending`/`applied`）+ TTL 1800s + commit-intent 恢复 + per-vault 独占锁（`VaultLock`/`VaultLockGroup`/owner sidecar/`lock recover`）。

**实测这些机制的运行状况：**

```
var/state/commit-intents/     0 个文件     ← 崩溃恢复从未触发
var/state/locks/*.lock        2 个文件, 均 0 字节  ← owner sidecar 从未写入内容
var/state/operations/         1,968 个     ← 状态机记录
audit/operations/             2,341 个
release/public-confirmations/   269 个
代码: write_operation.py 640 + operation_store.py 402 + vault_lock.py 190
      + release_confirmation.py 139 + release_input.py 76 + validation/confirm.py 231
      + validation/override.py 206 + capability.py 89  ≈ 1,975 行
```

**这些机制没有捕获过任何实际缺陷。** 而反过来，真正存在的缺陷全部静默通过了门禁：

- 74% 的页面只有 1 条 claim（覆盖率门禁只要求"至少 1 条"）
- （**更正**）引文一致性**并非未校验**：`validate` 经 `rules.py:194-196` → `resolution.verify_quote` 用 `canonical_quote` 校验 wiki 引文。本 ADR 初稿记载的"23 条引文已坏"是**错误比对口径造成的假阳性**（原始字节 vs `canonical_quote`；实测 23/23 在归一化下均命中，真实坏引文 = 0）。真实缺口是**缺少全库回归**——校验只在单文件、显式运行 `validate` 时发生。
- `config/schemas.yaml` 对 source 声明的 8 个字段 0/474 存在（声明层不校验自身与事实的一致性）
- `working` 层的 `source_ref` 硬约束在 20/20 文件中均不满足（该约束从未生效）
- source 正文与 archive 快照 100% 重复（双重事实源），无任何机制报告

**同时，环境已具备替代条件**：所有 durable 内容都经由 git 管理，`content/` 是自由的普通文件（`.pre-commit-config.yaml` 的 `exclude` 已把 `content/.*` 排除在自动改写之外，以保证 hash 链稳定），且工作区不自动提交（`git commit` 由人显式执行）。

## 候选方案

- **A：保留现状。** 审批最强，但代价是约 1,975 行公共模块、1,968+2,341+269 条记录，且实测未捕获任何缺陷；同时它把"写一次内容"变成 10+ 步操作。
- **B：全部删除，只留 git。** 最简。但会丢掉两类真实风险的防护：私密内容外泄（不可逆）与"审的版本 ≠ 发的版本"（发布产物非纯函数）。
- **C：按"是否捕获过真实缺陷"保留门禁，其余退场**（本 ADR 决策）。

## 决策

采用方案 C。

**1）审批 = git commit / merge。** 工具不再提供独立的审批关口，不再产生人工签名事件。工具的职责是**把变更落到工作区**；审核由 `git diff` 承担，批准由 `git commit` 承担。这与项目既有的工作流一致（工作区不自动提交）。

**2）门禁只保留三条，判定标准是"是否捕获过真实缺陷 + 捕获后是否会被修 + 修复成本是否低于损失"。**

| 门禁 | 捕获过真实缺陷 | 捕获后会被修 | 保留 |
| --- | --- | --- | --- |
| **per-claim 引文可验证性**（逐字命中快照 / selector 一致 / 快照存在 / claim 可解析到 source） | **更正**：未捕获过缺陷（真实坏引文 = 0）。但它是"证据链完整"这个不变量的定义本身，且 `validate` **已用同一实现（`canonical_quote`）覆盖单文件校验**——本门禁的增量只是"全库可回归" | ✅ | **硬门禁**（成本＝复用既有实现 + 批量跑） |
| **leak-gate**（私密内容不进 public 输入树 / staging / dist） | ✅ 曾有内网 registry URL 与私密内容扫描记录 | ✅ | **硬门禁** |
| **publish 纯函数**（发布产物必须由当前 HEAD 的已提交文件确定性派生，projection 不静默过滤、前端不重写字段） | 未发生（新规则，防"审的≠发的"） | ✅ | **硬门禁**（成本极低） |
| 确定性 schema / 规则校验 | ✅ | ✅ | 保留（并入 validate） |
| 覆盖率 ≥2/4（ADR-0018） | ❌（新规则） | ✅ | 软门禁（见 ADR-0018 重新评估条件） |
| 四类确认事件 + operation 状态机 + 锁 | ❌ 未捕获任何缺陷 | — | **删除** |

**3）删除清单。**

- 四类人工确认事件（`--confirm` 布尔、`operation-confirmation/v1` 的 apply/publish scope、`public-release-confirmation/v1`、`validation-override/v1`）及其 CLI（`confirm-apply`、`confirm`、`release`、`override`）。
- operation 状态机、TTL、commit-intent 与 `recover`；中断恢复交由 git（`git status` 可见半成品）。
- per-vault 锁体系（`VaultLockGroup` 排序与防死锁、owner sidecar、`lock recover`）。保留的写原语仅为"临时文件 + `os.replace` 原子替换"，其本身即为原子操作。
- 存盘的**校验值**字段（见第 5 条）；**定位指针**保留。
- 命令面按 ADR-0017 收敛为 7 条人输入；`anchor`/`validate`/`audit`/`write`/`confirm`/`confirm-apply`/`override`/`release`/`lock`/`transfer`/`inventory`/`migrate`/`reposition` 退场（`video-*` 并入 `source`，`read`/`backlinks` 并入 `query`，`projection`/`index` 合并为 `build`）。

**4）审计定位为 advisory，且按 claim 硬拦。**

- LLM 审计只产出信号，不参与放行；报告 append-only。
- per-claim 判定：`support ∈ {direct, synthesis, inferred}` 且审计 `fail` → **硬阻**；`support: personal` → 仅告警。
- `support: personal` **只表示"这是我的观点"**，不承担"我不同意审计"的语义。
- **`--force --reason "<理由>"` 保留**，作为唯一的操作层出口（例如 provider 不可用但仍需发布），并写入一条可 review 的留痕记录（不绑 hash、不进确认体系）。审计误判的正解是**改内容**：改到能被引文支持，或把该论断显式降级为 personal 观点。
- `VAL-003`（"同一内容 hash 下多份报告分歧时取 fail，唯一推翻路径是 owner 签署的 `validation-override/v1`"）随之修订为：分歧时仍取 `fail`，推翻路径是改内容或 `--force --reason` 留痕。

**5）区分"定位指针"与"校验值"：指针落盘，校验值不落盘。**

实测各 hash 的真实角色并不相同：

| 字段 | 角色 | 消费者 | 处置 |
| --- | --- | --- | --- |
| `snapshot_sha256` | **定位指针**（决定读哪个 archive 文件） | `citation.py:13`、`evidence_anchor.py:71,81` | **落盘** |
| `raw_ref.path` | **定位指针**（原始字节） | 采集流水线 | **落盘** |
| `raw_ref.sha256` | 校验值（且与 `path` 冗余） | 采集流水线 | **删除** |
| `content_sha256` / `evidence_sha256` | 校验值（仅被确认机制与 `question.py:1114` 消费） | 确认机制（将删除） | **不落盘**，现算现比 |
| `selector_sha256` / `quote_sha256` | 校验值 | `citation.py:36,50`、`audit.py:633-636` | **不落盘**，现算现比 |

判据：**没有它就无法找到数据 → 必须落盘；有它只是为了比对是否被篡改 → 不落盘。** 前者是指针（数据的名字），后者是校验值（数据的指纹）。

- 所有**校验值**字段从 canonical 文件删除；`validate` / `citation` 在运行时读取 archive 并现算比对。这与 wiki 既有的"派生字段运行时算、不落盘"原则统一，并推广到全部实体。
- `archive/text/<sha256>.md` 与 `archive/raw/<sha256>.<ext>` 的文件名继续保持 content-addressed：它既是定位指针，也是"快照不可变"的实现（天然去重、一眼可验、git 可审计）。改为路径式命名会使重新采集静默替换锚点内容。
- 内容去重的范围限定为**内容重复**（source 正文副本，见 ADR-0017 存储模型），**不含指针字段**——指针不是冗余。

**6）配置与文档同步（本 ADR 的直接后果）。** `config/policy.yaml` 的 `write` / `locks` / `validation.human_audit` 段与 `layers.unmanaged_excluded_from` 已删除（均无读取方）；`config/schemas.yaml` 的 `operation` 段（两阶段写入的 9 态状态机声明）随之删除；`human_audit_confirmation` 段描述的门禁仍在运行（`derived.has_private_confirmation`），其字段规格的权威副本在 F003/F004 acceptance 与 ADR-0010，config 侧的无读者副本按"消除双重事实"删除。`OPS-001`（所有写操作必须经过 Preview、用户确认和 Apply）、`OPS-004`（commit-intent/recovery journal）、`SEC-003`（internal private publish 必须有 confirmation + warning ack）需修订或撤销。

## 后果

- 退场约 **1,975 行**公共模块，以及 1,968 条 operation / 2,341 条 audit / 269 条 release 记录所承载的状态机负担；命令面从 29 条收敛到 **7 条人输入**（见 ADR-0017）。
- 发布链变为：`validate`（硬）→ `audit`（advisory）→ `publish`（纯函数派生）→ 前端构建（leak-gate 三段）→ 人工 `git diff` → `git commit`。人工参与点从"每篇签两次字"变为"审一次 diff"。
- **一致性保证发生转移而非消失**：删锁之后，API 进程与 CLI 并发写、或改 source 的同时跑 publish，最坏情况是工作区出现半套数据。它可见（`git status`）、可回滚（git），但**该保证依赖"发布产物可重建"这一前提**——即 `publish` 纯函数门禁必须成立。若将来引入不可逆的对外发布动作（例如自动部署到公网），必须重新评估是否需要运行时互斥。
- 变更面（实测）：16 个测试文件引用确认/状态机（`test_write_operation.py` 10 处、`test_public_projection.py` 8 处、`test_frontend_projection.py` 6 处等）、traceability 中 52 条 AC 约 20 条、4 份 ADR。
- 失去的能力：无法再从持久化记录中回答"谁在何时批准了哪个 hash"。替代答案是 git 的 commit author 与时间戳；因此 **`git commit` 必须是人工执行且 message 应携带对象标识**，这一点从"工作流习惯"上升为契约要求。

## 实现状态（2026-09-15）

- **已落地**：四类确认事件、operation 状态机、TTL、commit-intent、per-vault 锁在**写入通道**上已删除（`source_ingestor` / `video_frames` / `skill_runtime` / `backend` 改为一次落盘，失败即结构化返回）；审批由 `git commit` 承担。
- **部分落地**：命令面 **29 → 22**。已退场 `write` / `confirm-apply` / `lock` / `inventory` / `migrate` / `transfer` / `reposition`；`anchor` / `validate` / `audit` / `confirm` / `override` / `release` 与 `video-*` 的退场等待 ADR-0017 的 `wiki` / `build` 动词落地 —— 而 ADR-0017 仍为 Proposed，其 7 条命令面里的 `wiki` 与 `build` **尚未实现**。因此"收敛到 7 条"是目标而非现状。
- **部分落地**：§5「所有校验值字段从 canonical 文件删除」只做了一半。`content_sha256` 确已不落盘；但 **`selector_sha256` 与 `quote_sha256` 仍由 `tools/evidence_anchor.py` 写入 canonical source 的 `evidence_items`**（实测 275 个 source 含这两个字段）—— 它们是"现算可得"的校验值，正属 §5 的删除范围。`snapshot_sha256` 作为定位指针保留（494 个 source），符合"指针落盘、校验值不落盘"。
- **进行中（2026-09-15）**：config 死声明四批清理完成。`config/vocab.yaml` 全份 294 行删（合法取值单一来源收敛为 `tools/common.py` 枚举 + `wiki-v1.json` 的 `enum`）；`policy.yaml` 删 `write`/`locks`/`validation.human_audit`/`layers.unmanaged_excluded_from` 与 6 个无读者顶层段（`retrieval`/`source`/`normalization`/`granularity`/`archive`/`frontend`）；`schemas.yaml` 删 `operation` 与 21 个对象契约副本（921→458 行）。清理后 `policy.yaml` 9 段 / `schemas.yaml` 8 段全部有读取方。对象契约的权威确定在代码/jsonschema（wiki→`wiki-v1.json`+jsonschema、source→`source_validator.py`、API→`backend/schemas.py` 的 Pydantic），config 不再放无读者的形状声明。
- **反模式门禁（2026-09-15）**：上述"把设计说明塞进运行时配置、然后无人读"的模式已复发四批，故加 `tests/test_config_no_dead_sections.py`——AST 扫 `policy_value`/`schemas_value` 调用 + `path_contract` RULES 得"消费集"，断言两个 config 的每个顶层段都在其中。只判**顶层段整段死**，不判段内死子键（后者需键路径级比对，当前仅 `validation` 段一例，留待第二例再上）。检测口径是 AST 非 grep（grep 会因词形碰撞误判，本仓库栽过多次）。
- **待定（下一轮）**：`schemas.yaml` 的 `validation` 段内死子键（顶层活、90 行子键无读者）；`human_audit_confirmation` 段（活机制的无读者声明，其字段规格权威在 F003/F004 acceptance）。
- **副作用（实测）**：本 ADR §6 要求修订规范文档，而 `docs/myknowledge-system-design.md` §6 **同时是 LLM 审计的规则集来源**（`tools/validation/ruleset.py`）。因此修订 §6 使 `ruleset_sha256` 变化，把既有的 **1502 条审计结论**统一标记为 `stale_ruleset`。这是设计内的行为（AC-F003-015：可见、不阻断、由重跑 `audit` 刷新），`valid` / `public_publishable` / `confirm` 均不受影响；但它意味着**改规范文档 = 全库审计结论需要重跑**。

## 配置类型化：终态方向（记录，未落地）

死声明门禁（`test_config_no_dead_sections.py`）是**增量解**——事后检测，且只覆盖
顶层段。**终态解**是"配置即代码"：把运行时读的**设置值**加载进类型化模型，届时
"没读的字段" = "未用属性"，由 pyright/死代码工具**结构性**暴露，无需专门检测。

- **迁移规模（AST 实测）**：config 的**值访问**只有 **13 处调用 / 11 条唯一键路径**
  （`policy_value` 7 + `schemas_value` 4 + `config_value` 2），不是大工程。
- **选型**：`pydantic-settings` 的招牌能力是 env/secrets 多源分层加载，本仓库是
  单 YAML、无 env 覆盖，用不上——更合身的是普通 `pydantic.BaseModel` 或 stdlib
  `dataclass`，只取"类型 + 属性访问 + 死字段暴露"。仓库已用 Pydantic（backend），
  倾向 `BaseModel`。
- **硬约束（决定成败）**：config 里混着两类东西——(a) 运行时读的**设置值**（11 条，
  适合建模）与 (b) 给 `path_contract` 对账的**路径声明**（`audit/.../<id>.json` 之类
  模板）。**(b) 必须留在 YAML**：`path_contract` 的价值是"config 声明路径 ↔
  `paths.py` 派生路径"**两份独立事实互证**，迁到 pydantic 单一真相会削弱这个有意
  保留的门禁。所以终态是"(a) 迁 BaseModel、(b) 留 YAML"，不是全迁。
- **不现在做的理由**：config 低频变更（近期改动全是删死重、非加新键），增量检测
  （已建的 test）性价比高于终态迁移；且它触及 `path_contract` 的双重事实设计，属
  独立架构决策，应单独立项并先出设计。此条为方向记录，非承诺。

## 重新评估条件

- 若出现"已发布内容与已提交内容不一致"的实际事故（即 publish 纯函数门禁被绕过或未覆盖某条派生路径），说明纯函数前提不成立，需要恢复显式的发布确认。
- 若将来引入不可逆的对外发布（自动部署、公开 API 写入），运行时互斥与显式确认需重新评估。
- 若自动化脚本开始执行 `git commit`，则"审批 = git"的前提失效，必须恢复一层独立的审批关口。
- 若 `--force --reason` 在一次都没有留痕的情况下被频繁使用，说明审计的误报率高于可接受水平，应优先降低误报而不是增加出口。
- 若"校验值不落盘"导致发布链耗时不可接受（每次 validate 都要读 archive 全文现算），说明需要引入分层缓存，而不是恢复落盘 —— 缓存是可丢弃的派生，与"校验值落盘"性质不同。
