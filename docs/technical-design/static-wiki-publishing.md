# Astro/Starlight 静态 Wiki 发布实现设计

- 状态：Implemented（2026-08-27；Astro 工程骨架、projection build 与 input-tree/staging/dist 三阶段 leak gate）
- 相关 Feature：F007、F010、F011
- 相关规范：WEB、SEC、IDX、WIKI、MIG
- 相关 ADR：ADR-0002、ADR-0007、ADR-0009
- 相关验收：[F007](../acceptance/F007-static-wiki-publishing.md)、[F011](../acceptance/F011-private-vault.md)

## 1. 目标与非目标

### 目标

- 保留现有 Astro/Starlight 阅读体验，改为只消费 `public projection`；
- 让 public build 只产生 `public_publishable` Wiki、目录、路由、Pagefind 和 Wiki 图谱；
- 在构建前、staging 和 dist 三个边界执行 leak gate；
- 无 FastAPI、LLM 或 private vault 时仍能浏览、搜索、看图谱和使用浏览器本地状态；
- 保持现有 POC 的路由兼容、重复路由消歧、内部链接报告、Mermaid/KaTeX、Cytoscape 和 localStorage 行为；
- 构建失败时保留上一版可用 dist，不发布半成品。

### 非目标

- Astro 负责 source/wiki 写入、claim 验证、状态计算或发布确认；
- 静态站点展示 source/archive 正文、F008 题目 answer/explanation、LLM report 或 internal metadata；
- 在本设计中实现登录、SSR 权限、在线协作或后端 API。

## 2. 当前 POC 基线

当前未跟踪的 `frontend/` 已有一条可运行的 Astro POC，版本锁定在：

| 组件 | 版本/实现 |
| --- | --- |
| Astro | `7.1.3` |
| Starlight | `0.41.4` |
| Pagefind | Astro/Starlight build 集成 |
| Cytoscape | `3.34.0`，全局和文章局部图谱 |
| Mermaid | `11.16.0` |
| KaTeX | `0.16.25` + `remark-math`/`rehype-katex` |
| 内容准备 | `frontend/scripts/prepare-content.mjs` |
| 图谱生成 | `frontend/scripts/build-graph.mjs` |
| 构建验证 | `frontend/scripts/validate-build.mjs` |
| 内容集合 | `frontend/src/content.config.ts` 使用 Starlight `docsLoader/docsSchema` |
| 页面组件 | `src/pages/index.astro`、`graph.astro`、`src/components/PageTitle.astro` |
| 本地状态 | `localStorage` key `myknowledge:state:v1`，当前只保存 favorites/recent/阅读状态；题目复习状态留给后续 F008 |

当前 POC 通过 `MYKNOWLEDGE_CONTENT_MODE=legacy-validation` 读取旧根目录 `docs/`，但会排除 `acceptance/`、`adr/`、`technical-design/`、`deferred/` 和根目录治理文档；最近基线为 276 篇内容文章、224 条显式关系、19 条未解析链接。它自动生成 `src/content/docs/`、`public/generated/catalog.json`、`graph.json` 和 `compatibility-report.json`，只能用于迁移基线，不能作为 release input。正式发布必须使用 `MYKNOWLEDGE_CONTENT_MODE=projection`，读取 `queries/public/manifest.json`；manifest 缺失、schema 不匹配或任一 item 不满足 public allowlist 时 fail-closed。

当前工程已恢复 Astro/Starlight 依赖、projection adapter、catalog/graph 生成、构建失败保留旧 dist 和 leak gate 基础脚本。真实 public manifest、正式 Pagefind 中文/混合查询 fixture、人工 release confirmation、完整三段 leak gate 和 CI 发布证据仍未落地，不能把本轮工程骨架标记为 F007 Accepted。

