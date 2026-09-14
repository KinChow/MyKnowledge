# F008 Question Platform：可插拔题目域与练习后端

- 状态：Designed
- 日期：2026-09-11
- 相关 Feature：F008
- 相关 ADR：ADR-0008、ADR-0016
- 竞品参考：[F008 Deep-ML Inference Engineer 对齐与完整训练方案](./f008-deep-ml-interview-mapping.md)

## 1. 核心修正

Question 与 Wiki 是同一层级的内容域，不是 Wiki 的一个附属字段：

```text
Source ──> Wiki ──> public/local knowledge projection

Question Package ──> Question Registry ──> Practice Platform
                                      ├── catalog
                                      ├── import/enable/disable/delete
                                      ├── session/queue
                                      ├── grading
                                      └── review scheduling
```

二者可以通过 `knowledge_refs` 关联，但所有权不同：

- Wiki 管理知识事实、claim 和 evidence；
- Question 管理练习题面、答案、反馈、题型和题目来源；
- Practice Platform 管理运行时队列、作答、调度和统计；
- Question 不能反向成为 Wiki 的事实来源；
- 删除 Question 不删除 Wiki，Wiki 失效也不物理删除 Question。

题库当前为空不是异常。平台必须先以空目录、空 catalog、无题可练的可解释状态启动，再通过导入题目包产生内容。

## 2. 平台职责

### 2.1 Content plane

负责可审计、可版本化的题目内容：

- Question Package 导入；
- schema、题型和题目完整性校验；
- 来源和许可证记录；
- 可选的 Wiki claim 绑定；
- 题目版本和状态；
- 题目删除/撤回/禁用。

### 2.2 Runtime plane

负责用户练习：

- 按 domain/topic/skill/source/filter 生成 catalog；
- 生成短回合 session；
- 返回不泄露答案的 question view；
- 接收 answer 并确定性评分；
- 记录 attempt；
- 调用 FSRS；
- 返回反馈和统计。

### 2.3 不属于平台的职责

- 不自动把外部题目当作 verified Wiki；
- 不在导入时强制所有题目绑定 Wiki；
- 不把 Deep-ML 页面抓取结果直接当作 canonical question；
- 不内置 LLM 生成或实时开放回答评分；
- 不让前端直接读题目文件；
- 不让导入包覆盖用户已有题目或 review state。

## 3. 插件模型

“可插拔”分三层，不把所有插件混成一种：

| 层 | 插件对象 | 作用 | 首期 |
| --- | --- | --- | --- |
| Content source | `question-package/v1` | 导入题目内容和来源 | 必须 |
| Question type | `question-type/v1` | schema、view、grading、feedback | 内置 3 种 |
| Scheduler | `scheduler/v1` | 根据 review event 计算下一次复习 | FSRS adapter |

未来可以增加：

- `h5p-package` importer；
- `anki-apkg` importer/exporter；
- 外部题库 API importer；
- `code-task` grader；
- `design-checklist` grader。

插件不能绕过平台的统一边界。每个插件必须声明：

```json
{
  "plugin_id": "question-type/cloze",
  "plugin_version": "1.0.0",
  "schema_version": "question-type/v1",
  "capabilities": ["render", "grade", "feedback"],
  "network": false,
  "writes": ["attempt"],
  "license": "project-compatible"
}
```

插件只返回结构化结果，不获得 vault 路径、token、其他题目答案或任意文件读写能力。

## 4. Question Package

### 4.1 包结构

推荐导入包为 zip 或目录，内部结构稳定、可校验：

```text
package.json
questions/
  q-001.json
  q-002.json
sets/
  inference-basics.json
assets/
  ...
checksums.json
```

`package.json`：

```json
{
  "schema_version": "question-package/v1",
  "package_id": "llm-inference-basics",
  "revision": 1,
  "title": "LLM Inference Basics",
  "publisher": "personal",
  "license": "CC-BY-4.0",
  "source_refs": [],
  "question_count": 20,
  "package_sha256": "sha256:..."
}
```

### 4.2 导入原则

导入分为 `preview` 和 `apply`：

