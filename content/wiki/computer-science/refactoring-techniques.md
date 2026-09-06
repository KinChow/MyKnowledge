---
aliases: []
confidentiality: public
domain: computer-science
evidence:
- claim: 'Refactoring

    Refactoring is a systematic process of improving code without creating new functionality
    that can transform a mess into clean code and simple design.

    Dirty code is result of inexperience multiplied by tight deadlines, mismanagement,
    and nasty shortcuts taken during the development process.

    Clean code is code that is easy to read, understand and maintain. Clean code makes
    software development predictable and increases the quality of a resulting product.'
  claim_id: refactoring-techniques-audit-1
  support: direct
  supporting_quotes:
  - evidence_id: evidence-44aa0423b3cc
    exact: 'Refactoring

      Refactoring is a systematic process of improving code without creating new functionality
      that can transform a mess into clean code and simple design.

      Dirty code is result of inexperience multiplied by tight deadlines, mismanagement,
      and nasty shortcuts taken during the development process.

      Clean code is code that is easy to read, understand and maintain. Clean code
      makes software development predictable and increases the quality of a resulting
      product.'
  targets:
  - evidence_id: evidence-44aa0423b3cc
    source_id: web-computer-science-refactoring-techniques
id: refactoring-techniques
kind: reference
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-refactoring-techniques
- working-computer-science-refactoring-techniques
status: published
tags:
- refactoring
- software-design
title: 重构手法
updated_at: '2026-09-06'
---
# 重构手法

## 详细章节

### 重构手法

#### 概念

重构手法

* 抽（抽取方法）
* 替（替换方法）
* 组（抽取类）
* 改（重命名）
* 移（移动方法）



#### 软件重构的方法

##### 简化语句

* 合并条件表达式：用提炼函数把多个条件检查合并，要确保逻辑顺序不变
* 移动语句：相关联的代码搜集到一处，通常要在提炼函数之前做
* 卫语句取代嵌套条件表达式：最外层可被替换的逻辑，替换为卫语句



##### 重组函数

* 将查询函数和修改函数分离：任何查询类有返回值的函数都不应该有看得到的副作用，试着将查询动作从修改动作中分离出来
* 以明确函数替代参数：函数入参有多个可能值，尝试使用多个明确值的函数来替代
* 提炼函数：减少重复代码
* 内联函数：消除多余的间接性，把函数和被调用代码合并



##### 重组数据

* 拆分变量：某个变量承担多个职责时，容易造成理解困难和修改出错，此时应拆分为多个职责单一的变量

* 提炼类：根据职责不同重新组织类

* 内联类：消除不再有独立职责的类，重新组织类

* 类继承体现重构手法

  * 成员搬移
    * 函数上移
    * 函数下移
    * 字段上移
    * 字段下移
    * 移除子类
    * 以子类取代类型码
    * 构造函数本体上移

  * 继承关系调整
    * 提炼超类
    * 折叠继承体系
    * 以委托取代子类
    * 以委托取代超类

## 参考
- https://refactoring.guru/refactoring
