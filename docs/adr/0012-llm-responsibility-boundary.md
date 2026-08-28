# ADR-0012：LLM 责任边界——MyKnowledge 不内置生成式能力

- 状态：Accepted
- 日期：2026-08-28
- 相关规范：§8（LLM 审计）、§12（API）、SEC
- 相关 Feature：F003、F006、F009

## 背景

调用方向是"外层 Agent（Comate/Claude 等）通过 Skill/MCP 调用 MyKnowledge"，而不是 MyKnowledge 调用 Agent/LLM。外层 Agent 天然自带 LLM；若 MyKnowledge 内部再接 LLM provider，等于在同一链路上重复引入模型依赖、凭据管理与超时面，且生成的答案无法继承外层 Agent 的上下文。

## 候选方案

- A. MyKnowledge 内置 ask 生成 + F003 审计 provider 长期内置：能力自包含，但依赖/凭据重复、与"受控知识库"定位冲突。
- B.（选定）MyKnowledge 零生成式内置：检索/校验/回放全确定性；LLM 职责归外层 Agent，MyKnowledge 只提供契约化的输入输出。
- C. 完全移除 F003 provider 代码：激进；现有实现已 fail-closed（未配置 → `not_run`，人工确认兜底），保留为可选内置审计器成本为零。

## 决策

1. **`/api/ask` 与 Skill `ask` 永不接入 LLM provider**：永久返回 `unavailable` 或纯检索结果 + citations 是**设计决定而非待办**。正确的问答形态是：外层 Agent 调 `retrieve/query` 拿命中 → Agent 自身 LLM 生成回答 → 引用经 `citation replay` 校验可回放。
2. **F003 审计 provider 定位为"可选内置审计器"**：未配置时 `validation_state: not_run` + 人工确认兜底（现有行为，不是硬依赖）。长期演进方向是外层 Agent 消费 `wiki-validation-request/v1` 契约完成审计并回写 response——契约已存在，切换不需要改动门禁。
3. **确定性优先**：MyKnowledge 的所有门禁（schema/证据/发布/锁）保持确定性可重放；任何"智能"都发生在边界之外，其产物以结构化事件（带 hash）回流。

## 后果

- 少一条 provider 凭据管理面；ask 的"待接线"从 F006 边界中移除（设计排除）。
- 问答质量取决于外层 Agent；MyKnowledge 只保证它引用的证据可回放。
- F003 的 provider 实现保留（可选路径），未来若外层审计契约落地后仍长期不用，再评估退役。

## 重新评估条件

出现多用户服务形态（多人共享同一个 MyKnowledge 实例、无外层 Agent 中介）时重新评估。