```text
read package
  -> package manifest/schema validation
  -> checksum validation
  -> ID collision analysis
  -> license/confidentiality check
  -> question type plugin validation
  -> optional Wiki claim binding check
  -> preview report
  -> human confirmation
  -> apply to selected vault
  -> registry rebuild
```

preview 必须报告：

- 新增题目；
- 已存在且内容相同的题目；
- ID 相同但内容不同的冲突；
- 不支持的题型；
- 缺失答案/反馈/分类；
- 来源或 license 缺失；
- Wiki claim 绑定失效；
- 需要覆盖的 revision。

默认策略：

- 相同 `question_id + revision + content_sha256`：`noop`；
- 相同 ID、不同 revision：新增版本，不覆盖旧版本；
- 相同 ID、相同 revision、不同 hash：`conflict`，必须人工选择；
- 禁止导入包修改已有 attempt/review/card；
- 禁止导入包物理删除已有题目。

### 4.3 外部题库适配

外部来源必须先转换为 canonical package：

```text
Deep-ML / H5P / Anki / custom JSON
        ↓ importer
question-package/v1
        ↓ platform validator
Question Registry
```

Deep-ML 页面是竞品和能力地图，不是首期自动抓取对象。若未来需要导入，必须遵守页面版权、服务条款和人工筛选要求；导入的是用户有权使用的题目内容或用户自编重述，不默认复制第三方原文。

## 5. Question Registry

Registry 是平台的题目索引，不是题目内容的第二份真相：

```json
{
  "question_id": "q-001",
  "revision": 1,
  "package_id": "llm-inference-basics",
  "package_revision": 1,
  "vault_id": "private",
  "type": "single_choice",
  "domain": "llm-inference",
  "topics": ["kv-cache"],
  "skills": ["mechanism"],
  "concept_ids": ["kv-cache-growth"],
  "status": "enabled",
  "content_sha256": "sha256:...",
  "next_due_at": null
}
```

Registry 可从题目包和 review records 重建。题目文件保存 canonical content，Registry 不重复保存答案和解释。

## 6. 生命周期

```text
imported -> enabled -> disabled
                    ├── retired
                    └── deleted
```

- `imported`：已落盘但未进入练习队列；
- `enabled`：可被 catalog/session 选中；
- `disabled`：暂不练习，保留内容和历史；
- `retired`：作者撤回或来源失效，不再进入新 session；
- `deleted`：题目内容删除，但保留最小 tombstone 和 review 引用，避免 ID 重用。

删除 API 不是直接 `rm`：

```text
POST /api/practice/questions/{question_id}/disable
POST /api/practice/questions/{question_id}/retire
POST /api/practice/questions/{question_id}/delete/preview
POST /api/practice/questions/{question_id}/delete/apply
```

删除规则：

- 没有 attempt/review 的题目可以物理删除；
- 有历史记录的题目默认只做 `retired`；
- 强制删除必须显式确认，并留下 tombstone；
- question ID 永不复用；
- 删除题目不删除 Wiki 或来源；
- 删除 package 时先列出受影响题目，不能级联删除学习记录。

## 7. 后端模块

```text
backend/
  question_platform/
    package_reader.py       # zip/dir reader, manifest/checksum
    importer.py             # preview/apply, collision and license checks
    registry.py             # rebuildable question catalog
    lifecycle.py            # enable/disable/retire/delete
    views.py                # safe question view, answer redaction
    session.py              # queue and short session
    grading.py              # question-type plugin dispatch
    review.py               # attempt -> FSRS review event
    stats.py                # question/concept/package statistics
```

现有 `QuestionStore` 应降级为 `question/v1` 兼容 adapter 和底层文件读写，不再承担整个产品平台职责。

## 8. API

### 内容管理

```text
GET  /api/practice/packages
POST /api/practice/packages/import/preview
POST /api/practice/packages/import/apply
GET  /api/practice/packages/{package_id}
POST /api/practice/packages/{package_id}/retire

GET  /api/practice/questions
GET  /api/practice/questions/{question_id}
POST /api/practice/questions/{question_id}/enable
POST /api/practice/questions/{question_id}/disable
POST /api/practice/questions/{question_id}/retire
POST /api/practice/questions/{question_id}/delete/preview
POST /api/practice/questions/{question_id}/delete/apply
```

