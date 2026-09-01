# MyKnowledge 证据驱动知识系统设计

> 文档状态：架构设计与实施规范
>
> 更新时间：2026-08-26
>
> 实施边界：本文记录目标架构、约束和验收标准，不代表所有目标能力已经实现。

## 1. 文档目的

MyKnowledge 最初是个人知识博客和前端展示站点。重构后，当前版本承担三个工作流；另有一个不进入当前验收的 F008 扩展：

1. 查询阅读：快速找到已经学习过的知识，并沿关系和来源继续阅读。
2. 写入：把外部资料和个人原始文档稳定地纳入知识库。
3. 索引：从人工内容生成可查询、可导航、可供 Agent 使用的索引。
4. 做题（F008，后续）：单选题、多选题和面向面试的简答题；不属于当前主链路。

系统有两个运行环境：

- **公开静态环境**：部署到 kinchow.github.io，只展示已经通过证据门禁的 wiki 内容，不依赖后端。
- **本地完整环境**：启动 FastAPI 后端，提供 sources/wiki 的查询、写入辅助和验证；Question/练习能力留给后续 F008。

同时，系统提供 myknowledge Agent Skill。Skill 是 Agent 访问知识库的受控入口，不能绕过模板、schema、证据检查、LLM 验证和用户确认直接修改文件。

### 1.1 阅读顺序和术语

本文按“抽象模型 -> 数据契约 -> 工作流 -> 技术实现 -> 迁移和验收”的顺序组织。第一次阅读时建议先看第 2 至 4 节，理解三层数据和两个运行面；需要实现时再按第 5 至 15 节逐项落地；第 16 至 19 节用于迁移、测试和发布判断。

本文中的几个词有固定含义：

| 术语 | 含义 |
| --- | --- |
| source | 原始资料的结构化记录，保存来源、读取范围和证据边界 |
| wiki | 基于一个或多个 source 综合出的人工知识页面 |
| claim | wiki 中可以独立判断真假的核心论断 |
| snapshot | 不可变、内容寻址的归档文本或本地文件版本，是证据的事实载体 |
| evidence item | 绑定 snapshot 的 TextQuote/TextPosition selector，可被确定性解析的证据锚点 |
| source locator | 面向阅读的 source 章节定位；不是唯一的事实证据，权威锚点是 evidence item |
| validation report | 针对某个 content/wiki/source 内容 hash 生成的 LLM 证据验证报告 |
| operation | 一次可预览、可确认、可失效、可追踪的写入操作 |
| projection | 从同一内容库生成的 public 或 local 数据视图 |

## 2. 当前基线与目标边界

### 2.1 当前仓库基线

当前 MyKnowledge 已有：

- docs/ Markdown 内容源；
- MkDocs 配置；
- Astro + Starlight 展示层；
- Pagefind 静态搜索；
- Cytoscape 关系图；
- Mermaid 和 KaTeX 渲染；
- 浏览器本地收藏、最近阅读和阅读状态；题目复习留给 F008。

当前验证过的构建基线（legacy content adapter，2026-08-26）：

- 内容输入为 277 个 Markdown 文件（包含根目录 `docs/index.md`）；
- 排除根目录索引后生成 276 篇内容文章；
- 生成 224 条显式 Markdown 关系；
- 仍有 19 条未解析的内部 Markdown 链接需要在迁移阶段处理。

`docs/acceptance/`、`docs/adr/`、`docs/technical-design/`、`docs/deferred/` 以及根目录设计索引属于治理文档，不是公开 Wiki 内容，legacy adapter 必须排除它们。正式构建切换到 `var/queries/public` 后，`docs/` 只作为迁移输入，不再是静态站点的直接输入。

当前文章没有统一的知识库 Front Matter，原始 docs/ 不能直接被视为已经完成 source/wiki 分层的语料。

### 2.2 目标边界

目标系统必须满足：

- sources 先行，wiki 后置；
- wiki 必须有 source 证据，不能凭空创建；
- 后续 F008 的 question 必须绑定 wiki 的 claim；当前版本不创建 question；
- 保密分级统一声明、向下游传染，非公开内容只存在于可插拔的 private vault；
- wiki 必须经过确定性校验和 LLM 逐条证据验证；
- 未验证的 wiki 不得进入公开静态构建；
- public 和 local 使用不同的索引投影；
- public 静态 Wiki 使用现有 Astro/Starlight、Pagefind、Cytoscape 流水线，并由独立的发布投影和 leak gate 驱动；
- Agent 只能通过 Skill 和领域工具写入；
- 后续 F008 的复习状态属于本地用户数据，不进入公开仓库；
- internal 内容可以在 private vault 内经明确确认后发布，但必须显示告警；对外公开发布必须是单独的 release 操作。

不在第一阶段实现：

- 在线多用户协作；
- 云端数据库和账号系统；
- Elasticsearch 或独立向量数据库作为第一版的硬依赖；
- 让 LLM 直接替代结构化查询；
- 自动提交、推送和发布远程仓库。

## 3. 总体架构

~~~mermaid
flowchart TD
    A[外部资料 / 个人原始文档] --> B[sources 原始证据层]
    B --> C[确定性 schema 与引文校验]
    C --> D[LLM 规范审计 · 可选]
    C --> R[人工审计 · 必须]
    D --> R
    R --> E[wiki 人工综合知识层]
    E --> S{public_publishable?}
    S -->|yes| F[public 索引]
    F --> G[Astro 静态构建]
    G --> H[kinchow.github.io]

    B --> I[local 索引]
    E --> I
    I --> J[QMD 检索]
    J -->|不可用| K[SQLite FTS5]
    I --> K
    K --> L[FastAPI 本地后端]
    J --> L
    L --> M[本地完整前端]
    M --> N[查询与阅读]

    I --> P[myknowledge Agent Skill]
    P --> Q[Agent 查询 / 写入 / 索引]
~~~

### 3.1 数据流

~~~text
外部资料或个人文档
  -> source 模板
  -> source 校验
  -> wiki 候选
  -> claim/evidence 映射
  -> 确定性引文校验
  -> LLM 规范审计（可选）
  -> 人工审计确认（必须）
  -> wiki 原子写入
  -> public/local 索引
  -> 静态前端 / 本地后端 / Agent Skill
~~~

### 3.2 核心不变量

以下规则属于 blocking gate，违反即失败：

1. 外部资料和个人编写的原始文档必须先进入 content/sources/。
2. `kind: knowledge` 的 wiki.sources 不能为空；`kind: index`、`kind: reference` 和 `status: planned` 按 6.7 分档处理。
3. wiki.sources 中的每个 ID 必须存在。
4. source 只有 metadata 时不能支撑 published 的 `kind: knowledge` wiki。
5. `kind: knowledge` wiki 的每个核心论断必须有 claim 和至少一个绑定 snapshot/selector 的 evidence target；source locator 仅用于阅读导航。
6. wiki 必须通过确定性校验（schema、target 解析、snapshot 可读、selector 范围、`supporting_quotes.exact` 逐字匹配、hash 绑定）。这是唯一自动阻断门。
7. 发布必须有绑定当前 `(content_sha256, evidence_sha256)` 的人工审计确认。LLM 规范审计是可选层：未运行时 `validation_state: not_run`，不阻断且不得表述为已验证；运行后为 `fail` 时阻断；LLM 通过不替代人工审计，LLM 未运行也不改变人工审计的要求。详见 ADR-0010。
8. var/queries/ 是生成物，禁止人工直接编辑。
9. public 构建只能包含 `public_publishable: true` 的 wiki。
10. Agent 不能直接编辑 Markdown、索引、前端或后端代码。
11. 写入必须经过 preview、用户确认、hash 检查和原子应用。
12. 不执行自动 commit、push、发布和远程系统写操作。
13. `confidentiality: internal` 的对象只能存放在已挂载且等级足够的 private vault；任何允许 public projection 的 vault 中出现 internal 对象仍然是阻断错误。
14. wiki 的有效保密等级取自身声明与全部上游 source 的最高等级；internal 对象可以在明确选择的 private vault 内经显式确认后以 `status: published + publication_scope: private` 进入 `private_publishable` 投影，但默认不得进入 public projection、Pagefind 或外部快照服务。Question 的保密传染留给 F008。
15. 内容 hash 只覆盖正文和语义字段；tags、aliases、related 等分类字段变化不使验证报告失效。
16. Question 的 claim 绑定和状态门禁属于后续 F008，不是当前主链路的不变量。
17. 证据要求可以按页面类型分档（免 sources 或免 claim 级 evidence），但任何一档都不免除确定性校验；每档必须有替代检查且证据强度对读者可见。
18. `planned` 和 `deprecated` 页面不进入 public build、不作为 RAG 召回来源、不能被新的 claim 引用。
19. 删除内容必须先 `retire` 再 `purge`，且必须在 manifest 中留下 ID、hash 和废弃原因。
20. Source 只表示“已收集并声明了证据边界”，不表示来源必然正确；多个独立 source 对同一 claim 的一致支持提高 corroboration，但不能替代冲突检查和人工确认。
21. Source 之间出现矛盾、版本不一致或证据覆盖不足时，Wiki 必须设置 `status: review`，并将 `evidence_state` 设为 `conflicting` 或 `partial/unresolved`，不得静默按多数票发布。
22. 契约一次性定稿：接口、fallback、失败恢复必须在同一契约内实现，不以先做临时版本再重写为交付方式。实现允许按垂直切片推进（见 18 阶段零）——收窄覆盖面是允许的，降级为临时接口不是。
23. `public_release` 默认必须为 `false`；只有明确的人类操作才能为当前 hash 创建 confirmation，使 projection 派生 `public_release: true`，自动化、LLM、Agent 和 leak gate 不能代替该操作。
24. 每个 private vault 的 Git remote 与加密备份目标当前均为 `null`，各自 `backup_state` 为 `unconfigured`；工具必须逐 vault 告警，不得把任一仅有本地副本描述为已备份或可恢复。
25. 本地自然语言/混合检索默认使用 QMD；SQLite FTS5 是必选确定性 fallback，QMD 不可用时再回退 FTS5，FTS5 不可用时回退 Python/SQLite LIKE；公开 Astro 构建不依赖 QMD。
26. Canonical Source/Wiki 的内容引用必须在同一 owner Vault 内解析；任何 public-to-private 或 private-to-private 内容引用在写入/校验阶段直接拒绝。跨 Vault 的 `source_vault_ids` 只能出现在私有 lineage/audit，不是内容依赖。

### 3.3 三层数据的所有权

```text
sources   = 证据事实的入口，允许半自动生成，但必须人工校对
wiki      = 面向理解的人工综合，必须逐条绑定证据
queries   = 可重建的索引投影，任何手工修改都会在下次生成时被覆盖
```

`content/practice/` 目录为 F008 预留，不属于当前主链路；当前索引和发布不读取题目。`var/state/` 是本机运行状态：它可以记录操作和阅读偏好，但不能改变仓库中 source、wiki 的事实内容。

## 4. 目录与对象模型

仓库根目录由「若干工程根 + 三个数据域」组成：组件目录因为语言生态约束必须平铺在根（见 §4.4），数据侧收敛为 `content/`、`ledger/`、`var/` 三个域。知识领域仍由目录路径和 `domain` 表达；来源类型不再通过 blogs/、docs/、books/ 等物理目录表达，而是通过 Front Matter 表达。

~~~text
MyKnowledge/
├── tools/  backend/  frontend/  tests/  scripts/  skills/   # 组件：工程根，必须平铺
├── config/                     # 运行时契约：schemas.yaml / vocab.yaml / policy.yaml / vaults.*.yaml
├── docs/                       # 规范与设计；ruleset 运行时按 (doc, section) 抽取，属组件侧输入
├── templates/                  # 正文与 Front Matter 模板
│
├── content/                    # 域 1：人写、可编辑、不可重建、per-vault
│   ├── sources/<domain>/       #   managed，source/v1
│   ├── working/                #   unmanaged，过渡区，有 TTL
│   ├── journal/<YYYY>/<MM>/    #   unmanaged，append-only，无出口
│   ├── decisions/              #   轻管，内容级判定记录（CDR）
│   ├── wiki/<domain>/          #   managed，wiki/v1
│   │   └── assets/             #   public 附件
│   └── practice/questions/     #   F008 预留；当前版本不读取
│
├── ledger/                     # 域 2：机器写、不可变、append-only、被派生规则引用、per-vault
│   ├── archive/                #   text/  raw/  manifest.jsonl
│   ├── audit/                  #   operations/  validation/  backup/  retire/
│   └── release/                #   public-confirmations/：public-safe 人工确认事件
│
└── var/                        # 域 3：机器写、可重建、可删
    ├── queries/                #   public/  local/
    ├── state/                  #   本机运行态，Git 忽略，不是事实源
    └── reports/                #   验收与体检报告
~~~

`<domain>` 取值受 `config/vocab.yaml` 的 `domains` 约束，未知 domain 直接拒绝。`content/` 与 `ledger/` 在每个 vault 内结构一致；`var/` 只在 public checkout 内存在。

### 4.1 目录和元数据的职责

| 信息 | 位置 |
| --- | --- |
| 人写内容 / 不可变记录 / 可重建产物 | 顶层数据域 `content/`、`ledger/`、`var/` |
| 加工阶段（来源、过渡、日志、判定、成品） | `content/` 下的层目录 |
| 计算机科学、工具、工作方法等知识领域 | 目录路径和 domain |
| knowledge、index、reference | kind |
| draft、review、published | status |
| 复审到期时间 | wiki 的 `review_by`（报告项，见 §6.2） |
| 博客、文档、个人笔记、播客、视频、PR | source_type |
| 外部资料或个人资料 | origin |
| 标签、别名和关系 | tags、aliases、Markdown 链接、related |
| source 证据映射 | wiki 的 evidence |
| 对象所属 vault | object_ref 的 `vault_id`，不由路径表达 |
| 题目归属 | F008 预留；当前版本不建立题目关系 |

contents.md 在迁移后作为 kind: index 的普通 wiki 页面，不建立额外的 MOC 目录。

### 4.2 Vault 与保密分级

Private Git 仓库、多个子仓库挂载、unavailable 语义和内部发布告警的可执行接口见 [Private Vaults 子仓库实现设计](./technical-design/private-vault-submodule.md)。

当前仓库是 `public` vault。非公开资料放在 `0..N` 个独立的 private Git 仓库中，以可插拔 vault 子仓库形式挂载；任何 private 仓库都不把正文、快照或索引复制进 public 仓库。

~~~yaml
# config/vaults.local.yaml（被 .gitignore 忽略；public repo 只提交 vaults.example.yaml）
workspace_root: null              # 无外挂 vault 时表示当前 public worktree；有外挂时必须显式填写
vaults:
  - id: public
    path: .
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
    path: null                         # 仅 local manifest 填写
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
~~~

每个 private vault 的目录结构与 public vault 相同（`content/sources/`、`content/wiki/`、`content/practice/`、`ledger/archive/`、`var/queries/`），但位于独立私有 Git 仓库。推荐由一个本地私有 workspace superproject 管理 public repo 和任意数量的 private repo：

~~~text
MyKnowledge-workspace/
├── public/
└── vaults/
    ├── team-internal/
    ├── personal-private/
    └── research-private/
~~~

public repo 不提交任何 private remote URL、子仓库指针或 private 路径；若需要固定版本，submodule 指针只提交到私有 workspace。public repo 只提交不含路径的 `config/vaults.example.yaml`，实际路径和每个 vault 的运行参数放在被忽略的 local manifest。

当前 checkout 可以直接作为 `public` vault 运行。路径解析规则只有两种：`layout: direct-checkout` 且没有外挂 vault 时，`workspace_root: null` 将当前 public worktree 作为 root，`public.path: .` 是唯一特殊值；只要要挂载外部 private checkout，local manifest 就必须显式填写同时包含 public 与外挂仓库的 `workspace_root`，并把 `public.path` 改为该 root 下的相对路径。`layout: superproject` 时 `workspace_root` 必须是私有 superproject 根，public 路径通常为 `public`。两种布局共享同一 Vault Registry，不产生第二套数据模型；所有 path 必须是 root 内的相对路径，realpath 后彼此不重叠。

工具启动时由 Vault Registry 按稳定 `vault_id` 合并对象空间：`(vault_id, object_type, object_id)` 是对象的完整引用键，ID 只要求在**所属 Vault 内**唯一；不同 Vault 可以各自拥有同名知识对象，因为它们通常独立维护且不互相引用。Wiki、Evidence 和 Source 只能在同一 Vault 内互相引用，跨 Vault 内容引用在 canonical 校验阶段直接拒绝；`source_vault_ids` lineage 不属于内容引用。每个 vault 独立报告 `available`、`unavailable`、`revision_mismatch`、`dirty`、`conflict` 或 `invalid`；一个 vault 未挂载时只将其对象标记为 `availability: unavailable` 并附原因，不影响无关 vault 的查询和索引。

Vault 等级按 `public < internal` 比较：对象的有效保密等级不得高于所在 Vault 等级；internal Vault 可以保存 public 对象，但 public projection 的 owner 只能是 `vault_id: public` 且 `allow_public_projection: true`。因此“放在 private Vault”不会自动获得公开资格，也不会改变对象 owner。

保密等级规则：

| 规则 | 说明 |
| --- | --- |
| 枚举 | `confidentiality: public / internal`，缺省 `public`；后续如需更多等级在 `policy.yaml` 中扩展，等级之间必须是全序 |
| 存放位置 | `internal` 对象只能位于 `confidentiality: internal` 的 vault；任何 `allow_public_projection: true` 的 vault 中出现 `internal` 声明即为校验失败（当前只有 `public` vault 允许 public projection） |
| 传染 | wiki 有效等级 = max(自身声明, 全部被引 source 的等级)；Question 规则留给 F008 |
| 发布 | `internal` 对象只能在其 owner private vault 内以 `status: published` + `publication_scope: private` 进入派生的 `private_publishable` 投影；必须有 `operation-confirmation/v1`（`scope: publish_private`，且带 `warning_code`/`warning_text_sha256`）。`target_vault` 在创建/迁移时决定 owner，后续 `publish_private` 必须与 owner 相同；跨 Vault 搬迁必须生成新 owner copy 和 lineage，不能建立内容引用。进入 public projection 必须另行执行 `public_release`，默认 false，人工为当前 hash 创建 `public-release-confirmation/v1` 后由 projection 派生 true，自动流程不能完成 |
| 外部服务 | `internal` source 不得提交到 Wayback 等外部快照服务；确认后可以发送给 `internal_allowed` provider，但仍不得发送给 public provider |

任一 private vault 未挂载时，其中的对象视为 `unavailable` 而不是"不存在"：引用它们的 wiki 保持声明字段不变，派生 `availability: unavailable` 和阻断码 `upstream_unavailable`，并保留最近一次可计算的 `evidence_state`（从未成功计算时才为 `unresolved`）；校验器不得据此把已有 evidence 改成 `missing`、不得降级或改写引用。上游不可用属于 `availability` 轴，不写入 `validation_state`。其他已挂载 vault 仍可查询和生成不相关 projection；这样同一份 public 仓库在不同 private vault 组合的机器上都不会互相破坏校验结果。

安全边界：public vault 或某 private vault 中如果有对象引用了另一个 Vault 解析的 source/wiki ID，写入和校验都必须报告带 source/target `vault_id` 的 `cross_vault_reference` 并拒绝该 operation；不能先写入再仅靠 projection 过滤。迁移到另一个 Vault 必须生成新的 owner copy，并把原对象关系保存在私有 lineage/audit 中。目标 private vault 未挂载时显示 `availability: unavailable`，但不能把引用改成 missing 来绕过门禁。

未配置任何 private vault 时，全部行为兼容当前的单一公开仓库；挂载一个或多个私有子仓库后启用同一套合并、验证和私有发布流程，不另起数据模型。每个 private vault 的 Git remote、加密备份目标和 `backup_state` 独立维护；当前均使用 `null`/`unconfigured`。普通查询与可逆编辑可用，但 `vault check` 和涉及相应 vault 的高风险操作必须显示带 `vault_id` 的 `backup_not_configured`，不可宣称恢复链路就绪。

manifest 为了保持结构统一，可以在 `public` 条目中保留置空的 private remote/backup 字段；这不表示 public vault 没有其正常 Git 发布链路，也不把 public 条目计入 private 备份告警。`backup_not_configured` 只针对包含 private 数据的 vault 或涉及其数据的高风险操作。

### 4.3 仓库内容与生成物归属

必须明确每一类文件是"内容"还是"生成物"，否则每次重建索引都会产生大片脏 diff，而真正需要备份的用户数据反而没进版本管理。

| 路径 | 类别 | Git | 理由 |
| --- | --- | --- | --- |
| `content/sources/`、`content/wiki/`、`content/practice/` | 内容 | 入库 | 唯一真相源 |
| `config/`、`templates/`、`tools/`、`backend/`、`frontend/`（源码） | 内容 | 入库 | 规范与实现 |
| `ledger/archive/text/`、`ledger/archive/manifest.jsonl` | 证据副本 | 按 vault 入库 | public 只保存明确允许公开的资料；internal 只进入 private 子仓库 |
| `ledger/archive/raw/` | 证据副本 | private 子仓库优先，必要时 git-lfs | 原始文件默认不进入 public 仓库 |
| `var/queries/public/` | 生成物 | 入库 | 静态站构建输入，需要可复现发布 |
| `var/queries/local/`、`rag-index.jsonl`、向量索引文件 | 生成物 | 忽略 | 体积大、可重建、每次重建全变 |
| `ledger/audit/operations/`、`ledger/audit/validation/` | 持久审计/验证摘要 | 按 owner vault 入库；public-safe 摘要可进入 public repo | 人工操作者、确认事件、验证 attestation 和 hash 绑定不可重建，必须随对应内容保留；不得包含敏感正文 |
| `ledger/release/public-confirmations/` | public release 人工确认事件 | public-safe，入 public Git | public projection 在另一台机器上仍能复现当前人工批准；事件不得包含 private ID、路径或正文 |
| `var/state/operations/`、`var/state/llm-validation/` | 本机临时运行态/完整 provider 报告 | 忽略 | 可清理；不能作为发布或恢复的唯一依据 |
| `var/state/local-sources/` | 本机 local-file sidecar | 忽略 | 保存绝对路径映射和 file hash；不得进入 canonical Source、public artifact 或日志 |
| `var/state/reading/`（本地阅读状态） | 用户数据 | 本机 localStorage/状态目录 | 不属于 canonical 内容；F008 题目复习另行定义 |
| `.cache/fetch/`、`frontend/dist/`、`node_modules/` | 临时物 | 忽略 | 无保留价值 |

`var/queries/public` 入库是有意的：它决定公开站点的内容，需要能对照某个 commit 复现一次发布。`var/queries/local` 不入库，因为它随每次索引重建整体变化，且可以从内容完全重建。发布确认和验证 attestation 不能只放在被忽略的 `var/state/`；否则另一台机器无法判断当前 hash 是否确实经过人工批准。

相同 `snapshot_sha256` 的物理去重只发生在内容寻址 blob 层：默认每个 owner Vault 都保留自己的 manifest record 和可恢复路径；可选的 workspace blob cache 只是派生缓存，必须按 `(vault_id, snapshot_sha256)` 做权限检查，不能成为唯一备份或唯一解析入口。不同 Vault 的 Source/Wiki、evidence、confidentiality、备份和发布状态永远不因相同 snapshot 自动合并。

`ledger/archive/raw/` 从启用归档的那一次变更起就走 git-lfs，不经过"先普通入库、以后再迁"的中间状态。原因是 git 历史里的 blob 删不掉：一旦二进制原件以普通对象提交过，事后迁 LFS 必须重写历史（`git filter-repo`），而这个仓库是公开的、已有远端，重写历史会打断所有已有 clone 和引用。先配置后归档的顺序成本几乎为零，反过来就很贵。

启用步骤是归档功能的前置条件，缺一不可：

~~~text
git lfs install
git lfs track "ledger/archive/raw/**"      # 写入 .gitattributes 并提交
# 确认 .gitattributes 已生效后，才允许 Source 导入工具写入 raw
~~~

Source 导入工具启动时必须检查 `.gitattributes` 中存在对应的 LFS 规则；不存在时拒绝写入 `ledger/archive/raw/`，只写 `ledger/archive/text/` 并降级为 `archive_policy: text-only`。这条检查把"忘记配 LFS"变成一次明确失败，而不是一堆已经进了主仓历史的二进制文件。

`ledger/archive/text/` 保持普通入库：它是可解压回 canonical 文本的压缩 blob，体积在几 MB 量级，需要 Git 历史可追溯性，不适合放进 LFS；snapshot hash 和 selector 永远对解压后的逻辑文本计算。

