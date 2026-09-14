# F008 Question / 大模型学习练习验收

- Feature：F008
- 状态：Implemented（部分）；Question Platform 运行面未闭合
- 设计：[Question 与大模型学习练习实现设计](../technical-design/question-and-practice.md)
- 平台设计：[F008 Question Platform：可插拔题目域与练习后端](../technical-design/f008-question-platform.md)
- Deep-ML 对齐：[F008 Deep-ML Inference Engineer 对齐与完整训练方案](../technical-design/f008-deep-ml-interview-mapping.md)
- ADR：[ADR-0016](../adr/0016-f008-learning-product-and-component-boundary.md)

## Question Platform 验收

### AC-F008-000 空题库

- Given：没有任何 Question Package；
- When：启动本地后端并请求 catalog/session；
- Then：服务正常启动，catalog 返回 `state: empty` 和 `next_action: import_question_package`；创建 session 返回结构化 `practice_catalog_empty`，不返回 404，不从 Wiki 临时生成题目。

### AC-F008-020 题目包导入 preview

- Given：合法、损坏、缺字段、未知题型、缺 license 和校验和错误的 `question-package/v1`；
- When：执行 import preview；
- Then：只返回新增、noop、冲突、阻断和字段丢失报告，不写入 Question、Registry 或 review state。

### AC-F008-021 题目包导入 apply

- Given：经过人工确认的 preview；
- When：执行 import apply；
- Then：题目、package manifest、source/license 元数据和 Registry 原子落盘；重复 apply 幂等；不可覆盖已有不同 hash 的题目。

### AC-F008-022 题目版本和冲突

- Given：相同 question ID 的相同版本、不同版本和相同版本不同 hash；
- When：导入题目包；
- Then：相同 hash 为 noop，不同 revision 新增版本，相同 revision 不同 hash 阻断并要求人工处理；不修改已有 attempt/review/card。

### AC-F008-023 题目生命周期

- Given：imported、enabled、disabled、retired 和有历史记录的题目；
- When：执行 enable/disable/retire/delete；
- Then：disabled/retired 不进入新 session；有历史的题目默认保留 tombstone 和 review 引用，不物理删除；Question ID 不复用。

### AC-F008-024 删除隔离

- Given：题目关联 Wiki、package、attempt 和 review；
- When：删除或撤回题目；
- Then：不删除 Wiki、Source、package 中其他题目或 review history；删除 package 前返回受影响题目清单。

### AC-F008-025 可插拔题型

- Given：内置或已注册的 Question Type Plugin；
- When：导入并练习题目；
- Then：插件只能声明的 schema/render/grade/feedback 能力范围内运行；未知插件阻断导入；插件不能读 vault、token 或其他题目答案。

## 基础兼容门禁

### AC-F008-001 题目 schema 和版本

- Given：合法与非法的 `question/v1`、`question/v2` 定义；
- When：创建或加载题目；
- Then：未知字段、题型专属字段、非法 ID、缺少分类或缺少答案规则被拒绝；v1 可读取，v2 按新契约校验；
- 当前证据：v1 基础测试已通过；v2 待实现。

### AC-F008-002 Claim/evidence 绑定

- Given：Wiki 验证报告和一个或多个 claim；
- When：创建题目或刷新题目；
- Then：owner、wiki_id、claim_id、content_sha256、evidence_sha256 全部匹配；任一缺失、stale 或 hash 漂移则 blocked/disabled；
- 题目保留原文件和 review log，不删除历史。

### AC-F008-003 Private/public 隔离

- Given：题目包含答案、解析、accepted answers 和 review state；
- When：生成 public projection、Pagefind 索引或静态 dist；
- Then：这些内容不会被读取、复制或索引；即使题目被放在错误 public 路径也会被字段级 leak gate 拒绝。

### AC-F008-004 FSRS adapter

- Given：无 review state、已有 Card、非法 rating、FSRS 依赖缺失或调度器异常；
- When：提交 review；
- Then：可用时保存 `fsrs-card/v1` 和 scheduler version；不可用时返回结构化 `provider_unavailable`，不得伪造 due；
- Card 可在备份恢复后继续调度。

### AC-F008-005 题目完整性

