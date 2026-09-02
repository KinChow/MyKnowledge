# Architecture Decision Records

ADR 只记录具有长期影响、存在多个合理方案且需要保留取舍原因的决策。

## 生命周期

```text
Proposed → Accepted → Superseded
                    ↘ Deprecated
```

被替代的 ADR 保留，不删除。字段和状态机属于系统规范，模块接口属于 Technical Design，验证场景属于 Acceptance。

## 模板

```markdown
# ADR-NNNN：标题

- 状态：Proposed
- 日期：2026-08-25
- 相关规范：
- 相关 Feature：

## 背景
## 候选方案
## 决策
## 后果
## 重新评估条件
```

## 索引

| ADR | 状态 | 决策 | 链接 |
| --- | --- | --- | --- |
| ADR-0001 | Accepted | Source-first 与证据模型 | [正文](./0001-source-first-evidence-model.md) |
| ADR-0002 | Accepted | 公开仓库与 Private Vaults（0..N） | [正文](./0002-public-repository-and-private-vault.md) |
| ADR-0003 | Accepted | 原文快照与 Git LFS | [正文](./0003-source-snapshot-and-git-lfs.md) |
| ADR-0004 | Accepted | 内容 Hash 与失效粒度 | [正文](./0004-content-hash-and-invalidation.md) |
| ADR-0005 | Accepted | 引文规范化与验证 | [正文](./0005-quote-normalization-and-verification.md) |
| ADR-0006 | Accepted | Preview/Apply 写协议 | [正文](./0006-preview-apply-write-protocol.md) |
| ADR-0007 | Accepted | 检索和索引架构 | [正文](./0007-retrieval-and-index-architecture.md) |
| ADR-0008 | Accepted | Question 门禁与 FSRS（基础实现；完整运行面按 Acceptance 增量闭合） | [正文](./0008-question-evidence-and-fsrs.md) |
| ADR-0009 | Accepted | Astro/Starlight 静态 Wiki 发布链 | [正文](./0009-static-wiki-publishing.md) |
| ADR-0010 | Accepted | 发布门禁：确定性校验 + 可选 LLM 规范审计 + 必须人工审计 | [正文](./0010-publish-gate-llm-audit-and-human-approval.md) |
| ADR-0011 | Accepted | 入口层必须消费共享 domain service | [正文](./0011-entry-layer-shared-services.md) |
| ADR-0012 | Accepted | LLM 责任边界：MyKnowledge 不内置生成式能力 | [正文](./0012-llm-responsibility-boundary.md) |
| ADR-0013 | Accepted | ASR 派生 snapshot 的证据强度上限为 attested | [正文](./0013-asr-derived-snapshot-strength.md) |
| ADR-0014 | Accepted | 数据分域、五层归属与三条写入通道 | [正文](./0014-layer-domains-and-write-channels.md) |
| ADR-0015 | Accepted | 审计分歧取 fail，唯一推翻路径是留痕的人工复议 | [正文](./0015-audit-disagreement-and-human-reconsideration.md) |

> 状态从各 ADR 正文「- 状态：」行读取；被替代的 ADR 保留不删除（Superseded/Deprecated）。
> 索引完整性由 `tools.matrix_sync.check_doc_indexes` 机器校验（新增 ADR 必须登记）。