复习进度属于后续 F008 的用户数据边界，不纳入当前主链路。F008 确定题型、判分和复习算法后，再定义其备份与恢复要求。

生成物统一带生成器版本、生成时间、输入集合 hash 和 schema 版本；`var/queries/` 中的任何手工修改都会在下次生成时被覆盖，工具不做保护。

### 4.4 布局判据与三个数据域

目录结构的唯一职责是让「这东西该放哪」「要不要备份」「能不能删」有唯一答案。归属由五条可判定属性决定：

1. **谁写**：人手写 / 机器生成；
2. **能否重建**：删除后能否用命令重新生成；
3. **是否被引用锁定**：路径是否写进 append-only 记录或派生规则；
4. **是否随 vault 复制**：per-vault / 只在 public checkout；
5. **是否是语言生态的工程根**：是否必须位于特定位置才能 import 或构建。

第 5 条决定组件不进子目录：`python -m tools.cli` 依赖 `tools/` 位于仓库根即 `sys.path[0]` 下，`frontend/` 是独立 npm 工程根。把它们收进 `platform/` 或 `src/` 会改写全部 import、Agent Skill 入口和文档命令，成本远大于收益。**组件平铺在根是生态约束下的正解，不是布局缺陷**；需要收敛的是数据侧。

数据域准入规则（新增目录按此判定，不允许无归属目录）：

| 域 | 判据 | 备份 | 可否删除 |
| --- | --- | --- | --- |
| `content/` | 人手写、可编辑、删除后必须重写 | 必须 | 否 |
| `ledger/` | 机器写、只能追加、路径被 durable 派生规则引用 | 必须 | 否 |
| `var/` | 机器写、可用命令重新生成 | 不必 | 可 |
| 根级组件 | 需要被 import 或作为外部工具的工程根 | 随代码 | 否 |
| `config/`、`docs/` | 运行时读取的契约与规范原文 | 随代码 | 否 |

`ledger/archive/` 虽然是「来源的副本」，但它是机器抓取、内容寻址、人不可编辑的，且 `manifest.jsonl` 是 append-only，因此按判据 1 与 3 归入 `ledger/`，不进 `content/`。`docs/` 虽然是人手写的，但 LLM 规范审计的 ruleset 在运行时按 `(doc, section)` 抽取其原文并计算 `extract_sha256`（见 §8），因此它是运行时输入，属组件侧，不进 `content/`。



### 4.5 五层与三条写入通道

`content/` 内部按加工阶段分五层。层的物理位置与对象归属的关系取决于它是否有 object 身份：

| 层 | 受 schema 管 | object 身份 | 进 projection | TTL | 出口 |
| --- | --- | --- | --- | --- | --- |
| `sources/` | 是，`source/v1` | 有 | 否（仅被引用） | 无 | 被 wiki 引用 |
| `working/` | 否，unmanaged | 无 | 物理不可能 | 30 天 | wiki / journal / 删除 |
| `journal/` | 否，unmanaged | 无 | 物理不可能 | 无 | 无出口，终点 |
| `decisions/` | 轻管（CDR 模板） | 无 | 物理不可能 | 无 | 无出口，终点 |
| `wiki/` | 是，`wiki/v1` | 有 | 是 | 无，用 `review_by` | published → public release |

「进 projection 物理不可能」不是额外门禁：`policy.yaml` 的 `projection.body_path_prefixes` 只允许 `var/queries/public/` 与 `content/wiki/`，未列出的前缀无法成为 `body_path`。

**vault 归属的差异**：`sources/` 与 `wiki/` 有 `object_ref = [vault_id, object_type, object_id]` 且被 `evidence.targets` 真实引用，因此必须每个 vault 各有一份。`working/`、`journal/`、`decisions/` 是 unmanaged、没有 object 身份，`working → wiki` 是人工重写而不是对象引用，因此不构成 cross-vault reference，可以只存在一份：放在当前可用的最私密 vault 中。未挂载 private vault 时这三层位于 public checkout；挂载后 internal 素材使用该 vault 自己的 `content/working/`。维护面因此是 `2N + 3` 而不是 `5N`。

三条写入通道，门禁强度与出口封锁各不相同：

- **通道 A 主链路**：`source → snapshot → evidence item → claim → 确定性校验 → LLM 审计 → 人工确认 → published → public release`，产出 `strength ∈ {verified, corroborated, attested}`。规范见 §5–§9，不因本节改变。
- **通道 B 降级落位**：写入 `content/working/`，唯一硬约束是 `source_ref` 或 `legacy_path` 非空。它**不产生 wiki 对象**，因此不存在"五字段快速 wiki 条目"这种入口（原快速通道设计已取消，理由见 ADR-0014 决策 4）。存量误登记为 source 的加工文档整批降级到这一层；`content/wiki/` 只能**逐篇人工升级**进入，升级即走通道 A 全流程。安全性由出口封锁保证：不进任何 projection、不出现在任何 wiki 的 `evidence.targets`、不进 RAG 召回。
- **通道 C 日志**：写入 `journal/`，零门槛，不产生对象，永不升级。

降级与升级不对称是有意的：降级是**批量**动作（承认"它本来就不是 source"这一事实，一条 CDR 记录整批理由即可），升级是**逐篇**动作（八段正文 + claim/evidence 映射 + 引文逐字校验 + 人工确认，无法批量代劳）。任何"把 working 批量升级进 wiki"的路径都不存在——批量升级等于批量伪造证据链。

层间 gate：进入 `working/` 的唯一硬约束是 `source_ref` 或 `legacy_path` 非空；`working/` 到期由 `doctor` 报告，人工在「升级 / 转 journal / 删除」三者中选择，工具永不自动删除。`wiki` 执行 retire 或 deprecate 时必须在 `decisions/` 留一条 CDR 记录理由，判定值沿用 §16.2 `content_verdict` 的四值语义。

unmanaged 层不参与 operation 协议：它们不进入 `before_hashes`/`after_hashes`，手工编辑与后台 apply 的路径集不相交，`locks.scope: per-vault` 无需扩展。它们也没有 `object_ref`，因此不能进入 `query-result/v1`；检索由独立的文本匹配命令提供，不伪造 object 身份。

### 4.6 路径域基线与迁移映射

本表是路径归属的唯一事实源。下游 Technical Design、Acceptance、`config/` 与代码中仍存在的历史路径按本表映射；两者不一致时以本表为准，且必须在执行对应迁移 commit 时同步更新。

| 历史路径 | 目标路径 | 迁移批次 |
| --- | --- | --- |
| `queries/` | `var/queries/` | 批次 1 |
| `state/` | `var/state/` | 批次 1 |
| `reports/` | `var/reports/` | 批次 1 |
| `specs/`（空目录） | 删除 | 批次 1 |
| `sources/` | `content/sources/` | 批次 2 |
| `wiki/` | `content/wiki/` | 批次 2 |
| `practice/` | `content/practice/` | 批次 2（F008 预留，尚未创建） |
| 新增 | `content/working/`、`content/journal/`、`content/decisions/` | 批次 2 |
| `archive/` | `ledger/archive/` | 批次 3 |
| `audit/` | `ledger/audit/` | 批次 3 |
| `release/` | `ledger/release/` | 批次 3 |

迁移的可行前提是**对象身份与物理路径解耦**：`target_ref` 是 `object_ref` 而非路径，`record_sha256 = sha256(canonical_json(record_without_record_sha256))` 不包含路径，因此搬移目录不改变任何对象身份、引用或既有记录的 hash。

三条不变量约束迁移方式：

- 历史 `operation` 记录中的 `applied_files` 记录的是**当时**的相对路径。它们是历史事实，受 `record_sha256` 覆盖且受 `audit.append_only` 约束，**不得重写**；读取侧必须容忍历史路径形态。
- `ledger/archive/manifest.jsonl` 的 `archive_path` 指向 `ledger/archive/text/`，批次 2 不影响它；批次 3 只改声明式路径常量，不重写已有 manifest 行。
- `body_path` 属于 `release_input_fields`，因此批次 2 会改变 `release_input_sha256`，已发布页面的 `public_release` 按 `hash_change_behavior: retain-old-event-but-derive-false` 自动回落 `false`，需重新执行一次人工确认。`route` 与 `body_path` 是独立字段，公开路由不变，不产生死链。

`docs/<domain>/` 下的存量旧文档是 `content/working/` 的临时前身：它的 `legacy_path` 已记入迁移台账，因此不参与上述搬移；迁移完成后按 §16 的退役条件删除该目录。

## 5. Source 规范

### 5.1 Source Front Matter


~~~yaml
---
id: source-transformer-paper
title: "Transformer 原始资料"
domain: computer-science
origin: external
source_type: doc
provenance:
  publisher: "example.com"
  derived_from: []
  independence_group: "publisher-or-experiment-identity"
confidentiality: public
url: "https://example.com/source"
captured_at: 2026-08-25
tags: [transformer]
aliases: []
read_status: retrieved
evidence_status: source-reported
related: []
retrieval:
  acquisition: fetch
  fetched_at: 2026-08-25T10:12:00+08:00
  http_status: 200
  etag: 'W/"6f21-abc"'
  last_modified: "Mon, 18 Aug 2026 03:00:00 GMT"
  snapshot_sha256: "sha256:9f2c..."
  raw_sha256: "sha256:41ab..."
  archive_policy: text+raw
  snapshot_url: "https://web.archive.org/web/20260825/https://example.com/source"
  extractor_name: trafilatura
  extractor_version: "2.2.0"
  extractor_options_hash: "sha256:..."
  normalization_version: canonical-text-v1
evidence_items:
  - id: e1
    snapshot_sha256: "sha256:9f2c..."
    locator:
      heading_slug: "已读取事实"
      selector:
        - type: TextQuoteSelector
          exact: "The output is computed as a weighted sum of the values."
          prefix: "For each query, key, and value tuple, "
          suffix: " The weights are normalized before aggregation."
        - type: TextPositionSelector
          start: 1204
          end: 1262
          offset_space: unicode-code-point
    selector_sha256: "sha256:..."
    quote_sha256: "sha256:..."
---
~~~

Source 文件中的 `vault_id` 仍由 Registry 注入，不由作者填写；上面的示例省略该派生字段。`evidence_items` 的 `exact` 必须是 `snapshot_sha256` 对应归档正文的逐字子串，不能把 Source Markdown 的中文摘要当作证据。

### 5.2 Source 正文模板

~~~markdown
# 资料标题

## 摘要

## 已读取事实

## 关键接口或约束

## 适用范围

## 未读取部分与疑点

## 证据边界
~~~

### 5.3 Source 字段约束

origin：

- external：外部博客、文档、书籍、PR、竞赛资料等；
- personal：用户自己的原始文档、观察、实验记录和经验总结。

source_type：

- blog；
- doc；
- book；
- contest；
- pr；
- local-file：本地代码、PDF、离线文档、日志和实验输出，见 5.8；
- personal-note。

read_status：

- metadata-only：只拿到目录、标题、链接或附件占位符；
- partial：正文只读取了一部分；
- retrieved：已获取目标正文范围。

evidence_status：

- source-reported：外部来源明确表达的事实；
- common-knowledge：语言标准、公开规范、教科书级公认事实，必须给出可查证的权威入口（标准号、官方文档、cppreference 等），见 6.7；
- personal-observation：个人观察或个人实验记录；
- inferred：根据来源、代码、日志或实验推断；
- metadata-only：只有资料入口，不支撑正文结论。

confidentiality：

- public：可以进入公开仓库和公开构建的资料；
- internal：内部资料、受限文档和不可对外的实验数据，只能位于 private vault。

保密等级由人工声明，工具不猜测，但网络安全检查不能被人工声明关闭。写入 preview 时，如果 URL、任一 redirect 或 DNS 解析命中 policy 的内网域名模式（以及始终启用的 loopback、RFC1918、link-local、`.local`/`.internal` 规则），而声明为 `public`，必须直接阻断并要求改为 `internal` 或改用 private vault；即使声明为 `internal`，也只能写入 private vault，并按 provider/归档外发门禁处理。

### 5.3.1 Source 字段级契约

Source Front Matter 的 canonical schema version 是 `source/v1`，其中 `evidence_items` 的每个元素单独定型为 `evidence-item/v1`（因为它会被 Wiki 的 target 与验证报告独立引用）。两者在 `config/schemas.yaml` 的 `objects` 注册表中登记；下表是字段级约束，不重复注册表内容。

| 字段 | 必填 | 约束 |
| --- | --- | --- |
| id | 是 | 在所属 Vault 内唯一的 kebab-case 标识，写入后不自动重命名；跨 Vault 可以同名 |
| vault_id | 生成 | 由 Vault Registry 根据实际文件所属仓库注入；写入请求必须明确目标 vault，不能由页面作者伪造 |
| title | 是 | 非空，作为查询和阅读显示名 |
| domain | 是 | 必须来自 `config/vocab.yaml`，并与目录领域一致 |
| origin | 是 | `external` 或 `personal` |
| source_type | 是 | `blog`、`doc`、`book`、`contest`、`pr`、`local-file`、`personal-note` |
| confidentiality | 是 | `public` 或 `internal`，缺省 `public`；必须与所在 `vault_id` 等级一致 |
| url | 网络来源必填 | 外部网页的原始链接；链接已失效时保留为历史出处，见 5.6.1 |
| url_status | 有 url 时必填 | `live`、`dead`、`unreachable`、`unknown` |
| local | local-file 必填 | `file_sha256`、媒体类型和读取范围必填；实际 `path` 只存在于被忽略的本机 local manifest/private sidecar，不进入 canonical Front Matter |
| captured_at | 是 | ISO 8601 日期或时间 |
| read_status | 是 | `metadata-only`、`partial`、`retrieved` |
| evidence_status | 是 | 与 origin 和正文证据边界兼容 |
| provenance | external source 建议；personal source 可为空 | 记录 publisher、derived_from 和 `independence_group`，用于区分独立来源与转载链；工具不凭域名单独推断独立性 |
| retrieval | 网络来源、`local-file` 和 `personal-note` 必填 | 获取/生成与归档元数据，必须含 `acquisition` 与 `snapshot_sha256`；personal-note 的 snapshot 由 canonical note body 生成 |
| evidence_items | retrieved/partial 且被 Wiki 引用时必填 | 每个 item 必须绑定 `snapshot_sha256`、`TextQuoteSelector`、`TextPositionSelector`（可由工具从已归档正文生成后人工确认） |
| tags、aliases、related | 否 | 缺省为空数组，不能写成未解析字符串 |
| content_sha256 | 生成 | 按 6.6 的规范化正文计算，Agent 不得手写 |

`read_scope`、附件清单和人工校对备注放在正文的“证据边界”章节或扩展 metadata 中。source 原文、抓取缓存和凭据不放入 Front Matter；Front Matter 只保存可公开审计的来源元数据。

### 5.4 Source 证据边界

- 只有搜索摘要时，不能写入正文接口、参数和性能数字。
- PDF 只读目录时，必须标记 metadata-only。
- 只读取部分正文时，必须记录读取章节和未读取章节。
- 个人 source 可以作为个人经验的证据，但不能自动写成普遍性外部事实。
- 被引用的 snapshot/evidence item 或 source 的证据性质发生变化后，相关 wiki 验证结果失效；只改未被引用的阅读笔记章节不影响其他 target。

### 5.5 Source locator 规范

Source 的章节 locator 只用于阅读和组织，不是证据锚点。权威证据必须绑定不可变 snapshot 和 selector。

```text
<source-id>#<heading-slug>
<source-id>#<heading-slug>@L<start>-L<end>
```

其中 `heading-slug` 由 source 正文的 Markdown 标题稳定生成；`@L...` 是阅读辅助行范围。校验器只确认 source ID 存在，章节标题不存在时给出提示而不阻断——locator 是展示提示，没有 hash 也没有失效轴。章节重命名或正文重排不改变已保存的 snapshot，也不使任何 claim 失效；Wiki 是否仍可验证完全由 evidence item 的 snapshot/selector 决定。

同名标题按出现顺序追加序号消歧：`#限制条件`、`#限制条件-2`。行号是当前 source 版本的辅助定位，不是跨版本稳定 ID；跨版本稳定性由 `snapshot_sha256`、selector 和 normalization 版本共同保证。

Source 中增加 `evidence_items`，每个 item 必须指向一个不可变 snapshot：

```yaml
evidence_items:
  - id: e1
    snapshot_sha256: "sha256:..."
    locator:
      heading_slug: "工作机制"
      selector:
        - type: TextQuoteSelector
          exact: "原文中的完整引文"
          prefix: "引文前文"
          suffix: "引文后文"
        - type: TextPositionSelector
          start: 1204
          end: 1268
          offset_space: unicode-code-point
    selector_sha256: "sha256:..."
    quote_sha256: "sha256:..."
```

`TextQuoteSelector` 和 `TextPositionSelector` 采用 W3C Web Annotation 语义；exact 匹配是 blocking gate，prefix/suffix/position 用于消歧和 UI 恢复。近似匹配只能生成“建议重新锚定”，不得单独使 claim 通过。

`TextPositionSelector.start/end` 使用**规范化 snapshot 文本的 Unicode code-point offset，半开区间 `[start, end)`**，不是 UTF-8 字节偏移、UTF-16 code unit 或压缩文件偏移。生成 selector 前先固定 `normalization_version`；读取、匹配、高亮和 `selector_sha256` 都必须使用同一版本。snapshot hash 计算的是提取后、LF 归一化、未压缩的 canonical text，压缩格式和文件路径不参与 hash：

```text
snapshot_sha256 = sha256(canonical_snapshot_text_utf8)
selector_sha256 = sha256(canonical_yaml(selector + normalization_version + snapshot_sha256))
quote_sha256    = sha256(canonical_quote(exact))
```

`canonical_yaml` 不是依赖 YAML 原始排版的字符串：实现必须先解析数据，再用 UTF-8、递归排序 key、固定数组顺序和无额外空白的 canonical JSON 序列化后计算 hash；禁止 YAML anchor、隐式类型或浮点格式影响 hash。引文校验同时维护 `normalized_text` 到 canonical snapshot code-point 的 offset map：先在 selector 的 canonical `[start, end)` 范围内截取，再对候选和 `exact` 使用同一 `normalization_version` 归一化，并把唯一匹配映射回 canonical 区间。若归一化后出现多个候选或无法映射，必须返回 `ambiguous_selector`/`selector_unresolved`，不能仅凭近似匹配通过。

### 5.6 原文快照归档与来源漂移

**来源必须明确，且必须保存本地快照副本。** 只记录 URL 是不够的：网页会改版、会失效，等到需要复查时原文已经不是当初读的那一份。Source Markdown 是人工阅读记录；snapshot 才是 claim 的事实载体，evidence item 是两者之间的可验证连接。

归档采用内容寻址加压缩存储，同一份资料被多个 source 引用时只存一份：

~~~text
ledger/archive/
├── text/            # 提取后的正文，纯文本，长期保留
│   └── <sha256[:2]>/<sha256>.md.zst
├── raw/             # 原始 HTML/PDF/附件，体积大
│   └── <sha256[:2]>/<sha256>.<ext>[.zst]  # compression=none 时不追加 .zst
└── manifest.jsonl   # append-only logical owner records; blob may be physically deduplicated
~~~

source 通过 `retrieval` 引用归档条目：

| 字段 | 说明 |
| --- | --- |
| acquisition | 获取方式：`fetch`（HTTP 抓取）、`local-file`（读取本地原件或离线 HTML/PDF）、`personal-note`（从 canonical note body 生成 snapshot） |
| fetched_at | 实际读取资料的时间；`local-file` 记录导入/读取时间 |
| http_status | 抓取时的 HTTP 状态码；`local-file` 留空 |
| etag、last_modified | 服务端版本标识，用于后续廉价比对 |
| snapshot_sha256 | 规范化、未压缩正文的 hash，指向 `ledger/archive/text/` 中的不可变副本；这是证据权威 hash |
| raw_sha256 | 原始文件的 hash，指向 `ledger/archive/raw/`；未保留时为空 |
| archive_policy | `text-only`、`text+raw`；`external-only` 仅允许 metadata-only、不能支撑 claim |
| snapshot_url | 第三方快照地址（如 Wayback），作为补充不作为替代 |

归档 manifest 每行是一条 `snapshot-manifest/v1` 记录，至少包含：`snapshot_sha256`、逻辑 owner（`vault_id` + `source_id`）、`archive_path`、`availability`、`extractor_name`、`extractor_version`、`extractor_options_hash`、`normalization_version`、`source_media_type`、canonical byte length、compression format/version 和可选 `raw_sha256`。同 hash 的记录可以共享物理内容，但每个 owner 的逻辑记录、相对归档路径、可用性、保密等级、备份和发布状态不能合并丢失。抽取器或规范化规则升级时生成新 snapshot，不覆盖旧 snapshot；旧 claim 继续绑定旧版本，是否迁移到新版本由人工确认。manifest 是 append-only：修复元数据只能追加 superseding record，不能原地改写已被引用的记录。

本系统把“从本机已有副本导入”的入口统一定义为 `source_type: local-file`；`acquisition: local-file` 记录读取方式。若该副本有原始网页或文档出处，原始 URL 和原始资料类型只能作为 `provenance.original_url` / `provenance.original_type` 保存，不能把本地输入伪装成一次新的网络抓取。网络直接读取的资料才使用 `source_type: blog|doc|book|contest|pr` 与 `acquisition: fetch`。

压缩与体积策略：

- 正文用 zstd（`-19`，文本压缩比通常 4-6 倍）；已压缩格式（PDF、图片、视频）不做二次压缩，按原样存储，并在 manifest 标记 `compression: none`（不强行追加 `.zst`）。
- 归档前先做正文提取（HTML 去导航去广告），**提取后的文本才是证据载体**；原始 HTML 只作为争议时的复核备份。
- 单文件阈值写在 `policy.yaml`：正文超过 `text_max_bytes` 需要先按 5.7 拆分；原始文件超过 `raw_max_bytes`（建议 2 MB）时 `archive_policy` 降为 `text-only`，只保留正文并在 manifest 中记录被跳过的原始文件 hash 和体积。
- `ledger/archive/raw/` 走 git-lfs，且 LFS 规则必须先于归档写入配置好，见 4.3。
- 大体积二进制（视频、数据集、完整代码仓）一律不归档，改用 5.8 的 `local-file` 加可复现定位（repo + commit + 路径 + 行号）。

体积预估：当前 285 个独立外链，按网页正文均值 30 KB 计，`ledger/archive/text/` 压缩后约 2-3 MB；启用 `text+raw` 后原始 HTML 约 15-25 MB 压缩后 5-8 MB。这个量级适合直接进 git。PDF 与书籍扫描件不在此列，必须走 `text-only` 或 `local-file`。

`ledger/archive/raw/` 的 git 归属见 4.3：走 git-lfs，LFS 规则未配置时归档降级为 `text-only`。

归档的三条硬约束：

1. **归档副本不得进入 public build。** 它是第三方内容的本地复制件，用于个人复核，不是可再发布的内容。leak gate 必须扫描 `dist/` 中不出现 `ledger/archive/` 的任何内容（见 13.3）。
2. `confidentiality: internal` 的资料，归档副本只能落在 private vault，且禁止提交到 Wayback 等外部快照服务。
3. 需要鉴权的来源，凭据只从环境变量或本机凭据文件读取，不写入 Front Matter、manifest 和日志；归档文件本身不得包含 Cookie、Authorization 头和会话标识。

抓取约束：只抓取用户明确要求读取的单个 URL，不做站点爬取和批量抓取。

### 5.6.1 离线 HTML/PDF 导入

原链接已经失效、但手上有离线 HTML、PDF 或其他副本时，**统一以 `local-file` 作为 source 入口**。原 URL 只保留为历史出处；本地文件 hash、抽取器版本和不可变 snapshot 才是可复核证据。

~~~text
tools.cli source --from-file <本地副本路径> --url <原始链接> --url-status dead
  -> acquisition: local-file
  -> 正文提取
  -> ledger/archive/text/<sha256>.md.zst
  -> ledger/archive/raw/<sha256>.<ext>.zst（按 LFS policy）
  -> manifest.jsonl 记录 file_sha256、extractor 和 snapshot hash
~~~

对应的 source：

~~~yaml
source_type: local-file
url: "https://blog.example.com/dead-post"     # 历史出处
url_status: dead
local:
  file_sha256: "sha256:..."
  media_type: text/html
  path_ref: "local-sidecar:source-dead-post"
  read_range: "完整文件"
  copy_note: "2019 年浏览器保存的 HTML 副本"
provenance:
  original_url: "https://blog.example.com/dead-post"
  original_type: blog
