# MyKnowledge 证据驱动知识系统设计

> 文档状态：架构设计与实施规范
>
> 更新时间：2026-08-25
>
> 实施边界：本文记录目标架构、约束和验收标准，不代表所有目标能力已经实现。

## 1. 文档目的

MyKnowledge 最初是个人知识博客和前端展示站点。重构后，它同时承担四个工作流：

1. 查询阅读：快速找到已经学习过的知识，并沿关系和来源继续阅读。
2. 写入：把外部资料和个人原始文档稳定地纳入知识库。
3. 索引：从人工内容生成可查询、可导航、可供 Agent 使用的索引。
4. 做题：围绕 wiki 内容生成单选题，进行记忆检索和间隔复习。

系统有两个运行环境：

- **公开静态环境**：部署到 kinchow.github.io，只展示已经通过证据门禁的 wiki 内容，不依赖后端。
- **本地完整环境**：启动 FastAPI 后端，提供跨 sources、wiki 和 practice 的查询、写入辅助、验证、做题和复习能力。

同时，系统提供 myknowledge Agent Skill。Skill 是 Agent 访问知识库的受控入口，不能绕过模板、schema、证据检查、LLM 验证和用户确认直接修改文件。

### 1.1 阅读顺序和术语

本文按“抽象模型 -> 数据契约 -> 工作流 -> 技术实现 -> 迁移和验收”的顺序组织。第一次阅读时建议先看第 2 至 4 节，理解三层数据和两个运行面；需要实现时再按第 5 至 15 节逐项落地；第 16 至 19 节用于迁移、测试和发布判断。

本文中的几个词有固定含义：

| 术语 | 含义 |
| --- | --- |
| source | 原始资料的结构化记录，保存来源、读取范围和证据边界 |
| wiki | 基于一个或多个 source 综合出的人工知识页面 |
| claim | wiki 中可以独立判断真假的核心论断 |
| source locator | 能定位到 source 具体章节，必要时定位到行范围的引用 |
| validation report | 针对某个 wiki/source 内容 hash 生成的 LLM 证据验证报告 |
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
- 浏览器本地收藏、最近阅读和复习状态。

当前验证过的构建基线：

- docs/ 中约 277 个 Markdown 源文件；
- Astro 构建生成 276 篇文章；
- 生成 224 条显式 Markdown 关系；
- 仍有 19 条未解析的内部 Markdown 链接需要在迁移阶段处理。

当前文章没有统一的知识库 Front Matter，原始 docs/ 不能直接被视为已经完成 source/wiki 分层的语料。

### 2.2 目标边界

目标系统必须满足：

- sources 先行，wiki 后置；
- wiki 必须有 source 证据，不能凭空创建；
- question 必须绑定 wiki 的 claim，不能凭空创建；
- 保密分级统一声明、向下游传染，非公开内容只存在于可插拔的 private vault；
- wiki 必须经过确定性校验和 LLM 逐条证据验证；
- 未验证的 wiki 不得进入公开静态构建；
- public 和 local 使用不同的索引投影；
- Agent 只能通过 Skill 和领域工具写入；
- 复习状态属于本地用户数据，不进入公开仓库。

不在第一阶段实现：

- 在线多用户协作；
- 云端数据库和账号系统；
- Elasticsearch 或独立向量数据库；
- 让 LLM 直接替代结构化查询；
- 自动提交、推送和发布远程仓库。

## 3. 总体架构

~~~mermaid
flowchart TD
    A[外部资料 / 个人原始文档] --> B[sources 原始证据层]
    B --> C[确定性 schema 校验]
    C --> D[LLM claim 证据验证]
    D --> E[wiki 人工综合知识层]
    E --> S{status == published?}
    S -->|yes| F[public 索引]
    F --> G[Astro 静态构建]
    G --> H[kinchow.github.io]

    B --> I[local 索引]
    E --> I
    J[practice 单选题] --> I
    I --> K[SQLite FTS5]
    K --> L[FastAPI 本地后端]
    L --> M[本地完整前端]
    M --> N[查询阅读]
    M --> O[做题与复习]

    I --> P[myknowledge Agent Skill]
    P --> Q[Agent 查询 / 写入 / 索引 / 做题]
~~~

### 3.1 数据流

~~~text
外部资料或个人文档
  -> source 模板
  -> source 校验
  -> wiki 候选
  -> claim/evidence 映射
  -> LLM 证据验证
  -> 用户确认
  -> wiki 原子写入
  -> public/local 索引
  -> 静态前端 / 本地后端 / Agent Skill
~~~

### 3.2 核心不变量

以下规则属于 blocking gate，违反即失败：

1. 外部资料和个人编写的原始文档必须先进入 sources/。
2. `kind: knowledge` 的 wiki.sources 不能为空；`kind: index`、`kind: reference` 和 `status: planned` 按 6.7 豁免。
3. wiki.sources 中的每个 ID 必须存在。
4. source 只有 metadata 时不能支撑 published 的 `kind: knowledge` wiki。
5. `kind: knowledge` wiki 的每个核心论断必须有 claim 和 source locator。
6. wiki 必须通过确定性校验；不属于 6.7 豁免范围的必须通过 LLM 证据验证。
7. LLM 不可用、返回 malformed JSON 或验证失败时，不得发布。
8. queries/ 是生成物，禁止人工直接编辑。
9. public 构建只能包含 status: published 的 wiki。
10. Agent 不能直接编辑 Markdown、索引、前端或后端代码。
11. 写入必须经过 preview、用户确认、hash 检查和原子应用。
12. 不执行自动 commit、push、发布和远程系统写操作。
13. `confidentiality: internal` 的对象只能存放在已挂载的 private vault，不得出现在公开仓库中。
14. wiki 和 question 的有效保密等级取自身声明与全部上游对象的最高等级；internal 对象不得 published，不得进入 public 索引和外部快照服务。
15. 内容 hash 只覆盖正文和语义字段；tags、aliases、related 等分类字段变化不使验证报告失效。
16. question 必须绑定所属 wiki 的 claim_id，且只能引用 validated 或 published 的 wiki。
17. 证据豁免只免除 LLM 语义验证，不免除确定性校验；每类豁免必须有替代检查且证据强度对读者可见。
18. `planned` 和 `deprecated` 页面不进入 public build、不作为 RAG 召回来源、不能被新的 claim 引用。
19. 删除内容必须先 `retire` 再 `purge`，且必须在 manifest 中留下 ID、hash 和废弃原因。

### 3.3 三层数据的所有权

```text
sources   = 证据事实的入口，允许半自动生成，但必须人工校对
wiki      = 面向理解的人工综合，必须逐条绑定证据
queries   = 可重建的索引投影，任何手工修改都会在下次生成时被覆盖
```

`practice/` 是 wiki 的消费层：题目可以引用 wiki，但不能反向成为 wiki 的证据。`state/` 是本机运行状态：它可以记录操作和复习进度，但不能改变仓库中 source、wiki 的事实内容。

## 4. 目录与对象模型

目录按知识内容组织。来源类型不再通过 blogs/、docs/、books/ 等物理目录表达，而是通过 Front Matter 表达。

~~~text
MyKnowledge/
├── sources/
│   ├── computer-science/
│   ├── multimedia/
│   ├── reading-notes/
│   ├── tools/
│   └── work-methods/
├── wiki/
│   ├── computer-science/
│   ├── multimedia/
│   ├── reading-notes/
│   ├── tools/
│   └── work-methods/
├── practice/
│   └── questions/
├── archive/
│   ├── text/
│   ├── raw/
│   └── manifest.jsonl
├── queries/
│   ├── public/
│   └── local/
├── config/
│   ├── schemas.yaml
│   ├── vocab.yaml
│   ├── vaults.yaml
│   └── policy.yaml
├── backend/
├── frontend/
├── tools/
├── templates/
└── state/
    ├── operations/
    ├── review/
    └── llm-validation/
~~~

### 4.1 目录和元数据的职责

| 信息 | 位置 |
| --- | --- |
| 计算机科学、工具、工作方法等知识领域 | 目录路径和 domain |
| knowledge、index、reference | kind |
| draft、validated、published | status |
| 博客、文档、个人笔记、PR | source_type |
| 外部资料或个人资料 | origin |
| 标签、别名和关系 | tags、aliases、Markdown 链接、related |
| source 证据映射 | wiki 的 evidence |
| 题目归属 | question 的 wiki_id |

contents.md 在迁移后作为 kind: index 的普通 wiki 页面，不建立额外的 MOC 目录。

### 4.2 Vault 与保密分级

当前仓库中的资料全部是公开资料，因此本仓库就是 public vault。非公开资料不放进本仓库，而是以可插拔的 private vault 形式挂载：

~~~yaml
# config/vaults.yaml
vaults:
  - id: public
    path: .
    confidentiality: public
    required: true
  - id: internal
    path: ~/Documents/知识/MyKnowledge-private
    confidentiality: internal
    required: false
~~~

private vault 的目录结构与 public vault 相同（`sources/`、`wiki/`、`practice/`），只是位于公开仓库之外。工具在启动时按 `vaults.yaml` 合并对象空间：ID 在全部已挂载 vault 内唯一，跨 vault 引用按 ID 解析，不需要写路径。

保密等级规则：

| 规则 | 说明 |
| --- | --- |
| 枚举 | `confidentiality: public \| internal`，缺省 `public`；后续如需更多等级在 `policy.yaml` 中扩展，等级之间必须是全序 |
| 存放位置 | `internal` 对象只能位于 `confidentiality: internal` 的 vault；public vault 中出现 `internal` 声明即为校验失败（防止误放） |
| 传染 | wiki 有效等级 = max(自身声明, 全部被引 source 的等级)；question 有效等级 = max(自身声明, 所属 wiki 的有效等级) |
| 发布 | 有效等级非 `public` 的对象不得 `published`，不得进入 `queries/public`、Pagefind 和 dist/ |
| 外部服务 | `internal` source 不得提交到 Wayback 等外部快照服务，不得出现在发送给外部 LLM provider 的请求中 |

private vault 未挂载时，其中的对象视为 `unavailable` 而不是"不存在"：引用它们的 wiki 保持当前状态并标记 `upstream_unavailable`，校验器不得据此判定 source 缺失、不得降级或改写引用。这样同一份 public 仓库在挂载和未挂载两台机器上都不会互相破坏校验结果。

未配置 private vault 时，全部行为退化为当前的单一公开仓库，不引入额外成本。

当前仓库内的资料已确认全部为公开资料，因此第一阶段只落地 `confidentiality` 字段、传染规则和误放拦截这三项确定性检查；private vault 的挂载与合并作为已定义但暂不实现的扩展点，等真的有非公开资料需要纳入时再启用。这样既不增加当前实现成本，也不会在将来需要时被迫改数据模型。

### 4.3 仓库内容与生成物归属

必须明确每一类文件是"内容"还是"生成物"，否则每次重建索引都会产生大片脏 diff，而真正需要备份的用户数据反而没进版本管理。

| 路径 | 类别 | Git | 理由 |
| --- | --- | --- | --- |
| `sources/`、`wiki/`、`practice/` | 内容 | 入库 | 唯一真相源 |
| `config/`、`templates/`、`tools/`、`backend/`、`frontend/`（源码） | 内容 | 入库 | 规范与实现 |
| `archive/text/`、`archive/manifest.jsonl` | 证据副本 | 入库 | 证据链锚点，体积可控（见 5.6） |
| `archive/raw/` | 证据副本 | git-lfs 入库 | 二进制原件走 LFS，避免污染主仓历史 |
| `queries/public/` | 生成物 | 入库 | 静态站构建输入，需要可复现发布 |
| `queries/local/`、`rag-index.jsonl`、向量索引文件 | 生成物 | 忽略 | 体积大、可重建、每次重建全变 |
| `state/operations/`、`state/llm-validation/` | 运行记录 | 忽略 | 本机审计信息，可重生成 |
| `state/review/`（FSRS 进度） | 用户数据 | 忽略但必须备份 | 唯一不可重建的数据，见下 |
| `.cache/fetch/`、`frontend/dist/`、`node_modules/` | 临时物 | 忽略 | 无保留价值 |

