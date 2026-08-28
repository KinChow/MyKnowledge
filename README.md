# 📚 MyKnowledge - 个人知识管理系统

一个现代化的个人知识管理解决方案，支持多格式内容管理、智能搜索和跨设备同步。

------

## 🚀 核心功能

| 功能           | 说明                                                         |
| :------------- | :----------------------------------------------------------- |
| **多格式记录** | 支持 Markdown、图片、视频、PDF 等多种格式，满足全场景知识记录需求 |
| **智能分类**   | 通过标签系统和目录树实现三维分类，支持自定义分类维度         |
| **全文检索**   | 本地自然语言/混合检索默认使用 QMD；不可用时回退 FTS5 和 SQLite LIKE |
| **版本与同步** | public repo 使用 Git 管理；private Git remote 和加密备份位置当前待配置，不默认声称已同步或已备份 |
| **版本控制**   | 内置 Git 版本管理，随时回溯历史版本                          |

------

## 📂 项目结构

```bash
MyKnowledge/
├── docs/                  # 迁移中的原始内容与设计文档
├── frontend/              # Astro/Starlight 静态 Wiki（public projection 消费者；已临时移除，规划中）
├── sources/               # 目标 Source 层（实现后创建）
├── wiki/                  # 目标 Wiki 层（实现后创建）
├── config/                # schema、policy 和 public + 0..N vault 示例
├── tools/                 # Source/校验/锚定等工具（python -m tools.cli）
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
- Node.js 22+（frontend 重建后所需；本地自然语言/混合检索默认使用 QMD，QMD 不可用时自动回退 SQLite FTS5，再回退 SQLite LIKE）

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

MkDocs 回退预览已于 2026-08-28 退役（B5）。当前用法：

```bash
python -m tools.cli doctor          # 健康自检
python -m tools.cli projection generate   # 生成 public projection
cd frontend && MYKNOWLEDGE_CONTENT_MODE=projection MYKNOWLEDGE_ROOT=.. npm run build
cd dist && python3 -m http.server 8766   # 本地预览
```

frontend 用法（正式 public projection 消费链路，架构见系统设计文档）：

```bash
cd frontend
npm ci
npm run dev
```

访问 ➡️ [http://127.0.0.1:4321](http://127.0.0.1:4321/)。该模式只用于迁移基线和内容回归。

正式 public projection 预览/验证必须显式选择投影输入，并在 manifest、人工确认和 leak gate 全部满足后才可构建：

```bash
cd frontend
MYKNOWLEDGE_CONTENT_MODE=projection npm run validate:projection
MYKNOWLEDGE_CONTENT_MODE=projection npm run dev
```

正式前端只读取 `queries/public` 或 public projection，不读取 private vault；当前仓库没有正式 manifest 时，上述 projection 命令会 fail-closed。

### 3. 内容创作

1. 通过 Source-first 工具导入或创建 `sources/` 记录；不要把无来源正文直接标记为 published。
2. 通过 Wiki writer 创建 claim/evidence target，并经过 deterministic/LLM 验证和 Preview/Apply。
3. 公开站点只消费 `public_publishable` projection；`public_release` 默认是 `false`，只有人工对当前 hash 改为 `true` 并完成 public confirmation 才能发布；internal 内容写入用户明确选择的 private vault，并在私有发布时显示告警。

### 4. 部署发布

frontend 已临时移除，以下为重建后的规划发布链路：

```bash
# 正式 public 发布前必须先在 frontend 中完成 projection、人工确认和三段 leak gate：
cd frontend
MYKNOWLEDGE_CONTENT_MODE=projection npm run validate:projection
# 本仓库当前只生成并验证 dist，不自动 deploy；实际 GitHub Pages 命令
# 由部署仓库维护，且 public CI 不得 checkout 任何 private vault。
```

------

## 🤝 参与贡献

欢迎提交 Issue 或 PR，请遵循：

1. Fork 项目并创建特性分支
2. 提交前运行 `python -m pytest` 与 `python -m tools.cli doctor`
3. 使用 Conventional Commits 格式编写提交信息

------
