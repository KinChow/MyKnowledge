# F008 Deep-ML Inference Engineer 对齐与完整训练方案

- 状态：Designed
- 日期：2026-09-11
- 相关 Feature：F008
- 相关设计：[Question 与大模型学习练习实现设计](./question-and-practice.md)
- 参考页面：<https://www.deep-ml.com/interview-prep/inference-engineer-general?role=inference-engineer>
- 参考集合：<https://www.deep-ml.com/collections/Inference%20Engineering>

## 1. 调研结论

Deep-ML 对 Inference Engineer（General）的描述不是单一知识问答，而是一个能力组合：

- Prefill/Decode 的性能经济学；
- KV-cache 数学；
- Attention kernel；
- Quantization 数值；
- Parallelism；
- 从零实现 attention、KV cache、softmax、sampling、scheduler；
- 端到端 serving system design；
- live debugging。

Deep-ML 的 Inference Engineering collection 当前列出 111 个练习，覆盖模型评估、微调/蒸馏、延迟吞吐、线性层和 softmax、speculative decoding、prefix cache/KV memory budget、tensor/expert parallelism、PD 分离、VLM、embedding、ASR 和 TTS 等方向。

因此 F008 的产品目标必须分层：

```text
短题即时反馈       覆盖 recall / discrimination / calculation
代码练习            覆盖 implementation / correctness / complexity
系统设计练习        覆盖 architecture / tradeoff / scale
故障诊断练习        覆盖 diagnosis / evidence / prioritization
口头模拟             覆盖 communication / interview expression
```

选择题和填空题只能覆盖第一层和第二层的一部分，不能单独证明“已经具备 inference engineer 面试能力”。

## 2. 与用户需求的对应关系

| 用户需求 | 方案支持 | 不能完全支持的部分 | 补偿机制 |
| --- | --- | --- | --- |
| 学习和复习大模型知识 | Wiki claim、concept、题目变式、FSRS | 单纯复习不能保证工程迁移 | scenario/code/design 题 |
| 配合 Wiki 和面经 | Wiki 是事实来源，面经是场景/题目来源 | 面经可能是非正式、过时或公司特定 | source provenance、confidence、review_by |
| 核心知识深度理解 | mechanism、boundary、counterexample 题 | 选择题容易变成识别 | 先回忆、再选项；延迟变式题 |
| 面试表达 | keypoint_select、cloze、短答草稿、计时口述 | 几秒自动评分不能可靠评估完整口头答案 | 结构化要点评分 + 可选人工/外部评分 |
| 工程迁移 | 日志、配置、算力/带宽、架构取舍场景题 | 真实系统复杂度远超题目 | 代码实验、system design、debug session |
| 几秒自动评分 | choice、cloze、数值、公式结构可确定性评分 | 开放式设计、任意代码质量、自然语言表达 | 分层练习，不强行统一评分器 |
| 领域/分类 | domain/topic/concept/skill/mode | 多标签会造成筛选语义复杂 | 约束主分类 + 可选标签，API 明确交集/并集 |

结论：**可以满足“快速学习和复习入口”的需求，也可以覆盖面试能力训练的主干；不能仅靠几秒自动评分替代完整 mock interview。** 需要把“自动评分练习”和“深度评审练习”明确分成两条产品路径。

## 3. 能力树设计

### 3.1 一级领域

```text
llm-foundation
llm-architecture
llm-training
llm-inference
llm-serving
distributed-computing
performance-debugging
interview
```

### 3.2 Inference Engineer 重点主题

```text
model-evaluation
latency-throughput
transformer-attention
softmax-sampling
kv-cache
prefix-cache
speculative-decoding
quantization
tensor-parallelism
expert-parallelism
prefill-decode-disaggregation
scheduling
kernel-optimization
memory-bandwidth
serving-system-design
observability-debugging
```

### 3.3 技能轴

```text
recall             术语、定义、组件职责
derive             公式、维度、数量级推导
calculate          给定参数计算结果
implement          从零实现并通过测试
discriminate       区分相近概念和瓶颈
mechanism          解释因果机制
diagnose           从症状和日志定位问题
tradeoff           解释方案的收益、成本和边界
design             端到端系统设计
communicate        面试中的结构化表达
```

一个题目至少有一个 `concept_id` 和一个 `skill`；代码题和设计题可以有多个 skill，但不能没有主 skill。

## 4. 题型分层

### L0：快速记忆题

题型：`single_choice`、`multi_choice`、`cloze`、`keypoint_select`。

目标：5--30 秒，确定性评分。

适合：