`queries/public` 入库是有意的：它决定公开站点的内容，需要能对照某个 commit 复现一次发布。`queries/local` 不入库，因为它随每次索引重建整体变化，且可以从内容完全重建。

`archive/raw/` 从启用归档的那一次变更起就走 git-lfs，不经过"先普通入库、以后再迁"的中间状态。原因是 git 历史里的 blob 删不掉：一旦二进制原件以普通对象提交过，事后迁 LFS 必须重写历史（`git filter-repo`），而这个仓库是公开的、已有远端，重写历史会打断所有已有 clone 和引用。先配置后归档的顺序成本几乎为零，反过来就很贵。

启用步骤是归档功能的前置条件，缺一不可：

~~~text
git lfs install
git lfs track "archive/raw/**"      # 写入 .gitattributes 并提交
# 确认 .gitattributes 已生效后，才允许 archive_source.py 写入 raw
~~~

`archive_source.py` 启动时必须检查 `.gitattributes` 中存在对应的 LFS 规则；不存在时拒绝写入 `archive/raw/`，只写 `archive/text/` 并降级为 `archive_policy: text-only`。这条检查把"忘记配 LFS"变成一次明确失败，而不是一堆已经进了主仓历史的二进制文件。

`archive/text/` 保持普通入库：它是压缩后的纯文本，体积在几 MB 量级，需要 diff 与历史可读性，不适合放进 LFS。

FSRS 复习进度是全库唯一无法从内容重建的数据，却又不适合进公开仓库。必须指定一条明确的备份路径：定期导出到同步目录，或推送到一个私有仓库。没有配置备份路径时，`tools/` 应在每次做题会话结束时给出提示——这条数据丢了就是记忆调度从零开始。

生成物统一带生成器版本、生成时间、输入集合 hash 和 schema 版本；`queries/` 中的任何手工修改都会在下次生成时被覆盖，工具不做保护。

## 5. Source 规范

### 5.1 Source Front Matter

~~~yaml
---
id: source-transformer-paper
title: "Transformer 原始资料"
domain: computer-science
origin: external
source_type: doc
confidentiality: public
url: "https://example.com/source"
captured_at: 2026-08-25
tags: [transformer]
aliases: []
read_status: retrieved
evidence_status: source-reported
related: []
retrieval:
  fetched_at: 2026-08-25T10:12:00+08:00
  http_status: 200
  etag: 'W/"6f21-abc"'
  last_modified: "Mon, 18 Aug 2026 03:00:00 GMT"
  text_sha256: "sha256:9f2c..."
  raw_sha256: "sha256:41ab..."
  archive_policy: text+raw
  snapshot_url: "https://web.archive.org/web/20260825/https://example.com/source"
---
~~~

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

保密等级由人工声明，工具不猜测。写入 preview 时，如果 URL 命中 `policy.yaml` 中的内网域名模式（例如 `*.baidu-int.*`、私有网段），而声明为 `public`，必须直接阻断并要求改为 `internal` 或改用 private vault。

### 5.3.1 Source 字段级契约

| 字段 | 必填 | 约束 |
| --- | --- | --- |
| id | 是 | 全库唯一的 kebab-case 标识，写入后不自动重命名 |
| title | 是 | 非空，作为查询和阅读显示名 |
| domain | 是 | 必须来自 `config/vocab.yaml`，并与目录领域一致 |
| origin | 是 | `external` 或 `personal` |
| source_type | 是 | `blog`、`doc`、`book`、`contest`、`pr`、`local-file`、`personal-note` |
| confidentiality | 是 | `public` 或 `internal`，缺省 `public`；必须与所在 vault 等级一致 |
| url | 网络来源必填 | 外部网页的原始链接；链接已失效时保留为历史出处，见 5.6.1 |
| url_status | 有 url 时必填 | `live`、`dead`、`unreachable`、`unknown` |
| local | local-file 必填 | `path` 与 `file_sha256` 必填，见 5.8；原文不入库 |
| captured_at | 是 | ISO 8601 日期或时间 |
| read_status | 是 | `metadata-only`、`partial`、`retrieved` |
| evidence_status | 是 | 与 origin 和正文证据边界兼容 |
| retrieval | 网络来源与离线副本必填 | 抓取/导入与归档元数据，见 5.6；必须含 `acquisition` 与 `text_sha256`；纯 `local-file` 不适用 |
| tags、aliases、related | 否 | 缺省为空数组，不能写成未解析字符串 |
| content_sha256 | 生成 | 按 6.6 的规范化正文计算，Agent 不得手写 |
| locator_sha256 | 生成 | 每个可引用章节的正文 hash，见 6.6 |

`read_scope`、附件清单和人工校对备注放在正文的“证据边界”章节或扩展 metadata 中。source 原文、抓取缓存和凭据不放入 Front Matter；Front Matter 只保存可公开审计的来源元数据。

### 5.4 Source 证据边界

- 只有搜索摘要时，不能写入正文接口、参数和性能数字。
- PDF 只读目录时，必须标记 metadata-only。
- 只读取部分正文时，必须记录读取章节和未读取章节。
- 个人 source 可以作为个人经验的证据，但不能自动写成普遍性外部事实。
- source 发生变化后，所有引用它的 wiki 验证结果失效。

### 5.5 Source locator 规范

为了让引用可复查，`source_refs` 不接受只有 source ID 的模糊引用。第一阶段采用以下格式：

```text
<source-id>#<heading-slug>
<source-id>#<heading-slug>@L<start>-L<end>
```

其中 `heading-slug` 由 source 正文的 Markdown 标题稳定生成；`@L...` 是可选的行范围，用于长文、代码或实验日志。校验器必须确认：source ID 存在、章节标题存在、行范围在 source 当前版本内。章节重命名或正文重排会使旧 locator 失效，必须重新映射并重新验证。

Source 校验还应保存可供定位的章节目录：

```yaml
locators:
  - heading: "已读取事实"
    slug: "已读取事实"
    line_start: 12
    line_end: 28
    sha256: "sha256:..."
```

行号是当前 source 版本的辅助定位，不是跨版本稳定 ID；跨版本稳定性由章节 slug 和章节级 `sha256` 共同保证。同名标题按出现顺序追加序号消歧：`#限制条件`、`#限制条件-2`。

### 5.6 原文快照归档与来源漂移

**来源必须明确，且必须保存本地快照副本。** 只记录 URL 是不够的：网页会改版、会失效，等到需要复查时原文已经不是当初读的那一份，整条证据链就断在"我手写的那篇摘要"上。归档副本是证据链的锚点。

归档采用内容寻址加压缩存储，同一份资料被多个 source 引用时只存一份：

~~~text
archive/
├── text/            # 提取后的正文，纯文本，长期保留
│   └── <sha256[:2]>/<sha256>.md.zst
├── raw/             # 原始 HTML/PDF/附件，体积大
│   └── <sha256[:2]>/<sha256>.<ext>.zst
└── manifest.jsonl   # sha256 -> {url, fetched_at, content_type, bytes, ext}
~~~

source 通过 `retrieval` 引用归档条目：

| 字段 | 说明 |
| --- | --- |
| acquisition | 获取方式：`fetch`（HTTP 抓取）、`offline-copy`（导入离线副本）、`local-file`（引用本地原件） |
| fetched_at | 实际读取该资料的时间；`offline-copy` 记录导入时间 |
| http_status | 抓取时的 HTTP 状态码；`offline-copy` 与 `local-file` 留空 |
| etag、last_modified | 服务端版本标识，用于后续廉价比对 |
| text_sha256 | 提取后正文的 hash，指向 `archive/text/` 中的副本 |
| raw_sha256 | 原始文件的 hash，指向 `archive/raw/`；未保留时为空 |
| archive_policy | `text-only`、`text+raw`、`external-only`（见下） |
| snapshot_url | 第三方快照地址（如 Wayback），作为补充不作为替代 |

`acquisition` 与 `source_type` 是正交的两件事：`source_type` 说明"这份资料是什么"（博客、文档、书、PR），`acquisition` 说明"我是怎么拿到它的"。一篇博客的离线副本仍然是 `source_type: blog`，只是 `acquisition: offline-copy`。

压缩与体积策略：

- 正文用 zstd（`-19`，文本压缩比通常 4-6 倍）；已压缩格式（PDF、图片、视频）不做二次压缩，按原样存储。
- 归档前先做正文提取（HTML 去导航去广告），**提取后的文本才是证据载体**；原始 HTML 只作为争议时的复核备份。
- 单文件阈值写在 `policy.yaml`：正文超过 `text_max_bytes` 需要先按 5.7 拆分；原始文件超过 `raw_max_bytes`（建议 2 MB）时 `archive_policy` 降为 `text-only`，只保留正文并在 manifest 中记录被跳过的原始文件 hash 和体积。
- `archive/raw/` 走 git-lfs，且 LFS 规则必须先于归档写入配置好，见 4.3。
- 大体积二进制（视频、数据集、完整代码仓）一律不归档，改用 5.8 的 `local-file` 加可复现定位（repo + commit + 路径 + 行号）。

体积预估：当前 285 个独立外链，按网页正文均值 30 KB 计，`archive/text/` 压缩后约 2-3 MB；启用 `text+raw` 后原始 HTML 约 15-25 MB 压缩后 5-8 MB。这个量级适合直接进 git。PDF 与书籍扫描件不在此列，必须走 `text-only` 或 `local-file`。

`archive/raw/` 的 git 归属见 4.3：走 git-lfs，LFS 规则未配置时归档降级为 `text-only`。

归档的三条硬约束：

1. **归档副本不得进入 public build。** 它是第三方内容的本地复制件，用于个人复核，不是可再发布的内容。leak gate 必须扫描 `dist/` 中不出现 `archive/` 的任何内容（见 13.3）。
2. `confidentiality: internal` 的资料，归档副本只能落在 private vault，且禁止提交到 Wayback 等外部快照服务。
3. 需要鉴权的来源，凭据只从环境变量或本机凭据文件读取，不写入 Front Matter、manifest 和日志；归档文件本身不得包含 Cookie、Authorization 头和会话标识。

抓取约束：只抓取用户明确要求读取的单个 URL，不做站点爬取和批量抓取。

### 5.6.1 离线副本导入

原链接已经失效、但手上有离线副本（浏览器保存的 HTML、导出的 PDF、收藏夹里的存档）时，**以离线副本作为证据载体，原 URL 降为历史出处**。这是唯一正确的处理方式：拿不到原文就不建 source 会白扔掉手里已有的证据，而只写 URL 又等于没有证据。

离线副本走与抓取相同的归档流程，只是入口不是 HTTP：

~~~text
archive_source.py --from-file <离线副本路径> --url <原始链接> --url-status dead
  -> 正文提取
  -> archive/text/<sha256>.md.zst
  -> archive/raw/<sha256>.<ext>.zst（走 LFS）
  -> manifest.jsonl 记录 acquisition: offline-copy
~~~

对应的 source：

~~~yaml
source_type: blog
url: "https://blog.example.com/dead-post"     # 历史出处，不可再抓取
url_status: dead                              # live | dead | unreachable | unknown
retrieval:
  acquisition: offline-copy
  fetched_at: 2026-08-25T10:12:00+08:00       # 导入时间
  text_sha256: "sha256:..."
  raw_sha256: "sha256:..."
  archive_policy: text+raw
  copy_note: "2019 年浏览器保存的 HTML 副本"
~~~

规则：

