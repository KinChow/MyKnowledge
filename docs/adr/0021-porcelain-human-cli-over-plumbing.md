# ADR-0021：人用入口 = porcelain 层，tools.cli 保留为 plumbing

- 状态：Accepted
- 日期：2026-09-15
- 相关规范：命令面（§0.2）
- 相关 Feature：F001–F013（全命令面）
- 相关 ADR：ADR-0017（命令面收敛到 7 条人输入的终态）、ADR-0019（写入直落 + git 审批）
- 取代目标：无（本 ADR 新增）

## 背景

命令面对人过宽：`tools.cli` 22 条命令 + `skill` 25 个 action + backend HTTP。用户痛点明确为**人手输的命令太多**（agent 调用面不需动）。实测 22 条里约 7 条本不该占人输入面（`index`/`projection`/`local-projection`/`matrix`/`skill`/`read`/`backlinks` 是派生、构建或 agent 面），其余压力来自内容流水线动词散落——`source→anchor→validate→audit→confirm→release` 六个平级命令本是一件事的六个阶段。

ADR-0017 已给出终态（人输入收敛到 7 条名词），但它绑定实体模型重构（5 实体 + 统一动词引擎 + claim 一等对象），工作量大、跨会话。关键观察：**命令面收敛（展示层）与实体模型（存储层）是可分离的两件事。**

## 候选方案

- **A：原地重构 `tools.cli` 成 noun-verb。** 命令数直接降，但改名会打断 454 个测试 + CI + skill 对旧命令名的依赖，churn 大。
- **B：新增薄 porcelain 入口，转调现有 `tools.cli`，后者保留为 plumbing。** git 的 porcelain（status/add/commit）/plumbing（hash-object/commit-tree）分层是成熟先例；`gh`/`kubectl` 的"少量名词 + 第二层动词"同源。
- **C：上 TUI/REPL。** 多一个渲染层的永久维护面，而痛点只是"命令多"，不值。

## 决策

采用方案 B。

- 新增 `python -m tools.myk`（porcelain）：7 个名词 `source / wiki / question / query / build / doctor / backup`，noun-verb 分派，全部转调 `tools.cli.COMMANDS`，**不复制任何 domain 逻辑**。
- `tools.cli`（plumbing）保留不动：细粒度，供 CI / skill / 测试链式调用。`matrix`（pre-commit 钩子）与 `skill`（agent 面）不进 myk 人输入面。
- 人性化默认落在 porcelain 层：`--actor-id` 从 git 身份自填、`--json` 反选、action 命令默认打印一行人类摘要。
- 规矩：**myk 是人的唯一入口；面向人的文档只写 myk，`tools.cli` 只出现在"给机器/agent"的语境。**
- 映射 `read`/`backlinks`→`query`、`projection`/`index`→`build`、`vault`→`doctor`，与 ADR-0017 命令面一致——本 ADR 是 ADR-0017 命令面那一节里"与实体模型无关"的先行兑现。

## 后果

- 人手输面从 22 条降到 7 个名词，零底层改动、可逆、当天生效。
- 代价一：短期新旧两套叫法并存（缓解：面向人的文档一次性切到 myk、不留别名）。
- 代价二：总入口数增加（cli + myk），但人只看 myk。
- 与 ADR-0017 的关系：本 ADR 只做展示层；实体模型 / 统一动词引擎 / claim 一等对象仍归 ADR-0017。其未落地时 myk 只包已有能力（`source list/show/delete`、`wiki 新建` 等未实现动词先不造）。
- 因是 facade，ADR-0017 未来落地时 myk 的名词面不需再变，只是底层从多个 `main` 收敛为统一动词引擎。

## 重新评估条件

- 若 ADR-0017 实体模型落地、`tools.cli` 被统一动词引擎取代，评估 porcelain 是否直接建在引擎上、plumbing 是否还需保留。
- 若人开始频繁手敲 `index`/`projection` 等机器命令，说明人/机边界切错，重新划分。
- 若出现浏览类强交互需求（翻题库 / wiki 上下选），再评估 TUI（当前明确不做）。
