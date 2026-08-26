# MyKnowledge 技术方案系统 Review（2026-08-26）

## Review 基线

- 基线 commit：`a63b06ceb26e2b17ad065492be7e25e6e3d05216`（`docs: establish redesign delivery baseline`）。
- Review 工作树：`main`，存在本轮未提交改动；本记录不代表已提交、推送或发布。
- 范围：系统规范、ADR、Feature/Acceptance/Traceability、配置契约、Astro projection 构建脚本、CI 和 README。
- 已确认决策：方案 B（一个 public repo + `0..N` 个独立 private Git Vault）；完整引用为 `(vault_id, object_type, object_id)`；相同 snapshot 可以物理去重但必须保留 owner 记录；本机文件统一 `source_type: local-file`；`public_release` 默认 `false` 且只能由人工确认事件改为 `true`；F008 题型/复习单独延后。

## 本轮发现与修复

| 问题 | 修复 |
| --- | --- |
| leak gate 用同一组 HTML 正则扫描 Astro、Mermaid、Pagefind JS，正常 `<script>`/`javascript:` 字符串被误报 | 输入与 staging 继续严格拒绝 active content；dist HTML 只拒绝危险嵌入、事件处理器和危险 URL，JS/CSS 不套 HTML 标签正则 |
| 递归扫描时 `sourceKind` 随目录层级变化，catalog 检查永远不能命中；catalog 也没有兼容 `id`/`object_id` | `scanTree` 保持根扫描类型；dist catalog 按 public manifest object ID 校验 |
| 普通运行时代码中的 `authorization` 字段名可能被当成凭据 | 改为高置信凭据模式（实际字符串值、Bearer/Basic、私钥材料） |
| `validation_expired` 与枚举 `expired` 不一致 | 统一为 `validation_state: expired` |
| internal source 的旧文字写成“不可 published”，与 private Vault 私有发布决策冲突 | 改为允许 owner private Vault 内 `published + private`，必须有发布确认和 internal warning；不得进入 public projection |
| `require_network` 被写成全局联网门 | 明确只约束 fetch/provider；`local-file`、`personal-note` 和已有本地证据的 draft 可按 allowlist 离线执行 |
| LLM 不可用时“不能写 wiki”与“保持 draft”矛盾 | 允许保存有 provenance 的 draft candidate，但禁止晋级 validated/published/projection |
| FSRS 参考资料看起来像当前实现 | 所有当前验收移除 Question/FSRS；参考表改为 F008 候选，版本待后续决定 |
| Query 文档把 `projection` 当查询权限字段 | 查询统一使用 `scope: public/local/private`；`projection` 只表示索引生成视图 |
| F007 缺少 manifest volatile hash 和 release-input 覆盖验收，追踪矩阵未覆盖 | 新增 AC-F007-014/015 并同步矩阵；`validate:docs` 检查所有场景 |
| README/前端 README 把默认 dev 预览描述成正式 public 站点 | 明确默认是 legacy 迁移预览；正式链路必须显式 `MYKNOWLEDGE_CONTENT_MODE=projection` 和 `npm run validate:projection` |
| 生成的 leak 报告写入 `frontend/state/` 却未被忽略，容易误提交 | 增加 `frontend/state/` 忽略规则；报告仍只作为本机诊断，不是 durable release record |
| 确认事件示例使用 `evt_...`/`op_...`，校验器却复用对象 ID 格式 | 在 vocab 中分离 event/operation ID 规则，并在 prepare 阶段校验安全字符、nonce、actor 和 reason |
| projection 文件在路径检查后可能被替换，失败恢复对“原先不存在的生成目录”不完整 | body/附件/确认事件采用读前读后 inode/realpath 校验；release backup 记录 absent 状态并在失败时清理新目录 |
| §9.5 写入准入表头/行列数不一致，查询文档把 QueryResult 与 AskResult/写操作字段混在一起 | 修正 Markdown 表格；明确 `query-result/v1`、`ask-result/v1` 和 operation response 的边界，并在 registry 中登记必填字段 |
| validate-build 只按普通 `readFile/JSON.parse` 读取生成 JSON，且只检查 Pagefind 入口存在 | 所有 manifest/generated JSON 使用 regular-file + inode/realpath/mtime/ctime 稳定读取并重新计算 manifest hash；校验 Pagefind language `page_count` 与 catalog 闭包、sitemap URL 集合闭包 |
| leak-gate 报告普通覆盖写，扫描文件读后可被替换 | 报告改为临时文件 fsync + atomic rename；每个扫描文件增加读前后 inode/realpath/时间稳定性检查，变化记为阻断 finding |
| projection 正文可留下根相对/private route 或未声明的非 `.md` 本地链接 | prepare 增加 public route/attachment allowlist；只接受 manifest route、声明附件、anchor 和允许外部 scheme，未知本地路径 fail-closed，并纳入 link/graph 闭包 |
| public confirmation 的 human/actor/reason 约束可被伪造或携带私有元数据 | 强制安全 actor pseudonym、public-safe reason、可选 `target_vault` 只能为 public；文档明确这是交互流程门禁而非密码学身份认证，非交互 confirm 必须由 writer 阻断并写 durable audit |
| provider capability 文字允许缺失 token 上限时“保守估算” | canonical `context_window_tokens`/`max_output_tokens` 仍为必填；只有固定 tokenizer/版本化预算证明可派生，否则 `validation_state: unavailable` |
| `config/schemas.yaml` 被误读为可执行领域 JSON Schema | 新增 Schema Validator 技术设计和 AC-F002-007；明确 registry 通过不等于 Source/Wiki/event 已验证，Ajv/JSON Schema 2020-12 与跨字段 rule layer 仍是实现阻断 |
| provider capability 只列布尔能力，未固定安全处理、上下文和 verdict 聚合字段 | 补齐 `provider-capability/v1` canonical report、`wiki-validation-request/v1`/response、三次保守聚合和 verdict 词表 |
| 主规范保留旧四选一 Question schema，形成第二事实源 | §7 收敛为 F008 延期边界，完整待议内容只保留在 `docs/deferred/` |
| confirmation 若要求预先绑定最终 dist 报告会与 build 形成循环 | 明确人工只确认 release input/输入扫描；构建后独立执行最终 dist gate，失败保留旧 dist |
| input-tree 与 dist leak gate 共用错误 schema version，无法按 registry 区分报告边界 | input-tree 使用 `public-input-leak-gate/v1`，dist 使用 `public-leak-gate/v1`；release runner 按 scope 校验对应版本 |
| `public_release` 既被描述为 operation 字段又可能被误写到 Front Matter，缺少唯一权威事实源 | 明确它是 projection materialized field；只有 `release/public-confirmations/<event_id>.json` 与 owner `audit/operations/<operation_id>.json` 的匹配 hash chain 才能派生 true，手写字段、manifest 字符串和临时 state 一律忽略 |
| Ask citation 只有字符串类型名，不能保证证据可回放 | 增加 `citation/v1`/`citation-locator/v1` registry，要求完整 ObjectRef、owner snapshot 解压/hash 校验、TextQuote exact、TextPosition Unicode code-point 半开区间和 selector hash |
| capability token 只有“需要 token”的口头约束，没有轮换、权限和传递边界 | 增加 `capability-token/v1` registry/policy：进程启动随机轮换、state 目录/文件权限、无 HTTP 获取、受保护传递、audience/scope、恒定时间比较和错误行为 |
| 备份状态只有枚举，没有 target 变化/失败/过期转换和 durable manifest 归属 | 明确 `unconfigured -> configured -> verified`、失败进入 `failed`、target 变化/过期回到 `configured`；manifest 固定在 `audit/backup/<backup_id>.json`，密钥只保留 opaque reference，shared cache 不代替 owner 备份 |

