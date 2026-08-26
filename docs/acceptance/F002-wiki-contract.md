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

## AC-F002-003 派生字段和 hash 由工具计算

- Given：作者手写 `vault_id`、`content_sha256`、`semantic_sha256`、`evidence_sha256`、`validation_state` 或 `public_publishable`；
- When：执行 schema/preview 校验；
- Then：拒绝不可信的派生字段或以 canonical 计算结果覆盖并报告差异；正文、语义字段和 evidence 的 hash 结果可复现；
- 失败时不变量：不能让手写状态或 hash 使未验证对象进入 published/projection；
- 自动化级别：Unit/Integration。

## AC-F002-004 状态轴与合法组合

- Given：Wiki 分别处于 planned、draft、review、published、deprecated，并组合 evidence/validation/availability/publication 字段；
- When：执行确定性校验；
- Then：合法组合通过，非法组合逐字段拒绝；`availability: unavailable` 不被写成 `evidence_state: missing`，`validation_state: not_run` 不被写成 `pass`，`public_release` 默认 false；
- 失败时不变量：不能通过修改单一 status 绕过 evidence、人工审计确认或 Vault 门禁；`planned` 不能直接跳到 `published`；
- 自动化级别：Unit。

## AC-F002-005 owner Vault 内引用解析

- Given：两个 private Vault 存在相同 `source_id`，Wiki 位于其中一个 Vault；
- When：解析 `sources`/evidence targets 并生成 object ref；
- Then：默认只解析 Wiki owner Vault 内的 source，API/报告返回完整 `(vault_id, object_type, object_id)`；显式跨 Vault target 被拒绝并报告 `cross_vault_reference`；
- 失败时不变量：不能按 manifest 顺序选择对象或泄漏另一个 Vault 的 metadata；
- 自动化级别：Unit/Integration。

## AC-F002-006 派生字段与发布组合拒绝

- Given：Wiki 手写 `public_release: true`、`public_publishable`、`private_publishable`，或组合 `status: published + publication_scope: none`、`public_release: true + owner != public`；
- When：执行 schema/preview 校验；
- Then：返回字段级 `derived_field_mismatch`/`invalid_public_release`，不改变 canonical 文件和 projection；
- 失败时不变量：任何手写派生字段、发布开关或不合法组合都不能绕过 durable validation、confirmation 和 Vault 门禁；
- 自动化级别：Unit/Integration/Security。

## AC-F002-007 可执行 schema validator 与 registry 分离

- Given：Source/Wiki/operation/event 输入分别包含缺失必填字段、未知字段、错误类型和非法跨字段组合；`config/schemas.yaml` 只提供版本/字段 registry；
- When：调用领域 schema validator；
- Then：validator 使用版本化的可执行 JSON Schema（及明确的跨字段规则）返回字段级错误，拒绝未知字段和错误 schema version；`validate:config` 仅证明 registry/policy 一致，不能被当作领域对象已验证；
- 失败时不变量：仅修改 registry 或手写派生字段不能使对象进入 `published`/projection；schema validator 的版本、输入 hash 和结果必须进入 operation/validation 诊断；
- 自动化级别：Unit/Integration。
