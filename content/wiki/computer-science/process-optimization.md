---
aliases: []
confidentiality: public
domain: computer-science
evidence:
- claim: 'These options control various sorts of optimizations.

    Without any optimization option, the compiler’s goal is to reduce the cost of
    compilation and to make debugging produce the expected results. Statements are
    independent: if you stop the program with a breakpoint between statements, you
    can then assign a new value to any variable or change the program counter to any
    other statement in the function and get exactly the results you expect from the
    source code.'
  claim_id: process-optimization-audit-1
  support: direct
  supporting_quotes:
  - evidence_id: evidence-b28e1a4e44dc
    exact: 'These options control various sorts of optimizations.

      Without any optimization option, the compiler’s goal is to reduce the cost of
      compilation and to make debugging produce the expected results. Statements are
      independent: if you stop the program with a breakpoint between statements, you
      can then assign a new value to any variable or change the program counter to
      any other statement in the function and get exactly the results you expect from
      the source code.'
  targets:
  - evidence_id: evidence-b28e1a4e44dc
    source_id: web-computer-science-process-optimization
id: process-optimization
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-process-optimization
- working-computer-science-process-optimization
status: published
tags:
- compiler
- optimization
- performance
title: 过程级优化
updated_at: '2026-09-06'
---
# 过程级优化

## 一句话结论

过程级优化是编译器针对"过程"（函数）进行的一类优化，包括别名消除、常数传播、内联替换、过程克隆与全局变量优化；它们通过解除编译器优化的障碍（指针别名、全局状态）、传播已知常量、消除函数调用开销、按调用上下文定制过程实现来提升程序性能。

## 核心概念

- **别名消除**：同一程序中两个以上指针引用相同存储位置即存在指针别名，会阻碍编译器优化；通过 `restrict` 声明告知编译器无别名后可放心优化。
- **常数传播**：替代表示式中已知常数的过程，一般在编译前期进行；复杂控制流下编译器难以把全部情况识别出来，建议优化人员尽量手动进行。
- **内联替换**：在被调用处复制函数代码副本（代码膨胀），将被调函数体内联到调用处，同时被调过程的形参替换为主调过程的实参，节省函数调用的时空开销。
- **过程克隆**：当过程在不同调用环境下表现出不同特性时，根据需要生成该过程的多个实现，便于对每个实现做不同优化；调用点根据上下文属性选择调用某个版本。
- **全局变量优化**：全局变量尤其是多个文件共享的全局数据结构会阻碍编译器优化，并使得程序员不便追踪其变化、难以手工优化。

## 工作机制

1. **别名消除**：编译器因担心指针别名而不敢优化（如循环向量化），加 `restrict` 声明后编译器可放心变换。
2. **常数传播**：把已知常数值代入表达式（如 `a=16` 时 `a/4` 替换为 `4`），在编译前期进行；复杂控制流下建议手动传播。
3. **内联替换**：用代码膨胀把被调函数体复制到调用处、形参换成实参，消除调用与返回开销。
4. **过程克隆**：按调用上下文生成过程的多版本（如 `j=0||j>4` 时调用可向量化版本），调用点选对应版本。
5. **全局变量优化**：尽量不用全局变量，必须用时通过参数传递等方式传递，减少对编译器优化的阻碍。

## 示例或代码

- **别名消除**：`void add(int* a, int* b)` → `void add(int* restrict a, int* restrict b)`，编译器可以做优化。
- **常数传播**：`x[i] = a / 4 + i;`（`a=16`）→ `x[i] = 4 + i;`。
- **内联替换**：循环内 `func1(&a[0], i)` 内联为 `a[i] = a[i] + i;`。
- **过程克隆**：`func(A, j)` 克隆为 `func1`（`N-j` 范围）与 `func2`（`N` 范围，后续可向量化），按 `j` 取值选择版本。
- **全局变量优化**：`func()` 直接修改全局 `a` → `func(int *a)` 通过指针参数修改 `*a`。

## 常见误区

- **以为编译器会自动消除所有别名**：复杂控制流下编译器难以把所有常数/别名情况识别出来，别名与全局状态会持续阻碍优化。
- **以为内联总是有益**：内联通过代码膨胀换取性能，是典型的空间换时间，会增大代码体积。
- **以为全局变量无害**：全局变量阻碍编译器优化、不便追踪变化、难以手工优化，并行程序尤其应避免。
- **以为常数传播全靠编译器**：复杂控制流下编译器识别困难，建议优化人员手动进行常数传播。

## 证据映射

| claim_id | 来源 | 要点 |
| --- | --- | --- |
| process-optimization-audit-1 | web-computer-science-process-optimization | 编译器优化选项控制各类优化；无优化选项时编译器以降低编译成本、保证调试结果符合预期为目标 |

