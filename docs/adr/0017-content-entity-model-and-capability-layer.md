# ADR-0017：内容实体模型 = 共享 metadata + 统一动词 + 能力接口探测

- 状态：Proposed
- 日期：2026-09-14
- 相关规范：LAY、SRC、WIKI、EVD、QST、OPS
- 相关 Feature：F001、F002、F003、F004、F008、F011
- 相关 ADR：ADR-0006、ADR-0011、ADR-0014、ADR-0019、ADR-0020（本 ADR 一旦 Accepted，取代 ADR-0006 与 ADR-0014 的写入通道部分）
- 取代目标：本 ADR Accepted 时，ADR-0006（Preview/Apply 写协议）与 ADR-0014（三条写入通道）标记 Superseded

## 背景

当前 `tools/` 有 6 条平行写通道，各自 `OperationStore(root)` 并各自手写 apply 语义：`ingest/source_ingestor.py:270`、`evidence_anchor.py:35`、`ingest/video_frames.py:117`、`vault_transfer.py:22`、`write_operation.py:106`、`reposition.py`（后者还重写了一遍 commit-intent）。公共能力没有单一实现。

对现有内容做反向抽取（474 source / 208 wiki / 20 working / 360 question），四个实体的**字段集高度异构**：

| 实体 | 全量字段 | 可选字段 | 存储 | 身份 | hash |
| --- | --- | --- | --- | --- | --- |
| source | 13 | 5 | md + front matter（正文与 archive 快照逐字重复） | `id` | `snapshot_sha256` |
| wiki | 13 | 1 | md + front matter | `id` | 不落盘（运行时算） |
| working | 2（`domain`/`title`） | 0 | md + front matter | 无 | 无 |
| question | 12 | 5 | JSON | `id` | `content_sha256` |

同时四条事实说明"实体间的关系"与"存储的事实源"都从未建立：

1. `claim` 不是实体——只存在于 `content/wiki/*.md` front matter 的 `evidence[]` 数组里，无独立身份、无唯一性保证。实测 469 条 claim、467 条唯一、**2 条重复**（`definition`、`mali-gpu-ip`），命名规则不统一（仅 108/469 以 `-<数字>` 结尾）。
2. `question` 与 `wiki` 的绑定**从未建立**：`QUESTION_FIELDS`（`tools/question.py:28-45`）中 6 个字段（`claim_id`/`wiki_id`/`vault_id`/`rubric`/`confidentiality`/`company_tags`）在 360 个题目文件中**0 次出现**；`wiki_refs` 全量存在但 **0/360 非空**。题目实际是独立撰写（`source_refs` 311/360 指向外部 URL）。
3. `config/schemas.yaml`（967 行）的 `field_contracts` 与事实不符：对 source 声明的 8 个字段（`title`/`tags`/`aliases`/`related`/`captured_at`/`evidence_status`/`content_sha256`/`part_of`）实测 **0/474 存在**；对 wiki 声明的 4 个字段（`content_sha256`/`evidence_sha256`/`part_of`/`review_by`）实测 **0/208 存在**。
4. **存储存在双重事实源与三处身份登记**。`archive/` 是两层：`text/` 630 个规范化快照、`raw/` 216 个原始字节（含 15 个 PDF）。但 `content/sources/<domain>/<id>/<id>.md` 的正文与 `archive/text/<snapshot_sha256>.md` **逐字相同——474/474，零例外，重复文本 17.5 MB**。同一条身份信息存于三处：archive 文件名、`archive/manifest.jsonl`（773 条记录，**只登记 text、0 条登记 raw**，含 143 条历史重复）、source front matter（`snapshot_sha256` + `raw_ref: {path, sha256}`，后者 `path` 已含 sha）。raw 与 text 走**两套互不相通的登记渠道**，导致 manifest 与文件系统无法互证（216 个 raw 文件在 manifest 中 0 条记录）。另有 162 个 text 快照无任何 source 引用、474 个 source 只引用 468 个唯一快照（6 处 CAS 去重已生效，说明该机制本身是对的）。

## 候选方案