- `url` 保留原始链接作为历史出处，用于说明这段内容出自何处、便于日后查 Wayback，但**不参与可达性检查**；
- `url_status` 记录判定结果，`unknown` 表示尚未确认（离线导入时允许），联网后由 `check_sources.py` 复核并更新；
- 离线副本的可信度由你自己承担：工具能保证"这份副本此后没被改过"（hash），不能保证"这份副本忠实于当年的原文"。因此 `copy_note` 必填，写清副本的来历和获取时间；
- 已有 source 的链接后来失效（5.6 的 `gone`）不需要转成 `offline-copy`：它的归档正文是从活链接抓取的，可信度更高，只标记 `link_rot` 即可。

获取方式的优先级：

~~~text
1. URL 可达            -> acquisition: fetch      （最可信：正文直接来自原站）
2. URL 不可达 + 有离线副本 -> acquisition: offline-copy（次之：副本来历需人工说明）
3. 有完整本地原件        -> acquisition: local-file  （见 5.8：原件完整、可重复读取）
4. 以上都没有            -> 不允许写入（见 5.9）
~~~

`tools/check_sources.py` 定期巡检外部链接：

~~~text
unchanged     etag/last_modified/text_sha256 一致
changed       原文已变化，写入新快照版本，标记 source_drift: true
gone          404/410 或域名失效，标记 link_rot: true（本地快照仍可用）
unreachable   网络或鉴权问题，不改变任何标记
~~~

`changed` 时**不覆盖旧快照**：内容寻址天然保留多版本，`retrieval` 里增加一条历史记录。这样"我当时读到的是哪一版"永远可回溯。

漂移语义必须与验证失效区分开：source.md 是人工整理的证据记录，外部原文变化不会改变它的 `content_sha256`，因此 **不自动使 wiki 验证报告失效**，也不自动把页面打回 draft。工具只做三件事：置 `source_drift` / `link_rot` 标记、在本地查询和页面上显示提示、把该 source 及其下游 wiki 列入待复核清单。是否重读原文由人决定。`gone` 时本地快照仍然构成完整证据，已发布内容不受影响。

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
  path: "~/code/llvm-project/llvm/lib/Transforms/Vectorize/LoopVectorize.cpp"
  file_sha256: "sha256:..."
  byte_size: 412355
  read_range: "L1200-L1480"
  resolved_at: 2026-08-25
read_status: partial
evidence_status: source-reported
---
~~~

字段规则：

- `origin` 仍是 `external`——内容不是你写的；`personal` 只用于你自己产出的记录。
- `url` 对 `local-file` 不必填；`local.path` 与 `local.file_sha256` 必填，`retrieval` 与 `snapshot_url` 不适用。
- 原文**不进仓库**，只记录路径和 hash。仓库体积不因引用大文件而膨胀。
- 换机器或文件被移动导致路径解析失败时，状态为 `unresolved`，语义与 4.2 的 vault 未挂载一致：不得判定为证据缺失、不得据此降级或改写引用。
- `file_sha256` 变化的处理与 5.6 的 source drift 一致：只标记待复核，不自动使 wiki 报告失效——因为 source.md 记录的是你已读取的那个版本的事实。

### 5.9 写入的联网要求与来源完备性

**写入必须在有网络的环境下进行，且没有来源的内容一律不允许写入。**

这两条是同一个目标的两面：一次 apply 完成后，证据载体必须已经完整落库。如果允许离线写入网络来源，就会留下一批"有 URL、没归档正文"的 source，它们看起来合规，实际上证据链是空的，而且这个缺口只有等到复查时才会被发现。与其事后补，不如在写入时就拒绝。

来源完备性检查——每个 source 必须满足三者之一，否则 preview 直接 blocked：

| 来源形态 | 完备条件 |
| --- | --- |
| 网络来源（`acquisition: fetch`） | `url` 可访问、抓取成功、`archive/text/` 中已存在对应 `text_sha256` 的归档正文 |
| 离线副本（`acquisition: offline-copy`） | 副本文件存在、归档正文已生成、`url` 与 `copy_note` 已填，见 5.6.1 |
| 本地来源（`acquisition: local-file`） | `local.path` 可解析、`local.file_sha256` 已计算并记录 |
| 个人来源（personal-note） | `origin: personal` 且正文非空，`evidence_status` 为 personal-observation 或 inferred |

三者皆不满足的写入被拒绝，不存在"来源待补"的中间状态。这一条同样适用于 `metadata-only`：它表示"只拿到了目录或入口页"，而不是"什么都没拿到"——那个目录页本身也必须抓取并归档，否则连"入口存在过"这件事都无法复核。

`policy.yaml` 中的开关：

~~~yaml
write:
  require_network: true          # apply 前必须确认网络与归档可达
  allow_offline_kinds:           # 例外：不需要抓取的来源形态
    - offline-copy
    - local-file
    - personal-note
~~~

`require_network: true` 时，`apply` 在获取写锁后、写入 staging 前做一次可达性检查；失败即 operation 转 `blocked`，不写入任何文件。`allow_offline_kinds` 是有意保留的窄例外：这三种形态的证据载体本来就在本机，强制联网不增加任何保障。把这个例外做成配置项而不是硬编码，是为了让"为什么这次能离线写"有据可查。

离线导入的副本，其 `url_status` 允许暂时为 `unknown`，联网后由 `check_sources.py` 复核补齐——这不影响证据完备性，因为证据来自副本而不是链接。

离线状态下仍然可用的能力：

| 能力 | 离线可用 |
| --- | --- |
| 建立 offline-copy / local-file / personal source | 可用（按 `allow_offline_kinds`） |
| 建立网络来源 source（`acquisition: fetch`） | **不可用**，preview 可生成候选，apply 被拒绝 |
| wiki 写作、claim 映射、locator 校验 | 可用（前提是引用的 source 已在库） |
| wiki 的 apply | 不可用（`require_network` 生效） |
| 索引生成、FTS5 检索、图谱、做题与 FSRS 复习 | 完全可用 |
| Embedding 与向量召回（本地模型） | 可用 |
| LLM 语义验证 | 需要 provider；可指向本机或内网的 OpenAI-compatible endpoint |

因此离线时的正确用法是"读和练"，而不是"写"：查询、阅读、做题、复习全部可用；要写入就联网。这个约束会带来一点不便，换来的是"库里每一条外部论断都有本地归档正文"这个可以直接依赖的性质，不需要每次都去确认哪些 source 的归档是完整的。

## 6. Wiki 严格规范

### 6.1 Wiki Front Matter

~~~yaml
---
id: wiki-transformer
title: "Transformer"
domain: computer-science
kind: knowledge
status: draft
confidentiality: public
tags: [transformer]
aliases: [Transformer 模型]
sources:
  - source-transformer-paper
related: []
question_ids: []
evidence:
  - claim_id: c1
    claim: "Attention 使用 Q、K 的相关性计算权重，再对 V 加权求和。"
    source_refs:
      - source-transformer-paper#已读取事实
    support: direct
updated_at: 2026-08-25
---
~~~

### 6.1.1 Wiki 字段级契约

| 字段 | 必填 | 约束 |
| --- | --- | --- |
| id、title、domain、kind、status | 是 | `kind` 为 `knowledge`、`index`、`reference`；`status` 为 `planned`、`draft`、`validated`、`published`、`deprecated` |
| confidentiality | 是 | `public` 或 `internal`，缺省 `public`；有效等级按 4.2 从上游 source 传染，声明低于上游即校验失败 |
| tags、aliases、related、question_ids | 是 | 始终为数组；ID 必须能解析到对应对象 |
| sources | knowledge 必填 | 至少一个已存在 source ID，不能只引用 metadata-only source；index/reference/planned 见 6.7 |
| evidence | knowledge 必填 | 每个核心 claim 一条唯一 `claim_id`，每条至少一个 locator；豁免类型见 6.7 |
| updated_at | 是 | ISO 8601 日期或时间 |
| supporting_quote | common-knowledge claim 必填 | 原文引文，由工具在归档正文中逐字校验，见 6.7 |
| content_sha256 | 生成 | 按 6.6 规范化正文计算 |
| evidence_sha256 | 生成 | 按 6.6 规范化 evidence 块计算；claim 文本、source_refs 或 support 变化即失效 |

`validated` 不是作者自由填写的状态。写入工具必须根据确定性校验结果和有效 LLM report 计算它；属于 6.7 豁免范围的页面按替代检查结果和 `verdict: exempt` 记录计算。作者只能创建 `draft` 候选，`published` 还需要明确的发布确认事件。

### 6.2 Wiki 状态机

~~~text
planned -> draft -> validated -> published
              ^          |
              |          +-- source 变化 / 验证过期
              +----------+

任意状态 -> deprecated（人工判定内容错误或过时）
deprecated -> draft（修订后重新进入流程）
~~~

- planned：只有标题和意图，没有正文和 source。用于"知道要写但还没写"的条目，不进索引正文、不进 public build，只出现在待写清单和查询结果的 `pending` 字段。
- draft：可以编辑、预览和查询，但不进入 public build。
- validated：结构、引用、claim 和 LLM 验证全部通过。
- published：用户确认发布，允许进入 public build。
- deprecated：内容已被判定为错误或过时。保留文件和路由以免死链，但不进 public build、不作为 RAG 召回来源、不能被新的 claim 引用，关联题目自动 `enabled: false`。

`planned` 与 `deprecated` 都只能由人工显式设置，工具不自动推断。任何 source 或 wiki 内容变化后，页面自动回到 draft 或标记验证过期，不能继续沿用旧报告。

`planned` 条目只需要 `id`、`title`、`domain`、`kind`、`status` 五个字段，不要求 sources 和 evidence——它还不是知识，只是一条待办。批量导入的标题清单（例如一份没有答案的问题列表）应该进 `planned`，而不是生成一批空壳 draft 页面。

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
    source_refs:
      - source-a#已读取事实
    support: direct

  - claim_id: c2
    claim: "综合两个来源得到的结论。"
    source_refs:
      - source-a#机制
      - source-b#限制条件
    support: synthesis

  - claim_id: c3
    claim: "根据实验日志推断出的待验证方向。"
    source_refs:
      - source-personal#实验结果
    support: inferred
~~~

支持类型：

| 类型 | 规则 |
| --- | --- |
| direct | 必须由外部 source 明确表达 |
| synthesis | 必须由两个或多个 source 共同支持 |
| inferred | 必须写出观察事实、推理过程和下一步验证动作 |
| personal | 只能引用 origin: personal 的 source |

以下情况一律阻断 published：

- sources 为空；
- source ID 不存在；
- source locator 不存在；
- claim 引用的 source 是 metadata-only；
- 核心论断没有 claim_id；
- claim 没有 source_refs；
- 个人 source 被用来支撑外部普遍事实；
- LLM 返回 unsupported、contradicted 或 unmapped。

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

`common-knowledge` 的适用范围是"查一下就能确认、且不会因版本而变"的事实：语言关键字语义、标准库接口约定、公开协议字段、数学定义。**不适用**于版本相关行为、编译器实现细节、性能数据和最佳实践——这些必须走正常的 source locator 加验证路径。判断依据是"权威入口是否直接写了这句话"，不是"我觉得这是常识"。

`common-knowledge` 必须有明确来源：`url` 必填、`read_status` 必须是 `retrieved`、必须有 `archive/text/` 中的归档正文。这条约束是为了消除滥用动机——如果标记它比正常引用更省事，48 篇找不回出处的旧文都会涌向这一类。要求"确实打开过并归档"之后，它的成本与正常引用相当，只省掉逐条 LLM 判定这一步。

`common-knowledge` 的豁免不是"不做语义检查"，而是**把语义检查从模型判断换成确定性匹配**。每条 claim 的 evidence 必须人工填写 `supporting_quote`：

~~~yaml
evidence:
  - claim_id: c1
    claim: "constexpr 变量必须在编译期完成初始化。"
    source_refs:
      - source-cppref-constexpr#正文
    support: direct
    supporting_quote: "constexpr 变量必须立即被初始化，且其初始化必须是常量表达式。"
~~~