- Prefill 与 Decode 的区别；
- KV cache 保存什么；
- TTFT、ITL、TPS 的定义；
- quantization 的基本数值关系；
- 哪些因素影响显存、带宽和延迟；
- 面试表达必须包含的关键要点。

不适合：

- 让用户完整解释一个系统；
- 判断自然语言表达是否清晰；
- 判断代码是否工程可用。

### L1：计算与推导题

题型：`numeric_answer`、`formula_select`、`tensor_shape`、`unit_convert`。

目标：30--120 秒；仍然可以本地自动评分。

示例：

- 根据 layers、KV heads、head_dim、sequence length、dtype 计算 KV cache 大小；
- 根据 timestamp stream 计算 TTFT、平均 ITL、P95 ITL 和 TPS；
- 根据 tensor parallel degree 判断通信量和张量形状；
- 根据图像分辨率和 patch size 计算视觉 token 数。

评分：

- 有理数/浮点数使用题目声明的绝对或相对误差；
- 单位必须匹配或经过声明的单位转换；
- 中间步骤可选，不将字符串解释作为自动评分依据；
- 结果记录 `numeric_tolerance` 和 `unit_normalization`。

### L2：实现题

题型：`code_task`。

目标：10--60 分钟；不属于“几秒自动评分”，但属于 inference engineer 必需能力。

示例：

- 实现 stable softmax；
- 实现 causal attention；
- 实现 KV cache append/read；
- 实现 top-k/top-p sampling；
- 实现 speculative decoding verification；
- 实现 continuous batching scheduler；
- 实现 prefix-cache hit-rate calculator。

成熟方案复用：

- 复用 pytest 作为测试执行器；
- 复用 NumPy/PyTorch 作为题目运行环境；
- 复用现有 CI/fixture 机制；
- 不引入在线代码执行平台作为核心服务。

安全边界：

- 代码题必须在隔离 subprocess/container 中执行；
- 设置 CPU、内存、时间、输出和文件系统限制；
- 默认禁止网络；
- 用户代码不能访问 vault、token 或题库答案；
- 代码题结果只保存测试摘要和 hash，不保存任意运行产物到 public。

第一版可以不实现在线代码执行，只保存题目定义和本地命令入口；否则 L2 会显著扩大安全和运行时复杂度。

### L3：系统设计题

题型：`design_prompt` + `design_checklist`。

目标：15--45 分钟；不做默认自动判分。

示例：

- 设计高并发 LLM serving；
- 设计 Prefill/Decode disaggregation；
- 设计 prefix cache；
- 设计量化推理服务；
- 设计多副本请求路由和故障转移。

自动化部分：

- 检查是否覆盖必需组件；
- 检查是否回答容量、延迟、可靠性和观测；
- 检查是否指出至少一个 trade-off；
- 计时和阶段提示；
- 生成答题 checklist。

不自动声称：

- 设计一定正确；
- 架构可以上线；
- 用户已经具备系统设计能力。

### L4：故障诊断题

题型：`diagnosis_case`。

输入：

- 指标；
- 日志；
- 配置；
- 硬件/网络拓扑；
- 已知约束。

输出：

- 最可能瓶颈；
- 排查顺序；
- 需要补采集的指标；
- 修复方案；
- 副作用或回滚条件。

自动评分采用分层要点：

```text
核心诊断正确      0.6
关键证据命中      0.2
排查顺序合理      0.1
副作用/边界条件   0.1
```

首期可将它实现成多选和 keypoint_select；完整自由诊断留给 L3。

## 5. 题目数据模型增量

在 `question/v2` 的 `classification` 之外增加能力字段：

```json
{
  "classification": {
    "domain": "llm-inference",
    "topic": "kv-cache",
    "concept_id": "kv-cache-memory-budget",
    "skill": "calculate",
    "mode": "interview",
    "level": "L1"
  },
  "difficulty": {
    "author": 3,
    "estimated_seconds": 45
  },
  "assessment": {
    "transfer_target": "engineering",
    "requires_calculation": true,
    "delayed_variant_group": "kv-cache-budget-v1"
  }
}
```

### 5.1 不把难度当作调度真相

`difficulty.author` 只用于初始筛选；实际表现来自 attempts/reviews：

- response time；
- independent correctness；
- hint usage；
- error tags；
- delayed variant result；
- code test result；
- design checklist coverage。

### 5.2 concept 与 variant group

`concept_id` 表示知识点；`variant_group` 表示同一知识点的不同问法。

例如：

```text
concept_id: kv-cache-memory-budget
variant_group:
  - formula_recall
  - numeric_calculation
  - configuration_diagnosis
  - serving_tradeoff
```

