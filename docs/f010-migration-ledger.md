# F010 迁移台账（docs → sources）

> 目的：把迁移作为**受控批次**管理，防止返工与重复劳动。
> 状态字段：`Pending → In Progress → Done → Skipped(decision)`。
> 本文是唯一的人工决策记录；**逐篇状态不手写在本表**，由清单命令从
> `sources/` 实际状态派生（见"防返工约束"），避免台账与真实状态漂移。

> **生命周期声明（2026-09-02）**：本文是**迁移过程决策记录**，不是规范，
> 不参与 ruleset 抽取；只承担 F010 迁移窗口期的治理职责。当系统设计 §16
> 的退役条件满足（迁移 inventory 无未终结条目、`docs/` 无 `<domain>/`
> 子目录）时，本文随 `docs/` 退役归档至 `ledger/`（F013 批次 3 后）或
> 与 docs/ 知识域一并归档，不长期驻留规范目录。

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
| R8 | 跨目录同名文件（stem 冲突） | source_id 用 `parent-stem` 消歧（如 `gpu-overview`、`git-commands`）；批量导入前检查 inventory stem 重复组 | B2 执行时 69 篇 contents/互撞暴露；classifier 已修复 contents.md 一律判 index |

## 2. 批次计划

| 批次 | 范围 | 数量 | 状态 | 完成定义（DoD） |
| --- | --- | --- | --- | --- |
| B0 试点 | `linux-compilers`、`von-neumann-architecture`、`tools/git-commands` | 3 | **Done**（2026-08 前） | front matter + snapshot + manifest 登记（已验证） |
| B1 样本批 | R4 优先 10 篇 + R5a 3 篇（每域覆盖）+ empty 2 篇登记 | 13+2 | **In Progress** | 2026-08-28：13 篇已导入（10 R4 + 3 R5a，machine 吞吐 13 篇/0.1s，人工成本集中在出处确认）；R5a 检索结论待 owner 确认（见 §7）；empty 2 篇（`class-and-struct`、`pointer`）登记待补 |
| B2+B3 source 层 | 全部知识域 article（一次执行，原计划分批；机器成本为零） | 218+13 | **Done（source 层）** | 2026-08-28：B1+B2 批量导入时过滤未限域，实际完成 B3 的 source 层；4 篇根级工程文档被 domain 枚举校验天然拦截（R1 防线生效） |
| B3 大域批（source 层已并入上格） | wiki 提炼与出处检索（R5a）按需分批 | 250 | Pending | source 层已完成；wiki 化按域渐进 |
| B4 复核批 | R3 的 16 篇 empty：登记"待补内容"清单，**补充内容后**按 R4/R5 迁移 | 16 | Pending | 逐篇补充并迁移；不丢弃 |
| B5 退役批 | ~~`mkdocs.yml`~~（**已于 2026-08-28 退役**，含 pip 依赖与 README 链路）+ Astro legacy 预览模式退役；**删除 32 篇 `contents.md` 导航页** | — | In Progress | mkdocs 部分完成；剩余前置：F007 projection 链路以真实多页内容验收通过 |

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

## 8. 执行记录（按时间正序）

### 8.1 B2/B3 source 层批量执行记录（2026-08-28）

- 实际导入 231 篇（B1 13 + B2/B3 218），4 篇根级工程文档被 domain 校验拦截；
- 暴露并修复 3 个系统问题：
  1. **FrontMatter render/parse roundtrip 不保真**（python-frontmatter 库对 body 加前导空行/剥结尾换行）→ 161 篇 source 与 snapshot hash 断链；已改为适配层原样拼接 + 精确切片，全部重写对齐，校验 0 失败（`tools/front_matter.py`）；
  2. **inventory 分类器把富目录页（contents.md）误判为 article** → 69 篇 R2 导航页混入迁移；已修复（文件名 contents.md 一律 index）；
  3. **同名 stem 互撞静默覆盖** → 新增 R8 消歧规则，overview×3/commands×2 已用 parent-stem id 补回；
- 全量 `pytest`（338）与 `SourceValidator`（sources 全部）通过。

### 8.2 B1 wiki 提炼演示（AAR）中发现并修复/待修的问题（2026-08-28）

