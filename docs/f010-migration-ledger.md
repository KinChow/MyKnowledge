# F010 迁移台账（docs → sources）

> 目的：把迁移作为**受控批次**管理，防止返工与重复劳动。
> 状态字段：`Pending → In Progress → Done → Skipped(decision)`。
> 本文是唯一的人工决策记录；**逐篇状态不手写在本表**，由清单命令从
> `sources/` 实际状态派生（见"防返工约束"），避免台账与真实状态漂移。

## 1. 判定规则（先定规则，再动内容）

| 规则 | 判定 | 处理 | 依据 |
| --- | --- | --- | --- |
| R1 | 工程文档（`acceptance/` `adr/` `technical-design/` `deferred/` + 4 个根级规范文档，共 45 篇） | **留在 `docs/`，不迁移** | 无来源/快照语义，是仓库开发文档；混入 sources 污染 manifest |
| R2 | `contents.md` 等 index 形态（32 篇） | 不迁移；**全部批次完工后随 B5 删除**（不保留） | 手工导航页是 legacy 腐化源；导航由 projection graph 派生 |
| R3 | empty 形态（16 篇） | **不丢弃：登记为"待补内容"清单，补充内容后按 R4/R5 迁移** | 空文档多为开了头的知识点占位，有补充价值 |
| R4 | 含外部 URL 的文章（23 篇） | **优先批**：可回溯出处，`source_type` 可标 `url/doc/book` | 迁移成本低、证据链完整 |
| R5a | 无外部 URL 的文章 | **先联网检索出处**（标题/关键概念检索）；找到出处的按 R4 处理（`url/doc/book`） | 多数笔记源自学习过的外部资料，只是当时没记链接 |
| R5b | 检索确认无外部出处的本人总结 | **迁移终点是 wiki 层而非 source 层**：作为个人知识写入 wiki（provenance 标注为本人综合，不伪装外部证据），或先以 `personal-note` 入 sources 再提炼 wiki | 个人总结不是"来源"，是知识本身；corroboration 为空是事实而非缺陷。**待决**：wiki schema 的证据门禁是否接受"本人综合"类 claim（见 §6） |
| R6 | 一切迁移必须经 SourceIngestor（`tools.cli source`）/ WriteOperation | 禁止 `git mv` 物理搬家 | 迁移的价值在 front matter + snapshot + manifest 登记 |
| R7 | wiki 提炼与 source 迁移解耦 | R4/R5a 走 Source→Wiki 链路；R5b 可直接 wiki | 避免为迁移阻塞在提炼质量上 |

## 2. 批次计划

| 批次 | 范围 | 数量 | 状态 | 完成定义（DoD） |
| --- | --- | --- | --- | --- |
| B0 试点 | `linux-compilers`、`von-neumann-architecture`、`tools/git-commands` | 3 | **Done**（2026-08 前） | front matter + snapshot + manifest 登记（已验证） |
| B1 样本批 | R4 优先 10 篇 + 每域各 1-2 篇覆盖（含 R5 形态） | ~15 | Pending | 规则 R1-R7 实测校准；记录单篇吞吐 → 全量估算；**F007 用本批真实内容跑通 projection 多页发布** |
| B2 小域批 | `tools` + `work-methods` + `multimedia` + `reading-notes` 剩余 | ~23 | Pending | 同 B0 DoD；B1 校准后的规则执行 |
| B3 大域批 | `computer-science` 分子域分批（建议 4 批 × ~60 篇） | 250 | Pending | 同上；每批后跑 `validate` + manifest 全量核对 |
| B4 复核批 | R3 的 16 篇 empty：登记"待补内容"清单，**补充内容后**按 R4/R5 迁移 | 16 | Pending | 逐篇补充并迁移；不丢弃 |
| B5 退役批 | `mkdocs.yml` + Astro legacy 预览模式退役；**删除 32 篇 `contents.md` 导航页** | — | Pending | 前置：F007 projection 链路以真实多页内容验收通过 |

## 6. 待决项（B1 前需拍板）

1. **R5b 的 wiki 证据门禁**：无外部证据的"本人综合"类 wiki 是否允许（例如 `claim_type: synthesis` 或 `evidence_state` 白名单）？涉及 F002/F003 规范修订，B1 样本批前必须定，否则 R5b 路径无法执行。
2. **R5a 联网检索的归属判定**：检索到的"疑似出处"需人工确认确为学习来源（防止把无关网页当出处），B1 中定义确认标准（如内容关键句匹配）。

## 3. 当前实测基线（2026-08-28，inventory v1）

```bash
python -m tools.cli inventory --output /tmp/inv.json   # 确定性重算，树 hash 绑定
```

- 总量 321：知识内容 276（computer-science 250 / work-methods 12 / multimedia 11 / tools 2 / reading-notes 1）+ 工程 45
- 形态：article 273 / index 32 / empty 16
- 出处：有外部 URL 23 / 无 298
- `sources/` 现有 3 篇（= B0）

## 4. 防返工约束

1. **单一事实源**：某篇是否"已迁移"以 `sources/` + `archive/manifest.jsonl` 为准；本表只记批次与决策，不维护逐篇清单。
2. **批次不并行开启**：B1 未校准规则前不动 B2/B3，防止规则变更导致已迁移篇目返工。
3. **顺序依赖**：B5（legacy 退役）必须在 F007 projection 以真实内容验收后；在此之前 `docs/` 知识域保持只读，**不删原件**（Source 导入是复制+快照，原件删除属于 B5）。
4. **每批收尾**：全量 `pytest` + `tools.cli validate` 抽查 + 本表状态更新，同批 commit。

## 5. 与主线的并行关系

迁移不阻塞 F005/F006 review（主线）；B1 样本批可与 F007 验收互为输入（B1 产出真实 source/wiki 供 F007 projection 验收）。`confirm-apply` CLI 独立小项可插任意空档。