本轮增量调查（2026-08-30）：继续复用 Astro/Starlight static output、Pagefind final-HTML index 和 Quartz graph closure；新增独立 projection validator，参考 Starlight content collection 的 schema-first fail-fast 习惯。替代方案是直接信任 manifest 字符串字段，无法防止 duplicate ID、编码路径穿越或 practice/source/archive 混入，明确不采用。

本轮多页集成调查（2026-08-27）：Astro 7.1.3/Starlight 0.41.4（MIT）与 Pagefind 1.4（MIT，<https://github.com/CloudCannon/pagefind>）继续作为静态输出/离线索引方案；Quartz v4（MIT，<https://github.com/jackyzha0/quartz>）仅借鉴 catalog-to-graph 闭包。替代方案是直接扫描 `docs/` 或由前端动态读取 local index，会把治理文档、practice 或 private 内容带入发布，明确排除。临时 fixture 在独立 root 运行 prepare-content/build-graph，不改生产 manifest、canonical 或 dist。

发布编排增量复用 POSIX `O_EXCL` lockfile 语义：`build-release.mjs` 在仓库 `state/public-release.lock` 建立 0600 锁，构建失败保留旧 `dist`，正常退出才释放锁；已存在锁一律返回 `release_lock_held`，不按超时自动删除，陈旧锁需人工恢复。

public release 事件使用独立 `tools/release_confirmation.py` 校验 `public-release-confirmation/v1`：target 必须是 public Wiki、actor 必须为 human、reason 不得含 URL/路径/private 字样，leak-gate scope 固定为 `input-tree`，事件 hash 由去除自身 hash 的 canonical JSON 计算。写入采用 append-only `release/public-confirmations/<event_id>.json`，不由 Agent/CI 自动生成。`prepare-content.mjs` 对每个 manifest item 重新读取该 event，校验 target/object ID/event hash 后才复制正文；手写 `public_release` 或缺失 event 不能进入 staging。

## 3. 发布输入契约

### 3.1 Public projection manifest

上游 `generate_public_projection.py` 在 public vault 内生成可审计 manifest。正式 schema 为 `public-projection/v1`，示例：

```json
{
  "schema_version": "public-projection/v1",
  "projection": "public",
  "generated_from": "commit-or-tree-hash",
  "policy_version": "policy-v1",
  "items": [
    {
      "id": "wiki-transformer",
      "object_type": "wiki",
      "vault_id": "public",
      "title": "Transformer",
      "route": "computer-science/transformer",
      "domain": "computer-science",
      "kind": "knowledge",
      "body_path": "wiki/computer-science/transformer.md",
      "attachments": [],
      "public_confirmation_path": "release/public-confirmations/event-123.json",
      "status": "published",
      "publication_scope": "public",
      "public_publishable": true,
      "public_release": true,
      "release_input_sha256": "sha256:...",
      "public_confirmation_sha256": "sha256:...",
      "public_lineage_commitment": "sha256:...",
      "strength": "verified",
      "effective_confidentiality": "public",
      "validation_state": "pass",
      "evidence_state": "supported",
      "links": ["wiki-attention"],
      "content_sha256": "sha256:...",
      "evidence_sha256": "sha256:...",
      "leak_gate_report_sha256": "sha256:...",
      "leak_gate_report_scope": "input-item"
    }
  ]
}
```

