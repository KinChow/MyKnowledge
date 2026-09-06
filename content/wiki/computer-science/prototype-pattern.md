---
aliases:
- prototype
- 原型
confidentiality: public
domain: computer-science
evidence:
- claim: 原型模式是一种创建型设计模式，当要创建的对象的类型由某个原型实例决定时，通过克隆该原型实例来产生新对象。
  claim_id: prototype-pattern-definition
  support: direct
  supporting_quotes:
  - evidence_id: evidence-12a7d834f0c6
    exact: The prototype pattern is a creational design pattern in software development.
      It is used when the types of objects to create is determined by a prototypical
      instance, which is cloned to produce new objects.
  targets:
  - evidence_id: evidence-12a7d834f0c6
    source_id: web-computer-science-prototype-pattern
id: prototype-pattern
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-prototype-pattern
status: published
tags:
- design-pattern
- creational
- prototype
- object-oriented
title: 原型模式
updated_at: '2026-09-06'
---
# 原型模式

## 一句话结论

原型模式是一种**创建型设计模式**：当**要创建的对象的类型由某个原型实例决定**时使用——通过**克隆（clone）原型实例**来产生新对象，而不是用 `new` 直接构造。它避免了像工厂方法那样在客户端为"对象创建者"派生大量子类，也能规避按标准方式创建新对象（如 `new`）的高昂成本（如复杂初始化、重 I/O 场景）。

## 核心概念

- **Prototype（原型接口）**：声明返回**自身副本**的方法（如 `clone()`）。
- **ConcretePrototype（具体原型）**：实现 `clone()`，返回自身的一份拷贝。
- **克隆（clone）**：以现有实例为模板复制出新对象，避免重复"从头构建"的成本。
- **浅拷贝 vs 深拷贝**：浅拷贝只复制引用，深拷贝递归复制引用指向的对象。
- **运行时确定类型**：具体类型在运行时由被选中的原型实例决定，无需为每种类型建立独立的创建者子类。
- **原型示例**：细胞的有丝分裂——一个细胞分裂成两个基因型完全相同的细胞，细胞"自我复制"，正是原型模式的体现。

## 工作机制

### 解决的问题

- **如何创建对象，使得具体类型可在运行时确定？**
- **如何实例化动态加载的类？**

直接在需要（使用）对象的类中创建对象是不灵活的：它把该类在编译期就绑定到特定对象，无法在运行时指定要创建哪些对象。原型模式通过如下方式解决：

1. 定义一个 `Prototype` 对象，它返回自身的一份拷贝。
2. 通过**拷贝**一个 `Prototype` 对象来创建新对象。

这允许用不同的 `Prototype` 对象配置一个类，新对象由拷贝原型产生；甚至可在**运行时增删**原型对象。

### 工作流程

1. 客户端持有一个（或多个）原型实例。
2. 需要新对象时，调用原型的 `clone()`。
3. 原型返回自身的副本（浅拷贝或深拷贝），作为新对象。
4. 运行时更换原型集合即可改变后续创建的对象类型。

### 与其他创建方式的对比

- **工厂方法**：通过**为创建者建子类**来决定产品类型；原型模式通过**克隆原型**来避免这种子类化。
- **直接 `new`**：每次从零初始化；原型复用现有实例状态，避免"以标准方式创建新对象"的高昂成本。

## 示例或代码

**Java（`Cloneable` + 深拷贝）：**

```java
import java.util.HashMap;
import java.util.Map;

class MazePrototype implements Cloneable {
    private final Map<String, String> rooms = new HashMap<>();

    public void addRoom(String id, String type) { rooms.put(id, type); }

    @Override
    public MazePrototype clone() {                 // 返回自身副本
        MazePrototype copy = new MazePrototype();
        copy.rooms.putAll(this.rooms);             // 深拷贝成员
        return copy;
    }

    public void describe() { System.out.println(rooms); }
}

// 客户端：克隆原型而非 new
MazePrototype base = new MazePrototype();
base.addRoom("r1", "wall");

MazePrototype game1 = base.clone();   // 新对象，状态由原型决定
MazePrototype game2 = base.clone();
game1.addRoom("r2", "door");          // 修改不影响原型/其他副本
```

**Python（`copy.deepcopy`）：**

```python
import copy

class Maze:
    def __init__(self):
        self.rooms = {}
    def add_room(self, rid, rtype):
        self.rooms[rid] = rtype
    def clone(self):
        return copy.deepcopy(self)     # 深拷贝，避免共享可变成员

base = Maze(); base.add_room("r1", "wall")
game1 = base.clone()
game1.add_room("r2", "door")           # 不影响 base
```

**C++（虚函数 clone 实现多态拷贝）：**

```cpp
class Prototype {
public:
    virtual ~Prototype() {}
    virtual std::unique_ptr<Prototype> clone() const = 0;
};

class MazePrototype : public Prototype {
    std::map<std::string, std::string> rooms_;
public:
    std::unique_ptr<Prototype> clone() const override {
        return std::make_unique<MazePrototype>(*this);  // 复制构造
    }
    void addRoom(const std::string& id, const std::string& t) {
        rooms_[id] = t;
    }
};
```

