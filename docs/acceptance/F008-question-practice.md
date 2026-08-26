# F008 Question / 面试练习验收

- Feature：F008
- 状态：Implemented（基础能力；完整验收未闭合）
- 实现证据：`tools/question.py`、`tests/test_question.py`

## AC-F008-001 题型与 schema

- Given：单选、多选、简答和非法题目定义；When：创建题目；Then：合法题目写入 `question/v1`，非法字段被拒绝；失败时不变量：不产生题目文件。
- 对应测试：`tests/test_question.py::QuestionTests::test_create_requires_verified_claim`；当前状态：通过。

## AC-F008-002 Claim 绑定与证据 hash

- Given：Wiki claim 验证报告；When：创建题目；Then：保存 Wiki/claim/content/evidence 绑定；未验证或 evidence 不可用时阻断；当前状态：基础绑定通过，Wiki 变化后的自动迁移待补。

## AC-F008-003 自动评分与简答复核

- Given：单选、多选或简答答案；When：作答；Then：选择题 deterministic 评分，简答返回 rubric/manual review；当前状态：通过，测试见 `tests/test_question.py`。

## AC-F008-004 FSRS review adapter

- Given：rating 1..4；When：更新复习状态；Then：调用 FSRS，依赖不可用时返回明确 `unavailable`；当前状态：adapter 边界通过，安装 FSRS 后的真实调度回归待补。

## AC-F008-005 Public 隔离

- Given：practice 题目包含答案、解析和 review state；When：生成 public projection；Then：public 输入、索引和静态构建不读取 practice；当前状态：由 F007 leak gate 集成验收待补。

## 本轮证据（2026-08-30）

- AC-F008-002/003：`tests/test_question.py::QuestionTests::test_claim_hash_change_disables_question` 验证 claim content hash 变化后题目变为 `disabled`，后续作答返回 `question_disabled`。
- AC-F008-005：`tests/test_api.py::test_practice_api_is_private_and_does_not_bypass_validator` 验证练习 API 缺 capability 时返回 401，携带 capability 但题目不存在时返回结构化 `question_not_found`，不会绕过题目服务。
- AC-F008-004：FSRS 缺失时仍返回 `unavailable/provider_unavailable`，不伪造调度成功。

真实 FSRS 版本回归、practice backup/restore、public build 全量输入扫描和简答 LLM 辅助评分仍待闭合。

## 评分记录增量证据（2026-08-30）

- AC-F008-003/005：自动评分和简答 manual review 结果追加到 `practice/reviews/<question_id>.jsonl`，写入后显式 fsync；该目录不在 public projection 输入范围内。
