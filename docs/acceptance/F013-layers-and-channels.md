# F013 分层布局与写入通道验收

- Feature：F013
- 相关规范：LAY-001~004、CHN-001、WIKI-003（系统设计 §4.4–§4.6、§6.2、§6.7）
- ADR：ADR-0014
- 实现设计：[分层布局与写入通道](../technical-design/layers-and-channels.md)
- 状态：Designed（2026-08-30；尚未实现，全部场景待实现）
- 测试运行：`.venv/bin/python -m pytest`（迁移批次以既有全量测试为主护栏）+ `python -m tools.cli doctor`

## 分批交付说明

批次 1 = `var/` 域迁移与删除空目录；批次 2 = `content/` 域迁移与三个 unmanaged 层落地；批次 3 = `ledger/` 域迁移；功能项 = `review_by`、TTL 报告与降级落位。四组可独立验收，互不阻塞。快速通道与 unmanaged 层文本检索命令已于 2026-09-01 取消（ADR-0014 决策 4）。

## AC-F013-001 批次 1：var 域迁移后全链路不变

- Given：`queries/`、`state/`、`reports/` 迁入 `var/`，`specs/` 已删除，`paths.py` 与 `policy.yaml` 的投影前缀同步更新；
- When：执行全量测试、`doctor` 与 `projection generate`；
- Then：既有全量测试全绿，`doctor` 无新增告警，projection 重建成功且 manifest 中 `body_path` 前缀为更新后的值；
- 失败时不变量：迁移未完成时不得生成新的 public projection；不得只改 `paths.py` 而遗漏 `policy.yaml` 的前缀声明，否则 `build.warning_policy: blocking-unknown-v1` 会把未声明路径当阻断；
- 自动化级别：Integration。
- 对应测试：待实现。
- 当前状态：待实现。

## AC-F013-002 批次 2：content 域迁移后对象身份不变

- Given：`sources/`、`wiki/` 迁入 `content/`（`git mv` 保留历史），新建 `content/working|journal|decisions/`；
- When：重跑全量测试与 `doctor`；
- Then：全部测试通过；所有 source/wiki 的 `object_ref` 与 `content_sha256`、`evidence_sha256` 不变；
- 失败时不变量：不得因搬移而改写任何对象 ID 或 hash；`route` 必须保持不变，公开路由不产生死链；
- 自动化级别：Integration。
- 对应测试：待实现。
- 当前状态：待实现。

## AC-F013-003 批次 2：历史 durable record 保持有效且不被重写

- Given：`ledger/audit/operations/` 下 254 条含 `applied_files` 历史相对路径的记录；
- When：批次 2 完成后重算全部记录的 `record_sha256`；
- Then：254 条记录逐条校验通过，文件内容零改动；`doctor` 把已不存在的历史路径报告为「历史路径」而非 stranded 或缺失；
- 失败时不变量：`audit.append_only` 禁止为修正路径而重写历史记录；不得为了让校验通过而追加 superseding record；
- 自动化级别：Integration。
- 对应测试：待实现。
- 当前状态：待实现。

## AC-F013-004 批次 2：public_release 回落与重新确认

- Given：`aar` 页在迁移前 `public_release == true`，其确认事件绑定旧 `release_input_sha256`；
- When：批次 2 改变 `body_path` 后重新生成 projection；
- Then：`public_release` 自动派生为 `false`，旧确认事件保留；重新执行一次人工 public release 确认后恢复为 `true`；
- 失败时不变量：这是 `hash_change_behavior: retain-old-event-but-derive-false` 的预期行为，不得当作故障处理，不得直写 Front Matter 的 `public_release`，也不得部分发布；
- 自动化级别：Integration + 人工确认。
- 对应测试：待实现。
- 当前状态：待实现。

## AC-F013-005 批次 3：ledger 域迁移后发布授权仍可派生

- Given：`archive/`、`audit/`、`release/` 迁入 `ledger/`，约 15 个声明式 durable path 常量同步更新（含跨 vault 模板 `source_lineage_operation_path`）；
- When：执行 `doctor`、`projection generate` 与一次 public release 派生；
- Then：`public_release` 能按 durable record 正常派生；`doctor` 的 archive ledger 双向校验通过；backup manifest 路径一致；
- 失败时不变量：`ledger/archive/manifest.jsonl` 已有行不得重写；缺失 durable record 时必须 `derive-false-and-block-publish`，不得放行；
- 自动化级别：Integration。
- 对应测试：待实现。
- 当前状态：待实现。

## AC-F013-006 降级落位不产生 wiki 对象