`items` 是 allowlist，不是从 local index 过滤出来的动态结果。生成器在写 manifest 前拒绝：`vault_id != public` 或 `allow_public_projection != true`、internal effective confidentiality、非 published 状态、`validation_state` 为 `fail`、缺少绑定当前 `(content_sha256, evidence_sha256)` 的人工审计确认（`operation-confirmation/v1`）、`evidence_state` 为 `missing`/`partial`/`conflicting`/`unresolved`/`stale`、source/archive/practice 路径、任一 private vault ID/hash、`public_publishable != true`、派生出的 `public_release != true`、缺少当前 `release_input_sha256` 绑定的 `public-release-confirmation/v1` 人工 confirmation event。`public_release` 不是作者可写的 Front Matter 事实字段；生成器必须从 `release/public-confirmations/<event_id>.json` 和 public owner 的 `audit/operations/<operation_id>.json` 重新计算它。只修改 Front Matter 为 `true`、只修改 manifest 字符串或只存在临时 `state/` 都必须派生为 false 并阻断。每个 item 还必须给出 `content_sha256`、`evidence_sha256`、`attachments`（每个附件的 public-relative path + sha256）、`public_confirmation_path` 和 public Wiki object ID；`body_path` 与附件的 canonical hash 不一致时，adapter 必须拒绝。`release_input_sha256` 必须覆盖附件集合，附件不能通过正文之外的路径偷偷进入 staging。公开 manifest 只保留不可逆 `public_lineage_commitment`、`public_confirmation_sha256` 和不含 private ID 的字段，不保留 `source_vault_ids`。生成器只读取 public-owned projection、public-safe confirmation event 和已提交的人工审计确认摘要，不需要 checkout private vault。

`leak_gate_report_sha256` 在当前 `public-projection/v1` 和人工 confirmation 中表示**单个 item 输入边界**的确定性摘要（scope=`input-item`）；它绑定 item、正文和声明附件的 hash/安全 findings。另有一次 `public-input-leak-gate/v1`、scope=`input-tree` 的全量输入扫描在 Astro 前执行，覆盖 manifest、所有 public 输入目录和未被 item 引用的文件；构建后以 `public-leak-gate/v1` 再次扫描 input、staging 和 dist（scope=`dist`）。人工先审核固定的 release input、evidence 和输入扫描结果，再生成 confirmation。最终 dist 报告摘要只写入 `build-manifest.json`，不反写 manifest/confirmation，避免形成“必须先确认才能构建、又必须先构建才能确认”的循环。任一输入摘要变化使人工 confirmation 失效；最终 dist 报告失败则本次构建阻断并保留旧 dist，但不改写 canonical 对象或伪造新的人工事件。三种报告的 schema version 按 scope 固定，`input-tree` 不能写成 `public-leak-gate/v1`，`dist` 不能写成 `public-input-leak-gate/v1`。

### 3.1.1 Canonical hash 规则

- 所有 hash 输入先转 UTF-8；正文把 CRLF/CR 归一为 LF，移除行尾空格，并保证非空正文只有一个末尾 LF；Front Matter 不进入 `content_sha256`，但允许的公开 metadata 会进入 `release_input_sha256`。
- JSON canonicalization 递归按 key 的 UTF-8 字节序排序，不保留 YAML 排版、anchor、隐式类型或额外空白；数组默认保持语义顺序。manifest 的 `items` 按 `id` 排序，item 的 `links` 按 object ID 排序，`attachments` 按 path 再按 hash 排序后再 hash。
- `manifest_sha256` 只在顶层忽略 policy 声明的 volatile 字段（当前为 `generated_at`、`generatedAt` 和自身 `manifest_sha256`）；两种时间字段不能同时出现；改变正文、权限、状态、链接、路径或任何非 volatile metadata 都必须改变 hash。
- `release_input_sha256` 的字段集合与 `config/schemas.yaml:release_input_fields` 完全一致：canonical body、body path、已排序附件 path/hash、允许的 public metadata、去重排序后的 Wiki links、route、`public_lineage_commitment`、policy version 和 schema version。
- 输入 leak 摘要只记录规范化 findings（类别、相对路径、finding digest 和结果），不把匹配正文写入 hash 或日志；计算 item-level `input-item` 摘要时排除自身 `leak_gate_report_sha256` 和派生的 `public_confirmation_sha256`，避免与 confirmation event 形成循环；最终 dist 报告保留完整扫描文件清单用于诊断，但其 `report_sha256` 不受生成时间和文件清单变化影响。

### 3.1.2 `public_release` 权威来源

