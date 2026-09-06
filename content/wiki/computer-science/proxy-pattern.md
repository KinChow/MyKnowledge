---
aliases:
- 代理模式
- Proxy Pattern
- Surrogate Pattern
confidentiality: public
domain: computer-science
evidence:
- claim: 代理模式是一种软件设计模式，其中代理类是作为某事物接口的类，可用于网络连接、内存大对象、文件等。
  claim_id: proxy-pattern-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-5596c3d426d5
    exact: 'the proxy pattern is a software design pattern which is a class functioning
      as an interface to something else. The proxy could interface to anything: a
      network connection, a large object in memory, a file, or some other resource
      that is expensive or impossible to duplicate.'
  targets:
  - evidence_id: evidence-5596c3d426d5
    source_id: web-computer-science-proxy-pattern
id: proxy-pattern
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-proxy-pattern
status: published
tags:
- design-pattern
- structural
- proxy
title: 代理模式
updated_at: '2026-09-06'
---
# 代理模式

## 一句话结论

代理模式（Proxy Pattern）用一个**代理对象充当真实对象的替身/接口**，客户端通过代理访问真实对象，代理在转发请求的同时可附加额外逻辑——如**缓存、访问控制、懒加载、远程转发**——而客户端无需感知真实对象的存在。

## 核心概念

- **Subject（主题接口）**：真实对象与代理共同实现的接口。
- **RealSubject（真实对象）**：真正执行业务的对象，通常昂贵或难以直接创建/访问。
- **Proxy（代理）**：实现 Subject，持有 RealSubject 引用，转发请求并附加逻辑。
- **替身语义**：代理是可被客户端调用的包装/代理对象，客户端不区分它和真实对象。
- **附加逻辑**：缓存、前置条件检查、权限校验、日志、远程调用等。

## 工作机制

1. `RealSubject` 与 `Proxy` 实现同一个 `Subject` 接口。
2. 客户端持有 `Subject` 引用，运行时拿到的是 `Proxy`。
3. `Proxy` 在调用真实方法前可做前置处理（权限、缓存、懒加载判定等），随后把请求转发给 `RealSubject`，必要时做后置处理。
4. 客户端无法（也无需）分辨自己操作的是真实对象还是代理。

由于代理实现了与真实对象相同的接口，可无缝替换，这正是代理模式"替代访问"的关键。

## 示例或代码

以"图片懒加载代理"为例（真实图片加载昂贵，代理延迟加载）：

```java
// Subject：主题接口
public interface Image {
    void display();
}

// RealSubject：真实对象，加载昂贵
public class RealImage implements Image {
    private String filename;
    public RealImage(String f) { filename = f; loadFromDisk(); }
    private void loadFromDisk() { System.out.println("Loading " + filename); }
    public void display() { System.out.println("Displaying " + filename); }
}

// Proxy：代理，延迟创建真实对象并转发
public class ImageProxy implements Image {
    private RealImage real;
    private String filename;
    public ImageProxy(String f) { filename = f; }
    public void display() {
        if (real == null) real = new RealImage(filename); // 懒加载
        real.display();
    }
}

// 客户端只面对 Image 接口
Image img = new ImageProxy("photo.jpg");
img.display(); // 首次显示时才真正加载
```

## 常见误区

- **把代理与装饰器混淆**：两者都包装对象、结构相似；装饰器"添加行为"，代理"控制访问/替身"。
- **把代理与适配器混淆**：代理不改接口（与真实对象同接口），适配器转换接口。
- **误以为代理只能做一种事**：代理可组合远程、虚拟、保护、缓存、日志等多种关注点。
- **以为代理必然懒加载**：懒加载只是虚拟代理的一种职责，远程/保护/缓存代理各有侧重。
- **把动态代理与静态代理对立**：静态代理手写一个类；动态代理（如 Java Proxy）在运行期生成代理类，本质同一模式。

## 证据映射

| claim_id | 来源 | 要点 |
| --- | --- | --- |
| proxy-pattern-definition | web-computer-science-proxy-pattern | 代理是作为某事物接口的类，为昂贵或难以复制的资源充当替身 |

## 待验证项

无。定义已由 web 源（Wikipedia Proxy pattern 条目）锚定。

## 关联知识

- [[software-design]] —— 设计模式分类：代理属于结构型模式。
- [[object-oriented]] —— 接口与多态使代理可无缝替换真实对象。
- [[decorator-pattern]] —— 与代理结构相似；装饰器加行为，代理控访问。
- [[adapter-pattern]] —— 代理不改接口，适配器改接口。
- [[facade-pattern]] —— 外观隐藏子系统；代理控制对单个对象的访问。
- [[lazy-loading]] —— 虚拟代理常用懒加载实现。
- [[class-diagram]] —— 用 UML 类图表达 Subject/Proxy/RealSubject 关系。

## 详细章节

### 定义

代理模式（Proxy Pattern）是 GoF 二十三种设计模式之一，属于结构型模式。它是一个**作为某事物的接口**的类，可代理网络连接、内存中的大对象、文件或其它昂贵/难以复制的资源。简言之，代理是客户端调用、以访问背后真实服务对象的包装或代理对象。代理可以是简单转发，也可提供额外逻辑（如对资源密集操作做缓存，或在调用真实对象前检查前置条件）。

### 参与者

- **Subject**：定义 RealSubject 与 Proxy 的共同接口，使 Proxy 可替代 RealSubject。
- **RealSubject**：真实对象，Proxy 所代表的对象。
- **Proxy**：持有对 RealSubject 的引用，控制对其的访问，并实现 Subject 接口。
- **Client**：通过 Subject 接口与对象交互。

### 结构

```
Client → Subject (interface)
            ↑        ↑
         Proxy ──► RealSubject
```

### 常见代理类型

- **远程代理（Remote Proxy）**：本地对象代表异地地址空间的对象（如 ATM 代理远程银行信息）。
- **虚拟代理（Virtual Proxy）**：延迟创建/加载昂贵的对象（懒加载）。
- **保护代理（Protection Proxy）**：访问前检查权限等前置条件。
- **缓存代理（Cache Proxy）**：对资源密集操作结果做缓存。
- **智能引用/日志代理**：在访问真实对象时附加引用计数、日志等。

### 适用场景

- 需要控制对某对象的访问（权限、频控）。
- 需要在访问真实对象时附加额外功能（缓存、日志、懒加载、远程转发）。
- 对象昂贵或位于远程，希望以替身代理访问。
- 需要延迟创建开销大的对象。

### 优点与缺点

优点：

- 职责清晰分离：访问控制、缓存等关注点与业务逻辑解耦。
- 符合开闭原则：新增代理类型无需修改真实对象与客户端。
- 可透明替换真实对象，客户端无感。

缺点：

- 增加系统间接层，类数量增多。
- 代理层处理不当可能引入延迟或额外开销。
- 若代理与真实对象接口高度耦合，扩展受限于 Subject 接口。

### 与相关模式的关系

- **与装饰器（Decorator）**：结构相同（都包装对象）；目的不同——装饰器增强行为，代理控制访问。
- **与适配器（Adapter）**：适配器改变对象的接口，代理实现与真实对象相同的接口。
- **与外观（Facade）**：外观提供简化接口，代理保持原接口并控制访问。

## 参考
- https://en.wikipedia.org/wiki/Proxy_pattern
