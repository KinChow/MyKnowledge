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

本轮题目持久化完整性调查（2026-08-30）：Anki collection 的备份/恢复流程将 note 内容与 card/review 状态分离，并在状态迁移前要求 collection integrity/backup（<https://docs.ankiweb.net/deck-options.html>，Anki GPL-3.0）；FSRS 官方实现同样把 Card state 作为可序列化调度状态，而非题目事实（MIT，<https://github.com/open-spaced-repetition/free-spaced-repetition-scheduler>）。替代方案是仅依赖 JSON 可解析或文件名稳定 ID，无法发现题干、选项、答案、解析和 rubric 被篡改。采用 `QuestionStore.load()` 对 `content_sha256` 做 fail-closed 校验：事实字段必须匹配 hash，`status`/`review_state` 作为可变生命周期状态保留；兼容旧 hash 计算格式，但不接受未知 schema、ID 错配或内容 hash 漂移。离线校验不访问网络、不记录答案，升级需重跑题目 schema、FSRS 和备份回归。

本轮简答评分调查（2026-08-27）：`py-fsrs` 6.3.2（MIT，<https://github.com/open-spaced-repetition/free-spaced-repetition-scheduler>）不负责答案评分；Anki 24.x / AnkiDroid 2.19（GPL-3.0，<https://github.com/ankitects/anki>、<https://github.com/ankidroid/Anki-Android>）采用 note/card/review 分离，本轮仅借鉴状态边界。替代基线为无依赖的固定间隔/Leitner rubric：可离线复现但不能理解开放表达，因此采用 deterministic rubric 作为基线、人工复核为默认，LLM 仅通过注入 provider 可选启用。LLM client 参考 OpenAI Python 1.x（Apache-2.0，<https://github.com/openai/openai-python>）的可注入边界，但 QuestionStore 不创建网络 client；缺失或离线时返回 `provider_unavailable`，升级只影响 adapter，不改变 `question/v1` 或 practice 格式。

本轮 practice 备份调查（2026-08-27）：Git bundle/checkout 的对象哈希与显式空目录恢复（GPL-2.0，<https://git-scm.com/docs/git-bundle>）适合离线、可审计的 owner checkout；SQLite Online Backup API（Public Domain，<https://sqlite.org/backup.html>）适合一致性快照。替代方案 rsync（GPL-3.0，<https://github.com/WayneD/rsync>）只复制文件，无法表达 `(vault_id, object_id)` owner 或 manifest 自校验，因此不作为恢复判据。MyKnowledge 复用 manifest 的相对路径/sha256/空 target/失败清理边界，并把 practice/questions 与 practice/reviews 纳入所属 vault；不复制 Git/SQLite 内部格式，也不把外部 target、凭据或 token 写入记录。

本轮批量失效调查（2026-08-27）：Anki/AnkiDroid 的 note/card 引用在内容变更后重新调度或暂停，FSRS 只处理 review state；替代方案是删除旧题目，会破坏 review history 和审计可追溯性，因此采用逐题 `disabled` 保留文件与记录。`refresh_all()` 按 `wiki_id` 报告重放所有本地题目，缺失报告按不可信处理并禁用，不把 stale claim 当成新事实。

本轮练习 API 调查（2026-08-27）：FastAPI/Pydantic 的枚举 query 参数（MIT）用于把评分模式纳入 OpenAPI 契约；替代方案是让请求体携带任意 `provider`/URL，会扩大网络和能力边界，明确排除。API 只允许 `manual|deterministic|llm`，LLM provider 由进程外注入，缺失时返回 `provider_unavailable`。

## 契约与边界

Question 使用 `question/v1`，题目由已验证 Wiki claim 派生，保存 claim 的 Wiki content/evidence hash。题目、答案、解析、评分和 review state 位于 `practice/questions/`，不进入 public projection/index/Pagefind。Wiki hash 或 evidence 状态变化后，题目必须由上层重校验并标记 disabled。

本轮增量（2026-08-27）：创建题目除验证 Wiki/evidence 状态外，还必须核对验证报告中的 owner `object_id` 与 `spec.wiki_id`，并确认 `spec.claim_id` 存在于该报告的 evidence claim 集合；Skill/API 不得仅凭作者提交的字符串建立绑定。
刷新题目状态时同样重放 owner/Claim identity，再比较 content/evidence hash；不能用错误 Wiki 报告的同 hash 结果维持题目可复习状态。

`QuestionStore` 负责 schema/绑定/评分和状态持久化；`refresh_status()` 在 Wiki content/evidence hash 或 evidence 状态变化时将题目设为 `disabled`，避免继续复习陈旧事实。简答默认人工复核，也支持无网络 deterministic rubric（字符串或 `{keywords: [...]}`）及显式注入 LLM provider；provider 只能返回 0..1 score 和可选短 rationale，异常、缺失或 malformed 输出统一为 `unavailable`。作答结果以 append-only `practice/reviews/<question_id>.jsonl` 本地记录并 fsync；FSRS 只负责 review scheduling，不拥有事实、证据或隐私规则。`/api/practice/{question_id}/answer|review` 仅允许 local/private capability 调用，不能绕过 validator 或公开 practice 数据。

## 当前限制

基础实现尚未接入完整 Preview/Apply operation 和外部 target 传输；practice backup/restore 已接入 F012 owner-scoped manifest，批量失效已支持，完整跨仓库恢复演练仍待补。FastAPI 练习 API 与 FSRS 6.3.2 运行时已接入并有回归测试。

本轮调度状态兼容调查（2026-08-30）：`py-fsrs` 官方 `Card.to_dict()/from_dict()` 负责卡片序列化，Anki 的 review log 采用显式版本化状态边界；替代方案是只保存裸 Card 字段，升级后无法判断状态由哪个调度器版本产生。故 review state 保留兼容的 Card 字段，同时增加 `review_state_schema` 与 `scheduler_version` 元数据；升级不会伪造迁移成功，旧卡仍交给 adapter 重放，adapter 异常返回结构化 `unavailable`。

本轮 public leak 调查（2026-08-30）：Pagefind/静态发布常用输入树与 dist denylist 扫描（MIT，<https://github.com/CloudCannon/pagefind>）配合 schema-first projection allowlist；替代方案是只禁止 `practice/` 路径，题目 JSON 被误放到 `wiki/` 时仍可能公开答案。故 public leak gate 额外拒绝 `question/v1`、`review_state`、`answer`、`explanation`、`correct_option_ids` 与 `rubric` 字段，不依赖物理路径。

本轮恢复语义校验调查（2026-08-27）：Git bundle/checkout（GPL-2.0，<https://git-scm.com/docs/git-bundle>）提供对象哈希和离线传输，但不会理解题目 schema；SQLite Online Backup API（Public Domain，<https://sqlite.org/backup.html>）适合一致性数据库快照，本项目 practice 是 JSON/JSONL 文件而非 SQLite。替代方案 rsync（GPL-3.0，<https://github.com/WayneD/rsync>）只能复制字节，不能发现恢复后题目内容 hash、schema 或 review 所属题目不一致。故恢复流程保留 manifest 的逐文件 sha256，再额外执行 practice 语义闭包校验；任何题目 hash、schema、review question_id 或 JSONL 记录错误都返回结构化失败，目标目录清理且不派生 verified。该校验离线运行，不写入答案日志，不改变 `question/v1`/`practice-review-record/v1` 格式；升级只增加恢复门禁，不迁移既有事实。
