# ADR-0006：Preview/Apply 写协议

- 状态：Superseded（被 ADR-0019 取代，2026-09-15）
- 日期：2026-08-25
- 相关规范：OPS
- 相关 Feature：F004
- 取代说明：Preview/Apply 及其配套的 operation 状态机、per-vault 锁、TTL、commit-intent 已从代码中删除（`tools/write_operation.py` / `operation_store.py` / `vault_lock.py` 与其 CLI/API 入口、测试，2026-09-15）。写入改为一次落盘，审批由 `git commit` 承担（ADR-0019）。本 ADR 保留作为历史取舍记录。

## 决策

所有写入必须经过 Preview、用户确认和 Apply。Apply 使用幂等键、目标 Vault 的排他锁（多 Vault 按稳定 `vault_id` 顺序获取）、fencing token 和原子落盘；rename、move、废弃和删除是受控的一等操作。锁恢复必须显式执行并留下 durable audit record，不能按超时自动抢占。

## 后果

写入更可审计，Agent 不能绕过门禁直接修改文件；实现需要处理重试、中断、陈旧锁恢复和 token 失效。跨 Vault 操作不承诺分布式事务，只承诺有序锁、部分成功记录和可补偿恢复。

## 重新评估条件

出现新的写入客户端或需要跨仓库事务时重新评估。