工具按 6.9 的规范化规则，在该 locator 章节对应的归档正文中逐字查找这段引文，找不到即豁免失败、页面保持 `draft`。这样 `attested` 页面的检查强度和 `verified` 相当——都要求"这句话确实出现在原文里"——区别只在于前者由人指出引文、后者由模型指出引文。人工填引文的成本是复制粘贴一句话，换来一条真正可执行的检查，而不是仅仅确认"有链接、有归档"这类形式条件。

引文与 claim 表述不同不构成失败：`claim` 是你的转述，`supporting_quote` 是原文。校验只检查引文的存在性，不判断转述是否忠实——后者是 `verified` 路径上 LLM 的职责，也是选择 `common-knowledge` 时所接受的取舍。因此适用范围必须严格限制在"转述空间很小"的事实上（见下）。

当一个 claim 同时引用 external 和 personal source 时，若结论是普遍事实，至少需要 external source 作为直接或综合证据；personal source 只能作为补充经验。若没有 external source，claim 必须降级为 personal 或 inferred。

`metadata-only` source 可以作为资料目录中的待读取入口保留，但不能出现在任何已验证核心 claim 的 `source_refs` 中；如果一个 wiki 没有其他可用证据，或者它的核心 claim 只能落到 metadata-only source，页面必须保持 `draft`。

### 6.6 内容 hash 契约与失效粒度

本节适用于 source、wiki 和 question 三类对象，是 8.5 验证失效判定的唯一依据。

**hash 只覆盖正文和语义字段。** 分类字段变化不使任何验证报告失效——新增一个标签、补一个别名、调整 related 都不应该触发重新验证和重新花费 LLM 调用。

~~~text
content_sha256   = sha256(canonical_body)
evidence_sha256  = sha256(canonical_yaml(evidence))          # 仅 wiki
locator_sha256[<slug>] = sha256(canonical_body_of_section)   # 仅 source
~~~

`canonical_body` 的规范化规则：剥离 Front Matter，只取正文；统一为 LF；去掉行尾空白；折叠文件末尾空行为单个换行；不做其他改写（不动大小写、不动标点、不重排列表）。

字段分类：

| 类别 | 字段 | 变化是否触发失效 |
| --- | --- | --- |
| 语义内容 | 正文、`evidence`（claim 文本 / source_refs / support）、source 的 `read_status`、`evidence_status`、`origin`、`confidentiality` | 是 |
| 分类与导航 | `tags`、`aliases`、`related`、`domain`、`title`、`question_ids` | 否 |
| 派生字段 | `status`、`updated_at`、`content_sha256`、`evidence_sha256`、`locator_sha256`、`retrieval` | 否，且不参与自身 hash 计算 |

`evidence` 在 Front Matter 中，但它是语义内容，必须单独 hash。只 hash 正文会留下一个绕过门禁的口子：改掉 claim 文本或换掉 `source_refs` 之后，旧的通过报告仍然"有效"。`content_sha256` 与 `evidence_sha256` 必须同时绑定到验证报告。

派生字段不参与自身 hash，因此不存在"改内容 → hash 变 → status 回退 → 写 status 又改文件 → hash 再变"的不动点问题：写 `status` 和 `content_sha256` 不会改变 `content_sha256`。

**失效粒度按 locator 而不是按整个 source 文件。** 修改 source 中未被引用的章节，不影响引用其他章节的 wiki：

| 变更 | 失效范围 |
| --- | --- |
| source 某章节正文变化 | 仅 `source_refs` 命中该章节的 claim 失效 |
| source 章节被重命名或删除 | 引用该 slug 的 claim 失效，报 locator 不存在 |
| source 新增章节 | 不失效 |
| source 的 tags/title 变化 | 不失效 |
| source 的 `read_status`、`evidence_status`、`origin`、`confidentiality` 变化 | 引用它的全部 claim 失效（证据性质改变） |
| wiki 正文变化 | 该 wiki 的报告失效 |
| wiki 某条 claim 变化 | 该 wiki 的报告失效（第一阶段按整篇重验，不做 claim 级增量） |
| wiki 的 tags/aliases/related 变化 | 不失效 |
| 外部原文变化（source_drift） | 不失效，仅进入待复核清单，见 5.6 |

claim 级增量重验放在后续阶段：报告结构已按 claim 存储，具备增量能力，但第一阶段先用整篇重验换取实现简单和判定确定。

### 6.7 证据豁免矩阵

不是所有页面都能套用"每条核心论断都要有外部 source locator 并通过 LLM 验证"。强行套用会产出大量无意义的仪式性证据（把官方 API 手册抄成 claim，再让模型判断抄得对不对）。但豁免必须遵守一条原则：

> **豁免只免除 LLM 语义验证，不免除确定性校验。** 每一类豁免都必须有替代性的确定性检查，并且在页面上对读者可见。

| 豁免场景 | 判定条件 | 免除什么 | 替代检查 |
| --- | --- | --- | --- |
| `kind: index` 导航页 | 正文主要是链接与分类 | sources、evidence、LLM 验证 | 全部链接必须可解析到库内对象；不得含正文结论 |
| `kind: reference` 参考清单 | API 清单、关键字表、枚举、资源索引 | claim 级 evidence、LLM 验证 | 必须有 metadata-only 以上的 source；每个条目必须有可查证入口；不得出现推断性表述 |
| `evidence_status: common-knowledge` | 语言标准、公开规范、教科书级公认事实 | LLM 逐条验证 | source 必须有 `url`、`read_status: retrieved` 和归档正文快照；每条 claim 必须人工填写 `supporting_quote`，由工具在归档正文中逐字校验 |
| `origin: personal` 自撰内容 | 论断来自本人理解、观察或实验 | LLM 验证（模型验证你的话是否支持你的话是同义反复） | 必须使用个人语气；不得表述为外部普遍事实；support 只能是 `personal` 或 `inferred` |
| `status: planned` 待写条目 | 无正文 | sources、evidence、正文模板 | 只允许五个字段；不进索引正文与 public build |
| `status: deprecated` 废弃内容 | 人工判定错误或过时 | 重新验证 | 不进 public build、不进 RAG 召回、不可被新 claim 引用 |
| `kind: knowledge` 的常规页面 | 以上都不适用 | 不豁免 | 完整走 source → claim → locator → LLM 验证 |

页面必须显示自己的证据强度，读者不需要读 Front Matter 就能知道这页是"外部来源验证过的事实"还是"我的个人理解"：

~~~text
verified      通过 LLM 逐条证据验证
attested      common-knowledge，有权威入口但未逐条验证
personal      个人理解或实验记录
reference     参考清单，只保证条目入口可查
index         导航页，不含论断
~~~

这个标识由工具从 `kind`、`evidence_status`、`origin` 和验证报告计算，不由作者填写，并且必须同时出现在页面、查询结果和 Agent 输出契约中。豁免的代价是读者需要知道强度差异，因此**可见性是豁免成立的前提**：任何无法在前端显示强度标识的豁免类型，都不允许启用。

`common-knowledge` 与 `personal` 的边界必须人工判断，不允许工具自动降级：判不准时按 `personal` 处理（更保守的一侧）。

豁免页面同样需要一份可失效的验证记录，否则 `validated` 状态无从计算。豁免走与 8.4 相同的报告结构，只是 `verdict: exempt`：

~~~yaml
wiki_id:
validator_version:
exemption: index | reference | common-knowledge | personal
substitute_checks:        # 实际执行的替代检查及结果
quote_checks:             # common-knowledge 专用：claim_id -> 引文匹配结果
wiki_content_sha256:
wiki_evidence_sha256:
locator_sha256:
verdict: exempt
~~~

豁免记录绑定同样的三组 hash，因此失效规则与 8.5 完全一致：页面正文或 evidence 变化后豁免记录同样失效，必须重新判定豁免是否仍然成立。这一点很关键——否则一个页面可以先以 `personal` 豁免通过，再把正文改写成外部普遍事实而不触发任何检查。

豁免类型变化（例如 personal 页面后来补上了外部 source）必须重新走一次判定，不允许沿用旧类型的记录。

### 6.8 声明字段、派生字段与合法组合

字段分成两组，边界必须清楚：**声明字段由人写，派生字段由工具算**。作者写错声明字段会被拒绝；作者手写派生字段一律以工具计算结果覆盖。

声明字段（人工）：

~~~text
kind                knowledge | index | reference
status              planned | draft | validated | published | deprecated
confidentiality     public | internal
origin              external | personal            （source）
evidence_status     source-reported | common-knowledge | personal-observation | inferred | metadata-only（source）
support             direct | synthesis | inferred | personal（claim）
~~~

派生字段（工具计算，不入 hash）：

~~~text
effective_confidentiality   max(自身, 全部上游对象)
evidence_class              full | exempt-index | exempt-reference | exempt-common | exempt-personal
strength                    verified | attested | personal | reference | index
publishable                 true | false
validation_state            valid | expired | missing | exempt
~~~

`strength` 的映射规则，按顺序命中第一条：

| 条件 | strength |
| --- | --- |
| `kind: index` | index |
| `kind: reference` | reference |
| 全部 claim 的 source 均为 `origin: personal` | personal |
| 全部 claim 的 source 均为 `evidence_status: common-knowledge` | attested |
| 存在有效 LLM report 且 verdict 为 pass | verified |
| 其他 | 不可发布，`publishable: false` |

`kind: knowledge` 的页面若同时含 personal 与 external claim，取更保守的一侧：只要有任一 claim 只由 personal source 支撑，整页 strength 降为 `personal`。混合来源不产生"部分已验证"这种中间状态，因为读者无法逐条区分。

kind 与 status 的合法组合：

| kind | planned | draft | validated | published | deprecated |
| --- | --- | --- | --- | --- | --- |
| knowledge | 允许 | 允许 | 允许 | 允许 | 允许 |
| index | 允许 | 允许 | 允许（走豁免记录） | 允许 | 允许 |
| reference | 允许 | 允许 | 允许（走豁免记录） | 允许 | 允许 |

`publishable` 的判定必须同时满足：`status == published`、`effective_confidentiality == public`、`validation_state ∈ {valid, exempt}`、无 `source_drift` 阻断项。任一不满足时 public 构建跳过该页，并在构建报告中列出原因。

互斥与前置约束：

