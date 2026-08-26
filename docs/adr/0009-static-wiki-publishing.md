# ADR-0009：保留 Astro/Starlight 的静态 Wiki 发布链

- 状态：Accepted
- 日期：2026-08-26
- 相关规范：WEB、SEC、IDX、MIG
- 相关 Feature：F007、F010、F011

## 背景

仓库已经有 Astro + Starlight 的静态前端 POC，包含 Pagefind 搜索、Cytoscape 全局/局部图谱、Mermaid/KaTeX、路由兼容和浏览器本地收藏/最近阅读状态。题库/复习属于后续 F008，不作为当前静态发布依赖。早期设计只写了“静态站点”，没有说明现有实现如何接入 source/wiki 发布状态，也没有明确 source、archive 和 internal 内容的泄漏边界。

## 候选方案

### A. 继续使用现有 Astro/Starlight，并增加 public projection adapter（选定）

复用已验证的阅读、搜索和图谱体验，只替换内容输入和构建门禁。改动集中在 prepare/build adapter，FastAPI 不成为静态站点依赖。

### B. 回到 MkDocs Material

迁移成本低、生态成熟，但现有 Astro POC 的路由、交互和图谱需要重做，且同样需要额外的 public projection 和 leak gate。MkDocs 只保留为迁移期间的回退链。

### C. 引入 Quartz 或全新的 Wiki 框架

Quartz 的 backlinks/graph 很有参考价值，但会重新承担主题、路由、构建和数据投影迁移；没有 source/claim 发布门禁，不能直接作为真相源。收益不足以抵消一次性重写风险。

## 决策

保留现有 Astro/Starlight 作为静态展示层，明确职责边界：

1. `queries/public` 或等价的 `public projection manifest` 是正式构建的唯一输入。Astro 不直接读取 `sources/`、`archive/`、`practice/` 或任何 private vault；当前迁移基线允许一个明确标记为 legacy/validation-only 的 `docs/` adapter 用于测量路由和链接，但它不能被标记为 release input，也不得绕过发布投影。
2. public projection 只包含 `public_publishable == true` 的 Wiki，以及经过 allowlist 批准的标题、正文、公开标签、路由和 Wiki-to-Wiki links；`public_release` 默认是 `false`，只有人工为当前输出 hash 创建单独的 public confirmation，projection 从 durable event/operation record 派生为 `true` 后才能发布。Source locator 只能作为引用信息，不能内联归档正文。
3. 构建阶段保留现有 POC 的模块分工：`prepare-content.mjs` 负责 projection -> Starlight content adapter、路由和 Markdown link rewrite；`build-graph.mjs` 只从 public catalog 生成 `graph.json`；`astro.config.mjs` 负责 Starlight、中文 locale、Mermaid/KaTeX 和站点 base；`PageTitle.astro` 及页面组件只读取 public catalog；`validate-build.mjs` 执行数量、路由、图谱和 leak gate。
4. Pagefind 只对最终 public HTML 建索引。中文 `lang="zh-CN"` 由 Starlight 页面继承，Pagefind multilingual 配置和中文检索回归作为验收项；Pagefind 失效时文章和图谱仍可浏览，构建报告必须标记搜索不可用。
5. Cytoscape 图谱只使用 `vault_id: public` 的 Wiki 节点和显式 Wiki-to-Wiki edges；source、evidence target、任一 private vault 对象、未发布页面不进入节点、边、catalog、页面脚本或 URL。图谱数据生成失败时保留旧 dist，不发布半成品。
6. 静态站点不调用 FastAPI。首页、文章、搜索、图谱、Mermaid、KaTeX 和浏览器 localStorage 状态在无后端时仍可用；本地完整模式可以由 Astro dev proxy 额外访问 `/api`，但这不是 public build 的输入或成功条件。
7. 构建采用 staging 目录：先生成 projection、Astro dist、Pagefind 和 graph，再执行 allowlist/denylist/leak gate；全部通过后原子替换正式 dist。失败时保留上一份可浏览 dist 和上一份 public manifest。
8. 迁移期间保留旧路由 map，兼容 POC 已处理的 slug normalization、重复路由消歧和未解析链接报告。切换到 wiki-only 后，旧 `docs/` 不再是第二份维护源。

## 后果

优点：保留已有前端投入和用户体验，静态站点可独立部署，FastAPI/LLM/私有 vault 不会进入公开运行时；发布边界变成可测试的 projection 和 leak gate。

代价：需要实现 projection adapter、构建 staging、泄漏扫描和 Pagefind 中文回归；旧 docs 到新 wiki 的路由与链接迁移仍需人工确认；Astro 依赖版本必须锁定并定期升级。

## 重新评估条件

如果需要服务端权限、实时协作、登录后个性化 public 页面或 Astro 无法满足构建规模，再评估 SSR/其他 Wiki 框架；即使更换展示层，也必须保留 public projection、snapshot 证据边界和 leak gate。