retrieval:
  acquisition: local-file
  fetched_at: 2026-08-25T10:12:00+08:00
  extractor_name: trafilatura
  extractor_version: "2.2.0"
  extractor_options_hash: "sha256:..."
  normalization_version: canonical-text-v1
  snapshot_sha256: "sha256:..."
  raw_sha256: "sha256:..."
  archive_policy: text+raw
evidence_items:
  - id: e1
    snapshot_sha256: "sha256:..."       # must equal retrieval.snapshot_sha256
    locator:
      selector:
        - type: TextQuoteSelector
          exact: "The output is computed as a weighted sum of the values."
          prefix: "For each query, key, and value tuple, "
          suffix: " The weights are normalized before aggregation."
        - type: TextPositionSelector
          start: 1204
          end: 1262
          offset_space: unicode-code-point
    selector_sha256: "sha256:..."
    quote_sha256: "sha256:..."
~~~

规则：

- `url` 不参与 local-file 可达性检查；`url_status: unknown` 允许保持未知；
- sidecar 中的 `local.path` 和原始文件 `file_sha256` 必须存在；canonical Source 只保存 hash、媒体类型和读取范围，`copy_note` 说明副本来源和获取时间；
- local-file 的文本提取、snapshot 和 evidence selector 必须与 URL 抓取走同一 schema；
- 文件 hash 变化生成新 snapshot，不覆盖旧 snapshot；旧 claim 继续绑定旧版本并等待人工复核；
- URL 后续恢复可达时，来源巡检工具只能追加 fetch 记录，不能把旧 local-file snapshot 替换掉；
- 没有 URL 的本地代码、日志和实验输出也使用同一 `local-file` 入口，只省略历史出处字段。

获取方式的优先级：

~~~text
1. URL 可达          -> source_type: blog|doc|book|contest|pr, acquisition: fetch
2. 已有本地原件      -> source_type: local-file, acquisition: local-file
3. 以上都没有        -> 不允许写入（见 5.9）
~~~

来源巡检工具定期巡检外部链接：

~~~text
unchanged     etag/last_modified/snapshot_sha256 一致
changed       原文已变化，写入新快照版本，标记 source_drift: true
gone          404/410 或域名失效，标记 link_rot: true（本地快照仍可用）
unreachable   网络或鉴权问题，不改变任何标记
~~~

`changed` 时**不覆盖旧快照**：内容寻址天然保留多版本，`retrieval.history[]` 里增加一条历史记录，并保留当前 binding 的 `snapshot_sha256`。这样"我当时读到的是哪一版"永远可回溯。

漂移语义必须与验证失效区分开：source.md 是人工整理的证据记录，外部原文变化不会改变它的 `content_sha256`，因此 **只要 Wiki 仍绑定原 snapshot，不能自动使验证报告失效**，也不自动把页面打回 draft。工具只做三件事：置 `source_drift` / `link_rot` 标记、在本地查询和页面上显示提示、把该 source 及其下游 wiki 列入待复核清单。若人工把 binding 切换到新 snapshot，或旧 snapshot/owner 不再可用，则按 6.6 的 hash 规则使对应 claim 失效。`gone` 时本地快照仍然构成完整证据，已发布内容不受影响。

### 5.7 Source 粒度与拆分

一个 source 对应一个**可独立引用的证据单元**：一篇博客、一份文档的一个章节、一本书的一章、一个 PR、一次实验记录。不是"一个主题的全部资料"。

拆分的第一依据是**抽象层级**，不是字数。同一个对象从概念到实现天然分层：概念上可以很简单，实现组成却很庞大。这两者的证据来源、稳定性和读者不同，必须分开承载：

| 层级 | 承载内容 | 典型稳定性 |
| --- | --- | --- |
| overview | 它是什么、解决什么问题、边界在哪 | 稳定，很少变 |
| mechanism | 工作机制、关键约束、为什么这样设计 | 中等 |
| implementation | 具体实现、参数、调优手段、踩坑 | 易变，随版本漂移 |
| reference | 接口清单、关键字表、枚举、资源索引 | 随上游版本整体替换 |

把四层塞进一个 source，等于把"很少变的概念"和"每个版本都变的参数"绑在同一个 hash 上——改一个参数就波及概念层的全部 claim。分层之后，implementation 层频繁重验，overview 层长期有效。

字数阈值是这个原则的兜底，不是主判据。初始值写在 `config/policy.yaml`，先设一档，运行一段时间后按实际重验频率调整：

~~~yaml
# config/policy.yaml（初始值，可调）
granularity:
  default:
    source_body_warn: 8000
    source_body_block: 16000
    section_warn: 1500
    section_block: 3000
    wiki_claims_warn: 12
    wiki_claims_block: 20
  by_kind:
    reference:            # 参考清单整体替换、整体引用，拆分反而增加维护成本
      source_body_warn: 20000
      source_body_block: null     # null = 只告警不阻断
      section_warn: 3000
      section_block: null
archive:
  text_max_bytes: 2000000
  raw_max_bytes: 2000000
~~~

`by_kind` 覆盖 `default`，`null` 表示该项只告警、不阻断。`kind: reference` 走这条通道：API 清单、关键字表、枚举这类内容随上游版本整体替换，拆成十份只会增加维护面，因此只提示体积、不拒绝写入。其余 kind 仍然按阻断阈值执行。

阻断语义是"这个对象承载了多个证据单元，必须先拆"，不是"内容不能长"。拆分按资料的自然边界进行——按抽象层级、按章、按接口、按实验批次——不按字数机械切割。

拆分后的关系表达：

~~~yaml
id: source-neon-intrinsics-arith
part_of: source-neon-intrinsics-checklist   # 可选，指向拆分前的父资料
~~~

`part_of` 只表达资料归属，不产生证据传递：引用子 source 的 claim 不会自动获得父 source 的支持，父 source 也不因子 source 通过验证而变为已读取。

超过阻断阈值的资料在 preview 阶段就被拒绝，并返回按标题划分的建议拆分清单，而不是先写进来再治理。同一约束适用于迁移：旧文档中的聚合型长文必须先按抽象层级拆成独立单元，再进入 source/wiki 流程。

### 5.8 本地文本来源

**能读到本地原文时，优先建立本地来源，而不是引用一个只能凭记忆概述的网页。** 本地文件在你手上、可重复读取、可用 hash 校验；网页会改版、会失效，只能靠 5.6 的归档快照和漂移检测兜住。

`source_type: local-file` 用于本地代码库、下载的 PDF、离线文档、日志和实验输出：

~~~yaml
---
id: source-llvm-loop-vectorize-pass
title: "LLVM LoopVectorize.cpp 实现"
domain: computer-science
origin: external
source_type: local-file
confidentiality: public
local:
  file_sha256: "sha256:..."
  media_type: text/x-c++src
  path_ref: "local-sidecar:source-llvm-loop-vectorize-pass"
  byte_size: 412355
  read_range: "L1200-L1480"
  resolved_at: 2026-08-25
retrieval:
  acquisition: local-file
  fetched_at: 2026-08-25T10:12:00+08:00
  extractor_name: plain-text
  extractor_version: "1"
  extractor_options_hash: "sha256:..."
  normalization_version: canonical-text-v1
  snapshot_sha256: "sha256:..."
  raw_sha256: null
  archive_policy: text-only
evidence_items:
  - id: e1
    snapshot_sha256: "sha256:..."       # exactly retrieval.snapshot_sha256
    locator:
      heading_slug: "loop-vectorize"
      selector:
        - type: TextQuoteSelector
          exact: "The loop vectorizer widens the loop when the cost model permits it."
          prefix: "In the selected pass, "
          suffix: " The decision is recorded in the analysis remarks."
        - type: TextPositionSelector
          start: 1204
          end: 1273
          offset_space: unicode-code-point
    selector_sha256: "sha256:..."
    quote_sha256: "sha256:..."
read_status: partial
evidence_status: source-reported
---
~~~

字段规则：

- `origin` 仍是 `external`——内容不是你写的；`personal` 只用于你自己产出的记录。
- `url` 对 `local-file` 不必填；sidecar 的 `local.path`、canonical 的 `local.file_sha256` 和 `retrieval.acquisition: local-file` 必填；`snapshot_url` 不适用。
- 原始本地文件默认不进仓库，但提取后的不可变 `ledger/archive/text` snapshot 必须按 Vault policy 保存；大文件 raw 是否保存由 LFS policy 决定。
- 换机器或文件被移动导致 sidecar 无法解析路径时，状态为 `unresolved`，语义与 4.2 的 vault 未挂载一致：不得判定为证据缺失、不得据此降级或改写引用。
- `file_sha256` 变化时，若只是 sidecar 检测到本地原件变更而 canonical Source 仍绑定旧 snapshot，则只标记待复核；若用户将 Source 的当前 binding 更新到新 snapshot，则按 6.6 使对应 claim 失效并重新验证。任何情况下都不得覆盖旧 snapshot。

### 5.9 写入的联网要求与来源完备性

**网络来源写入必须在可联网环境下完成；local-file 和 personal-note 是明确允许离线写入的例外。没有来源的内容一律不允许写入。**

网络 source 的 apply 完成后，证据载体必须已经完整落库；如果允许离线写入网络 source，就会留下"有 URL、没归档正文"的 source。local-file 的证据载体已在本机；personal-note 在 apply 前由 canonical note body 生成 snapshot，因此两者不需要额外联网。

来源完备性检查——每个 source 必须满足三者之一，否则 preview 直接 blocked：

| 来源形态 | 完备条件 |
| --- | --- |
| 网络来源（`acquisition: fetch`） | `url` 可访问、抓取成功、`ledger/archive/text/` 中已存在对应 `snapshot_sha256` 的归档正文 |
| 本地/离线来源（`acquisition: local-file`） | sidecar 中的 path 可解析、`local.file_sha256` 已计算并记录、归档正文和 snapshot manifest 已生成 |
| 个人来源（personal-note） | `origin: personal`、正文非空、生成不可变 snapshot，`evidence_status` 为 personal-observation 或 inferred |

三者皆不满足的写入被拒绝，不存在"来源待补"的中间状态。这一条同样适用于 `metadata-only`：它表示"只拿到了目录或入口页"，而不是"什么都没拿到"——那个目录页本身也必须抓取并归档，否则连"入口存在过"这件事都无法复核。

`policy.yaml` 中的开关：

~~~yaml
write:
  require_network: true          # apply 前必须确认网络与归档可达
  allow_offline_kinds:           # 例外：不需要抓取的来源形态
    - local-file
    - personal-note
~~~

`require_network: true` 时，网络 source 的 `apply` 在获取写锁后、写入 staging 前做一次可达性检查；失败即 operation 转 `blocked`，不写入任何文件。`allow_offline_kinds` 是有意保留的窄例外：这两种形态的证据载体本来就在本机，强制联网不增加保障。把例外做成配置项而不是硬编码，是为了让"为什么这次能离线写"有据可查。

local-file 的历史 URL（如有）其 `url_status` 允许暂时为 `unknown`，联网后由来源巡检工具复核补齐；这不影响证据完备性，因为证据来自本地 snapshot。

离线状态下仍然可用的能力：

| 能力 | 离线可用 |
| --- | --- |
| 建立 local-file / personal source | 可用（按 `allow_offline_kinds`） |
| 建立网络来源 source（`acquisition: fetch`） | **不可用**，preview 可生成候选，apply 被拒绝 |
| wiki 写作、claim 映射、locator 校验 | 可用（前提是引用的 source 已在库） |
| 仅引用已归档 local-file/personal-note 的 wiki apply | 可用；不因全局 `require_network` 误阻断 |
| 需要网络 provider 的 wiki apply/验证 | provider 不可用时保持 `validation_state: not_run`，人工审计仍可推进 |
| 索引生成、FTS5 检索和图谱 | 完全可用 |
| Embedding 与向量召回（本地模型） | 可选增强；不作为第一阶段就绪条件 |
| LLM 语义验证 | 由 Agent Skill runtime 提供合规 provider capability；具体 endpoint、模型版本和密钥读取方式不进入本设计 |

因此当前离线能力聚焦于查询、阅读和图谱；题库与复习在 F008 设计完成后再接入。

### 5.10 音视频与转录来源

音视频没有天然的可引用单元，只有时间轴；且原始媒体通常不可归档。因此它的 source 模型一拆为三：原始媒体（`song`/`broadcast`/`speech`）、转录稿（派生实体）、引文（在转录稿上锚定）。

`source_type` 的取值对齐 CSL / Zotero item type 的子集，只新增不重命名：既有的 `blog`、`doc`、`book`、`contest`、`pr`、`local-file`、`personal-note` 全部保留，新增 `podcast`、`video`、`talk`、`paper`、`spec`、`software`、`dataset`。**不允许重命名既有取值**：`source_type` 位于 `hash_inputs.source_semantic`，重命名会改变全部既有 source 的 semantic hash 并触发全库重验。CSL 对齐通过映射表表达，不通过改名表达。

时间锚点使用 W3C Media Fragments URI 语法，作为 `evidence_items.locator` 的可选字段，与 `heading_slug` 并列：

~~~yaml
evidence_items:
  - id: e1
    snapshot_sha256: "sha256:..."     # 转录稿的 canonical text hash
    locator:
      media_fragment: "#t=1450,1520"  # 秒；仅用于定位与展示
      heading_slug: null
      selector:
        - type: TextQuoteSelector
          exact: "转录稿中的完整引文"
~~~

`media_fragment` 与 §5.5 的章节 locator 同性质：只用于阅读定位，没有 hash 也没有失效轴。逐字校验仍然发生在 selector 与 snapshot 之间。

**转录稿是 lossy 派生物，这决定了它的证据强度上限。** 逐字 exact 匹配成功只证明"匹配了转录稿"，不证明说话人说过这句话。因此 ASR 产生的 snapshot 必须在 `snapshot-manifest/v1` 中记录 `extractor_name`、`extractor_version` 和 `extractor_options_hash`（现有字段已足够表达，无需扩展 schema），并且由它支撑的 claim 强度上限为 `attested`，不得派生为 `verified`；只有人工逐字校对该片段并标注后才解除上限。平台自带的人工字幕属于准原文，不受此上限约束；自动字幕按 ASR 处理。

口头来源的分级落在 claim 级而非来源级：同一集播客里，作者亲述设计意图对「意图」类断言是直接证据，而凭记忆给出的性能数字必须降级。因此固定规则是——**任何数字类断言若仅由口头来源支撑，一律按 `inferred` 处理并写明待验证动作**，须由文档或本人实测升级。

`archive_policies` 新增 `transcript-only`：只归档转录稿与元数据，不归档媒体原件。它避免了在「把几十 MB 音频纳入 git-lfs」与「`external-only` 导致没有可复核快照」之间二选一。此档下转录稿是主快照，不是补充快照。

## 6. Wiki 严格规范

### 6.1 Wiki Front Matter

~~~yaml
---
id: wiki-transformer
title: "Transformer"
domain: computer-science
kind: knowledge
status: draft
publication_scope: none       # requested projection; publish operation is separate
confidentiality: public
tags: [transformer]
aliases: [Transformer 模型]
sources:
  - source-transformer-paper
related: []
evidence:
  - claim_id: c1
    claim: "Attention 使用 Q、K 的相关性计算权重，再对 V 加权求和。"
    targets:
      - source_id: source-transformer-paper
        evidence_id: e1
    support: direct
    supporting_quotes:
      - evidence_id: e1
        # This is a verbatim substring of the immutable snapshot selected by
        # source-transformer-paper/e1, not a restatement of the claim above.
        exact: "The output is computed as a weighted sum of the values."
updated_at: 2026-08-25
review_by: 2027-08-25         # optional; report-only, see 6.2
---
~~~

上面是作者可编辑的 canonical 输入。`vault_id`、`evidence_state`、`validation_state`、`effective_confidentiality`、`strength`、`public_publishable`、`private_publishable`、`public_confirmation_sha256` 和 `public_release` 不属于作者输入；它们由 Vault Registry、确定性 validator、durable attestation 和 publish operation 计算。为了便于说明，工具生成的运行视图可能包含：

~~~yaml
vault_id: public
evidence_state: supported
validation_state: not_run
effective_confidentiality: public
strength: verified
public_publishable: false
private_publishable: false
public_release: false
~~~

`supporting_quotes.exact` 必须逐字来自 `source-transformer-paper/e1` 所绑定的 snapshot selector 范围；示例中的英文句子只是与 snapshot fixture 配套的原文片段，实际写入时由工具从归档 snapshot 生成并由人工确认，不能把 claim 的中文转述复制进去冒充证据。

### 6.1.1 Wiki 字段级契约

Wiki Front Matter 的 canonical schema version 是 `content/wiki/v1`，在 `config/schemas.yaml` 的 `objects` 注册表中登记。下表是字段级约束。

| 字段 | 必填 | 约束 |
| --- | --- | --- |
| id、title、domain、kind、status | 是 | `kind` 为 `knowledge`、`index`、`reference`；`status` 为 `planned`、`draft`、`review`、`published`、`deprecated` |
| vault_id | 生成 | 由 Vault Registry 注入实际 owner；写入请求必须明确目标 vault，作者不能手写或改写 |
| evidence_state、validation_state | 生成 | 分别表示证据覆盖/一致性和 LLM 规范审计运行结果；作者不能手写派生值 |
| publication_scope | 是 | `none`、`private` 或 `public`，表示请求的投影；实际发布仍需 publish operation 和确认事件 |
| confidentiality | 是 | `public` 或 `internal`，缺省 `public`；必须与 `vault_id` 等级一致，有效等级按 4.2 从上游 source 传染，声明低于上游即校验失败 |
| tags、aliases、related | 是 | 始终为数组；ID 必须能解析到对应对象 |
| sources | knowledge 必填 | 至少一个已存在 source ID，不能只引用 metadata-only source；index/reference/planned 见 6.7 |
| evidence | knowledge 必填 | 每个核心 claim 一条唯一 `claim_id`，每条至少一个 `target(source_id, evidence_id)` |
| updated_at | 是 | ISO 8601 日期或时间 |
| supporting_quotes | 每个 claim 的 target 必填 | 原文引文，由工具在 target 指向的 snapshot 范围内逐字校验，见 6.7 和 6.9 |
| content_sha256 | 生成 | 按 6.6 规范化正文计算 |
| evidence_sha256 | 生成 | 按 6.6 规范化 evidence 块计算；claim 文本、targets、selectors、supporting_quotes 或 support 变化即失效 |

作者文件中的 `source_id`/`evidence_id` 是 owner Vault 上下文内的短引用，便于移动和阅读；validator 在解析后必须为每个 target 生成不可变的 `resolved_object_ref: {vault_id, object_type: source, object_id}`，并把它写入 evidence binding、hash 和报告。任何 adapter 不得仅凭裸 `source_id` 或裸 `snapshot_sha256` 读取内容。

`published` 不是作者自由填写的状态。作者只能创建 `planned`/`draft`/`review` 候选；进入 `published` 需要确定性校验全部通过、LLM 规范审计不为 `fail`，以及绑定当前 `(content_sha256, evidence_sha256)` 的人工审计确认事件。

### 6.2 Wiki 状态机

~~~text
planned -> draft -> review -> published
              ^       |
              |       +-- 确定性校验失败、LLM 审计 fail
              |       +-- evidence_state: partial/conflicting/unresolved
              |       +-- 内容 hash 变化使人工审计确认失效
              +-------+

published --public_release:false--> human sets true -> public projection
                                      |
                                      +-> hash changed -> false

任意状态 -> deprecated（人工判定内容错误或过时）
deprecated -> draft（修订后重新进入流程）
~~~

- planned：只有标题和意图，没有正文和 source。用于"知道要写但还没写"的条目，不进索引正文、不进 public build，只出现在待写清单和查询结果的 `pending` 字段。
- draft：可以编辑、预览和查询，但不进入 public build。
- review：结构、selector、claim 与冲突检查的结果待人工判断，或需要人工判断来源质量、多个 source 的冲突、版本差异和推断边界。确定性校验通过但尚未获得人工审计确认的页面停在这里。
- published：用户确认发布；`publication_scope: private` 可进入 private projection，`publication_scope: public` 才可进入 public projection。
- deprecated：内容已被判定为错误或过时。保留文件和路由以免死链，但不进 public build、不作为 RAG 召回来源、不能被新的 claim 引用；F008 若启用，关联题目按其独立规则处理。

`planned` 与 `deprecated` 都只能由人工显式设置，工具不自动推断。任何 source、snapshot 或 wiki 内容变化后，页面自动标记验证过期；若存在证据冲突则进入 `review`，不能继续沿用旧报告。

Wiki 的“状态可能很多”不通过无限扩张单一 enum 实现，而通过多个派生轴表达：

| 轴 | 值 | 含义 |
| --- | --- | --- |
| `status` | planned/draft/review/published/deprecated | 生命周期和人工决策 |
| `evidence_state` | missing/partial/supported/corroborated/conflicting/unresolved/stale | source 是否存在、是否一致、是否可定位 |
| `validation_state` | not_run/pass/fail/stale_ruleset | LLM 规范审计的运行结果；确定性校验结果不进这一轴 |
| `availability` | available/unavailable/conflict/invalid | 当前 Vault/object/snapshot 是否可读取；不是证据质量判断 |
| `publication_scope` | none/private/public | 作者请求的投影；实际是否进入由 publishability 派生字段决定 |
| `public_release` | false/true | public release materialized field；默认 false，只有人类为当前 hash 创建 durable confirmation 后才能由 projection 派生为 true |

查询、前端和 Agent 显示组合状态，例如 `status: review + evidence_state: conflicting`、`status: draft + evidence_state: partial`、`status: draft + availability: unavailable`、`status: published + validation_state: not_run`、`status: published + publication_warning: internal`。`corroborated` 只表示多个独立 source 一致支持；它不是事实正确性的数学证明，仍需冲突检查和人工审计。`availability: unavailable` 只表示当前读取条件不足，不得写入 `evidence_state` 作为"证据缺失"的同义词，也不得写入 `validation_state`。`validation_state: not_run` 不得被渲染为"已验证"。

`planned` 条目只需要 `id`、`title`、`domain`、`kind`、`status` 五个字段，不要求 sources 和 evidence——它还不是知识，只是一条待办。批量导入的标题清单（例如一份没有答案的问题列表）应该进 `planned`，而不是生成一批空壳 draft 页面。

`review_by` 是**时间维度的复审提示，不是第七个状态轴**。`evidence_state: stale` 只覆盖"source 或 snapshot 变了"这一类失效，无法表达"source 没变但世界变了"（例如文档描述的是旧版本行为）。因此 `review_by` 是可选的作者声明字段，语义受三条约束：

- 它位于 `hash_inputs.excluded_from_content_hash`，与 `status`、`updated_at` 同列。续期不改变 `content_sha256` 与 `evidence_sha256`，因此**不作废已绑定当前 hash 的人工审计确认**。若续期会作废确认，这个字段的使用成本将高到无人使用。
- 到期**不改变任何 `*_state` 字段、不改变 `status`**，只出现在 `doctor` 的到期清单里。状态轴已有六个，第七件事应该是报告项而不是状态。
- 它是选填。只有作者判断"这页会随版本过时"时才填；方法论类内容通常不需要。


### 6.3 Wiki 必填正文

~~~markdown
# 知识主题

## 一句话结论

## 核心概念

## 工作机制

## 示例或代码

## 常见误区

## 证据映射

## 待验证项

## 关联知识
~~~

### 6.4 Claim 和 Evidence

每个核心论断必须有显式证据映射：

~~~yaml
evidence:
  - claim_id: c1
    claim: "一个来源明确支持的事实。"
    targets:
      - source_id: source-a
        evidence_id: e1
    support: direct
    supporting_quotes:
      - evidence_id: e1
        exact: "原文中的完整引文"

  - claim_id: c2
    claim: "综合两个来源得到的结论。"
    targets:
      - source_id: source-a
        evidence_id: e2
      - source_id: source-b
        evidence_id: e3
    support: synthesis
    supporting_quotes:
      - evidence_id: e2
        exact: "来源 A 的引文"
      - evidence_id: e3
        exact: "来源 B 的引文"

  - claim_id: c3
    claim: "根据实验日志推断出的待验证方向。"
    targets:
      - source_id: source-personal
        evidence_id: e4
    support: inferred
    supporting_quotes:
      - evidence_id: e4
        exact: "实验观察的引文"
~~~

支持类型：

| 类型 | 规则 |
| --- | --- |
| direct | 至少一个 external source 的 evidence item 明确表达；多个独立 source 一致时标记 `corroborated` |
| synthesis | 必须由两个或多个 source 的 evidence item 共同支持，且不能存在未解释的矛盾 |
| inferred | 必须写出观察事实、推理过程和下一步验证动作 |
| personal | 只能引用 origin: personal 的 source |