- `planned` 不能有正文、sources、evidence、question_ids；
- `planned` 不能直接跳到 `validated` 或 `published`，必须先经过 `draft`；
- `deprecated` 与其他 status 互斥，是终态之一，只能通过显式修订回到 `draft`；
- `validated` 与 `published` 必须存在对应的 `validation_state ∈ {valid, exempt}`，否则自动回落到 `draft`；
- question 只能挂在 `status ∈ {validated, published}` 且 `kind: knowledge` 的 wiki 上——index 与 reference 页面不出题。

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
| 3 | 剥离 Markdown 行内标记：`` ` ``、`*`、`_`、`~`、`\` 转义符 | 原文里的 `constexpr` 与引文里的 constexpr 应视为相同 |
| 4 | 删除所有空白字符（空格、制表、换行、零宽字符 U+200B/FEFF、不换行空格 U+00A0） | 中文不依赖空格分词，中英文之间的空格纯属排版偏好 |
| 5 | 保留大小写 | 大小写在技术标识符里是语义性的（`Size` 与 `size`） |
| 6 | 保留数字与单位原样 | `4KB` 与 `4 KB` 经步骤 4 已等价，但不做数值换算 |

匹配规则：

- 规范化后做**子串包含**判断（引文 ⊆ 章节正文），不是相等判断；
- 匹配目标是 `source_refs` 命中的那个 locator 章节，不是整篇 source——引文出现在别的章节等于引错位置，判失败；
- 引文规范化后长度小于 `policy.yaml` 的 `quote_min_chars`（建议中文 12 字符）时判失败：太短的引文可以匹配到任何地方，不构成证据；
- 一条 claim 有多个 `source_refs` 时，每个 ref 各需一条引文，逐条匹配。

删除全部空白是这套规则里最关键的一步，也是对中文最稳的选择：它同时吸收了中英文间距、软换行、缩进和列表标记造成的差异。代价是英文引文中的词边界信息丢失（`in to` 与 `into` 变得相同），对技术文档的实际影响可以忽略。

失败时必须返回可诊断信息：规范化后的引文、章节的规范化长度、以及最长公共子串的位置和长度。只返回"不匹配"会让人无法判断是引错了章节、抄漏了半句，还是规范化规则太严。规范化规则的调整必须与 fixture 一起提交，避免为了让某一篇通过而悄悄放宽标准。

## 7. 单选题规范

### 7.1 Question Front Matter

~~~yaml
---
id: q-transformer-001
wiki_id: wiki-transformer
claim_ids: [c1]
type: single_choice
difficulty: 2
confidentiality: public
tags: [transformer]
enabled: true
wiki_content_sha256: "sha256:..."
wiki_evidence_sha256: "sha256:..."
---
~~~

### 7.1.1 Question 字段级契约

| 字段 | 必填 | 约束 |
| --- | --- | --- |
| id | 是 | 全库唯一，写入后不自动复用 |
| wiki_id | 是 | 必须指向已存在的 wiki；题目不能孤立存在 |
| claim_ids | 是 | 非空数组，每个 ID 必须存在于 `wiki_id` 的 `evidence` 中 |
| type | 是 | 第一阶段固定为 `single_choice` |
| difficulty | 是 | 1 至 5 的整数 |
| confidentiality | 是 | 缺省 `public`；有效等级从所属 wiki 传染 |
| tags | 否 | 缺省为空数组 |
| enabled | 是 | 由工具计算，只有确定性校验和答案证据校验都通过才为 true |
| wiki_content_sha256、wiki_evidence_sha256 | 生成 | 出题时所属 wiki 的 hash 快照，用于检测题目过期 |
| answer、explanation | 是 | 只存在于 local/practice 投影，不进入 public projection |

### 7.1.2 题目的证据约束

题目是唯一会被反复主动记忆的产物，一个错误的答案键会持续强化错误认知，因此它的门禁不能弱于 wiki：

1. `claim_ids` 非空，且全部命中所属 wiki 的 evidence；
2. 所属 wiki 的 `status` 必须是 `validated` 或 `published`；不能给 draft 出题，draft 的论断本身还没有通过证据验证；
3. 正确答案和解析中的事实必须被 `claim_ids` 覆盖，不得引入 wiki 没有的新结论；校验方式与 8.1 一致——要求模型给出解析所依据的 claim 原文片段，再确定性校验该片段确实存在于对应 claim 或其 locator 章节中；
4. 干扰项必须是"错误但相关"，不得与正确答案语义等价，也不得依赖 wiki 之外的知识才能排除；
5. 所属 wiki 的 `content_sha256` 或 `evidence_sha256` 变化后，题目置 `enabled: false` 并标记 `needs_review`，不静默删除、不静默保留；
6. wiki 被引 claim 删除后，题目直接失效并进入待处理清单。

题目重新校验不改变 wiki 的 LLM 验证报告；wiki 与 question 的验证是两条独立链路，只共享 claim 作为接口。

题目的门禁**严于** wiki 是有意的，不是不一致：wiki 走 8.2 的 claim 证据验证，题目在此之上还要额外校验答案键与解析都落在已验证 claim 覆盖范围内。原因是消费方式不同——wiki 是被阅读的，读者能看到证据强度并自行判断；题目是被反复主动记忆的，错误答案键会持续强化错误认知，没有第二道人工把关。因此不是所有 validated wiki 都适合出题，只有 claim 足够明确、可判真假的才行。

### 7.2 Question 正文模板

~~~markdown
# Transformer 基础概念

## 题干

Attention 中 Q、K、V 的主要作用是什么？

## 选项

- A. ...
- B. ...
- C. ...
- D. ...

## 正确答案

B

## 解析

解释正确选项，并说明其他选项为什么不正确。
~~~

第一阶段只支持 4 选 1：

- 恰好 4 个选项；
- 恰好 1 个正确答案；
- wiki_id 必须存在，且 wiki 已 validated 或 published；
- claim_ids 非空且全部可解析；
- 题目、答案和解析必须落在 claim_ids 覆盖的范围内；
- 答案和解析不进入 public build。

## 8. LLM 证据验证

### 8.1 验证职责

LLM 只负责判断 wiki claim 是否被 source 支持，不负责替代 source，不负责直接决定事实真伪，也不允许自由扩展 source 没有表达的结论。

验证输入：

- wiki 候选正文；
- wiki 的 evidence claim 列表；
- 对应 source 正文和章节；
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
      "source_refs": ["source-transformer-paper#已读取事实"],
      "supporting_quote": "注意力权重由 Q 与 K 的点积经 softmax 得到，再与 V 加权求和。",
      "reason": "来源明确描述了该机制"
    }
  ],
  "unmapped_claims": [],
  "contradictions": [],
  "missing_evidence": []
}
~~~

`supporting_quote` 必填且**必须逐字来自被引 locator 章节**。工具在收到响应后做一次确定性校验：按 6.9 的规范化规则把引文与该章节正文归一后做子串匹配，找不到即判 `unsupported`，无论模型自己给出什么 verdict。

这一步的作用是把一半判断从"相信模型"变成字符串匹配。没有它，模型倾向于给出宽松的 `supported`，而门禁没有任何机制能识别这种幻觉式支持。`synthesis` 类 claim 需要为每个 `source_ref` 各给一条引文；`inferred` 类 claim 的引文指向作为推理前提的原文，而不是结论本身。

验证还要求：temperature 设为 0；同一输入独立采样 3 次，三次 verdict 不一致时取最保守结果并降级为 `partially_supported`。这两条都是为了让判定可复现——一个不稳定的门禁比没有门禁更糟，因为它会让人误以为已经检查过了。

验证器自身的准确率必须被度量：维护一组人工标注的 fixture（既有真实支持、也有似是而非的伪支持），把精确率与召回率作为阶段三的退出门。不度量的门禁只是橡皮章。

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

LLM provider 未配置、网络不可用、返回格式错误或模型调用失败时：

- source 查询和 source 写入仍可用；
- wiki 可以生成 draft 候选；
- wiki 不得变为 validated 或 published；
- 不能使用“跳过验证”“默认通过”或“agent 判断通过”。

### 8.4 验证报告

每次验证保存：

~~~yaml
wiki_id:
validator_version:
model:
validated_at:
wiki_content_sha256:
wiki_evidence_sha256:
locator_sha256:
  source-transformer-paper#已读取事实: sha256:...
claims:
unmapped_claims:
contradictions:
verdict:
~~~

报告绑定的是三组 hash：wiki 正文、wiki evidence 块、以及**被实际引用的每个 locator 章节**，不是整个 source 文件的摘要 hash。这样修改 source 中未被引用的章节不会波及已验证的 wiki，避免一次错别字修正引发全库重验。报告还应记录验证提示词版本、schema 版本和输入 locator 列表，便于复现。报告放在 `state/llm-validation/` 或本地 artifact 中，不进入公开前端。报告不保存 API key、密码和敏感凭据。

`confidentiality: internal` 的 source 正文只能发送给 `policy.yaml` 中标记为 `internal_allowed` 的 LLM provider；没有这样的 provider 时，internal wiki 的验证返回 `unavailable` 并保持 draft，不得改用公开 provider。

### 8.5 验证报告失效规则

验证报告只有在下列条件全部满足时才有效：

1. wiki 当前 `content_sha256` 等于报告中的 `wiki_content_sha256`；
2. wiki 当前 `evidence_sha256` 等于报告中的 `wiki_evidence_sha256`；
3. 报告中每个 `locator_sha256[<locator>]` 等于该 source 章节当前的章节 hash；
4. 全部被引 locator 仍然存在，且上游 source 的 `origin`、`read_status`、`evidence_status`、`confidentiality` 未变化；
5. validator、schema 和 prompt 版本仍在 `policy.yaml` 声明的兼容范围内；
6. 报告 verdict 为 `pass`，且没有 partially supported、unsupported、contradicted 或 unmapped claim。

按 6.6 的分类，tags、aliases、related、title 和 domain 变化不影响以上任何一条，不触发重新验证。

任一条件不满足，页面都必须回到 `draft` 或标记为 `validation_expired`。`validation_expired` 是内部计算状态，不是允许 public build 的状态；重新验证通过后才可回到 `validated`。

prompt 或 validator 升级时，`policy.yaml` 必须显式声明兼容策略：`compatible` 表示旧报告继续有效，`breaking` 表示全量重验。默认按 `breaking` 处理，避免静默沿用旧标准。

## 9. 写入操作协议

所有写入必须是两阶段 operation：

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

1. 获取仓库级写锁（见 9.8）；
2. 检查网络与归档可达性（`require_network`，见 5.9）；
3. 重新检查目标文件 hash；
4. 重新检查 source/wiki 输入 hash；
5. hash 不匹配则 operation 失效；
6. 写入 staging 目录；
7. 原子替换目标文件；
8. 重建索引；
9. 运行最终校验；
10. 失败时保留旧文件并清理 staging；
11. 释放写锁。

### 9.3 Operation 状态和幂等性

```text
created
  -> previewed
  -> awaiting_confirmation
  -> applied

previewed / awaiting_confirmation
  -> expired       (超过有效期或输入 hash 变化)
  -> rejected      (用户拒绝)
  -> failed        (应用或最终校验失败)
