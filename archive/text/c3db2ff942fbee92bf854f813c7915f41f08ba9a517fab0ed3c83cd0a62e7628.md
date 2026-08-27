# 过程级优化

## 别名消除

C语言中为了方便编码为变量定义了别名，但在同一程序中两个以上的指针引用相同的存储位置时，将存在指针别名的问题。

### 例子

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





## 常数传播

常数传播是指替代表示式中已知常数的过程，一般在编译前期进行。实际程序中可能存在复杂的控制流，编译器把所有情况的常数替换都识别出来并对程序实施正确的常数替换优化是较为困难的，因此建议优化人员尽量手动进行常数传播优化。

### 例子

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





## 内联替换

为了节省函数调用的时空开销，可以采用内联替换的思路优化程序，具体优化思路为函数在被调用处复制函数代码副本，并通过代码膨胀将被调函数体副本直接在调用处进行内联替换，同时被调过程内的形参也将被替换为主调过程内的实参。

### 例子

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





## 过程克隆

过程克隆是指当一个过程在不同的调用环境下表现出不同的特性时根据需要生成该过程的多个实现，便于后续针对每个实现进行不同的优化处理，程序中的调用点会根据其上下文的属性信息来选择调用过程实现的某个版本。

### 例子

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





## 全局变量优化

全局变量尤其是多个文件共享的全局数据结构会阻碍编译器的优化。 并且其使得程序员不便追踪其变化，难以进行手工优化。对于并行程序来说，全局变量除非在迫不得已的情况下才建议使用，就算要使用全局变量，也尽量通过参数传递的方式。

### 例子

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