F010 迁移澄清（2026-08-28）：检索确认无外部出处的**本人综合**按 personal 建模——
以 `personal-note` source（本人笔记快照）作为 provenance，claim 用
`support: personal` 引用其 evidence item。此时 `evidence_state` 表达映射完整性
（引文定位成功即为 supported），信任降级由 `strength: personal` 承载（§6.8
"全 personal 支撑 → personal"）；personal strength 不进入证据阻断集合，
published 路径不被证据门禁挡住，但不得伪装外部普遍事实（上表个人 source
规则不变）。端到端证据：`tests/validation/test_synthesis_claims.py`。

以下情况一律阻断 published：

- sources 为空；
- source ID 不存在；
- evidence item、snapshot 或 selector 不存在/无法解析；
- claim 引用的 source 是 metadata-only；
- 核心论断没有 claim_id；
- claim 没有 `targets`，或 target 没有同时解析到 source、evidence item、snapshot 和 selector；
- 个人 source 被用来支撑外部普遍事实；
- LLM 返回 unsupported、contradicted 或 unmapped。

Source 不是可信事实的自动证明。验证器必须对同一 claim 的所有 target 做一致性分析：

- `corroborated`：多个独立 source 对同一命题和适用范围一致支持；提高证据强度，但仍保留来源质量告警；
- `conflicting`：source 对数值、版本、前提或结论存在冲突，Wiki 设置 `status: review`；
- `partial`：source 只覆盖 claim 的一部分，Wiki 不能进入 `published`；
- `unresolved`：selector 能定位但无法判断 claim 范围，必须由人工补充边界或改写 claim。

`corroborated` 只在至少两个不同 `independence_group` 的 source 对同一命题、适用范围和版本窗口一致支持时派生。相同 publisher 的转载、互相声明 `derived_from` 的文章、同一实验数据的不同摘要默认属于同一组，不能通过数量制造"独立佐证"。无法确定独立性时按单一 source 处理，并在报告中告警。

独立性判定由 LLM 规范审计执行——逐对核对转载链是人工在规模上做不到的事。但它的举证义务更严：每条独立性结论必须回引 source 的 `provenance` 字段（`publisher`、`derived_from`、`independence_group`）或引文原文中的转载声明，并给出字符区间。**禁止以域名、站点名、URL 相似度、发布时间先后或"看起来像原创"作为独立性依据**：同一机构可有多个域名，转载站也可有独立域名，域名与独立性没有可靠映射。无法从 `provenance` 或原文举证时必须输出 `independence_unknown`，按单一 source 处理，不得猜测。

冲突不能用“多数 source 票数”自动消解。验证报告必须列出冲突 target、`independence_group`、版本/时间范围、冲突字段和建议的人工决策；即使已有两个 source 一致，也不能自动压过第三个冲突 source。

### 6.5 来源类型与论断语气矩阵

确定性校验和 LLM 验证共同执行下面的兼容矩阵：

| source origin | 允许的 support | 正文语气要求 |
| --- | --- | --- |
| external / source-reported | direct、synthesis | 可以陈述来源明确的外部事实，但不得超出 locator |
| external / common-knowledge | direct、synthesis | 可以陈述为公认事实，但必须落在权威入口覆盖的范围内，不得延伸到具体实现细节和性能数字 |
| external / 任意 | inferred | 必须明确写出“推断”、依据和待验证动作 |
| personal | personal、inferred | 必须使用“我的记录/本次实验/个人观察”等语气 |
| personal | direct、synthesis | 禁止将个人记录包装成外部普遍事实 |
| personal + common-knowledge | 无 | 非法组合，公认事实不能以个人来源承载 |

`common-knowledge` 的适用范围是"查一下就能确认、且不会因版本而变"的事实：语言关键字语义、标准库接口约定、公开协议字段、数学定义。**不适用**于版本相关行为、编译器实现细节、性能数据和最佳实践——这些必须走正常的 evidence target 加验证路径。判断依据是"权威入口是否直接写了这句话"，不是"我觉得这是常识"。

`common-knowledge` 必须有明确来源：`url` 必填、`read_status` 必须是 `retrieved`、必须有 `ledger/archive/text/` 中的归档正文。这条约束是为了消除滥用动机——如果标记它比正常引用更省事，48 篇找不回出处的旧文都会涌向这一类。要求"确实打开过并归档"之后，它的成本与正常引用相当。

`common-knowledge` 不是"不做语义检查"，而是**把语义检查从模型判断换成确定性匹配**。每条 claim 的 evidence 必须人工填写 `supporting_quotes`，并指向已解析的 evidence item：

~~~yaml
evidence:
  - claim_id: c1
    claim: "constexpr 变量必须在编译期完成初始化。"
    targets:
      - source_id: source-cppref-constexpr
        evidence_id: e-constexpr-1
    support: direct
    supporting_quotes:
      - evidence_id: e-constexpr-1
        exact: "constexpr 变量必须立即被初始化，且其初始化必须是常量表达式。"
~~~

工具按 6.9 的规范化规则，在 evidence item 指向的 snapshot 范围内逐字查找每条 supporting quote，找不到即校验失败、页面保持 `draft`。所有普通 claim 也必须经过同一确定性 quote/selector 检查。这样 `attested` 页面的检查强度和 `verified` 相当，而不是仅仅确认"有链接、有归档"。

引文与 claim 表述不同不构成失败：`claim` 是你的转述，`supporting_quotes.exact` 是原文。确定性校验只检查引文的存在性，不判断转述是否忠实——后者是 LLM 规范审计的职责；跳过它时页面只能是 `attested` 而不是 `verified`。因此 `common-knowledge` 的适用范围必须严格限制在"转述空间很小"的事实上（见下）。

当一个 claim 同时引用 external 和 personal source 时，若结论是普遍事实，至少需要 external source 作为直接或综合证据；personal source 只能作为补充经验。若没有 external source，claim 必须降级为 personal 或 inferred。

`metadata-only` source 可以作为资料目录中的待读取入口保留，但不能出现在任何已验证核心 claim 的 `targets` 中；如果一个 wiki 没有其他可用证据，或者它的核心 claim 只能落到 metadata-only source，页面必须保持 `draft`。

口头、私聊、内部会议和电话沟通类材料**不建立独立 source 类型**：`source_types` 中不存在 `personal-communication`，且不得新增。这类材料若必须使用，只能作为 `personal-note` 承载，`support` 只能是 `personal`，并且不得作为任何普遍事实型 claim 的唯一支撑。理由是它不可被他人复核、没有版本、也没有可归档的原文快照，纳入独立类型只会制造一条绕过 §5.9 来源完备性的通道。

### 6.6 内容 hash 契约与失效粒度

本节适用于 source、wiki；Question 的 hash 规则留给后续 F008，不属于当前交付。

### 6.6.1 逻辑 ID 与 hash 的职责边界

`id` 表示可被链接、引用和审计追踪的逻辑对象，创建后保持稳定；`content_sha256` 表示该对象当前内容版本；`snapshot_sha256` 表示不可变证据快照；`evidence_sha256`/`selector_sha256` 表示证据绑定版本。Source 和 Wiki 不使用正文 hash 作为主 ID，因为一次正文修改不应让所有下游引用和路由失效为“指向不存在的对象”。Question 的 ID/hash 规则留给 F008。

ID 生成规则：用户显式提供的合法 kebab-case ID 优先；需要自动生成时，工具从规范化标题/相对路径生成候选 slug，并在 preview 中报告**同一 Vault、同一 object type**内的冲突。迁移器使用 `slug + stable collision suffix`（由输入路径 hash 的短前缀产生），同一输入重复运行必须得到相同 ID；不同 Vault 的同名对象不冲突，引用解析仍以 owner `vault_id` 为上下文。ID 一旦 Apply 不再自动改名，改名只能走 rename operation 并同步 route、引用和审计记录。

内容寻址只用于不可变数据和去重：snapshot 可以直接用 `snapshot_sha256` 定位，selector/evidence binding 使用对应 hash；逻辑对象修改时保留原 `id`、生成新 hash，并让依赖该 hash 的验证报告或题目进入失效状态。若未来需要 hash 型展示 ID，只能作为只读别名，不能替代逻辑 `id`。

**hash 只覆盖正文和语义字段。** 分类字段变化不使任何验证报告失效——新增一个标签、补一个别名、调整 related 都不应该触发重新验证和重新花费 LLM 调用。发布/运行态字段也不能被混入内容 hash。

~~~text
content_sha256   = sha256(canonical_body)
evidence_sha256  = sha256(canonical_json(evidence))          # 仅 wiki
~~~

`canonical_body` 的规范化规则：剥离 Front Matter，只取正文；统一为 LF；去掉行尾空白；折叠文件末尾空行为单个换行；不做其他改写（不动大小写、不动标点、不重排列表）。

只保留这两个内容 hash。source 的 `read_status`、`evidence_status`、`origin`、`confidentiality` 属于**声明字段**，每次 `validate_pages` 都能确定性重查，用不着单独的 `semantic_sha256` 来绑定失效——多一个 hash 只是多一处需要同步的状态。章节 locator 是阅读导航，不是证据锚点，因此也没有 `locator_sha256`：它没有失效轴，改了章节标题不该让任何 claim 失效。

字段分类：

| 类别 | 字段 | 变化是否触发失效 |
| --- | --- | --- |
| 语义内容 | 正文、`evidence`（claim 文本 / targets / selectors / supporting_quotes / support）、evidence item、当前绑定的 `retrieval.snapshot_sha256` | 是 |
| 声明字段（每次重查，不入 hash） | source 的 `read_status`、`evidence_status`、`origin`、`confidentiality` | 是（由重查判定，不靠 hash 绑定） |
| 分类与导航 | `tags`、`aliases`、`related`、`domain`、`title`、章节 heading slug | 否 |
| 派生/运行字段 | `status`、`updated_at`、`content_sha256`、`evidence_sha256`、`validation_state`、`public_release` | 否，且不参与自身 hash 计算 |

`evidence` 在 Front Matter 中，但它是语义内容，必须单独 hash。只 hash 正文会留下一个绕过门禁的口子：改掉 claim 文本、target 或 selector 之后，旧的通过报告仍然"有效"。`content_sha256`、`evidence_sha256` 和被引用的 snapshot/selector/quote hash 必须同时绑定到人工审计确认。canonical JSON 采用 UTF-8、递归排序 key、固定数组顺序和无额外空白。

派生字段不参与自身 hash，因此不存在"改内容 → hash 变 → status 回退 → 写 status 又改文件 → hash 再变"的不动点问题：写 `status` 和 `content_sha256` 不会改变 `content_sha256`。

**失效粒度按 evidence item/snapshot，而不是按整个 source 文件。** 修改 source 中未被引用的章节，不影响引用其他章节的 wiki：

| 变更 | 失效范围 |
| --- | --- |
| source 阅读笔记章节变化 | 不失效；章节只是阅读导航，权威锚点是 snapshot + selector |
| 被引用 snapshot 或 evidence selector 变化 | 命中该 evidence item 的 claim 失效 |
| source 新增或重命名章节 | 不失效 |
| source 的 tags/title 变化 | 不失效 |
| source 的 `read_status`、`evidence_status`、`origin`、`confidentiality` 变化 | 引用它的全部 claim 失效（证据性质改变）；由每次重查判定 |
| wiki 正文变化 | 该 wiki 的人工审计确认失效 |
| wiki 某条 claim 变化 | 该 wiki 的确认失效（第一阶段按整篇重审，不做 claim 级增量） |
| wiki 的 tags/aliases/related 变化 | 不失效 |
| 外部原文变化（source_drift），但旧 snapshot 仍存在且 Wiki 仍绑定旧 snapshot | 不失效，仅进入待复核清单，见 5.6 |
| source 将当前 evidence binding 切换到新 snapshot，或旧 snapshot/manifest owner 不可用 | 命中该 binding 的 claim 失效并标记 `stale`/`unavailable` |

claim 级增量重验放在后续阶段：报告结构已按 claim 存储，具备增量能力，但第一阶段先用整篇重验换取实现简单和判定确定。

### 6.7 证据要求分档

不是所有页面都能套用"每条核心论断都要有外部 evidence item"。强行套用会产出大量无意义的仪式性证据（把官方 API 手册抄成 claim，再让模型判断抄得对不对）。但分档必须遵守一条原则：

> **可以免除 content/sources/claim 级 evidence 的要求，不能免除确定性校验。** 每一档都必须有替代性的确定性检查，并且在页面上对读者可见。

| 页面类型 | 判定条件 | 免除什么 | 替代检查 |
| --- | --- | --- | --- |
| `kind: index` 导航页 | 正文主要是链接与分类 | sources、evidence | 全部链接必须可解析到库内对象；不得含正文结论 |
| `kind: reference` 参考清单 | API 清单、关键字表、枚举、资源索引 | claim 级 evidence | 必须有 metadata-only 以上的 source；每个条目必须有可查证入口；不得出现推断性表述 |
| `evidence_status: common-knowledge` | 语言标准、公开规范、教科书级公认事实 | 无 | source 必须有 `url`、`read_status: retrieved` 和归档 snapshot；每个 target 必须有 `supporting_quotes.exact`，由工具在 evidence item 指向的 snapshot 中逐字校验 |
| `origin: personal` 自撰内容 | 论断来自本人理解、观察或实验 | 外部 source 支持 | 必须使用个人语气；不得表述为外部普遍事实；support 只能是 `personal` 或 `inferred` |
| `status: planned` 待写条目 | 无正文 | sources、evidence、正文模板 | 只允许五个字段；不进索引正文与 public build |
| `status: deprecated` 废弃内容 | 人工判定错误或过时 | 无 | 不进 public build、不进 RAG 召回、不可被新 claim 引用 |
| `kind: knowledge` 的常规页面 | 以上都不适用 | 不免除 | 完整走 source → snapshot/evidence item → claim → 冲突检查 |

页面必须显示自己的证据强度，读者不需要读 Front Matter 就能知道这页是"外部来源验证过的事实"还是"我的个人理解"：

~~~text
verified      确定性引文校验通过、LLM 规范审计为 pass，且论断由 ≥2 个独立 source 支撑
corroborated  多个独立 source 一致支持，但仍显示来源范围和告警
conflicted    source 之间存在未解决冲突，不可发布
attested      确定性引文校验通过但只有单一 source 支撑（含 LLM 审计已 pass 的情形），
              或 common-knowledge 有权威入口且引文逐字匹配、未做 LLM 语义审计
personal      个人理解或实验记录
reference     参考清单，只保证条目入口可查
index         导航页，不含论断
~~~

`verified` 只授予"多来源交叉可证"的论断：LLM 审计 pass 只证明转述忠实于所引原文，不证明原文本身正确，因此单一 source 的页面上限是 `attested`。这条边界让 `verified` 保持"外部世界交叉验证过"的含义，而不是退化成"模型说 OK"。

这个标识由工具从 `kind`、`evidence_state`、`evidence_status`、`origin`、`validation_state` 和验证报告计算，不由作者填写，并且必须同时出现在页面、查询结果和 Agent 输出契约中。多个 source 的一致性可以提升为 `corroborated`，但不改变"来源可能错误"的基本假设。

`common-knowledge` 与 `personal` 的边界必须人工判断，不允许工具自动降级：判不准时按 `personal` 处理（更保守的一侧）。

LLM 规范审计是可选层，因此本节不存在"免 LLM"这一档，也不存在独立的 `verdict: exempt` 报告结构或"豁免类型变化必须重判"规则——所有页面走同一条门禁（确定性校验必过 + LLM 审计不为 `fail` + 人工审计确认）。`kind: index`、`kind: reference`、`status: planned`、`status: deprecated` 通常 `validation_state` 保持 `not_run`，发布仍需人工审计确认。

### 6.8 声明字段、派生字段与合法组合

字段分成三组，边界必须清楚：声明字段由人写，派生字段由工具算，operation-controlled 字段只能由对应受控操作写入。作者写错声明字段会被拒绝；作者手写派生字段或直接修改 operation-controlled 字段一律拒绝。

声明字段（人工）：（作者只能直接创建 `planned`/`draft`/`review` 候选；`published` 由 publish operation 在人工审计确认后写入，不接受裸字段跳转。）

~~~text
kind                knowledge | index | reference
status              planned | draft | review | published | deprecated
confidentiality     public | internal
publication_scope   none | private | public       （期望进入的投影；发布操作仍需显式确认）
origin              external | personal            （source）
evidence_status     source-reported | common-knowledge | personal-observation | inferred | metadata-only（source）
support             direct | synthesis | inferred | personal（claim）
~~~

派生字段（工具计算，不入 hash）：

~~~text
effective_confidentiality   max(自身, 全部上游对象)
evidence_state              missing | partial | supported | corroborated | conflicting | unresolved | stale
validation_state            not_run | pass | fail | stale_ruleset
strength                    verified | corroborated | attested | personal | conflicted | partial | unresolved | reference | index
private_publishable         true | false
public_publishable          true | false
publication_warning         none | internal
~~~

operation-controlled 输入字段（只能由对应受控操作写入）：

~~~text
public_release_confirmation_ref  event_id + operation_id（只由人工 public-release confirm 产生）
public_release              false | true   （默认 false；projection 根据 durable record 派生，不接受 Front Matter/manifest 直接写入）
~~~

以下字段是投影/运行时派生值，不能写回 canonical Source/Wiki Front Matter：
`effective_confidentiality`、`availability`、`availability_reason`、`strength`、`private_publishable`、`public_publishable`、`public_release`、`publication_warning`、`validation_attestation_ref` 和 `public_confirmation_sha256`。它们由 Registry、validator 和 projection generator 根据 canonical 内容、durable record 与当前 Vault 状态重新计算；如果旧生成物中的值与当前计算结果不同，旧值必须被丢弃并报告 `derived_field_mismatch`。`public_release` 只有在 public-safe confirmation event、public owner operation record、当前 release/content/evidence/input-leak hash、人工 actor、未消费 nonce 和完整 audit chain 全部匹配时才派生为 true；hash 变化后旧事件保留但派生值回到 false。

发布确认与验证的 durable record 位置固定为：

~~~text
<owner-vault>/audit/operations/<operation_id>.json
<owner-vault>/audit/validation/<object_type>/<object_id>/<attestation_sha256>.json
public/release/public-confirmations/<event_id>.json
~~~

`var/state/` 中的完整 provider 响应、锁和临时 staging 只能作为运行缓存，不能证明审计、人工确认或恢复能力。每个 durable record 都必须包含 canonical schema version、owner `vault_id`、target ObjectRef、相关 hash、生成工具版本和 `record_sha256`；写入采用 append-only，新状态用新 record 表示，不原地修改已被引用的审计记录。审计侧的 durable record 类型是 `audit-record/v1`。确认事件只有两个版本化类型：`operation-confirmation/v1`（用 `scope: apply | publish_private` 区分普通 apply 与私有发布；有效保密等级为 internal 时还必须携带 `warning_code` 和 `warning_text_sha256`）和 `public-release-confirmation/v1`。**public release 故意不做成一个 scope 值**：它是唯一不可撤销的对外行为，独立类型使"写错一个 scope 就公开了 internal 内容"在 schema 层不可表达。`event_sha256` 定义为去掉自身字段后的 canonical JSON UTF-8 hash；public-safe event 不能包含 private ID、路径、正文或裸 private hash。一次性 `confirmation_nonce` 只用于 public release：apply 与私有发布的重放已由 hash 绑定挡住（输入一变事件就不再匹配）。public release 的目标 operation record 固定在 public owner 的 `ledger/audit/operations/<operation_id>.json`；若存在 private lineage，源 owner 的同 operation/audit record 只作为私有审计，不进入 public event。

Durable record 的防篡改由 Git 提供，不自建 hash chain。每条记录仍带 `record_sha256`（按去掉自身字段后的 canonical JSON 计算）用于校验单条记录的自完整性，但记录之间不再串 `sequence` / `previous_record_sha256` / `chain_scope`——Git commit 本身就是一条哈希链：每个 commit 摘要覆盖树内容并指向父 commit，篡改历史任一点都会改变后续所有摘要。在 canonical 文件之上再叠一条自建链，是用弱得多的实现（无签名、无分布式见证、与 Git 历史可能不一致）重复一个已经成立的保证。

因此顺序与篡改证据来自 `git log`；加载、备份和恢复只需校验单条 `record_sha256` 与 target owner 一致。并发追加由目标 Vault 锁串行化；锁恢复本身追加 `record_type: lock-recovery` 记录。

声明字段中的 `publication_scope` 只表示作者请求的投影，不等于已经发布。首次写入时的 `target_vault` 决定对象 owner；它不写入 Wiki Front Matter，只写入 operation record，并由 writer 生成 `vault_id`。`publish_private` 的 `target_vault` 必须等于 owner；目标 Vault 不可用、记录缺失或 hash 不匹配时为 false。若用户要把内容迁移到另一个 Vault，必须走显式 copy/move operation，生成新的 owner 对象和完整 lineage，不得让旧对象跨 Vault 引用。实际发布必须由 operation 记录 `operation-confirmation/v1` 且 `scope: publish_private`；internal 内容的同一事件还必须携带 `warning_code` 和 `warning_text_sha256`，证明告警被展示并确认。工具不得接受作者手写派生字段或直接写 `public_release`，旧版本的 `publishable` 字段只作为兼容读取字段，写回时拆分为 `private_publishable` 和 `public_publishable`。

人工审核不引入复杂的 review 状态机：`public_release` 仍默认为 `false`，唯一允许产生可派生 true 的入口是一次明确的人类确认事件（推荐交互式 `public-release confirm --operation-id ...`，桌面 UI 或人工提交也必须由 writer 校验并记录）。Skill/Agent 只能生成 preview 和展示材料，不能代替该事件。事件至少包含：

```yaml
event_type: public-release-confirmation/v1
event_id: evt_...
operation_id: op_...
target_ref: {vault_id: public, object_type: wiki, object_id: wiki-example}
actor_type: human
actor_id: local-opaque-id
confirmed_at: 2026-08-26T12:00:00+08:00
release_input_sha256: sha256:...
reviewed_content_sha256: sha256:...
reviewed_evidence_sha256: sha256:...
diff_sha256: sha256:...
leak_gate_report_sha256: sha256:...
leak_gate_report_scope: input-item
decision: approve
reason: "人工确认当前输出可公开"
confirmation_nonce: nonce-from-preview
event_sha256: sha256:...
```

`release_input_sha256` 覆盖 public copy 的正文、allowlisted attachments 的相对路径与 hash、允许公开的 metadata、Wiki-to-Wiki links、route、`public_lineage_commitment` 以及 policy/schema 版本；它不是单独的 `content_sha256`。`leak_gate_report_sha256` 在这一事件中只表示输入边界扫描摘要；最终 dist 扫描在确认之后执行，结果写入本次 `build-manifest.json`，不反向修改人工事件。`public_confirmation_sha256` 只是 projection 对当前 public-safe event `event_sha256` 的命名引用，不是第二个独立 hash。writer 在 Apply 前重新计算这些 hash，任一变化就把 `public_release` 视为 false 并使事件失效；只有 `actor_type: human`、安全 pseudonym 格式的 `actor_id`、无 URL/路径/private lineage 的短 `reason`、当前 hash 完全匹配且 `decision: approve` 的事件才可生成 public projection。若事件携带 `target_vault`，其值必须是 `public`。一次性 nonce 的消费结果必须写入 durable operation record。

`actor_type: human`、CLI/UI 入口和一次性 nonce 是流程门禁，不是不可伪造的密码学身份认证：普通 JSON 文件本身不能证明是谁点击了确认。因此生产实现必须让非交互/CI 进程不能调用 confirm 子命令，确认命令在消费 nonce 时再次展示 diff/证据/leak 摘要并写 durable audit；代码 review/提交只能作为额外审计，不得替代 writer 的交互确认。若未来需要强身份保证，再单独引入签名或 OS 凭据方案，不把当前字段误称为密码学证明。

`evidence_state` 的计算规则，按阻断优先级命中第一条：

| 条件 | evidence_state |
| --- | --- |
| 没有 target | missing |
| snapshot/selector 不存在或 selector 本身无法解析 | unresolved |
| 上游 Vault 未挂载、revision 不匹配或本地 sidecar 不可用 | 保留最近一次可计算的 evidence_state；若从未成功计算则为 `unresolved`，同时设置对象 `availability: unavailable` 和具体 `availability_reason` |
| 被引 snapshot 已漂移、snapshot manifest 变化或 evidence binding hash 失效 | stale |
| target 之间存在版本、前提、数值或结论冲突 | conflicting |
| 只有部分 claim/target 被确定性检查覆盖 | partial |
| 至少两个独立 source 对同一命题和范围一致支持 | corroborated |
| 全部 target 可定位且支持，但只有一个独立 source | supported |

