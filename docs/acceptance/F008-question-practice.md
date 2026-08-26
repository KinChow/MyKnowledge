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

## AC-F008-006 简答评分 provider 边界

- Given：简答题 rubric；When：分别以人工、deterministic 和注入 LLM provider 评分；Then：人工返回 `manual_review`，deterministic 按 rubric 可重复计算 0..1 分数，LLM 缺失/异常/malformed 返回 `unavailable`；provider endpoint、密钥和原始 prompt 不写入 practice 记录。
- 对应测试：`tests/test_question.py::QuestionTests::test_short_answer_deterministic_rubric_and_provider_boundaries`；当前状态：通过。

## AC-F008-007 Practice 备份与恢复

- Given：题目答案、解析和 review state 位于某个 vault 的 `practice/`；When：生成 owner-scoped manifest、校验并恢复到空 checkout；Then：questions/reviews 均按 sha256 恢复，不读取其他 vault，非空目标或篡改 manifest 阻断；当前状态：通过，测试见 `tests/test_vault_registry.py::VaultRegistryTests::test_practice_entries_are_owner_scoped_and_restored` 与 `test_private_manifest_does_not_read_public_or_escape_owner`。

## AC-F008-008 批量题目失效

- Given：多个本地题目分别绑定仍有效、已变化或缺失的 Wiki；When：执行 `refresh_all(wiki_reports)`；Then：有效题目保持 enabled，stale/missing claim 题目变为 disabled 并保留原文件和 review 记录；当前状态：通过 `tests/test_question.py::QuestionTests::test_refresh_all_disables_missing_or_stale_wiki_reports`。

## 本轮证据（2026-08-30）

- AC-F008-002/003：`tests/test_question.py::QuestionTests::test_claim_hash_change_disables_question` 验证 claim content hash 变化后题目变为 `disabled`，后续作答返回 `question_disabled`。
- AC-F008-005：`tests/test_api.py::test_practice_api_is_private_and_does_not_bypass_validator` 验证练习 API 缺 capability 时返回 401，携带 capability 但题目不存在时返回结构化 `question_not_found`，不会绕过题目服务。
- AC-F008-004：`.venv` 中实际安装 `fsrs==6.3.2` 后，`tests/test_question.py::QuestionTests::test_fsrs_unavailable_is_explicit` 验证真实 `scheduled` 结果与 Card state 持久化；依赖缺失路径仍由 adapter 返回 `unavailable/provider_unavailable`，不伪造调度成功。

真实 FSRS 版本回归、practice backup/restore、public build 全量输入扫描仍待闭合；简答 provider 边界已通过 AC-F008-006。

## 评分记录增量证据（2026-08-30）

- AC-F008-003/005：自动评分和简答 manual review 结果追加到 `practice/reviews/<question_id>.jsonl`，写入后显式 fsync；该目录不在 public projection 输入范围内。
