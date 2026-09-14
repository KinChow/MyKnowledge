# F008 Question 与大模型学习练习实现设计

- 状态：Implemented（部分）；现有 `question/v1` 基础实现已落地，学习产品运行面尚未完成
- 相关 Feature：F008
- 相关 ADR：ADR-0008、ADR-0012、ADR-0016
- 相关验收：[F008](../acceptance/F008-question-practice.md)
- Deep-ML 对齐：[F008 Deep-ML Inference Engineer 对齐与完整训练方案](./f008-deep-ml-interview-mapping.md)
- 平台设计：[F008 Question Platform：可插拔题目域与练习后端](./f008-question-platform.md)

## 1. 产品定义

F008 是面向大模型知识的短回合学习和复习系统。它消费已经通过 Wiki/evidence 门禁的知识，并把知识组织成可在几秒到几十秒内完成的练习。

三个学习目标：

| 目标 | 训练内容 | 主要题型 |
| --- | --- | --- |
| 核心知识深度理解 | 定义、机制、前提、边界、反例 | 单选、多选、填空、概念要点 |
| 面试表达 | 先说结论，再说机制、取舍和边界 | 要点选择、句子填空、表达骨架 |
| 工程迁移 | 从现象判断瓶颈、方案和副作用 | 日志/配置/架构场景选择、多选、排序 |

F008 不把“读过文章”“即时答对”直接等同于掌握。它记录题目层结果，并按 `concept_id` 聚合显示；实际复习调度仍以可独立回答的题目为最小执行单元。

Deep-ML 仅作为竞品和能力覆盖参考；题目导入、题目生命周期和后端承接平台见
[F008 Question Platform：可插拔题目域与练习后端](./f008-question-platform.md)。Deep-ML 的
能力分析、代码/系统设计/故障诊断边界和完整训练路径见
[F008 Deep-ML Inference Engineer 对齐与完整训练方案](./f008-deep-ml-interview-mapping.md)。

## 2. 成熟方案复用边界

### 2.1 采用 `py-fsrs` 的部分

复用：

- `Scheduler`；
- `Card` 创建、序列化和恢复；
- `Rating` 四级调度输入；
- 调度器版本和参数指纹。

MyKnowledge 自己负责：

- 将题目结果映射为 FSRS rating；
- 处理提示、跳过、部分得分、猜测和错误标签；
- 保存 append-only review log；
- 将多道题聚合为知识点统计。

FSRS 只回答“下一次何时安排”，不回答“这道题是否定义良好”“一个知识点是否能迁移”。

### 2.2 H5P standalone 的可选复用

借鉴：

- 单题即时反馈；
- Question Set 的短组卷；
- Multiple Choice 和 Fill in the Blanks 的交互状态；
- 正确答案、解释和错误反馈分离。

P2 之前不引入；P2 可评估本地 self-hosted `h5p-standalone`：

- 它可以读取项目内自托管的 H5P content folder；
- 不需要 Moodle、H5P.com 或远程 iframe；
- 可以作为现有题目 JSON 的播放副本；
- 结果仍必须由 MyKnowledge 接收并写入自己的 attempt/review log。

不复用：

- H5P 宿主；
- iframe 或外部 H5P 服务；
- H5P 内容包作为 canonical 题库；
- H5P 的结果事件作为本项目 review log。

原因：H5P standalone 解决的是播放和部分判分，不解决 private vault、claim hash、知识点聚合和本地 FSRS。直接采用它还会带来 content package/library 版本锁定、CSS/JS 体积、事件回传和题型字段映射成本。因此 P0 先使用 Astro 原生组件，P2 再用真实题目样本比较两条路径的维护成本。

### 2.3 借鉴 Anki 的部分

借鉴：

- 内容事实与复习状态分离；
- review log 追加写入；
- 卡片状态可序列化和恢复；
- 题目/卡片稳定 ID。

不引入：