调度不能在短时间连续展示同一 variant group，否则会把短期记忆误判成长期掌握。

## 6. 练习模式

### 6.1 Daily Review

默认 6 题：

```text
2 道 due/relearning
1 道旧知识变式
1 道新概念
1 道计算或诊断
1 道面试表达要点
```

目标：5--10 分钟，维持覆盖和复习节奏。

### 6.2 Concept Deep Dive

围绕一个 `concept_id` 生成：

```text
定义 -> 机制 -> 边界 -> 计算 -> 工程场景
```

目标：15--25 分钟。完成后才显示 concept 的分维度结果。

### 6.3 Interview Sprint

按角色和主题组卷，例如 `inference-engineer-general`：

```text
2 道概念快问
1 道公式/数量级
1 道工程诊断
1 道系统设计 checklist
1 道代码题入口
```

支持计时、无提示模式和“结束后统一反馈”模式。

### 6.4 Error Replay

只复习：

- Again/relearning；
- `concept_confusion`；
- `missing_condition`；
- `quantity_error`；
- 延迟变式失败；
- 设计 checklist 缺核心项。

不能只按“答错次数”排序，否则重复点击和猜测会污染队列。

## 7. 调度设计

### 7.1 调度层次

```text
题目 Card：由 py-fsrs 调度下一次出现
concept 聚合：由 attempts/reviews/variant 统计生成
session 组卷：按用户筛选和能力配额生成
interview track：按角色能力覆盖率生成缺口
```

只允许题目 Card 有一个 FSRS owner。concept 和 track 不各自再跑一个 FSRS。

### 7.2 不同 level 的调度策略

| Level | 调度 |
| --- | --- |
| L0 | FSRS 题目卡；同 concept 做变式轮换 |
| L1 | FSRS 题目卡；保留单位/误差和耗时 |
| L2 | 不默认自动 FSRS；按 code task 完成/失败和人工标记安排 |
| L3 | 按 mock session 和 checklist 缺口安排，不把一次设计评分压成四级 rating |
| L4 | 可对核心子题使用 FSRS；完整 case 作为周期性模拟 |

这样能复用 FSRS，同时避免把系统设计能力伪装成普通闪卡记忆。

## 8. 评分和反馈

### 8.1 自动评分优先级

```text
choice exact set
cloze normalized exact
numeric tolerance
tensor shape exact
keypoint weighted set
code test cases
design checklist coverage
external/manual review
```

越靠后，评分越不适合放入几秒热路径。

### 8.2 反馈必须回答三个问题

每次答错至少显示：

1. 正确机制或计算结果；
2. 用户答案对应的误区；
3. 回到哪个 Wiki claim 或面经场景继续学习。

只显示“正确答案是 B”不满足深度理解目标。

### 8.3 评分结果不能直接等于掌握

应分别显示：

- immediate correctness；
- independent correctness；
- delayed variant correctness；
- transfer correctness；
- interview checklist coverage。

最终的 `concept_mastery` 只能是报告字段，不作为事实或 FSRS 输入的唯一来源。

## 9. API 方案

在现有题目 API 之外，目标接口分为四组：

```text
GET  /api/practice/catalog
POST /api/practice/sessions
GET  /api/practice/sessions/{id}/next
POST /api/practice/sessions/{id}/answer

GET  /api/practice/concepts/{concept_id}
GET  /api/practice/stats
GET  /api/practice/tracks/inference-engineer-general

POST /api/practice/code-runs
POST /api/practice/design-sessions
POST /api/practice/design-sessions/{id}/submit

POST /api/practice/{question_id}/review
```

P0 只实现第一组和最后一个 review 接口。第二组在 P1 实现，第三组分别是 P2/P3，避免一开始把代码沙箱和开放式评估引入主链路。

## 10. 与 Deep-ML 内容的映射

| Deep-ML 方向 | MyKnowledge 题型 | 自动评分 | 需要的 Wiki/来源 |
| --- | --- | --- | --- |
| Model evaluation | numeric、formula、choice | 高 | 评估 Wiki、公式 claim |
| Latency/throughput | numeric、scenario | 高 | TTFT/ITL/TPS claim |
| Softmax/sampling | code、numeric、cloze | 中/高 | 算法 Wiki + 代码 fixture |
| KV cache | cloze、numeric、diagnosis | 高 | KV cache Wiki |
| Speculative decoding | choice、numeric、code | 中 | 机制和接受率 claim |
| Quantization | numeric、choice、scenario | 高 | 数值误差和部署取舍 Wiki |
| TP/EP | numeric、scenario、design | 中 | 通信/并行 Wiki |
| PD disaggregation | diagnosis、scenario、design | 中 | PD、RDMA、XCCL Wiki |
| Scheduling | code、scenario、design | 中 | serving scheduler Wiki |
| Production serving | design、diagnosis | 低/人工 | 面经、架构决策、工程记录 |

