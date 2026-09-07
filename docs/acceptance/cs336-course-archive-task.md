# CS336 课程归档任务验收

- 类型：F014 首个真实任务
- 状态：Partial（P1-P18 full transcript 已 Apply；P18 官方 lecture 映射仍 ambiguous；T6/T7 已验证）
- 日期：2026-09-07
- 所属 Feature：[F014 音视频与转录来源](./F014-media-sources.md)
- 任务设计：[CS336 课程归档演练](../technical-design/cs336-course-archive-task.md)

本文件不是新的 Feature 验收。它是 F014 的第一个真实数据集验收，所有场景通过后，F014 才能从 `Designed` 进入实现验收阶段；任务本身不能替代 unit/integration tests。

## TASK-CS336-001 独立任务环境

- Given：当前仓库存在用户改动和 LFS 文件；
- When：启动 CS336 任务；
- Then：下载、模型、临时转写、抽帧和报告都在独立 task workspace/环境中，canonical checkout 不产生半成品；
- 失败时不变量：不得把视频、模型、Cookie、signed URL 或临时缓存写进 `content/`、`archive/`、`audit/`；
- 自动化级别：Integration；
- 测试：待实现；
- 当前状态：验证通过；样本媒体、模型、转录、抽帧和报告均位于 `/tmp/cs336-task-20260907.VpgWY3/`。

## TASK-CS336-002 Bilibili inventory

- Given：用户提供 `BV1j9Kc6mEq4`，合集约定为中文 18 个、英文 18 个；
- When：执行 metadata-only flat inventory；
- Then：可复现地发现 36 个 P，保存每个 P 的稳定 URL、序号、标题、语言/可用性和 inventory hash；
- 失败时不变量：不能下载全量视频冒充 inventory，不能丢失英文 18 个，也不能把前 18 个误当成中文 18 个；
- 自动化级别：Integration；
- 测试：已完成一次真实 inventory：36 项、中文选中 18 项、英文排除 18 项，inventory hash 为 `sha256:366a72576d4fe1c166e4fc87e776e616bcc9f12222baa26c119dbc2d07e57614`；
- 当前状态：验证通过；18 项 full transcript Source 已 canonical Apply；无用的 bounded 关键帧已移除；P18 官方 lecture 映射仍需人工复核。

## TASK-CS336-003 中文 18 项筛选

- Given：inventory 为 36 项，其中中文 18 项、英文 18 项；
- When：按 `language=zh` 生成 scope manifest 并执行 Preview；
- Then：选中 18 个中文 P，英文 18 个保留为 `excluded`，每项有 `excluded_reason`；语言无法判定的条目阻断 Preview；
- 失败时不变量：不得按序号选前 18 个，不得把英文 P 处理成中文 transcript，也不得丢失被排除项的 inventory 记录；
- 自动化级别：Integration + Human spot check；
- 测试：已完成真实标题标记筛选；代码单测覆盖显式 `[中文]`/`[英文]` 标记和排除理由；
- 当前状态：验证通过；18 项 scope manifest 和 canonical Source 已生成，full transcript 覆盖 P1-P18；英文 P19-P36 仍仅保留 inventory 排除记录。

## TASK-CS336-004 官方课程资料 allowlist

- Given：`https://cs336.stanford.edu/` 提供当前 schedule 和官方资源链接；
- When：解析课程资料；
- Then：只收集官网直接资源和 `stanford-cs336` 官方仓库，记录 URL、页面/文件角色、commit/ref、文件 hash；
- 失败时不变量：不爬取 sponsor、pricing、第三方博客、学生提交或无界 Git 历史；
- 自动化级别：Integration；
- 测试：官网首页、lecture PDF、Assignment 1 PDF 的 allowlist/ref/file hash 已真实获取；
- 当前状态：部分完成，详见 `/tmp/cs336-task-20260907.VpgWY3/task-report.json`。

## TASK-CS336-005 官方映射优先于 P 序号