```

`operation_id` 使用随机 UUID，不以标题或时间戳代替。一个 operation 只能应用一次；重复 apply 必须返回已完成或已失效，而不是再次覆盖文件。批量操作必须把每个目标文件、before hash、after hash 和失败阶段写入 manifest。

### 9.4 禁止操作

Skill 和知识库工具禁止：

- 无 source 直接写 wiki；
- 直接修改 queries/；
- 直接修改 frontend/、backend/；
- 自动删除、移动、覆盖和重命名页面；
- 自动 commit、push、发布；
- 通过模糊的“继续”“好的”确认未知范围的批量写入。

### 9.5 三类对象的写入准入

source、wiki、question 都不能"随便增加"。preview 阶段必须逐条检查下表，任一项不满足即 blocked，并返回缺失项和修复动作：

| 检查项 | source | wiki | question |
| --- | --- | --- | --- |
| schema 与必填字段 | 必须通过 | 必须通过 | 必须通过 |
| 来源完备性（5.9） | 必须满足三者之一 | 不适用 | 不适用 |
| 网络可达（`require_network`） | 网络来源必须满足 | 必须满足 | 必须满足 |
| ID 全库唯一（含已挂载 private vault） | 必须 | 必须 | 必须 |
| domain 在词表内 | 必须 | 必须 | 继承 wiki |
| confidentiality 与所在 vault 一致 | 必须 | 必须，且不低于上游 source | 必须，且不低于所属 wiki |
| 内网 URL 与 public 声明冲突 | 阻断 | 不适用 | 不适用 |
| 正文模板章节齐全 | 必须 | 必须 | 必须（题干/选项/答案/解析） |
| 证据边界与 read_status 一致 | 必须 | 不适用 | 不适用 |
| external 必须有 url 与 retrieval | 必须 | 不适用 | 不适用 |
| 上游对象存在且可解析 | 不适用 | sources 非空且全部存在 | wiki_id 存在 |
| 上游状态门槛 | 不适用 | 不能只引用 metadata-only source | wiki 必须 validated 或 published |
| claim 映射 | 不适用 | 每个核心论断有 claim_id 和 locator | claim_ids 非空且全部命中 wiki evidence |
| 支持类型兼容矩阵（6.5） | 不适用 | 必须通过 | 不适用 |
| LLM 证据验证 | 不需要 | 必须 pass 才能离开 draft | 答案与解析必须被 claim 覆盖 |
| 结构约束 | 不适用 | 不适用 | 恰好 4 选项、恰好 1 正确答案 |
| hash 快照写入 | content_sha256、locator_sha256 | content_sha256、evidence_sha256 | wiki 的两个 hash 快照 |

新增顺序是强约束：没有 source 不能建 wiki，没有 validated wiki 不能建 question。这条链上任何一层想跳过，正确做法都是补齐上一层，而不是放宽当前层的检查。

来源完备性和联网要求也是同一性质的约束：没有来源的内容不允许写入，`require_network` 生效时离线不允许 apply。preview 可以在离线状态下生成候选供阅读，但不得进入 `awaiting_confirmation` 状态，避免留下一批永远无法完成的待确认操作。

### 9.6 废弃与删除

内容会过时，也会被发现本来就是错的。9.4 禁止的是**自动**删除，不是禁止删除；需要一个显式、可预览、可回滚的退役路径，否则错误内容只能靠手工乱改。

两级操作，都必须走 preview/apply：

~~~text
retire   标记 status: deprecated，保留文件与路由
purge    真正删除文件，需要 retire 已生效且引用已清理
~~~

`retire` 的效果：从 public build 与 public 索引移除；从 RAG 索引移除对应 chunk；关联 question 置 `enabled: false` 并标记 `needs_review`；保留旧路由指向一个"此页已废弃"的提示页，避免外部链接直接 404；在 backlinks 中把该页标记为废弃而不是删除链接。

`purge` 的前置条件（任一不满足即阻断）：

1. 目标已处于 `deprecated`；
2. 没有任何 published wiki 的 claim 引用它；
3. 引用它的 question 已删除或已改绑；
4. `part_of` 子对象已处理完毕；
5. route map 中已登记旧路径的最终归属（重定向目标或明确的墓碑页）。

删除的是文件，不是历史：`purge` 前必须把对象的 ID、标题、最后内容 hash 和废弃原因写入 `state/operations/` 的 manifest。这样将来遇到同一份错误资料时，能知道它曾被判定为错误并且原因是什么，不会再次原样引入。

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

ID、标题和路径都会需要调整，而一次改名要同时波及：反向索引、backlinks、`related`、`part_of`、`question_ids`、`sources` 引用、route map、验证报告中的 locator 前缀。手工改这些一定会漏，因此重命名必须是一等操作，而不是"人工去改"。

~~~text
rename   改 ID（连带所有引用）
move     改路径与 domain（不改 ID）
retitle  改 title（不影响引用）
~~~

`rename` 的 preview 必须列出全部受影响对象与文件，并区分两类改动：引用更新（机械替换，可自动）与内容改写（正文里提到旧名称的自然语言表述，需人工确认）。apply 时全部改动在一个 operation 内原子完成，任一文件失败则整体回滚。

规则：

- 旧 ID 进入 route map 并保留重定向，避免外部链接与旧笔记失效；
- 旧 ID 不得被复用为新对象的 ID；
- 改 ID 不改变正文内容，因此 `content_sha256` 不变，验证报告仍然有效——但报告中的 locator 前缀需要同步重写，这是纯机械替换；
- `move` 改变 domain 时必须重新校验 domain 与目录一致性；
- `retitle` 只影响显示名，不触发任何重验（title 属于 6.6 的分类字段）。

### 9.8 并发与锁

单用户环境仍然存在三方并发：Agent、本地后端、编辑器。`before_sha256` 检查与原子替换之间存在窗口，两个 apply 交错会造成一方的写入被静默覆盖。

- 所有 `apply`、`retire`、`purge`、`rename` 和索引生成必须先获取仓库级排他锁（`state/.lock`，记录持有者、operation_id 和获取时间）；
- 锁只保护写入，查询与 preview 不加锁；
- 锁必须有超时与陈旧锁清理（记录 PID 与时间戳），避免异常退出后永久阻塞；
- 拿不到锁时返回 `blocked` 并说明当前持有者，不排队等待、不强行抢占。

## 10. 四条工作流

### 10.1 查询阅读

公开模式：

~~~text
Pagefind -> published wiki
~~~

本地模式：

~~~text
SQLite FTS5 -> sources + wiki + metadata
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
practice:
evidence:
limits:
next_gate:
~~~

Agent 不直接扫描任意 Markdown，而是调用本地 CLI、生成索引或 FastAPI 查询接口。

### 10.2 写入

固定写入顺序：

~~~text
source -> wiki -> question -> validate -> index -> build
~~~

Source 和 wiki 是两个独立 operation：

```text
source preview -> 用户确认 -> 写入 sources -> source 校验
wiki preview   -> 确定性校验 -> LLM 验证 -> 用户确认 -> 写入 wiki
```

如果用户要求“把一段话写成 wiki”，但没有 source，必须先创建 personal source，不能在同一个隐式操作中跳过 source 层。LLM 验证通过前，不能向用户展示“可应用写入”的 wiki 候选。

### 10.3 索引

生成六张反向索引：

~~~text
by-domain
by-tag
by-alias
by-link
by-source
by-question
~~~

同时生成：

~~~text
catalog.json
graph.json
rag-index.jsonl
backlog.json
~~~

`backlog.json` 汇总 `status: planned` 条目和 `content_verdict: pending-review` 的待处理项，是"还需要写什么"的唯一入口。`deprecated` 页面单独成表，供查询时给出替代目标。

public index 只包含 `status: published` 且 `confidentiality: public` 的 wiki；local index 包含 sources、wiki 和 practice。`planned` 与 `deprecated` 只进 local index 的元数据表，不进正文检索和 RAG 索引。

索引文件必须带有生成器版本、生成时间、输入集合 hash 和 schema 版本。索引生成失败时，旧索引保持不变；不能留下只有一半内容的新索引。

知识库会持续变大，`planned` 条目、按抽象层级拆分出的子 source 和归档快照都会推高对象数量，这是预期结果而不是问题。索引生成必须为此留出余量：

- 每个对象记录 `content_sha256` 与上次入索引时的 hash，只重算发生变化的对象；
- 全量重建保留为可显式触发的操作（schema 或生成器版本变化时必须全量）；
- 增量结果必须与全量结果一致，这条要有对照测试，否则增量会静默漂移；
- 对象数超过 `policy.yaml` 中的阈值时，`catalog.json` 与 `graph.json` 按 domain 分片输出，避免单文件过大拖慢前端首屏。

`planned` 条目保留为独立文件而不是集中清单：它们是未来的写作入口，需要能被直接打开、被链接引用、被 backlinks 统计。文件数增长由索引和 RAG 承担，不通过压缩对象模型来回避。

### 10.4 做题

第一阶段 API：

~~~text
GET  /api/quiz/next
POST /api/quiz/{question_id}/answer
GET  /api/review/due
GET  /api/review/stats
GET  /api/review/export
POST /api/review/import
~~~

复习流程：

1. 根据主题、难度和到期时间选题；
2. 先展示题目和选项；
3. 提交后判分；
4. 展示正确答案、解析和关联 wiki；
5. 使用 again、hard、good、easy 更新 FSRS；
6. 记录下一次复习时间。

复习状态只保存到本地，不进入 Git 和公开静态文件。

## 11. 索引与查询技术

### 11.1 Public index

~~~text
wiki.status == published && confidentiality == public
  -> queries/public
  -> Astro prepare-content
  -> Pagefind
  -> GitHub Pages
~~~

### 11.2 Local index

~~~text
sources + wiki + practice
  -> queries/local
  -> SQLite FTS5
  -> FastAPI
  -> 本地前端 / Agent Skill
~~~

第一阶段的基础检索不引入 Elasticsearch、独立向量数据库或 LangChain。知识规模、部署形态和个人查询需求优先要求确定性、可解释、可离线运行。RAG 作为本地自然语言问答和知识综合能力接入，但不改变 source/wiki 的内容真相源。

规模假设是"最终会很大"，而不是"永远只有几百篇"。这直接影响两处选型：向量检索从一开始就用可持久化、可增量更新的方案（FAISS 或 sqlite-vec），不用一次性全量加载的内存暴力检索；FTS5 与向量索引都必须支持按对象增量更新，避免每次写入都全库重建。`archive/text/` 也是 RAG 的合法输入之一——归档正文比人工整理的 source 摘要更完整，适合作为召回材料，但**它不是证据载体**：claim 的 locator 只能指向 source 章节，不能指向归档原文。

### 11.3 查询、RAG 和证据验证的边界

“查找文档”和“基于文档回答问题”是两种不同能力：

| 能力 | 是否需要 RAG | 第一阶段方案 |
| --- | --- | --- |
| 根据 ID、标题、标签、关键词找页面 | 否 | Pagefind、SQLite FTS5、反向索引 |
| 根据自然语言问题返回相关文档片段 | 可选 | FTS5，后续增加向量召回 |
| 基于多个文档片段生成回答 | 是 | Retriever + LLM + citations |
| 基于 source 生成 wiki 草稿 | 可使用 | RAG 辅助候选生成，仍须 evidence validation |
| 根据 wiki 生成题目 | 可使用 | RAG 找相关 claim，题目仍需 claim 绑定和答案证据校验 |

RAG 的职责是“找到回答所需的上下文并组织答案”；Evidence Validator 的职责是“判断 wiki claim 是否被 source 支持”。RAG 检索到片段不能直接证明最终论断，也不能直接将页面变为 `validated` 或 `published`。

### 11.4 RAG 标准处理链

```text
用户问题
  -> 查询解析
  -> FTS5 关键词召回
  -> 可选 Embedding 召回
  -> 合并去重（RRF）
  -> 可选 Reranker
  -> 选取 source/wiki 片段
  -> LLM 生成回答
  -> 引用和 locator 校验
  -> 返回答案、引用和局限
