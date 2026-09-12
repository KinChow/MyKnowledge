# F008 个人题库与大模型知识练习验收

- Feature：F008
- 状态：Designed；现有 v1 基础能力已实现，个人 MVP 运行面未完成
- Technical Design：[Question 与面试练习实现设计](../technical-design/question-and-practice.md)

## 范围

本轮只验收单用户本地题库：

- 题目以 JSON 文件存在于 `content/practice/questions/`；
- 支持导入、校验、启用、禁用和删除；
- 支持单选、多选、填空；
- 支持按 domain/topic/concept/skill 筛选；
- 支持短回合、即时评分、错题重练和 FSRS；
- 题目和复习状态不进入 public projection。

不在本轮验收：插件系统、题目包 registry、H5P/Anki/Moodle、代码沙箱、开放式答案自动评分、多用户和跨设备同步。

## 题库与导入

### AC-F008-001 空题库

- Given：`content/practice/questions/` 不存在或为空；
- When：启动本地后端并请求题目目录/队列；
- Then：服务正常启动，返回 `state: empty` 和 `next_action: import_question`；不从 Wiki 临时生成题目。

### AC-F008-002 题目 JSON 校验

- Given：合法题目、未知字段、缺少题型字段、重复选项 ID、非法答案和错误 hash；
- When：执行导入或索引；
- Then：合法题目可落盘；非法题目被拒绝并返回字段级错误；失败不产生半成品题目或 review 记录。

### AC-F008-003 导入幂等和冲突

- Given：同一题目重复导入、同 ID 不同内容导入；
- When：执行 `practice import`；
- Then：内容 hash 相同为 noop；同 ID 不同 hash 阻断，不覆盖原题，不修改既有复习状态。

### AC-F008-004 启用、禁用和删除

- Given：enabled、disabled 题目以及已有 review 记录的题目；
- When：执行 enable、disable 或 delete；
- Then：disabled 不进入新队列；无 review 的题目可以删除；有 review 的题目默认保留题目文件和历史并标记 disabled；删除不影响 Wiki 和其他题目。

### AC-F008-005 可选 Wiki 关联

- Given：有 Wiki claim 绑定和没有 Wiki 绑定的题目；
- When：导入并索引；
- Then：两者都可以进入个人题库；存在 `wiki_refs` 时校验 Wiki/claim hash，漂移后题目 disabled；没有 Wiki 绑定不能伪装为已验证 Wiki。

## 题型与评分

### AC-F008-006 单选和多选

- Given：单选、多选题以及未知选项、重复选项、正确答案和错误答案；
- When：提交答案；
- Then：评分确定且可重放；未知/重复选项被拒绝；多选反馈显示缺少项和多选项。

### AC-F008-007 填空

- Given：accepted answers、aliases 和 term/phrase/number 规范化规则；
- When：提交大小写、空格、别名和非法近似答案；
- Then：只按题目声明的规则评分；不调用 LLM；返回规范化和判分结果。

### AC-F008-008 即时反馈

- Given：答对或答错的题目；
- When：完成 answer；
- Then：返回正确答案、解释、相关 Wiki 引用和可选错误标签；答题前不返回答案或隐藏解释。

## 队列与复习

### AC-F008-009 题目分类筛选

- Given：不同 `domain`、`topic`、`concept_id` 和 `skill` 的题目；
- When：请求 catalog 或 queue；
- Then：只返回符合筛选条件的 enabled 题目；无匹配时返回空结果和原因。

### AC-F008-010 短回合 session

- Given：新题、到期题和错题；
- When：创建 3、6 或 10 题 session；
- Then：返回稳定题目顺序；同一知识点不会无意义连续重复；session 不泄露答案。

### AC-F008-011 答题与复习分离

- Given：一次 session 答题；
- When：先调用 answer，再提交 rating；
- Then：answer 只记录 attempt 和反馈；review 才调用 FSRS；任一失败不伪造另一阶段成功。

### AC-F008-012 错题重练

- Given：答错或使用提示后答对的题目；
- When：请求 error queue；
- Then：最近一次作答错误的题目进入活动队列；最近一次作答正确的题目从活动队列移除；所有历史 attempt、原始错误标签、提示状态和最近作答时间仍保留；移出队列不产生“已掌握”结论。

### AC-F008-013 FSRS 状态

- Given：无卡片、已有卡片、非法 rating 和 FSRS 依赖缺失；
- When：提交 review；
- Then：可用时保存 Card 和 scheduler version；不可用时返回结构化 `provider_unavailable`，不伪造 due。

### AC-F008-014 状态恢复

- Given：题目和 review JSONL 已存在；
- When：重启后重新构建索引；
- Then：题目、队列和 FSRS 状态可继续使用；索引可删除并重建，不改变 canonical 题目和 review log。

## 隔离与真实切片

### AC-F008-015 Public 隔离

- Given：题目含答案、解释、accepted answers 和 review state；
- When：生成 public projection、索引或 dist；
- Then：这些字段不被复制或索引；字段级 leak gate 仍然拒绝误放到 public 路径的题目内容。

### AC-F008-016 真实垂直切片

- Given：至少 10 道个人有权使用的大模型题目，覆盖 KV Cache、Prefill/Decode 或推理性能；
- When：完成至少 5 个短回合；
- Then：能按领域筛选、答题、查看反馈、重练错题并完成 FSRS review；所有记录位于 local/private。

## 完成定义

F008 个人 MVP 只有在 AC-F008-001 至 AC-F008-016 均有测试或真实运行证据后，才从 Designed/Implemented（基础）推进 Accepted。
