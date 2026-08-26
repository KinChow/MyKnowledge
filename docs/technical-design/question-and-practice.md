# F008 Question 与面试练习实现设计

- 状态：Implemented（2026-08-27；schema、绑定、评分和 FSRS adapter 基础能力）
- 相关 Feature：F008
- 相关 ADR：ADR-0008
- 相关验收：[F008](../acceptance/F008-question-practice.md)

## 成熟方案调查

- FSRS 官方 `py-fsrs` Python 包 `fsrs` 6.3.2（MIT，<https://github.com/open-spaced-repetition/free-spaced-repetition-scheduler>）：本地 Scheduler/Card/Rating 模型；MyKnowledge 通过 adapter 调用并持久化 `Card.to_dict()`，依赖缺失时仍返回 `unavailable`。
- Anki/AnkiDroid（https://github.com/ankitects/anki、https://github.com/ankidroid/Anki-Android）：借鉴 note/card/review state 分离和本地状态边界，不复用其 deck 数据格式。
- 固定间隔/Leitner：作为调度替代基线，仅用于方案对照，本轮不自研替代 FSRS。

本轮增量调查（2026-08-30）：继续采用 `py-fsrs` 的 Scheduler/Card/Rating adapter，不复制其调度算法；Anki 的 card/review state 分离作为状态持久化参考。练习 API 复用本地 FastAPI capability boundary；替代方案是把答案写入 canonical Wiki，因会污染事实链和 public projection，明确排除。

## 契约与边界

Question 使用 `question/v1`，题目由已验证 Wiki claim 派生，保存 claim 的 Wiki content/evidence hash。题目、答案、解析、评分和 review state 位于 `practice/questions/`，不进入 public projection/index/Pagefind。Wiki hash 或 evidence 状态变化后，题目必须由上层重校验并标记 disabled。

`QuestionStore` 负责 schema/绑定/评分和状态持久化；`refresh_status()` 在 Wiki content/evidence hash 或 evidence 状态变化时将题目设为 `disabled`，避免继续复习陈旧事实。作答结果以 append-only `practice/reviews/<question_id>.jsonl` 本地记录并 fsync；FSRS 只负责 review scheduling，不拥有事实、证据或隐私规则。`/api/practice/{question_id}/answer|review` 仅允许 local/private capability 调用，不能绕过 validator 或公开 practice 数据。

## 当前限制

基础实现尚未接入完整 Preview/Apply operation、批量失效迁移和 practice backup/restore 演练；FastAPI 练习 API 与 FSRS 6.3.2 运行时已接入并有回归测试。