`public_release` 是 projection 的 materialized field，不是 Wiki Front Matter 的可写事实字段。作者、Agent、LLM、CI 或手工编辑只能提交候选值，writer 在 projection 前必须忽略该候选并重新读取两个 durable record：`release/public-confirmations/<event_id>.json`（public-safe 人工事件）和 public owner 的 `audit/operations/<operation_id>.json`（操作记录）。存在 private lineage 时，源 owner Vault 的 `audit/operations/<operation_id>.json` 也必须可解析，但其中的 private 字段不能进入 public record。

只有以下条件全部满足时才派生 `public_release: true`：事件 schema/hash 有效、`actor_type: human` 且 `decision: approve`、事件的 `release_input_sha256`/content/evidence/input-tree leak hash 与当前输入完全相同、target ObjectRef 的 owner 是 `public`、target operation record 的 `record_sha256` 自校验通过且引用该事件。Front Matter 直接写入 `public_release: true`、只修改 manifest 字符串、缺少任一 durable record 或只保留临时 state 都必须派生为 `false` 并阻断发布。输入 hash 变化后旧事件 append-only 保留但不再匹配，新的 projection 必须回到 `false`，不能自动复用旧批准。

### 3.2 内容读取

Adapter 只允许读取 manifest 中的 `body_path`，并把路径解析后限制在仓库内的 projection staging allowlist；拒绝 `..`、绝对路径、编码穿越、manifest/body/attachment 的 symlink 或 hard-link，以及未列出的附件。manifest 本身也要以 regular-file + 读前后 inode/realpath 校验读取。projection 输入保留 allowlisted 的相对 body path，避免把所有页面压扁到同一个临时目录；正式 projection 出现重复 route 直接失败，不能在人工确认后自动追加后缀。Adapter 重新计算 canonical body hash，并读取 `public_confirmation_path` 校验 `event_sha256`、人工 actor、target ref、release/content/evidence/leak hash；任何一个不匹配都 fail-closed。若正文没有 Front Matter，adapter 只从 manifest 的公开 `title`/`route` 生成最小 Front Matter；已有 Front Matter 只允许 `title`、`slug`、`description`、`draft`、`pagefind`，其余字段拒绝而不是原样复制。一个 public attachment 可以被多个 item 复用，但每个 owner 必须声明相同 path+sha256；与正文路径冲突或 hash 不一致直接失败。脱敏 public copy 必须已经拥有自己的 public-safe source/evidence binding；private source ID、snapshot selector 和跨 Vault content reference 只能存在私有 lineage/audit，不得作为 public copy 的 `sources` 或页面引用。

## 4. 构建流水线

```text
npm run validate:config
  -> npm run build:release (projection mode)
       -> isolated staging input
       -> prepare-content adapter
       -> input-tree leak gate (before Astro)
       -> Astro/Starlight + Pagefind
       -> build-graph (public catalog only)
       -> validate catalog/routes/graph
       -> leak gate (input + staging + dist; input is repeated)
       -> atomic promote dist + build manifest
```

### 4.1 prepare-content adapter

保留 `prepare-content.mjs` 的职责，但按模式选择输入：legacy-validation 使用显式排除列表，projection 使用 manifest staging root：

- 读取 manifest 并复制/链接 allowlisted Markdown 和公开附件；
- 生成稳定 route，保留现有 `slug`、相对路径和 `routeFromRelativeWithNamedSymbols` 规则；
- 对重复路由按显式 slug、源文件名和稳定后缀消歧；
- 移除重复一级标题，保留 Front Matter；
- 只重写 manifest 内的 Wiki-to-Wiki Markdown links；外部 `http(s)`/`mailto`/`tel` URL 和 anchor 原样保留；本地相对 route 只能解析到 manifest 内的 public route，声明附件必须有 path+hash，根绝对路径、协议相对 URL、未声明的相对 route 和其他 scheme 直接拒绝；
- unresolved link 写入兼容性报告并按 policy 阈值阻断或告警；
- 输出 `catalog.json`，每项只包含公开字段和 `content_sha256`。

