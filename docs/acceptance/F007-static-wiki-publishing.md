# F007 Astro/Starlight 公共静态 Wiki 验收

- Feature：F007
- 相关规范：WEB、SEC、IDX、MIG
- 相关 ADR：ADR-0007、ADR-0009
- 实现设计：[静态 Wiki 发布](../technical-design/static-wiki-publishing.md)
- 状态：Implemented（2026-08-28；工程骨架与 fail-closed 基础能力，完整静态发布验收待补）
- 实现证据：`frontend/package.json`、`frontend/astro.config.mjs`、`frontend/scripts/prepare-content.mjs`、`frontend/scripts/build-release.mjs`、`frontend/scripts/leak-gate.mjs`
- 当前边界：已加入可审计的空 `public-projection/v1` manifest 作为离线输入门；真实发布条目、Pagefind、graph browser、人工 release confirmation 和完整 leak-gate/旧 dist 演练尚未完成。

## 本轮成熟方案调查（2026-08-28）

- Astro 7.1.3 + Starlight 0.41.4（MIT，<https://github.com/withastro/astro>、<https://github.com/withastro/starlight>）：复用静态输出、内容目录和 sidebar 结构；限制是不会替 MyKnowledge 判断 public allowlist，输入仍由 manifest adapter 控制。
- Pagefind 1.4（MIT，<https://github.com/CloudCannon/pagefind>）：复用构建后离线索引；限制是只索引最终 HTML，不能作为权限过滤或 canonical 数据源。
- 替代方案 Quartz（MIT，<https://github.com/jackyzha0/quartz>）提供 Markdown/图谱范式，但其默认内容扫描范围过宽，本轮仅借用 graph/catalog 闭包思路，不直接扫描 `docs/`、`source/` 或 private vault。

本轮落地的 `queries/public/manifest.json` 是空 allowlist，确保 projection 模式在无 public 条目时可确定性运行；条目必须由后续 projection generator 根据人工确认和当前 hash 生成，不能手写伪造发布状态。

## Starlight projection collection 增量证据（2026-08-27）

- `frontend/src/content.config.ts` 使用 Starlight 官方 `docsLoader()` 与 `docsSchema()`；内容集合只接收 `prepare-content.mjs` 从已校验 `public-projection/v1` manifest 复制的 Markdown。
- `tests/test_frontend_projection.py::test_starlight_content_collection_uses_projection_output` 验证配置不会回退到直接扫描 `docs/`；同文件多页 fixture 验证 route/catalog/graph 闭包。
- 前端门禁 `validate:config`、`validate:docs`、`validate:legacy`、projection validator 和 `npm run build` 均通过；空 public manifest 只生成首页，仍保持 fail-closed。

## Release precondition hash 增量证据（2026-08-27）

- `prepare-content.mjs` 现在同时校验 manifest 的 `release_input_sha256`、`content_sha256`、`evidence_sha256`、`public_confirmation_sha256` 与人工 `public-release-confirmation/v1` event；`tests/test_frontend_projection.py::test_prepare_content_rejects_confirmation_precondition_drift` 验证 hash 漂移在 staging 前阻断。

## Static graph page 增量证据（2026-08-27）

- `frontend/src/pages/graph.astro` 仅读取构建生成的 `public/generated/graph.json`，以静态 HTML 展示节点和闭包链接；`tests/test_frontend_projection.py::test_graph_page_is_static_and_reads_generated_graph_only` 验证页面源码不读取 sources/practice/local projection。

## Projection validator 增量证据（2026-08-30）

- AC-F007-011/012/017：`tests/test_frontend_projection.py` 验证空 public manifest 通过，practice 路径、编码 `%2e%2e` 穿越、重复 ID 均 fail-closed。
- validator 只校验 allowlist/schema/path 边界，不生成或提升 `public_release`；当前仓库没有真实 Wiki/人工 confirmation，因此仍不标记 Accepted。

## Active content / Mermaid callback 增量证据（2026-08-27）

- `tests/test_frontend_projection.py::test_leak_gate_rejects_active_html_and_mermaid_callbacks` 验证 input-tree leak gate 拒绝 `<iframe>` 与 Mermaid `click ... href https://...` callback；同时拒绝事件处理器属性和危险 URL，避免静态页面执行外部脚本或导航。

