# 存量内容迁移与质量清理实现设计

- 状态：Implemented（2026-08-28；legacy inventory 基础能力）
- 相关 Feature：F010
- 相关规范：MIG、SRC、WIKI、EVD、WEB
- 相关 ADR：ADR-0001、ADR-0005、ADR-0009
- 相关验收：[F010](../acceptance/F010-content-migration.md)

## 迁移原则

本轮成熟方案调查：借鉴 Quartz/Dendron 的路径与 route map 思路、Trafilatura/Docling 的来源形态分类边界；inventory 只做确定性扫描，不把 URL/字数推断为事实正确性，也不改写旧 `docs/`。

旧 `docs/` 是迁移输入，不是迁移后的 canonical source。迁移器只生成 inventory、preview、source/wiki draft 和 route map，不自动把内容标记为 published，也不改写旧文件。

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