## 待验证项

无

## 关联知识

- [[compilation-and-runtime-optimization]]：编译与运行优化
- [[compilation-principle]]：编译原理
- [[gcc]]：GCC 编译器及优化选项
- [[loop-optimization]]：循环级优化
- [[statement-optimization]]：语句级优化

## 详细章节

### 过程级优化

#### 别名消除

C语言中为了方便编码为变量定义了别名，但在同一程序中两个以上的指针引用相同的存储位置时，将存在指针别名的问题。

##### 例子

优化前

```c++
void add(int* a, int* b) {
    int C = 5;
    for (int i = 0; i < N; i++)
        a[i] = b[i] + C;
}

int main() {
    int a[N], b[N];
    int i;
    for (i = 0; i < N; i++) {
        a[i] = i;
        b[i] = i + 1;
    }
    add(a, b);
    printf("%d\n", a[1]);
}
```



优化后

```c++
void add(int* restrict a, int* restrict b) { // 编译器可以做优化
    int C = 5;
    for (int i = 0; i < N; i++)
        a[i] = b[i] + C;
}

int main() {
    int a[N], b[N];
    int i;
    for (i = 0; i < N; i++) {
        a[i] = i;
        b[i] = i + 1;
    }
    add(a, b);
    printf("%d\n", a[1]);
}
```





#### 常数传播

常数传播是指替代表示式中已知常数的过程，一般在编译前期进行。实际程序中可能存在复杂的控制流，编译器把所有情况的常数替换都识别出来并对程序实施正确的常数替换优化是较为困难的，因此建议优化人员尽量手动进行常数传播优化。

##### 例子

优化前

```c++
int main() {
    int a = 16;
    int i;
    const int n = 256;
    int x[n];
    for (i = 0; i < n; i++) {
        x[i] = a / 4 + i; // 优化前
    }
    return 0;
}
```



优化后

```c++
int main() {
    int a = 16;
    int i;
    const int n = 256;
    int x[n];
    for (i = 0; i < n; i++) {
        x[i] = 4 + i; // 优化后
    }
    return 0;
}
```





#### 内联替换

为了节省函数调用的时空开销，可以采用内联替换的思路优化程序，具体优化思路为函数在被调用处复制函数代码副本，并通过代码膨胀将被调函数体副本直接在调用处进行内联替换，同时被调过程内的形参也将被替换为主调过程内的实参。

##### 例子

优化前

```c++
void func1(int* x, int k) {
    x[k] = x[k] + k;
}

int main() {
    int i;
    const int n = 256;
    int a[n];
    for (i = 0; i < n; i++)
        a[i] = i;
    for (i = 0; i < n; i++)
        func1(&a[0], i);
    printf("%d", a[5]);
}
```



优化后

```c++
int main() {
    int i;
    const int n = 256;
    int a[n];
    for (i = 0; i < n; i++)
        a[i] = a[i] + i; // func1内联替换
}
```





#### 过程克隆

过程克隆是指当一个过程在不同的调用环境下表现出不同的特性时根据需要生成该过程的多个实现，便于后续针对每个实现进行不同的优化处理，程序中的调用点会根据其上下文的属性信息来选择调用过程实现的某个版本。

##### 例子

优化前

```c++
void func(int *A,int j){
    int k = 1;
    for (int i = 0; i < N-j; i++) {
       A[i + j] = A[i] + k;
    }
}
int main() {
    int A[N] = {0}, i, j;
    j = rand() % 10;
    func(A,j);
}
```



优化后

```c++
void func1(int *A,int j){
    int k = 1;
    for (int i = 0; i < N-j; i++) {
        A[i + j] = A[i] + k;
    }
}
void func2(int *A,int j){
    int k = 1;
    for (int i = 0; i < N; i++) {
        A[i+j] = A[i] + k; // 后续可以进行向量化优化
    }
}
int main() {
    int A[N] = {0}, i, j;
    j = rand() % 10;
    if(j=0||j>4)
        func2(A,j);
    else
        func1(A,j);
}
```





#### 全局变量优化

全局变量尤其是多个文件共享的全局数据结构会阻碍编译器的优化。 并且其使得程序员不便追踪其变化，难以进行手工优化。对于并行程序来说，全局变量除非在迫不得已的情况下才建议使用，就算要使用全局变量，也尽量通过参数传递的方式。

##### 例子

优化前

```c++
int a = 1;

void func() {
	int c = 14;
	a = a + c;
}

int main() {
	func();
	printf("%d", a);
}
```



优化后

```c++
int a = 1;

void func(int *a) {
	int c = 14;
	*a = *a + c;
}

int main() {
	func(&a);
	printf("%d", a);
}
```
