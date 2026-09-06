---
aliases: []
confidentiality: public
domain: computer-science
evidence:
- claim: Microsoft 的指南用于在 Windows 上安装 Visual Studio 以及 Microsoft C/C++ 工具。
  claim_id: compilers-on-windows-audit-1
  support: direct
  supporting_quotes:
  - evidence_id: evidence-c9056513fd73
    exact: If you haven't installed Visual Studio and the Microsoft C and C++ tools
      yet, here's how to get started.
  - evidence_id: evidence-24363ada65c6
    exact: This article applies to installation of Visual Studio on Windows.
  targets:
  - evidence_id: evidence-c9056513fd73
    source_id: microsoft-vs-cpp-install-v2
  - evidence_id: evidence-24363ada65c6
    source_id: microsoft-vs-cpp-install-v2
id: compilers-on-windows
kind: reference
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- microsoft-vs-cpp-install-v2
- working-computer-science-compilers-on-windows
status: published
tags:
- compiler
- windows
- msvc
- gcc
- clang
title: Windows的编译器
updated_at: '2026-09-06'
---
# Windows的编译器

## 详细章节

### Windows的编译器

#### Microsoft Visual C++ (MSVC)

##### 下载链接

https://visualstudio.microsoft.com/zh-hans/downloads/



##### 安装方法

1. 下载并安装Visual Studio社区版或专业版（根据需求选择）。
2. 在安装过程中选择“使用C++的桌面开发”工作负载。





#### MinGW-w64 (GNU Compiler Collection - GCC)

##### 下载链接

https://github.com/niXman/mingw-builds-binaries/releases



##### 安装方法

1. 选择合适的压缩包
   * x86_64：64位系统
   * i686：32位系统
   * win32：开发 Windows 程序
   * posix：开发 Linux、Unix、Mac OS 等其他操作系统下的程序





#### Clang/LLVM

##### 下载链接

https://github.com/llvm/llvm-project/releases/



##### 安装方法

1. 下载并安装LLVM安装包，其中包含Clang编译器。
   * win64：64位系统
   * win32：32位系统
