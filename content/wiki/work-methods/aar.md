---
aliases:
- After Action Review
- 行动后回顾
confidentiality: public
domain: work-methods
evidence:
- claim: AAR 是针对事件、聚焦绩效标准的专业讨论，让士兵自行发现发生了什么、为什么、如何保持优势并改进不足。
  claim_id: definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-6ee1d813f9cd
    exact: An after-action review (AAR) is a professional discussion of an event,
      focused on performance standards, that enables soldiers to discover for themselves
      what happened, why it happened, and how to sustain strengths and improve on
      weaknesses. It is a tool leaders and units can use to get maximum benefit from
      every mission or task.
  targets:
  - evidence_id: evidence-6ee1d813f9cd
    source_id: aar-tc25-20
- claim: 存在由美国陆军（Department of the Army）发布的训练通告 TC 25-20。
  claim_id: army-origin
  support: direct
  supporting_quotes:
  - evidence_id: evidence-68b2a80bb990
    exact: '**HEADQUARTERS DEPARTMENT OF THE ARMY**'
  - evidence_id: evidence-c05892b14a9a
    exact: '**TC 25-20**'
  targets:
  - evidence_id: evidence-68b2a80bb990
    source_id: aar-tc25-20
  - evidence_id: evidence-c05892b14a9a
    source_id: aar-tc25-20
id: aar
kind: knowledge
publication_scope: public
related: []
sources:
- aar-tc25-20
status: published
tags:
- retrospective
- knowledge-management
title: AAR 事后回顾
updated_at: '2026-09-03'
---
# AAR 事后回顾

## 一句话结论

AAR（After Action Review，事后回顾）是团队在任务关键节点后，用结构化讨论评估并捕获经验教训、保持优势改进缺点、并立即改进的复盘方法，源自美国陆军（官方训练通告 TC 25-20）。

## 核心概念

- **事后回顾**：团队在项目或活动关键阶段，通过简单、结构化的讨论来评估和捕获经验教训，以保持优势、改善缺点。
- **引导式对话**：通过引导，团队从刚完成的任务、事件或活动中捕获经验教训，并立即应用以提升绩效。
- **即时性**：任务结束后立即执行，趁记忆新鲜捕获事实。
- **正式 / 非正式**：正式 AAR 资源投入大（场地、辅助人员、支援），通常在公司及以上层级、训练前六到八周规划；非正式 AAR 用于排及以下小单元训练，资源要求低、机动灵活。

## 工作机制

1. 任务或活动到达关键阶段后，团队立即召集 AAR；
2. 围绕四个结构化问题依次讨论：期望发生什么 / 实际发生什么 / 为什么有差异、学到什么 / 下次怎么做；
3. 引导原则：用开放式问题而非"是/否"问题，鼓励参与者自行得出结论（AAR 不是批评或讲座）；
4. 捕获的经验教训立即转化为下一步行动，反馈到后续执行。

## 示例或代码

- 软件团队迭代结束后的四问复盘：计划的交付目标 vs 实际交付，差异原因（估时、阻塞、需求变更），下迭代的具体改进行动。
- 事故响应后：期望的恢复时间 vs 实际恢复时间，根因与响应流程缺口，改进项进入待办。

## 常见误区

- 把 AAR 开成追责会：AAR 是"专业讨论"而非批评——讨论目标是事实与改进，不是个人责任判定；
- 只谈问题不谈保持：AAR 同时捕获"做得好的要保持"的优势；
- 没有下一步动作：捕获了教训但不落到行动，等于没复盘；
- 用是/否式提问：应引导式讨论，用开放式问题让参与者自己发现差距。

## 证据映射

- `definition` claim 由美国陆军 TC 25-20 权威定义逐字支撑（direct）；
- `army-origin` claim 由 TC 25-20 官方通告属性支撑（direct）；
- 引导原则、正式/非正式区分等正文内容来自 TC 25-20 相关章节（body 推理，未逐字锚定为 claim）；
- 与 Retrospective / PDCA 的对照为知识综合，属 body 内容，不上升为 claim。

## 待验证项

- [ ] AAR 起源的 1970s National Training Center 具体时间线：当前网络下 Army 官方历史站（history.army.mil / armyupress.army.mil）与维基均不可抓取，待网络可达时补独立权威来源并升级证据；
- [ ] AAR 在非军事领域的适配边界（如 NHS 医疗场景应用）：待补权威文献。

## 关联知识

- 团队知识管理与经验传承
- 迭代复盘（Sprint Retrospective）
- 戴明 PDCA 循环：AAR 的"下次怎么做"对应 PDCA 的 Act 环节，但 AAR 更强调事后即时、团队自我发现，PDCA 更强调循环改进；Retrospective 是敏捷迭代末的团队复盘，与 AAR 同源但常用于软件研发节奏。

## 详细章节

### AAR

#### 什么是AAR

AAR，事后回顾，是一个团队对话的会议，在项目或活动的关键阶段，通过简单、结构化的讨论来评估和捕获经验教训，以保持优势，改善缺点的方法。通过引导，团队从刚刚完成一项任务，事件或活动中捕获团队的经验教训，并立即应用这些知识来提高团队绩效。



AAR的四个结构化问题

* 我们原先期望发生了什么？
* 实际发生了什么？
* 为什么有差异？我们从中学到什么？
* 下次我们将怎么做？



AAR最早是美国陆军所进行的一项任务后的经验传递和改进方法，对美国陆军来说，使用这种方法的好处在于当产生新的改进建议时，马上响应到行动上，他们使用AAR解决了很多问题。



#### 为什么需要AAR

* AAR主要用于团队内经验迅速闭环应用
* 有效帮助捕获项目重要经验教训，持续学习，不断改进
* 促进组织内部隐性知识沉淀，避免知识因项目解散而流失
* 通过集体的学习，丰富团队成员的知识和经验，促进团队的成长
* 团队将能更熟练的设定实际可达到的目标
* 帮助成员对团队发生的事情及意义形成统一的观点或理解，这是团队达成进一步共识的基础
* 帮助建立团队坦诚、开放的氛围
* AAR产生的经验教训也可以传递给有需要的团队，促进经验教训和优秀实践分享，避免问题重犯，识别机会点