`validation_state` 只表达 LLM 规范审计的运行结果：`not_run` 表示未运行（离线、provider 不可用、输出 malformed 或覆盖不全），`pass` 表示审计通过，`fail` 表示存在规则违反，`stale_ruleset` 表示被引用的规范章节已变化、结论需重跑。确定性校验的结果不进这一轴——它是阻断门，不通过页面根本不会进入 `review`。上游不可用属于 `availability` 轴。

同一 `(content_sha256, evidence_sha256)` 下可以存在多份审计报告（不同 provider、不同时间）。它们分歧时**取 `fail`**，不按时间取最新：按最新取值等于"最后跑的模型说了算"，可以反复换 provider 重跑到出现一次 `pass` 就过门禁（审计洗牌）。要过门禁只能改内容，不能换模型。

模型判定本身有随机性，所以 fail 优先必须配一个留痕的复议出口（`VAL-003`）：owner 可以对某一份 `fail` 报告签一条 `validation-override/v1` 记录，声明"我读过这份 fail，它是误判"。该记录必须由 `actor_type: human` 签署（Agent 不得代签）、必须给出 `reason`、必须逐条列出该报告里全部非 `supported` 的 claim（只翻一条不能整份翻案），并绑定被复议报告的稳定标识与当前 `(content_sha256, evidence_sha256)`——内容一改，复议自动失效。复议后该报告不再参与派生；若全部 verdict 报告都被复议掉，`validation_state` 回落 `not_run`，而不是自动变成 `pass`。复议记录 append-only，`record_sha256` 自证，篡改即失效。

`strength` 的映射规则，按顺序命中第一条：

| 条件 | strength |
| --- | --- |
| `kind: index` | index |
| `kind: reference` | reference |
| `evidence_state: conflicting` | conflicted |
| `evidence_state: partial` | partial |
| `evidence_state: unresolved` 或 `stale` | unresolved |
| 全部 claim 只能由 `origin: personal` source 支撑 | personal |
| 全部 claim 为 `evidence_status: common-knowledge` 且替代检查通过 | attested |
| `evidence_state: corroborated` 且验证报告通过 | corroborated |
| 有效 LLM report 且 verdict 为 pass，且 claim 的 `resolved_targets` 覆盖 ≥2 个不同 `source_id` | verified |
| 有效 LLM report 且 verdict 为 pass，但只有单一 source | attested |
| 其他 | 不可发布，等待补证或人工决策 |

`kind: knowledge` 的页面若同时含 personal 与 external claim，取更保守的一侧：只要有任一 claim 只由 personal source 支撑，整页 strength 降为 `personal`。混合来源不产生"部分已验证"这种中间状态，因为读者无法逐条区分。

kind 与 status 正交：三种 `kind` 都可处于任一 `status`。真正的约束在下面的「互斥与前置约束」清单里，不用一张全为"允许"的矩阵表达。

`private_publishable` 的判定必须同时满足：`status == published`、`publication_scope == private`、存在明确且可用的 `target_vault`、`validation_state ∈ {not_run, pass, stale_ruleset}`、`evidence_state ∉ {missing, partial, conflicting, unresolved, stale}`、无未解决的 `source_drift` 阻断项，以及存在当前内容 hash 绑定的人工审计确认。当有效保密等级为 `internal` 时，确认操作还必须展示并记录 internal 发布告警确认；未确认告警不得发布。

`public_publishable` 的判定必须同时满足：对象 owner `vault_id == public` 且该 vault `allow_public_projection == true`、`status == published`、`publication_scope == public`、`effective_confidentiality == public`、`validation_state ∈ {not_run, pass, stale_ruleset}`、存在当前 `(content_sha256, evidence_sha256)` 绑定的人工审计确认、`evidence_state ∉ {missing, partial, conflicting, unresolved, stale}`、无 `source_drift` 阻断项、当前 `release_input_sha256` 绑定的 public-safe 人工 confirmation event 存在，且由 durable authority 重新派生的 `public_release == true`。`public_release` 默认值为 `false`；它是 projection 的 materialized field，不是作者可写的 Front Matter 字段。只有匹配当前 release/content/evidence/input-leak hash 的人工事件和 public owner `ledger/audit/operations/<operation_id>.json` 才能使它派生为 true；hash 变化后旧事件保留但自动回到 false。任何 private vault 对象不能仅通过修改该字段进入 public projection；必须先生成新的 public-owned 输出、重新校验并通过 leak gate。任一不满足时 public 构建跳过该页，并在构建报告中列出原因。

直接创建的 public Wiki 与 private source 脱敏后生成的 public copy 都必须有 operation record：直接 public 的完整审计摘要保存在 public Vault 的 `ledger/audit/operations/`，public copy 的完整 lineage、`source_vault_ids` 和人工操作记录保存在源 private Vault；public-owned 的脱敏确认事件另存于 public repo 的 `ledger/release/public-confirmations/`，使 public projection 在没有 private checkout 时仍可复现。public projection 只保留当前 `release_input_sha256`、`public_release`、`public_lineage_commitment`、确认事件 hash 和不含 private ID 的公开字段。该 commitment 是 lineage 记录路径的 sha256，只用于本机回到审计记录；它不含 private Vault 名称或对象 ID，因此不需要额外的 HMAC 密钥体系。

`publication_warning` 在有效保密等级为 `internal` 且 `private_publishable` 为 true 时为 `internal`，其他情况为 `none`。页面、查询结果和 Agent 输出都必须显示该告警。public release 的 preview 只生成 `public_release: false` 和待审材料；人工通过交互式 confirm 写入 `ledger/release/public-confirmations/<event_id>.json` 与 `ledger/audit/operations/<operation_id>.json`，projection 再重新派生开关。任何自动流程、LLM、Agent、leak gate、Front Matter 或 manifest 字符串都不能单独修改它。输出 hash 变化、来源变化或 leak gate 重新失败时，旧事件 append-only 保留但不能匹配，工具必须将派生值重置为 `false`。

互斥与前置约束：

- `planned` 不能有正文、sources、evidence；F008 的题目关系不参与当前状态计算；
- `planned` 不能直接跳到 `published`，必须先经过 `draft`；
- `deprecated` 与其他 status 互斥，是终态之一，只能通过显式修订回到 `draft`；
- `published` 必须有确定性校验全部通过、`validation_state != fail`，以及绑定当前 `(content_sha256, evidence_sha256)` 的人工审计确认；否则自动回落到 `draft` 或 `review`；
- `published` 必须有 `publication_scope: private|public`；`publication_scope: none` 不能与 `status: published` 组合；internal private 发布还必须有 internal 告警确认；
- `public` `published` 必须有当前输出 hash 绑定的 `public_release: true`、人工操作者和 public confirmation；hash 变化后必须回到 `false`，不得复用旧确认；
- `public_release: true` 只能由 `public-release-confirmation/v1` 的人工事件驱动，并且只能出现在 owner `vault_id: public`、`publication_scope: public`、`status: published` 的 public-owned object 上；其他组合必须拒绝，而不是仅把它派生为 false；
- F008 题目只能挂在通过其独立门禁的 `kind: knowledge` wiki 上；当前版本不创建或解析题目关系。

这张表是实现的判定依据，也是测试用例的来源：每个非法组合都必须有一条对应的拒绝测试，避免各校验点各自推理出不同结论。

### 6.9 引文规范化与逐字匹配

6.7 的人工引文和 8.2 的模型引文用**同一个规范化函数**，不允许两处各写一套——两处标准不一致会导致同一条引文在一条路径上通过、在另一条路径上失败。

```python
def canonical_quote(s: str) -> str:
    ...
```

规范化步骤按顺序执行：

| 步骤 | 处理 | 理由 |
| --- | --- | --- |
| 1 | Unicode NFKC 归一 | 统一全角/半角字母数字、兼容字符 |
| 2 | 全角标点映射为半角：`，。；：？！（）【】「」“”‘’、` → `,.;:?!()[][]""''` | 中文技术写作里同一句话的标点常在全半角之间漂移 |
| 3 | 只在 extractor 明确声明 `markup_projection` 时，按其 offset map 去除包装标记；canonical code/log/PDF text 中的 `` `*`、`_`、`~`、`\\` `` 等字符一律保留 | 不能把 C/C++ 运算符、指针或 shell 转义误当成 Markdown 标记 |
| 4 | 将连续排版空白映射为单个空格；删除零宽字符 U+200B/FEFF 和不换行空格 U+00A0，但不删除语义性空格 | 保留英文词边界，避免 `in to` 与 `into` 或代码 token 被错误合并 |
| 5 | 保留大小写 | 大小写在技术标识符里是语义性的（`Size` 与 `size`） |
| 6 | 保留数字与单位原样 | 不做数值换算；是否有空格按步骤 4 的结果保留 |

匹配规则：

- 先按 target 读取不可变 snapshot，再用 evidence item 的 `TextPositionSelector` 限定候选范围，用 `TextQuoteSelector.exact` 做**规范化后的子串包含**判断；
- selector 的 `prefix`、`suffix` 和 position 只用于消歧、恢复建议和 UI 高亮，近似匹配不能单独通过门禁；
- 匹配目标是 target 指向的 snapshot 范围，不是当前 source 阅读笔记全文；引文出现在其他 snapshot 或未绑定的章节等于证据错配，判失败；
- 引文规范化后长度小于 `policy.yaml` 的 `quote_min_chars`（建议中文 12 字符）时判失败：太短的引文可以匹配到任何地方，不构成证据；
- 一条 claim 有多个 target 时，每个 target 都必须有对应的 `supporting_quotes`，逐条匹配并记录 offset。

canonical snapshot 已在提取阶段固定文本边界，因此匹配不再粗暴删除全部空白或猜测 Markdown 标记。对 HTML/PDF 的展示换行，extractor 必须提供可验证的 offset map；对代码、日志和纯文本，空白和标点按原样保留。这样既能容忍排版换行，又不会把有语义的代码字符归一掉。若无法建立一一对应的 offset map，返回 `selector_unresolved`，不能用更宽松的规则兜底。

失败时必须返回可诊断信息：规范化后的引文、snapshot hash、evidence item ID、selector 范围、snapshot 的规范化长度、以及最长公共子串的位置和长度。只返回"不匹配"会让人无法判断是引错了 snapshot、抄漏了半句，还是规范化规则太严。规范化规则的调整必须与 fixture 一起提交，避免为了让某一篇通过而悄悄放宽标准。

## 7. F008 Question/练习延期边界（非当前规范）

旧的 Question 字段和四选一模板已废弃。F008 现行契约见 [Question 与面试练习实现设计](./technical-design/question-and-practice.md)：支持单选题、多选题和面向面试的简答题，绑定已验证 Wiki claim，复习调度采用 FSRS；题目、答案、解析和复习状态仅位于 local/private，public 运行时仍不得读取 practice。

## 8. LLM 证据验证

### 8.1 验证职责

LLM 只负责判断 wiki claim 是否被 source 支持，不负责替代 source，不负责直接决定事实真伪，也不允许自由扩展 source 没有表达的结论。Source snapshot、wiki 正文、claim 和引文都属于**不可信数据**，不是系统指令；验证请求必须使用显式数据边界/固定系统提示，禁止把 snapshot 中的“忽略规则”“调用工具”或外部链接当作指令。provider validation 运行时禁用工具调用、外部 URL 访问、自动浏览和隐式网络；LLM 输出只作为待校验数据，不能直接改变 canonical、状态、发布或 Vault 配置。

验证输入：

- wiki 候选正文；
- wiki 的 evidence claim 列表；
- 对应 evidence target 的 snapshot 正文、selector 范围和 source 阅读 locator；
- source 的 origin、read status 和 evidence status；
- wiki 和 source 的内容 hash。

### 8.2 结构化输出

~~~json
{
  "wiki_id": "wiki-transformer",
  "verdict": "pass",
  "claims": [
    {
      "claim_id": "c1",
      "verdict": "supported",
      "targets": [
        {"source_id": "source-transformer-paper", "evidence_id": "e1"}
      ],
      "supporting_quotes": [
        {
          "evidence_id": "e1",
          "exact": "注意力权重由 Q 与 K 的点积经 softmax 得到，再与 V 加权求和。"
        }
      ],
      "reason": "来源明确描述了该机制"
    }
  ],
  "unmapped_claims": [],
  "contradictions": [],
  "missing_evidence": []
}
~~~

`supporting_quotes` 必填且每一条**必须逐字来自 target 指向的不可变 snapshot**。工具在收到响应后做一次确定性校验：按 6.9 的规范化规则，把引文与 evidence item selector 限定的 snapshot 范围归一后做子串匹配，找不到即判 `unsupported`，无论模型自己给出什么 verdict。

这一步的作用是把一半判断从"相信模型"变成字符串匹配。没有它，模型倾向于给出宽松的 `supported`，而门禁没有任何机制能识别这种幻觉式支持。`synthesis` 类 claim 需要为每个 target 各给一条引文；`inferred` 类 claim 的引文指向作为推理前提的原文，而不是结论本身。

验证还要求 adapter 固定可审计的采样参数（`temperature=0`，或 provider 等价能力），单次调用并记录 call ID 与输入 hash。不做多次采样聚合：确定性采样下重复调用要么恒同（无信息量），要么说明 provider 并非确定性（声明失效），两种情况都不该用"取最保守"掩盖。判定严格性由覆盖与举证义务保证（全 claim 全 target 覆盖、逐条回引规则条目、rationale 必须引用原文区间），而不是靠重复调用。

审计器的判定质量必须被度量：维护一组人工标注的 fixture（既有真实支持、也有似是而非的伪支持），在更换 provider、改动 prompt 或调整 `rule_refs` 时跑回归，并记录精确率与召回率的变化。它是回归 fixture，不是阶段退出门——LLM 审计是可选层，把它做成退出门会让「审计器不够准」变成「无法发布」。但覆盖义务的校验（全覆盖、逐条回引、原文区间举证）是硬性的自动检查，不依赖这组 fixture。

单条 verdict：

~~~text
supported
partially_supported
unsupported
contradicted
unmapped
~~~

发布门禁：

- supported：允许继续；
- partially_supported：只能保持 draft；
- unsupported：失败；
- contradicted：失败；
- unmapped：失败。

### 8.3 LLM 不可用时

Skill runtime 未提供合规 provider、网络不可用、返回格式错误、覆盖不全或模型调用失败时：

- source 查询和 source 写入仍可用；
- 确定性校验照常运行，它不依赖 provider；
- `validation_state` 记为 `not_run` 并附结构化 `not_run_reason`（`provider_unavailable` / `offline` / `context_exceeded` / `malformed_output` / `incomplete_coverage`），不记为 `fail`；
- 页面、preview 和查询结果必须显示"未做语义审计"，不得表述为已验证；
- 人工审计通道不受影响：确定性校验通过 + 人工审计确认后仍可 `published`。

不做 provider capability 协商：LLM 既然是可选层，「能力不足」的正确处理就是不跑并记录原因，而不是与 provider 谈判能力矩阵再 fail-closed。具体 endpoint、模型版本和密钥由 Skill runtime 管理，不进入验证 schema、Vault manifest、Git 或普通审计日志；报告只保存 opaque provider identity 与 `not_run_reason`。

同样不允许的是反向偷懒：`not_run` 只能由运行时观测到的事实产生，模型不能自行声明 `not_run`；操作者主动跳过则不写审计报告——没跑就是没跑，不留"已审"痕迹。审计一旦运行，必须满足 ADR-0010 的覆盖与举证义务（全 claim 全 target 覆盖、逐条回引规则条目、rationale 引用原文区间），否则整次审计无效。

### 8.4 验证报告

每次验证保存（只记录运行时安全摘要，不记录 endpoint、密钥或敏感请求正文）：

~~~yaml
wiki_id:
validator_version:
provider_identity:
ruleset_sha256:
audited_at:
wiki_content_sha256:
wiki_evidence_sha256:
evidence_bindings:
  - resolved_object_ref:
      vault_id: public
      object_type: source
      object_id: source-transformer-paper
    source_id: source-transformer-paper
    evidence_id: e1
    snapshot_sha256: sha256:...
    selector_sha256: sha256:...
    quote_sha256: sha256:...
claims:
unmapped_claims:
contradictions:
verdict:
~~~

报告绑定 `wiki_content_sha256`、`wiki_evidence_sha256`，以及**每个 target 的 snapshot/selector/quote**，不是整个 source 文件的摘要 hash。这样修改 source 中未被引用的阅读笔记章节不会波及已审计的 wiki，避免一次错别字修正引发全库重审。报告还应记录审计提示词版本、schema 版本、输入 target 列表和 snapshot manifest 版本，便于复现。完整 provider 响应只保存在被忽略的 `var/state/llm-validation/`；发布所需的人工审计确认必须写入 owner vault 的 `ledger/audit/validation/`，不能把临时目录当作唯一依据。报告不保存 API key、密码和敏感凭据。

`confidentiality: internal` 的 source 正文只能发送给满足 runtime 保密要求的 provider；没有这样的 provider 时记 `validation_state: not_run` + `not_run_reason: provider_unavailable`，不得改用公开 provider。provider 的 endpoint、模型版本和密钥由 Skill 运行时读取并管理，不写入仓库或普通报告。

验证报告还应记录 adapter 版本、`ruleset_sha256` 和 call ID；报告 append-only。人工审计确认固定写入 `ledger/audit/validation/<object_type>/<object_id>/<confirmation_sha256>.json`，不能把临时目录当作唯一依据。确认证明的是"人在该 hash 上背书过"，不是模型事实正确性的密码学证明。

### 8.5 验证报告失效规则

验证报告只有在下列条件全部满足时才有效：

1. wiki 当前 `content_sha256` 等于报告中的 `wiki_content_sha256`；
2. wiki 当前 `evidence_sha256` 等于报告中的 `wiki_evidence_sha256`；
3. 报告中每个 evidence binding 的 `snapshot_sha256`、`selector_sha256` 和 `quote_sha256` 等于当前 target；
4. 全部被引 evidence item 和 snapshot 仍然存在，且上游 source 的 `read_status`/`evidence_status`/`origin`/`confidentiality` 重查结果与报告记录一致；
5. validator、schema 和 prompt 版本仍在 `policy.yaml` 声明的兼容范围内；
6. 报告 verdict 为 `pass`，且没有 partially supported、unsupported、contradicted 或 unmapped claim。

按 6.6 的分类，tags、aliases、related、title 和 domain 变化不影响以上任何一条，不触发重新验证。

任一条件不满足，页面都必须回到 `draft` 或 `review`；人工审计确认随内容 hash 变化自动失效，重新确认后才能回到 `published`。规范章节变化只把 LLM 结论标记 `stale_ruleset`，不影响人工确认的有效性。

prompt 或 validator 升级时，`policy.yaml` 必须显式声明兼容策略：`compatible` 表示旧报告继续有效，`breaking` 表示全量重验。默认按 `breaking` 处理，避免静默沿用旧标准。

## 9. 写入操作协议

所有写入必须是两阶段 operation，每次写入生成一条 `operation/v1` 记录作为该次写入的权威凭据：

~~~text
preview -> explicit apply
~~~

### 9.1 Preview

Preview 阶段：

- 不修改目标文件；
- 生成候选内容和 diff；
- 运行确定性校验；
- wiki 运行 LLM 验证；
- 生成 operation_id；
- 生成 diff_sha256；
- 保存目标文件的 before_sha256。

输出格式：

~~~text
status: preview
operation_id:
targets:
diff_sha256:
deterministic_validation:
llm_validation:
confirmation_required: true
~~~

### 9.2 Apply

只有用户明确确认同一个 operation_id 后才能 apply：

1. 获取目标 Vault 的排他写锁（多 Vault operation 按稳定 `vault_id` 顺序获取全部锁，见 9.8）；
2. 仅对 `acquisition: fetch` 或需要网络 provider 的 operation 检查网络与归档可达性（`require_network`，见 5.9）；纯 local-file/personal-note operation 不因网络离线失败；
3. 重新检查目标文件 hash；
4. 重新检查 source/wiki 输入 hash；
5. hash 不匹配则 operation 失效；
6. 在目标 Vault 同一文件系统创建 staging，写入 canonical 文件、durable record、projection 和索引候选；对每个文件计算 after hash；
7. 对 staging 运行最终 schema、引用、保密、证据和 leak gate 校验，任何失败都只清理 staging；
8. 写入并 fsync `var/state/operations/<operation_id>.commit-intent.json`（包含旧/新 hash、待替换路径和恢复动作），再原子替换 canonical 文件和 durable record；
9. 写入 commit marker 并 fsync 目录；启动恢复器若发现 intent 无 marker，按 manifest 恢复旧文件，发现 marker 则补建索引并完成 operation；
10. 原子替换 projection/index；若此阶段失败，保留旧 projection，operation 进入 `applied_index_pending`，canonical 变更不回滚也不被伪装为全链路成功；
11. 索引完成后追加 `applied` durable record，清理 intent/staging，释放写锁。

单 Vault 的“原子”边界因此由 commit-intent + recovery journal 保证，而不是假设多个文件系统 rename 可以组成事务；跨 Vault operation 仍只提供按 Vault 排序的锁和可补偿的部分成功记录，不声称分布式事务。

### 9.3 Operation 状态和幂等性

```text
created
  -> previewed
  -> awaiting_confirmation
  -> applied
  -> applied_index_pending

previewed / awaiting_confirmation
  -> blocked     (缺少来源、provider、Vault 或安全门禁)

previewed / awaiting_confirmation
  -> expired       (超过有效期或输入 hash 变化)
  -> rejected      (用户拒绝)
  -> failed        (应用或最终校验失败)
```

`operation_id` 使用随机 UUID，不以标题或时间戳代替。一个 operation 只能应用一次；重复 apply 必须返回既有结果，而不是再次覆盖文件。`blocked` 表示当前前置条件不足，可在条件修复后重新 preview；它不是“暂存后自动继续”。`applied_index_pending` 表示 canonical 文件和 durable record 已安全提交，但 projection/index 尚未完成；在该状态恢复前，相关对象不能成为新的 `public_publishable`，旧 projection 可以继续提供上一版结果。批量操作必须把每个目标文件、before hash、after hash 和失败阶段写入 manifest。幂等 key 必须是字段名明确的 canonical JSON（`kind`、`target_ref`、`input_hash`、`target_vault`、排序后的 `source_vault_ids`、`policy_version`），禁止直接拼接字符串造成碰撞。

`operation_id` 的规范形态是 `op_<32 位小写 hex>`；生成端与校验端必须共用同一实现（`tools/common.py::new_operation_id` / `safe_operation_id`），禁止各调用点自行剥前缀再套用其他 ID 词表——`release confirm` 曾因此对每一个真实 operation 都返回 `event_id_invalid`。校验只约束前缀、字符集与长度上限（`operation_id` 会成为审计文件名，要挡的是路径穿越与文件名注入），不复刻生成端的位宽。

幂等命中不是失败：重复提交一条内容完全相同、且已经落盘的 append-only 记录（确认事件、apply 结果）必须返回 `already_applied` 并回带既有记录的 hash 与路径，退出码为成功。只有“同 ID、不同内容”才是冲突，返回 `*_conflict` 并 fail-closed 拒绝覆盖。把这两种情况都报成失败会诱导操作者删除 append-only 记录重跑，等于用删审计换一次“成功”。

### 9.4 禁止操作

Skill 和知识库工具禁止：

- 无 source 直接写 wiki；
- 直接修改 var/queries/；
- 直接修改 frontend/、backend/；
- 自动删除、移动、覆盖和重命名页面；
- 自动 commit、push、发布；
- 通过模糊的“继续”“好的”确认未知范围的批量写入。

### 9.5 Source/Wiki 的写入准入

当前主链路只实现 Source 和 Wiki。preview 阶段必须逐条检查下表，任一项不满足即 blocked，并返回缺失项和修复动作；Question 的写入准入留给 F008：

