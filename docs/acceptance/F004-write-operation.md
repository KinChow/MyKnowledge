# F004 写操作验收

- Feature：F004
- 相关规范：OPS、SEC
- 状态：Not Implemented

## AC-F004-001 未确认不得 Apply

- Given：存在 Preview 但没有用户确认；
- When：执行 Apply；
- Then：操作被拒绝且目标文件不变；
- 自动化级别：Integration。

## AC-F004-002 重复 Apply 幂等

- Given：同一 operation 已成功 Apply；
- When：重复执行 Apply；
- Then：返回原结果，不产生重复对象或损坏索引；
- 自动化级别：Integration。

## AC-F004-003 并发写入保持一致

- Given：两个写操作同时获取仓库写锁；
- When：并发执行；
- Then：只有一个持有锁，另一个可重试或明确失败，仓库不出现半成品；
- 自动化级别：Integration。