## Hash 与发布边界

当前契约区分三类摘要：

1. `manifest_sha256`：canonical manifest hash，忽略 `generated_at`、`generatedAt`、自身 `manifest_sha256` 等 volatile 字段。
2. `release_input_sha256`：覆盖 canonical body、body path、公开 Front Matter metadata、附件路径/排序/hash、links、route、lineage commitment 和 policy/schema 版本。
3. `leak_gate_report_sha256`：当前 projection item 的输入边界扫描摘要。最终 Astro/dist 扫描报告是一次构建的运行产物，由 `operation_id` 标识并写入 build manifest；两者不能互相冒充。

人工 confirmation 必须绑定当前 release/content/evidence/输入扫描摘要和 public object ref；它不预先绑定尚未生成的最终 dist 报告。确认后构建器再执行最终 dist leak gate 并把结果写入本次 build manifest；任一输入变化、最终 dist leak gate 失败或旧 event 不匹配，都必须阻断发布并保持旧 dist，不能形成“先构建才能确认、先确认才能构建”的循环。

## 验证证据

以下命令在本轮工作树执行并通过：

```bash
cd frontend
npm run validate:config
npm run validate:docs
npm run validate:legacy
node --check scripts/prepare-content.mjs
node --check scripts/build-graph.mjs
node --check scripts/validate-build.mjs
node --check scripts/build-release.mjs
node --check scripts/leak-gate.mjs
node --check scripts/validate-docs.mjs
node --check scripts/validate-config.mjs
git diff --check
```