| 问题 | 状态 |
| --- | --- |
| `derived.has_public_confirmation` 只 glob `evt_*.json`（下划线），与 `write_event`/generator 的 `*.json` + safe_id 连字符命名不一致，导致发布确认事件永不生效 | **已修复**（统一为 `*.json`，含注释）——这是 F007 发布链路首次真实闭环的直接 blocker |
| `tools.cli validate` 对含 PosixPath 的 report 做 json.dumps 崩溃 | 待修（report 序列化前 str 化） |
| `release_confirmation.write_event` 相对 root 下 `relative_to(root.resolve())` 崩溃（事件已写入但返回失败） | 待修（构造时 resolve） |

### 8.3 补充迁移：有内容的 article 全量导入（2026-09-02）

- **范围**：上轮实测发现 docs/ 知识域有 6 篇有正文的 article 未进 manifest（此前 B2/B3 批量导入漏掉）；
  按 owner 决策"有内容的都迁移，后续优化文档"，本批全部导入。
- **规则应用**：6 篇均无外部 URL，非外部来源快照 → 走 `--personal-note` 通道
  （`source_type: personal-note` + `origin: personal`），避免 `--from-file` 的
  `origin: external` 失真登记（与 reposition 改判同一原则，源头就不登记错）。
- **导入清单**（source_id / domain）：
  - `dry-principle` / computer-science
  - `yagni-principle` / computer-science
  - `algorithm-manual` / work-methods
  - `camera-competitive-product-analysis` / multimedia
  - `computer-hardware` / computer-science
  - `camera-provider-performance` / computer-science
- **完成定义**：6 篇均在 `content/sources/` 落位、front matter 完整（schema_version:
  source/v1, snapshot_sha256 绑定）、快照入 `archive/text/`、`archive/manifest.jsonl`
  登记 6 条新记录；全量 `pytest` 437 通过、`doctor --assert-clean` healthy。
- **遗留**：docs/ 知识域仍剩 39 篇空文档（R3 待补类），按规则登记待补不迁移；
  docs/ 原件按 §4.3 保持只读不删，待 B5 退役。迁移后内容优化由 owner 后续执行。

### 8.4 编译器向量化指南：去重 + 补源 + 修复（2026-09-02）

- **去重**：working 层 A 档 `compiler-vectorization-guide` 与 `a-guide-of-compiler-vectorization`
  为同一文档的重复导入（`snapshot_sha256` 逐字节一致）。保留 canonical
  `a-guide-of-compiler-vectorization`，删除重复副本 `compiler-vectorization-guide`；
  manifest/归档为 append-only 历史，不重写。删除后 working 层 161 → 160 文件。
- **补源**：为指南升级导入 `gcc-auto-vectorization` source
  （`source --url https://gcc.gnu.org/projects/tree-ssa/vectorization.html`，快照
  `2dff0614…`）；`llvm-auto-vectorization`（`llvm.org/docs/Vectorizers.html`，快照
  `15bcdf01…`）为既有 source 复用，未重复导入。
- **内容修复**：指南正文按联网核对修复 8 类问题（`-fveclib` 取值、`--param min-vect-loop-bound`、
  `-vectorize-loops` 措辞、`-02→-O2`、Unicode `≥`、未声明 `n`、汇编示例尾部逻辑、~12 处笔误）；
  "NEON 32 字节对齐最佳"经文献验证不成立，改为"16 字节向量宽度 + cache line"可辩护表述，
  真机实测留待验证项。front matter `snapshot_sha256` 保留指向归档原文，未动 archive。

### 8.5 编译器向量化指南：wiki 发布闭环（2026-09-03）

- **发布链全通**：`compiler-vectorization` wiki（id `compiler-vectorization`）确定性校验 0 error → LLM 审计 pass（18/18 supported, openai-compatible）→ owner confirm（op_6bd39884…, actor local-user）→ `status: published` → `release confirm`（evt-vec-guide-d958e2, actor zhouzijian01）→ public projection 生成、索引重建、query 可查 → `strength: verified`、`public_publishable: True`。
- **待验证项收口**：4 项验证完成 3 项（GCC -O2 实证：pass 启用 ≠ 实际向量化；GCC 诊断：`-ftree-vectorizer-verbose` 为 no-op 旧接口；LLVM 特性：clang 21 全默认向量化），验证结论并入正文；NEON 对齐的 Cortex 真机基准为唯一遗留项。验证方法段补"原生执行验证（arm64 主机）"一节。
- **working 移出**：`a-guide-of-compiler-vectorization` 完成使命，从 working 删除（内容已完整入 wiki，零删减）；working 161 → 159。manifest/归档为 append-only 历史，未动。
- **遗留说明**：`aar` 在 projection 中报 `lineage_record_missing`（既有问题，与本次无关，A 档剩余 55 篇升级时留意）。