- **A：父子类继承**（`Source`/`Working`/`Wiki` 共一个基类，各自继承扩展）。能复用字段集，但**无法复用写动词**：source 的 create 是"采集 + 快照 + 归档"流水线，question 的 update 是 append-only 作答事件（`content/practice/reviews/*.jsonl`），父类的 create/update 对子类无意义。更严重的后果是晋升（working → source）会变成类型转换，而类型转换必然更换 id，会断掉实测中 **145 条** `working-*` 引用（wiki → source 引用共 424 条，`working-*` 占 145，为第一大来源）。Python 还会引入脆弱基类问题。
- **B：每个实体一套完整 CRUD 入口**（现状延续）。四条独立实现，公共逻辑复制四份；这是当前 6 条写通道的来源，也是"使用步骤多"的直接原因。
- **C：共享 metadata + 统一动词 + 按实体探测的能力接口**（Kubernetes API server 模型）。所有对象共享一份 identity/时间/机密级的 metadata；引擎提供统一动词；每个实体**声明它实现哪些能力**，未实现的能力不注册。Python 用 `typing.Protocol`（PEP 544 结构子类型）表达，不引入继承。

存储层另有独立取舍：

- **D：保留 source 正文副本**（现状）。收益是单文件自包含、`cat` 即可读全文、编辑器与 diff 友好。代价是 17.5 MB 重复、双重事实源、raw/text 两套登记渠道。
- **E：内容寻址存储（CAS）+ 引用，元数据与数据分离**（git object store / OCI 镜像层 / IPFS / Nix store 的共同模型；DVC 与 git-lfs 的"数据文件 + 指针文件"分离；数据湖 manifest 表的元数据/数据分离）。source 只留元数据与指针，正文按指针读 archive。

## 决策

采用 **方案 C（实体与能力）+ 方案 E（存储）**。

**实体收敛为 5 个**：`source`、`working`、`wiki`、`claim`、`question`。

**公共能力（引擎侧，按实体探测）**，以 `typing.Protocol` 表达，`@runtime_checkable` 供运行时探测：

| 实体 | List | Read | Delete | Update | Collect | Compose | Answer/Review |
| --- | --- | --- | --- | --- | --- | --- | --- |
| source | ✅ | ✅ | ✅ | ❌ | ✅ | — | — |
| working | ✅ | ✅ | ✅ | ✅ | — | ✅（晋升） | — |
| wiki | ✅ | ✅ | ✅ | ✅ | — | ✅ | — |
| claim | ✅ | ✅ | ❌ | ✅ | — | — | — |
| question | ✅ | ✅ | ✅ | ✅ | — | — | ✅ |

- **公共部分 = R/D/L + 校验编排 + 关系解析**（这部分是同构的，且实测是机械的）。
- **C（create）与 U（update）不做公共抽象**：source 的 create 是采集流水线（`Collector`），working 的 update 是自由写，question 的 update 含 append-only 作答事件（`Answerer`/`Reviewer`）。每个实体保留自己的领域函数。
- **source 保留为采集流水线，不给它套通用 CRUD**：它是系统中最健康的一层（实测 474 sources / 引用悬空 0），其"写"是采集、快照、归档、manifest 与锚定，字段只有 13+5 个。视频/音频导入属于该流水线。
- **`claim` 提升为一等对象**，满足四个条件：(i) 标识由工具生成（`<wiki_id>-c<NNN>`，手写 id 降级为 `alias`）；(ii) 全局唯一由 `validate` 校验；(iii) 有独立 schema 与校验；(iv) 可被外部引用（公开 `claim_id → (wiki_id, section, claim_sha256)` 的派生索引）。**存储上保持内联在 wiki front matter**——"一等"指可寻址，不指必须拆文件。
- **provenance 采用 W3C PROV-O 术语**，不自造字段：`prov:wasQuotedFrom`（wiki 引 source 引文）、`prov:wasRevisionOf`（source 重新采集）、`prov:wasDerivedFrom`（working 晋升、question 引用 claim）。三者语义不同，不可用一个 `derived_from` 合并——失效传播依赖它们区分（例如 source 被修订后，只有 `wasQuotedFrom` 能回答"哪些 wiki 引文需要重锚"）。

### 存储模型：内容存一层，身份登记一处

archive 的两层分离（`raw/` 原始字节含 PDF + `text/` 归一化文本）是合理的；问题在于第三层复制了 `text` 的内容。

- `content/sources/<domain>/<id>/<id>.md` = **front matter（元数据）+ 指针**，**不再含正文副本**。正文经 `snapshot_sha256` 读 `archive/text/<sha256>.md`。
- `archive/manifest.jsonl` 是**唯一登记处**：raw 与 text 两层都必须登记；废除 source `raw_ref` 这一平行渠道，并去掉 `raw_ref.sha256` 冗余（`path` 已含 sha）。
- 内容寻址命名保持不变（`<sha256>.md` / `<sha256>.<ext>`）：它同时承担定位与"不可变自证"。
- **直接收益**：消除 17.5 MB 重复，并消除**双重事实源**——现在 source 与 archive 内容相同，所以"谁是真源"从未被检验；一旦允许 source 原地改文本，两者必然漂移，而当前没有任何机制能发现。
- **取舍（需明确接受）**：`cat` 一个 source 文件将不再直接看到全文，只看到元数据与指针。这是"单一事实源"的价格。
- **去重的前置动作**：162 个无引用 text 快照与 216 个不在 manifest 的 raw 文件，必须先做 manifest ↔ 文件系统 ↔ source 三方对账再谈清理。**未引用 ≠ 无用**（raw 仍被 `raw_ref` 指向）。