- Given：一批被误登记为 source 的加工文档（`content/sources/<domain>/<id>.md`），以及它们在 `archive/` 中的快照与 manifest 行；
- When：执行整批降级落位到 `content/working/<domain>/<id>.md`；
- Then：落位文件只保留 `legacy_path`、`snapshot_sha256`、`domain`、`title`，以及**清单携带且非空时**才写入的 `legacy_first_commit_at`；不再带 `schema_version: source/v1`；不产生任何 wiki 对象与 `object_ref`；`archive/` 快照与 `manifest.jsonl` 逐字节不动；整批只写一条 CDR（绑 plan hash 与全部 `source_id`）；
- 失败时不变量：降级不得删除或改写 append-only 归档（曾经导入过是事实）；不得为落位文件伪造 object 身份；不得逐篇写 CDR 制造"每篇都被单独决策过"的假象；时间事实取不到时不得写空值或用落位时间冒充（清单的 `legacy_time_unresolved` 必须显式计数）；`apply` 不得自行推断时间（只落位清单里的值，保证可复核）；
- 自动化级别：Unit + Integration。
- 对应测试：`tests/test_reposition.py::test_apply_relocates_every_category_into_the_working_layer`、`::test_relocation_carries_the_legacy_git_time_when_the_plan_has_it`、`::test_apply_requires_the_public_vault_write_lock`
- 当前状态：代码通过；161 篇真实落位等 owner 确认清单（Task 9.7）。

## AC-F013-007 working 层无法晋级与外泄

- Given：一个 `content/working/` 下的文件；
- When：尝试让它进入 projection、出现在另一篇 wiki 的 `evidence.targets`、进入 `before_hashes`/`after_hashes`、或出现在 `query-result/v1` 中；
- Then：全部不发生——`projection.body_path_prefixes` 未列出该前缀使其物理上无法成为 `body_path`；它没有 `object_ref`，`evidence.targets` 解析必然 fail-closed；unmanaged 路径不进 operation hash；RAG 召回不包含它；
- 失败时不变量：出口封锁是安全边界，不得由作者字段覆写；不存在"批量把 working 升级为 wiki"的路径，升级只能逐篇走通道 A 全流程；
- 自动化级别：Unit。
- 对应测试：`tests/test_write_operation.py`（working 层入口约束返回 `schema_invalid`）；projection/hash 隔离断言待补。
- 当前状态：待实现（部分）。

## AC-F013-008 review_by 不改变任何 hash 与确认

- Given：两篇真实 published wiki（hash 不变性取 `content/wiki/reading-notes/how-to-read-a-book.md`；确认不变性取带真实发布确认、`public_publishable: true` 的 `content/wiki/work-methods/aar.md`），fixture 使用其真实 hash，不构造假 hash；
- When：为它增加或修改 `review_by`；
- Then：`content_sha256` 与 `evidence_sha256` 逐字节不变；既有 `operation-confirmation` 仍有效；`status` 与全部 `*_state` 不变；
- 失败时不变量：若续期作废人工确认，说明 `hash_inputs.excluded_from_content_hash` 未同步更新，必须阻断合入；
- 自动化级别：Unit。
- 对应测试：`tests/test_review_by.py`。
- 当前状态：已实现。

## AC-F013-009 review_by 到期只产生报告

- Given：一篇 `review_by` 已过期的 published wiki；
- When：执行 `doctor`；
- Then：它出现在到期清单中；`status`、`evidence_state`、`validation_state`、`public_release` 全部不变；页面仍可正常发布与检索；
- 失败时不变量：不得引入第七个状态轴，不得自动降级或撤回发布；
- 自动化级别：Unit。
- 对应测试：`tests/test_review_by.py::test_doctor_lists_due_review_without_changing_any_state`。
- 当前状态：已实现。

## AC-F013-010 working 层入口约束与 TTL 报告

- Given：向 `content/working/` 写入一条无 `source_ref` 也无 `legacy_path` 的内容，以及一条已超过 `ttl_days` 的内容；
- When：执行写入与 `doctor`；
- Then：前者被拒绝并返回 `schema_invalid`；后者出现在到期清单中且文件未被删除；
- 失败时不变量：工具永不自动删除 `content/working/` 内容；不存在"来源待补"的中间状态；
- 自动化级别：Unit。
- 对应测试：`tests/test_write_operation.py::UnmanagedLayerContractTests`、`tests/test_doctor.py::test_doctor_lists_overdue_working_notes_and_never_touches_them`。
- 当前状态：已实现（TTL 时间基准优先 `created_at`，缺失时退到 mtime 并在报告里标明 `basis`）。

## AC-F013-011 unmanaged 层不进入四类边界

- Given：`content/working/`、`content/journal/`、`content/decisions/` 下存在内容；
- When：生成 projection、执行 leak gate 输入扫描、执行一次 apply、调用 `retrieve`；
- Then：四者的输出中均不包含 unmanaged 层的路径或正文；apply 的 `before_hashes`/`after_hashes` 不含它们；`query-result/v1` 的 items 不含它们；
- 失败时不变量：`projection.body_path_prefixes` 不得包含 unmanaged 前缀（回归锁定）；不得为可检索性给 unmanaged 层伪造 `object_ref`；
- 自动化级别：Unit + Integration。
- 对应测试：待实现。
- 当前状态：待实现。

## AC-F013-012 retire/deprecate 必须留下 CDR

- Given：一篇 published wiki；
- When：对它执行 retire 或 deprecate；
- Then：`content/decisions/` 中新增一条 CDR 记录，含判定值（沿用 §16.2 `content_verdict` 四值语义）与理由；
- 失败时不变量：缺少 CDR 时阻断该操作；CDR 只增不改，被推翻时新增记录而不是原地修改；
- 自动化级别：Unit。
- 对应测试：待实现。
- 当前状态：待实现。
