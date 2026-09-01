# ADR-0014：数据分域、五层归属与三条写入通道

- 状态：Accepted
- 日期：2026-08-30
- 相关规范：§4.4–§4.6、§6.2、§6.7、LAY-001~004、CHN-001、WIKI-003
- 相关 Feature：F002、F004、F007、F010、F011、F013

## 背景

两个问题同时暴露：

**一、仓库根目录没有归属规则。** 20 个根目录混合了组件（`tools/`、`backend/`、`frontend/`）、人写内容（`sources/`、`wiki/`）、不可变记录（`archive/`、`audit/`、`release/`）和可重建产物（`queries/`、`state/`、`reports/`），新增目录时没有可判定的归属依据，`specs/` 已经退化成空的死目录。

**二、没有常驻的中间层。** `docs/` 下 378 篇存量是一次性迁移队列、有终点；迁移完成后"读了一半的想法""还没成型的推理"没有合法住所。`status: planned` 只允许五个字段且不含正文，承载不了未定稿内容。同时 12 个 Feature 的门禁全部指向"published wiki"这一个出口，实测产出是 2 篇 published wiki 对 163 篇 source——门禁强度与产出速率严重失配。

## 候选方案

**分域**

- A. 保持平铺：零成本，但归属规则缺失的问题不解决。
- B. 只聚合内容层（`content/`）：内容清晰，但组件与机器产物仍混在根级。
- C. 组件也聚合到 `platform/`，或采用 PyPA 的 `src/` layout：破坏 `python -m tools.cli`（依赖 `tools/` 位于 `sys.path[0]`），需改写全部 import、Agent Skill 入口与文档命令，且本项目不发布到 PyPI，收益为零。
- D.（选定）组件平铺 + 数据侧收敛为 `content/` / `ledger/` / `var/` 三域：三域的备份策略、Git 忽略策略与灾难恢复优先级各不相同，合并任意两个都会丢信息。

**中间层的 vault 归属**

- E. 五层全部 per-vault：语义最直接，但挂 N 个 vault 就有 5N 个目录、N 份到期清单。
- F.（选定）managed 层 per-vault，unmanaged 层单例：`sources/`、`wiki/` 有 `object_ref` 且被 `evidence.targets` 真实引用，必须 per-vault；`working/`、`journal/`、`decisions/` 没有 object 身份，`working → wiki` 是人工重写而非对象引用，因此不构成 cross-vault reference。维护面 `2N + 3`。

**中间层是否受 schema 管**

- G. 给 unmanaged 层建 object schema：可统一检索，但写一条随手笔记要走 preview → confirm → apply 三步协议。这正是导致产出停滞的同类失效模式。
- H.（选定）不建 schema：唯一硬约束是 `source_ref` 或 `legacy_path` 非空；检索由编辑器与 grep 承担，不伪造 object 身份。原计划的"独立文本匹配命令"于 2026-09-01 取消：一个不产生 `object_ref`、不进索引、不进 `query-result/v1` 的检索出口没有增量价值，只多一个要维护的入口。

**低摩擦入口的形态**

- I. 五字段快速 wiki 条目（原决策）：`origin: personal` + `publication_scope: none` + `status ≤ draft`，派生 `strength: personal`。它让「随手记」也落在 `content/wiki/` 里。
- J.（2026-09-01 改选）不给 wiki 开低摩擦入口，随手记直接写 `content/working/`：`working/` 本身就是零 schema 的层，再给 wiki 开一个"几乎没有约束的 wiki"等于制造两个语义重叠的低门槛入口，并且让 `content/wiki/` 同时容纳"已验证的知识"与"随手记"，读者无法从目录判断可信度。

## 决策

1. **三个数据域**：`content/`（人写、可编辑、不可重建）、`ledger/`（机器写、append-only、路径被派生规则引用）、`var/`（机器写、可重建）。归属由 §4.4 的五条判据判定，不允许无归属目录。组件平铺在根是生态约束下的正解。
2. **`ledger/archive/` 不进 `content/`**：它是"来源的副本"，但机器抓取、内容寻址、人不可编辑，且 manifest 是 append-only。**`docs/` 不进 `content/`**：LLM 审计 ruleset 在运行时抽取其原文算 `extract_sha256`，它是运行时输入。
3. **五层与 vault 归属**：见候选 F。unmanaged 层不进 projection、leak gate 输入树、`before_hashes`/`after_hashes` 与 `query-result/v1`。
4. **三条写入通道**：主链路（不变）、**降级落位通道**（写 `content/working/`，唯一硬约束 `source_ref` 或 `legacy_path` 非空，不产生 wiki 对象）、日志通道（零门槛，无出口）。**2026-09-01 修订**：原"五字段快速 wiki 条目"取消（候选 J 替代 I）。理由是它与 `content/working/` 语义重叠，且会让 `content/wiki/` 同时装"已验证知识"和"随手记"；`content/wiki/` 的准入因此收紧为**逐篇人工升级**，降级则是批量动作（一次降级一条 CDR）。降级/升级不对称是有意的：批量升级等于批量伪造证据链。
5. **`review_by` 是报告项不是状态轴**：进 `excluded_from_content_hash`，到期只产生 `doctor` 清单，不改变任何 `*_state`。理由见 §6.2。
6. **迁移分三批且不重写历史**：对象身份与路径解耦（`target_ref` 是 `object_ref`，`record_sha256` 不含路径）使搬移可行；但 `applied_files` 中的历史路径是事实，`audit.append_only` 禁止重写，读取侧必须容忍历史路径形态。`body_path` 属于 `release_input_fields`，批次 2 会让已发布页面的 `public_release` 自动回落 `false`，需重新人工确认一次——这是既有机制的正常行为，不是异常。

## 后果

- 根目录呈现为「若干工程根 + 三个数据域 + config/docs」，新增目录有唯一归属答案。
- `content/working/` 承担全部低摩擦写入：TTL 到期项的出口是「升级 / 转 journal / 删除」三选一，由人判定，工具只报告。
- 代价：`content/` 与 `ledger/` 各多一层路径深度；`policy.yaml` 的 `body_path_prefixes`、`paths.py` 的路径属性和约 15 个声明式 durable path 常量需要一次性更新。
- 迁移窗口随已发布页面数量单调收窄（每多一个已发布页面就多一次重新确认），因此批次 2 应尽早执行。
- 取消快速通道的代价：`content/wiki/` 的写入摩擦没有下降，因此 wiki 的篇数会长期远小于 `content/working/` 的篇数。这是预期结果而不是问题——wiki 的价值来自"进得去的都是被验证过的"。

## 重新评估条件

- 挂载第一个 private vault 后，若发现 unmanaged 层单例导致 internal 素材频繁需要跨 vault 搬运，则退回候选 E；
- 若 `content/working/` 的检索需求强到必须与 wiki 在同一个 `query` 结果中出现，则重新评估候选 G，引入独立的 `note/v1` 对象类型；
- 若 `content/working/` 长期只增不减、几乎没有内容被升级进 wiki，说明升级门禁（而非入口摩擦）是产出停滞的根因，需重新审题——此时应先降低单篇升级成本（例如把"claim 是否超出引文"的检查前移到写入时），而不是重新给 wiki 开低摩擦入口。
