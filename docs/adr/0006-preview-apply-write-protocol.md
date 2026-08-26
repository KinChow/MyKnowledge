# ADR-0006：Preview/Apply 写协议

- 状态：Accepted
- 日期：2026-08-25
- 相关规范：OPS
- 相关 Feature：F004

## 决策

所有写入必须经过 Preview、用户确认和 Apply。Apply 使用幂等键、目标 Vault 的排他锁（多 Vault 按稳定 `vault_id` 顺序获取）、fencing token 和原子落盘；rename、move、废弃和删除是受控的一等操作。锁恢复必须显式执行并留下 durable audit record，不能按超时自动抢占。

## 后果

写入更可审计，Agent 不能绕过门禁直接修改文件；实现需要处理重试、中断、陈旧锁恢复和 token 失效。跨 Vault 操作不承诺分布式事务，只承诺有序锁、部分成功记录和可补偿恢复。

## 重新评估条件

出现新的写入客户端或需要跨仓库事务时重新评估。