本轮新增契约与验收后，`npm run validate:config`、`npm run validate:docs` 已重新执行；当前文档验收场景总数为 119（原 113 个基础场景加上 capability/citation、leak-gate/public-release authority、backup state/manifest 六个场景）。这证明 registry、policy、acceptance ID 和治理链接一致，不代表任何新增 runtime 已实现。

另用临时、明确标记的 projection fixture 验证了：1 个页面、4 个静态页面、Pagefind、graph、validate-build、输入/staging/dist leak gate、带 `evt_`/`op_` 前缀的确认事件和 `dist.next -> dist` 原子提升均通过；fixture 已删除。另验证了 manifest 缺失时 fail-closed、生成目录失败恢复（包括原先不存在的目录）以及旧生成内容 hash 不变。因此这些结果只能证明构建契约可运行，不能证明 F007 已 Accepted；新增 token/citation/backup 规则目前仍是设计和验收约束，尚无对应 backend/runtime 实现证据。

## Feature 状态边界

| Feature | Review 后状态 |
| --- | --- |
| F001–F004 | Designed；规范和验收已补齐，领域 writer/backend 尚未实现 |
| F005–F006 | Designed；QMD → FTS5 → deterministic fallback 契约已写明，运行时尚未交付 |
| F007 | Designed/Not Implemented；构建脚本和 fail-closed POC 可运行，真实 manifest、正式搜索 fixture、人工发布演练和 CI 发布证据未完成 |
| F008 | 已启动；单选、多选、面向面试简答题，FSRS 与完整运行面按独立 Acceptance 闭合 |
| F009 | Designed/Not Implemented；`skills/myknowledge/SKILL.md` 和领域 writer/backend 尚不存在，不能创建误导性的空 Skill |
| F010 | Designed；迁移仍以 legacy 基线为输入，未声称内容迁移完成 |
| F011 | Designed；支持 `0..N` Vault 的契约已补齐，真实外挂仓库挂载/冲突演练未完成 |
| F012 | Designed；remote 与加密备份位置逐 Vault 仍为 `null`/`unconfigured`，不能声称恢复链路就绪 |

## 尚未关闭的交付阻断

- 上游 public projection generator、Source/Wiki writer、Vault Registry、FastAPI 和 Agent Skill 尚未实现。
- `queries/public/manifest.json` 当前不存在；正式 public 内容、Pagefind 中文/英文/混合查询 fixture 和人工 release 记录尚未建立。
- private remote、加密备份目标和 credential helper 仍待配置；任何未配置 Vault 的备份/恢复操作必须告警或阻断。
- 可执行 JSON Schema 文件、Source/Wiki/domain writer、跨字段 validator 和 schema hash replay 尚未实现；当前 `config/schemas.yaml` 只是 registry，不能把 `validate:config` 通过当作领域对象验收。
- 需要在真实实现中补齐 malicious projection、public route/link、附件类型、SSRF/文件竞态、Vault 不可用/冲突、warning policy、Pagefind/sitemap 闭包和旧 dist 保留的自动化测试；当前脚本检查不替代运行时验收。
- 发布工具仍必须按“人工 input confirmation -> 构建 -> final dist leak gate -> 原子提升”编排；不能只凭 input hash、最终扫描或 `public_release: true` 字符串放行。

## 结论

本次 review 已修复当前文档、配置契约和 POC 校验器之间的主要矛盾，并补齐 F002/F007 的 schema、链接、页面集合与确认流程追踪门。设计可以进入实现阶段，但当前仍是“设计完成、核心运行时未交付”的状态；任何发布、备份恢复或 Agent 写入能力都必须等待对应 Feature 的真实实现和验收证据。