### 8.6 AAR 定位纠偏 + 来源补建（2026-09-03）

- **定位纠正**：`work-methods/aar` 原为本人加工综述（reposition-plan 判 `intermediate`/C 档）却被登记为 source（`origin: external` + local-file）——登记失真。已从 `content/sources/` 迁至 `content/working/c-intermediate/work-methods/aar.md`，front matter 改造为 working 格式并记录定位判定（positioning 字段）。
- **来源补建**：新增 `aar-tc25-20` source（U.S. Army TC 25-20《A Leader's Guide to After-Action Reviews》，HSDL 官方 PDF，快照 `1588c243…`，pypdf 抽取），锚定 2 条 evidence：权威定义（`evidence-bd71610a92c6`）+ 陆军官方通告属性（`evidence-5ca92dbc3cf1`）。
- **wiki 重建**：`content/wiki/work-methods/aar.md` 重建为"蒸馏核心八段 + working 全文零删减"（此前只蒸馏了定义/起源两问，丢了"为什么需要 AAR"等内容），证据从本人笔记切换到 TC 25-20 外部来源；status 重置为 draft 重新走链。
- **遗留**：AAR 起源（1970s National Training Center）需独立权威来源（Army 历史站当前抓取受限）；旧 source `aar` 的 manifest/归档登记为 append-only 历史保留。

### 8.7 AAR 内容优化 + 两篇 wiki 标题修正（2026-09-03）

- **AAR 内容优化**：阅读重建后 wiki，补"正式/非正式 AAR""引导原则（开放式问题、AAR 非批评）"等核心内容，扩展常见误区，新增与 Retrospective / PDCA 差异对照；待验证项收口（起源 1970s 标注网络限制——Army 站/维基当前不可达，留待补权威来源）。
- **标题修正（两篇）**：`## 详细章节（working 原文，零删减）` 统一改为 `## 详细章节`（aar + compiler-vectorization）。
- **发布链重走**：标题/内容改动触发 content_sha256 变化 → 两篇均重跑 校验 + LLM 审计（aar 2/2、vectorization 18/18 均 supported）→ owner confirm → `release confirm`（evt-aar-hdr-20260903-f3da / evt-vec-hdr-20260903-f038）→ projection 重建（manifest 2ab6dc33…，含 aar + compiler-vectorization 两篇）→ 索引重建（item_count 2）→ doctor healthy、477 tests。
- **存量遗留（非本轮引入）**：`llvm-auto-vectorization` 等旧 wiki `public_publishable: False`、`how-to-read-a-book` `release_input_mismatch`，未进 projection——历史状态待后续处理。

### 8.8 how-to-read-a-book 定位纠正 + 原书 PDF 补源（2026-09-03）

- **定位纠正**：`reading-notes/how-to-read-a-book` 为个人读书笔记（含书籍模板字段/阅读日期，仅检视阅读层次），被登记为 source——同 aar 的登记失真。已迁至 `content/working/c-intermediate/reading-notes/`，front matter 改造并记录定位判定。
- **原书补源**：新增 `how-to-read-a-book-book` source（阿德勒、范多伦《如何阅读一本书》PDF，`--from-file` 本地导入，快照 `38c6f896…`，pypdf 提取），锚定四阅读层次总述（`evidence-501345402a89`）。
- **wiki 重建**：蒸馏核心八段 + 全文零删减 + `## 详细章节` 标题（与 aar/compiler-vectorization 对齐）；`four-levels` claim 切到原书 PDF 外部证据；检视阅读/四问/理解 vs 资讯为笔记转述（personal），不深入补内容（按 owner 指示"只读了一半，无需补充太多"）。
- **遗留**：分析阅读/主题阅读笔记待读完补；`how-to-read-a-book` 原 `release_input_mismatch` 待重建发布后解决。

### 8.9 how-to-read-a-book 发布闭环 + aar 格式修正（2026-09-03）

