# 存量内容迁移与质量清理实现设计

- 状态：Implemented（2026-08-28；legacy inventory 基础能力）
- 相关 Feature：F010
- 相关规范：MIG、SRC、WIKI、EVD、WEB
- 相关 ADR：ADR-0001、ADR-0005、ADR-0009
- 相关验收：[F010](../acceptance/F010-content-migration.md)

## 迁移原则

本轮成熟方案调查（2026-08-28）：Quartz（<https://github.com/jackyzha0/quartz>，MIT）和 Dendron（<https://github.com/dendronhq/dendron>，AGPL-3.0）分别提供 route/backlink 图谱与层级迁移经验；本轮只复用 route map/幂等清单思想，避免直接采用会扫描整个工作树的默认导入器。Trafilatura（<https://github.com/adbar/trafilatura>，Apache-2.0）和 Docling（<https://github.com/docling-project/docling>，MIT）可作为 HTML/PDF 抽取器，但其网络/二进制依赖和抽取不确定性不适合直接写 canonical；当前迁移按扩展名识别 Markdown/HTML/TXT/PDF，复用 `TextExtractor` 的 Trafilatura/pypdf/UTF-8 handler，Office/Docling 仍保持待定。

本轮代表性样本调查（2026-08-27）：继续复用 Quartz v4（MIT）的 content pipeline、Dendron（AGPL-3.0）的层级/链接迁移清单、Trafilatura 2.2+（Apache-2.0）与 Docling 2.x（MIT）的抽取器候选。`apply_sample` 使用现有 SourceIngestor 的 local-file 稳定读取、snapshot/hash 和 manifest，再用 WriteOperation 生成 `status: draft` Wiki；直接复制 `docs/` 到 `wiki/` 会绕过 Source/evidence/confirmation，明确排除。抽取器缺失、输入竞态或写入失败均保持 pending/blocked，旧 docs 永不改写。

本轮迁移幂等调查（2026-08-30）：Dendron 的迁移清单/稳定 ID（AGPL-3.0，<https://github.com/dendronhq/dendron>）与 Quartz 的 content pipeline（MIT，<https://github.com/jackyzha0/quartz>）都把输入路径和内容摘要作为可重放边界；替代方案是每次重复执行底层 writer，虽然文件最终可能相同，却无法证明同一迁移意图，也会重复触发 Source/provider。采用 owner-local `audit/migrations` durable record，以 `legacy_path + body_sha256 + migration_version` 为幂等键；命中时直接重放既有结果，输入 hash 改变则生成新记录并重新经过 Source-first 门禁。记录不包含绝对路径或正文。

本轮批量迁移调查（2026-08-30）：Quartz `v4.0.8`（MIT，<https://github.com/jackyzha0/quartz/releases/tag/v4.0.8>）的内容管线按确定性输入生成路由；Dendron 主分支（AGPL-3.0，<https://github.com/dendronhq/dendron>）的迁移实践强调层级清单和逐项状态。两者的共同边界是批次只负责编排，单项仍需可重放和可定位。采用 `apply_batch` 的 `migration-batch/v1` 清单：先生成批次 key，再逐项调用既有 `apply_sample`，成功项保留、失败项显式 `blocked`、未确认时整体只返回 `awaiting_confirmation`；批次记录使用 `record_sha256` 原子写入并可重放。直接把整个 `docs/` 目录复制到 canonical 目录作为替代方案会绕过 Source snapshot/evidence/Wiki writer，明确排除。离线模式只读取本地 inventory，外部抽取器/provider 不可用时保留 pending/blocked；升级影响限定在批次 schema 和单项 durable record，不改变旧 docs。

本轮 replay 完整性调查（2026-08-30）：Git object hash 和 SQLite durable record 的自校验要求记录内容与摘要绑定；替代方案是只验证 migration key，篡改者可伪造 `result` 并绕过 Source/Wiki 门禁。迁移记录现在通过 `record_sha256` 校验，且使用原子写入；校验失败视为未命中，重新执行完整 Source-first 流程。

