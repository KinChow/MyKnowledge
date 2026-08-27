# F002 Wiki 契约验收

- Feature：F002
- 相关规范：WIKI
- 状态：Implemented（2026-08-26；58/58 测试通过，其中 F002 18 条模块级测试）
- 测试运行：`.venv/bin/python -m pytest tests/validation/ -v`

## AC-F002-001 合法知识 Wiki

- Given：Wiki 具备合法 front matter、正文模板和 Source 引用；
- When：执行 schema 校验；
- Then：校验通过并计算正确状态字段；
- 失败时不变量：未通过校验的对象不得发布；
- 自动化级别：Unit。
- 对应测试：`tests/validation/test_wiki_validator.py::WikiValidatorTests::test_legal_knowledge_wiki`
- 当前状态：通过。派生字段（evidence_state/validation_state/availability/strength/publishable/public_release）全部计算；hash 可复现（两次校验一致）。

## AC-F002-002 缺少来源时拒绝知识 Wiki

- Given：`kind: knowledge` Wiki 没有有效 Source；
- When：执行校验；
- Then：校验失败并给出字段级错误；
- 自动化级别：Unit。
- 对应测试：`tests/validation/test_wiki_rules.py::RulesTests::test_missing_source_rejected`
- 当前状态：通过。`source_missing`（sources 为空）与 `source_not_found`（引用了不存在的 source）字段级拒绝。

## AC-F002-003 派生字段和 hash 由工具计算

- Given：作者手写 `vault_id`、`content_sha256`、`semantic_sha256`、`evidence_sha256`、`validation_state` 或 `public_publishable`；
- When：执行 schema/preview 校验；
- Then：拒绝不可信的派生字段或以 canonical 计算结果覆盖并报告差异；正文、语义字段和 evidence 的 hash 结果可复现；
- 失败时不变量：不能让手写状态或 hash 使未验证对象进入 published/projection；
- 自动化级别：Unit/Integration。
- 对应测试：`tests/validation/test_wiki_schema.py::SchemaTests::test_derived_fields_rejected`（7 个字段逐字段断言）、`tests/validation/test_wiki_validator.py`（hash 可复现）
- 当前状态：通过。`FORBIDDEN_DERIVED_FIELDS`（15 个字段）先于 schema 校验，返回 `derived_field_mismatch`；`content_sha256`（canonical_body）与 `evidence_sha256`（解析后 evidence 含 resolved_object_ref）由工具计算。

## AC-F002-004 状态轴与合法组合

- Given：Wiki 分别处于 planned、draft、review、published、deprecated，并组合 evidence/validation/availability/publication 字段；
- When：执行确定性校验；
- Then：合法组合通过，非法组合逐字段拒绝；`availability: unavailable` 不被写成 `evidence_state: missing`，`validation_state: not_run` 不被写成 `pass`，`public_release` 默认 false；
- 失败时不变量：不能通过修改单一 status 绕过 evidence、人工审计确认或 Vault 门禁；`planned` 不能直接跳到 `published`；
- 自动化级别：Unit。
- 对应测试：`tests/validation/test_wiki_rules.py::RulesTests::test_status_axis_combinations`、`tests/validation/test_wiki_derived.py::DerivedTests::test_snapshot_drift_derives_stale`、`tests/validation/test_wiki_derived.py::DerivedTests::test_validation_report_drives_states`
- 当前状态：通过。planned 五字段例外（JSON Schema if/then + domain rule `planned_with_content`）；published+scope none → `published_scope_none`；snapshot 漂移 → `evidence_state: stale`；validation report 驱动 conflicting/partial/corroborated/verified；`public_release` 恒 false（F002 阶段）。

## AC-F002-005 owner Vault 内引用解析

- Given：两个 private Vault 存在相同 `source_id`，Wiki 位于其中一个 Vault；
- When：解析 `sources`/evidence targets 并生成 object ref；
- Then：默认只解析 Wiki owner Vault 内的 source，API/报告返回完整 `(vault_id, object_type, object_id)`；显式跨 Vault target 被拒绝并报告 `cross_vault_reference`；
- 失败时不变量：不能按 manifest 顺序选择对象或泄漏另一个 Vault 的 metadata；
- 自动化级别：Unit/Integration。
- 对应测试：`tests/validation/test_wiki_resolution.py::ResolutionTests::test_owner_vault_reference_resolution`
- 当前状态：通过。target 解析为 `{vault_id: public, object_type: source, object_id}` 并写入 evidence hash；显式 `vault_id: private` → `cross_vault_reference`。

## AC-F002-006 派生字段与发布组合拒绝

