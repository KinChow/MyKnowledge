# F014 首个真实任务：CS336 课程归档演练

- 类型：Feature task / end-to-end rehearsal
- 所属 Feature：F014 音视频与视频来源
- 状态：Partial（P1-P18 full transcript 已 Apply；P18 官方 lecture 映射仍 ambiguous；T6/T7 已验证，不新增 Feature）
- 日期：2026-09-07
- 任务验收：[CS336 课程归档任务验收](../acceptance/cs336-course-archive-task.md)
- 通用设计：[音视频与视频来源](./media-sources.md)

## 任务目标

使用真实的 Bilibili CS336 合集中的 18 个中文分 P 和 Stanford 官方 CS336 资料，验证 F014 是否能完成：来源发现、语言筛选、平台字幕/ASR、关键帧、官方资料归档、版本 hash、Evidence 锚定、失败恢复和 public/private 隔离。

这不是新的 Feature，也不是立即导入内容的授权。它是 F014 完成后的第一个真实任务和准出样本；任务执行前必须通过 Preview 和中文语言范围确认。

## 输入来源

平台视频：

```text
https://www.bilibili.com/video/BV1j9Kc6mEq4/
```

官方课程入口：

```text
https://cs336.stanford.edu/
```

官方资源范围由官网当前 schedule 解析得到，优先包括：

- 课程首页和 schedule；
- 官网直接列出的 lecture page/PDF；
- `stanford-cs336/lectures` 指定 commit/ref 下的 lecture 文件；
- Assignment 1–5 的 README、PDF preview、指定 commit/ref 和必要的源码入口。

以下内容默认只登记链接或 `skip_reason`，不自动下载：赞助商/云 GPU pricing、第三方博客、学生提交、无界 Git 历史、官网未明确关联的外部参考。

## 关键发现与范围门

当前平台 inventory 已发现 Bilibili 合集包含 **36 个分 P：中文 18 个、英文 18 个**。本任务只归档中文 18 个；英文 18 个必须保留在 inventory 中，并标记 `excluded_reason: language_not_selected`，不能静默丢弃。

任务必须先产生：

```yaml
inventory_item_count: 36
selected_item_count: 18
excluded_item_count: 18
selection_status: confirmed
selection_basis: language=zh
selected_language: zh
```

筛选与确认规则：

- 所有 36 个 P 先保存 metadata inventory；
- 按平台语言字段、标题/字幕语言和必要的人工抽查确定中文 18 个；
- 不得按 P 序号选前 18 个；
- 英文 18 个保留 inventory 和排除理由，不进入本次 transcript/raw/frame 处理；
- 语言无法判定的条目进入 `needs_review`，不能自动归入中文集合。

scope manifest 必须逐项列出中文 P、标题、语言判定、官方 lecture 映射和选择理由；不得把 36 个 P 宣称为 18 个官方 lecture。

## 中文 18 个视频 URL

以下列表来自 2026-09-07 的 Bilibili metadata inventory。P1–P18 的平台标题均带 `[中文]` 标记，因此本任务只处理这些 URL；P19–P36 为英文视频，不在本任务 URL 清单中展开。

本次真实 inventory 已验证：`inventory_item_count: 36`、`selected_item_count: 18`、`selection_language: zh`，inventory hash 为 `sha256:366a72576d4fe1c166e4fc87e776e616bcc9f12222baa26c119dbc2d07e57614`。该 hash 只证明本次 metadata inventory 输入，不代表视频、字幕或转录稿已经归档。

