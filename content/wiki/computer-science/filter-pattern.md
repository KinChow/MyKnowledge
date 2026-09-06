---
aliases:
- 过滤器模式
- Filter Pattern
- 标准模式
- Criteria Pattern
confidentiality: public
domain: computer-science
evidence:
- claim: 过滤器模式允许开发人员使用不同的标准来过滤一组对象，通过逻辑运算以解耦的方式把它们连接起来，属于结构型模式。
  claim_id: filter-pattern-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-9f2f33b8f144
    exact: Filter Pattern）或标准模式（Criteria Pattern）是一种设计模式，这种模式允许开发人员使用不同的标准来过滤一组对象，通过逻辑运算以解耦的方式把它们连接起来。这种类型的设计模式属于结构型模式，它结合多个标准来获得单一标准。用于将对象的筛选过程封装起来，允许使用不同的筛选标准动态地筛选对象。
  targets:
  - evidence_id: evidence-9f2f33b8f144
    source_id: web-computer-science-filter-pattern
id: filter-pattern
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-filter-pattern
status: published
tags:
- design-pattern
- structural
- filter
title: 过滤器模式
updated_at: '2026-09-06'
---
# 过滤器模式

## 一句话结论

过滤器模式（Filter Pattern，也称**标准模式 / Criteria Pattern**）把"筛选过程"封装成独立的过滤器对象，允许使用不同的筛选标准（Criteria）过滤一组对象，并通过逻辑与/或等运算把多个标准**以解耦的方式组合**起来获得单一标准——从而避免在客户端代码中硬编码筛选逻辑。

## 核心概念

- **过滤器接口（Filter/Criteria）**：定义筛选方法（如 `matches()`），用于根据特定条件过滤对象。
- **具体过滤器（Concrete Filter/Concrete Criteria）**：实现过滤器接口，封装具体的筛选条件与逻辑。
- **对象集合**：被过滤的对象（一组人、一组产品等具有共同属性的实例）。
- **组合过滤器**：把多个筛选器用逻辑与（AND）、逻辑或（OR）等组合，形成复杂筛选逻辑。
- **客户端（Client）**：把对象集合与过滤器结合，获得符合条件的对象。

## 工作机制

1. 定义统一的筛选接口（如 `matches(candidate)` 返回是否通过）。
2. 为每个筛选标准实现一个具体过滤器，封装各自的筛选逻辑。
3. 允许过滤器之间组合：AND/OR/NOT 组合器把多个过滤器连接成更复杂的判定。
4. 客户端只需把对象集合交给过滤器（或过滤器组合），由过滤器负责筛选，筛选逻辑与客户端解耦。

筛选标准变化时，只新增/修改过滤器类，无需改动客户端与既有过滤器——这正是该模式"解耦、可扩展"的价值。

## 示例或代码

以按性别、婚姻状态筛选 Person 列表为例：

```java
import java.util.*;
import java.util.stream.*;

public class Person {
    String name; String gender; String maritalStatus;
    Person(String n, String g, String m) { name = n; gender = g; maritalStatus = m; }
}

// Filter/Criteria 接口：筛选接口
public interface Criteria {
    List<Person> meetCriteria(List<Person> persons);
}

// Concrete Criteria：按男性筛选
public class CriteriaMale implements Criteria {
    public List<Person> meetCriteria(List<Person> persons) {
        return persons.stream()
            .filter(p -> p.gender.equalsIgnoreCase("Male"))
            .collect(Collectors.toList());
    }
}

// 组合器：逻辑与（AND），把多个标准以解耦方式连接
public class AndCriteria implements Criteria {
    private Criteria first, second;
    public AndCriteria(Criteria a, Criteria b) { first = a; second = b; }
    public List<Person> meetCriteria(List<Person> persons) {
        return second.meetCriteria(first.meetCriteria(persons)); // 逐级过滤
    }
}

// 客户端组合使用：单身男性 = 男性 AND 单身
List<Person> singles = new AndCriteria(new CriteriaMale(), new CriteriaSingle())
        .meetCriteria(persons);
```

