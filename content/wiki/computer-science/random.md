---
aliases: []
confidentiality: public
domain: computer-science
evidence:
- claim: 'Pseudo-random number generation

    The random number library provides classes that generate random and pseudo-random
    numbers. These classes include:

    - Uniform random bit generators (URBGs), which include both random number engines,
    which are pseudo-random number generators that generate integer sequences with
    a uniform distribution, and true random number generators (if available).

    - Random number distributions (e.g.'
  claim_id: random-audit-1
  support: direct
  supporting_quotes:
  - evidence_id: evidence-324908828b55
    exact: 'Pseudo-random number generation

      The random number library provides classes that generate random and pseudo-random
      numbers. These classes include:

      - Uniform random bit generators (URBGs), which include both random number engines,
      which are pseudo-random number generators that generate integer sequences with
      a uniform distribution, and true random number generators (if available).

      - Random number distributions (e.g.'
  targets:
  - evidence_id: evidence-324908828b55
    source_id: web-computer-science-random
id: random
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-random
- working-computer-science-random
status: published
tags:
- cpp
- random
- stl
- number-generation
title: 随机数
updated_at: '2026-09-06'
---
# 随机数

## 一句话结论

C++ 生成随机数使用 `<random>` 标准库：先用随机数引擎（如 `std::mt19937`）作为底层伪随机数发生器，再用分布对象（如 `std::uniform_int_distribution`）把引擎输出映射到目标范围；以当前时间作为种子可保证每次运行生成不同的随机数序列。

## 核心概念

- **随机数引擎（URBG）**：如 `std::mt19937`（梅森旋转算法），是伪随机数发生器，产生整数序列。随机数库提供生成随机与伪随机数的类，包括产生均匀分布整数序列的伪随机引擎，以及（若可用）真随机数发生器。
- **随机数分布（Distribution）**：如 `std::uniform_int_distribution`，把引擎输出的原始序列映射为指定范围/分布的随机数。
- **种子（Seed）**：引擎的初始状态；使用当前时间作种子可让每次运行的随机序列不同。

## 工作机制

1. 用当前时间初始化种子：`unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();`
2. 构造引擎：`std::mt19937 generator(seed);`
3. 定义分布：`std::uniform_int_distribution<int> distribution(1, 100);`（生成 1~100 的整数）
4. 调用 `distribution(generator)` 生成随机数。

## 示例或代码

```cpp
unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
std::mt19937 generator(seed);
std::uniform_int_distribution<int> distribution(1, 100);  // 生成1到100之间的随机整数
int random_number = distribution(generator);
```

完整可运行代码见下文「详细章节」。

## 常见误区

- **"随机数就是 `rand()`"**：C++ `<random>` 库把"引擎"与"分布"分离，可生成符合指定分布的随机数，能力更强。
- **"引擎输出即可直接用"**：引擎产生的是整数序列，需经分布对象（如 `uniform_int_distribution`）映射到目标范围。
- **"每次运行结果应该相同"**：以当前时间作为种子，每次运行会得到不同的随机数序列；固定种子则结果可复现。

## 证据映射

| claim_id | 来源 | 要点 |
| --- | --- | --- |
| random-audit-1 | web-computer-science-random | 随机数库提供生成随机/伪随机数的类：URBG（含均匀分布整数序列的伪随机引擎与真随机发生器）与随机数分布两大类，原文案与主题相关，保留 |

## 待验证项

无。

## 关联知识

- [[cpp]] —— C++ 语言（`<random>` 属 C++ 标准库）。

## 详细章节

### 随机数

#### 随机数的生成

使用当前时间作为随机数生成器的种子，这样可以保证每次运行程序时都会生成不同的随机数序列。
然后定义了一个 `std::uniform_int_distribution` 对象，用于生成1到100之间的随机数，然后使用 `distribution(generator)` 方法来生成随机数。



```c++
#include <iostream>
#include <random>
#include <chrono>

int main()
{
	// 使用当前时间作为种子
    unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
    std::mt19937 generator(seed);
    std::uniform_int_distribution<int> distribution(1, 100);  // 生成1到100之间的随机整数
    // 生成10个随机数
    for (int i = 0; i < 10; i++) {
        int random_number = distribution(generator);
    	std::cout << random_number << " ";
    }
    return 0;   
}
```

