---
archive_policy: text-only
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-08f2ab2da0b9
  position:
    end: 29
    start: 10
    type: TextPositionSelector
  quote_sha256: sha256:0d6a70bb8bac45835aa50d881831ec6cfcc92182eec0a8050f752f70f490b328
  selector:
    exact: 存储程序计算机在体系结构上主要特点有：
    prefix: '# 冯诺依曼结构


      '
    suffix: '


      1. 以运算单元为中心

      2. 采用存储程序原理

      3. 存储器'
    type: TextQuoteSelector
  selector_sha256: sha256:f7b62319c2a5aebcc9011535e9088162873e6fdbb4a308f75d2f0c611964a8a6
  snapshot_sha256: sha256:b53e8489f81c0b746157b555810a93f2314ea7289d1a986ea1e7d2c3ceab525c
extractor: utf8/1
id: von-neumann-architecture
local:
  file_sha256: sha256:b53e8489f81c0b746157b555810a93f2314ea7289d1a986ea1e7d2c3ceab525c
  path_ref: local-sidecar:public/von-neumann-architecture
media_type: text/markdown
origin: external
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:b53e8489f81c0b746157b555810a93f2314ea7289d1a986ea1e7d2c3ceab525c
source_type: local-file
vault_id: public
---
# 冯诺依曼结构

存储程序计算机在体系结构上主要特点有：

1. 以运算单元为中心
2. 采用存储程序原理
3. 存储器是按地址访问、线性编址的空间
4. 控制流由指令流产生
5. 指令由操作码和地址码组成
6. 数据以二进制编码



存储程序计算机的两个核心点：

* 可编程
* 可存储



一台计算机包含部分

* 包含算术逻辑单元和处理器寄存器的处理器单元，来完成各种算术和逻辑运算
* 包含指令计算器和程序计数器的控制器单元，用来控制程序的流程，通常是不同条件下的分支和跳转。
* 存储数据和指令的内存
* 更大容量的外部存储 硬盘
* 输入输出设备

简单的想计算机的任何一个部件都可以归到运算器、控制器、存储器、输入和输出设备



计算机程序可以抽象为从输入设备读取输入信息，通过运算器和控制器来执行存储在存储器里的程序，最终把结果输出到输出设备。



<img src="von-neumann-architecture.assets/Von_Neumann_Architecture.jpg" alt="Single system bus evolutions of the architecture" style="zoom:50%;" />

