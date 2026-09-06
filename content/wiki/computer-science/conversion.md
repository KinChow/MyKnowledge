---
aliases: []
confidentiality: public
domain: computer-science
evidence:
- claim: C++ 在表达式类型 T1 用于不接受 T1 但接受 T2 的上下文时执行隐式转换。
  claim_id: conversion-audit-1
  support: direct
  supporting_quotes:
  - evidence_id: evidence-86d01210e629
    exact: 'Implicit conversions are performed whenever an expression of some type
      T1 is used in context that does not accept that type, but accepts some other
      type T2; in particular:'
  targets:
  - evidence_id: evidence-86d01210e629
    source_id: cppreference-cpp-conversion-v2
id: conversion
kind: reference
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- cppreference-cpp-conversion-v2
- working-computer-science-conversion
status: published
tags:
- cpp
- conversion
- cast
- reference
title: 转换
updated_at: '2026-09-06'
---
# 转换

## 详细章节

### 转换

#### static_cast

##### 作用

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



#### dynamic_cast 

##### 作用

沿继承层级向上、向下及侧向，安全地转换到其他类的指针和引用。



#### const_cast

##### 作用

在有不同 cv 限定的类型间转换。



#### reinterpret_cast

##### 作用

通过重新解释底层位模式在类型间转换。

## 参考

- https://en.cppreference.com/w/cpp/language/implicit_conversion
- https://en.cppreference.com/w/cpp/language/explicit_cast