- **aar 详细章节格式修正**：`## 详细章节` 下标题层级统一为 `###` 起（原 working `#`/`##` 未降级）——与 compiler-vectorization 对齐；重走审计 pass + owner confirm + release（evt-aar-fmt-20260903-ed47）。
- **how-to-read-a-book 格式修正**：同样修正详细章节层级 + 修复引文换行缺失（`quote_mismatch`）；重走审计 pass（four-levels supported，原书 PDF `how-to-read-a-book-book` 支撑）+ owner confirm + release（evt-htrab-fmt2-20260903-8c04）。
- **working 移出**：`how-to-read-a-book`（个人笔记）从 working 删除（内容已完整入 wiki）；working 161 → 159。原 `release_input_mismatch` 已解决，现进 projection。
- **public projection**：manifest ddbf0ba2…，item_count 3（aar / how-to-read-a-book / compiler-vectorization），query 均可查；doctor healthy、477 tests。
- **遗留**：`llvm-auto-vectorization` 等 4 篇旧 wiki `public_publishable: False` 仍未进 projection（历史状态，待后续）。

### 8.10 4 篇存量 wiki review + CRLF 快照漂移修复 + 详细章节补全（2026-09-03）

- **CRLF 快照漂移修复（2 个孤儿 source）**：`cornell-memory-concepts`、`ddca-lecture10-microarchitecture` 的 archive 快照含 CRLF 行尾（pypdf 抽取 Windows 风格 PDF），快照以 CRLF 原始字节 sha 命名，而 doctor/validator 用 `read_text()`（通用换行归一 CRLF→LF）重算 → 漂移。修复：LF 归一化 + 重命名 blob（`1123ad49…`/`7a51de54…`）+ 更新 source front-matter `snapshot_sha256` + **就地重写 2 条未提交的 manifest record**（append-only 只约束已提交历史）。全量扫描 261 blob：仅这 2 个有 CR，同类型清零。两 source 无 wiki evidence 引用，未破坏锚点。
- **4 篇 wiki 详细章节修复/补全**：
  - `program-performance-analysis`、`llvm-auto-vectorization`：**补** `## 详细章节`（此前 working 内容完全未入 wiki，即"working 内容缺失"根因）——working 全文 +2 降级（`#`→`###`、`##`→`####`…）零删减捕获。
  - `cpu-pipeline-and-hazards`：详细章节补回 working 的 `分级缓存机制`/`虚拟内存管理`/`常见性能优化手段` 三节，并修正标题层级（`####`/`#####` 被拍平 → 恢复 +2 层级嵌套 `######`/`#######`）。
  - `isa-and-microarchitecture`：详细章节补回 working 的 `现代处理器基本架构`/`CPU核微架构`/`Cache子系统`/`基于处理器微架构的性能分析`/`基于处理器微架构的软件调优` 五节，修正 ISA 节标题层级，修正遗留错别字（井→并、架抅→架构、教据→数据、返度→速度、营换→替换、決→决、統→统、Wal→Wall 等）。
- **审查结论**：4 篇 wiki 的改写多数是证据驱动正确修正（五阶段非冯诺依曼通用、AArch64 SP/PC 非通用寄存器等）；引文截断 2 处（isa `isa-definition`/`isa-vs-micro`）待重锚，未在本轮处理。
- **验证**：4 篇 wiki 确定性校验全 `valid` + `evidence_state: supported`；doctor healthy、477 tests 全过。

### 8.11 4 篇 wiki 遗留项收口：引文重锚 + claim 升级 + 重审计（2026-09-03）

- **isa 引文重锚**：`isa-definition`/`isa-vs-micro` 两条截断引文重锚为完整句（接口句 + Hennessy-Patterson"程序可见属性"定义 + 微架构实现句 + 乱序语义句），并校准 claim（"规定程序可见的属性（概念结构与功能行为）"）。审计过程中又裁 4 条超出引文的 claim（same-isa 去掉"性能/内部组织不必相同"、risc-cisc 去掉"设计倾向而非硬性定义"（"更多内存操作"→"单条指令执行多个操作"）、arm-aarch64-registers 去掉"不应计作第 32/33 个"——这些限定/排除仍在正文/详细章节）。
- **program-performance claim 升级**：`little-law`→direct（Columbia `little-law-columbia`）、`profile-form`→direct（OSTI `osti-profiling-tracing`），`segmented-search` 保持 personal。因 F007 保守规则（任一 claim personal → 整页 personal），本页 `strength` 仍 `personal`（如实反映）。
- **cpu-pipeline 审计修正**：3 条 partially_supported 修正——`pipeline-throughput` 裁剪"多个事务同时进行"、`out-of-order-commit` 补 ROB 引文（tail allocation + 按序分配/回收）并去"维持精确状态"、`cache-platform-dependence` 补"cache 系统具体细节"引文。
- **审计结果**：4 篇全部 `pass`；`strength`：cpu-pipeline/isa `verified`、llvm `attested`、program-performance `personal`。`public_publishable: false`（待 owner confirm + release）。
- **待验证项收口**：cpu-pipeline/isa 全部 `[x]` 删除（结论并入正文），保留小节标注"已收口"；llvm 删除已验证项（运行时指针检查/epilogue 已在详细章节），保留 GCC 对照与英文引文两项；program-performance 删已升级项，保留 LUMI 补锚与等待排队两项。
- **文件名结论**：4 篇 wiki 文件名（object_id）不需要修改——文件名反映蒸馏身份（claim 范围），详细章节是 working 材料零删减捕获；改 object_id 会破坏引用链且无收益。