## 离线空 projection 构建证据（2026-08-27）

- 在 `frontend/` 执行 `npm run validate:config`、`npm run validate:docs`、`npm run validate:legacy`、`MYKNOWLEDGE_CONTENT_MODE=projection npm run validate:projection` 和 `npm run build` 均通过。
- release build 生成静态 Astro 输出并完成 Pagefind 索引（2 个 HTML，包含 404 与首页）；输入树、staging 和最终 dist 的 leak gate 均返回 `findings: []`，`build_valid` 通过。
- 该证据只证明无 public 条目时构建链离线可运行和 fail-closed；当前 projection 仍为空，真实 Wiki、多语言检索和浏览器交互验收待补。

## Release lock 增量证据（2026-08-30）

- AC-F007-006/016：`tests/test_frontend_projection.py::test_release_lock_blocks_concurrent_build` 验证已有 `state/public-release.lock` 时构建立即返回 `release_lock_held`（退出码 2），不触碰正式 dist；正常构建后 lock 会清理。
- 完整 warning allowlist、陈旧锁人工恢复、真实 public confirmation 和多页面 sitemap/Pagefind 闭包仍待验收。

## 本轮 sitemap 闭包增量证据（2026-08-30）

- `frontend/scripts/build-release.mjs` 在 Astro 静态构建成功后按 catalog 生成确定性 `dist/sitemap.xml`，仅包含 `/`、`/graph/` 和 public catalog routes；`validate-build.mjs` 拒绝重复、缺失或额外 URL。
- `npm run build` 在空 projection 上通过 Pagefind、sitemap、graph 和 dist leak gate；Astro 未配置外部 `site` 时仍不联网，sitemap 使用站内相对 URL。该证据不替代真实多文章浏览器验收。

## Public release confirmation 增量证据（2026-08-30）

- AC-F007-009/022/025：`tests/test_release_confirmation.py::test_public_release_event_is_hashed_and_written` 验证 public release event 的 schema、target、human actor、input-tree scope 和 canonical event hash，并以 append-only 文件写入。
- `test_public_release_event_rejects_private_reason_or_target` 验证 private target 与 URL/private reason 均被 fail-closed 拒绝。

事件校验不等于已发布页面；当前仍没有真实 Wiki 的完整 validation attestation、release-input hash 和最终多页面发布闭包。

## Prepare confirmation replay 增量证据（2026-08-30）

- AC-F007-009/012/025：`tests/test_frontend_projection.py::test_prepare_content_requires_matching_confirmation` 使用临时 projection fixture 验证 manifest item 缺失 `public-release-confirmation/v1` 时，prepare 在生成 catalog/page 之前返回 `confirmation_missing`。
- prepare 现在会校验 event schema、human approve、public Wiki target、object ID 和 canonical event hash；confirmation 校验不等于最终发布，仍需完整 validation/release-input/leak-gate 闭包。

## 多页 projection 增量证据（2026-08-27）

- AC-F007-001/002/013：`tests/test_frontend_projection.py::test_projection_prepare_and_graph_build_multi_page_fixture` 在隔离临时 checkout 中生成两篇 public Wiki 与人工 confirmation，运行 `prepare-content.mjs` 和 `build-graph.mjs`；catalog 节点集合为 `{one,two}`，唯一边为 `one -> two`，未读取 practice/source/private 内容。该证据不替代真实 Astro/Pagefind 浏览器验收。

## AC-F007-001 只构建 public projection

- Given：projection 同时包含 `vault_id: public` 的 `public_publishable`、两个或更多 private vault 的 internal private、draft、review、conflicted 和 deprecated Wiki；
- When：执行完整 public build；
- Then：catalog、HTML、sitemap、graph 和 Pagefind 只包含 `public_publishable == true` 的 Wiki；
- 失败时不变量：未发布、证据冲突、internal 或 deprecated 对象不得以正文、标题、ID 或链接形式出现；
- 自动化级别：Integration。
- 当前状态：待真实 public manifest fixture。

## AC-F007-002 catalog、路由和图谱闭包