- Given：题干、选项、答案、解释或 rubric 被直接篡改；
- When：answer、review、backup restore；
- Then：`content_sha256` 校验失败并 fail-closed；API 不把完整性错误伪装成 `question_not_found`。

### AC-F008-006 禁用题目不可复习

- Given：题目 status 为 disabled，或 Wiki claim 已 stale；
- When：answer 或 review；
- Then：两条路径都返回 `question_disabled`，不追加答案记录，不改变 FSRS Card。

## 题型验收

### AC-F008-007 单选和多选

- Given：单选、多选题和选项解释；
- When：提交未知选项、重复选项、正确答案、错误答案和部分多选；
- Then：输入校验确定；评分可重放；多选反馈显示缺少项/多选项；错误选项可显示 misconception tag。

### AC-F008-008 填空

- Given：带 accepted、aliases、term/phrase/number/unit normalization 的 cloze；
- When：提交大小写、空格、Unicode、别名、非法近似和数字边界输入；
- Then：只按题目声明的规范化规则判分；不调用 LLM；结果包含规范化后的判分原因。

### AC-F008-009 面试表达骨架

- Given：包含核心要点和加分要点的 `keypoint_select`；
- When：选择完整、缺少核心或混入错误要点；
- Then：显示缺失的核心要点及 Wiki 引用；结果不被标记为“完整口头表达能力”。

### AC-F008-010 工程迁移

- Given：日志、配置或架构约束场景题；
- When：选择瓶颈、排查项、方案或副作用；
- Then：使用 deterministic choice grading，并保留 `diagnosis`/`tradeoff` 等 skill 标签。

## 练习流程验收

### AC-F008-011 Catalog 和分类

- Given：多个 domain/topic/concept/skill 的 enabled 题目；
- When：请求 catalog；
- Then：返回可练习分类、enabled/due/new/error 数量；不返回答案。

### AC-F008-012 六题短回合

- Given：到期题、新题和错题均存在；
- When：创建默认 session；
- Then：生成 6 题，默认包含 3 道到期/错题、2 道新题、1 道变式/面试/工程题；同一 concept 不连续重复超过两题。

### AC-F008-013 答题和复习分离

- Given：一个 session；
- When：先 answer，再显式 review；
- Then：answer 只写 attempt 和反馈；review 才调用 FSRS；任一阶段失败不会伪造另一阶段成功。

### AC-F008-014 错题重练

- Given：一次错误或看强提示后答对；
- When：选择 only_errors；
- Then：题目或同 concept 的变式可进入优先队列，并保留原始错误标签。

### AC-F008-015 领域筛选

- Given：`domain`、`topic`、`mode`、`skill`、`only_due`、`only_errors`；
- When：创建 session；
- Then：只返回满足过滤器的题目；空结果返回明确状态，不随机跨域补题。

### AC-F008-016 Concept 聚合

- Given：同一 concept 下多种题型的 attempts；
- When：请求 stats；
- Then：区分题目正确率、独立答对率、提示后答对率、lapse 次数和最近变式题结果；不能用单题正确率冒充 concept mastery。

### AC-F008-017 真实大模型垂直切片

- Given：至少 10 道绑定真实 Wiki/面经的题目，覆盖推理或 Transformer 一个领域；
- When：连续使用至少 5 个 session；
- Then：可以完成 Wiki、面试、工程三类中的至少两类练习，所有记录可从 private 数据重建。

## 互操作验收

### AC-F008-018 H5P 导出为副本

- Given：通过 v2 validator 的选择题/填空题；
- When：执行可选 H5P 导出；
- Then：输出明确标记为副本，列出字段丢失和 license 检查结果；不改变 canonical question，不写回 review state。

### AC-F008-019 Anki 导出为副本

- Given：通过 v2 validator 的题目和允许导出的字段；
- When：执行可选 Anki 单向导出；
- Then：导出不成为第二个调度 owner，不回写 MyKnowledge，不携带 private vault 禁止字段到 public target。

## 当前状态

已通过的基础证据主要覆盖 v1 schema、claim 绑定、选择题评分、FSRS adapter、private backup 和 leak gate。AC-F008-007 之后的 v2 题型、session、catalog、concept 聚合和真实垂直切片属于本轮设计后的待实现范围。