- Anki collection 作为主数据源；
- Anki 客户端作为内嵌 UI；
- AnkiConnect 作为本地 API 依赖；
- 第二套调度 owner。

### 2.4 借鉴 Moodle 的部分

只借鉴题库的分类和组卷概念：

- 分类：domain/topic/concept/skill；
- 过滤：新题、到期题、错题、面试模式、工程模式；
- 组卷：按能力配额混合题型。

不引入 Moodle 服务、数据库、用户、课程和成绩模型。

### 2.5 不采用的成熟方案

| 方案 | 不采用原因 |
| --- | --- |
| 直接部署 Moodle | 对单人 local-first 过重，且需要维护第二套平台 |
| 直接嵌入 Anki | 不是 Astro/FastAPI 的嵌入式运行时，数据 owner 不清晰 |
| 直接嵌入 RemNote | 产品数据模型和 UI 不由本项目控制，不能满足 private/local 边界 |
| LLM 实时评分 | 延迟、可重复性、隐私和判分一致性不满足秒级热路径 |

## 3. 数据分层

```text
content/practice/questions/<question_id>.json
    题目事实：题干、选项、答案、解释、知识点和 evidence 绑定

content/practice/sets/<set_id>.json                 [可选]
    作者定义的题目组和领域配额，不保存用户进度

content/practice/reviews/<question_id>.jsonl
    append-only 作答和调度事件，属于 local/private vault

var/state/practice/session-<id>.json                [可重建/可过期]
    当前短回合的顺序、已答题目和视图状态

var/reports/practice-stats.json                     [可重建]
    题目和 concept 聚合统计
```

题目和复习数据都不得进入 public projection。前端 public build 可以包含一个不读取 practice 的静态入口，但只有本地模式和 capability token 可获取练习数据。

## 4. 目标题目契约：`question/v2`

当前代码继续兼容读取 `question/v1`。新的题目定义采用下面的概念模型；落地时由 schema validator 决定 JSON 字段的精确 required/optional 集合。

```json
{
  "schema_version": "question/v2",
  "id": "q-kv-cache-growth-01",
  "revision": 1,
  "type": "cloze",
  "vault_id": "private",
  "confidentiality": "private",
  "status": "enabled",
  "classification": {
    "domain": "llm",
    "topic": "inference",
    "concept_id": "kv-cache-memory",
    "skill": "mechanism",
    "mode": "wiki"
  },
  "knowledge_refs": [
    {
      "wiki_id": "kv-cache",
      "claim_ids": ["kv-cache-grows-with-sequence"],
      "content_sha256": "sha256:...",
      "evidence_sha256": "sha256:..."
    }
  ],
  "prompt": "Decode 阶段通常每次只生成一个新的 ____。",
  "payload": {
    "blanks": [
      {
        "id": "b1",
        "accepted": ["token"],
        "aliases": ["令牌"],
        "normalization": "term"
      }
    ]
  },
  "feedback": {
    "explanation": "Decode 每一步通常追加一个新 token，并复用已有 KV。",
    "misconception_tags": ["prefill_decode_confusion"]
  },
  "answer_key": {
    "kind": "exact"
  },
  "created_at": "2026-09-09T00:00:00Z",
  "content_sha256": "sha256:..."
}
```

### 4.1 必须字段

- `id`：稳定逻辑 ID；
- `revision`：题目事实版本；
- `type`：题型；
- `classification`：至少包含 `domain`、`topic`、`concept_id`、`skill`；
- `knowledge_refs`：至少一个 Wiki claim 或经过 private vault 门禁的面经/来源引用；
- `prompt` 和题型 payload；
- `feedback.explanation`；
- `answer_key`：只在 private practice 服务内部使用；
- `content_sha256`：不包含 status、统计和 review state。

### 4.2 知识引用规则

