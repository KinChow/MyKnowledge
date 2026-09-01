# 分层布局与写入通道实现设计（F013）

规范以 [系统设计 §4.4–§4.6、§6.2、§6.7](../myknowledge-system-design.md) 为准；决策取舍见 [ADR-0014](../adr/0014-layer-domains-and-write-channels.md)。规范 ID：LAY-001~004、CHN-001、WIKI-003。

## 目标与非目标

**目标**：把「加工阶段」与「时间维度」两个缺失的轴显式化，并让仓库根目录的归属规则可判定。具体交付三件事：三个数据域的物理迁移、`content/working/` 降级落位层、`review_by` 报告项。

**非目标**：不改变主链路的任何门禁强度；不改变任何 hash 计算范围；不给 unmanaged 层引入 object 身份；不引入新的 `strength` 或 `status` 取值。

## 当前基线（2026-08-30 实测）

- `tools/paths.py` 是集中路径容器，其 docstring 已声明「布局变更只改本类，业务代码只消费命名属性/方法」。生产代码通过它取路径，因此域迁移对代码是 `sources_root`/`wiki_root` 等属性的改动。
- `target_ref` 是 `object_ref`（`{vault_id, object_type, object_id}`），不是路径；`record_sha256 = sha256(canonical_json(record_without_record_sha256))` 不包含路径。**对象身份与物理路径已解耦**，这是迁移可行的前提。
- `release/public-confirmations/` 下存在 1 个确认事件；`queries/public/manifest.json` 中 `body_path: wiki/work-methods/aar.md`，`route: /wiki/aar`。
- `audit/operations/` 下 264 条记录中 254 条含 `applied_files` 的历史相对路径。
- `state/`、`queries/local/` 已整体 Git 忽略；`specs/` 为空且未被 Git 跟踪。
- 硬编码路径字面量：生产代码约 6 处，测试约 45 处（集中在 `tests/test_skill_runtime.py`、`test_api.py`、`test_write_operation.py`）。

## 模块边界

| 关注点 | 归属 | 说明 |
| --- | --- | --- |
| 路径解析 | `tools/paths.py` | 唯一改动点；新增 `working_root`、`journal_dir`、`decisions_root` |
| 域声明与阈值 | `config/policy.yaml` 的 `layers:` 段 | `unmanaged_paths`、`working.ttl_days`、`review` |
| working 层入口约束 | `tools/layers.py` | `working_contract_error()`：缺 `source_ref`/`legacy_path` 返回 `schema_invalid`（唯一实现点，写操作侧消费） |
| 到期报告 | `tools/doctor.py` | 两项新报告（`working_ttl`、`review_due`），按域分组输出 |

## 数据模型

`config/policy.yaml` 新增段（键名与语义）：

~~~yaml
layers:
  vault_content_roots: [content/sources/, content/wiki/]      # per-vault，有 object 身份
  vault_store_roots:   [ledger/archive/, ledger/audit/, ledger/release/]
  derived_roots:       [var/queries/, var/state/, var/reports/]
  unmanaged_paths:     [content/working/, content/journal/, content/decisions/]
  unmanaged_excluded_from: [projection_input_tree, leak_gate_input_tree, operation_hashes, query_result]
  working: {ttl_days: 30, require_source_ref: true, ttl_action: report-only}
  journal: {path_pattern: "content/journal/<YYYY>/<MM>/", append_only: true}
  decisions: {id_prefix: CDR, required_on: [retire, deprecate, downgrade]}
review:
  field: review_by
  required: false
~~~

`fast_lane`（五字段快速 wiki 条目）已于 2026-09-01 取消，不进 `policy.yaml`：它与 `content/working/` 语义重叠，且会让 `content/wiki/` 同时装"已验证知识"与"随手记"。低摩擦写入统一由 `content/working/` 承担，`content/wiki/` 只接受逐篇人工升级。见 ADR-0014 决策 4（候选 J）。

`config/schemas.yaml`：`field_contracts.wiki.allowed_fields` 增加 `review_by`；`hash_inputs.excluded_from_content_hash` 同步增加 `review_by`。**两处必须同一个 commit 改**，只改前者会让续期作废人工审计确认；两处键名由 `tests/test_review_by.py` 直接断言。

`projection.body_path_prefixes` / `attachment_path_prefixes`：`wiki/` → `content/wiki/`，`queries/public/` → `var/queries/public/`。这两个键同时承担「允许的投影输入前缀」职责，因此它们是 unmanaged 层无法进入 projection 的物理原因，不需要额外门禁。

## 正常流程

**批次 1**：删除 `specs/`；`git mv queries var/queries`、`state`、`reports`；改 `paths.py` 4 处、`.gitignore` 3 行、`policy.yaml` 的 `queries/public/` 前缀；重跑 `projection generate`。

