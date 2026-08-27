---
archive_policy: text-only
confidentiality: public
domain: computer-science
extractor: utf8/1
id: conversion
local:
  file_sha256: sha256:c2bac752a8751ee36819e05509c3c8c588671407e58eef33a1ce4ff4f4e47b83
  path_ref: local-sidecar:public/conversion
media_type: text/markdown
origin: external
read_status: retrieved
retrieval:
  acquisition: local-file
schema_version: source/v1
snapshot_sha256: sha256:c2bac752a8751ee36819e05509c3c8c588671407e58eef33a1ce4ff4f4e47b83
source_type: local-file
vault_id: public
---
# 转换

## static_cast

### 作用

使用隐式和用户定义转换的组合来进行类型之间的转换。

* 静态向下转换
* 左值到亡值
* 初始化转换
* 弃值表达式
* 隐式转换的逆转换
* 数组到指针后随向上转换
* 有作用域枚举到 int 或 float
* int 到枚举，枚举到另一枚举
* 指向成员指针向上转换
* void *到任意类型



## dynamic_cast 

### 作用

沿继承层级向上、向下及侧向，安全地转换到其他类的指针和引用。



## const_cast

### 作用

在有不同 cv 限定的类型间转换。



## reinterpret_cast

### 作用

通过重新解释底层位模式在类型间转换。