- `wiki` 题目必须绑定已验证的 Wiki claim；
- `interview` 题目必须绑定面经来源，并且其答案要点要能映射到一个或多个 Wiki claim，除非明确标为个人经验；
- `engineering` 题目必须绑定相关 Wiki claim 或已审计的配置/日志来源；
- 任一引用 hash 漂移，题目进入 `disabled`，保留原题和 review log；
- 允许多 claim 绑定，不能再限制为“一题一个 claim”；
- 题目答案不能成为 Source/Wiki 的事实来源。

## 5. 首期题型和判分

首期只实现能本地确定性评分的题型。每题评分目标是 5--30 秒，结果必须可重放。

### 5.1 `single_choice`

适合定义、概念辨析、工程取舍和日志诊断。

- 选项 ID 唯一；
- 正确答案恰好一个；
- 默认整题正确/错误；
- 每个错误选项可配置 `misconception_tag` 和解释；
- UI 可以先让用户思考再显示选项，但不能把隐藏选项当作评分依据。

### 5.2 `multi_choice`

适合检查必要条件和方案组合。

- 正确集合必须精确匹配；
- 可计算展示分数，但 FSRS 信号只使用 `correct/incorrect`、提示和反应时；
- 部分选中必须显示缺少项和多选项，不得只显示“错”。

### 5.3 `cloze`

适合术语、关键机制、公式变量和面试表达骨架。

规范化顺序固定为：

1. Unicode NFKC；
2. `casefold`；
3. 合并连续空白；
4. 去除题目声明允许忽略的首尾标点；
5. 只使用题目显式声明的别名、单位或数字容差。

默认不使用模糊编辑距离，不调用 LLM，不把任意近义词自动判为正确。每个 blank 可以声明 `term`、`phrase`、`number` 或 `unit` 规范化器。

### 5.4 `keypoint_select`

用于面试表达，不要求用户输入长文本：

```text
问题：解释 KV Cache 时，必须包含哪些要点？
作答：选择“保存历史 K/V”“避免重复计算”“随序列增长”“占用显存”
```

- 每个要点带 `keypoint_id`；
- 必选要点集合精确匹配；
- 可配置“核心要点”和“加分要点”；
- 反馈显示缺少的核心要点及对应 Wiki；
- 训练的是表达结构，不声称等同于完整口头表达。

### 5.5 `scenario_choice`

用于工程迁移，表现为单选或多选的结构化场景题：

- 输入：日志片段、配置差异、性能现象或架构约束；
- 输出：瓶颈、优先排查项、方案取舍或副作用；
- 仍使用确定性 option grading；
- 题目必须带 `skill: diagnosis`、`tradeoff` 或 `design`。

### 5.6 暂不作为自动评分题型

`short_answer` 保留兼容，但不属于首期核心闭环。人工评分和外部注入 scorer 可以继续使用；MyKnowledge 不在默认 API 内创建网络 LLM client。

## 6. 题目组和领域模型

### 6.1 分类维度

```text
domain       大模型基础 / 训练 / 推理 / 分布式 / 性能 / 面试
topic        Transformer / Attention / KV Cache / 并行 / 量化 ...
concept_id   可独立复习的最小知识点
skill        recall / discrimination / mechanism / diagnosis / tradeoff / interview
mode         wiki / interview / engineering
```

首批领域建议：

- 大模型基础；
- Transformer 与 Attention；
- 训练与优化；
- 推理与 KV Cache；
- 并行、通信与 PD；
- 量化、压缩与 serving；
- 性能分析与故障诊断；
- 面试综合。

### 6.2 `question_set`

题组不是调度对象，只是 session 生成模板：

```json
{
  "schema_version": "question-set/v1",
  "id": "set-llm-inference-daily",
  "filters": {"domain": "llm", "topic": "inference"},
  "quota": {
    "due": 3,
    "new": 2,
    "error_replay": 1,
    "mode": "mixed"
  },
  "max_questions": 6
}
```