### 练习运行

```text
GET  /api/practice/catalog
POST /api/practice/sessions
GET  /api/practice/sessions/{session_id}/next
POST /api/practice/sessions/{session_id}/answer
POST /api/practice/sessions/{session_id}/review
GET  /api/practice/stats
```

所有内容管理写操作遵循项目既有 `preview -> human confirmation -> apply`；answer/review 是用户学习事件，不走内容写入审批，但必须使用 local/private capability。

## 9. 空题库行为

空题库是正常状态，API 必须返回：

```json
{
  "schema_version": "practice-catalog/v1",
  "state": "empty",
  "question_count": 0,
  "packages": [],
  "available_filters": [],
  "next_action": "import_question_package"
}
```

创建 session 不应返回 404 或随机读取 Wiki 生成题目；应返回 `practice_catalog_empty`。题目导入成功后，registry、catalog 和 session 才会出现可练习内容。

## 10. 与 Wiki 的关系

Question 可以有多种来源：

```text
wiki-derived       绑定 Wiki claim，要求 hash 可验证
interview-derived  来自面经/题库，允许没有 Wiki 绑定
personal           用户自定义，保留 provenance
external-package   外部包导入，必须有 source/license
```

`wiki-derived` 是强绑定；其他类型不被强行伪装为 Wiki claim。若外部题目要进入“核心知识”报告，可以另行建立 Wiki 绑定或标记为未验证。

这使得题目平台可以先导入面经题，再逐步补齐 Wiki，而不阻塞题库建设。

## 11. 关键 trade-off

### 11.1 文件包 vs 数据库

首期采用 package + JSON/JSONL：

- 适合单人、local-first、Git 和可审计导入；
- 能保留原始题包和 package hash；
- 导入 preview 易于复现；
- 大规模筛选和并发写入较弱。

当题库或 review log 达到需要索引事务、多设备同步或高并发时，再将 Registry/attempt 索引迁移到 SQLite；canonical package 不因此改变。

### 11.2 题目独立于 Wiki vs 强制绑定 Wiki

选择可选绑定：

- 可以承接 Deep-ML 风格面经题和外部题包；
- 不会因为 Wiki 尚未整理完而无法导入；
- 代价是题目可信度需要显式显示；
- 通过 `provenance`、`verification_state` 和 `knowledge_refs` 区分可信程度。

### 11.3 直接复用 H5P vs canonical schema

选择 importer/adapter：

- H5P 可作为成熟题型输入来源；
- canonical schema 保持与项目安全、claim、review 和 registry 兼容；
- 代价是字段映射和部分高级交互会丢失；
- 丢失字段必须在 import preview 中显式报告。

## 12. P0--P3

### P0：平台空壳和导入闭环

- 空题库 catalog；
- `question-package/v1`；
- package list/detail；
- import preview/apply；
- collision、license、checksum；
- question list/detail/disable/retire；
- 单选、多选、填空插件；
- 10--20 道真实用户有权使用的题目包；
- 不做 Deep-ML 自动抓取。

### P1：练习运行面

- safe question view；
- catalog filter；
- 6 题 session；
- answer、feedback、attempt；
- FSRS review；
- 错题和到期队列；
- package/source/concept stats。

### P2：扩展导入和题型

- H5P importer 或 standalone 播放 adapter；
- Anki importer/exporter；
- numeric、keypoint、scenario；
- 多 claim 绑定；
- package revision migration。

### P3：深度能力

- code-task；
- design checklist；
- diagnosis case；
- 外部/人工评分；
- 角色 track 和模拟面试。

## 13. 验收关键点

- 空题库可启动且错误信息可解释；
- 导入 preview 不产生内容写入；
- apply 可重放、幂等、可审计；
- 同 ID 冲突不会覆盖已有题目；
- 删除不误删 Wiki、package 或 review history；
- 禁用题目不会进入新 session；
- 外部题目来源和 license 可追溯；
- question plugin 不能越权读 vault；
- public projection 不读取题目答案和 review state；
- 导入后不需要修改平台代码即可出现新题目。
