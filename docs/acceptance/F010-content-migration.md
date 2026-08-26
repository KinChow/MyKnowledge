# F010 存量内容迁移和质量清理验收

- Feature：F010
- 相关规范：MIG、SRC、WIKI、EVD
- 状态：Not Implemented

## AC-F010-001 迁移清单与状态边界

- Given：现有 docs 内容；
- When：生成迁移清单；
- Then：每个文件有 source/wiki 目标、证据状态、目标 Vault、route、`body_sha256`、输入 tree hash、classifier/threshold 版本和 completed/pending 状态；
- 失败时不变量：没有来源的内容不得自动标记 published。
- 自动化级别：Repository/Integration（清单生成）；`content_verdict` 和最终发布为 Manual review。

## AC-F010-002 代表性样本迁移

- Given：包含网络 URL、local-file HTML/PDF、个人笔记、无来源和冲突来源的样本；
- When：执行迁移；
- Then：统一进入 Source → snapshot → evidence → Wiki 流程，local-file 记录 file hash 和 extractor 信息；
- 失败时不变量：不改写原 public 内容，不绕过验证门禁。
- 自动化级别：Integration/Manual review。

## AC-F010-003 链接与回滚

- Given：存在 unresolved internal Markdown links；
- When：生成 route map 和修复报告；
- Then：每条链接标记已修复/待人工处理，迁移失败可保留旧 public dist 和 canonical 内容；
- 失败时不变量：不得删除无法解释的旧对象。
- 自动化级别：Repository/Integration。