本轮确认竞态调查（2026-08-27）：Quartz 的 content pipeline（MIT，<https://github.com/jackyzha0/quartz>）与 Dendron migration workspace（AGPL-3.0，<https://github.com/dendronhq/dendron>）都把输入清单/树摘要作为阶段边界；替代方案是只要求布尔 `confirmed`，无法证明用户确认的内容仍是 preview 内容。故 `apply_batch` 支持调用方回传 `expected_preview_sha256`，Apply 前重新生成 inventory/route plan 并逐字节比较 preview hash；hash 不一致返回 `input_changed` 且不调用任何 Source/Wiki writer。该门禁离线运行，升级只影响批次调用契约，不改写原 `docs/`。

本轮 rollback 调查（2026-08-27）：Dendron 的迁移清单/稳定 ID（AGPL-3.0，<https://github.com/dendronhq/dendron>）用于精确定位一次迁移产物，Quartz v4 content pipeline（MIT，<https://github.com/jackyzha0/quartz>）保留源内容并允许重新生成输出；Git 的对象/工作树 hash（GPL-2.0）提供“只撤销未漂移生成物”的 precondition 思路。替代方案是 `rm -rf wiki/ sources/` 或全库 reset，会删除无关用户工作和 immutable evidence，明确排除。`rollback_sample` 从已自校验的 `migration-record/v1` 读取仓库相对 Source/Wiki 路径及完成时 hash，先生成 purge preview，人工确认后委托 `WriteOperation`；旧 `docs/`、content-addressed archive、manifest 和 audit 均保留。任何输出漂移、缺失或 symlink 均 fail-closed；成功写入 `migration-rollback-record/v1` 并可幂等重放。离线无网络，不执行 Git reset/commit/push。

DOCX 仅通过 Docling handler 处理；未安装时返回 `extractor_unavailable:docling`，禁止退回二进制 UTF-8 解码。

链接修复增量（2026-08-27）：参考 Quartz 的 canonical absolute link 与 Dendron 的 route rewrite，`apply_sample` 只把 inventory 中可确定映射的相对 `.md` 链接改为 `/legacy/...` route；外部 URL、绝对路径和 unresolved target 原样保留，并在结果中分别记录 `repaired`/`unresolved`。不扫描或改写原 `docs/`。

CLI 增量（2026-08-27）：`python -m tools.cli migrate --apply-sample <legacy-path> --confirm` 仅是 `apply_sample` 的薄入口，未提供 `--confirm` 时返回 `awaiting_confirmation`；CLI 不拥有第二套迁移规则。

旧 `docs/` 是迁移输入，不是迁移后的 canonical source。`tools/migrate_legacy.py` 只生成 inventory、preview、source/wiki draft 描述和 route map，不自动把内容标记为 published，也不改写旧文件。外部抽取器缺失时结果必须保持 pending，不能伪造完成。

## 阶段

1. Inventory：由版本化的 `tools/inventory_legacy.py`（或等价确定性工具）记录相对路径、字节数、`body_sha256`、内容形态、外链、已有标题、候选 domain、当前 route 和迁移状态；输出同时包含输入 tree hash、classifier version、阈值和生成时间，避免历史统计被误当作当前事实。
2. 分类：空文件/导航页/占位页/实质文章/资源清单/聚合页分别映射 `planned`、`index`、`reference` 或完整 source-first 流程。
3. Source：网络资料走 `fetch`，本地 HTML/PDF/代码/日志统一走 `local-file`，无出处内容只能进入 personal source 或 pending，不得伪造 external source。
4. Wiki：生成稳定 ID、claim/evidence 草稿、snapshot selector 和 public/private target；经过 deterministic/LLM validation 后由人工决定 publish。
5. Route：生成旧路径到新 public route 的 map；未解析链接逐条标记，不删除旧对象。

## ID 与回滚

迁移 ID 由规范化路径/标题生成 kebab-case 候选；同 Vault 冲突时必须在 preview 中人工选择稳定后缀，不能按文件覆盖。保存 `migration_id`、输入文件 hash、输出 object IDs、目标 Vault 和 route map hash。`content_verdict`、provenance 归类和最终发布必须作为人工审核字段保留；工具不得从“有 URL/字符数”自动推断事实正确性。任何阶段失败只清理 staging，保留旧 docs、旧 dist 和已完成对象；已应用对象通过 operation record 逐项回滚或继续，不执行全库 reset。

## 退出门

代表性样本必须覆盖 URL、local-file HTML/PDF、personal note、无来源、冲突来源、长聚合页和 unresolved link。只有 inventory 完整、每个结果有 completed/pending 状态、public projection leak gate 通过且旧站点可回退，才允许扩大迁移范围。
