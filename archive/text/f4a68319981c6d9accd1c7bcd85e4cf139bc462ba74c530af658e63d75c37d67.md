# C++ vs Python

## C++和Python运行方式不同

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

  



## 静态语言和动态语言

### 主要语言

* 静态语言（强类型语言）
  * C++、Java、C、go、rust
* 动态语言（弱类型语言）
  * Python、PHP、Asp、JavaScript、Perl



### 定义

* 静态语言（强类型语言）
  * 编译时变量的数据类型可以确定
* 动态语言（弱类型语言）
  *   运行时才确定数据类型



### 优点

* 静态语言（强类型语言）
  * 编译时可以发现类型不匹配错误
  * 编译器能针对类型信息对程序做优化
* 动态语言（弱类型语言）
  * 编写代码数量少，更整洁。对阅读程序理解代码有帮助



### 缺点

* 静态语言（强类型语言）
  * 需要声明类型，代码量更多
* 动态语言（弱类型语言）
  * 无法保证变量类型，容易在运行时出现类型错误type error



## C++和Python语法对比

### hello world

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

  



### 变量定义

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

  



### 注释

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

  



### 函数

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

  



### lambda

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

  



### 类

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

  



### 继承

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
  
  



### 分支

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
  
  



### switch

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
  
  



### 循环

#### while

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

  



#### for

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

  



### 基本数据类型

* C++
* Python



## C++有而Python没有的

### struct/union

#### 示例

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



#### 作用

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



### 指针和引用

#### 示例

```c++
int number = 10; // 定义整型常量
int *ptr; // 声明指针变量
ptr = &number; // 使用引用将指针指向变量的地址
int arr[] = {0, 1, 2, 3};
for (int *b = arr; b != &arr[4]; ++b) {
    std::cout << *b << std::endl;
}
```



#### 作用

* 指针/引用是C++/C语言的精髓所在
* 本质上是拿到了数据在内存上的一个地址
* 指针可以参与运算，意味着可以操作一片内存
* 指针可以指向任何数据类型：包括基础类型和复合类型，也可以指向函数、class、class成员等等
* 裸指针有极大的内存溢出风险，为了避免风险，C++11后引入了RAII机制，即智能指针



### const

#### 示例

```c++
const int MAX_VALUE = 100;
const int *const ptr = arr;
int getNum() const {
    return num; // 函数内部不修改成员变量
}
```



#### 作用

* const阻止一个变量被改变，在函数调用过程中，变量声明中会使用
* const可以作用于指针和函数



## 总结

* C++和Python使差异非常大的语言，从运行方式、类型定义方面有着极大的不同
* C++和Python在便利性和性能方面各有千秋
* 很多开源软件项目，如TVM、TensorFlow都会把C++和Python结合起来，利用Python做API，利用C++做底层实现，这样既利用了Python的便利性，也利用了C++的高性能