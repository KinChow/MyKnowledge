# ADR-0022：公开发布与本地能力边界收敛

- 状态：Accepted
- 日期：2026-09-21
- 相关规范：WIKI-001、EVD-001、VAL-001、ARC-002
- 相关 Feature：F006、F007、F008、F009

## 背景

个人知识库保留 Markdown/JSON 事实源、Astro 静态公开 projection 和本地
FastAPI/MCP。需要修复的是权限、发布版本与删除状态的边界，不是增加服务层级。
本决策补充 ADR-0019，并替代 ADR-0010/0015 中**公开发布**对逐页人工确认和
LLM 结果的阻断要求；历史审计记录和私人发布契约保留。

## 决策

1. `tools/access_policy.py` 是 HTTP/MCP 的能力策略入口。公开匿名读取仅指 public
   projection；练习、复习记录和题目管理是本地数据，`scope=public` 不豁免鉴权。
   新增 action 默认需要 write capability。MCP 未配置 token 时也拒绝受保护动作。
2. Git commit 是内容审批边界。正式构建要求发布输入（正文、source/snapshot、
   规则、生成器和前端代码）与当前提交一致；构建前后复核 revision 和干净状态。
   `var/state/release/manifest.json` 记录 `source_revision`，不把本地预览当正式发布。
3. schema、确定性引用/snapshot 校验、公开范围和 leak-gate 仍为硬门禁。LLM 报告
   保留、展示但仅 advisory。`release confirm` 返回明确的退役错误，不再写事件；
   `release/public-confirmations/` 只作为历史审计和备份材料。
4. public body 读取统一经 `tools/published_files.py`：目录约束、symlink/hardlink
   拒绝、canonical body hash 复核；漂移返回 `projection_body_stale`，不回退到
   canonical 扫描。HTTP、CLI 和静态 staging 共享该实现。
5. 软删除 ledger 使用 append order 的最新有效事件决定 active/deleted/purged。
   restore 取消旧删除周期的 purge 资格；损坏行阻断永久清理。
6. 公开站部署在 `/MyKnowledge/`，只提供文章、搜索、图谱和导航，不连接本机 API，
   不携带 capability token。practice 路由及其页面资源从 release 剔除；本地 Astro
   dev 使用同源 `/local-api` 代理，token 由开发服务器注入，不进入浏览器存储。
7. projection 更新显式标记 FTS stale，不启动自动重建；使用 `myk build index`
   显式重建。doctor 保留 warning，不能将未知/过期索引报为健康。

## 后果与验证

不增加 OAuth、账户/RBAC、数据库、队列或缓存服务；多 Vault/备份保持兼容。
未提交上述发布输入时 `npm --prefix frontend run build` 被拒绝是预期行为。
本地预览可运行 `npm --prefix frontend run prepare-content` 和 `npm --prefix frontend run dev`；
正式发布须先人工审阅并提交。确认命令的旧参数保留用于返回兼容错误。

回归覆盖权限矩阵、旧 confirmation 非依赖、hash/link/path 失败关闭、恢复后拒绝 purge、
脚本/source map 泄漏扫描及项目页链接闭包。公开文章 ID 集合不因迁移而改变。
