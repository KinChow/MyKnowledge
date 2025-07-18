# 语句级优化

## 删除冗余语句

在开发和修改程序时可能遗留有死代码，死代码是指程序在一个完整的执行过程该段代码并没有得到任何的运行，也可能是一些声明了但没有用到的变量，此时可以将其删除，避免程序在运行中进行不相关的运算行为，减少运行的时间。 

### 例子

优化前

```c++
int get()
{
    int a = 1;
    int b = 2;
    int c = a + b; // 冗余语句
    int d = a - b;
    return d;
}
```



优化后

```c++
int get()
{
    int a = 1;
    int b = 2;
    // int c = a + b; // 冗余语句
    int d = a - b;
    return d;
}
```





## 代数变换

程序员在编写程序时可能忽略了代数表达式也可以进一步优化，达到简化计算缩短运行时间的目的。此代码中的计算语句可以进行简化，原计算语句中含有乘法、加法和除法三种运算，而简化后仅剩乘法运算。

### 例子

优化前

```c++
int a = 2;
int b = (a + a) + 6 * a / 2;
```



优化后

```c++
int a = 2;
int b = 5 * a;
```





## 去除相关性

### 标量扩展

语句中依赖关系的存在非常不利于进行语序调整、向量化等优化方法的开展，且由于编译器优化的局限性，需要优化人员在编写程序时尽量消除依赖关系。

标量扩展是将循环中的标量引用用编译器生成的临时数组引用替换，可以有效地消除一些由内存单元的重用而导致的依赖。 

#### 例子

优化前

```c++
for (int i = 0; i < n; i++) {
    tmp = a[i];
    a[i] = b[i];
    b[i] = tmp;
}
```



优化后

```c++
for (int i = 0; i < n; i++) {
    tmp[i] = a[i];
    a[i] = b[i];
    b[i] = tmp[i];
}
```





### 标量重命名

通过引入两个不同的变量代替现有的变量来消除依赖。 

#### 例子

优化前

```c++
int a = 2;
int b = 3;
int x = a + a;
a = 1 + b;
int y = a * a;
```



优化后

```c++
int a = 2;
int b = 3;
int x = a + a;
int c = 1 + b;
int y = c * c;
```





### 数组重命名

数组的存储单元有时被重用会导致不必要的反依赖和输出依赖，此时可以使用数组重命名的方法来消除。

数组重命名需要增加和数组大小成比例的额外内存空间，因此数组重命名的安全性和有利性都比标量重命名复杂，这种代价可能会严重影响到程序的性能，因此在实施数组重命名时应该更加谨慎。 

#### 例子

优化前

```c++
for (int i = 0; i < n; i++) {
    a[i] = a[i - 1] + x;
    b[i] = a[i] + y;
    a[i] = c[i] + z;
}
```



优化后

```c++
for (int i = 0; i < n; i++) {
    d[i] = a[i - 1] + x;
    b[i] = d[i] + y;
    a[i] = c[i] + z;
}
```





## 公共子表达式优化

当程序中表达式含有两个或者更多的相同子表达式，仅需要计算一次子表达式的值即可。

### 例子

优化前

```c++
void func(int &a, int &b)
{
    // 计算3次 a + b
    if ((a + b) > 3 && (a + b) < 10) {
        a += b;
    }
}
```



优化后

```c++
void func(int &a, int &b)
{
    // 计算1次 a + b
    int tmp = a + b;
    if (tmp > 3 && tmp < 10) {
        a = tmp;
    }
}
```





## 分支语句优化

### 合并判断条件

当程序中的分支判断条件是复杂表达式，优化人员可以将其进行优化。

#### 例子

优化前

```c++
void func(int &a, int &b, int &c)
{
    if ((a != 0) && (b != 0) && (c != 0)) {
        a += b + c;
    }
}
```



优化后

```c++
void func(int &a, int &b, int &c)
{
    int tmp = a && b && c;
    if (tmp != 0) { // 简化分支判断条件，提高流水线性能
        a += b + c;
    }
}
```





### 生成选择指令

一些平台支持选择指令，选择指令是一个三目运算指令，在某些情况下可以将分支指令用选择指令进行替换，达到提升效率的目的。

#### 例子

优化前

```c++
int x;
int a = 4;
int b = 5;
if (a > 0) {
    x = a;
} else {
    x = b;
}
```



优化后

```c++
int x;
int a = 4;
int b = 5;
x = a > 0 ? a : b; // 改进后--将分支判断移除，生成一条选择指令
```





### 运用条件编译

由于宏条件在编译时就已经确定，编译器可直接忽略不成立的分支，所以条件编译是在编译时判断。而普通分支判别是在运行时判断，故编译后的代码要长，效率也不如条件编译。

#### 例子

优化前

```c++
void arm_f() {
    printf("ON_ARM \n");
}

void x86_f(){
    printf("ON_X86 \n");
}
```



优化后

```c++
#ifdef __ARM__
void arm_f() {
    printf("ON_ARM \n");
}
#endif

#ifdef __X86__
void x86_f(){
    printf("ON_X86 \n");
}
#endif
```





### 移除分支语句

如果在程序设计时，编程人员能够将各分支路径的计算结果放到一张表中，并将分支条件转化为表中值对应的索引，那么就可以将分支跳转转化为访问表中元素，这是查表法移除分支的主要思想。

#### 例子

优化前

```c++
if (score >= 90) {
    printf("A");
} else if (score >= 80) {
    printf("B");
} else if (score >= 70) {
    printf("C");
} else {
    printf("D");
}
```



优化后

```c++
char s[] = { 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'C', 'B', 'A' };
printf("%c", s[score / 10]);
```





### 平衡分支判断

C语言中的switch运算符是程序员经常使用的一种语法，包含大量的分支，在一些程序中switch运算符可以含有数千个设置值，若直接实现这种需求的话，所得到的逻辑树会特别高。

#### 例子

优化前

```c++
switch (a) {
    case 1: func1(); break;
    case 2: func2(); break;
    case 4: func4(); break;
    case 6: func6(); break;
    case 8: func8(); break;
    case 10: func10(); break;
}
```



优化后

```c++
if (a < 5) {
    if (a < 3) {
        if (a < 2) {
            if (a == 1) {
                func1();
            }
        } else {
            if (a == 2) {
                func2();
            }
        }
    } else {
        if (a == 4) {
            func4();
        }
    }
} else {
    if (a < 7) {
        if (a == 6) {
            func6();
        }
    } else {
        if (a < 9) {
            if (a == 8) {
                func8();
            }
        } else {
            if (a == 10) {
                func10();
            }
        }
    }
}
```