```

本地 RAG 索引由 `sources/` 和 `wiki/` 投影生成。每个 chunk 必须保留对象身份和证据定位，不能只保存一段没有来源的纯文本：

```json
{
  "chunk_id": "source-transformer-paper:已读取事实:001",
  "object_type": "source",
  "object_id": "source-transformer-paper",
  "vault": "public",
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

`internal` chunk 只存在于 private vault 对应的本地索引文件中，不写入公开仓库；`/api/ask` 的回答如果引用了 internal chunk，响应必须标记 `confidentiality: internal` 且不写入可共享的回答缓存。

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

### 11.6 推荐技术组合

第一阶段采用成熟组件加薄适配层：

```text
Markdown + YAML
  -> MyKnowledge 规范化分块
  -> SQLite FTS5
  -> sentence-transformers / FlagEmbedding
  -> FAISS 本地向量索引
  -> RRF 混合召回
  -> BGE Reranker（可选）
  -> OpenAI-compatible LLM
  -> citation/locator 校验
```

推荐组件：

| 能力 | 推荐 | 说明 |
| --- | --- | --- |
| 关键词检索 | SQLite FTS5 | 基础能力，离线、确定性、无外部服务 |
| Embedding | `BAAI/bge-m3` 或 `bge-small-zh-v1.5` | 根据机器资源选择多语或轻量中文模型 |
| 向量检索 | FAISS | 本地持久化简单，适合个人知识库第一版 |
| Reranker | `BAAI/bge-reranker-v2-m3` | 召回候选较多时再启用 |
| RAG 编排 | 自有 Retriever 接口，必要时接 LlamaIndex/Haystack | 保持 source、hash、locator 和状态由 MyKnowledge 控制 |
| 效果评估 | 自定义引用测试，必要时接 Ragas/DeepEval | 不能用评估分数替代 claim evidence 验证 |

不建议第一版直接引入 Elasticsearch、独立向量数据库、RAGFlow、Dify 或 LangChain。未来若需要独立服务，再将 Qdrant、pgvector 或 OpenSearch 接到同一个 Retriever 接口后面。

### 11.7 Retriever 接口和索引工具

```python
class Retriever:
    def search(self, query, scope, top_k=8):
        ...
```

第一阶段实现：

```text
FtsRetriever
EmbeddingRetriever
HybridRetriever
```

建议工具：

```text
tools/
├── build_rag_index.py
├── retrieve.py
├── rerank.py
├── answer_with_citations.py
└── validate_citations.py
```

这些工具只负责索引、召回、回答和引用校验，不拥有 source/wiki 写入权限。`queries/local/rag-index.jsonl` 和 FAISS 文件都是生成物，不能人工编辑。

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
  "scope": "wiki",
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
      "source_ref": "source-transformer-paper#已读取事实",
      "text": "..."
    }
  ],
  "retrieval": {"method": "hybrid", "chunks": 6},
  "limits": []
}
```

Agent Skill 增加 `ask` 模式；`query` 继续负责确定性检索，`synthesize` 可以调用 RAG 生成 wiki draft，但必须进入原有的 source 检查、claim 映射、LLM 验证和 preview/apply 流程。

### 11.9 RAG 分阶段落地

```text
阶段 A：SQLite FTS5 和 metadata 查询
阶段 B：Embedding + FAISS 语义召回
阶段 C：FTS5 + 向量的 HybridRetriever（RRF）
阶段 D：Reranker、引用校验和回答缓存
阶段 E：必要时评估 Qdrant/pgvector/GraphRAG
```

每个阶段都必须保留离线查询能力。LLM、Embedding 或向量索引不可用时，确定性查询仍可用；RAG 问答必须返回 `unavailable` 或明确降级，不能伪造“已基于文档回答”。

## 12. FastAPI 本地后端

核心 API：

~~~text
GET  /api/health
GET  /api/search
GET  /api/page/{id}
GET  /api/page/{id}/sources
GET  /api/page/{id}/backlinks
POST /api/retrieve
POST /api/ask
POST /api/operations/preview
POST /api/operations/apply
POST /api/wiki/{id}/validate
GET  /api/quiz/next
POST /api/quiz/{id}/answer
GET  /api/review/due
GET  /api/review/export
POST /api/review/import
~~~

后端职责：

- 加载 local index；
- 建立 SQLite FTS5；
- 执行结构化查询；
- 返回 wiki 和 source 证据；
- 执行写入 preview/apply；
- 调用 LLM 验证器；
- 执行题目判分和复习调度；
- 保存本地 review state。

技术选择：

| 能力 | 方案 | 选择原因 |
| --- | --- | --- |
| API | FastAPI | Python 工具链和结构化 schema 适配好 |
| 数据校验 | Pydantic + PyYAML | 复用 Python schema 能力 |
| 全文检索 | SQLite FTS5 | 无外部服务，适合个人知识库 |
| LLM 输出 | OpenAI-compatible structured output | 不绑定供应商，便于切换模型 |
| 复习 | FSRS/Anki 兼容库 | 不自行实现记忆调度算法 |

后端不是新的内容真相源。它启动时读取仓库文件和生成索引，写入时只通过 operation service 生成 staging 并原子应用；SQLite 只保存检索索引和本地 review state，不能直接修改 source/wiki 正文。

### 12.1 离线降级

未启动后端时，Agent 和前端仍可通过 `tools/query.py` 读取 `queries/public` 或静态 catalog 完成离线查询。以下能力必须明确返回 `unavailable`，不能伪造成功：LLM 验证、写入 apply、FSRS 持久化同步和 local source 全文检索。后端恢复后再重建 local index，不自动补写用户内容。

完全断网时的能力边界见 5.9：查询、阅读、做题和复习全部可用，写入不可用。离线时的正确用法是"读和练"；`local-file` 与 `personal-note` 是 `allow_offline_kinds` 中有意保留的窄例外。不得为了让页面通过而放宽证据要求或跳过归档。

## 13. Astro 双运行模式

### 13.1 公开静态模式

- 只读取 wiki/；
- 只包含 status: published；
- 只建立 wiki Pagefind 索引；
- 图谱只展示 wiki 节点；
- 不展示 sources、题目答案、解析和验证报告；
- 无 FastAPI 时仍可正常浏览和搜索。

### 13.2 本地完整模式

- Astro 开发服务器代理 /api 到 FastAPI；
- 查询可以覆盖 sources、wiki 和本地 metadata；
- 页面可以查看 source 证据和验证状态；
- 首页提供今日复习、错题和查询入口；
- 后端不可用时退化为公开 wiki 阅读模式。

### 13.3 Public leak gate

静态构建结束后必须扫描 dist/：

- 不得出现 sources/ 正文；
- 不得出现 practice/ 答案和解析；
- 不得出现 state/；
- 不得出现 archive/ 中的任何归档正文或原始文件；
- 不得出现 LLM 验证报告；
- 不得出现任何 `confidentiality: internal` 对象的 ID、标题、URL 和正文；
- 文章数量必须等于 public 且 published 的 wiki 数量；
- catalog、graph 和 Pagefind 数据只能来自 public wiki 投影。

保密分级的门禁不止在 dist/。本仓库是公开仓库，因此 internal 内容的第一道防线是"根本不写进来"：

- `tools/validate_pages.py` 必须拒绝 public vault 中任何 `confidentiality: internal` 的文件；
- 提交前检查（`knowledge-check.yml` 与本地 pre-commit）扫描待提交文件，命中 internal 声明、内网域名模式或 private vault 路径即失败；
- private vault 的绝对路径不写入 public 仓库中的任何生成物，`queries/public` 不含 internal 对象的存在性信息（连"有一篇 internal wiki"都不暴露）。

Public projection 不复制 source 正文、归档快照、题目答案、题目解析、验证报告、操作 manifest 和复习状态。归档副本是第三方内容的本地复制件，只用于个人复核，把它发布到公开站点等于重新发布他人内容，必须由 leak gate 硬拦。wiki 中的“证据映射”可以保留为引用信息，但只能包含 source ID/章节等 locator，不得把 source 正文内联到静态页面。构建前后都要执行一次 allowlist/denylist 扫描，避免模板或错误 import 把 local 数据带入 dist。

## 14. Agent Skill

Skill 位置：

~~~text
/Users/zhouzijian01/Desktop/workspace/code/kinchow/zhouzijian-skills/skills/myknowledge/
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── page-schemas.md
│   ├── write-policy.md
│   ├── query-contract.md
│   └── workflow-modes.md
└── scripts/
    ├── detect_root.py
    └── invoke.py
~~~

支持模式：

~~~text
query
read
ask
ingest
synthesize
question
index
quiz
audit
~~~

Skill 默认只读。Skill 不实现第二套业务逻辑，而是调用 MyKnowledge 的 CLI 或 FastAPI：

~~~text
myknowledge skill
  -> tools/query.py
  -> tools/read_page.py
  -> tools/create_source.py
  -> tools/create_wiki.py
  -> tools/create_question.py
  -> tools/validate_wiki_evidence.py
  -> tools/generate_indices.py
~~~

Skill 只负责：

- 发现 MyKnowledge 根目录；
- 自然语言模式路由；
- 调用 FastAPI 或离线 CLI；
- 强制 preview/apply；
- 传递 validation、evidence 和 limits；
- 把错误以结构化结果返回给 Agent。

### 14.1 Agent 统一输出契约

所有 Skill 模式都返回相同的顶层字段，字段没有值时使用空数组、空对象或明确的 `null`，不省略字段：

```yaml
status: ok | preview | applied | rejected | blocked | error
operation_id: null
wiki: []
sources: []
claims: []
strength: null
validation: {}
diff: {}
changed_files: []
pending: []
next_gate: null
```

`strength` 是 6.7 定义的证据强度标识（`verified`、`attested`、`personal`、`reference`、`index`），查询和阅读结果都必须返回它，让 Agent 在引用知识库内容时能区分"已验证的外部事实"和"我的个人理解"。`pending` 承载 `planned` 条目和待复核项。

查询和阅读操作的 `operation_id`、`diff`、`changed_files` 必须为空；写入 preview 必须包含 `operation_id`、`diff_sha256`、确定性校验和 LLM 校验结果。错误必须说明阻断规则和下一步动作，不能只返回自然语言错误。

写入模式的强制决策表：

| 请求 | 无 source | 有 source 但验证失败 | 验证通过未确认 | 同 operation_id 且 hash 未变 |
| --- | --- | --- | --- | --- |
| ingest source | 允许创建 source preview | 不适用 | 等待确认 | 允许 apply |
| synthesize wiki | 拒绝，先提示创建 source | 保持 draft | 等待用户确认 | 允许 apply |
| question | 拒绝：无 validated/published wiki 或无可绑定 claim 时不出题 | 题目保持 `enabled: false` | 等待确认 | 允许 apply |
| index | 只允许调用生成器 | 生成 public 时跳过未发布和 internal 内容 | 不适用 | 允许生成 |

写入 preview 的结果中必须回传 `confidentiality` 和有效等级的来源（自身声明还是上游传染），让用户在确认前就能看到这次写入会落到哪个 vault。目标 vault 由 `confidentiality` 决定，Agent 不能自选路径。

Skill 不根据对话上下文猜测用户确认范围；“确认”必须能解析为当前 `operation_id`。用户修改 source 或 wiki 后，旧 operation 自动失效，必须重新 preview。

## 15. 工具模块边界

~~~text
tools/
├── common.py
├── query.py
├── read_page.py
├── create_source.py
├── create_wiki.py
├── create_question.py
├── validate_pages.py
├── validate_wiki_evidence.py
├── check_sources.py
├── archive_source.py
├── rename_page.py
├── retire_page.py
├── generate_indices.py
├── build_rag_index.py
├── retrieve.py
├── rerank.py
├── answer_with_citations.py
├── validate_citations.py
└── task_manifest.py
~~~

建议职责：

- common.py：root、vault 挂载、路径安全、Front Matter、hash 和页面读取；
- create_source.py：source 模板、preview 和 apply；
- create_wiki.py：source 检查、claim/evidence、preview 和 apply；
- create_question.py：claim 绑定、4 选 1 校验、答案证据校验和写入；
- validate_pages.py：确定性 schema、引用、链接、状态组合和保密分级校验；
- validate_wiki_evidence.py：LLM adapter、结构化输出、引文逐字校验和报告；
- check_sources.py：外部链接巡检、归档快照更新和漂移标记；
- archive_source.py：抓取、离线副本导入（`--from-file`）、正文提取、压缩、内容寻址写入和 manifest 维护；
- rename_page.py：ID/路径变更、引用同步、route map 和原子回滚；
- retire_page.py：`retire` 与 `purge` 的前置检查、preview 和 apply；
- generate_indices.py：public/local 索引原子生成；
- build_rag_index.py：规范化分块、Embedding 和本地向量索引；
- retrieve.py：FTS、向量和混合召回；
- rerank.py：可选候选重排；
- answer_with_citations.py：基于检索片段生成带引用的回答；
- validate_citations.py：检查回答和 claim 是否能定位到 source locator；
- query.py：离线查询和统一 QueryResult；
- task_manifest.py：记录操作范围、输入 hash、结果和失败阶段。

所有公共入口只能委托这些领域工具，不能在 CLI、FastAPI 和 Skill 中重复实现规则。

## 16. 迁移策略

当前 docs/ 下 277 个 Markdown 文件不能直接批量标记为 published，因为它们没有 source、claim 映射和 LLM 验证。但"277 篇文章"并不是实际迁移量——实测的形态分布决定了绝大多数文件根本不走完整证据链。

### 16.1 存量实测分布

| 形态 | 文件数 | 字符量 | 迁移去向 |
| --- | --- | --- | --- |
| 空文件（0 字节） | 16 | 0 | `status: planned` 或删除 |
| 导航页（`contents.md`） | 71 | 20809 | `kind: index`，走 6.7 豁免 |
| 占位 stub（正文 ≤200 字） | 54 | 9886 | `status: planned` 待写清单 |
| 短笔记（201-800 字） | 45 | 38575 | 完整链路，成本较低 |
| 实质文章（>800 字） | 78 | 297663 | 完整链路，主要成本 |
| 资源链接清单 | 1 | 2891 | `kind: reference` |
| 超大聚合页（需先拆分） | 12 | 233251 | 先按 5.7 抽象层级拆分，再入链路 |

真正承载内容的是实质文章与超大聚合页共 90 个文件，占全库字符量的 88%；141 个文件（空文件、导航页、占位 stub）没有可迁移的正文。

出处线索的实测结论：只有 59/277 个文件含任何外链，实质文章中 48/78 篇完全没有 URL；git 历史是一次性批量导入（18 个 commit，全部文件同期首次提交），无法提供逐篇来源线索。因此**无出处内容的处理方式是迁移的主要工作量和主要风险**，不是技术实现。

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
- 单选题 4 选 1；
- source 正文和章节超过阻断阈值时必须被拒绝并返回拆分建议；
- `local-file` source 缺少 path 或 file_sha256 必须失败；
- `local-file` 路径无法解析时标记 unresolved，不得判定为证据缺失；
- 每类豁免必须命中对应的替代检查，不得同时豁免确定性校验；
- `planned` 页面不得出现在 public build 和 RAG 索引中；
- `deprecated` 页面不得被新 claim 引用；
- `purge` 在存在引用时必须被阻断；
- `rename` 必须同步全部引用、backlinks 和 route map，任一失败整体回滚；
- 旧 ID 不得被复用；
- 并发 apply 必须被写锁串行化，不得出现静默覆盖；
- kind × status 的每个非法组合都必须被拒绝；
- 派生字段被手写时必须以工具计算结果覆盖；
- `supporting_quote` 不能逐字匹配到 locator 章节时必须判 unsupported；
- 增量索引结果必须与全量重建结果一致；
- 归档正文缺失时 `common-knowledge` 豁免必须失败；
- `common-knowledge` 的 `supporting_quote` 无法逐字匹配归档正文时必须失败；
- `archive/raw/` 在 LFS 规则未配置时必须拒绝写入并降级为 text-only；
- 无来源的 source 写入必须被拒绝（三种完备形态之一都不满足）；
- `require_network` 生效且离线时 apply 必须被拒绝，且不留下待确认操作；
- `metadata-only` source 缺少入口页归档时必须失败；
- `offline-copy` 缺少 `copy_note` 或归档正文时必须失败；
- `url_status: dead` 不得触发可达性检查失败，也不得阻断已有页面发布；
- 引文规范化：全角半角、中英文空格、Markdown 行内标记、零宽字符的等价性用例；
- 引文短于 `quote_min_chars` 必须失败；
- 引文出现在其他章节而非被引 locator 时必须失败；
- 题目 claim_ids 必须命中 wiki evidence；
- 引用 draft wiki 的题目必须被拒绝；
- wiki 正文或 evidence 变化后题目自动 `enabled: false`；
- public vault 中出现 internal 声明必须失败；
- 内网 URL 声明为 public 必须失败；
- wiki 引用 internal source 时有效等级必须升级且不可 published；
- private vault 未挂载时不得把 internal 引用误判为 source 缺失；
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
- 豁免页面生成 `verdict: exempt` 记录，且内容变化后同样失效；
- 豁免类型变化后不得沿用旧记录。

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

- public 页面数量等于 published wiki 数量；
- draft/validated 页面不进入构建；
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
| LLM 不可用/格式错误 | 不写入 wiki | source 可用，wiki 保持 draft | 稍后重新验证 |
| hash 变化 | 不写入目标 | operation expired | 重新 preview |
| 题目引用的 claim 变化或被删除 | 题目文件保留 | `enabled: false` + needs_review | 重新出题或改绑 claim |
| public vault 中出现 internal 声明 | 不写入 | blocked，提示改用 private vault | 挂载 private vault 后重做 |
| 外部原文变化或链接失效 | 不改内容 | source_drift / link_rot 提示 | 人工决定是否重读修订 |
| staging 或索引失败 | 旧页面和旧索引保持不变 | apply failed | 清理 staging，修复后重试 |
| public leak gate 失败 | 不发布 dist | build blocked | 找出泄漏字段并修复投影 |

### 17.6 可观测性和审计

每次 query、preview、apply、validate、index、quiz 操作记录结构化事件：`operation_id`、模式、输入 hash、目标 ID、状态、失败阶段和耗时。日志只保存必要的诊断信息，source 正文、API key、Authorization header 和用户隐私字段不得写入日志。审计记录可删除或归档，但不能被用来绕过当前校验。

## 18. 实施阶段

### 阶段一：规范基础

- 创建 schema、词表、policy 和三类模板；
- 定义 `config/vaults.yaml` 与保密分级校验；
- 实现 6.6 的 hash 契约（正文 hash、evidence hash、locator hash）；
- 实现 Front Matter、路径安全和页面读取；
- 实现 source/wiki/question 确定性校验和 9.5 写入准入表。

### 阶段二：受控写入

- 实现 operation preview/apply；
- 实现 before hash、diff hash 和原子写入；
- 实现仓库级写锁与陈旧锁清理；
- 实现归档抓取、正文提取、压缩与内容寻址存储；
- 实现 rename/move 与 retire/purge 操作；
- 实现失败清理和回滚；
- 禁止直接文件写入。

### 阶段三：LLM 证据验证

- 实现 OpenAI-compatible adapter；
- 实现 claim 逐条验证；
- 保存验证报告和内容 hash；
- 没有 provider 时严格保持 draft。

### 阶段四：索引和后端

- 生成 public/local 两套索引；
- 接入 SQLite FTS5；
- 实现 FastAPI query/read/source/backlink API；
- 接入题库和本地复习状态；
- 先实现 `FtsRetriever`，再按阶段增加 Embedding、FAISS、HybridRetriever 和 Reranker；
- 实现 `/api/retrieve`、`/api/ask` 及引用定位校验；
- RAG 不可用时保留确定性查询，并明确返回降级状态。

### 阶段五：静态前端

- 将 Astro 输入切换为 published wiki；
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
| 规范基础 | 无 | schema、词表、模板、validator fixtures | 非法页面全部能被拒绝 |
| 受控写入 | 规范基础 | operation service、manifest、staging | preview 不改工作树，apply 可回滚 |
| LLM 验证 | 受控写入 | adapter、结构化 report、失效检查 | provider 失败时 fail-closed |
| 索引和后端 | 规范基础 | public/local index、SQLite、FastAPI | CLI/API QueryResult 一致 |
| 静态前端 | public index | wiki-only build、leak gate | dist 只含 published wiki |
| Agent Skill | 受控写入、查询 API | `myknowledge` skill | Agent 不能绕过 writer 和 validator |
| 内容迁移 | 前六阶段 | source、wiki、question、route map | 每页都有证据和明确发布状态 |

阶段之间不允许以“代码已合入”代替退出门；只有对应的测试、报告或人工确认记录齐全，阶段才算完成。

## 19. 完成标准

系统完成必须同时满足：

- source、wiki、question 都有统一 schema 和模板；
- 无 source 不能写 `kind: knowledge` wiki，无 validated wiki 不能写 question；
- `kind: knowledge` wiki 必须有 claim-level evidence，question 必须绑定 claim_id；
- published wiki 必须有通过 hash 绑定的验证记录（正常路径为 LLM report，豁免路径为 exempt 记录）；
- 每个页面对读者可见自己的证据强度；
- 每个网络来源都有明确出处和本地归档快照；
- 内容 hash 只覆盖正文和语义字段，分类字段变更不触发重验；
- internal 内容不进入公开仓库和公开构建；
- LLM 不可用时不能发布；
- public 构建只包含 published wiki；
- local 后端可查询 source、wiki 和题目；
- 单选题可以判分并进入 FSRS 复习；
- Agent Skill 支持四条工作流，但写入不可绕过规范；
- preview/apply 可追踪、可失效、可回滚；
- 旧内容迁移有清单、route map 和明确的 completed/pending 边界。

完成标准按三类证据验收：

| 类别 | 可接受证据 | 不可替代的证据 |
| --- | --- | --- |
| 静态/代码 | 单元测试、schema 报告、构建日志 | 不能代替真实 LLM 或内容正确性 |
| 运行能力 | FastAPI smoke、查询/做题端到端测试 | 不能声称已经完成内容迁移 |
| 内容质量 | source locator、claim 验证报告、人工确认记录 | 不能用搜索摘要或模型自信度代替 |

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
  -> published wiki
  -> 静态展示 / 本地查询 / Agent 查询
~~~

## 20. 参考实现和对标

- [Quartz authoring content](https://github.com/jackyzha0/quartz/blob/v4/docs/authoring%20content.md)：Markdown、Front Matter、别名和内容发布。
- [Quartz graph view](https://github.com/jackyzha0/quartz/blob/v4/docs/features/graph%20view.md)：本地图谱和全局图谱。
- [Quartz backlinks](https://github.com/jackyzha0/quartz/blob/v4/docs/features/backlinks.md)：反向链接导航。
- [Dendron](https://github.com/dendronhq/dendron/blob/master/README.md)：渐进结构、模板、Git vault 和链接重构。
- [Logseq Markdown Syntax](https://github.com/logseq/logseq/blob/master/docs/logseq-markdown-syntax.md)：属性、引用、块和任务语义。
- [FSRS](https://github.com/open-spaced-repetition/free-spaced-repetition-scheduler/blob/main/README.md)：本地间隔复习调度。
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
| Anki/FSRS | 复习调度和导入导出 | 不负责知识证据和内容管理 | 仅用于 question review state |
| kernelwiki-kunlun | fail-closed、manifest、证据边界 | 其领域词表和运行环境不适合 MyKnowledge | 复用流程思想，重新定义领域 schema |

因此，第一阶段的核心不是增加更多 AI 功能，而是先把“可追溯写入”和“不可绕过发布门禁”做成确定性基础。语义检索、自动摘要和更复杂题型都必须作为后续消费者接入，不能改变 source -> evidence -> wiki 的主链路。

## 21. 规范 ID 基线

本文是系统规范的唯一事实源。下游 Feature、Technical Design、Acceptance 和追踪矩阵使用稳定 ID 引用约束；章节移动不改变 ID。

| 前缀 | 范围 | 主要章节 |
| --- | --- | --- |
| SYS | 系统目标、不变量和边界 | §1–§3、§19 |
| SRC | Source 契约、来源和写入要求 | §5 |
| ARC | 原文快照、归档和来源漂移 | §4.3、§5.6 |
| WIKI | Wiki schema、状态和正文契约 | §6 |
| EVD | Claim、Evidence 和引文 | §6.4、§6.9 |
| VAL | 确定性校验、LLM 验证和报告失效 | §8 |
| OPS | Preview/Apply、幂等、锁和对象操作 | §9 |
| IDX | 索引、检索和 RAG 边界 | §11 |
| API | FastAPI 本地后端 | §12 |
| WEB | Astro 公开静态模式 | §13 |
| QST | Question 和 FSRS 复习 | §7、§14 |
| SKILL | Agent Skill 受控入口 | §15 |
| MIG | 迁移、发布和回滚 | §16–§18 |
| SEC | confidentiality、Vault 和公开泄漏门禁 | §4.2、§13.3 |

当前 P0 规范编号：

- `SRC-001`：每个 Source 必须满足一种来源完备性通道。
- `ARC-001`：网络来源必须保存可复核的本地文本快照。
- `WIKI-001`：知识型 Wiki 必须符合 schema、状态和正文契约。
- `EVD-001`：知识型 Wiki 的可验证 Claim 必须显式映射 Evidence。
- `VAL-001`：`supporting_quote` 必须在指定 locator 内逐字匹配。
- `OPS-001`：所有写操作必须经过 Preview、用户确认和 Apply。

ID 的详细交付映射见 [规范到验收追踪矩阵](./traceability-matrix.md)；交付状态见 [Feature List](./feature-list.md)。
