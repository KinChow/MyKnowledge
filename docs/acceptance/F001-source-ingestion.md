# F001 Source 导入与归档验收

- Feature：F001
- 相关规范：SRC、ARC、SEC
- 状态：Not Implemented

## AC-F001-001 网络来源成功归档

- Given：URL 可访问且正文非空；
- When：执行 Source Preview；
- Then：生成合法 Source、text 快照和 `file_sha256`；
- 失败时不变量：不能生成无来源或无 hash 的可发布对象；
- 自动化级别：Integration。

## AC-F001-002 来源不完整时拒绝

- Given：URL 不可访问且没有 local-file 或 personal-note 兜底；
- When：执行导入；
- Then：操作失败且不产生半成品；
- 自动化级别：Integration。

## AC-F001-003 raw 归档遵守 LFS 门禁

- Given：尝试写入 raw 快照；
- When：检查 `.gitattributes` 和 Git LFS；
- Then：规则生效才允许 raw，否则拒写或按契约降级 text-only，并记录原因；
- 自动化级别：Repository。