## 常见误区

- **把过滤器模式当成普通的 if 条件**：其价值在于把筛选逻辑封装为可复用、可组合、可替换的对象。
- **忽视"解耦连接"**：多个标准通过逻辑运算组合成单一标准，而不是在客户端写一大堆 if-else。
- **把过滤与校验混淆**：过滤是"从集合中挑出符合条件的子集"；校验是"判断单个对象是否合法"。
- **认为模式只能用于 Java**：它是通用结构型模式，任何语言都可实现（函数式语言常用谓词/高阶函数组合）。
- **过度使用**：筛选条件很少且不会变化时，引入过滤器对象反而增加复杂度。

## 证据映射

| claim_id | 来源 | 要点 |
| --- | --- | --- |
| filter-pattern-definition | web-computer-science-filter-pattern | 过滤器模式允许用不同标准过滤一组对象，并通过逻辑运算解耦地连接多个标准 |

## 待验证项

定义已由 web 源（runoob 过滤器模式条目，因 Wikipedia 无 Filter pattern 专页）锚定；后续可补充 refactoring.guru 等英文源交叉验证。

## 关联知识

- [[software-design]] —— 设计模式分类：过滤器属于结构型模式。
- [[object-oriented]] —— 接口多态使筛选逻辑可复用、可组合。
- [[chain-of-responsibility]] —— 职责链的过滤/拦截思想与过滤器相关。
- [[intercepting-filter]] —— J2EE 的拦截过滤器（Intercepting Filter）对请求做预处理/过滤，同源思想。
- [[functional-programming]] —— 谓词与高阶函数是过滤器组合的现代实现方式。

## 详细章节

### 定义

过滤器模式（Filter Pattern）或标准模式（Criteria Pattern）是一种设计模式：它允许开发人员使用不同的标准来过滤一组对象，通过逻辑运算以**解耦**的方式把它们连接起来。这种类型的设计模式属于结构型模式，它结合多个标准来获得单一标准。其意图是把对象的筛选过程封装起来，允许使用不同的筛选标准动态地筛选对象。

### 参与者

- **过滤器接口（Filter/Criteria）**：定义筛选方法（如 `matches()`），作为所有筛选器的统一契约。
- **具体过滤器（Concrete Filter/Concrete Criteria）**：实现过滤器接口，具体定义筛选对象的条件与逻辑。
- **对象集合（Items/Objects to be filtered）**：被过滤的对象，通常是具有共同属性的实例。
- **客户端（Client）**：使用具体过滤器类来筛选对象集合，将集合与过滤器结合。

### 结构

```
Client → Criteria (interface) ──► ConcreteCriteriaA
                      │            ConcreteCriteriaB
                      └──► AndCriteria / OrCriteria（组合器，持有一组 Criteria）
```

组合器本身也实现 Criteria，从而可以递归组合出任意复杂的筛选树。

### 适用场景

- 对象集合需要根据不同的标准进行筛选。
- 筛选逻辑可能变化，或需要动态组合多个筛选条件。
- 希望避免在客户端代码中硬编码筛选逻辑。
- 需要按多个维度（如作者、年份、类别）灵活筛选一组实体。

### 优点与缺点

优点：

- 封装性：筛选逻辑被封装在独立的筛选器对象中。
- 灵活性：可动态添加、修改或组合筛选条件。
- 可扩展性：容易添加新的筛选标准，无需修改现有代码。

缺点：

- 复杂性：随着筛选条件增多，系统可能变得复杂。
- 性能：筛选器组合过于复杂时可能影响性能。

### 与相关模式的关系

- **与职责链（Chain of Responsibility）**：都以"链式处理/过滤"组织多个处理者，职责链可传可不传，过滤器为最终筛出子集。
- **与拦截过滤器（Intercepting Filter）**：J2EE 的拦截过滤器对请求做统一预处理，与过滤器模式同源。
- **与策略（Strategy）**：每个具体过滤器可视为一种筛选策略。

## 参考
- https://www.runoob.com/design-pattern/filter-pattern.html
