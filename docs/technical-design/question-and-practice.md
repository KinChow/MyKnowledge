# F008 个人题库与大模型知识练习实现设计

- 状态：Designed；现有 `question/v1` 基础实现为 Implemented，个人 MVP 运行面尚未完成
- 相关 Feature：F008
- 相关 ADR：ADR-0008
- 相关验收：[F008](../acceptance/F008-question-practice.md)

## 1. 目标与边界

F008 只服务一个本地用户。题目是独立于 Wiki 的本地内容域，当前没有题目是正常状态；题目通过导入 JSON 文件进入题库，后端扫描题目目录提供 catalog、queue、answer 和 review。

目标：

- 学习和复习大模型知识；
- 配合 Wiki 和面经；
- 支持单选、多选、填空；
- 支持 domain/topic/concept/skill 分类；
- 支持几秒内确定性评分和即时解释；
- 使用 `py-fsrs` 进行题目级间隔复习。

非目标：

- 通用题库平台；
- 多用户、账号、同步和教师后台；
- 插件注册系统；
- H5P、Anki 或 Moodle 运行时；
- 代码沙箱、系统设计自动评分和 LLM 实时评分。

## 2. 数据布局

```text
content/practice/questions/<question_id>.json
    canonical question facts

content/practice/reviews/<question_id>.jsonl
    append-only attempts and review events

var/state/practice-index.json
    rebuildable catalog/index

var/state/practice-sessions/<session_id>.json
    short-lived session order and progress
```

题目和 review 属于 local/private，不进入 public projection。索引和 session 都是可删除重建的数据。

## 3. 题目文件

首期统一使用 `question/v1`，不另起 question package、revision registry 或插件协议：

```json
{
  "schema_version": "question/v1",
  "id": "q-kv-cache-001",
  "type": "single_choice",
  "domain": "llm-inference",
  "topic": "kv-cache",
  "concept_id": "kv-cache-growth",
  "skill": "mechanism",
  "prompt": "KV Cache 主要解决什么问题？",
  "options": [
    {"id": "a", "text": "避免重复计算历史 token 的 K/V"},
    {"id": "b", "text": "减少模型参数量"}
  ],
  "correct_option_ids": ["a"],
  "answer": null,
  "explanation": "Decode 时复用历史 token 的 K/V。",
  "rubric": null,
  "wiki_refs": [],
  "status": "enabled",
  "content_sha256": "sha256:..."
}
```

字段规则：

- `id`、`type`、`prompt`、分类字段必填；
- choice 必须有唯一 option ID 和合法 correct option；
- cloze 使用 `answer` 保存 accepted answers、aliases 和 normalization；
- `wiki_refs` 可为空；非空时校验 wiki/claim identity 和 hash；
- `status` 只有 `enabled`、`disabled`；
- `content_sha256` 不包含 status、review_state 和统计字段；
- review state 不写回题目事实文件，保存到 review log 或独立 state。

## 4. 导入和删除

### 4.1 导入

首期提供：

```text
python -m tools.cli question import ./questions/
POST /api/practice/import
```

导入流程：

```text
read JSON
  -> validate schema/type/hash
  -> check question ID and content hash
  -> copy to content/practice/questions/
  -> rebuild index
```

规则：

- 相同 ID 和相同内容 hash：幂等 no-op；
- 相同 ID 和不同 hash：阻断，不覆盖；
- 导入失败不留下半成品；
- 不修改已有 review log；
- 导入可以一次包含多个 JSON，但不引入 zip package manifest。

### 4.2 删除

首期提供：

```text
python -m tools.cli question disable <id>
python -m tools.cli question delete <id>
POST /api/practice/{id}/disable
DELETE /api/practice/{id}
```

删除策略：

- 没有 review 记录的题目可以物理删除；
- 已有 review 的题目默认改为 disabled，保留文件和历史；
- 删除不影响 Wiki、Source 或其他题目；
- 不引入 tombstone 和 ID 永不复用规则；单用户本地题库中，重新使用 ID 前由导入校验阻断当前文件即可。

## 5. 后端服务

保持现有 `QuestionStore` 作为领域服务，新增少量职责，不建设独立平台目录：

```text
QuestionStore
  load/list/import/disable/delete
  answer/review
  rebuild_index
  catalog/queue
```

新增的队列和 session 逻辑放在现有 `tools/` domain service；FastAPI 只做鉴权、参数校验和响应映射。

API：

```text
GET  /api/practice/catalog
GET  /api/practice/queue
POST /api/practice/sessions
POST /api/practice/{question_id}/answer
POST /api/practice/{question_id}/review
POST /api/practice/import
POST /api/practice/{question_id}/disable
DELETE /api/practice/{question_id}
```

空题库返回：

```json
{
  "state": "empty",
  "question_count": 0,
  "next_action": "import_question"
}
```

## 6. 评分

### 单选/多选

- 选项 ID allowlist；
- 单选精确匹配；
- 多选集合精确匹配；
- 反馈包含正确答案、解释和错误标签；
- 不调用 LLM。

### 填空

答案规范化：

1. Unicode NFKC；
2. casefold；
3. 合并空白；
4. 仅使用题目声明的 aliases；
5. 不默认使用编辑距离或开放语义匹配。

### Review 信号

记录 `correct`、`hint_used`、`response_ms`、`error_tags`。默认映射：

- 独立答对：Good；
- 答对但不确定或耗时长：Hard；
- 看强提示后答对：Again；
- 答错：Again。

answer 只记录 attempt；review 显式调用 FSRS。FSRS 只负责下一次 due，不代表 concept mastery。

错题与掌握状态分离：

- `content/practice/reviews/<question_id>.jsonl` 永久保留答题尝试和判分结果；
- 错题重练队列只读取每道题的最近一次作答结果，最近一次错误进入队列，最近一次正确移出队列；
- 移出活动错题队列不等价于“已掌握”，当前 MVP 不写入 mastery 结论；
- 后续版本可用连续正确次数、正确间隔和 FSRS due 联合计算 `mastery_state`，但不得覆盖历史记录。

## 7. 分类和短回合

分类字段：

```text
domain       llm-inference / llm-training / distributed
topic        kv-cache / attention / quantization / pd
concept_id   可独立复习的知识点
skill        recall / mechanism / calculate / diagnosis / interview
```

默认 6 题 session：

```text
2 道 due/relearning
1 道错题
2 道 new
1 道分类匹配的变式题
```

可按 `domain`、`topic`、`concept_id`、`skill`、`only_due`、`only_errors` 筛选。空结果不跨领域补题。

同一 `concept_id` 在一个 session 中最多出现两次，并尽量轮换题型。

## 8. 备份和 public 边界

沿用现有 practice backup、owner scope、content hash 和 leak gate。个人 MVP 不新增 Question Package、Registry 或跨设备同步协议。

Public projection 不读取：

- `content/practice/`；
- `answer`、`correct_option_ids`、`explanation`、`rubric`；
- attempts、review state、session state。

## 9. 实施阶段

### P0

- 题目 JSON schema；
- import/list/disable/delete；
- empty catalog；
- single/multi/cloze；
- catalog/queue/session；
- answer/review；
- FSRS；
- 10--20 道真实大模型题。

### P1

- 错题重练；
- Wiki 关联；
- 统计；
- 面试/工程模式；
- 更好的反馈和移动端交互。

### P2：按需

- H5P/Anki 导入导出；
- numeric/keypoint/scenario；
- SQLite 索引；
- 代码题和系统设计练习。

只有真实使用暴露出题量、同步或导入复杂度问题时，才引入更重的平台抽象。
