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

- [ADR-0001 Source-first 与证据模型](./0001-source-first-evidence-model.md)
- [ADR-0002 公开仓库与 Private Vaults（0..N）](./0002-public-repository-and-private-vault.md)
- [ADR-0003 原文快照与 Git LFS](./0003-source-snapshot-and-git-lfs.md)
- [ADR-0004 内容 Hash 与失效粒度](./0004-content-hash-and-invalidation.md)
- [ADR-0005 引文规范化与验证](./0005-quote-normalization-and-verification.md)
- [ADR-0006 Preview/Apply 写协议](./0006-preview-apply-write-protocol.md)
- [ADR-0007 检索和索引架构](./0007-retrieval-and-index-architecture.md)
- [ADR-0008 Question 门禁与 FSRS](./0008-question-evidence-and-fsrs.md)
- [ADR-0009 Astro/Starlight 静态 Wiki 发布链](./0009-static-wiki-publishing.md)
- [ADR-0010 发布门禁：确定性校验 + 可选 LLM 规范审计 + 必须人工审计](./0010-publish-gate-llm-audit-and-human-approval.md)
- [ADR-0011 入口层必须消费共享 domain service](./0011-entry-layer-shared-services.md)
