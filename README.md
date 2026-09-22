# 📚 MyKnowledge - 个人知识管理系统

一个现代化的个人知识管理解决方案，支持多格式内容管理、智能搜索和跨设备同步。

------

## 🚀 核心功能

| 功能           | 说明                                                         |
| :------------- | :----------------------------------------------------------- |
| **多格式记录** | 支持 Markdown、图片、视频、PDF 等多种格式，满足全场景知识记录需求 |
| **智能分类**   | 通过标签系统和目录树实现三维分类，支持自定义分类维度         |
| **全文检索**   | 本地检索默认 SQLite FTS5（simple 分词）索引，不可用时回退 SQLite LIKE |
| **版本与同步** | public repo 使用 Git 管理；private Git remote 和加密备份位置当前待配置，不默认声称已同步或已备份 |
| **版本控制**   | 内置 Git 版本管理，随时回溯历史版本                          |

------

## 📂 项目结构

```bash
MyKnowledge/
├── content/               # 内容层：sources/、wiki/（canonical 知识对象）
├── docs/                  # 治理层：系统设计、ADR、Technical Design、Acceptance、Feature List
├── frontend/              # Astro/Starlight 静态 Wiki（public projection 消费者）
├── backend/               # FastAPI 本地服务（loopback only）
├── config/                # schema、policy 和 public + 0..N vault 示例
├── tools/                 # Source/校验/锚定/发布等工具（人用 python -m tools.myk；机器 tools.cli）
├── archive/  audit/  release/   # 归档快照、durable 审计与发布确认（F013 批次 3 迁入 ledger/）
├── var/                   # 生成物与临时运行态（projection/索引/state）
├── scripts/               # bootstrap 与本地启停脚本
├── requirements.txt       # Python 依赖列表
└── README.md              # 项目说明
```

需要同时挂载多个外挂仓库时，使用仅本机存在的私有 workspace（不提交到 public repo）：

```text
MyKnowledge-workspace/
├── public/                 # 当前 MyKnowledge public repo checkout
└── vaults/
    ├── team-internal/      # private repo 或 submodule checkout
    ├── personal-private/   # 可选
    └── research-private/   # 可选
```

当前仓库也可以不搬目录，直接作为 `public` vault 运行，并在被忽略的 local manifest 中填写一个或多个 `vaults/*` 路径。两种布局使用同一个 Vault Registry 和对象模型。

## 📐 重构方案

证据驱动知识系统的完整架构、数据 schema、source-first 写入规范、LLM 证据验证、Agent Skill、FastAPI 本地模式、Astro 静态模式、迁移计划和验收门禁见：[MyKnowledge 证据驱动知识系统设计](docs/myknowledge-system-design.md)。

该文档当前是设计与实施规范，不代表目标能力已经全部实现；方案确认后按文档中的实施阶段逐步落地。

重构交付文档：

- [Feature List](docs/feature-list.md)：功能拆解、优先级、依赖和交付状态。
- [ADR](docs/adr/README.md)：长期架构决策及其取舍原因。
- [Technical Design](docs/technical-design/README.md)：具体实现边界、流程、失败处理和测试策略。
- [Acceptance](docs/acceptance/README.md)：可执行验收场景和通过规则。
- [Traceability Matrix](docs/traceability-matrix.md)：规范、Feature、实现设计、验收和测试的映射。

------

## 🛠️ 快速开始

### 前置要求

- Python 3.11+
- Git 2.20+
- Node.js 22+（frontend 重建后所需；本地检索用 SQLite FTS5（simple 分词），不可用时回退 SQLite LIKE）

### 1. 环境配置

```bash
# 克隆仓库
git clone https://github.com/KinChow/MyKnowledge.git
cd MyKnowledge

# 一键引导（venv + 依赖 + 自检）
bash scripts/bootstrap.sh

# 或仅安装 Python 依赖
pip install -r requirements.txt
```

### 2. 本地运行

MkDocs 回退预览已于 2026-08-28 退役（B5）。日常联调（两个独立进程，顺序不限）：

```bash
bash scripts/start-frontend.sh   # Astro    http://127.0.0.1:4321/  知识库可单独浏览
bash scripts/start-backend.sh    # FastAPI  http://127.0.0.1:8765/api/health  首页才出现练习入口
```

frontend 用法（正式 public projection 消费链路，架构见系统设计文档）：

```bash
cd frontend
npm ci
npm run prepare-content
npm run dev
```

