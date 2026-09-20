# Recipes（任务导向使用手册）

> 本目录是**面向任务的操作指南**（"我要完成 X，怎么做"），不是规范、不是决策记录。
> 规范以 [系统设计](../myknowledge-system-design.md) 为唯一事实源，实现边界见
> [Technical Design](../technical-design/README.md)，决策原因见 [ADR](../adr/README.md)。

## 为什么单列这一层（业界惯例）

参照 **Diátaxis** 文档框架（Daniele Procida 提出，Django / Canonical(Ubuntu) /
Cloudflare / Gatsby 等广泛采用），技术文档分四象限：

| 象限 | 回答 | 本仓库落点 |
| --- | --- | --- |
| Tutorials（教程） | 新手第一次上手 | （暂缺） |
| **How-to guides（操作指南）** | **"我要做 X 怎么做"** | **本目录 `recipes/`** |
| Reference（参考） | 精确的接口/契约事实 | `technical-design/`、系统设计 |
| Explanation（阐释） | "为什么这样设计" | `adr/` |

"Recipe / Cookbook" 是 How-to 象限的通行命名（参见 OpenAI Cookbook、LangChain
cookbook、Rust Cookbook）：每篇是可照抄、可复现的任务配方，聚焦"怎么用"，把"为什么/
精确契约"留给上面两层，避免与规范重复。

## 写作约定

- 一篇一个任务/主题；标题即任务（如"写入 Source"）。
- 给**可直接跑的命令 / 请求体**，覆盖三入口（CLI/myk、后端 HTTP、Agent Skill、编程 registry）。
- 只描述"怎么用 + 关键注意"；精确字段/失败码指向 Technical Design，别在此处再造一份规范。
- 命令与契约若与实现漂移，以实现与 Technical Design 为准，并回来更新本篇。

## 目录

| 配方 | 主题 |
| --- | --- |
| [写入 Source（create/update/delete/purge）](./source-write.md) | source 的统一创建契约与两阶段删除的四入口用法 |
