# F001/F002/F003 工具

这些工具实现 Source 导入、不可变 text snapshot、evidence selector、Wiki 契约校验与 LLM 证据审计。所有写操作都必须先 Preview，再由人工显式确认 Apply（确认/审计记录为 durable audit，不属于两阶段写操作）。

统一入口（在仓库根目录执行）：

```bash
python3 -m tools.cli <source|anchor|validate|audit|confirm> [options...]
```

## Source 导入（source）

```bash
python3 -m tools.cli source \
  --from-file docs/path/to/article.md \
  --domain computer-science \
  --source-id stable-source-id \
  --media-type text/markdown
```

Preview 输出 `operation_id` 后，确认当前 diff、目标 Vault 和 hash，再执行：

```bash
python3 -m tools.cli source --apply op_<id> --confirm --actor-id local-user
```

Apply 会生成：

- `sources/<domain>/<source-id>.md`
- `archive/text/<snapshot_sha256>.md`
- `archive/manifest.jsonl`
- `audit/operations/<operation_id>.json`
- local-file 的 `state/local-sources/public/<source-id>.json`

## Evidence 锚定（anchor）

```bash
python3 -m tools.cli anchor \
  archive/text/<snapshot_sha256>.md \
  '原文中的唯一引文' \
  --source sources/<domain>/<source-id>.md \
  --root .
```

Preview 输出 operation ID 后执行：

```bash
python3 -m tools.cli anchor \
  --root . \
  --apply op_<id> \
  --confirm \
  --actor-id local-user
```

Evidence 使用 Unicode code-point 半开区间、TextQuoteSelector、selector hash 和 quote hash。引文未命中、多重命中、过短或 snapshot hash 漂移都会阻断 Apply。

## Wiki 确定性校验（validate）

```bash
python3 -m tools.cli validate wiki/computer-science/transformer.md --root .
```

对 Wiki canonical 文件执行 schema 校验（`config/json-schema/wiki-v1.json`）与跨字段规则，输出派生字段（evidence_state / validation_state / strength / availability / publishable）、内容 hash 与字段级错误；退出码 0 表示校验通过。手写派生字段（vault_id / content_sha256 / evidence_sha256 等 15 个）一律拒绝。

## LLM 证据审计（audit）

```bash
python3 -m tools.cli audit wiki/<domain>/<id>.md --root . [--provider agent-cli|openai] [--cli ducc]
```

对 Wiki 执行 LLM 证据审计（§8）：确定性校验 → 规则集抽取（`config/policy.yaml` 的 `validation.ruleset.rule_ids`，按 spec ID 从规范文档实时取文）→ provider 单次调用（`temperature=0` 等价能力，禁工具/URL）→ 覆盖义务校验（全 claim×target、逐条回引规则、rationale 引用区间）→ 模型引文逐字二次校验 → corroboration-v1 多 source 一致性 → append-only 报告写入 `audit/validation/wiki/<id>/`。

- provider 由 Skill runtime 注入：`agent-cli`（默认，ducc/ducx 非交互模式，`--cli` 可指定路径）或 `openai`（环境变量 `OPENAI_BASE_URL`/`OPENAI_API_KEY`/`OPENAI_MODEL`）；endpoint/model/key 不写入仓库或报告。
- 覆盖不全 / malformed / provider 不可用 / 模型自声明 not_run → `not_run` + 结构化 reason（不写"已审"痕迹）；LLM `fail` 阻断发布。
- 规则集变化只把既有结论标 `stale_ruleset`（可见、不阻断），不使人工确认失效（AC-F003-015）。

## 人工审计确认（confirm）

```bash
python3 -m tools.cli confirm wiki/<domain>/<id>.md --root . --actor-id local-user [--decision approve|reject]
```

对当前 `(content_sha256, evidence_sha256)` 写入 `operation-confirmation/v1`：确定性校验必须通过；LLM `fail` 阻断。确认记录含 DeterministicReport 摘要 hash、LLM 审计状态与历史 fail 次数，双路径写入 `audit/validation/wiki/<id>/` 与 `audit/operations/`（后者驱动 publishability）。正文/evidence 变化使确认自动失效。

## 本次试迁移

本轮只迁移了 3 篇 legacy 文档用于验证，不修改 `docs/`：

- `sources/tools/git-commands.md`
- `sources/computer-science/von-neumann-architecture.md`
- `sources/computer-science/linux-compilers.md`

批量迁移仍属于 F010，不由这些工具自动执行。

## 依赖与来源

优先使用成熟开源库，不自建轮子（对应 `requirements.txt`）：

| 依赖 | 来源 | 用途 |
| --- | --- | --- |
| PyYAML | https://github.com/yaml/pyyaml（MIT） | Front Matter 底层 YAML（经 python-frontmatter） |
| python-frontmatter | https://github.com/rafaelmardojai/python-frontmatter（MIT） | Front Matter 解析/渲染（薄适配 + fail-closed 闭合检查） |
| jsonschema | https://github.com/python-jsonschema/jsonschema（MIT） | F002 wiki/v1 + F003 wiki-validation/v1 可执行 JSON Schema 校验 |
| filelock | https://github.com/tox-dev/py-filelock（MIT） | per-vault 独占写锁（Unix flock / Windows msvcrt） |
| trafilatura | https://github.com/adbar/trafilatura（Apache-2.0） | HTML 网页正文提取（去噪/编码检测）；失败归一为结构化错误码，不降级 |
| pypdf | https://github.com/py-pdf/pypdf（BSD-3） | PDF 正文提取 |
| difflib | Python 标准库 | 引文不匹配的最长公共子串诊断 |
| openai | https://github.com/openai/openai-python（Apache-2.0） | F003 OpenAI 兼容 provider 调用（可选；agent-cli 路径不依赖） |
| packaging | https://github.com/pypa/packaging（Apache-2.0/BSD-2） | corroboration-v1 版本半开区间比较（Version） |
| ducc/ducx（外部 CLI） | Comate/Codex 命令行 | F003 默认 LLM provider：非交互结构化输出（`-p --json-schema` / `exec --json`），运行时注入 |

F003 语义参照：claim-evidence 判定结构借鉴 [FEVER](https://fever.ai)/[AVeriTeC](https://fever.ai/2024/task.html)（SUPPORTED/REFUTED/conflicting-evidence，坚持逐字引文而非近似匹配）；prompt 数据边界借鉴 Anthropic/OpenAI prompt 工程定界符做法；不引入通用 sanitizer 库（固定系统提示 + 禁工具 + schema 校验已覆盖 AC-F003-011）。

路径布局由 `tools/paths.py` 的 `RepoPaths` 统一管理（借鉴 cookiecutter.config.Paths 模式），
布局变更只改该类。领域特定逻辑（`canonical_quote` 引文归一、`evidence_state`/`strength`
派生计算、Wiki 契约规则）无对应开源可移植对象，按 `docs/myknowledge-system-design.md`
§6.9 / §6.8 实现并保持单份实现。