没有题组文件时，API 根据请求过滤器生成等价的临时题组。session 不改变题目事实。

## 7. 作答、反馈和 review 事件

### 7.1 作答结果

```json
{
  "schema_version": "practice-attempt/v1",
  "attempt_id": "a-...",
  "question_id": "q-...",
  "question_revision": 1,
  "concept_id": "kv-cache-memory",
  "result": "correct",
  "score": 1.0,
  "confidence": "independent",
  "hint_used": false,
  "response_ms": 8200,
  "error_tags": [],
  "recorded_at": "2026-09-09T00:00:00Z"
}
```

`confidence` 取：

- `independent`：未看提示直接答对；
- `weak_hint`：看弱提示后答对；
- `strong_hint`：看强提示后答对；
- `guess`：答对但用户标记为猜测；
- `unknown`：未提供信号。

### 7.2 错因标签

首期固定枚举：

- `concept_confusion`
- `missing_condition`
- `direction_reversed`
- `term_confusion`
- `quantity_error`
- `scenario_misread`
- `guessing`

### 7.3 FSRS rating 映射

FSRS rating 不是由 `score` 单独决定：

| 作答信号 | 默认 rating |
| --- | --- |
| 独立答对，非猜测，反馈后无纠错 | Good |
| 独立答对但耗时很长，或答对后标记不确定 | Hard |
| 看弱提示后答对 | Hard |
| 看强提示后答对 | Again |
| 答错 | Again |
| Easy 由用户显式选择或后续策略产生，不由“答对”自动推断 |

首期每次提交 answer 后返回评分结果，不自动调用 FSRS；客户端或 session service 在用户确认“继续/完成”时提交 review。这样可以把“作答反馈”和“调度决策”分开测试。

### 7.4 review log

复用现有 `practice-review-record/v1` 兼容读取，目标增量记录：

- `attempt`；
- `rating`；
- `card_before`；
- `card_after`；
- `review_log`；
- `scheduler`、`scheduler_version`；
- `question_revision`；
- `parameters_sha256`。

review log 是唯一不可重建的学习事实；队列、统计和 concept 聚合都可以从它重建。

## 8. 队列和短回合 session

### 8.1 队列优先级

过滤后按以下顺序生成：

1. 当前 session 的错题重练；
2. relearning/Again；
3. 到期题；
4. 新题；
5. 非到期但长期未见的题。

同一 `concept_id` 在一个 session 内最多出现两题，避免连续重复造成“刚看过所以会”的假象。相邻题目尽量轮换 `type` 和 `skill`。

### 8.2 session 默认配额

默认 6 题：

```text
3 道到期/错题
2 道新题
1 道变式或面试/工程题
```

用户可以选择：

- 领域；
- topic；
- mode：wiki / interview / engineering；
- skill；
- only_due；
- only_errors；
- question_count：3、6、10。

### 8.3 session 状态

session 是 local runtime 状态，可以过期，可以从最后一个未完成题目恢复。它不改变题目 JSON，不保存正确答案到浏览器 localStorage。题目视图由 API 在 answer 前裁剪 `answer_key` 和解释。

## 9. API 契约

保留现有接口兼容：

```text
POST /api/practice/{question_id}/answer
POST /api/practice/{question_id}/review
```

新增：

```text
GET  /api/practice/catalog
POST /api/practice/sessions
GET  /api/practice/sessions/{session_id}
GET  /api/practice/sessions/{session_id}/next
POST /api/practice/sessions/{session_id}/questions/{question_id}/answer
POST /api/practice/sessions/{session_id}/questions/{question_id}/review
POST /api/practice/sessions/{session_id}/complete
GET  /api/practice/stats
```

### 9.1 `GET /catalog`

只返回可练习题目的元数据，不返回答案：