| 检查项 | source | wiki |
| --- | --- | --- |
| schema 与必填字段 | 必须通过 | 必须通过 |
| 来源完备性（5.9） | 必须满足三者之一 | 不适用 |
| 网络可达（`require_network`） | 网络来源必须满足；`local-file`/`personal-note` 按 allowlist 可离线 | 仅在需要 fetch/provider 时检查；纯 local-file/personal-note 且已有有效验证记录时可离线 |
| ID 在所属 Vault 内唯一 | 必须 | 必须 |
| domain 在词表内 | 必须 | 必须 |
| confidentiality 与所在 vault 一致 | 必须 | 必须，且不低于上游 source |
| 内网 URL 与 public 声明冲突 | 阻断 | 不适用 |
| 正文模板章节齐全 | 必须 | 必须 |
| 证据边界与 read_status 一致 | 必须 | 不适用 |
| external 必须有 url 与 retrieval | 必须 | 不适用 |
| 上游对象存在且可解析 | 不适用 | sources 非空且全部存在 |
| 上游状态门槛 | 不适用 | 不能只引用 metadata-only source |
| claim 映射 | 不适用 | 每个核心论断有 claim_id 和 evidence target |
| 支持类型兼容矩阵（6.5） | 不适用 | 必须通过 |
| LLM 证据验证 | 不需要 | 必须 pass 才能离开 draft |
| snapshot/selector 绑定 | 不适用 | 每个 target 必须解析到不可变 snapshot 和 selector |
| 发布确认与保密告警 | 不适用 | private publish 必须有当前 hash 的 confirmation；internal private 还必须 warning ack；public release 默认 false，只有人工 confirmation event 才能改为 true |
| hash 快照写入 | content_sha256、snapshot hash | content_sha256、evidence_sha256、evidence bindings |

新增顺序是强约束：没有 source 不能建 wiki。Question 的 source/claim 绑定和题型门禁不在当前表中，由 F008 单独定义。

来源完备性和联网要求是两个正交约束：没有来源的内容不允许写入；`require_network` 只约束 `acquisition: fetch` 和需要网络的 provider 调用。`local-file`/`personal-note` 在归档 snapshot、selector 和其他 precondition 完整时可离线 preview/apply；网络 source 只能在抓取与归档完成后进入可确认状态，避免留下没有证据载体的待确认操作。

### 9.6 废弃与删除

内容会过时，也会被发现本来就是错的。9.4 禁止的是**自动**删除，不是禁止删除；需要一个显式、可预览、可回滚的退役路径，否则错误内容只能靠手工乱改。

两级操作，都必须走 preview/apply：

~~~text
retire   标记 status: deprecated，保留文件与路由
purge    真正删除文件，需要 retire 已生效且引用已清理
~~~

`retire` 的效果：从 public build 与 public 索引移除；从 RAG 索引移除对应 chunk；F008 题目若存在，是否失效由 F008 的独立迁移规则处理；保留旧路由指向一个"此页已废弃"的提示页，避免外部链接直接 404；在 backlinks 中把该页标记为废弃而不是删除链接。

`purge` 的前置条件（任一不满足即阻断）：

1. 目标已处于 `deprecated`；
2. 没有任何 `public_publishable` 或 `private_publishable` wiki 的 claim 引用它；
3. 若 F008 已启用，引用它的题目已按 F008 规则删除或改绑；当前版本无此前置条件；
4. `part_of` 子对象已处理完毕；
5. route map 中已登记旧路径的最终归属（重定向目标或明确的墓碑页）。

删除的是文件，不是历史：`purge` 前必须把对象的 ID、标题、最后内容 hash 和废弃原因写入 owner vault 的 `ledger/audit/operations/` manifest。这样将来遇到同一份错误资料时，能知道它曾被判定为错误并且原因是什么，不会再次原样引入；运行态 `var/state/operations/` 不能作为唯一历史记录。

废弃原因是必填的枚举加自由说明：

~~~text
obsolete      上游版本演进导致内容过时
incorrect     内容本身错误
superseded    已被另一个页面取代（必须给出 replaced_by）
duplicate     与另一个页面重复（必须给出 replaced_by）
out-of-scope  不再属于本知识库范围
~~~

`superseded` 与 `duplicate` 必须填 `replaced_by`，前端和查询把旧 ID 解析到新页面，Agent 查询旧 ID 时返回新目标而不是空结果。

### 9.7 重命名与移动

ID、标题和路径都会需要调整，而一次改名要同时波及：反向索引、backlinks、`related`、`part_of`、`sources` 引用、route map、验证报告中的 object/evidence binding。F008 若启用，再由其迁移规则处理题目引用。手工改这些一定会漏，因此重命名必须是一等操作，而不是"人工去改"。

~~~text
rename   改 ID（连带所有引用）
move     改路径与 domain（不改 ID）
retitle  改 title（不影响引用）
~~~

`rename` 的 preview 必须列出全部受影响对象与文件，并区分两类改动：引用更新（机械替换，可自动）与内容改写（正文里提到旧名称的自然语言表述，需人工确认）。apply 时全部改动在一个 operation 内原子完成，任一文件失败则整体回滚。

规则：

- 旧 ID 进入 route map 并保留重定向，避免外部链接与旧笔记失效；
- 旧 ID 不得被复用为新对象的 ID；
- 改 ID 不改变正文内容，因此 `content_sha256` 不变，验证报告仍然有效——但报告中的 object/evidence binding 前缀需要同步重写，这是纯机械替换；
- `move` 改变 domain 时必须重新校验 domain 与目录一致性；
- `retitle` 只影响显示名，不触发任何重验（title 属于 6.6 的分类字段）。

### 9.8 并发与锁

单用户环境仍然存在三方并发：Agent、本地后端、编辑器。`before_sha256` 检查与原子替换之间存在窗口，两个 apply 交错会造成一方的写入被静默覆盖。

- 所有 `apply`、`retire`、`purge`、`rename` 和索引生成必须先获取目标 Vault 的排他锁（`var/state/locks/<vault_id>.lock`，记录持有者、operation_id、随机 `lock_token`、fencing token、获取时间和 `heartbeat_file`）；锁主体在持有期间不可变，最新心跳写入同目录 sidecar 并原子替换；涉及多个 Vault 时按稳定 `vault_id` 顺序获取全部锁，避免死锁；锁目录属于临时运行态并被 Git 忽略。
- 锁只保护写入，查询与 preview 不加锁；
- 锁必须有超时与陈旧锁清理（记录 PID、进程启动时间、时间戳和 `lock_token`），避免异常退出后永久阻塞。陈旧锁默认只阻断并要求显式 `lock recover`，不能按时间自动删除；恢复前要检查 PID/进程启动时间，恢复动作追加 `lock-recovery` durable audit record。
- writer 在写 canonical、commit-intent、projection/index 和释放锁前都必须重新读取锁文件并校验 `lock_token`/operation_id；token 不匹配时立即中止并保留旧产物，防止人工恢复旧锁后原进程继续写入。锁恢复不能当作分布式 fencing，只保证同一工作区内的提交点再次校验。
- 拿不到锁时返回 `blocked` 并说明当前持有者，不排队等待、不强行抢占。

## 10. 当前三类工作流

### 10.1 查询阅读

公开模式：

~~~text
Pagefind -> public_publishable wiki
~~~

本地模式：

~~~text
精确 ID/反向索引 -> direct lookup
自然语言/混合查询 -> QMD (default) -> SQLite FTS5 -> Python/SQLite LIKE fallback
~~~

查询优先级：

1. 精确 ID；
2. 标题和别名；
3. 领域和标签；
4. 正文关键词；
5. backlinks、related 和 source 回溯。

统一返回：

~~~text
route:
answer:
wiki:
sources:
related:
evidence:
availability:
availability_reason:
confidentiality:
method:
degraded:
limits:
next_gate:
~~~

Agent 不直接扫描任意 Markdown，而是调用本地 CLI、生成索引或 FastAPI 查询接口。

### 10.2 写入

固定写入顺序：

~~~text
source -> wiki -> validate -> index -> build
~~~

Source 和 wiki 是两个独立 operation：

```text
source preview -> 用户确认 -> 写入 sources -> source 校验
wiki preview   -> 确定性校验 -> LLM 验证 -> 用户确认 -> 写入 wiki
```

如果用户要求“把一段话写成 wiki”，但没有 source，必须先创建 personal source，不能在同一个隐式操作中跳过 source 层。LLM 验证通过前，不能向用户展示“可应用写入”的 wiki 候选。

### 10.3 索引

生成五张反向索引：

~~~text
by-domain
by-tag
by-alias
by-link
by-source
~~~

同时生成：

~~~text
catalog.json
graph.json
rag-index.jsonl
backlog.json
~~~

`backlog.json` 汇总 `status: planned` 条目和 `content_verdict: pending-review` 的待处理项，是"还需要写什么"的唯一入口。`deprecated` 页面单独成表，供查询时给出替代目标。

public index 只包含 `public_publishable: true` 的 wiki；local index 包含已挂载 vault 的 sources 和 wiki，并保留 `vault_id`、有效保密等级和 `publication_warning`。`planned` 与 `deprecated` 只进 local index 的元数据表，不进正文检索和 RAG 索引；unavailable private 对象只保留状态元数据，不伪造正文。F008 若启用题库，再由其独立生成题目索引。

索引文件必须带有生成器版本、生成时间、输入集合 hash 和 schema 版本。索引生成失败时，旧索引保持不变；不能留下只有一半内容的新索引。

知识库会持续变大，`planned` 条目、按抽象层级拆分出的子 source 和归档快照都会推高对象数量，这是预期结果而不是问题。索引生成必须为此留出余量：

- 每个对象记录 `content_sha256` 与上次入索引时的 hash，只重算发生变化的对象；
- 全量重建保留为可显式触发的操作（schema 或生成器版本变化时必须全量）；
- 增量结果必须与全量结果一致，这条要有对照测试，否则增量会静默漂移；
- 对象数超过 `policy.yaml` 中的阈值时，`catalog.json` 与 `graph.json` 按 domain 分片输出，避免单文件过大拖慢前端首屏。

`planned` 条目保留为独立文件而不是集中清单：它们是未来的写作入口，需要能被直接打开、被链接引用、被 backlinks 统计。文件数增长由索引和 RAG 承担，不通过压缩对象模型来回避。

### 10.4 Question/复习（后续 F008，不属于当前运行面）

F008 提供独立 Question/练习服务；题目 schema、claim 绑定、答案/解析校验、FSRS local state 和备份边界见其 Technical Design。public API、索引和静态构建仍不读取题目答案、解析或复习状态。

## 11. 索引与查询技术

### 11.1 Public index

~~~text
wiki.public_publishable == true
  -> var/queries/public
  -> Astro prepare-content
  -> Pagefind
  -> GitHub Pages
~~~

### 11.2 Local index

~~~text
sources + wiki
  -> var/queries/local
  -> QMD (default local natural-language/hybrid retriever)
  -> SQLite FTS5 fallback
  -> Python/SQLite LIKE deterministic fallback
  -> FastAPI
  -> 本地前端 / Agent Skill
~~~

第一阶段的基础检索不引入 Elasticsearch、独立向量数据库或 LangChain。知识规模、部署形态和个人查询需求优先要求确定性、可解释、可离线运行。RAG 作为本地自然语言问答和知识综合能力接入，但不改变 source/wiki 的内容真相源。

规模假设是"最终会很大"，但第一阶段不因此预埋一套自研向量系统。第一阶段的硬契约是 `QMD（若本机可用） -> SQLite FTS5 -> Python/SQLite LIKE`：

**检索分词与替代方案决策（2026-08-28 修订，均经联网核验）**：

- **QMD 替代已定**：QMD 二进制在公开渠道不可获得（brew 无包）。中文分词由 **wangfenjin/simple**（MIT，https://github.com/wangfenjin/simple，v0.7.1，858★/CI/预编译 release）承担：FTS5 建表 `tokenize='simple'`，查询经 `jieba_query()`（词级分词 + AND，跨虚词命中如"结构化讨论"→"结构化的讨论"）；扩展位于 `var/state/lib/libsimple`（gitignored，bootstrap 自动下载），加载/词典失败 fail-closed 回退 unicode61，tokenizer 记入 `index_info` 并由 doctor 显性报告。
- **其他核验过的候选**（已评估未采纳）：Meilisearch（MIT CE、hybrid 检索、中文优化，但需常驻服务+同步管线，语义需求真实出现时再评估，届时需新 ADR）；Tantivy（MIT、Lucene 级库形态，需 Rust 编译链+替换索引层）；sqlite-vec/向量（仅解决语义，引入 embedding 模型依赖，与确定性内核冲突）。
- **决策原则**：检索按痛点加层，不做终点站切换。向量**不是**终极方案——精确词组/可解释性/重嵌入成本/模型绑定四项固有短板使纯向量不适合证据驱动库；生产终态是 hybrid（词法+向量+融合），且 FTS5 在 5 万篇内不是规模瓶颈。静态站的检索由 Pagefind 承担（v1 起内建 CJK 分词，与 FTS5 分层互不依赖）。

原契约（qmd 段落继续有效）：
QMD 自己是否启用向量、rerank 或模型缓存由其运行时能力决定，MyKnowledge 只消费带身份的候选并做权限/hash 二次校验；不要求单独部署 Embedding、FAISS 或 sqlite-vec，也不把它们列为第一阶段退出门。若未来 QMD 质量或规模不足，再以同一 `Retriever` 接口增加可持久化向量 adapter，并为其单独固定模型、索引版本和增量/全量一致性测试。`ledger/archive/text/` **可以**作为 local/private RAG 的可选召回输入，但当前 policy 默认 `include_archive_in_local_rag: false`；只有用户在对应 Vault 明确打开且通过 owner/保密检查时才加入。无论是否加入，归档正文都**不是证据载体**：claim 的权威 target 只能指向 source 绑定的 snapshot/evidence item，不能把 RAG 片段当作证据。

### 11.3 查询、RAG 和证据验证的边界

“查找文档”和“基于文档回答问题”是两种不同能力：

| 能力 | 是否需要 RAG | 第一阶段方案 |
| --- | --- | --- |
| 根据 ID、标题、标签、关键词找页面 | 否 | Pagefind、SQLite FTS5、反向索引 |
| 根据自然语言问题返回相关文档片段 | 是 | QMD 默认；不可用时 FTS5，再回退 Python/SQLite LIKE |
| 基于多个文档片段生成回答 | 是 | Retriever + LLM + citations |
| 基于 source 生成 wiki 草稿 | 可使用 | RAG 辅助候选生成，仍须 evidence validation |
| 根据 wiki 生成题目 | F008 延后 | 当前版本不暴露题目生成入口，不建立题目索引 |

RAG 的职责是"找到回答所需的上下文并组织答案"；Evidence Validator 的职责是"判断 wiki claim 是否被 source 支持"。RAG 检索到片段不能直接证明最终论断，也不能直接将页面变为 `published`。

### 11.4 RAG 标准处理链

```text
用户问题
  -> 查询解析
  -> QMD 默认 BM25/向量/RRF 召回
  -> FTS5 fallback（QMD 不可用）
  -> Python/SQLite LIKE fallback（FTS5 不可用）
  -> 合并去重（QMD 路径内部使用 RRF；fallback 路径跳过）
  -> 可选 Reranker
  -> 选取 source/wiki 片段
  -> LLM 生成回答
  -> 引用和 locator 校验
  -> 返回答案、引用和局限
```

QMD 可用时由 QMD 完成 BM25/向量融合和 RRF；切换到 FTS5 或 LIKE 后直接返回确定性候选，不伪造 RRF/语义分数，并在响应的 `method`、`degraded` 和 `limits` 中标明降级。

本地 RAG 索引由 `content/sources/` 和 `content/wiki/` 投影生成。每个 chunk 必须保留对象身份和证据定位，不能只保存一段没有来源的纯文本：

```json
{
  "chunk_id": "source-transformer-paper:已读取事实:001",
  "object_type": "source",
  "object_id": "source-transformer-paper",
  "vault_id": "public",
  "confidentiality": "public",
  "domain": "computer-science",
  "section": "已读取事实",
  "source_ref": "source-transformer-paper#已读取事实",
  "origin": "external",
  "read_status": "retrieved",
  "content_sha256": "...",
  "text": "..."
}
```

chunk 的 metadata 至少包含 `chunk_id`、`object_id`、`section`、`source_ref`、`origin`、`status`、`confidentiality`、`content_sha256`。空章节不生成 chunk，避免模板留下的空标题污染召回。source 或 wiki 正文变化后，相关 chunk 和回答缓存必须失效并重建；只改 tags 时不需要重建向量，只更新 metadata。

`internal` chunk 只存在于其 owner private vault 对应的本地索引文件中，不写入公开仓库；chunk 和回答缓存必须保留 `vault_id` 以便权限判断。`/api/ask` 的回答如果引用了任一 internal chunk，响应必须标记 `confidentiality: internal`、返回受影响的 private vault 集合（仅本地私有模式可见）且不写入可共享的回答缓存。

### 11.5 成熟方案对标

| 方案 | 类型 | 优点 | MyKnowledge 取舍 |
| --- | --- | --- | --- |
| LlamaIndex | RAG 编排框架 | 文档索引、Retriever、引用和 Query Engine 完整 | 可作为可选编排层，不接管内容写入和发布状态 |
| Haystack | Pipeline 框架 | 组件边界清晰，适合 FastAPI 和生产流水线 | 如果需要多 Retriever、Reranker 和评估，优先考虑 |
| LangChain | 通用 LLM 编排 | 生态广、集成多 | 不作为核心依赖，避免抽象过重和版本漂移 |
| RAGFlow | 完整 RAG 产品 | 解析、索引、问答和 UI 完整 | 不适合作为 Git Markdown 知识库的内容真相源 |
| Dify | LLM 应用平台 | 可快速搭建问答和工作流 | 不纳入核心架构，写入门禁难以由 MyKnowledge 控制 |
| Microsoft GraphRAG | 图增强 RAG | 适合大规模语料的全局总结 | 当前规模和成本不匹配，作为后续研究方向 |
| LightRAG | 图增强 RAG | 结合实体关系和向量检索 | 可实验，不作为第一阶段基线 |
| QMD | 本地 BM25/向量/RRF/Rerank 工具 | 增量 hash、CJK normalization、行号读取和 MCP 已有实现 | 作为本地自然语言/混合检索的默认只读 adapter；不写 canonical 文件、不决定状态；不可用时回退 FTS5 |

### 11.6 推荐技术组合

完整的 QMD 默认适配器、FTS5 必选基线和 fallback 契约见 [ADR-0007](./adr/0007-retrieval-and-index-architecture.md)。

第一阶段采用成熟组件加薄适配层，一次性交付 QMD 默认检索、FTS5/LIKE fallback、QueryResult、索引重建和测试；Embedding/FAISS/Reranker 只作为后续可插拔增强，不是第一阶段的隐含依赖：

```text
Markdown + YAML
  -> MyKnowledge 规范化分块
  -> QMD read-only adapter (default local natural-language/hybrid)
  -> SQLite FTS5 fallback
  -> Python/SQLite LIKE fallback
  -> [optional future] sentence-transformers / FlagEmbedding
  -> [optional future] FAISS or sqlite-vec adapter
  -> [optional future] RRF / reranker
  -> Skill provider runtime adapter
  -> citation/locator 校验
```

推荐组件：

| 能力 | 推荐 | 说明 |
| --- | --- | --- |
| 关键词检索 | SQLite FTS5 | 基础能力，离线、确定性、无外部服务 |
| 本地混合检索 | QMD 2.8.3（Node >=22） | 默认 BM25/向量/RRF/rerank；必须经 manifest/hash 校验；不可用自动回退 FTS5/LIKE |
| Embedding | 后续可选（例如 `BAAI/bge-m3`） | 必须单独评估模型、许可证、缓存和增量索引；不阻断第一阶段 |
| 向量检索 | 后续可选（FAISS/sqlite-vec adapter） | 只有在 QMD/FTS5 质量或规模不足时引入，不能成为第一版硬依赖 |
| Reranker | 后续可选（例如 `BAAI/bge-reranker-v2-m3`） | 仅影响召回排序，不改变证据/发布状态 |
| RAG 编排 | 自有 Retriever 接口，必要时接 LlamaIndex/Haystack | 保持 source、hash、locator 和状态由 MyKnowledge 控制 |
| 效果评估 | 自定义引用测试，必要时接 Ragas/DeepEval | 不能用评估分数替代 claim evidence 验证 |

不建议第一版直接引入 Elasticsearch、独立向量数据库、RAGFlow、Dify 或 LangChain。QMD 是本地默认运行时，但不是 public Astro 构建的硬依赖；未来若需要独立服务，再将 Qdrant、pgvector 或 OpenSearch 接到同一个 Retriever 接口后面，并保留 FTS5/LIKE fallback。

### 11.7 Retriever 接口和索引工具

```python
class Retriever:
    def search(self, query, scope, top_k=8):
        ...
```

第一阶段实现：

```text
FtsRetriever
QmdRetriever (default local natural-language/hybrid, read-only)
DeterministicFallbackRetriever
```

`EmbeddingRetriever`、`HybridRetriever` 和独立 `Reranker` 不属于第一阶段实现清单；如果未来接入，必须实现同一 `Retriever`/`QueryResult` 契约，并保留 FTS5/LIKE fallback。

建议工具：

```text
tools/ 建议职责模块：
- 索引构建：规范化分块、Embedding 和本地向量索引；
- 召回：FTS、向量和混合检索；
- 重排：可选候选重排；
- 带引用回答：基于检索片段生成带引用的回答；
- 引用校验：校验回答与 claim 的 locator 和 evidence target。
```

这些工具只负责索引、召回、回答和引用校验，不拥有 source/wiki 写入权限。默认本地自然语言/混合查询先调用 `QmdRetriever`；其输出必须重新解析为统一 `QueryResult`，验证 object ID、vault、confidentiality、hash 和 source/evidence 定位。QMD 不可用时自动选择 FTS5，FTS5 不可用时选择确定性 fallback 并标记降级；精确 ID/反向索引可直接走确定性路径。第一阶段不生成自有 FAISS/Embedding 文件；若未来启用向量 adapter，其索引、模型缓存和 `var/queries/local/rag-index.jsonl` 都是受 manifest/hash 管理的生成物，不能人工编辑。

### 11.8 RAG API 和 Agent Skill

本地后端增加：

```text
POST /api/retrieve
POST /api/ask
```

请求示例：

```json
{
  "query": "Transformer 中 Attention 是如何计算的？",
  "scope": "local",
  "top_k": 6,
  "include_sources": true
}
```

返回必须包含答案、引用、检索方式、片段数量和局限：

```json
{
  "answer": "...",
  "citations": [
    {
      "object_ref": {"vault_id": "public", "object_type": "source", "object_id": "source-transformer-paper"},
      "source_ref": "source-transformer-paper#已读取事实",
      "snapshot_sha256": "sha256:...",
      "text": "...",
      "confidentiality": "public"
    }
  ],
  "retrieval": {"method": "qmd", "chunks": 6, "degraded": false},
  "limits": []
}
```

Agent Skill 增加 `ask` 模式；`query` 继续负责确定性检索，`synthesize` 可以调用 RAG 生成 wiki draft，但必须进入原有的 source 检查、claim 映射、LLM 验证和 preview/apply 流程。

### 11.9 RAG 分阶段落地

```text
基线能力包：QMD 默认 read-only adapter + SQLite FTS5 fallback + deterministic LIKE fallback + QueryResult + 增量/全量重建 + 引用定位测试，一次性交付。
可插拔增强：Embedding/FAISS -> QMD/向量 Hybrid（RRF）增强 -> Reranker/回答缓存 -> 必要时评估 Qdrant/pgvector/GraphRAG；任何增强都不能移除 FTS5/LIKE fallback。
```

每个阶段都必须保留离线查询能力。LLM、Embedding 或向量索引不可用时，确定性查询仍可用；RAG 问答必须返回 `unavailable` 或明确降级，不能伪造“已基于文档回答”。

## 12. FastAPI 本地后端

核心 API：

~~~text
GET  /api/health
GET  /api/query?q=&scope=&vault_ids=&top_k=
GET  /api/read/{vault_id}/{object_type}/{object_id}
GET  /api/backlinks/{vault_id}/{object_type}/{object_id}
GET  /api/vault/check
POST /api/retrieve
POST /api/ask
POST /api/source/preview
POST /api/wiki/preview
POST /api/operation/{operation_id}/apply
POST /api/validate/{vault_id}/{object_type}/{object_id}
~~~

`POST /api/retrieve` 是结构化检索的唯一规范入口；`GET /api/query` 只是兼容别名，将 `q`/`vault_ids`/`top_k` 归一化为同一个 `RetrieveRequest`，必须返回同一 `query-result/v1`，不能出现独立排序、权限或 fallback 逻辑。请求只允许 `query`、`scope`、`vault_ids`、`top_k`、`include_sources`、`include_archive`；长度、数量、body 和 timeout 上限来自 `config/policy.yaml`，超限返回 `query_limit_exceeded`/`request_too_large`，不得静默截断。`projection` 不是权限 scope，`wiki` 不是合法别名。`POST /api/ask` 是独立生成能力，返回 `AskResult` 和 citations；没有 LLM/引用校验能力时返回 `unavailable`，不能把检索结果伪装成生成回答。