访问 ➡️ [http://127.0.0.1:4321](http://127.0.0.1:4321/)。`astro dev` 通过 `/local-api` 代理本机 FastAPI；静态 `dist` 预览不含练习页。

正式 public projection 预览/验证必须显式选择投影输入，并在 manifest、确定性校验和 leak gate 全部满足后才可构建：

```bash
cd frontend
MYKNOWLEDGE_CONTENT_MODE=projection npm run validate:projection
MYKNOWLEDGE_CONTENT_MODE=projection npm run dev
```

正式前端只读取 `queries/public` 或 public projection，不读取 private vault；当前仓库没有正式 manifest 时，上述 projection 命令会 fail-closed。

### 3. 内容创作

1. 通过 Source-first 工具导入或创建 `content/sources/` 记录；不要把无来源正文直接标记为 published。
2. 综合 source 写出 `content/wiki/` 页面与 claim/evidence 映射，跑确定性校验与 LLM 审计；落盘一次到位，审批由 `git diff` + `git commit` 承担（ADR-0019）。
3. 公开站点只消费通过确定性门禁的 public projection；Git commit 是公开发布审批边界，`public_release` 从合格内容派生，不可手写。逐页 `release confirm` 已退役，历史文件保留；LLM 审计仅 advisory，不阻断公开发布（ADR-0022）。internal 内容仍写入用户明确选择的 private vault。

### 4. 部署发布

公开前端部署到 GitHub Pages 的 `/MyKnowledge/` 项目页；FastAPI/MCP 仅本地运行。
practice 页面与专用资源从 release 剔除，公开页面不探测本机 API、不携带本地 token。

```bash
# 先人工审阅并提交发布输入。dirty canonical/config/build-code 会被构建拒绝。
PUBLIC_BASE_PATH=/MyKnowledge/ npm --prefix frontend run build
# build 从当前提交重新生成 projection，执行三段 leak-gate 与链接闭包校验。
# .github/workflows/deploy-pages.yml 使用同一入口；本地 build 不部署。
```

------


## 日常使用

人用入口是 porcelain `myk`（少量名词 + 动词，参照 git/gh）；机器与 agent 用 plumbing `tools.cli`（细粒度，供脚本链式调用）。下面给人的示例都用 `myk`。

> 想直接敲 `myk` 而不是 `python -m tools.myk`：仓库根有一个 `myk` wrapper 脚本，把仓库根加入 `PATH`，或 `alias myk="$(pwd)/myk"`（在仓库根执行）即可。它从任意目录都能运行。浏览类命令默认缩进输出，加 `--json` 看原始结构。

```bash
# 健康自检（每天一次即可：projection/索引/sources/备份一屏可见）
python -m tools.myk doctor

# 查询知识（FTS5 索引自动接线；结果含 object_ref/snippet/证据 hash）
python -m tools.myk query "<关键词>"
python -m tools.myk query read <wiki-id>          # 读已发布 wiki 正文
python -m tools.myk query backlinks <wiki-id>     # 反向引用
```

### 写入（一次落盘 → git 审批）

写入没有独立的审批关口：工具只负责把变更落到工作区，审核由 `git diff` 承担、批准由 `git commit` 承担（ADR-0019）。`write` / `confirm-apply` / `lock` 命令已退场。

```bash
# 1) 导入外部资料为 Source（url 抓取 / 本地文件 / 个人笔记）
python -m tools.myk source add --url https://... --domain tools --source-id my-doc
python -m tools.myk source add --from-file ./note.md --domain work-methods

# 2) 写/改 wiki 或任意文件：直接用编辑器编辑 content/ 下的文件
#    （agent / FastAPI 走受控落盘通道 python -m tools.cli skill write，一次写到位）

# 3) 审阅 diff 并提交（人工执行；这是唯一的批准动作）
git diff && git commit
```

### 校验、审计与发布（Source → Wiki → 公开页）

```bash
python -m tools.myk wiki anchor <snapshot.md> "<引文>" --source content/sources/<dom>/<id>/<id>.md  # 证据锚定
python -m tools.myk wiki validate content/wiki/<dom>/<id>.md    # 确定性校验
python -m tools.myk wiki audit    content/wiki/<dom>/<id>.md    # LLM 证据审计（默认复用本机 agent CLI，零配置）
# LLM 结果仅作建议；公开发布不再要求 wiki confirm / wiki publish confirm。
python -m tools.myk build projection               # 本地预览 projection（标记 FTS stale）
python -m tools.myk build index --scope public --index var/state/index/public.sqlite3
# 审阅并提交后，正式构建绑定当前 Git commit
PUBLIC_BASE_PATH=/MyKnowledge/ npm --prefix frontend run build
```

（每条 action 默认打印一行人类摘要，加 `--json` 看完整结构。）

### 静态站（浏览器）

提交/CI 浏览器门禁见 [Browser regression gates](frontend/e2e/README.md)：
pre-push 先跑 Python 回归，再构建 `/MyKnowledge/` 并运行公开站与隔离本地练习
两组 Playwright 用例；PR/push CI 同样执行，Pages 上传前必须通过公开站用例。
没有本地定时看护。首次运行需要安装 Playwright Chromium；可设置
`MYK_E2E_CHANNEL=chrome` 使用本机 Google Chrome。

```bash
cd frontend && MYKNOWLEDGE_CONTENT_MODE=projection MYKNOWLEDGE_ROOT=.. npm run build
cd dist && python3 -m http.server 8766    # http://127.0.0.1:8766/wiki/<id>/
```

### 本地 API 与 Agent 通道（机器面，plumbing）

```bash
python -m backend.server --root . --port 8765   # FastAPI（loopback only，写入需 capability token；无确认事件）
python -m tools.cli skill <action> --payload p.json   # Agent 受控 action（写入为一次落盘，审批走 git）
```

### 备份

```bash
python -m tools.myk backup manifest --root .          # 生成 durable manifest（写入前校验全库）
python -m tools.myk backup export-bundle --manifest audit/backup/<id>.json --target /备份盘/bundle
python -m tools.myk backup restore-bundle --manifest /备份盘/bundle --target /恢复目录 --target-vault-id public
```

### LLM provider（可选；默认零配置）

```bash
# 路径 A：默认复用本机 agent CLI（ducc/ducx），无需任何配置
# 路径 B：OpenAI 兼容 API —— cp config/providers.example.yaml config/providers.local.yaml 填好后：
export MYKNOWLEDGE_LLM_PROFILE=deepseek
python -m tools.myk wiki audit content/wiki/<dom>/<id>.md --provider openai
```

## 🤝 参与贡献

欢迎提交 Issue 或 PR，请遵循：

1. Fork 项目并创建特性分支
2. 提交前运行 `python -m pytest` 与 `python -m tools.myk doctor`
3. 使用 Conventional Commits 格式编写提交信息

------