- Given：中文 18 个 Bilibili P 的序号和 Stanford schedule lecture 编号可能不一致；
- When：生成课程映射；
- Then：以官方 lecture/date/topic 为课程键，Bilibili P 仅作为媒体定位，并显式记录 `mapped`/`ambiguous`/`unmapped`；
- 失败时不变量：不能把 `p=1` 自动声明为官方 lecture 1；歧义项不能进入 evidence-ready；
- 自动化级别：Unit + Human review；
- 测试：已生成 `cs336-course-index` Source；P1-P17 主题映射，P18 保持 `ambiguous`；
- 当前状态：部分完成；P18 需要人工复核，不得把它自动声明为某个 official lecture。

## TASK-CS336-006 字幕/ASR 和术语 provenance

- Given：选定的中文视频可能有人工字幕、自动字幕或无字幕；
- When：生成 transcript；
- Then：保存原始字幕、canonical transcript、SRT/VTT/JSON、extractor/version/options/model hash，并标记字幕来源；
- 失败时不变量：`.vtt` 后缀不能证明人工字幕；ASR transcript 支撑的 claim 不能派生 `verified`；
- 自动化级别：Integration；
- 测试：待实现；
- 当前状态：部分完成；P1-P18 前 30 秒使用 OpenAI Whisper Turbo 真实跑通并记录模型 hash，P1-P18 已使用 whisper.cpp 完成 full transcript 并 Apply；ASR provenance 和媒体 hash 已记录。

## TASK-CS336-007 官方资料与视频证据关系

- Given：同一主题同时存在 Stanford lecture PDF 和 Bilibili transcript；
- When：建立 claim/evidence；
- Then：两个来源分别保留 provenance/independence_group，transcript 引用带 `media_fragment`，PDF 引用带文件/page/selector；
- 失败时不变量：不能把视频搬运源当成官方资料，也不能把同一转载链重复计为独立佐证；
- 自动化级别：Integration；
- 测试：待实现；
- 当前状态：部分完成；P1 transcript 已有 `media_fragment` Evidence，官方 PDF 已独立归档；跨来源 claim 关系尚未建立。

## TASK-CS336-008 关键帧和资料画面

- Given：视频包含课程标题、幻灯片、代码或公式画面；
- When：对选定片段抽帧；
- Then：生成 frame manifest、时间戳、图片 hash、抽取参数和可选 OCR；
- 失败时不变量：抽帧图片不能脱离视频 hash/时间戳单独作为事实证据；抽帧全量不能自动进入 public attachment；
- 自动化级别：Integration；
- 测试：待实现；
- 当前状态：按任务范围完成；原先的 54 个 bounded PNG 被人工判定为无用并已移除；F014 的关键帧 Preview/Apply 能力仍由独立测试覆盖，本课程不把无用帧作为归档资料。

## TASK-CS336-009 幂等、漂移和部分失败

- Given：重复执行、一个 P 下载失败、字幕 404 或官方文件 commit/hash 变化；
- When：重新执行相同任务；
- Then：相同输入幂等；变化项生成新 snapshot；失败项为 `partial` 并保留 next action；其它项不被回滚或掩盖；
- 失败时不变量：不能覆盖旧 snapshot、不能伪造全量完成；
- 自动化级别：Fault injection + Integration；
- 测试：待实现；
- 当前状态：验证通过；`/tmp/cs336-task-20260907.VpgWY3/drift-report.json` 覆盖 Source 幂等、SRT/媒体漂移、字幕缺失、官方文件 hash 变化和单项失败隔离；full batch report 另记录 P1-P18 均 applied。

## TASK-CS336-010 F014 准出

- Given：TASK-CS336-001 至 009 全部通过；
- When：生成任务报告；
- Then：报告包含 inventory/scope/resource/transcript/frame/evidence/hash/leak gate 的输入和结果，F014 才可进入整体验收判断；
- 失败时不变量：只完成视频下载、ASR 或 metadata inventory，不能标记 F014 `Accepted`；
- 自动化级别：Release review；
- 测试：待实现；
- 当前状态：部分通过；18 项 full transcript、T6/T7 和 canonical hash/leak 检查已完成，P18 官方映射与正式 release review 仍未闭合，因此 task report 保持 `partial`。