- Given：Wiki 手写 `public_release: true`、`public_publishable`、`private_publishable`，或组合 `status: published + publication_scope: none`、`public_release: true + owner != public`；
- When：执行 schema/preview 校验；
- Then：返回字段级 `derived_field_mismatch`/`invalid_public_release`，不改变 canonical 文件和 projection；
- 失败时不变量：任何手写派生字段、发布开关或不合法组合都不能绕过 durable validation、confirmation 和 Vault 门禁；
- 自动化级别：Unit/Integration/Security。
- 对应测试：`tests/validation/test_wiki_rules.py::RulesTests::test_publication_combo_rejected`、`tests/validation/test_wiki_rules.py`（published 组合）、`tests/validation/test_wiki_derived.py::DerivedTests::test_private_publishable_with_confirmation`
- 当前状态：通过。手写发布字段 → `derived_field_mismatch`；`private_publishable` 仅在 published+scope private+审计确认 hash 匹配时派生为 true。

## AC-F002-007 可执行 schema validator 与 registry 分离

- Given：Source/Wiki/operation/event 输入分别包含缺失必填字段、未知字段、错误类型和非法跨字段组合；`config/schemas.yaml` 只提供版本/字段 registry；
- When：调用领域 schema validator；
- Then：validator 使用版本化的可执行 JSON Schema（及明确的跨字段规则）返回字段级错误，拒绝未知字段和错误 schema version；`validate:config` 仅证明 registry/policy 一致，不能被当作领域对象已验证；
- 失败时不变量：仅修改 registry 或手写派生字段不能使对象进入 `published`/projection；schema validator 的版本、输入 hash 和结果必须进入 operation/validation 诊断；
- 自动化级别：Unit/Integration。
- 对应测试：`tests/validation/test_wiki_schema.py::SchemaTests::test_executable_schema_rejects_unknown_and_wrong_version`
- 当前状态：通过。`config/json-schema/wiki-v1.json`（JSON Schema 2020-12，additionalProperties: false）为可执行 schema；未知字段 → `unknown_field`、错误 version → `wrong_schema_version`、类型错误 → `schema_invalid`（含 keyword）；jsonschema 库（来源：python-jsonschema/jsonschema，MIT）执行。

---

## 验收记录

- 测试：58/58 通过（2026-08-26，Python 3.14.2 / pytest 8.4.2，F001 37 + F002 17 模块级 + 结构守卫 3 + 崩溃注入 1）
- F002 测试按模块组织于 `tests/validation/`（fixtures 共享于 `tests/wiki_fixtures.py`）
- 人工验证：`python -m tools.cli validate --root <root> <wiki>` CLI 冒烟——合法 wiki 输出 valid: true + 全部派生字段与 hash
- 复核人：zhouzijian01
- 未决项（不影响 Implemented，阻却 Accepted）：
  - `cross_vault_reference` 的完整语义依赖 private Vault 挂载（F011），当前仅覆盖显式 target.vault_id 拒绝；
  - conflicting/partial/corroborated/verified 由 validation report（F003 定义契约）驱动，F002 定义了消费字段（verdict/claim_verdicts/corroborated）但报告生成属于 F003；
- `public_publishable` 的 public-safe confirmation event 判定（release/public-confirmations/）随 F007 发布 authority 落地。

## Front matter 重复键增量证据（2026-08-27）

- `tests/test_front_matter.py::FrontMatterTests::test_duplicate_yaml_keys_are_rejected` 验证 YAML front matter 的重复 key 返回 `front_matter_invalid_yaml`，不会采用后值覆盖前值；该门禁复用 PyYAML SafeLoader 的安全解析边界，保护 schema、状态和保密字段的一致性。

## Evidence ID 唯一性增量证据（2026-08-27）

- `tests/validation/test_wiki_resolution.py::ResolutionTests::test_duplicate_evidence_id_is_rejected` 验证同一 Source 内重复 `evidence_id` 返回 `duplicate_evidence_id`，不会按最后一条静默覆盖。

## F002 专项验收报告（2026-08-27）

- 专项命令：`.venv/bin/python -m pytest -q tests/validation/test_wiki_schema.py tests/validation/test_wiki_rules.py tests/validation/test_wiki_derived.py tests/validation/test_wiki_resolution.py tests/test_front_matter.py`
- 结果：21 passed，覆盖可执行 JSON Schema、未知字段/版本/类型、派生字段拒绝、status/evidence/availability 组合、owner-scoped 引用和重复 evidence ID。
- 成熟方案边界：直接复用 jsonschema 的版本化校验与 additionalProperties 门禁；状态组合由 MyKnowledge 离线 domain rules 保留，不把 Pydantic/transitions/XState 引入 canonical 数据或发布判据。
- 边界：F002 专项证据证明 schema 与状态契约可执行；F003 的 LLM/corroboration 审计和 F007 public confirmation 仍是独立门禁，当前 Feature 仍为 `Implemented（部分）`。
