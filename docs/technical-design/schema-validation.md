# 可执行 Schema Validator 实现设计

- 状态：Draft
- 相关 Feature：F002、F003、F004、F007
- 相关规范：WIKI、EVD、OPS、SEC
- 相关验收：[F002](../acceptance/F002-wiki-contract.md)、[F003](../acceptance/F003-evidence-validation.md)

## 为什么需要单独的 validator

`config/schemas.yaml` 当前是跨模块共享的 schema/version/字段 registry，不是可直接执行的 JSON Schema。`npm run validate:config` 只能证明 registry、policy、vocabulary 之间没有明显漂移，不能证明一个 Source、Wiki、operation 或 confirmation event 符合领域对象契约。把 registry 校验通过误报成领域对象已校验会让手写字段和未知字段绕过写入门。

## 推荐实现

使用成熟的 JSON Schema 2020-12 validator（Node 侧优先 Ajv 8 + `ajv-formats`），把可执行 schema 放在版本化目录：

```text
config/
├── schemas.yaml                 # 名称、版本、枚举和跨模块 registry
└── json-schema/
    ├── source-v1.json
    ├── wiki-v1.json
    ├── evidence-item-v1.json
    ├── operation-v1.json
    ├── public-projection-v1.json
    ├── confirmation-v1.json
    └── query-result-v1.json
```

每个 JSON Schema 使用 `$id` 与 `schemas.yaml.objects.*` 完全对应，设置 `additionalProperties: false`，对 hash、ObjectRef、route、Vault ID、enum、日期和大小做类型/格式约束。共享定义放在同版本 `$defs`，禁止通过网络解析 `$ref`；validator 启动时只加载仓库内、固定 hash 的 schema 文件。

## 跨字段规则

JSON Schema 负责结构和局部约束；以下规则由同一 validator 的 domain rule layer 执行，并返回稳定的 `code/path/keyword/schema_version`：

- Source `source_type: local-file` 必须有 `retrieval.acquisition: local-file`、file hash、`local-sidecar:` path ref 和 snapshot hash；
- Wiki 的 owner/confidentiality、source ObjectRef、状态轴、evidence/validation/publication 组合必须合法；
- public projection item 必须是 public-owned wiki，route/link/attachment/confirmation/hash 闭环；
- event 的 target、actor、nonce、hash 和 `public_safe_forbidden_fields` 必须匹配；
- 所有内容引用在 owner Vault 内解析，跨 Vault content reference 返回 `cross_vault_reference`。

Domain rule layer 不修改输入；它输出 `DeterministicReport`，写入/发布操作把 `schema_version`、validator version、schema files hash、input hash 和错误列表写入 operation/audit。未知 schema version、schema 文件缺失/hash 不匹配、validator 版本不兼容均 fail-closed。

## 运行和迁移

1. CI 与本地工具先执行 registry/policy 校验，再加载 executable schemas。
2. Preview、prepare、validation、projection 和 API 共享同一 validator facade，不能各自复制一套字段检查。
3. 新 schema 版本并行加载；旧 durable record 继续按其 `$id` 重放，不能静默用新规则解释旧报告。
4. 在 executable schemas 和 domain rule tests 完成前，F002/F003/F004/F007 只能保持 Designed/Not Implemented；POC fixture 通过不构成领域契约验收。

## 最小验收

需要覆盖合法对象、未知字段、错误类型、错误 version、跨字段非法组合、schema 文件 hash 变化、跨 Vault 引用和错误恢复；错误必须字段级、可重放且不写入 canonical。`validate:config` 与 `validate:docs` 通过不能替代这些测试。