- Given：projection 包含重复 slug、旧路由映射、Wiki-to-Wiki links 和 unresolved link fixture；
- When：执行 prepare-content、build-graph 和 validate-build；
- Then：文章 ID 唯一，route normalization 和 unresolved report 可复现，graph 节点集合等于 catalog，所有边两端都存在；
- 失败时不变量：不得生成指向 source、internal 或不存在 Wiki 的节点/边；
- 自动化级别：Integration。

## AC-F007-003 Pagefind 中文和混合检索

- Given：页面含中文连续文本、英文标识符和中英混合标题；
- When：完成 Astro build 并执行 Pagefind fixture 查询；
- Then：中文、英文和混合查询能命中预期公开文章并生成高亮；
- 失败时不变量：Pagefind 失败时不得误报搜索通过；按 policy 阻断发布或明确标记 `search_degraded`；
- 自动化级别：Browser/Integration。

## AC-F007-004 public leak gate

- Given：在 projection、allowlisted attachments、staging、dist、HTML、JS、CSS、sitemap 或 source map 中注入 source 正文、archive snapshot、practice answer、LLM report、任一 private vault 的 ID、内网 URL 和 private path；
- When：执行输入 allowlist、staging denylist 和 dist leak gate；
- Then：命中任一敏感类别即失败并报告相对路径、类别和 hash；
- 失败时不变量：CI 日志不回显匹配正文，正式 dist 不被替换；
- 自动化级别：Security/Integration。

## AC-F007-005 无 FastAPI 的静态降级

- Given：不启动 FastAPI、LLM provider 或任何 private vault；
- When：打开首页、文章、搜索和图谱；
- Then：公开文章、Pagefind、图谱、Mermaid/KaTeX 和 localStorage 收藏/最近阅读仍可用；本验收只覆盖 public 静态阅读状态；
- 失败时不变量：API 不可用只影响本地增强区域，不阻断静态阅读；
- 自动化级别：Browser。

## AC-F007-006 构建失败保留旧产物

- Given：Astro、Pagefind、graph 校验或 leak gate 任一步失败，且已有上一版 `dist`；
- When：执行 staging build；
- Then：命令失败，上一版 dist、public manifest 和可浏览页面保持不变，失败报告可定位阶段；
- 失败时不变量：不得先清空正式 dist，不得发布半成品；
- 自动化级别：Integration。

## AC-F007-007 路由兼容

- Given：旧 MkDocs/Astro 路由与新 Wiki route map 存在差异；
- When：访问旧 route、规范化 route 和新 route；
- Then：允许的旧 route 重定向或显示兼容页面，最终只指向 public Wiki；未允许 route 返回明确 404；
- 失败时不变量：兼容逻辑不得复制旧 docs 正文或暴露未发布对象；
- 自动化级别：Browser/Integration。

## AC-F007-008 版本和生成物可复现

- Given：相同 public projection hash、lockfile 和 Node/Astro 版本；
- When：在干净工作树重复构建；
- Then：catalog、graph、route report 和页面集合一致，build manifest 记录输入和工具版本；
- 失败时不变量：生成物差异必须有可解释的版本/时间字段，不得修改 canonical source/wiki；
- 自动化级别：Repository/Integration。

## AC-F007-009 Public release 人工审核门禁

- Given：public projection 中同时存在 `public_release: false` 和当前 hash 已由人工改为 `true` 的对象；
- When：执行 public manifest 生成和 Astro build；
- Then：只有当前 hash 绑定的 `public_release: true`、public-safe confirmation event、durable validation attestation 且存在 public confirmation 的对象进入；人工事件绑定 release input/evidence/输入 leak 摘要，构建随后独立执行最终 dist leak gate；其余记录被跳过并列出原因；构建不需要 checkout private vault；
- 失败时不变量：只有人工操作可以把 false 改为 true；自动化、LLM、Agent 或仅通过 leak gate 不能代替人工操作；最终 dist leak gate 失败时上一版正式 dist 保持不变；
- 自动化级别：Security/Integration/Manual review。

## AC-F007-010 Public-safe event 与私有 lineage 脱敏

- Given：public-owned 脱敏输出带有 private lineage、confirmation event、validation attestation 和公开 hash；
- When：执行 projection、staging、dist、sitemap、source map 和 leak gate 扫描；
- Then：只保留 public `event_sha256`/`public_lineage_commitment` 等 allowlist 字段，不出现 private ID、路径、source_vault_ids、snapshot exact 或裸 private hash；
- 失败时不变量：命中任一私有元数据时构建失败且旧 dist 不变，不能通过改名、删字段或过滤 local index 绕过；
- 自动化级别：Security/Integration。

