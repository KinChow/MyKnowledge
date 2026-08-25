# 📚 MyKnowledge - 个人知识管理系统

一个现代化的个人知识管理解决方案，支持多格式内容管理、智能搜索和跨设备同步。

------

## 🚀 核心功能

| 功能           | 说明                                                         |
| :------------- | :----------------------------------------------------------- |
| **多格式记录** | 支持 Markdown、图片、视频、PDF 等多种格式，满足全场景知识记录需求 |
| **智能分类**   | 通过标签系统和目录树实现三维分类，支持自定义分类维度         |
| **全文检索**   | 基于关键词的快速搜索，支持布尔运算符和模糊匹配               |
| **云端同步**   | 自动备份至 GitHub/Gitee，以便在不同设备上访问        |
| **版本控制**   | 内置 Git 版本管理，随时回溯历史版本                          |

------

## 📂 项目结构

```bash
MyKnowledge/
├── docs/                  # 知识库核心目录
│   └── index.md           # 知识库入口
├── mkdocs.yml             # 站点配置
├── requirements.txt       # 依赖列表
└── README.md              # 项目说明
```

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

- Python 3.8+
- Git 2.20+

### 1. 环境配置

```bash
# 克隆仓库
git clone https://github.com/KinChow/MyKnowledge.git
cd MyKnowledge

# 安装依赖（推荐方式）
pip install -r requirements.txt

# 或手动安装核心组件
pip install mkdocs mkdocs-material mkdocs-mermaid2-plugin
```

### 2. 本地运行

```bash
mkdocs serve
```

访问 ➡️ [http://127.0.0.1:8000](http://127.0.0.1:8000/)

### 3. 内容创作

1. 在 `docs/` 目录下创建 `.md` 文件
2. 使用 Markdown 语法编写内容
3. 实时预览会自动刷新

### 4. 部署发布

```bash
# 部署到 GitHub Pages
# cd ../orgname.github.io/
# mkdocs gh-deploy --config-file ../my-project/mkdocs.yml --remote-branch main
cd ../KinChow.github.io/
mkdocs gh-deploy --config-file ../MyKnowledge/mkdocs.yml --remote-branch main

# 自定义部署路径（示例）
mkdocs build --site-dir ../public_knowledge/
```

------

## 🤝 参与贡献

欢迎提交 Issue 或 PR，请遵循：

1. Fork 项目并创建特性分支
2. 提交前运行 `mkdocs build` 验证构建
3. 使用 Conventional Commits 格式编写提交信息

------
