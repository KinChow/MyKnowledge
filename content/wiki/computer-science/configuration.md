---
aliases: []
confidentiality: public
domain: computer-science
evidence:
- claim: Pro Git 第一章《关于版本控制》与第二章《Git 基础》覆盖版本控制概念与 Git 基础操作：获取仓库、记录变更、查看提交历史、撤销操作、远程协作、标签、别名等。
  claim_id: configuration-audit-1
  support: direct
  supporting_quotes:
  - evidence_id: evidence-df7f846923e5
    exact: "- 1.1 About Version Control\n  - 1.2 A Short History of Git\n  - 1.3 What
      is Git?\n  - 1.4 The Command Line\n  - 1.5 Installing Git\n  - 1.6 First-Time
      Git Setup\n  - 1.7 Getting Help\n  - 1.8 Summary\n- \n  2. Git Basics\n  - 2.1
      Getting a Git Repository\n  - 2.2 Recording Changes to the Repository\n  - 2.3
      Viewing the Commit History\n  - 2.4 Undoing Things\n  - 2.5 Working with Remotes\n
      \ - 2.6 Tagging\n  - 2.7 Git Aliases\n  - 2.8 Summary\n-"
  targets:
  - evidence_id: evidence-df7f846923e5
    source_id: web-computer-science-configuration
id: configuration
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-configuration
- working-computer-science-configuration
status: published
tags:
- git
- version-control
- configuration
title: Git配置
updated_at: '2026-09-06'
---
# Git配置

## 一句话结论

Git 配置分为系统（`--system`，对所有用户）、用户（`--global`，当前用户）、仓库（`--local`，当前项目）三个层级，可配置个人身份、文本换行符、文本编码与服务器认证，是使用 Git 前的基础设置。

## 核心概念

- **系统配置**：对所有用户生效，存放在 Git 安装目录下 `%Git%/etc/gitconfig`，使用 `git config` 时加 `--system` 选项。
- **用户配置**：只适用于当前用户，存放在用户目录下，使用 `--global` 选项。
- **仓库配置**：只对当前项目生效，存放在工作目录的 `.git/config`，使用 `--local` 选项。
- **认证方式**：http/https 协议（口令缓存、证书信任）与 ssh 协议（公钥认证，无需输入密码，加密传输）。

## 工作机制

- **配置个人身份**：`user.name` / `user.email` 会体现在 git 仓库提交修改信息中，与 git 服务器认证使用的密码或公钥密码无关。
- **文本换行符**：Windows 用回车(CR)和换行(LF)两个字符结束一行，mac 或 linux 只用换行(LF)一个字符；`core.autocrlf true` 提交时自动把 CRLF 转成 LF、签出时把 LF 转成 CRLF；`core.autocrlf input` 提交时 CRLF 转 LF、签出时不转换。
- **文本编码**：`i18n.commitEncoding` 控制 git commit log 存储时采用的编码，`i18n.logOutputEncoding` 控制查看 git log 时显示的编码；`gui.encoding` 与 `core.quotepath false` 用于中文编码支持与显示路径中的中文。
- **服务器认证**：http/https 通过 `credential.helper store` 设置口令缓存、`http.sslverify false` 添加 https 证书信任；ssh 使用公钥认证（`ssh-keygen` 生成公钥后添加到代码平台）。

## 示例或代码

```shell
git config --system core.autocrlf
git config --global user.name "XXX"
git config --global user.email "xxx@xxx.com"
git config --global core.autocrlf true
git config --global core.autocrlf input

# 中文编码支持
git config --global gui.encoding utf-8
git config --global i18n.commitEncoding utf-8
git config --global i18n.logOutputEncoding utf-8

# 显示路径中的中文
git config --global core.quotepath false

# http/https 认证
git config --global credential.helper store
git config --global http.sslverify false

# ssh 认证：生成公钥
ssh-keygen -t ed25519 -C "xxx@xxx.com"
```

## 常见误区

- **把身份配置误认为与服务器认证相关**：`user.name` / `user.email` 只体现在提交修改信息中，与 git 服务器认证使用的密码或公钥密码无关。
- **混淆配置作用域**：`--system` 对系统所有用户生效，`--global` 只对当前用户生效，`--local` 只对当前项目生效；使用错误的选项会把配置写进错误的层级。

## 证据映射

| claim_id | 来源 | 要点 |
| --- | --- | --- |
| configuration-audit-1 | web-computer-science-configuration | Pro Git 第一章/第二章覆盖版本控制概念与 Git 基础操作（获取仓库、记录变更、查看历史、撤销、远程、标签、别名） |

## 待验证项

无。

## 关联知识

- [[git-commands]] —— Git 常用命令

## 详细章节

### Git配置

#### 概念

##### 系统配置（对所有用户使用）

存放在Git安装目录下：`%Git%/etc/gitconfig`。

使用`git config`时用`--system`选项，例如：

```shell
git config --system core.autocrlf
```



##### 用户配置（只适用于当前用户）

存放在用户目录下。

使用`git config`时用`--global`选项，例如：

```shell
git config --global user.name
```



##### 仓库配置（只对当前项目）

存放在工作目录的`.git/config`。

使用`git config`时用`--local`选项，例如：

```shell
git config --local remote.origin.url
```





#### 配置个人身份

```shell
git config --global user.name "XXX"
git config --global user.email "xxx@xxx.com"
```

这些配置信息会在git仓库提交修改信息中体现，与git服务器认证使用的密码或公钥密码无关。





#### 文本换行符配置

windows使用回车(CR)和换行(LF)两个字符结束一行，而mac或linux只是用换行(LF)一个字符。



提交时自动地把行结束符CRLF转换成LF，而签出代码时把LF转换成CRLF：

```shell
git config --global core.autocrlf true
```



提交时自动地把行结束符CRLF转换成LF，而签出时不转换：

```shell
git config --global core.autocrlf input
```





#### 文本编码配置

* i18n.commitEncoding 选项：git commit log存储时采用的编码
* i18n.logOutputEncoding 选项：查看git log时，显示采用的编码

```shell
# 中文编码支持
git config --global gui.encoding utf-8
git config --global i18n.commitEncoding utf-8
git config --global i18n.logOutputEncoding utf-8

# 显示路径中的中文
git config --global core.quotepath false
```





#### 与服务器的认证配置

##### 常见的两种协议认证方式

###### http/https 协议认证

设置口令缓存：

```shell
git config --global credential.helper store
```



添加https证书信任：

```shell
git config --global http.sslverify false
```





###### ssh 协议认证

使用公钥认证，无需输入密码，加密传输，操作便利又保证安全。



过程：

1. 生成公钥：

```shell
ssh-keygen -t ed25519 -C "xxx@xxx.com"
```

2. 添加公钥到代码平台。