不允许从源 Markdown 的任意链接推断 private/source 节点；link target 不在 public catalog 时直接 fail-closed（不再把潜在 private route 原样复制到 dist），不能把 internal ID 写入 JSON。每个解析出的 public route link 必须同时存在于 manifest item 的 `links` object ID 列表，最终 graph/catalog/link 集合做闭包校验。

### 4.2 Astro/Starlight

`src/content.config.ts` 继续使用 Starlight loader/schema。`astro.config.mjs` 保留站点、base、简体中文 locale、自定义 CSS、Mermaid/KaTeX 和 PageTitle 组件；页面组件通过 `catalog.json` 获取标题和 route，不扫描文件系统。

现有页面行为：

- 首页展示领域入口、文章数量、最近查看和收藏；阅读状态是本地 UI 增强，不等同于 F008 题目复习；
- `PageTitle.astro` 提供收藏、图谱跳转和相关文章；题目/复习入口留给后续 F008；
- `graph.astro` 从 `generated/graph.json` 加载 Cytoscape 全局图谱，支持搜索、领域过滤、节点详情和 `?focus=`；
- localStorage 写入失败时禁用相关控件并显示本地状态不可用，不影响阅读；
- Mermaid/KaTeX 渲染失败只标记该块，不使整篇文章空白。

Mermaid 必须使用 `securityLevel: strict`。进入渲染器前拒绝超长图表源、`click`/callback、`javascript:`/`vbscript:`、外部 URL 和 `data:` 资源；渲染后再通过 DOMParser 检查 SVG namespace，拒绝 `script`、`foreignObject`、外部 `href/src`、事件处理器和危险 CSS。SVG 不直接拼接到 `innerHTML`，只导入经过上述检查的节点。该策略只保护公开展示层，不能替代 projection 输入的 active-content/leak gate。

这些都是展示行为，不能读取或计算 evidence/validation/publication 状态。若要显示 `strength` 或 internal warning，只能消费 projection 已计算的公开字段；public projection 不应出现 internal warning，因为 internal 对象根本不进入 public。

### 4.3 图谱生成

`prepare-content.mjs` 在解析并重写 Markdown 链接时生成 public-safe 的 route link 集合，`build-graph.mjs` 只读取 `catalog.json` 中的该集合和 `input-metadata.json`；它不能再次扫描旧 `docs/` 或任意 Vault 路径。projection manifest 的 `links`（对象 ID）必须与正文解析出的 public route 集合一致，避免签名 manifest 与实际页面关系漂移：

```json
{
  "nodes": [{"id": "wiki-transformer", "title": "Transformer", "section": "computer-science"}],
  "edges": [{"source": "wiki-transformer", "target": "wiki-attention"}],
  "generated_from": "public-manifest-hash"
}
```

节点集合必须与 catalog 完全相等；边的 source/target 必须都在节点集合内，不允许把 source、F008 question、evidence 或未发布 Wiki 当作节点。图谱 JSON 的 `generated_from` 必须等于 projection manifest hash（legacy 模式使用明确的 `legacy:<mode>` 标识）。图谱布局仍由浏览器 Cytoscape 完成，静态构建只生成数据，不把随机布局坐标写入 canonical 内容。

### 4.4 Pagefind

Pagefind 只在 Astro 生成的 public HTML 上运行；不直接索引 Markdown projection。所有页面继承 `lang="zh-CN"`，配置和验收使用 Pagefind multilingual 文档的语言分段能力。必须有中文标题、中文连续文本、英文标识符和混合查询 fixture；Pagefind 版本升级时保存索引大小、命中页面和高亮结果基线。

