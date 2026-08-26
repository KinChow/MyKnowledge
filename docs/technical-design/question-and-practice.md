# F008 Question 与面试练习实现设计

- 状态：Implemented（2026-08-27；schema、绑定、评分和 FSRS adapter 基础能力）
- 相关 Feature：F008
- 相关 ADR：ADR-0008
- 相关验收：[F008](../acceptance/F008-question-practice.md)

## 成熟方案调查

- FSRS 官方 `py-fsrs`（MIT，https://github.com/open-spaced-repetition/free-spaced-repetition-scheduler）：本地 Scheduler/Card/Rating 模型；MyKnowledge 通过 adapter 调用，依赖缺失时返回 `unavailable`。
- Anki/AnkiDroid（https://github.com/ankitects/anki、https://github.com/ankidroid/Anki-Android）：借鉴 note/card/review state 分离和本地状态边界，不复用其 deck 数据格式。
- 固定间隔/Leitner：作为调度替代基线，仅用于方案对照，本轮不自研替代 FSRS。

## 契约与边界

Question 使用 `question/v1`，题目由已验证 Wiki claim 派生，保存 claim 的 Wiki content/evidence hash。题目、答案、解析、评分和 review state 位于 `practice/questions/`，不进入 public projection/index/Pagefind。Wiki hash 或 evidence 状态变化后，题目必须由上层重校验并标记 disabled。

`QuestionStore` 负责 schema/绑定/评分和状态持久化；FSRS 只负责 review scheduling，不拥有事实、证据或隐私规则。

## 当前限制

基础实现尚未接入完整 Preview/Apply operation、FastAPI 练习 API、FSRS 已安装运行时、批量失效迁移和 backup/restore 演练；这些属于后续 F008 验收增量。