## AC-F007-011 输入模式与治理文档隔离

- Given：legacy `docs/` 同时包含知识内容、acceptance、ADR、Technical Design、deferred 和根目录设计文档；另有缺失或 schema 错误的 `queries/public/manifest.json`；
- When：分别执行 `npm run validate:legacy` 与 `npm run validate:projection`；
- Then：legacy 报告明确列出治理文档为 omitted，基线只生成知识内容；projection 模式只接受 `public-projection/v1` manifest，manifest 缺失或 item 不满足 allowlist 时 fail-closed；
- 失败时不变量：治理文档不能被当作公开 Wiki，不能通过默认回退到旧 `docs/` 绕过 projection 门禁；
- 自动化级别：Repository/Integration。

## AC-F007-012 Projection 正文与确认事件 hash 校验

- Given：manifest item 的 `content_sha256`、`evidence_sha256`、`release_input_sha256` 或 `public_confirmation_path` 与实际正文/人工确认事件不一致；
- When：执行 projection prepare；
- Then：adapter fail-closed，返回具体 item/stage，不能生成 catalog、graph 或新的 dist；
- 失败时不变量：不能只相信 manifest 中的字符串 hash，不能用 `public_release: true` 或旧 event 绕过当前正文；
- 自动化级别：Security/Integration。

## AC-F007-013 Projection 图谱输入隔离

- Given：旧 `docs/`、private vault 和 public projection 同时存在，manifest 声明 public Wiki-to-Wiki links；
- When：执行 prepare/build-graph；
- Then：图谱只使用 projection 解析出的 public route links，`generated_from` 等于 manifest hash，不能读取旧 docs 或 private 路径；
- 失败时不变量：source、private object、未列出的 link 和 stale manifest 不得成为节点或边；
- 自动化级别：Repository/Security/Integration。

## AC-F007-014 Manifest hash 忽略 volatile 时间字段

- Given：同一组 `items`、`generated_from`、policy/schema 和正文 hash 生成两份 manifest，只改变 `generated_at`/`generatedAt` 或重新计算 `manifest_sha256`；
- When：执行 projection manifest canonical hash 校验；
- Then：两份 manifest 的 `manifest_sha256` 相同，且 adapter 不因生成时间变化而使 release input 失效；非 volatile 字段任一变化都必须产生不同 hash 并重新审核；
- 失败时不变量：不能通过修改时间字段掩盖内容、权限、链接或发布状态变化；
- 自动化级别：Unit/Integration。

## AC-F007-015 Release-input 完整覆盖与 active-content 拒绝

- Given：分别改变 canonical body、public Front Matter、`body_path`、route、links、附件路径/排序/hash、lineage commitment、policy/schema、public confirmation event，或在正文/附件中加入 script、iframe、事件处理器、危险 URL；
- When：执行 projection prepare 和 release-input/input leak-gate 校验；
- Then：前述任一 release 输入变化导致 `release_input_sha256` 或输入扫描摘要不匹配并 fail-closed；confirmation event 和最终 `generated/build-manifest.json` 都在扫描范围内；active content 在输入和 staging 阶段被拒绝；最终 dist 允许框架脚本但仍拒绝危险 HTML 行为；
- 失败时不变量：不能只改 manifest 中的字符串 hash 绕过实际文件校验，也不能把框架运行时代码误报为泄漏；item-level leak 摘要不得把自身摘要或派生 confirmation hash 纳入输入，避免形成不可计算的循环；
- 自动化级别：Security/Unit/Integration。

## AC-F007-016 发布锁与 warning policy

- Given：两个 release build 并发运行，或 Astro/Vite 输出未登记的 warning、已登记 advisory warning；
- When：执行 `build-release`；
- Then：`O_EXCL` release lock 只允许一个 operation，另一个返回 `release_lock_held`；未知 warning 返回 `warning_unallowlisted` 并保留旧 dist，登记的 advisory 仅记录摘要并继续；过期锁默认仍阻断，必须人工检查/恢复；
- 失败时不变量：不能自动删除他人锁、并发提升 dist、把 warning 当作成功或生成没有对应构建报告的发布物；
- 自动化级别：Integration/Security/Failure injection。