构建验证必须读取 `pagefind/pagefind-entry.json`，要求每个语言索引的 `page_count` 总和等于 public catalog 数量；同时解析 sitemap index 和所有 sitemap 文件，要求 URL 集合恰好是首页、图谱页和 catalog 文章 route（同一 base path、无 query/fragment/重复 URL）。Pagefind 或 sitemap 集合不闭合时阻断发布。

Pagefind 失败属于可恢复构建错误：若 policy 允许发布无搜索站点，必须在构建报告标记 `search_degraded: true`；默认 F007 验收要求搜索正常，因此 CI 阻断并保留旧 dist。

## 5. 路由与迁移兼容

兼容报告继续包含：

- `omittedSourcePages`；
- `routeNormalizations`（旧 source route -> 新 public route）；
- unresolved internal Markdown links；
- projection item ID 与最终 URL 的映射。

旧 MkDocs 路由切换时，生成静态 redirect 或 `404` 兼容页面只能引用 public route；不得为了兼容旧路径把旧 docs 原文重新复制进 dist。路由 map 属于迁移生成物，和 manifest hash 一起入库，变化需 review。

## 6. Leak gate

### 6.1 输入 allowlist

在 Astro 启动前执行 `public-input-leak-gate/v1`、scope=`input-tree` 的全量输入扫描；构建完成后以 `public-leak-gate/v1`、scope=`dist` 重复扫描输入并加入 staging/dist：

- manifest `projection == public`；
- 每个 item `public_publishable == true`；
- body/附件都在 allowlist；
- 无 `confidentiality: internal`、任一 private `vault_id`/private vault 字段、内网 URL、绝对 private path、snapshot exact、LLM report、practice answer/explanation。

### 6.2 Staging 和 dist denylist

输入 manifest、正文和附件以及 staging 递归扫描文件名、文本、JSON、HTML、JS、CSS、sitemap 和 source map，命中以下任一项即失败。最终 dist 对 HTML 使用同一私有/凭据/路径规则，但允许 Astro/Starlight/Pagefind 正常 `<script>`；只拒绝危险嵌入、事件处理器和 `javascript:`/`vbscript:` URL，JS/CSS 不套用 HTML 标签正则：

- `sources/`、`archive/`、`practice/`、`state/`、`queries/local/` 路径或正文；确认事件文件也必须经过输入扫描；
- 任一 private object ID、标题、URL、vault ID 或可推断 private 数量；
- 高置信 `Authorization`/Cookie/API key/Bearer/私钥材料、private path、内网域名；普通运行时代码中的 `authorization` 字段名本身不算命中；
- `supporting_quotes.exact`、snapshot hash 绑定详情、验证报告字段；
- private lineage raw IDs/hashes、`source_vault_ids`、private confirmation/operation record fields；public event hash 和 `public_lineage_commitment`（lineage 记录路径的 sha256）仅在 allowlist 字段中保留；
- 不在 public catalog 的 graph node、link 或 Pagefind document；最终 `generated/build-manifest.json` 也必须包含在最后一轮 dist 扫描范围内。

扫描器输出 code、相对文件、匹配类别和 hash，不在 CI 日志回显匹配正文；失败时 staging 保留在受控临时目录供本机诊断，CI 上传脱敏报告。输入摘要和最终 dist 报告分别计算，不能把其中一个 hash 冒充另一个。

## 7. 原子发布和失败恢复

每次构建使用：

```text
frontend/.staging/<operation_id>/
frontend/dist.previous/
frontend/dist.next/
```

1. 校验 manifest/hash，生成 `dist.next`，并在 Astro 前执行 `input-tree` leak gate；
2. 运行 Astro、Pagefind、graph、catalog、route 和 staging/dist leak checks；
3. 写 `build-manifest.json`（canonical schema version `build-manifest/v1`：manifest/input-tree hash、Astro/Node/Pagefind 版本、结果和时间）；
4. fsync 后将 `dist` 原子替换为 `dist.next`，保留一份 `dist.previous`；
5. 任一步失败，删除未发布的 `dist.next`，保留原 `dist` 和上一份 manifest。

