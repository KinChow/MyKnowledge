# ADR-0011：入口层必须消费共享 domain service，禁止自建加载与鉴权

- 状态：Accepted
- 日期：2026-08-28
- 相关规范：SEC、OPS、§12（Local API）、F009 Skill 契约
- 相关 Feature：F004–F009、F011、F012（全部入口接缝）

## 背景

F004 起的增量交付把编排逻辑直接堆进入口层（`tools/cli.py`、`backend/app.py`、`tools/skill_runtime.py`、`tools/mcp_server.py`），产生了同一契约的多份平行实现：

1. public projection 加载存在两份：`backend.app`（宽松，不校验 `public_release`、不带 body）与 `skill_runtime`（严格）。宽松版位于 API 层，与"public 只暴露已发布对象"的安全契约形成泄露面差异；且因 manifest 不含 body，API 的 fallback 检索只能匹配 title。
2. capability token 校验存在三份：`backend.app.require_capability`、`require_write_capability`、`mcp_server` 内联实现。恒定时间比较、TTL、audience/scope 等 ADR 契约靠重复代码而非结构保证。
3. `backend.app` 的 `/api/read`、`/api/backlinks` 曾对 public vault 直接 `rglob` canonical 内容，绕过 projection——未通过发布确认的 wiki 可被免 token 读取。
4. `tools.cli` 反向 import `backend.app` 的私有函数，形成 `tools ↔ backend` 环依赖。

根因不是单处代码疏漏，而是交付模式：每个 Feature 冲到 `Implemented` 后继续堆依赖，接缝层没有对应对账。本 ADR 把收敛后的结构固化为硬约束。

## 候选方案

- A. 只修复已知 bug，不立约束：成本最低，但同一模式会在 F013+ 复现（2026-08 已实际发生四次以上）。
- B. 引入重量级框架层（如完整 Clean Architecture 分层/依赖注入容器）：对单人工具仓库过度设计。
- C.（选定）最小分层约束：入口层只做"解析输入 → 调用共享 domain service → 翻译输出/错误"，共享服务单实现、入口不得自建。

## 决策

1. **入口层定义**：CLI（`tools/cli.py`）、Local API（`backend/app.py`）、Agent Skill（`tools/skill_runtime.dispatch`）、MCP（`tools/mcp_server.py`）。
2. **public projection 只有一个加载实现**：`tools/projection.PublicProjectionStore`（严格 allowlist + body + 防穿越）。任何入口不得自行读取 `queries/public/manifest.json` 或扫描 canonical `wiki/` 来响应 public 请求；public 读/反链语义与 `skill_runtime` 的 projection-only 行为一致。
3. **capability token 只有一个校验核**：`tools/capability.check_capability` 纯函数。HTTP/MCP adapter 只做错误翻译（HTTPException / blocked dict），不得复制比较、TTL 或 scope 逻辑。
4. **依赖方向单向**：`backend` → `tools`（domain），`tools` 不得 import `backend`；入口间共享逻辑一律下沉 domain 模块。
5. **离线降级语义归属 domain**：仅 `PublicProjectionStore.degraded_items()` 表达"manifest 缺失 → 空集合"（F006 启动路径）；需要显式失败的入口直接使用 `public_items()`，不得各自吞异常。

## 后果

- 新增入口（如未来 CLI 子命令、webhook）只需写薄 adapter，安全契约不随入口数量漂移。
- 测试可针对单实现验证契约（如"同一 manifest 在 API 与 Skill 返回同一可见集合"），而不是每入口重复测。
- 代价：domain 服务 API 变更会同时影响多入口，需全量测试（当前 324 项 ≈ 20s，可接受）。
- 实施：2026-08-28 结构收敛已完成上述收敛；`/api/read`、`/api/backlinks` 的 public 路径已改为 projection-only（未发布 wiki 返回 404）。

## 重新评估条件

出现第二种 projection 存储后端、多用户 API 或远程服务入口时重新评估分层边界。