### 8.12 3 篇 wiki 发布闭环：cpu-pipeline / isa / llvm 进 public projection（2026-09-03）

- **发布链走通**：4 篇全部重审 `validation_state: pass` → owner confirm（cpu-pipeline 用 zhouzijian、isa/llvm 用 local-user）→ `release input` → `release confirm`（owner 在终端执行，actor zhouzijian01，三条：evt-cpu-pipeline-and-hazards-20260903-e144 / evt-isa-and-microarchitecture-20260903-a572 / evt-llvm-auto-vectorization-20260903-f37e）→ `public_publishable: true`。
- **release confirm 参数来源（实操教训）**：`release confirm` 需要 `--nonce`（一次性随机数，secrets.token_hex(8)）、`--event-id`（evt-<wiki>-<日期>-<hex> 约定）、`--leak-gate-report-sha256`（**= sha256_text(leak-gate.mjs --scope input-tree 输出原文)**；干净扫描三篇同值 `14f65263…`，与既有 htrab 事件一致——干净报告本就相同，勿多加换行）。
- **projection**：`item_count 6`（aar / compiler-vectorization / how-to-read-a-book + cpu-pipeline-and-hazards / isa-and-microarchitecture / llvm-auto-vectorization）；索引重建 item_count 6；query 可检索（fts5 环境降级走 fallback，不影响结果）。
- **program-performance-analysis 未发布**：`segmented-search` 仍 personal → 整页 strength=personal → `not_public_publishable`（projection skipped 列表如实记录）。重确认后仅作私有背书。
- **验证**：doctor 0 error、477 tests 全过、manifest `d0c401c0…`。

### 8.13 program-performance-analysis 重做：补源 + 内容优化 + 待验证项收口（2026-09-03）

- **重做动机（owner 指示）**：原 wiki"写的很乱"（详细章节混入元注释"外部来源对照"、证据映射误写 strength=attested 实为 personal、待验证项 2 条未收、segmented-search 无外部出处导致不可公开）。
- **补源（2 个新 source）**：`bisect-performance-regression`（UBC《On the Effectiveness of Bisection in Performance Regression Localization》PDF，支撑分段查找=二分定位）；`queueing-theory-gfg`（GeeksforGeeks 排队论，定义系统与收集数据的操作步骤）。
- **claim 从 3 条扩到 6 条，全部 direct**：`little-law`（Columbia）、`profile-form`（OSTI）、`segmented-search`（UBC，**从 personal 升级 direct**）、`trace-form`/`snapshot-form`（LUMI tracing/sampling）、`wait-queue`（GfG 排队步骤）。**strength 从 personal 升为 verified**，`public_publishable` 可转为 true。
- **内容优化**：蒸馏核心重写（核心概念补事件记录/快照/排队分析、证据映射改正、待验证项收口"无遗留"）；详细章节移除元注释"外部来源对照"（sourcing 信息并入证据映射）；working 文档同步移除该节。
- **验证**：确定性校验 valid + evidence_state supported；LLM 审计一次 pass（6/6）；doctor 0 error、477 tests 全过。
- **待 owner**：内容变更后需重新 confirm → release input/confirm 进 projection。

## 9. 修订记录

| 日期 | 变更 |
| --- | --- |
| 2026-09-02 | 章节编号重排为连续（1-9，原 1/2/9/6/7/3/4/5/8/10 乱序）；R8 从批次表移入 §1 判定规则区；执行记录（原 §8/§9/§10）按时间正序合并为 §8；新增本修订记录表。内容零丢失 |
| 2026-09-02 | 新增头部「生命周期声明」：本文是迁移过程决策记录而非规范，不参与 ruleset 抽取；迁移完成后随 docs/ 退役归档至 `ledger/`，不长期驻留规范目录 |
