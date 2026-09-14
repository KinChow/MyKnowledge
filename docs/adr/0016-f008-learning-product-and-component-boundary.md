# ADR-0016：F008 学习产品边界与成熟组件复用

- 状态：Accepted
- 日期：2026-09-09
- 相关规范：QST、API、WEB、SEC
- 相关 Feature：F008
- 替代/补充：补充 ADR-0008；不改变 private/local 隔离和 FSRS adapter 决策

## 背景

F008 的目标已经从“题目 API 基础能力”扩展为面向大模型知识的学习和复习产品：

- 以 Wiki 和面经为知识来源；
- 按领域和主题组织练习；
- 训练核心知识理解、面试表达和工程迁移；
- 单题几秒到几十秒内完成；
- 默认本地确定性自动评分；
- 复习状态不进入 public projection。

当前实现已经有 `question/v1`、单选/多选/简答、claim 绑定和 FSRS adapter，但题库为空，且没有可承接外部题包的 Question Platform、填空、知识点聚合、题目队列、短回合 session 或前端消费流程。不能把现有基础实现直接当成完整产品。

## 候选方案

### A. 直接嵌入 Moodle

Moodle 的 Quiz、题库、分类、尝试记录和成绩能力完整，但它是独立 LMS，不是 Astro 的题型组件。引入后需要额外维护 PHP 服务、数据库、认证、权限、升级和数据同步。

### B. 直接嵌入 Anki

Anki 的本地复习体验和生态成熟，但客户端不是 FastAPI/Astro 的嵌入式运行时。Anki 数据模型、同步、卡片模板和外部连接都会形成第二个数据 owner。

### C. 使用 H5P standalone 作为题型运行时

H5P 的 Multiple Choice、Fill in the Blanks 和 Question Set 可以复用题型交互与判分语义。`h5p-standalone` 可以在自托管页面展示提取后的 H5P 内容，不必部署 Moodle 或外部 H5P 服务；但它仍不拥有本项目的 claim 绑定、知识点聚合和 FSRS 状态。

### D. Question Platform + MyKnowledge 薄学习层

由 Question Platform 负责题目包导入、题目 registry、版本和生命周期；由练习运行面负责知识绑定、题库筛选、session、私密状态和本地 API；复用成熟库的明确能力：

- `py-fsrs`：调度算法和 Card 序列化；
- H5P standalone：可选的本地题型播放层和 importer 输入；
- Anki：内容与 review state 分离、复习记录和键盘/移动交互参考；
- Moodle：题库分类和组卷语义参考，不引入运行时。

## 决策

采用方案 D。Question Platform 是 canonical question content 的承接层；Deep-ML 不作为运行时或题目 schema 来源，只作为竞品和能力覆盖参考。

### 组件所有权

| 能力 | 复用对象 | MyKnowledge 自己负责 | 是否运行时依赖 |
| --- | --- | --- | --- |
| 题目导入、版本、启停和删除 | `question-package/v1` 作为内部交换契约；H5P/Anki 等 importer 可选 | package registry、collision、license、preview/apply、tombstone | 是 |
| 单选、多选、填空交互 | H5P 题型语义和反馈设计；可选 `h5p-standalone` 播放器 | Astro 题目渲染、题目版本、错误标签 | P2 可选 |
| 复习调度 | `py-fsrs` `Scheduler`、`Card`、`Rating` | 何时调用、评分映射、review log、题目/知识点聚合 | 是，Python 可选依赖但生产 profile 必须锁版本 |
| 内容与复习状态分离 | Anki note/card/review 边界 | `question/v2`、claim hash、vault 和备份 | 否 |
| 分类和组卷 | Moodle question bank/category 思路 | domain/topic/concept/skill、筛选器和 session | 否 |
| 题目自动生成 | 不复用在线生成服务 | 外层 Agent 可生成候选，MyKnowledge 只做 schema/evidence 校验 | 否 |
| 开放回答评分 | 不放入热路径 | 首期不用 LLM；保留人工/外部 scorer 接口 | 否 |

### 明确排除

- 不部署 Moodle 作为 F008 的后端；
- 不把 Anki 客户端或 AnkiConnect 作为主运行时；
- 不把 H5P 宿主、H5P.com 或 iframe 作为本地练习的必要条件；
- 不使用 LLM 参与默认实时评分；
- 不把 H5P、Anki 或 Moodle 的数据格式作为 canonical schema；
- 不把 Deep-ML 页面抓取结果直接作为题库或 canonical schema；
- 不把 FSRS 直接当作“知识点掌握度”模型。

## 后果

- 需要自己实现一层薄的题目服务和本地练习 UI，但不会维护完整 LMS；
- 可以先用 10--20 道真实大模型题验证学习闭环；
- 题目内容、题目判分、知识点聚合和调度可以独立演进；
- H5P/Anki 导入导出只能是后续能力，不能绕过当前 evidence、privacy 和 hash 门禁；
- `question/v1` 与现有 review state 需要兼容读取，新的题目创建使用 `question/v2`。

## 重新评估条件

- 需要多人课程、教师后台、考试计时、成绩册或组织权限时，重新评估 Moodle；
- 需要完整 Anki 客户端同步和跨平台复习时，重新评估 Anki 导出/同步；
- 需要非本地网页编辑器和大量现成题包时，重新评估 H5P runtime；
- 需要开放式面试回答自动评分时，单独建立评分 provider ADR，不得直接放开当前热路径。

## 参考入口

- H5P Question Set：<https://h5p.org/question-set>
- H5P Fill in the Blanks：<https://h5p.org/fill-in-the-blanks>
- H5P standalone：<https://github.com/tunapanda/h5p-standalone>
- Moodle Quiz：<https://docs.moodle.org/en/Quiz_activity>
- Anki 手册：<https://docs.ankiweb.net/>
- FSRS：<https://github.com/open-spaced-repetition/free-spaced-repetition>
- py-fsrs：<https://github.com/open-spaced-repetition/py-fsrs>
