# ADR-0003：原文快照与 Git LFS

- 状态：Accepted
- 日期：2026-08-25
- 相关规范：ARC、SEC
- 相关 Feature：F001、F012

## 决策

网络 Source 保存内容寻址的本地文本快照；snapshot 的逻辑内容是未压缩 canonical UTF-8 文本，物理 `archive/text` blob 可使用固定参数 zstd 存储，恢复/读取时必须解压并重新校验 snapshot hash。必要时保存 raw 快照并使用 zstd。只有 `archive/raw/**` 这类不可有效 diff 的大文件使用 Git LFS。Markdown、YAML、JSON 和设计文档使用普通 Git。

## 后果

原文可离线复核，设计文档可正常 diff；raw 写入前必须检查 LFS 规则已生效。LFS 未配置时按规范拒写 raw 或降级为 text-only。

## 重新评估条件

归档规模、托管限制或恢复策略发生变化时重新评估。
