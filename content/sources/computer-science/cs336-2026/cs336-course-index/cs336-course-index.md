---
archive_policy: text-only
attachments:
- filename: cs336-course-index.txt
  kind: document
  media_type: text/markdown
  role: original
  sha256: sha256:5bf2bad9f2ece940db7744b9a5cce475b4a32cf0bc9008c67ebacc6fb4daf307
confidentiality: public
domain: computer-science
extractor: utf8/1
id: cs336-course-index
local:
  file_sha256: sha256:5bf2bad9f2ece940db7744b9a5cce475b4a32cf0bc9008c67ebacc6fb4daf307
  path_ref: local-sidecar:public/cs336-course-index
media_type: text/markdown
origin: external
raw_ref:
  path: archive/raw/5bf2bad9f2ece940db7744b9a5cce475b4a32cf0bc9008c67ebacc6fb4daf307.txt
  sha256: sha256:5bf2bad9f2ece940db7744b9a5cce475b4a32cf0bc9008c67ebacc6fb4daf307
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:5bf2bad9f2ece940db7744b9a5cce475b4a32cf0bc9008c67ebacc6fb4daf307
source_type: local-file
vault_id: public
---
# CS336 课程归档总览

这是 Stanford CS336: Language Modeling from Scratch 的归档入口。课程视频来自
Bilibili 合集 `BV1j9Kc6mEq4`，本次只归档标题标记为中文的 P1-P18；英文 P19-P36
只保留在 metadata inventory 中。每个视频正文仍保存在独立 Source，便于按视频、
时间戳和 snapshot hash 检索。

## 归档状态

- 视频范围：18/18 中文分 P 已完成 full transcript，并已通过 Preview/Apply 写入 canonical Source。
- 转录引擎：`whisper.cpp`，中文，模型 `ggml-model.bin`；每个 Source 记录模型 hash、引擎版本和媒体输入 hash。
- 图片范围：已删除此前无用的 `media/frames`，视频 Source 只保留 full transcript 和时间戳正文。
- 归档策略：`transcript-only`；原视频和 ASR 模型不进入仓库。
- 证据状态：P1 已有 `media_fragment` 示例；ASR 转录默认强度上限为 `attested`，未经人工逐字校对不升级为 `verified`。
- 任务状态：视频归档、T6 重跑/漂移/失败隔离、T7 public leak gate 已验证；P18 官方 guest lecture 具体对应人仍为 `ambiguous`。

## 中文视频 Sources

| P | 中文标题 | 课程映射 | Source |
| ---: | --- | --- | --- |
| 1 | 从零构建大语言模型，手把手教你理解 AI 核心 | Lecture 1: Overview, tokenization | [cs336-p01](../cs336-p01/cs336-p01.md) |
| 2 | 手把手教你从零训练大模型，PyTorch+einops 实战 | Lecture 2: PyTorch (einops) | [cs336-p02](../cs336-p02/cs336-p02.md) |
| 3 | 架构与超参数，你不想知道但又必须知道的一切 | Lecture 3: Architectures | [cs336-p03](../cs336-p03/cs336-p03.md) |
| 4 | 注意力机制替代方案与混合专家模型，突破长上下文瓶颈 | Lecture 4: Attention alternatives | [cs336-p04](../cs336-p04/cs336-p04.md) |
| 5 | GPU/TPU 底层原理与优化，从零理解 AI 算力核心 | Lecture 5: GPUs, TPUs | [cs336-p05](../cs336-p05/cs336-p05.md) |
| 6 | 手把手教你写 Triton 内核，GPU 编程从入门到实战 | Lecture 6: Kernels, Triton, XLA | [cs336-p06](../cs336-p06/cs336-p06.md) |
| 7 | 多 GPU 并行训练实战，从单卡到千卡集群全解析 | Lecture 7: Parallelism | [cs336-p07](../cs336-p07/cs336-p07.md) |
| 8 | 大模型训练如何实现 4D 并行？从数据到专家并行全解析 | Lecture 8: Parallelism | [cs336-p08](../cs336-p08/cs336-p08.md) |
| 9 | 缩放定律详解：从零理解大模型训练成本与性能预测 | Lecture 9: Scaling Laws | [cs336-p09](../cs336-p09/cs336-p09.md) |
| 10 | 大模型部署必学，从 KV Cache 到投机解码 | Lecture 10: Inference | [cs336-p10](../cs336-p10/cs336-p10.md) |
| 11 | 大模型扩展定律全揭秘，从理论到开源实战 | Lecture 11: Scaling Laws | [cs336-p11](../cs336-p11/cs336-p11.md) |
| 12 | 评估决定 AI 模型上限，90% 的人都忽略了 | Lecture 12: Evaluation | [cs336-p12](../cs336-p12/cs336-p12.md) |
| 13 | 语言模型的数据才是核心竞争力，Llama 3 论文都不敢公开的秘密 | Lecture 13: Data, sources and datasets | [cs336-p13](../cs336-p13/cs336-p13.md) |
| 14 | 大模型数据处理的完整流水线，过滤去重混合全讲透 | Lecture 14: Data processing | [cs336-p14](../cs336-p14/cs336-p14.md) |
| 15 | 从 GPT-3 到 ChatGPT 的后训练秘密 | Lecture 15: Mid/post-training | [cs336-p15](../cs336-p15/cs336-p15.md) |
| 16 | 后训练：RLVR 让模型自己学会推理 | Lecture 16: Post-training, RLVR | [cs336-p16](../cs336-p16/cs336-p16.md) |
| 17 | 多模态对齐，从语言模型走向全模态 AI | Lecture 17: Alignment, multimodality | [cs336-p17](../cs336-p17/cs336-p17.md) |
| 18 | 大模型推理部署，从电力到智能的工业革命 | Guest lecture / inference: ambiguous | [cs336-p18](../cs336-p18/cs336-p18.md) |

## Official Stanford Sources

- [Stanford CS336 course site](https://cs336.stanford.edu/)
- [official Lecture 3 PDF](../official-materials/lectures/lecture_03.pdf)
- [official Assignment 1 PDF](../official-materials/assignments/assignment-01/cs336_assignment1_basics.pdf)
- 官方 schedule、资源 URL、commit/ref 和文件 hash 记录在独立 task workspace 的
  `resources/official-resources.json`；官方资料与搬运视频保持不同来源角色。

## Reproducibility

- Bilibili inventory：36 个 P，中文选中 18 个，英文排除 18 个；inventory hash：
  `sha256:366a72576d4fe1c166e4fc87e776e616bcc9f12222baa26c119dbc2d07e57614`。
- Full batch report：独立 task workspace 中的 `video-batch-report.json`。
- 独立验证环境：独立 Python/uv 环境（具体本机路径不写入 Source）。
- 本总览不复制视频 transcript；请通过上表进入每个独立 Source 查看全文。

## Official materials

全部已下载的 Stanford 2026 课件与资料位于 [official-materials](../official-materials/README.txt)：

- `lectures/`：Lecture 1-17 的 Python/PDF 课件及必要辅助文件。
- `assignments/`：Assignment 1-5 的 README、PDF、Assignment 3 示例 notebook，以及 Assignment 5 safety supplement。
- `course-home/index.html`：官网 schedule 离线副本。
- `official-materials/SHA256SUMS`：每个文件的 SHA-256 和固定 commit 记录入口。