这张表说明：F008 P0 应先覆盖“短题可自动评分的高频知识”；代码、系统设计和复杂诊断必须作为后续能力，不应在 schema 中伪装成普通 choice。

## 11. Trade-off 评审

### 11.1 自研 Astro 题型 vs H5P runtime

选择 Astro 原生：

- 优点：数据 owner 单一；无跨域；直接复用 FastAPI capability；完全控制 question/v2 和 feedback；
- 缺点：需要自己实现 UI、可访问性、移动端和题型测试；
- 结论：符合 local-first；H5P 只作为题型设计参考和未来导出格式。

### 11.2 FSRS 题目级 vs concept 级

选择题目级 FSRS、concept 级聚合：

- 优点：符合 `py-fsrs` 输入模型，迁移简单，review log 可重放；
- 缺点：多题可能重复调度，一个 concept 的掌握不等于任一题掌握；
- 缓解：variant group 轮换、concept 报告分维度、延迟变式测试；
- 结论：当前阶段比自研 concept scheduler 更可验证。

### 11.3 确定性评分 vs LLM 评分

选择确定性评分为默认：

- 优点：快、可复现、离线、隐私边界清晰；
- 缺点：无法可靠评估自然语言表达和开放系统设计；
- 缓解：keypoint、numeric、scenario、checklist 结构化；开放回答走人工/外部 scorer；
- 结论：满足“几秒自动评分”，但不能承诺完整口语能力自动评估。

### 11.4 JSON 文件 vs SQLite

首期保留 JSON/JSONL：

- 优点：符合现有 content/ledger/vault、Git、hash 和 backup 约束；
- 缺点：队列查询、并发写入、统计聚合逐渐变重；
- 迁移条件：题目超过约 1,000、review log 超过约 100,000 条，或需要多设备并发同步时评估 SQLite；
- 结论：当前题库为空且单人 local-first，先不引入数据库迁移成本。

### 11.5 先做 111 题映射 vs 先做 10--20 题垂直切片

选择先做 10--20 题：

- 111 个练习类别适合作为覆盖地图，不适合作为首期交付量；
- 先验证题目是否真的能驱动 Wiki 阅读、复习和工程迁移；
- 通过真实 session 发现题目模型和 feedback 缺陷，再扩展覆盖。

## 12. 满足性结论

### 能满足

- 按领域、主题和面试角色选择练习；
- 几秒内完成的选择、填空、计算和关键点题；
- Wiki 与面经联合驱动；
- 通过 FSRS 进行题目级间隔复习；
- 记录错误类型、提示、耗时和变式表现；
- 将推理知识扩展到 KV cache、量化、并行、PD、调度、性能和 serving。

### 不能单独满足

- 完整自由口头表达的可靠自动评分；
- 真实代码工程质量的几秒判定；
- 端到端系统设计能力的完全客观评分；
- 没有真实题目和持续使用数据时的“掌握度证明”。

### 产品承诺

F008 应对外承诺：

> 帮助用户高频、可追踪地复习大模型和推理工程知识，并通过结构化题目、计算、诊断、代码和系统设计练习逐步准备面试。

不应承诺：

> 自动判断用户已经准备好通过 Inference Engineer 面试。

## 13. 建议交付顺序

### P0：短题垂直切片

- 领域：`llm-inference`；
- 主题：KV cache、Prefill/Decode、TTFT/ITL/TPS；
- 题目：10--20 道；
- 题型：choice、cloze、numeric、keypoint_select；
- API：catalog、session、answer、review；
- UI：移动端 6 题短回合；
- 验收：连续使用 5 个 session，记录可重放。

### P1：面试和工程迁移

- scenario diagnosis；
- variant group；
- concept stats；
- error replay；
- inference-engineer-general track；
- 覆盖 quantization、speculative decoding、parallelism。

### P2：代码训练

- softmax、attention、KV cache、sampling；
- 本地 pytest runner；
- 资源限制和结果摘要；
- 不保存任意用户代码到 public。

### P3：设计和模拟面试

- design_prompt；
- checklist；
- 计时；
- 人工/外部评分；
- 面试角色覆盖率报告。

### P4：互操作

- H5P 单向导出；
- Anki 单向导出；
- 导出副本不回灌、不成为第二个调度 owner。