## AC-F007-017 全量 public 输入扫描与路径边界

- Given：未被 manifest 引用的 `wiki/`、`queries/public/`、confirmation、附件或 staging 文件包含 private 字段；manifest/body/attachment 使用 `%2f`、`%5c`、`%2e%2e` 编码穿越，或 dist 中出现 catalog 未列出的额外 HTML；
- When：执行 prepare、leak gate 和 validate-build；
- Then：全量 public 输入树扫描命中即失败，编码穿越/符号链接/hard-link 被拒绝，额外 HTML 页面不在 allowlist；旧 dist 保持不变；
- 失败时不变量：不能靠不被 manifest 引用、改名、编码或额外静态页面绕过泄漏门禁；
- 自动化级别：Security/Repository/Integration。

## AC-F007-018 Mermaid SVG 安全

- Given：public Wiki 包含 Mermaid `click`/callback、外部 URL、危险 CSS、SVG script/foreignObject 或超长图表源；
- When：浏览器渲染文章；
- Then：输入被拒绝或图表块标记错误，不执行脚本、不加载外部资源；安全图表使用 `securityLevel: strict` 渲染并通过 SVG DOM 检查；
- 失败时不变量：不能通过 Mermaid 语法或生成 SVG 注入导航、脚本、事件处理器或跨域资源；
- 自动化级别：Browser/Security。

## AC-F007-019 输入 gate 时序与附件复用

- Given：两个 public Wiki item 声明同一个附件 path+sha256，且 public 输入目录另有未被 manifest 引用的文件；其中一个输入文件包含 denylist 内容；
- When：执行 `build-release`；
- Then：同 hash 附件只物理 staging 一份但保留两个 owner 声明；Astro 启动前的 `input-tree` gate 先发现未引用文件并阻断，不能生成新的 dist；输入无问题时构建后仍重复扫描 staging/dist；
- 失败时不变量：不能通过“不被 manifest 引用”、重复复制附件或把 gate 延迟到原子提升后绕过扫描；
- 自动化级别：Security/Integration/Failure injection。

## AC-F007-020 Manifest、路由和心跳文件竞态

- Given：构建期间替换 manifest/body/attachment 为 symlink、hard-link、编码穿越路径或修改 route；另有 release heartbeat 正在刷新；
- When：执行 projection prepare、输入 gate 和长时间 build；
- Then：manifest/body/attachment 的读前后 inode/realpath 校验或 route allowlist 失败，构建保留旧 dist；heartbeat 通过 sidecar 原子替换且不改变 lock inode/token；
- 失败时不变量：不能读取仓库外文件、生成危险 URL、因半写 JSON 误判锁丢失或让旧进程继续提升 dist；
- 自动化级别：Security/Integration/Failure injection。

## AC-F007-021 Public link route allowlist

- Given：正文分别包含 manifest 内已声明的 `.md` 链接、同页 anchor、已声明附件、根绝对路径、协议相对 URL、未声明的相对 route、private route 和未知 URL scheme；
- When：执行 projection prepare；
- Then：只有 public manifest route、anchor、声明附件以及允许的外部 `http(s)`/`mailto`/`tel` 链接通过；合法本地 route 被加入对应 manifest link 集合，其他本地路径和 scheme fail-closed；
- 失败时不变量：不能通过把链接写成非 `.md`、根相对路径或改名来访问未发布/private 页面；graph/catalog/link 集合保持闭包；
- 自动化级别：Unit/Integration/Security。

## AC-F007-022 Public confirmation 脱敏与人工流程边界

- Given：confirmation event 使用非 `public` 的 `target_vault`、包含 PII/路径/URL/private lineage 的 actor/reason、重复 nonce，或由非交互 CI 进程直接生成；
- When：执行 public-release confirm/prepare；
- Then：事件被拒绝；合法事件只接受安全 actor pseudonym、短 public-safe reason、`actor_type: human` 和一次性 nonce；confirm 命令必须在交互式人工入口消费 nonce 并写 durable audit；
- 失败时不变量：`actor_type: human` 不被误称为密码学身份认证；自动化、LLM、Agent、leak gate 或手写 `public_release: true` 不能单独放行；
- 自动化级别：Security/Integration/Manual review。

