# F003 Claim/Evidence 验收

- Feature：F003
- 相关规范：EVD、VAL
- 状态：Not Implemented

## AC-F003-001 Claim 显式绑定 Evidence

- Given：知识型 Wiki 包含可验证 Claim；
- When：执行证据校验；
- Then：每个 Claim 都有有效 Evidence 和 locator；
- 失败时不变量：缺失映射不得进入 validated；
- 自动化级别：Integration。

## AC-F003-002 supporting_quote 逐字匹配

- Given：quote 位于或不位于指定 locator；
- When：执行共享规范化匹配；
- Then：只有 locator 内、达到最小长度且逐字匹配的 quote 才通过；
- 自动化级别：Unit。

## AC-F003-003 验证报告绑定 hash

- Given：正文、语义字段或 Evidence 发生变化；
- When：复用旧验证报告；
- Then：报告失效，Wiki 不得继续以旧报告发布；
- 自动化级别：Integration。