## 常见误区

- **忽略浅拷贝/深拷贝**：默认 `clone`（如 C++ 默认拷贝、Java 浅拷贝）只复制引用；若原型持有可变引用成员，副本间会共享状态，需实现深拷贝。
- **把原型与工厂方法对立理解**：两者都是创建对象的手段，只是取舍不同——原型避免创建者子类化、复用已有实例状态；工厂方法靠子类决定类型。
- **以为克隆"免费"**：深拷贝在大对象/深层结构上也有成本；原型模式的价值在于"复用已构造好的状态、避免重复的昂贵初始化"，而不是没有成本。
- **忽略 `clone()` 的破坏性**：Java 的 `Cloneable` 是标记接口、`Object.clone()` 不做深拷贝，需自行实现；无正确保护时易产生别名问题。
- **为简单对象滥用原型**：对象创建成本低、类型在编译期已知时，直接 `new` 更清晰，原型属于过度设计。

## 证据映射

| Claim | 来源 | 要点 |
| --- | --- | --- |
| prototype-pattern-definition | web-computer-science-prototype-pattern | 原型模式是创建型模式，当创建对象类型由原型实例决定时，通过克隆原型产生新对象；用于避免像工厂方法那样子类化创建者，并规避标准 `new` 创建对象的高昂成本；定义返回自身副本的 Prototype，通过拷贝创建新对象，原型可在运行时增删 |

## 待验证项

无。

## 关联知识

- [[factory-pattern]] —— 工厂方法模式：通过子类化创建者决定产品类型；原型通过克隆避免子类化。
- [[abstract-factory-pattern]] —— 抽象工厂模式：可用原型作为产品创建的实现手段。
- [[builder-pattern]] —— 建造者模式：分步构建复杂对象。
- [[singleton-pattern]] —— 单例模式。
- [[object-oriented]] —— 面向对象（多态、克隆语义）。
- [[software-design]] —— 软件设计总览：设计原则与设计模式。

## 详细章节

### 定义

原型模式（Prototype Pattern）是一种创建型设计模式：**当要创建的对象的类型由某个原型实例决定时，通过克隆该原型来产生新对象**。它是 GoF《设计模式》中 23 个经典模式之一。核心思想是"让实例自我复制"——一个 `Prototype` 对象提供 `clone()`，客户端通过复制它来创建新对象，从而避免为每种对象类型派生创建者子类，也避免了按标准方式（`new` + 昂贵初始化）创建对象的高成本。

### 结构（参与者）

- **Prototype**：声明克隆自身的接口（如 `clone()`）。
- **ConcretePrototype**：实现克隆方法，返回自身的副本（浅或深）。
- **Client**：持有/配置原型实例，通过 `clone()` 获得新对象；可在运行时增删原型集合。

### 适用场景

- 要创建的**对象类型在运行时确定**（动态加载类、配置驱动）。
- 对象创建成本高（复杂初始化、重 I/O、需重复构造的状态），希望**复用已有实例的状态**。
- 想**避免为每种对象类型派生创建者子类**（工厂方法在类型繁多时会子类爆炸）。
- 产品类型差异主要体现在"实例状态"而非"类结构"时，克隆比新建更直接。

### 实现要点

- `clone()` 必须正确处理**浅拷贝与深拷贝**：仅含值类型成员可浅拷贝；含可变引用成员需深拷贝。
- C++ 常用**虚函数 + 复制构造**实现多态克隆（返回 `unique_ptr<Prototype>`）。
- Java 用 `Cloneable` 标记 + 覆写 `clone()`，注意 `Object.clone()` 是浅拷贝。
- Python 可用 `copy.copy()` / `copy.deepcopy()`。
- 原型注册表（prototype registry）：把常用原型放进一个容器，运行时按需取用/克隆/新增。

### 优缺点

**优点**

- 复用已有实例状态，避免重复的昂贵初始化，创建性能更好。
- 对客户端隐藏具体类，且不新增创建者子类（优于工厂方法的子类化成本）。
- 可在**运行时**动态增删原型，灵活性高。
- 为"对象类型由状态/配置决定"的场景提供自然解法。

**缺点**

- 每个原型类都要正确实现克隆（深拷贝实现易出错）。
- 深拷贝复杂对象（嵌套引用、循环引用、非拷贝成员）成本高、易出 bug。
- Java/C++ 的克隆与语言机制（`Cloneable`、复制构造）交互微妙，误用会产生别名/共享状态问题。
- 对象创建成本低、类型编译期已知时，属于过度设计。

### 与其他模式的关系

- **与工厂方法**：原型避免"为创建者建子类"，通过克隆原型创建对象；工厂方法通过子类化创建者决定产品类型。
- **与抽象工厂**：抽象工厂可用原型作为其产品创建的内部实现（每个产品存一份原型再克隆）。
- **与单例**：单例禁止克隆（保证唯一实例）；原型恰好相反，专注于复制。
- **与建造者**：建造者逐步组装新对象；原型直接复制现成对象。

### 参考

- https://en.wikipedia.org/wiki/Prototype_pattern
