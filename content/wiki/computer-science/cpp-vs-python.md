---
aliases:
- c-vs-python
confidentiality: public
domain: computer-science
evidence:
- claim: 'The Python Tutorial¶

    Tip

    This tutorial is designed for programmers that are new to the Python language,
    not beginners who are new to programming.

    Python is an easy to learn, powerful programming language. It has efficient high-level
    data structures and a simple but effective approach to object-oriented programming.'
  claim_id: cpp-vs-python-audit-1
  support: direct
  supporting_quotes:
  - evidence_id: evidence-2234ef972c4c
    exact: 'The Python Tutorial¶

      Tip

      This tutorial is designed for programmers that are new to the Python language,
      not beginners who are new to programming.

      Python is an easy to learn, powerful programming language. It has efficient
      high-level data structures and a simple but effective approach to object-oriented
      programming.'
  targets:
  - evidence_id: evidence-2234ef972c4c
    source_id: web-computer-science-c-vs-python
id: cpp-vs-python
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-c-vs-python
- working-computer-science-c-vs-python
status: published
tags:
- cpp
- python
- comparison
- programming-language
- interpreter
title: C++ vs Python
updated_at: '2026-09-06'
---
# C++ vs Python

## 一句话结论

C++ 与 Python 是差异非常大的语言：C++ 是编译型、静态（强类型）语言，先编译后运行、编译时确定类型；Python 是解释型、动态（弱类型）语言，边解释边运行、运行时才确定类型；两者在便利性和性能上各有千秋，很多开源项目（如 TVM、TensorFlow）把 C++ 与 Python 结合使用——用 Python 做 API、C++ 做底层实现。

## 核心概念

- **运行方式**：C++ 编译型语言，先编译后运行（source program → compiler → target program）；Python 解释型语言，边解释边运行（source program + input → interpreter → output）。
- **静态语言（强类型）**：C++、Java、C、go、rust；编译时变量的数据类型可以确定；优点：编译时能发现类型不匹配错误、编译器可针对类型信息优化；缺点：需要声明类型，代码量更多。
- **动态语言（弱类型）**：Python、PHP、Asp、JavaScript、Perl；运行时才确定数据类型；优点：编写代码数量少、更整洁；缺点：无法保证变量类型，容易在运行时出现类型错误（type error）。
- **C++ 有而 Python 没有的**：struct/union、指针和引用、const 等。

## 工作机制

- **语法对比**：hello world、变量定义、注释、函数、lambda、类、继承、分支、switch、循环（while/for）、基本数据类型等均展示出 C++ 需要显式声明类型、Python 更简洁的差异。
- **struct/union**：struct 是 C 语言遗留产物，能高效组织数据结构；struct 内部成员不共享内存空间，union 内部成员共享内存空间（示例中 `sizeof(a)` 为 5，`sizeof(b)` 为 4）。
- **指针和引用**：本质是拿到数据在内存上的地址；指针可以参与运算，可指向任何数据类型（基础类型、复合类型、函数、class、class 成员）；裸指针有极大内存溢出风险，C++11 后引入 RAII 机制即智能指针。
- **const**：阻止一个变量被改变，可作用于指针和函数；在函数调用过程中，变量声明中会使用。
- **工程实践**：把 C++ 与 Python 结合——Python 做 API、C++ 做底层实现，兼顾 Python 的便利性和 C++ 的高性能。

## 示例或代码

```cpp
// C++ hello world：先编译后运行，需包含头文件与 main 入口
#include <iostream>
int main() {
    std::cout << "hello world" << std::endl;
    return 0;
}
```

```python
# Python hello world：边解释边运行，一行即可
print("hello world")
```

```cpp
// C++ struct 与 union：struct 成员不共享内存，union 成员共享内存
struct a { char a; int year; };  // sizeof(a) == 5
union b { char a; int year; };   // sizeof(b) == 4
```

## 常见误区

- **以为"强类型"= "编译型"、"弱类型"= "解释型"**：静态/动态语言（强/弱类型）描述的是类型何时确定，编译/解释描述运行方式，两者是不同维度；C++ 是静态+编译型，Python 是动态+解释型。
- **以为动态语言没有类型错误**：动态语言无法保证变量类型，容易在运行时出现类型错误（type error）。
- **以为 C++ 不需要声明类型**：C++ 是静态语言，需要强制声明类型，代码量更多；Python 无需声明类型，代码更简洁。
- **以为指针只是"存地址"这么简单**：指针可参与运算、可指向任何数据类型（包括函数、class、成员），因此裸指针有极大的内存溢出风险，需要 RAII/智能指针管理。

## 证据映射

| claim_id | 来源 | 要点 |
| --- | --- | --- |
| cpp-vs-python-audit-1 | web-computer-science-c-vs-python | Python 官方教程：Python 易于学习、功能强大，具有高效高级数据结构与简洁有效的 OOP 方式 |

## 待验证项

无

## 关联知识

- [[cpp-vs-c]]：C++ 与 C 的对比
- [[cpp-vs-java]]：C++ 与 Java 的对比
- [[cpp-overview]]：C++ 语言概述
- [[cpp-class-and-raii]]：C++ RAII/智能指针

## 详细章节

### C++ vs Python

#### C++和Python运行方式不同

* C++为编译型语言，先编译后运行

  ```mermaid
  stateDiagram
  sp --> compiler
  compiler --> tp
  sp: source program
  tp: target program
  ```

  ```mermaid
  stateDiagram
  input --> tp
  tp --> output
  tp: target program
  ```

  