后端职责：

- 加载 local index；
- 建立 SQLite FTS5；
- 执行结构化查询；
- 返回 wiki 和 source 证据；
- 执行写入 preview/apply；
- 调用 LLM 验证器；
- Question/题目复习能力留给后续 F008；
- 当前只保存浏览器/本机阅读状态，不把它当作题目复习状态。

本地 API 的安全边界：默认只监听 `127.0.0.1`。任何写入、索引重建、验证调用和发布确认端点都要求本机启动时生成的 capability token，并校验 `Origin`/`Host`、请求体大小和 operation scope；token 存放在权限为 0600 的本机运行态或受保护环境变量中，不进入仓库、URL、浏览器存储和日志。缺少或错误 token 返回 `capability_token_required`/`capability_token_invalid`，不能因为“只有本机用户”而放行。只读 public 查询可以匿名访问；远程 bind、共享 Unix socket 和浏览器跨源写入必须由未来单独的安全决策启用。

技术选择：

| 能力 | 方案 | 选择原因 |
| --- | --- | --- |
| API | FastAPI | Python 工具链和结构化 schema 适配好 |
| 数据校验 | Pydantic + PyYAML | 复用 Python schema 能力 |
| 全文检索 | SQLite FTS5 | 无外部服务，适合个人知识库 |
| LLM 输出 | Skill provider adapter 的 structured output | 验证 schema 不绑定供应商，provider identity/capability 由运行时注入 |
| 复习 | 后续 F008 决定 | 当前版本不引入复习调度依赖 |

后端不是新的内容真相源。它启动时读取仓库文件和生成索引，写入时只通过 operation service 生成 staging 并原子应用；SQLite 只保存检索索引和可重建的本地 metadata，不能直接修改 source/wiki 正文。

### 12.1 离线降级

未启动后端时，Agent 和前端仍可通过查询工具读取 `var/queries/public` 或静态 catalog 完成离线查询。以下能力必须明确返回 `unavailable`，不能伪造成功：LLM 验证、写入 apply、后端 local index 和 F008 Question/复习。后端恢复后再重建 local index，不自动补写用户内容。

完全断网时的能力边界见 5.9：查询、阅读和图谱可用，网络 source 抓取和 LLM 验证不可用；`local-file` 与 `personal-note` 可以按 policy 写入。Question/复习不属于当前版本。不得为了让页面通过而放宽证据要求或跳过归档。

## 13. Astro 双运行模式

现有 Astro/Starlight POC 的输入适配、Pagefind/Cytoscape、staging、路由兼容和 leak gate 见 [Astro/Starlight 静态 Wiki 发布实现设计](./technical-design/static-wiki-publishing.md)；本节只保留系统级边界。当前 `legacy-validation` 构建仅用于迁移统计，正式 public build 必须使用 `var/queries/public/manifest.json`。

### 13.1 公开静态模式

- 只读取 public projection 中的 content/wiki/；
- 只包含 `public_publishable: true`；
- 只建立 wiki Pagefind 索引；
- 图谱只展示 wiki 节点；
- 正文中的本地链接只能解析到同一 public projection 的 manifest route 或已声明附件；根绝对路径、协议相对 URL、未声明 route 和危险 scheme 在 prepare 阶段阻断；
- 不展示 sources、题目答案、解析和验证报告；
- 无 FastAPI 时仍可正常浏览和搜索。

### 13.2 本地完整模式

- Astro 开发服务器代理 /api 到 FastAPI；
- 查询可以覆盖 sources、wiki 和本地 metadata；
- 页面可以查看 source 证据和验证状态；
- 首页提供查询、领域入口和最近阅读；复习入口留给后续 F008；
- 后端不可用时退化为公开 wiki 阅读模式。

### 13.3 Public leak gate

静态构建结束后必须扫描 dist/：

- 不得出现 content/sources/ 正文；
- 不得出现 content/practice/ 答案和解析；
- 不得出现 var/state/；
- 不得出现 ledger/archive/ 中的任何归档正文或原始文件；
- 不得出现 LLM 验证报告；
- 不得出现任何 `confidentiality: internal` 对象的 ID、标题、URL 和正文；
- 文章数量必须等于 `public_publishable: true` 的 wiki 数量；
- catalog、graph 和 Pagefind 数据只能来自 public wiki 投影。
- Pagefind 每个语言索引的 `page_count` 总和必须等于 public catalog；sitemap URL 集合必须恰好闭合为首页、图谱页和 public catalog routes。

保密分级的门禁不止在 dist/。本仓库是公开仓库，因此 internal 内容的第一道防线是"根本不写进来"：

- 页面校验工具 必须拒绝 `allow_public_projection: true` 的 vault 中任何 `confidentiality: internal` 文件；
- 提交前检查（`knowledge-check.yml` 与本地 pre-commit）扫描待提交文件，命中 internal 声明、内网域名模式或任一 private vault 路径即失败；
- 任一 private vault 的绝对路径不写入 public 仓库中的任何生成物，`var/queries/public` 不含任何 private 对象的存在性信息（连"有一篇 internal wiki"都不暴露）。

Public projection 不复制 source 正文、归档快照、题目答案、题目解析、验证报告、操作 manifest 和复习状态。归档副本是第三方内容的本地复制件，只用于个人复核，把它发布到公开站点等于重新发布他人内容，必须由 leak gate 硬拦。wiki 中的“证据映射”可以保留为引用信息，但只能包含 source ID/章节等 locator，不得把 source 正文内联到静态页面。构建前后都要执行一次 allowlist/denylist 扫描，避免模板或错误 import 把 local 数据带入 dist。

## 14. Agent Skill

Skill 位置（本仓库直接提供，Agent 从当前 checkout 加载）：

~~~text
skills/myknowledge/
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── page-schemas.md
│   ├── write-policy.md
│   ├── query-contract.md
│   └── workflow-modes.md
└── scripts/            # 仓库根检测与 Skill 调用入口
~~~

支持模式（当前版本）：

~~~text
query
read
ask
ingest
synthesize
index
audit
~~~

Skill 是 Agent 操作本仓库的官方受控入口。Skill 不实现第二套业务逻辑，而是调用 MyKnowledge 的领域 CLI/API；FastAPI 只是可选的本地 transport：

~~~text
myknowledge skill
  -> 查询工具
  -> 页面读取工具
  -> source 创建与导入工具
  -> wiki 创建工具
  -> 证据校验工具
  -> 索引生成工具
~~~

Skill 只负责：

- 发现 MyKnowledge 根目录；
- 自然语言模式路由；
- 调用 FastAPI 或离线 CLI；
- 强制 preview/apply；
- 传递 validation、evidence 和 limits；
- 把错误以结构化结果返回给 Agent。

Agent 不直接编辑 Markdown、manifest、queries、state 或 Git worktree；所有读写、preview、apply、发布和索引操作都必须经由该 Skill，再由领域工具执行 schema、证据、Vault 和确认门禁。

### 14.1 Agent 统一输出契约

所有 Skill 模式都返回相同的顶层字段，字段没有值时使用空数组、空对象或明确的 `null`，不省略字段：

```yaml
status: ok | preview | applied | rejected | blocked | error
operation_id: null
wiki: []
sources: []
claims: []
strength: null
evidence_state: null
validation_state: null
availability: null
availability_reason: null
publication_scope: null
publication_warning: null
public_release: false
vault_id: null
source_vault_ids: []
validation: {}
scope: null
method: null
degraded: false
warnings: []
error: null
diff: {}
changed_files: []
pending: []
next_gate: null
```

`strength` 是 6.7/6.8 定义的证据强度标识（`verified`、`corroborated`、`conflicted`、`partial`、`unresolved`、`attested`、`personal`、`reference`、`index`），查询和阅读结果都必须返回它，让 Agent 在引用知识库内容时能区分"已验证的外部事实"和"我的个人理解"。`evidence_state`、`validation_state`、`availability`/`availability_reason`、`publication_scope`、`publication_warning`、`public_release`、`vault_id` 和 `source_vault_ids` 用于表达多轴状态与 internal 告警；`method`/`degraded`/`warnings` 用于表达检索降级；`pending` 承载 `planned` 条目和待复核项。

查询和阅读操作的 `operation_id`、`diff`、`changed_files` 必须为空；写入 preview 必须包含 `operation_id`、`diff_sha256`、确定性校验和 LLM 校验结果。错误必须说明阻断规则和下一步动作，不能只返回自然语言错误。

写入模式的强制决策表（当前只列 Source/Wiki/Index；Question 行属于后续 F008）：

| 请求 | 无 source | 有 source 但验证失败 | 验证通过未确认 | 同 operation_id 且 hash 未变 |
| --- | --- | --- | --- | --- |
| ingest source | 允许创建 source preview | 不适用 | 等待确认 | 允许 apply |
| synthesize wiki | 拒绝，先提示创建 source | 保持 draft | 等待用户确认 | 允许 apply |
| index | 只允许调用生成器 | public 生成只接受 `vault_id: public` 且跳过未发布和 internal；private/local 生成保留全部可用 vault、owner 和告警 | 不适用 | 允许生成 |

写入 preview 的结果中必须回传 `confidentiality`、有效等级的来源（自身声明还是上游传染）和明确的 `target_vault`，让用户在确认前就能看到这次写入会落到哪个 vault。保密等级只能约束可选范围，不能替代目标选择；当存在多个等级足够的 private vault 时，用户或调用方必须显式选择稳定 `vault_id`，Agent 不能自选物理路径或默认使用某个名字。

Skill 不根据对话上下文猜测用户确认范围；“确认”必须能解析为当前 `operation_id`。用户修改 source 或 wiki 后，旧 operation 自动失效，必须重新 preview。

## 15. 工具模块边界

~~~text
tools/（按职责划分模块；文件命名是实现细节，不构成契约）
├── 共享基础：hash、canonical JSON、front matter、原子写、Vault 锁
├── Source 导入与归档：抓取、local-file/personal-note 导入、正文提取、snapshot 与 manifest
├── Evidence 锚定：selector/hash 生成与写回
├── 校验：请求/已发布文件 schema、页面、证据与引用校验
├── 查询与读取：页面读取、检索、重排、带引用回答
├── 发布：wiki 创建/重命名/退役、索引生成
└── 存量迁移：inventory 生成与任务清单
~~~

建议职责：

- 共享基础：root、vault 挂载、路径安全、front matter、hash 和页面读取；
- Source 导入与归档：source 模板、抓取、`local-file` 导入（`--from-file`）、正文提取、压缩、内容寻址写入、preview/apply 和 manifest 维护；
- Evidence 锚定：从已归档 snapshot 交互式选取引文，生成 `TextQuoteSelector`/`TextPositionSelector`（Unicode code-point 半开区间）、`selector_sha256` 和 `quote_sha256`，写回 source 的 `evidence_items`。这是 §5.1 evidence item 与 §6.4 claim target 的唯一落地入口；没有它，claim 只能手写 offset，全部迁移工作量无法开始。详见 [证据锚定实现设计](./technical-design/evidence-anchoring.md)；
- wiki 生命周期：source 检查、claim/evidence、preview/apply、ID/路径变更与引用同步、route map 和原子回滚、`retire`/`purge` 前置检查；
- 校验：确定性 schema、引用、链接、状态组合和保密分级校验；LLM adapter、结构化输出、引文逐字校验和报告；
- 来源巡检：外部链接巡检、归档快照更新和漂移标记；
- 索引与检索：public/local 索引原子生成；规范化分块、Embedding 和本地向量索引；FTS、向量和混合召回；可选候选重排；
- 回答与引用：基于检索片段生成带引用的回答；检查回答和 claim 是否能定位到 source locator，并校验 evidence target 的 snapshot/selector；
- 存量迁移：按固定 classifier/threshold 生成带输入 tree hash 的存量迁移 inventory；不改写内容、不推断事实正确性；
- 离线查询：统一 `QueryResult` 契约；
- 任务清单：记录操作范围、输入 hash、结果和失败阶段。

所有公共入口只能委托这些领域工具，不能在 CLI、FastAPI 和 Skill 中重复实现规则。外部 Skill 集合不是运行时依赖；如需同步到其他 Skill 仓库，只能由独立发布流程打包，不能改变本仓库的 canonical Skill。

### 15.1 开发要求

- **面向对象**：有状态与生命周期对象（锁、仓库、服务、提取器）使用类；无状态纯函数保留模块函数形式，不为"类化"而类化。
- **高内聚**：一个类一个职责，变更原因唯一；一个文件一个主类，私有辅助类/函数留在宿主文件内；禁止"工具杂物间"式模块持续膨胀。
- **低耦合**：依赖方向单向且无环（共享基础 → 领域服务 → CLI 入口）；服务依赖经构造函数注入，不在方法内直接实例化其他服务；禁止循环导入。
- **设计模式原则（SOLID）**：
  - 单一职责：一个类只承担一种职责；
  - 开闭原则：类型分派（source 类型、media 类型、提取器、校验器）使用注册表/策略扩展，新增类型通过注册新策略实现，不得修改已有类；
  - 里氏替换：继承标准库类（连接、解析器）必须保持父类语义契约；
  - 接口隔离：类只暴露调用方需要的方法，不为未使用能力定义接口；
  - 依赖倒置：服务依赖抽象（Protocol/抽象基类）而非具体实现，依赖经构造函数注入。
- **文件命名是实现细节**：不构成契约，总纲领不绑定文件名；technical-design 对已实现部分使用实际文件名。
- **可检查性**：上述条目纳入 code review 对照清单；重构不得改变对外契约（CLI 命令、错误码、审计格式、manifest schema）。

当前运行时工具集合不包含题目创建工具、题目读取器、quiz/review API 或 FSRS 状态处理器。F008 的工具目录和接口在 `docs/deferred/` 单独设计并通过独立 Feature 接入；在 F008 启动前，任何实现、Skill 或验收脚本都不得创建或解析 `Question`/`content/practice/` 题目对象。

## 16. 迁移策略

当前 docs/ 下 277 个 Markdown 文件不能直接批量标记为 published，因为它们没有 source、claim 映射和 LLM 验证。但"277 篇文章"并不是实际迁移量——实测的形态分布决定了绝大多数文件根本不走完整证据链。

### 16.1 存量形态分析（历史快照）

下面的形态分布来自早期迁移分析快照，不是当前运行时 inventory 的事实源。由于当时的分类脚本、阈值和输入提交没有作为工具/manifest 入库，表中的细分数字不得直接用来宣称当前迁移量；每次迁移必须重新生成带工具版本、输入 tree hash 和分类规则 hash 的 inventory。当前可复现的仓库基线只有第 2.1 节列出的 `277` 个输入 Markdown、`276` 篇 legacy 内容文章、`224` 条显式关系和 `19` 条未解析链接。

| 形态（旧分类规则） | 文件数（历史快照） | 字符量（历史快照） | 迁移去向 |
| --- | --- | --- | --- |
| 空文件（0 字节） | 16 | 0 | `status: planned` 或删除 |
| 导航页（`contents.md`） | 71 | 20809 | `kind: index`，按 6.7 分档 |
| 占位 stub（正文 ≤200 字） | 54 | 9886 | `status: planned` 待写清单 |
| 短笔记（201-800 字） | 45 | 38575 | 完整链路，成本较低 |
| 实质文章（>800 字） | 78 | 297663 | 完整链路，主要成本 |
| 资源链接清单 | 1 | 2891 | `kind: reference` |
| 超大聚合页（需先拆分） | 12 | 233251 | 先按 5.7 抽象层级拆分，再入链路 |

真正承载内容的是实质文章与超大聚合页共 90 个文件，占全库字符量的 88%；141 个文件（空文件、导航页、占位 stub）没有可迁移的正文。

出处线索的历史结论：只有 59/277 个文件含任何外链，实质文章中 48/78 篇完全没有 URL；git 历史是一次性批量导入（18 个 commit，全部文件同期首次提交），无法提供逐篇来源线索。该结论也必须在正式迁移 inventory 中重新计算。因此**无出处内容的处理方式是迁移的主要工作量和主要风险**，不是技术实现。

迁移 inventory 至少记录 `input_tree_sha256`、`classifier_version`、`thresholds`、`legacy_path`、`body_sha256`、`shape`、`provenance`、`content_verdict` 和生成时间；没有这些字段的旧表只能作背景参考，不能作为完成率分母。

### 16.2 迁移清单

先为每篇旧文档生成：

~~~yaml
legacy_path:
candidate_id:
domain:
title:
shape:            # empty | index | stub | short-note | article | reference | oversized
likely_origin:
provenance:       # has-url | recoverable | none
content_verdict:  # keep | downgrade | retire | pending-review
route:
link_dependencies:
migration_status:
~~~

`content_verdict` 是迁移的核心判断，必须逐篇人工确认，不允许工具推断：

- keep：内容仍然正确，按正常链路建 source 与 claim；
- downgrade：内容可用但找不回出处，降级为 personal source，并按 6.5 改写为个人语气；若属于语言标准或公开规范，改用 `evidence_status: common-knowledge` 并补权威入口，避免把公认事实写成个人观点；
- retire：内容错误或已过时，按 9.6 走 `retire`，不进 public build；
- pending-review：暂时判不准，保持 `draft` 或 `planned`，进待复核清单。

### 16.3 Source 归类

- 有外部 URL、书籍或明确出处：建立 external source；
- 原链接已失效但手上有离线副本：按 5.6.1 导入副本并归档，URL 保留为历史出处；
- 能找到本地原文（代码库、PDF、离线文档）：优先建立 `source_type: local-file`，原件完整可重复读取、版本可由 hash 校验，见 5.8；
- 明确是个人总结、笔记或实验：建立 personal source；
- 属于语言标准、公开规范或教科书级事实：`evidence_status: common-knowledge` 并给出权威入口；
- 无法判断来源：`content_verdict: pending-review`，不自动发布。

### 16.4 Wiki 迁移

- 旧文章迁移为 wiki draft，标题清单和空文件迁移为 `status: planned`；
- 超大聚合页先按抽象层级拆分，再逐单元进入链路；
- 生成初始 source 引用和 claim 候选；
- 运行确定性校验，按 6.7 判断是否需要 LLM 验证；
- 通过后由用户确认发布；
- 保留旧路径到新 ID 的 route map；
- 处理特殊字符、重复路由和未解析链接。

`docs/<domain>/` 是 `content/working/` 的临时前身，只承担一次性迁移队列的职责，因此不参与 §4.6 的路径搬移（它的 `legacy_path` 已记入迁移台账，搬移需要改写全部台账条目而收益为零）。**退役条件**：当迁移 inventory 中不存在 `migration_status` 未终结的条目、且 `docs/` 下不再存在任何 `<domain>/` 子目录时，从 `policy.yaml` 的路径声明中移除该目录并删除它。此后新的未定稿内容一律进入 `content/working/`，受 §4.5 的 TTL 约束。

迁移顺序建议：

~~~text
computer-science
-> tools
-> work-methods
-> multimedia
-> reading-notes
~~~

在迁移完成前，不切换正式站点到 wiki-only，避免现有公开内容一次性消失。切换完成后，旧 docs/ 不再作为第二份维护源。

## 17. 测试和门禁

### 17.1 Deterministic tests

- YAML 和 Front Matter 解析；
- 必填字段和枚举；
- ID 唯一性；
- source ID 存在性；
- source locator 存在性；
- personal/external 支持类型兼容性；
- （F008 延后）题目类型、选项数量和判分规则不属于当前测试集；
- source 正文和章节超过阻断阈值时必须被拒绝并返回拆分建议；
- `local-file` source 缺少 sidecar path 或 file_sha256 必须失败；
- `local-file` 路径无法解析时标记 unresolved，不得判定为证据缺失；
- 每档证据要求必须命中对应的替代检查，不得同时免除确定性校验；
- `planned` 页面不得出现在 public build 和 RAG 索引中；
- `deprecated` 页面不得被新 claim 引用；
- `purge` 在存在引用时必须被阻断；
- `rename` 必须同步全部引用、backlinks 和 route map，任一失败整体回滚；
- 旧 ID 不得被复用；
- 并发 apply 必须被写锁串行化，不得出现静默覆盖；
- status 转换的每个非法组合都必须被拒绝；
- 派生字段被手写时必须以工具计算结果覆盖；
- `supporting_quotes.exact` 不能逐字匹配到 target 指向的 snapshot selector 范围时必须判 unsupported；
- 增量索引结果必须与全量重建结果一致；
- 归档正文缺失时 `common-knowledge` 必须校验失败；
- `common-knowledge` 的 `supporting_quotes.exact` 无法逐字匹配归档正文时必须失败；
- 转载链、同一 publisher 或同一实验数据的多个 source 不得被误判为独立 corroboration；independence_group 不明确时按单一 source 处理；
- 多 source 冲突必须保留冲突 target、版本窗口和人工决策入口，不能用多数票自动清除；
- `ledger/archive/raw/` 在 LFS 规则未配置时必须拒绝写入并降级为 text-only；
- 无来源的 source 写入必须被拒绝（三种完备形态之一都不满足）；
- `require_network` 生效且离线时，只有 acquisition 为 `fetch` 或明确需要网络 provider 的 apply 才能被拒绝；`local-file`、`personal-note` 以及引用已有本地证据的 draft 写入按 allowlist 可离线完成，且不得留下伪造的网络检查结果；
- `metadata-only` source 缺少入口页归档时必须失败；
- `local-file` 缺少 `file_sha256`、sidecar path 或归档正文时必须失败；`copy_note` 仅在需要补充副本来源说明时记录，不作为绕过证据完备性的替代字段；
- `url_status: dead` 不得触发可达性检查失败，也不得阻断已有页面发布；
- 引文规范化：全角半角、中英文空格、Markdown 行内标记、零宽字符的等价性用例；
- 引文短于 `quote_min_chars` 必须失败；
- 引文出现在其他章节而非被引 locator 时必须失败；
- （F008 后续）题目 claim_ids 必须命中 wiki evidence；
- （F008 后续）引用 draft wiki 的题目必须被拒绝；
- （F008 后续）wiki 正文或 evidence 变化后题目自动 `enabled: false`；
- 任一允许 public projection 的 vault 中出现 internal 声明必须失败；
- 内网 URL 声明为 public 必须失败；
- wiki 引用 internal source 时有效等级必须升级；它可以在 owner private Vault 内经 `operation-confirmation/v1`（`scope: publish_private` + 告警确认字段）后以 `status: published`、`publication_scope: private` 发布，但不得进入 public projection；对外发布必须另建 public-owned 脱敏 copy 并重新校验；
- 任一 private vault 未挂载时不得把该 vault 的 internal 引用误判为 source 缺失，且其他 vault 仍可查询；
- 两个或更多 private vault 同时挂载时必须保留各自 `vault_id`；同一 Vault 内的 object ID 冲突必须阻断，不同 Vault 的同名对象保持独立；完全相同的 snapshot hash 可以去重但不能丢 owner；
- private-to-private 和 public-to-private 跨 Vault 内容引用必须在写入/校验阶段拒绝，并记录 source/target `vault_id`；public release 的 `source_vault_ids` 仅表示 lineage，不是内容引用许可；
- 每个 vault 的 remote/backup 未配置必须独立告警；涉及未验证 vault 的 purge/覆盖式恢复必须阻断；
- 只修改 tags/aliases/related 不得使验证报告失效；
- 修改 source 中未被引用的章节不得使已验证 wiki 失效；
- 修改被引用章节必须精确失效对应 claim；
- 路径穿越和 symlink 拒绝；
- operation hash 失效；
- staging 失败回滚；
- queries 生成物一致性；
- chunk 必须带 object_id、source_ref 和 content hash；
- RAG 召回结果必须能定位到 source/wiki；
- RAG 不可用时确定性查询仍可用。

### 17.2 LLM validation tests

使用固定 fixture 和 mock structured-output adapter 测试：

- 全部 supported；
- partially supported；
- unsupported；
- contradicted；
- unmapped；
- malformed JSON；
- provider 不可用；
- source hash 变化；
- wiki hash 变化；
- 引用缺失、locator 不存在和回答超出检索片段；
- LLM 覆盖不全、只给 advisory 不给 verdict、rationale 无原文引用区间，均须落到 `not_run: incomplete_coverage`；
- 模型自行声明 `not_run` 必须被拒绝。

真实 LLM 调用只作为集成测试，不作为离线单元测试依赖。

### 17.3 Skill tests

- query/read 不调用 writer；
- 无 source 的 synthesize 被拒绝；
- preview 不修改工作树；
- 未确认的 operation 不能 apply；
- hash 变化后 operation 失效；
- FastAPI 和离线 CLI 返回相同 QueryResult；
- Skill 不直接编辑 Markdown 和 queries；
- skill-creator quick_validate.py 通过。