## AC-F007-023 Pagefind 与 sitemap 集合闭包

- Given：Pagefind language entry 的 `page_count` 少于/多于 catalog，或 sitemap 缺少/增加首页、图谱页、文章 route，含重复/带 query 的 URL；
- When：执行 validate-build；
- Then：校验失败并保留旧 dist；只有 Pagefind 文档数与 catalog 相等、sitemap URL 集合完全闭合且使用同一 base path 时通过；
- 失败时不变量：搜索或 sitemap 不能索引未发布页面，也不能静默遗漏已发布页面；
- 自动化级别：Integration/Security。

## AC-F007-024 Leak gate schema version 按 scope 分离

- Given：分别生成 `input-tree`、`input-item` 和 `dist` leak-gate report；
- When：执行 projection prepare、输入扫描和最终 dist 扫描；
- Then：`input-tree` 使用 `public-input-leak-gate/v1`，`input-item` 使用 projection item 约定，`dist` 使用 `public-leak-gate/v1`；build manifest 记录 scope 与对应 report hash；
- 失败时不变量：不能用 dist 报告冒充输入扫描结果，不能把错误 schema version 的报告作为人工确认或发布依据；
- 自动化级别：Unit/Integration/Security。

## AC-F007-025 `public_release` 权威来源不可伪造

- Given：Wiki Front Matter 或 manifest 手写 `public_release: true`，但缺少匹配当前 hash 的 public confirmation、target operation record、未消费 nonce 或 audit chain；另有输入 hash 变化后仍保留旧 event 的 fixture；
- When：重新生成 public projection；
- Then：generator 忽略手写字段，只从 `release/public-confirmations/<event_id>.json` 与 public owner `audit/operations/<operation_id>.json` 派生；任一记录缺失/不匹配或 hash 变化都得到 `public_release: false` 并阻断发布，旧 event append-only 保留；
- 失败时不变量：不能只改 Front Matter、manifest 字符串、LLM verdict、Agent/CI 输出或临时 state 绕过人工确认；
- 自动化级别：Repository/Security/Integration/Manual review。

## 本轮三阶段 leak gate 证据（2026-08-27）

- 命令：`cd frontend && npm run build`。
- 结果：构建前输入树报告为 `public-input-leak-gate/v1`（scope=`input-tree`），staging 报告为 `public-leak-gate/v1`（scope=`staging`），最终 dist 报告为 `public-leak-gate/v1`（scope=`dist`）；三份报告 `findings=[]`，Astro/Pagefind 构建成功。
- 自动化复现：`tests/test_frontend_projection.py::test_leak_gate_reports_input_scope_and_rejects_practice` 验证 input scope schema 和 practice 内容拒绝；`npm run validate:docs`、`MYKNOWLEDGE_CONTENT_MODE=projection npm run validate:projection` 均通过。
- 边界：本证据覆盖 AC-F007-017/019/024 的离线构建门禁，不代表真实内容发布、浏览器检索闭包或 Mermaid 安全场景已 Accepted。

## Pagefind/HTML 集合校验增量证据（2026-08-27）

- `tests/test_frontend_projection.py::test_validate_build_rejects_pagefind_count_mismatch` 验证 Pagefind `page_count` 与产出的 HTML 数量不一致时 `validate-build` fail-closed。
- `frontend/scripts/validate-build.mjs` 在存在 Pagefind 时校验所有语言索引总页数与 HTML 文件数，并确保不小于 catalog；存在 sitemap 时逐条检查 catalog route 闭包。
- 空 projection 生产构建实际通过，Pagefind 报告 2 个固定 HTML 页面，集合校验通过；真实多文章 sitemap/浏览器检索仍待环境验收。

## Confirmation nonce replay 增量证据（2026-08-27）

- `tests/test_release_confirmation.py::test_public_release_nonce_cannot_be_reused_by_another_event` 验证不同 `event_id`/`operation_id` 也不能复用已消费的 confirmation nonce，返回 `confirmation_nonce_reused`；事件仍保持 append-only，不能靠改文件名重放人工批准。
