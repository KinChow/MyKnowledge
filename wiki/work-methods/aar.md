---
aliases:
- After Action Review
- 行动后回顾
confidentiality: public
domain: work-methods
evidence:
- claim: AAR 是通过结构化团队讨论评估并捕获经验教训、保持优势改进缺点的方法。
  claim_id: definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-b297b3fe87b6
    exact: AAR，事后回顾，是一个团队对话的会议，在项目或活动的关键阶段，通过简单、结构化的讨论来评估和捕获经验教训，以保持优势，改善缺点的方法
  targets:
  - evidence_id: evidence-b297b3fe87b6
    source_id: aar
- claim: AAR 起源于美国陆军的任务后经验传递与改进实践。
  claim_id: origin
  support: direct
  supporting_quotes:
  - evidence_id: evidence-867cda3460e7
    exact: AAR最早是美国陆军所进行的一项任务后的经验传递和改进方法
  targets:
  - evidence_id: evidence-867cda3460e7
    source_id: aar
id: aar
kind: knowledge
publication_scope: public
related: []
sources:
- aar
status: published
tags:
- retrospective
- knowledge-management
title: AAR 事后回顾
updated_at: '2026-08-28'
---

# AAR 事后回顾

## 一句话结论

AAR（After Action Review，事后回顾）是团队在任务关键节点后，用四个结构化问题捕获经验教训并立即改进的复盘方法，起源于美国陆军。

## 核心概念

- **结构化四问**：期望发生什么 / 实际发生什么 / 为什么有差异、学到什么 / 下次怎么做。
- **即时性**：任务结束后立即执行，趁记忆新鲜捕获事实。
- **团队对话**：不是个人总结，是集体对事实与差异的对齐。

## 工作机制

1. 任务或活动到达关键阶段后，团队立即召集 AAR 会议；
2. 主持人按四个结构化问题依次引导讨论，先对齐事实再分析差异；
3. 捕获的经验教训立即转化为下一步行动，反馈到后续执行。

## 示例或代码

- 软件团队在一个迭代结束后，用四问复盘：计划的交付目标 vs 实际交付，差异原因（估时、阻塞、需求变更），下迭代的具体改进行动。
- 事故响应后：期望的恢复时间 vs 实际恢复时间，根因与响应流程缺口，改进项进入待办。

## 常见误区

- 把 AAR 开成追责会：讨论目标是事实与改进，不是个人责任判定；
- 只谈问题不谈保持：AAR 同时捕获"做得好的要保持"的优势；
- 没有下一步动作：捕获了教训但不落到行动，等于没复盘。

## 证据映射

- `definition` claim 由个人笔记中 AAR 定义段落直接支撑（direct）；
- `origin` claim 由笔记中 AAR 起源段落直接支撑（direct）；
- 方法论原始出处：美国陆军 TC 25-20（B1 检索结论，见迁移台账 §7，待建外部 source 后升级证据）。

## 待验证项

- [ ] 建立 TC 25-20 / After Action Review 外部 source，将 definition/origin 升级为外部证据；
- [ ] 补充 AAR 与其他复盘方法（如 Retrospective、PDCA）的差异对照。

## 关联知识

- 团队知识管理与经验传承
- 迭代复盘（Sprint Retrospective）