# F001 Source 工具

这些工具实现 Source 导入、不可变 text snapshot 和 evidence selector。所有写操作都必须先 Preview，再由人工显式确认 Apply。

统一入口（在仓库根目录执行）：

```bash
python3 -m tools.cli <source|anchor|validate> [options...]
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
| jsonschema | https://github.com/python-jsonschema/jsonschema（MIT） | F002 wiki/v1 可执行 JSON Schema 校验 |
| filelock | https://github.com/tox-dev/py-filelock（MIT） | per-vault 独占写锁（Unix flock / Windows msvcrt） |
| trafilatura | https://github.com/adbar/trafilatura（Apache-2.0） | HTML 网页正文提取（去噪/编码检测）；失败归一为结构化错误码，不降级 |
| pypdf | https://github.com/py-pdf/pypdf（BSD-3） | PDF 正文提取 |
| difflib | Python 标准库 | 引文不匹配的最长公共子串诊断 |

路径布局由 `tools/paths.py` 的 `RepoPaths` 统一管理（借鉴 cookiecutter.config.Paths 模式），
布局变更只改该类。领域特定逻辑（`canonical_quote` 引文归一、`evidence_state`/`strength`
派生计算、Wiki 契约规则）无对应开源可移植对象，按 `docs/myknowledge-system-design.md`
§6.9 / §6.8 实现并保持单份实现。
