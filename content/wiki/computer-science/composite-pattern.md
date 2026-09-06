---
aliases:
- 组合模式
- Composite Pattern
- Part-Whole Pattern
confidentiality: public
domain: computer-science
evidence:
- claim: 组合模式将一组对象当作同类型的单个实例来对待，其意图是把对象组合成树形结构以表示部分-整体层次。
  claim_id: composite-pattern-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-47cf0145ae18
    exact: composite pattern describes a group of objects that are treated the same
      way as a single instance of the same type of object. The intent of a composite
      is to "compose" objects into tree structures to represent part-whole hierarchies.
  targets:
  - evidence_id: evidence-47cf0145ae18
    source_id: web-computer-science-composite-pattern
id: composite-pattern
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-composite-pattern
status: published
tags:
- design-pattern
- structural
- composite
title: 组合模式
updated_at: '2026-09-06'
---
# 组合模式

## 一句话结论

组合模式（Composite Pattern）把对象组合成**树形结构**来表示"部分-整体"层次，并让客户端把单个对象（叶子）与组合对象（容器）**统一对待**——操作单个对象与操作一组对象的方式一致，从而简化客户端代码。

## 核心概念

- **Component（组件）**：统一接口，叶子与容器都实现它，定义对子节点的通用操作。
- **Leaf（叶子）**：无子节点的基本对象，直接实现 Component。
- **Composite（容器）**：有子节点的对象，实现子节点增删方法，并把 Component 操作委派给所有子节点。
- **树形结构 / 部分-整体层次**：组合用树来表达"整体由部分构成、部分可以是整体"的递归关系。
- **统一对待**：客户端不必区分叶子与容器，这是组合模式的核心价值。

## 工作机制

1. 定义统一的 `Component` 接口，声明所有对象共有的操作。
2. `Leaf` 直接实现这些操作，没有子节点。
3. `Composite` 持有子节点集合，实现增删子节点的方法，并把每个 Component 操作递归地转发给全部子节点。
4. 客户端只面对 `Component`：调用容器时操作被递归下传到整棵子树；调用叶子时直接执行。

这样，处理一棵树与处理单个节点采用同一套代码，客户端复杂度显著降低。

## 示例或代码

以文件系统（文件与文件夹）为例：

```java
import java.util.*;

// Component：统一接口
public interface FileSystemNode {
    void display(int indent);
}

// Leaf：文件
public class FileNode implements FileSystemNode {
    private String name;
    public FileNode(String name) { this.name = name; }
    public void display(int indent) {
        System.out.println("  ".repeat(indent) + name);
    }
}

// Composite：文件夹，递归委派给子节点
public class DirectoryNode implements FileSystemNode {
    private String name;
    private List<FileSystemNode> children = new ArrayList<>();
    public DirectoryNode(String name) { this.name = name; }
    public void add(FileSystemNode n) { children.add(n); }
    public void display(int indent) {
        System.out.println("  ".repeat(indent) + name + "/");
        for (FileSystemNode n : children) n.display(indent + 1);
    }
}

// 客户端统一对待叶子与容器
DirectoryNode root = new DirectoryNode("root");
root.add(new FileNode("a.txt"));
DirectoryNode docs = new DirectoryNode("docs");
docs.add(new FileNode("b.txt"));
root.add(docs);
root.display(0); // 递归打印整棵树
```

## 常见误区

- **把组合当成简单的递归**：递归是手段，组合模式的本质是"叶子与容器实现同一接口、客户端统一对待"。
- **把子节点管理方法放进 Component 造成安全性问题**：早期 GoF 建议放进 Component（透明性），近期描述常把它限定在 Composite 中（安全性），需权衡透明与安全。
- **误以为组合只用于 UI/文件树**：凡是"部分-整体"层次都适用，如公司组织、菜单、语法树、目录树。
- **把组合与聚合混为一谈**：组合模式是设计模式；"组合/聚合"是对象关系术语，二者概念层级不同。

## 证据映射

| claim_id | 来源 | 要点 |
| --- | --- | --- |
| composite-pattern-definition | web-computer-science-composite-pattern | 组合模式把一组对象当作同类型单个实例处理，组合成树结构表示部分-整体层次 |

## 待验证项

无。定义已由 web 源（Wikipedia Composite pattern 条目）锚定。

## 关联知识

- [[software-design]] —— 设计模式分类：组合属于结构型模式。
- [[object-oriented]] —— 多态与递归是组合模式的语言基础。
- [[generic-tree]] —— 通用树的定义与遍历，是组合模式的数据结构基础。
- [[decorator-pattern]] —— 装饰器可视为只有一个子节点的组合对象，常与组合结合。
- [[bridge-pattern]] —— 桥接与组合可同时使用。
- [[class-diagram]] —— 用 UML 类图表达 Component/Leaf/Composite 的关系。

## 详细章节

### 定义

组合模式（Composite Pattern）是 GoF 二十三种设计模式之一，属于结构型模式，是一种"分区式"设计模式。它描述一组对象被当作同类型的单个实例来对待。组合的意图是把对象组合成树形结构以表示"部分-整体"层次，让客户端能够统一地对待单个对象与组合对象。

### 参与者

- **Component**：为组合中的对象声明接口；在适当情况下实现所有类共有的默认行为，并声明访问与管理子组件的接口。
- **Leaf**：叶子节点，没有子节点，实现 Component 的行为。
- **Composite**：定义有子节点的行为，存储子组件，实现与子组件有关的操作（增删、委派）。
- **Client**：通过 Component 接口操作组合结构。

### 结构

```
Client → Component (interface)
            ↑            ↑
          Leaf      Composite (children: Component[])
```

Composite 递归包含 Component，形成树；客户端统一通过 Component 访问。

### 适用场景

- 需要表示对象的"部分-整体"层次结构。
- 希望客户端忽略组合对象与叶子对象的差异，统一处理。
- 需要递归处理树形结构（渲染、遍历、统计、序列化等）。

### 优点与缺点

优点：

- 简化客户端：客户端统一处理叶子与容器，无需 if-else 区分。
- 易于新增节点类型：符合开闭原则，新叶子/容器类型无需改动客户端。
- 天然递归：遍历与操作整棵树很自然。

缺点：

- 设计过于一般化：区分叶子与容器的成本被掩盖，可能让部分操作（如仅容器才有的 add）语义混乱。
- 组件接口可能过于宽泛，违反接口隔离原则（ISP）。
- 树深度过大时递归实现有性能与栈溢出风险。

### 与相关模式的关系

- **与装饰器（Decorator）**：装饰器可看作只有一个子节点的组合；两者结构相关，常组合使用。
- **与桥接（Bridge）**：组合与桥接常结合，桥接让组合树中节点的实现可替换。
- **与迭代器（Iterator）**：迭代器可用来遍历组合结构。
- **与职责链（Chain of Responsibility）**：与组合结合，让请求沿树向上传递。

## 参考
- https://en.wikipedia.org/wiki/Composite_pattern