**批次 2**：`git mv sources content/sources`、`wiki content/wiki`；新建三个 unmanaged 目录；改 `paths.py` 2 处、`policy.yaml` 2 个前缀、测试 fixture；重跑 `projection generate`；对 `aar` 重新执行一次 public release 确认。

**批次 3**：`git mv archive audit release ledger/`；改 `paths.py` 6 个属性、`schemas.yaml` 的 `durable_records` 4 项、`policy.yaml` 的 `release.public_confirmation_path`/`durable_audit_path`/`public_release_authority.*_path`/`backup.durable_manifest_path`，以及跨 vault 模板 `source_lineage_operation_path`。

**降级落位**：`content/sources/` 下被误登记的加工文档 → 写 `content/working/<domain>/<id>.md`，front matter 只留 `legacy_path`、`snapshot_sha256`、`domain`、`title`，外加取得到时才写的 `legacy_first_commit_at` → 归档与 manifest 不动 → 整批一条 CDR。它不产生 object 身份，因此不走 preview/apply 的对象协议，只受 `working_contract_error()` 的入口约束。

`legacy_first_commit_at` 是 `legacy_path` 首次进入 Git 的作者时间，由 `classify` 求得写进清单、`apply` 原样落位不重算。它**不叫 `created_at`**：实测 161 篇里 156 篇同属 2025-07-06 的一次批量导入，叫 `created_at` 会把导入日误读成创作日。不用 mtime 的原因是 mtime 已成噪声——存量原文与副本的 mtime 全被迁移重写成同一天，落位还会再重写一次。取不到时不写该键（空值假装有时间比缺键更糟），清单的 `legacy_time_unresolved` 显式给出篇数。`content/working/` 的 TTL 判定仍按文件 mtime，不改用该字段：否则落位当天 161 篇会同时"超期"，报告失去筛选力。

**升级**：`content/working/` → `content/wiki/` 是**逐篇人工重写**，不是移动：需补齐八段正文、claim/evidence 映射，并走通道 A 的确定性校验 + 人工确认。不存在批量升级实现。

**`review_by`**：作者可选填写 → 不参与任何 hash → `doctor` 在到期时列入清单。

## 失败流程

- 批次 2/3 之后 `public_release` 派生为 `false` 是**预期行为**（`hash_change_behavior: retain-old-event-but-derive-false`），不得当作故障处理，也不得通过直写 Front Matter 绕过。
- `content/working/` 缺少 `source_ref` 且缺少 `legacy_path` → 拒绝写入，返回 `schema_invalid`；不允许"来源待补"的中间状态，与 §5.9 一致。
- `content/working/` 下的文件被写进某篇 wiki 的 `evidence.targets` → 该 target 没有 `object_ref`，resolution fail-closed，页面无法进入 `review`。
- `doctor` 遇到历史 `applied_files` 中已不存在的路径 → 必须报告为「历史路径」而不是 stranded/缺失。这是 LAY-004 的直接要求。

## 幂等与并发

unmanaged 层不进入 `before_hashes`/`after_hashes`，因此手工编辑 `content/working/` 与后台 apply 的路径集不相交，`locks.scope: per-vault` 无需扩展。`git mv` 是一次性操作，不属于 operation 协议，执行期间不得有未完成的 operation（先跑 `doctor` 确认无 `awaiting_confirmation`/`applied_index_pending`）。

## 安全边界

`content/working/`、`content/journal/`、`content/decisions/` 位于「当前可用的最私密 vault」。未挂载 private vault 时它们在 public checkout 内，其内容按 `confidentiality: public` 处理；挂载后 internal 素材使用该 vault 自己的 `content/working/`。三层永远不进 projection，因此不参与 leak gate 的 dist 扫描；它们在 input-tree 扫描中按 `unmanaged_excluded_from` 显式排除，而不是靠"未声明"被忽略——`build.warning_policy: blocking-unknown-v1` 会把未声明路径当阻断。

## 测试策略

- 迁移批次的主护栏是既有 345 个测试全绿 + `doctor` 正常 + `projection generate` 成功。
- `review_by` 的唯一真正验收点是「加字段后 `content_sha256` 与 `evidence_sha256` 逐字节不变」，fixture 必须取 `content/wiki/reading-notes/how-to-read-a-book.md` 的真实 hash，不构造假 hash。
- 历史记录不变性用真实的 254 条 operation 记录做重算校验，不用合成记录。

## 迁移与回滚

三个批次各自是一个 commit，可独立 `git revert`。批次 2/3 revert 后需再执行一次 public release 确认（hash 回到旧值，旧事件重新匹配则自动恢复 `true`）。`docs/<domain>/` 不参与搬移，按 §16 的退役条件在迁移完成后删除。

## 未决问题

- `doctor` 当前是否会重新解析 `applied_files`：执行批次 2 前必须先确认，若会则需先实现 LAY-004 的历史路径容忍。
- 挂载第一个 private vault 后，unmanaged 层单例是否够用（ADR-0014 的重新评估条件之一）。
