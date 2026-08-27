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
| B1 样本批 | R4 优先 10 篇 + R5a 3 篇（每域覆盖）+ empty 2 篇登记 | 13+2 | **In Progress** | 2026-08-28：13 篇已导入（10 R4 + 3 R5a，machine 吞吐 13 篇/0.1s，人工成本集中在出处确认）；R5a 检索结论待 owner 确认（见 §7）；empty 2 篇（`class-and-struct`、`pointer`）登记待补 |
| B2+B3 source 层 | 全部知识域 article（一次执行，原计划分批；机器成本为零） | 218+13 | **Done（source 层）** | 2026-08-28：B1+B2 批量导入时过滤未限域，实际完成 B3 的 source 层；4 篇根级工程文档被 domain 枚举校验天然拦截（R1 防线生效） |
| B3 大域批（source 层已并入上格） | wiki 提炼与出处检索（R5a）按需分批 | 250 | Pending | source 层已完成；wiki 化按域渐进 |
| B4 复核批 | R3 的 16 篇 empty：登记"待补内容"清单，**补充内容后**按 R4/R5 迁移 | 16 | Pending | 逐篇补充并迁移；不丢弃 |
| R8 | 跨目录同名文件（stem 冲突） | source_id 用 `parent-stem` 消歧（如 `gpu-overview`、`git-commands`）；批量导入前检查 inventory stem 重复组 | B2 执行时 69 篇 contents/互撞暴露；classifier 已修复 contents.md 一律判 index |

## 9. B2/B3 source 层批量执行记录（2026-08-28）

- 实际导入 231 篇（B1 13 + B2/B3 218），4 篇根级工程文档被 domain 校验拦截；
- 暴露并修复 3 个系统问题：
  1. **FrontMatter render/parse roundtrip 不保真**（python-frontmatter 库对 body 加前导空行/剥结尾换行）→ 161 篇 source 与 snapshot hash 断链；已改为适配层原样拼接 + 精确切片，全部重写对齐，校验 0 失败（`tools/front_matter.py`）；
  2. **inventory 分类器把富目录页（contents.md）误判为 article** → 69 篇 R2 导航页混入迁移；已修复（文件名 contents.md 一律 index）；
  3. **同名 stem 互撞静默覆盖** → 新增 R8 消歧规则，overview×3/commands×2 已用 parent-stem id 补回；
- 全量 `pytest`（338）与 `SourceValidator`（sources 全部）通过。

| B5 退役批 | `mkdocs.yml` + Astro legacy 预览模式退役；**删除 32 篇 `contents.md` 导航页** | — | Pending | 前置：F007 projection 链路以真实多页内容验收通过 |

## 6. 待决项

1. ~~**R5b 的 wiki 证据门禁**~~ **已决（2026-08-28）**：模型原生支持——`personal-note` source 作 provenance + `support: personal` claim；`evidence_state` 表达映射完整性（supported），信任降级由 `strength: personal` 承载，不进证据阻断集合，published 不被挡。规范 §6.7 已加澄清段；端到端证据 `tests/validation/test_synthesis_claims.py`。
2. **R5a 联网检索的归属判定**：检索到的"疑似出处"需人工确认确为学习来源（防止把无关网页当出处），B1 中定义确认标准（如内容关键句匹配）。

## 7. B1 R5a 出处检索结论（2026-08-28，待 owner 确认）

| 文档 | 检索结论 | 证据 | 建议出处 |
| --- | --- | --- | --- |
| `work-methods/AAR` | 外部方法论转述 | 四个结构化问题与美军 TC 25-20 AAR 逐条对应（多来源交叉：军研论文、百度百科"行动后学习机制"） | U.S. Army TC 25-20 / After Action Review |
| `reading-notes/how-to-read-a-book` | 读书笔记 | 四阅读层次/分析阅读规则与艾德勒&范多伦《如何阅读一本书》（商务印书馆中译）逐条对应 | 艾德勒、范多伦《如何阅读一本书》 |
| `tools/code-server` | 工具官方文档摘录 | 正文首行即官方安装脚本 `code-server.dev` | https://code-server.dev / github.com/coder/code-server |

确认标准（B1 校准）：笔记关键结构与检索结果的权威来源逐条对应（非仅主题相似）即判为出处；仅主题相似的判 R5b 本人综合。

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

## 8. B1 wiki 提炼演示（AAR）中发现并修复/待修的问题（2026-08-28）

| 问题 | 状态 |
| --- | --- |
| `derived.has_public_confirmation` 只 glob `evt_*.json`（下划线），与 `write_event`/generator 的 `*.json` + safe_id 连字符命名不一致，导致发布确认事件永不生效 | **已修复**（统一为 `*.json`，含注释）——这是 F007 发布链路首次真实闭环的直接 blocker |
| `tools.cli validate` 对含 PosixPath 的 report 做 json.dumps 崩溃 | 待修（report 序列化前 str 化） |
| `release_confirmation.write_event` 相对 root 下 `relative_to(root.resolve())` 崩溃（事件已写入但返回失败） | 待修（构造时 resolve） |
