# F008 Question / 面试练习（Deferred）

- 状态：Deferred
- 当前主链路：不实现、不读取、不索引 Question、题库或复习状态
- 依赖：Source/Wiki/Claim/Evidence 契约稳定后再设计

## 已确定范围

F008 只覆盖三类题目：

- 单选题；
- 多选题；
- 面向面试的简答题。

题目必须从已验证的 Wiki claim 派生，不能成为 Source/Evidence 的事实载体。题目、答案、解析和练习状态的保密级别不得低于所属 Wiki；公开静态 Wiki 不读取题目答案或解析。

## 尚未决策

以下内容留到 F008 正式设计，不在当前系统规范或验收中预设实现：

- Question schema、题型字段和 ID/hash 规则；
- claim 绑定粒度、题干/选项/解析的证据校验；
- 简答题的人工评分、LLM 辅助评分和可解释反馈；
- 题目生成、人工审核、版本失效和重新出题策略；
- 本地练习状态、同步/备份边界以及是否采用 FSRS；
- 公开投影是否只展示题干，以及任何导出格式。

## 当前禁止事项

实现 F001-F012 时不得创建或解析 `Question`、`practice/` 题目文件、答案/解析、quiz/review API 或 FSRS 状态。`practice/` 目录只作为未来 Vault 布局占位，不进入当前索引、RAG、静态构建和备份验收。

## 设计入口

正式启动 F008 时，应新增独立 Technical Design、Acceptance 和 Traceability 条目；主系统设计只保留本页链接，不把历史草案当作现行 schema。
