# ADR-0020：内容晋升是转换作业，claim 中间产物是一等输入

- 状态：Proposed
- 日期：2026-09-14
- 相关规范：LAY、WIKI、EVD、QST
- 相关 Feature：F002、F003、F008、F010
- 相关 ADR：ADR-0017（实体与存储模型）、ADR-0018（claim 粒度与模板契约）
- 取代目标：无（本 ADR 新增契约）

## 背景

**晋升（working → wiki）目前没有任何工具，也没有任何契约。** working 是"你的观点"的临时载体（`LAY-002` 定义为 unmanaged 层，无 object 身份），wiki 是"结构化 + 有据 + LLM 验证过"的 gold 层，但两者之间只有人手工搬运。

代价已经在数据上体现：

- 当前 20 篇 `llm-*` working 笔记（**206,252 字**正文 + 20 个 `.claims.json`）**在 `content/wiki` 中覆盖率为 0**——它们是已完成、每条主张都挂了来源、但一步都没落地的成品草稿。
- 更早一批（145 个 `working-*` source）是经"人工搬运"落地的，因此 provenance 只剩 id 前缀这一命名约定，front matter 里没有任何回指字段。

同时用户提出一条新约束：**working 转 wiki 时必须给出 claim。**

关于 `.claims.json`（20 个文件）：实测结构为 `[{claim, source_id, exact_quote}]`，每篇恰好 10 条、共 200 条；但 **代码引用数为 0**（`tools/`、`backend/`、`frontend/scripts/`、`config/`、`docs/` 全量检索无任何读写）——没有生成命令、没有 schema、没有校验、没有消费者，是一个孤儿产物。

## 候选方案

- **A：文件移动 + 人工补 claim**（现状）。最省实现，但不可重跑：改了 working 或改了 claim 之后，wiki 侧无法重新生成，只能手工同步——**这正是"双重事实源"的典型成因**（source 正文与 archive 快照 100% 重复就是这么来的）。
- **B：一次性转换脚本**。比 A 略好（有自动化），但仍不可重跑，且脚本不入库即成一次性代码。
- **C：可重跑的转换作业 + 显式 lineage**（medallion 的 silver → gold；dbt 的 model 与 `ref()` 自动 lineage）。分层纪律是：**升级是一个作业产出新数据集，不是让同一行"变成"上一层**；作业可重跑，lineage 显式记录。

## 决策

采用方案 C。

**1）晋升 = 一个可重跑的转换作业。**

- 触发：`wiki new --from-working <id>`（命令面见 ADR-0017，不单独设 `working` 命令）
- 输入：working 笔记正文 + 同目录 `.claims.json`
- 输出：**模板已填的 wiki 草稿**——10 节模板骨架 + claim 已按 G2 落到 4 个需证据小节 + 引文已锚定 + 一份校验报告
- 产物直接落到工作区（`content/wiki/...`），由 `git diff` 审核、由 `git commit` 批准（ADR-0019）
- lineage：写入 `prov:wasDerivedFrom`，指向输入 working 笔记与源 source
- **确定性要求**：同输入必产出同输出。实现上必须排序稳定、不写入时间戳、不依赖随机性；否则"可重跑"退化为"每次产出都不同"，作业失去意义

**2）`.claims.json` 升级为正式中间产物。**

- 定义 schema `claim-set/v1`：`[{claim, source_id, exact_quote, section?}]`
- 具备**生成命令**（从 source 快照抽取 claim 候选）与**校验**（`exact_quote` 必须在其 `source_id` 的快照中逐字命中——与 ADR-0019 的 per-claim 硬门禁同一条规则）
- 随 working 笔记一并受 git 跟踪（2026-09-14 已将 `content/working/` 的 40 个文件纳入 git，此前 0 个被跟踪）

**3）晋升完成后，working 侧进入删除候选。**

- `LAY-002`/`LAY-003` 的"working 层到期只产生 `doctor` 报告、工具不得自动删除内容"保持不变。
- 但删除的**前置条件**明确为：对应 wiki 已通过校验（即 gold 层已完整承载该观点）。
- 这条规则消解了一个潜在的双重事实源：claims 会同时存在于 `.claims.json`（输入侧）与 wiki front matter（产出侧）。二者不是重复，而是**同一信息在两个成熟度层的表示**（medallion 各层各有自己的数据）；只有 working 侧被删除后，重复才真正消失。

## 后果

- 20 篇 `llm-*` 的落地有现成输入：206,252 字正文 + 200 条带 `source_id`/`exact_quote` 的 claim，无需从零撰写。
- "改了 working 或改了 claims 之后要手工同步 wiki"这件事消失——重跑作业即可。这与 ADR-0018 决定"`## 证据映射` 表改为派生视图"是同一个思路：**能派生的就不手工维护。**
- `.claims.json` 从"代码引用数 0 的孤儿产物"变成有 schema、有生成、有校验、有消费者的正式中间产物。
- 代价一：需要定义 `claim-set/v1` schema 与生成/校验命令，这是新增的实现面。
- 代价二：确定性要求会约束实现（稳定排序、无时间戳），并在测试上要求"同输入两次运行产物一致"。
- 代价三：`--from-working` 产出的草稿质量取决于"claim → 小节"的自动映射能力。若映射不可靠，人工修订量可能超过手写成本——需以 1 篇实测决定（见重新评估条件）。
- 与 ADR-0019 的交互：`.claims.json` 的 `exact_quote` 校验**必须**复用同一条 per-claim 引文校验实现，不得有两份引文匹配逻辑。

## 重新评估条件

- **以 1 篇实测决定是否继续**：若 `--from-working` 产出的草稿人工修订量超过手写总成本的 50%，说明自动映射不划算，应退回到"作业只做脚手架（模板 + 引文锚定），claim 全部人工撰写"。
- 若后续 wiki 大多不再从 working 晋升（实测当前 208 篇 wiki 引用 145 个 `working-*` source，但 `content/working/` 仅存 20 个文件，说明历史批次是"晋升后即删"），说明该作业不是主路径，应评估降级为按需工具。
- 若 `.claims.json` 与 wiki front matter 的 claim 长期不一致且无法通过重跑收敛，说明两侧都成了手工维护的事实源，应改为"wiki claim 为唯一真相、`.claims.json` 降为一次性输入且不保留"。
- 若 `claim → 小节` 的映射需要频繁人工干预，应考虑让作业输出"未归类 claim 列表"而非强行归入某节，把归类交给撰写者。