* Python为解释型语言，边解释边运行

  ```mermaid
  stateDiagram
  sp --> interpreter
  input --> interpreter
  interpreter --> output
  sp: source program
  ```

  



#### 静态语言和动态语言

##### 主要语言

* 静态语言（强类型语言）
  * C++、Java、C、go、rust
* 动态语言（弱类型语言）
  * Python、PHP、Asp、JavaScript、Perl



##### 定义

* 静态语言（强类型语言）
  * 编译时变量的数据类型可以确定
* 动态语言（弱类型语言）
  *   运行时才确定数据类型



##### 优点

* 静态语言（强类型语言）
  * 编译时可以发现类型不匹配错误
  * 编译器能针对类型信息对程序做优化
* 动态语言（弱类型语言）
  * 编写代码数量少，更整洁。对阅读程序理解代码有帮助



##### 缺点

* 静态语言（强类型语言）
  * 需要声明类型，代码量更多
* 动态语言（弱类型语言）
  * 无法保证变量类型，容易在运行时出现类型错误type error



#### C++和Python语法对比

##### hello world

* C++

  ```c++
  #include <iostream>
  
  int main()
  {
      std::cout << "hello world" << std::endl;
      return 0;
  }
  ```

  

* Python

  ```python
  print("hello world")
  ```

  



##### 变量定义

* C++

  ```c++
  int a = 1;
  float b = 1.0f;
  std::string str = "hello";
  ```

  

* Python

  ```python
  a = 1;
  b = 1.0;
  str = "hello";
  ```

  



##### 注释

* C++

  ```c++
  // 注释1
  
  /* 注释2 */
  ```

  

* Python

  ```python
  # 注释1
  
  '''
  注释2
  '''
  ```

  



##### 函数

* C++

  ```c++
  int getNum(int x)
  {
      return x;
  }
  ```

  

* Python

  ```python
  def get_num(x: int) -> int:
      return x;
  ```

  



##### lambda

* C++

  ```c++
  [](int a, int b) {
      return a > b;
  };
  ```

  

* Python

  ```python
  lambda a, b: a > b
  ```

  



##### 类

* C++

  ```c++
  class A {
  public:
      A();
      ~A();
  };
  ```

  

* Python

  ```python
  class A(object):
      def __init__(self):
          pass
  ```

  



##### 继承

* C++

  ```c++
  class A {
  public:
      A();
      virtual ~A();
  };
  
  
  class B : public A {
  public:
      B();
      virtual ~B();
  };
  ```

  

* Python

  ```python
  class A(object):
      def __init__(self):
          pass
  
  
  class B(A):
      def __init__(self):
          super().__init__()
          pass
  ```
  
  



##### 分支

* C++

  ```c++
  if (a) {
      ;
  } else {
      ;
  }
  ```

  

* Python

  ```python
  if a:
      pass
  else:
      pass
  ```
  
  



##### switch

* C++

  ```c++
  switch(a){
      case 1:
      	;
      	break; // 可选的
      case 2:
  		;
      	break; // 可选的
  
      // 您可以有任意数量的 case 语句
      default: // 可选的
      	;
  }
  ```

  

* Python

  ```python
  match term:
      case 1:
      	pass
      case 2:
      	pass
      case _:
      	pass
  ```
  
  



##### 循环

###### while

* C++

  ```c++
  while (i > 0) {
      i--;
  }
  ```

  

* Python

  ```python
  while i > 0:
      i -= 1
  ```

  



###### for

* C++

  ```c++
  for (int i = 0; i < 10; i++) {
      ;
  }
  ```

  

* Python

  ```python
  for i in range(10):
      pass
  ```

  



##### 基本数据类型

* C++
* Python



#### C++有而Python没有的

##### struct/union

###### 示例

```c++
struct {
    string brand;
    string model;
    int year;
} myCar1, myCar2;

myCar1.brand = "BMW";
myCar1.model = "X5";
myCar.year = 1999;
```



###### 作用

* struct是C语言遗留产物

* 使用struct结构能高效的组织数据结构

* struct和union语法一致，不同之处在于struct内部成员不共享内存空间，union中共享

  ```c++
  struct a {
      char a;
      int year;
  };
  
  union b {
      char a;
      int year;
  };
  
  sizeof(a); // 5
  sizeof(b); // 4
  ```



##### 指针和引用

###### 示例

```c++
int number = 10; // 定义整型常量
int *ptr; // 声明指针变量
ptr = &number; // 使用引用将指针指向变量的地址
int arr[] = {0, 1, 2, 3};
for (int *b = arr; b != &arr[4]; ++b) {
    std::cout << *b << std::endl;
}
```



###### 作用

* 指针/引用是C++/C语言的精髓所在
* 本质上是拿到了数据在内存上的一个地址
* 指针可以参与运算，意味着可以操作一片内存
* 指针可以指向任何数据类型：包括基础类型和复合类型，也可以指向函数、class、class成员等等
* 裸指针有极大的内存溢出风险，为了避免风险，C++11后引入了RAII机制，即智能指针



##### const

###### 示例

```c++
const int MAX_VALUE = 100;
const int *const ptr = arr;
int getNum() const {
    return num; // 函数内部不修改成员变量
}
```



###### 作用

* const阻止一个变量被改变，在函数调用过程中，变量声明中会使用
* const可以作用于指针和函数



#### 总结

* C++和Python使差异非常大的语言，从运行方式、类型定义方面有着极大的不同
* C++和Python在便利性和性能方面各有千秋
* 很多开源软件项目，如TVM、TensorFlow都会把C++和Python结合起来，利用Python做API，利用C++做底层实现，这样既利用了Python的便利性，也利用了C++的高性能
