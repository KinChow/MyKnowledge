---
archive_policy: text-only
confidentiality: public
domain: computer-science
extractor: utf8/1
id: compilers-on-windows
local:
  file_sha256: sha256:9a249907c8db860a25289d8a9c28714f9ef6500d386030a3e8495cb77176d9f5
  path_ref: local-sidecar:public/compilers-on-windows
media_type: text/markdown
origin: external
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:9a249907c8db860a25289d8a9c28714f9ef6500d386030a3e8495cb77176d9f5
source_type: local-file
vault_id: public
---
# Windows的编译器

## Microsoft Visual C++ (MSVC)

### 下载链接

https://visualstudio.microsoft.com/zh-hans/downloads/



### 安装方法

1. 下载并安装Visual Studio社区版或专业版（根据需求选择）。
2. 在安装过程中选择“使用C++的桌面开发”工作负载。





## MinGW-w64 (GNU Compiler Collection - GCC)

### 下载链接

https://github.com/niXman/mingw-builds-binaries/releases



### 安装方法

1. 选择合适的压缩包
   * x86_64：64位系统
   * i686：32位系统
   * win32：开发 Windows 程序
   * posix：开发 Linux、Unix、Mac OS 等其他操作系统下的程序





## Clang/LLVM

### 下载链接

https://github.com/llvm/llvm-project/releases/



### 安装方法

1. 下载并安装LLVM安装包，其中包含Clang编译器。
   * win64：64位系统
   * win32：32位系统