### 命令面：区分人的接口与机器接口，人输入收敛到 7 条

参照 `gh`（少量名词 + 第二层动词）与 `kubectl`（少量动词 + 资源作参数）的共同做法：**构建/检查类命令不进人的输入面**。

```
人输入（7）
  source     采集 / 列举 / 查看 / 删除 / 重采集
  wiki       新建（含从 working 晋升）/ 列举 / 查看 / 删除 / 校验 / 审计 / 发布
  question   新建 / 列举 / 作答 / 复习 / 队列 / 质检
  query      检索 + 读取 + 反链
  build      生成投影 + 索引
  doctor     健康自检（含 vault 检查）
  backup     备份

不进人的输入面
  claim（内部对象，id 由工具生成）
  working（晋升由 wiki 新建的 --from-working 触发，见 ADR-0020）
  skill / mcp（agent 面）· matrix（pre-commit 钩子）
```

**配套修订（本 ADR 的直接后果）**：

- `config/schemas.yaml` 的 `field_contracts` 必须按实测重写，删除上述 12 个幽灵字段。
- `IDX-002` 仍描述"默认使用 QMD"，而 QMD 适配器已退役（`tools/indexing.py:411`），降级链实为 FTS5（simple/unicode61）→ LIKE；`cli.py:666` 与 `doctor.py:6` 的文案同样漂移，需一并修正。
- `CHN-001`/`LAY-003` 关于 `content/working/` 的"唯一硬约束是 `source_ref` 或 `legacy_path` 非空"与事实不符（实测 20/20 的 working 文件两者皆无）；`CHN-001` 另声称 working 派生文档"不得出现在任何 wiki 的 `evidence.targets`"，但实测有 145 个 `working-*` source 且被 wiki 引用 145 次——规范与其最大的一条数据通路冲突，需修订或对那批 source 重新定性。

## 后果

- 6 条平行写通道收敛为一个引擎 + 每个实体一个领域函数；公共能力只实现一遍。
- 命令面从 29 条收敛到 **7 条人输入**（外加不进人输入面的 claim/working 与 agent 面）；`read`/`backlinks` 并入 `query`，`projection`/`index` 合并为 `build`，`vault check` 并入 `doctor`。
- source 从"带正文的文档"变为"带元数据的指针文件"；读取正文需要经指针，工具侧必须提供统一的 `source show`（读元数据）与 `source read`（经指针读正文）两个语义。
- 晋升（working → source）保持"产生新对象 + 显式 provenance"，不换语义、不断引用。
- 实体间的桥（claim）建立后，question ↔ wiki 绑定才可能实现；在那之前 `QUESTION_FIELDS` 中 6 个死字段应删除或标记为未实现。
- 由于 `claim` 内联存储，469 条 claim 的迁移不需要改动 208 篇 wiki 的正文。
- 需要一次性的 claim id 回填（469 条）+ 2 条重复 id 的人工判定。
- 代价：`Protocol` 能力探测比直接继承更间接，需要运行时/静态两套校验（`@runtime_checkable` + mypy）；收益是实体之间零耦合、能力可单独测试。

## 重新评估条件

- 若某个实体的字段集增长到与其它实体高度重叠（例如 question 最终被并入 wiki 的派生视图），说明"5 实体"划分过细，应重新评估实体数。
- 若 `Protocol` 能力探测在实践中导致大量运行时分支（if-else 探测代替直接调用），说明抽象层级选错，应退回到显式的每实体函数而取消统一引擎。
- 若 question ↔ claim 绑定在建立后发现题目需要跨 wiki 复用同一条 claim，说明 claim 内联存储不再够用，需要评估外置为 `content/claims/` 独立文件（即本 ADR 已权衡并暂缓的路线 2）。
- 若"source 只留指针"导致日常阅读与检索体验明显下降（例如无法在编辑器里直接读全文），说明内容与元数据分离在这个单人使用场景下收益不足，应评估退回"保留正文副本 + 强制一致性校验"的折中。