```json
{
  "schema_version": "practice-catalog/v1",
  "domains": ["llm"],
  "topics": ["inference", "attention"],
  "skills": ["mechanism", "interview", "diagnosis"],
  "counts": {"enabled": 18, "due": 6, "new": 4}
}
```

### 9.2 `POST /sessions`

请求：

```json
{
  "domain": "llm",
  "topic": "inference",
  "mode": "mixed",
  "skill": null,
  "only_due": false,
  "only_errors": false,
  "question_count": 6
}
```

返回 session 元数据和第一道题的安全视图。安全视图不能包含 `answer_key`、`correct_option_ids`、accepted answers 或隐藏解析。

### 9.3 answer/review 分离

`answer` 只做 deterministic grading 并写入 attempt；`review` 接收显式 rating 和可选 confidence/hint metadata，再调用 FSRS 并写入 card state。任何 disabled、hash mismatch 或跨 vault 请求都 fail-closed。

## 10. 前端适配

F008 前端只在本地完整模式运行：

- Astro 提供静态 shell；
- 浏览器通过 loopback FastAPI 获取 catalog/session/question view；
- 选择题、填空、keypoint 和 scenario 由 Astro 原生组件渲染；
- 不把答案、解释或 review state 编译进 public dist；
- capability token 只通过本地启动流程注入，不写入题目文件或 public bundle；
- 手机端优先支持单列、键盘/触控和“下一题”操作。

H5P standalone 不作为 P0 前端依赖。P2 若引入，必须 self-host 并 pin player/library 版本；它只播放经过 schema/evidence 校验的题目副本，结果由 MyKnowledge API 统一接收，不能成为 canonical question 或 review state owner。H5P 导出仍视为副本。

## 11. 题目生产流程

```text
Wiki/面经选择
  -> 外层 Agent 或人工起草 question/v2
  -> QuestionValidator 校验 schema
  -> Claim/evidence identity 和 hash 校验
  -> answer_key/feedback/分类校验
  -> preview
  -> 人工确认
  -> apply 到 private vault
  -> refresh / projection leak gate
```

外层 Agent 可以生成候选题目，但不能跳过 preview/apply，也不能把生成结果直接当成 verified fact。题目批量生成不在实时练习请求内完成。

## 12. 实施阶段

### P0：垂直切片

- 选定一个领域：`llm/inference`；
- 建立 10--20 道真实题目；
- 实现 single_choice、multi_choice、cloze；
- 实现 catalog、session、answer、review；
- 继续用现有 FSRS adapter；
- 修复 disabled review 和完整性错误误报问题；
- 验收：连续完成 6 题，反馈、记录和下一次 due 均可重放。

### P1：面试和工程迁移

- `keypoint_select`；
- `scenario_choice`；
- domain/topic/concept/skill 过滤；
- 错题重练；
- concept 聚合统计；
- 24 小时和 7 天延迟复习 fixture。

### P2：生产和维护

- `question/v1` 到 `question/v2` 兼容迁移；
- 多 claim 绑定；
- Preview/Apply 题目写入；
- question revision 和失效迁移；
- 备份恢复完整回归；
- local-only Astro 练习页面。

### P3：可选互操作

- H5P 单向导出；
- Anki 单向导出；
- 不回灌、不产生第二个调度 owner；
- 每个导出格式单独做 license、字段丢失和隐私审计。

## 13. 完成定义

F008 只有满足以下条件才可从 Implemented 推进 Accepted：

- 至少一个大模型领域有真实题目，而非 fixture-only；
- 选择题和填空题能在本地 UI 完整完成；
- answer/review 分离且 review log 可重建；
- 题目按 domain/topic/skill 可筛选；
- 面试表达和工程迁移至少各有一种题型；
- 题目、答案、解析、review state 不进入 public projection；
- Wiki/claim hash 漂移会禁用题目；
- FSRS 缺失、题目损坏、权限不足均返回结构化失败；
- 运行完整 pytest、doctor、frontend validate 和浏览器本地模式验收。