### 17.4 Public build tests

- public 页面数量等于 `public_publishable: true` 的 wiki 数量；
- draft/review、conflicted、internal 页面不进入构建；
- internal 对象的 ID、标题、URL 和正文都不出现在 dist；
- source 不进入 dist；
- practice 答案和解析不进入 dist；
- graph、catalog 和 Pagefind 只来自 wiki；
- 无后端时首页、搜索、文章和图谱可用。

### 17.5 失败恢复矩阵

| 失败点 | 工作树结果 | 用户可见结果 | 恢复动作 |
| --- | --- | --- | --- |
| source schema 校验失败 | 不写入 | 返回缺失字段和修复建议 | 修改 source preview |
| wiki 无 source 或 locator | 不写入 | blocked，列出缺证据 claim | 补 source 或改写 claim |
| LLM 不可用/格式错误 | 不影响确定性校验结果；允许保存带 provenance 的 draft candidate | source 可用，`validation_state: not_run` 并附原因，人工审计通道仍可推进 | 可选：provider 恢复后重跑审计 |
| hash 变化 | 不写入目标 | operation expired | 重新 preview |
| F008 题目引用的 claim 变化或被删除 | 题目文件保留 | 由 F008 规则标记失效 | F008 重新出题或改绑 claim |
| 允许 public projection 的 vault 中出现 internal 声明 | 不写入 | blocked，提示改用 private vault | 将对象写入明确选择的 private vault 后重做 |
| 外部原文变化或链接失效 | 不改内容 | source_drift / link_rot 提示 | 人工决定是否重读修订 |
| staging 或索引失败 | 旧页面和旧索引保持不变 | apply failed | 清理 staging，修复后重试 |
| public leak gate 失败 | 不发布 dist | build blocked | 找出泄漏字段并修复投影 |

### 17.6 可观测性和审计

每次 query、preview、apply、validate、index 和 publish 操作记录结构化事件：`operation_id`、模式、输入 hash、目标 ID、Vault ID、状态、失败阶段和耗时。运行日志只保存必要的诊断信息，source 正文、API key、Authorization header 和用户隐私字段不得写入日志。临时日志和派生索引可以清理或重建；已被确认、审计、恢复和 purge 引用的 durable audit/event record 必须按 append-only 规则保留，若做分卷/归档只能连同 manifest 和恢复索引迁移，并保留对应 Git 历史，不能删除或改写后再声称当前校验有效。

## 18. 实施阶段

### 阶段零：垂直切片

在按模块铺开之前，先让 1 个 source → 1 个 wiki → 1 条 claim → 1 个 published page 真正跑通全部阻断门：归档 snapshot、`evidence_anchor` 生成 selector、确定性引文逐字匹配、人工审计确认、projection、leak gate、Astro 构建。

退出门是可观测的单一事实：**这一页真的出现在 `dist/` 里**，且删掉它的引文一个字符后构建会失败。

阶段零不引入任何临时实现：它使用的就是各模块的正式接口，只是覆盖面收窄到一条链路。它的作用是在铺开前证伪设计——如果这一页跑不通，后面六个阶段的方向都要重议。

### 阶段一：规范基础

- 创建 schema、词表、policy 和三类模板；
- 定义 `config/vaults.example.yaml`、被忽略的 `config/vaults.local.yaml` 与保密分级校验；
- 实现 6.6 的 hash 契约（正文 hash、evidence hash、locator hash）；
- 实现 Front Matter、路径安全和页面读取；
- 实现 source/wiki 确定性校验和 9.5 写入准入表；Question 校验留给 F008。

### 阶段二：受控写入

- 实现 operation preview/apply；
- 实现 before hash、diff hash 和原子写入；
- 实现逐 Vault 排他锁、fencing token 与陈旧锁人工恢复；
- 实现归档抓取、正文提取、压缩与内容寻址存储；
- 实现 rename/move 与 retire/purge 操作；
- 实现失败清理和回滚；
- 禁止直接文件写入。

### 阶段三：LLM 规范审计

- 实现 Skill provider adapter（协议可由运行时兼容 OpenAI，但不固化具体 endpoint/model/key）；
- 实现按 `rule_refs` 组装规则集与 `ruleset_sha256`；
- 实现 claim 逐条审计、`applied_rule_refs` 回引与原文区间举证；
- 实现覆盖义务校验：覆盖不全、只给 advisory、rationale 无引用区间一律落 `not_run: incomplete_coverage`；
- 保存 append-only 审计报告与内容 hash 绑定；
- 没有 provider 时落 `not_run` 并保持人工审计通道可用。

### 阶段四：索引和后端

- 生成 public/local 两套索引；
- 接入 SQLite FTS5；
- 实现 FastAPI query/read/source/backlink API；
- 生成 public/local index 和 QueryResult；题库/复习留给 F008；
- 一次性交付默认 `QmdRetriever`、`FtsRetriever` fallback、deterministic LIKE fallback、QueryResult 和索引重建；Embedding/FAISS/Hybrid/Reranker 作为可插拔 adapter，不改变基线契约；
- 实现 `/api/retrieve`、`/api/ask` 及引用定位校验；
- RAG 不可用时保留确定性查询，并明确返回降级状态。

### 阶段五：静态前端

- 将 Astro 输入切换为 `public_publishable` projection；
- 增加 public leak gate；
- 保留静态搜索和 wiki 图谱；
- 增加本地 API 检测和降级。

### 阶段六：Agent Skill

- 创建 skills/myknowledge；
- 接入 CLI/API 双路由；
- 固化 source-first、LLM gate、preview/apply；
- 更新 skill 清单和安装流程。

### 阶段七：内容迁移

- 建立旧文档迁移清单；
- 按领域创建 source 和 wiki draft；
- 逐页完成 claim、LLM 验证和发布；
- 完成 route map 和链接修复；
- 最后切换正式 public 构建。

### 18.1 阶段依赖和退出门

| 阶段 | 依赖 | 主要产物 | 退出门 |
| --- | --- | --- | --- |
| 垂直切片 | 无 | 1 source + 1 wiki + 1 claim + 1 published page | 该页出现在 dist；改动引文一个字符后构建失败 |
| 规范基础 | 无 | schema、词表、模板、validator fixtures | 非法页面全部能被拒绝 |
| 受控写入 | 规范基础 | operation service、manifest、staging | preview 不改工作树，apply 可回滚 |
| LLM 规范审计 | 受控写入 | adapter、结构化 report、覆盖义务校验 | provider 不可用时落 `not_run` 而非 `fail`，且不阻断人工审计通道 |
| 索引和后端 | 规范基础 | public/local index、SQLite、FastAPI | CLI/API QueryResult 一致 |
| 静态前端 | public projection | wiki-only build、leak gate、旧 dist 保留 | dist 只含 `public_publishable` wiki |
| Agent Skill | 受控写入、查询 API | `myknowledge` skill | Agent 不能绕过 writer 和 validator |
| 内容迁移 | 前六阶段 | source、wiki、route map | 每个迁移项都有证据和明确 completed/pending 状态 |

阶段之间不允许以“代码已合入”代替退出门；只有对应的测试、报告或人工确认记录齐全，阶段才算完成。

这里的阶段表示模块依赖和验收顺序。阶段零是唯一允许收窄覆盖面的阶段，它用的是正式接口而不是临时实现。除阶段零外，F007 静态 Wiki 和 F011 Private Vault 各自必须以完整能力包交付：正式接口、fallback、保密门禁、失败恢复、可观测性和验收场景在同一交付中闭合；后续只允许通过兼容 adapter 增加能力。

## 19. 完成标准

系统完成必须同时满足：

- source、wiki 都有统一 schema 和模板；Question schema 留给 F008；
- 无 source 不能写 `kind: knowledge` wiki；F008 的题目门禁不影响当前主链路；
- `kind: knowledge` wiki 必须有 claim-level evidence；Question 的 claim 绑定留给 F008；
- `public_publishable` 或 `private_publishable` wiki 必须有绑定当前 `(content_sha256, evidence_sha256)` 的人工审计确认，且 `validation_state != fail`；
- public `published` 必须有当前输出 hash 绑定的人工 `public_release: true`、操作者和 public confirmation；默认值为 `false`，hash 变化后回到 `false`；
- 每个页面对读者可见自己的证据强度；
- 每个网络来源都有明确出处和本地归档快照；
- 内容 hash 只覆盖正文和语义字段，分类字段变更不触发重验；
- internal 内容不进入公开仓库和公开构建；
- LLM 不可用不阻断发布，但 `validation_state: not_run` 必须对读者可见，且不得表述为已验证；LLM 审计一旦运行则必须全覆盖并逐条回引规则条目，`fail` 阻断发布；
- public 构建只包含 `public_publishable` wiki，private 构建显式显示 internal warning；
- 每个 private vault 的 Git remote/加密备份未配置时必须显示带 `vault_id` 的 `backup_not_configured`，不能声称恢复链路就绪；只有该 vault 配置后并完成自己的备份和恢复演练才可标记 `verified`；
- local 后端可查询 source、wiki；
- Question/复习不属于当前版本完成标准；F008 后续单独设计单选题、多选题和面向面试的简答题；
- Agent Skill 支持 query/read、ask、source、wiki、publish、index、audit 等模式（归并为查询、写入、发布、索引四类能力），写入不可绕过规范；
- preview/apply 可追踪、可失效、可回滚；
- 旧内容迁移有清单、route map 和明确的 completed/pending 边界。

完成标准按三类证据验收：

| 类别 | 可接受证据 | 不可替代的证据 |
| --- | --- | --- |
| 静态/代码 | 单元测试、schema 报告、构建日志 | 不能代替真实 LLM 或内容正确性 |
| 运行能力 | FastAPI smoke、查询/阅读端到端测试 | 不能声称已经完成内容迁移 |
| 内容质量 | source locator 展示信息、snapshot/evidence binding、claim 验证报告、人工确认记录 | 不能用搜索摘要或模型自信度代替 |

最终知识生产链为：

~~~text
source 先行
  -> source 校验
  -> wiki 候选
  -> claim 显式映射
  -> LLM 证据验证
  -> 用户确认
  -> 原子写入
  -> 自动索引
  -> public/private published projection
  -> 静态展示 / 本地查询 / Agent 查询
~~~

## 20. 参考实现和对标

- [Quartz authoring content](https://github.com/jackyzha0/quartz/blob/v4/docs/authoring%20content.md)：Markdown、Front Matter、别名和内容发布。
- [Quartz graph view](https://github.com/jackyzha0/quartz/blob/v4/docs/features/graph%20view.md)：本地图谱和全局图谱。
- [Quartz backlinks](https://github.com/jackyzha0/quartz/blob/v4/docs/features/backlinks.md)：反向链接导航。
- [Dendron](https://github.com/dendronhq/dendron/blob/master/README.md)：渐进结构、模板、Git vault 和链接重构。
- [Logseq Markdown Syntax](https://github.com/logseq/logseq/blob/master/docs/logseq-markdown-syntax.md)：属性、引用、块和任务语义。
- [FSRS](https://github.com/open-spaced-repetition/free-spaced-repetition-scheduler/blob/main/README.md)：作为 F008 的候选本地间隔复习调度；当前版本不引入或依赖它。
- kernelwiki-kunlun：source-first、证据边界、schema、任务 manifest、索引生成和 fail-closed 校验。

### 20.1 对标后的取舍

| 方案 | 借鉴 | 不直接采用的部分 | MyKnowledge 决策 |
| --- | --- | --- | --- |
| MkDocs Material（当前） | Markdown、成熟主题、低成本静态发布 | 内容源与发布状态耦合，难以表达 source/wiki 双投影 | 迁移期间保留作为回退，正式 public 层以 wiki-only Astro 构建为目标 |
| Astro/Starlight（现有 POC） | 内容集合、Pagefind、组件化阅读界面 | 需要构建期 content adapter 和 public leak gate | 继续作为静态展示层，不承担写入和证据判断 |
| Quartz | Markdown + Git、backlinks、graph、静态发布 | 没有 source/claim 发布门禁 | 保留静态展示思想，增加 evidence gate |
| Dendron | 层级命名、模板、批量重构 | 生态已较少维护，写入规则不够严格 | 只借鉴模板和渐进迁移 |
| Logseq | 属性、引用和双向链接 | block-first 数据模型会增加迁移复杂度 | 继续 page-first Markdown |
| Obsidian | 本地文件、插件和图谱体验 | 插件可直接改文件，难以形成硬门禁 | 不把插件作为写入真相源 |
| Anki/FSRS | 复习调度和导入导出 | 不负责知识证据和内容管理 | 留作 F008 评估候选；当前不实现 question review state |
| kernelwiki-kunlun | fail-closed、manifest、证据边界 | 其领域词表和运行环境不适合 MyKnowledge | 复用流程思想，重新定义领域 schema |

因此，第一阶段的核心不是增加更多 AI 功能，而是先把“可追溯写入”和“不可绕过发布门禁”做成确定性基础。语义检索、自动摘要和更复杂题型都必须作为后续消费者接入，不能改变 source -> evidence -> wiki 的主链路。

### 20.2 组件级实现对标（2026-08-26 核查）

以下不是“看到项目名就采用”，而是把可复用的稳定边界和不能交给第三方的职责分开：

| 能力 | 现成实现与具体细节 | 优点 | 限制/风险 | MyKnowledge 取舍 |
| --- | --- | --- | --- | --- |
| 文本证据锚定 | [W3C Web Annotation](https://www.w3.org/TR/annotation-model/) 的 `TextQuoteSelector` + `TextPositionSelector`；[Hypothesis quote matching](https://github.com/hypothesis/client/blob/main/src/annotator/anchoring/match-quote.ts) 使用 exact/approx quote、prefix/suffix 和 position scoring | 标准化、可跨渲染层恢复、已有近似匹配经验 | 近似匹配可能误锚；网页改版会造成漂移 | 采用 W3C 字段；exact + snapshot hash 是 blocking gate，Hypothesis 式近似只生成恢复建议 |
| HTML/正文提取 | [Trafilatura](https://github.com/adbar/trafilatura) `2.2.0`：HTML 主文、metadata、Markdown/JSON/TXT；[Docling](https://github.com/docling-project/docling) `2.122.0`：PDF/Office/HTML/OCR、版面和页级 provenance | 现成解析器覆盖常见来源，减少自研解析 | 抽取器升级会改变文本和 offset；复杂 PDF/OCR 仍需人工抽查 | source ingestion 通过 adapter 调用；manifest 固定 extractor/version/options hash，升级生成新 snapshot，不覆盖旧证据 |
| 网页归档 | [ArchiveBox](https://github.com/ArchiveBox/ArchiveBox#readme) 提供 CLI/Web/Python API 和多格式归档 | 归档格式广、导入方便 | 默认配置可能触发 archive.org，不能把第三方快照当内部 canonical store；输出结构需再校验 | 只借鉴归档任务思想；canonical 仍是本地内容寻址 `ledger/archive/text`，internal 禁止外发 |
| 关键词检索 | [SQLite FTS5](https://www.sqlite.org/fts5.html) 的 BM25、highlight、snippet、tokenizer | 内置、离线、确定性、可重建 | 中文 tokenizer 和 external-content 同步由应用负责 | 必选 baseline；维护 object/hash metadata 和 Python fallback |
| 混合检索 | [QMD](https://github.com/tobi/qmd) / [npm `@tobilu/qmd`](https://www.npmjs.com/package/@tobilu/qmd) `2.8.3`：BM25、向量、RRF、LLM rerank、CJK normalization、hash 增量、行号读取和 MCP | 一次获得较完整的本地语义检索能力 | Node `>=22`、模型/索引缓存、版本和输出 schema 会扩大运行面 | 默认本地 read-only adapter；所有结果回到 canonical projection 校验；不可用回退 FTS5/LIKE，不决定状态；public build 不依赖 |
| 静态搜索 | [Pagefind multilingual](https://pagefind.app/docs/multilingual/) 按 HTML `lang` 分段索引 | 构建期静态、无需后端、适合 GitHub Pages | 中文分词/混合 token 必须回归；索引只看最终 HTML | 保留现有 Pagefind，加入 zh-CN fixture 和 search degraded 规则 |
| Agent 接口 | [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) `2.1.1`，Python `>=3.10`，支持 stdio/Streamable HTTP/SSE | 现成协议和 transport，便于接 Skill/工具 | 不拥有 MyKnowledge 权限和状态语义；协议升级需锁版本 | MCP 只做 adapter，调用领域 CLI/API；不允许直接写 Markdown 或发布 |
| 复习调度（F008 候选） | [FSRS](https://pypi.org/project/fsrs/)（版本待 F008 评估时锁定） | 现成调度算法和 Python API | 不负责题目证据、内容 hash 或隐私边界；当前版本不依赖 | F008 再决定是否采用；题目门禁和本地 state 仍由 MyKnowledge 管理 |

这些组件都遵循同一条边界：成熟库负责解析、索引、协议或调度；source snapshot、evidence binding、状态计算、保密传染、publish operation 和 leak gate 必须由 MyKnowledge 自己掌握。这样可以尽量少写代码，又不会把事实真相或安全门禁交给不可审计的外部默认行为。

## 21. 规范 ID 基线

本文是系统规范的唯一事实源。下游 Feature、Technical Design、Acceptance 和追踪矩阵使用稳定 ID 引用约束；章节移动不改变 ID。

| 前缀 | 范围 | 主要章节 |
| --- | --- | --- |
| SYS | 系统目标、不变量和边界 | §1–§3、§19 |
| LAY | 目录分域、五层归属、写入通道与路径迁移 | §4.4–§4.6 |
| SRC | Source 契约、来源和写入要求 | §5 |
| ARC | 原文快照、归档和来源漂移 | §4.3、§5.6 |
| WIKI | Wiki schema、状态和正文契约 | §6 |
| EVD | Claim、Evidence 和引文 | §6.4、§6.9 |
| VAL | 确定性校验、LLM 验证和报告失效 | §8 |
| OPS | Preview/Apply、幂等、锁和对象操作 | §9 |
| IDX | 索引、检索和 RAG 边界 | §11 |
| API | FastAPI 本地后端 | §12 |
| WEB | Astro 公开静态模式 | §13 |
| QST | Question 和复习（F008 延后） | §7 |
| SKILL | Agent Skill 受控入口及工具边界 | §14–§15 |
| MIG | 迁移、发布和回滚 | §16–§18 |
| SEC | confidentiality、Vault 和公开泄漏门禁 | §4.2、§13.3 |

当前 P0 规范编号：

- `SRC-001`：每个 Source 必须满足一种来源完备性通道。
- `SRC-002`：`source_type` 只允许新增取值，不允许重命名或删除既有取值（它位于 `hash_inputs.source_semantic`，改名会触发全库重验）；口头与私聊材料不得新增独立来源类型。
- `LAY-001`：数据侧只有 `content/`、`ledger/`、`var/` 三个域，新增目录必须按 §4.4 的五条判据归入其中之一；组件目录平铺在仓库根。
- `LAY-002`：managed 层（`content/sources/`、`content/wiki/`）必须 per-vault；unmanaged 层（`working/`、`journal/`、`decisions/`）无 object 身份，只需单例，且不得进入 projection、leak gate 输入树、operation hash 集合与 `query-result/v1`。
- `LAY-003`：`content/working/` 到期只产生 `doctor` 报告，工具不得自动删除内容；进入该层的唯一硬约束是 `source_ref` 或 `legacy_path` 非空。
- `LAY-004`：目录迁移不得重写历史 durable record；`applied_files` 中的历史路径是事实，读取侧必须容忍历史路径形态。
- `CHN-001`：`content/working/` 的唯一入口约束是 `source_ref` 或 `legacy_path` 非空；该层不产生 wiki 对象，不得进入任何 projection、不得出现在任何 wiki 的 `evidence.targets`、不得进入 RAG 召回。存量误登记为 source 的加工文档整批降级至该层（一次降级一条 CDR），`content/wiki/` 只能逐篇人工升级进入，不存在批量升级路径。
- `WIKI-003`：`review_by` 是选填的报告项：不进 content hash、不改变任何 `*_state` 或 `status`，到期只出现在 `doctor` 清单中。
- `ARC-005`：ASR 派生 snapshot 支撑的 claim 强度上限为 `attested`，不得派生 `verified`；解除上限需人工逐字校对该片段并标注。
- `ARC-001`：网络来源必须保存可复核的本地文本快照。
- `ARC-002`：权威证据必须绑定不可变 snapshot、TextQuote/TextPosition selector 和 hash；source locator 仅用于阅读导航。
- `WIKI-001`：知识型 Wiki 必须符合 schema、状态和正文契约。
- `EVD-001`：知识型 Wiki 的可验证 Claim 必须显式映射 Evidence。
- `VAL-001`：`supporting_quotes.exact` 必须在 target 指定的 snapshot selector 范围内逐字匹配。
- `OPS-001`：所有写操作必须经过 Preview、用户确认和 Apply。
- `IDX-002`：本地自然语言/混合检索默认使用 QMD；SQLite FTS5 是必选确定性 fallback，QMD/FTS5 不可用时再回退 Python/SQLite LIKE，任何降级都必须明确标记。
- `API-001`：FastAPI、离线 CLI 和 Agent Skill 共用同一 QueryResult/错误契约；读取路径在 local scope 必须显式带 `vault_id`。
- `API-002`：FastAPI、LLM、QMD 或 private vault 不可用时必须返回明确 `unavailable`/`degraded`，不能伪造写入、验证或生成式回答成功。
- `WEB-001`：public build 只能消费 `public_publishable` projection，并通过 catalog/graph/Pagefind/leak gate。
- `WEB-002`：静态 Wiki 无 FastAPI/LLM/private vault 时仍可浏览和搜索，构建失败保留旧 dist。
- `SEC-002`：internal 对象只能位于等级足够的 private vault，public 输入、生成物和 dist 不得泄漏任何 private vault 的正文或存在性信息。
- `SEC-003`：internal private publish 必须有 confirmation + warning ack；public release 是独立 operation。
- `OPS-002`：多个 private vault 的挂载、ID 合并、unavailable、冲突、逐 vault 备份和 submodule 恢复必须可诊断、可回滚且不自动 reset/push。
- `ARC-004`：相同 snapshot 只能在物理 blob 层去重；每个 `(vault_id, snapshot_sha256)` owner record、权限、备份和发布状态必须独立保留。
- `VAL-002`：provider 必须提供 `provider-capability/v1` 的协议与 data-handling capability；缺少必需能力时 fail-closed，不能解释为模型质量判断。
- `OPS-004`：single-Vault apply 使用 commit-intent/recovery journal；projection 失败进入 `applied_index_pending`，不得伪造完整成功。
- `WEB-003`：正式 Astro build 只接受 `public-projection/v1` manifest；legacy docs adapter 只能用于 validation baseline。
- `VAL-003`：同一内容 hash 下多份审计报告分歧时取 `fail`；唯一推翻路径是 owner 签署的 `validation-override/v1` 复议记录（human 签署、reason 必填、逐条覆盖全部非 supported claim、绑定当前 hash、record 自证），复议后无可用 verdict 报告时回落 `not_run`。

当前 P1/P2 规范编号（已进入追踪矩阵，但仍未实现）：

- `ARC-003`：selector/quote 规范化必须保留 canonical offset map；近似匹配只能产生恢复建议，不能放宽证据范围。
- `WIKI-002`：声明字段、派生字段和 operation-controlled 字段必须分离；非法状态组合和手写派生值必须拒绝。
- `OPS-003`：confirmation/nonce、durable audit、跨 Vault staging 和索引失败恢复必须可回放，临时 `var/state/` 不能作为事实源。
- `SKILL-001`：Agent 只能从本仓库 canonical Skill 调用领域 CLI/API，不能直接修改 Markdown、manifest、索引或发布开关。
- `MIG-001`：存量迁移必须逐文件保留 source/wiki/route/证据/Vault 状态，人工判定与旧站回滚边界不可被自动化隐藏。
- `BAK-001`：备份和恢复按 Vault 独立验收，`backup_state` 不能由全局汇总替代。
- `BAK-002`：备份 manifest 必须覆盖 owner ObjectRef、snapshot、evidence、attestation、operation 和 confirmation hash，并通过隔离空仓恢复。
- `SEC-004`：本地 API capability token、Vault 路径隔离、SSRF/文件竞态和 public allowlist 必须有拒绝与恢复证据。

ID 的详细交付映射见 [规范到验收追踪矩阵](./traceability-matrix.md)；交付状态见 [Feature List](./feature-list.md)。