| P | 中文课程标题 | URL |
| ---: | --- | --- |
| 1 | 从零构建大语言模型，手把手教你理解 AI 核心 | [Bilibili P1](https://www.bilibili.com/video/BV1j9Kc6mEq4?p=1) |
| 2 | 手把手教你从零训练大模型，PyTorch+einops 实战 | [Bilibili P2](https://www.bilibili.com/video/BV1j9Kc6mEq4?p=2) |
| 3 | 架构与超参数，你不想知道但又必须知道的一切 | [Bilibili P3](https://www.bilibili.com/video/BV1j9Kc6mEq4?p=3) |
| 4 | 注意力机制替代方案与混合专家模型，突破长上下文瓶颈 | [Bilibili P4](https://www.bilibili.com/video/BV1j9Kc6mEq4?p=4) |
| 5 | GPU/TPU 底层原理与优化，从零理解 AI 算力核心 | [Bilibili P5](https://www.bilibili.com/video/BV1j9Kc6mEq4?p=5) |
| 6 | 手把手教你写 Triton 内核，GPU 编程从入门到实战 | [Bilibili P6](https://www.bilibili.com/video/BV1j9Kc6mEq4?p=6) |
| 7 | 多 GPU 并行训练实战，从单卡到千卡集群全解析 | [Bilibili P7](https://www.bilibili.com/video/BV1j9Kc6mEq4?p=7) |
| 8 | 大模型训练如何实现 4D 并行？从数据到专家并行全解析 | [Bilibili P8](https://www.bilibili.com/video/BV1j9Kc6mEq4?p=8) |
| 9 | 缩放定律详解：从零理解大模型训练成本与性能预测 | [Bilibili P9](https://www.bilibili.com/video/BV1j9Kc6mEq4?p=9) |
| 10 | 大模型部署必学，从 KV Cache 到投机解码 | [Bilibili P10](https://www.bilibili.com/video/BV1j9Kc6mEq4?p=10) |
| 11 | 大模型扩展定律全揭秘，从理论到开源实战 | [Bilibili P11](https://www.bilibili.com/video/BV1j9Kc6mEq4?p=11) |
| 12 | 评估决定 AI 模型上限，90% 的人都忽略了 | [Bilibili P12](https://www.bilibili.com/video/BV1j9Kc6mEq4?p=12) |
| 13 | 语言模型的数据才是核心竞争力，Llama 3 论文都不敢公开的秘密 | [Bilibili P13](https://www.bilibili.com/video/BV1j9Kc6mEq4?p=13) |
| 14 | 大模型数据处理的完整流水线，过滤去重混合全讲透 | [Bilibili P14](https://www.bilibili.com/video/BV1j9Kc6mEq4?p=14) |
| 15 | 从 GPT-3 到 ChatGPT 的后训练秘密 | [Bilibili P15](https://www.bilibili.com/video/BV1j9Kc6mEq4?p=15) |
| 16 | 后训练：RLVR 让模型自己学会推理 | [Bilibili P16](https://www.bilibili.com/video/BV1j9Kc6mEq4?p=16) |
| 17 | 多模态对齐，从语言模型走向全模态 AI | [Bilibili P17](https://www.bilibili.com/video/BV1j9Kc6mEq4?p=17) |
| 18 | 大模型推理部署，从电力到智能的工业革命 | [Bilibili P18](https://www.bilibili.com/video/BV1j9Kc6mEq4?p=18) |

URL 只作为任务输入和平台定位；后续实现仍需在 Preview 阶段重新读取 metadata、resolved URL、时长和 hash，不能把本表标题当作证据正文。

## 任务产物

```text
<task-output>/
├── inventory.json                 # 36 个 P 的 metadata inventory
├── scope-manifest.yaml            # language=zh 的 18 项选择与英文排除记录
├── official-resources.json        # 官网 allowlist + commit/file hashes
├── source-preview.json            # Preview operation/hash/warnings
├── transcript/                     # 选定视频的 raw + canonical text
├── frames/                        # 选定视频的 manifest/contact sheet/frames
├── evidence-preview.json          # quote/position/media_fragment
├── drift-report.json              # 重跑时的变化
└── task-report.json               # 阶段状态、测试和未决项
```

这些是 task workspace 产物，不得直接落到 MyKnowledge canonical 目录。通过 Preview、人工确认和 Apply 后，才写入 Source、archive manifest 和 audit records。

2026-09-07 task workspace：`/tmp/cs336-task-20260907.VpgWY3/`。该 workspace 保存
P1-P18 的早期 30 秒 bounded 样本和 Whisper Turbo 产物；full 批次位于
`/tmp/cs336-whispercpp-full-task.LKSQww/`，使用 whisper.cpp Metal，P1-P18
均已完成。18 项 full transcript 已分别通过 Preview/Apply 写入 canonical Source，
此前抽取但经人工判定无用的 `media/frames` 已从 Source 移除；P18 官方 lecture
映射仍保持 `ambiguous`，未盲目建立关系。P1 的
`media_fragment` Evidence 和官方 lecture/Assignment PDF Source snapshot 已 Apply。
任务报告仍标记 `status: partial`：视频 full transcript 已完成，但 P18 官方映射
和正式 release review 仍未闭合。

## 阶段与门禁

### T0：环境和安全边界

- 使用独立临时目录、独立 Python/uv 环境；
- 记录 `yt-dlp`、FFmpeg/ffprobe、ASR、模型和参数版本；
- 检查输出目录、磁盘、LFS/raw policy 和 private/public vault；
- 禁止 Cookie/Authorization/临时签名 URL 进入 artifact 或日志。

### T1：平台 inventory

- 对 Bilibili URL 使用 flat playlist/metadata 模式；
- 记录 36 个 P 的稳定 URL 和平台序号；
- 不下载完整视频；
- inventory hash 写入 task report。

### T2：官方资料 inventory

- 抓取官网首页和 schedule；
- 解析官网直接链接的 lecture/assignment 资源；
- 对 GitHub 文件 pin commit/ref 并记录文件 hash；
- 外部链接按 allowlist 分类，未收集项记录原因。

### T3：人工 scope confirmation

- 确认中文筛选结果为 18 个；
- 确认是否保存完整 assignment repo 还是 PDF/README/commit；
- 确认原视频采用 `transcript-only`，只对选定视频做音频/片段处理；
- 生成 hash-bound confirmation event。

### T4：文字和媒体处理

- 字幕优先：人工字幕、自动字幕、ASR 按 provenance 区分；
- 选定无字幕视频时，下载受限音频/片段并运行 ASR；
- 生成 canonical transcript、SRT/VTT/JSON；
- 按需抽取关键帧和 OCR，记录 frame timestamp、hash 和生成参数。

### T5：Source/Evidence 写入

- collection Source 保存课程目录、官方资料关系和阅读笔记；
- transcript 进入不可变 text snapshot；
- Evidence 使用 TextQuote/TextPosition selector，`media_fragment` 只做跳转；
- ASR evidence strength 最高 `attested`，未经人工逐字校对不得 `verified`。

### T6：重跑与失败恢复

- 重跑同一 scope 必须幂等；
- 模拟一个 P 失败、一个字幕 404、一个官方文件 hash 变化；
- 旧 snapshot 保留，新 snapshot append；
- 单项失败不能掩盖其它成功项，也不能报告全量成功。

### T7：发布隔离

- 完整视频、完整 ASR transcript、临时签名 URL、private path 不进入 public projection；
- 只发布明确 allowlisted 的 public-safe metadata/附件；
- leak gate 失败时保留旧 projection。

## 完成定义

任务通过必须同时满足：

1. 36 个 Bilibili P inventory 可复现，18 个中文 P 被选中且 18 个英文 P 有排除记录；
2. 官网 schedule 和官方资源 allowlist 可复现，至少一份 lecture/assignment 资料有 commit/file hash；
3. 至少一条真实视频完成字幕或 ASR transcript snapshot；
4. 至少一个 transcript 片段完成 Evidence selector + `media_fragment` 回放；
5. 关键帧能力由 F014 单测覆盖；本次 CS336 任务不保留无用的 bounded 帧；
6. 幂等、漂移、单项失败、raw/LFS 降级和 public leak gate 场景全部有报告；
7. MyKnowledge 仓库只接收经过 Preview/人工确认/Apply 的 canonical 产物，临时媒体和模型留在 task workspace/private storage。

任务失败时的结果必须保留为 `partial`/`blocked` 报告，不得把“能下载视频”或“ASR 有输出”称为 F014 已验收。