人工 confirmation 在第 1 步之前已经绑定 release input 和输入扫描摘要；第 3 步记录的是该次构建的最终 dist 报告，二者是不同摘要。最终报告不反向写入人工事件，也不能替代人工开关。无法生成或验证最终报告时，第 4 步不得执行。

不允许先清空正式 `dist` 再构建；不允许把 build warning 当作通过：未知 warning 阻断，只有 `policy.yaml` 中带版本的 framework advisory pattern 可以记录为 advisory。发布锁 `frontend/.staging/release.lock` 使用 `O_EXCL`，锁主体只写入不可变 operation/token/fencing/inode 记录；最新 `heartbeat_at` 写入同目录、同文件系统的 `release.lock.heartbeat` sidecar（canonical schema version `release-lock-heartbeat/v1`）并用临时文件 + fsync + rename 原子替换。持锁者始终校验主体 inode、operation 和 fencing token；存在锁时默认阻断，过期锁也不能自动删除，必须人工检查后显式恢复并留下审计记录。不允许在失败后自动回退 source/wiki 状态。

## 8. 本地完整模式

`astro dev` 可以代理 FastAPI `/api`，显示 source、evidence 和本地阅读状态，但其输入仍由后端 projection 控制。没有 FastAPI 时，页面自动退化到静态 public catalog；任何 API error 只影响本地增强区域，不影响文章、Pagefind 和图谱。public CI 不启动 FastAPI，也不读取 `queries/local`。

## 9. CI 与版本策略

GitHub Actions 在 public runner 上只 checkout public repo，执行：

```text
node --version / npm ci
npm run validate:config
npm run validate:docs
MYKNOWLEDGE_CONTENT_MODE=legacy-validation npm run validate:legacy  # 迁移基线
MYKNOWLEDGE_CONTENT_MODE=projection npm run validate:projection     # 仅在 manifest 存在时启用
```

Node、npm lockfile、Astro、Starlight、Pagefind 和插件版本固定；private vault、private secret、LLM provider 和 QMD 不作为 public CI 依赖。当前 workflow 只做验证，不自动 deploy；发布产物和人工 release confirmation 由单独授权步骤完成，验证失败不能替换旧 dist。

## 10. 测试策略

- projection allowlist、状态/保密过滤和 hash 一致性；
- 路由 slug、重复路由、相对链接、anchor/query 和 unresolved baseline；
- catalog 数量/唯一 ID、graph 节点边闭包、`?focus=`；
- Pagefind 中文/英文/混合查询和无搜索降级；
- Mermaid、KaTeX、图片和附件路径；
- localStorage 正常、损坏、禁用和版本迁移；
- source/archive/practice/internal ID/path/正文在输入、staging、dist、sitemap、JS 和 source map 中均不泄漏；
- Astro build、Pagefind、graph 或 leak gate 任一失败时旧 dist 不变；
- 无 FastAPI 时文章、搜索、图谱和首页仍可用；
- public projection 与 catalog/graph/Pagefind 文档集合完全一致。

## 11. 迁移与回滚

迁移阶段保留现有 `docs/` adapter，输出兼容性报告但不作为正式 public source。先选一小组已完成 evidence 的 Wiki 生成 projection，验证路线和 leak gate，再逐步扩大 manifest；旧站点在新 projection 通过 F007 验收前保持不变。切换后如果新构建失败，继续提供上一版 dist，修复 manifest/adapter 后重新构建，不回退 canonical source/wiki。

## 12. 实施参数

- GitHub Pages 的最终 base path 和 redirect 策略由部署仓库在接入时填写，不改变 projection 契约；
- Pagefind 的具体版本随 Astro lockfile 固定，升级时执行中文回归；
- `queries/public` 及其 projection manifest 入 Git，作为可审计的 public build 输入；它只能由生成器更新，禁止人工直接编辑。`queries/local` 仍忽略。
