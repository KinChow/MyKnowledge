# F002 Wiki 契约验收

- Feature：F002
- 相关规范：WIKI
- 状态：Not Implemented

## AC-F002-001 合法知识 Wiki

- Given：Wiki 具备合法 front matter、正文模板和 Source 引用；
- When：执行 schema 校验；
- Then：校验通过并计算正确状态字段；
- 失败时不变量：未通过校验的对象不得发布；
- 自动化级别：Unit。

## AC-F002-002 缺少来源时拒绝知识 Wiki

- Given：`kind: knowledge` Wiki 没有有效 Source；
- When：执行校验；
- Then：校验失败并给出字段级错误；
- 自动化级别：Unit。
