---
aliases: []
confidentiality: public
domain: computer-science
evidence:
- claim: LLVM 的优化是通过遍历程序某一部分的 passes 来实现的。
  claim_id: compilation-principle-claim-1
  support: direct
  supporting_quotes:
  - evidence_id: evidence-e5a7dc42e0a0
    exact: Optimizations are implemented as Passes that traverse some portion of a
      program to either collect information or transform the program.
  targets:
  - evidence_id: evidence-e5a7dc42e0a0
    source_id: web-computer-science-compilation-and-runtime-optimization
- claim: LLVM 的 passes 分为三类，分别是 Analysis、Transform 和 Utility。
  claim_id: compilation-principle-claim-2
  support: direct
  supporting_quotes:
  - evidence_id: evidence-0cbb21662389
    exact: The table below divides the passes that LLVM provides into three categories.
  - evidence_id: evidence-f0fb707195ca
    exact: The table below divides the passes that LLVM provides into three categories.
      Analysis passes compute information that other passes can use or for debugging
      or program visualization purposes. Transform passes can use (or invalidate)
      the analysis passes. Transform passes all mutate the program in some way. Utility
      passes provide some utility but don’t otherwise fit categorization.
  targets:
  - evidence_id: evidence-0cbb21662389
    source_id: web-computer-science-compilation-and-runtime-optimization
  - evidence_id: evidence-f0fb707195ca
    source_id: web-computer-science-compilation-and-runtime-optimization
- claim: Analysis passes 会为其他 passes 计算信息，也可用于调试或程序可视化。
  claim_id: compilation-principle-claim-3
  support: direct
  supporting_quotes:
  - evidence_id: evidence-39f1806db90e
    exact: Analysis passes compute information that other passes can use or for debugging
      or program visualization purposes.
  targets:
  - evidence_id: evidence-39f1806db90e
    source_id: web-computer-science-compilation-and-runtime-optimization
- claim: Transform passes 会以某种方式修改程序。
  claim_id: compilation-principle-claim-4
  support: direct
  supporting_quotes:
  - evidence_id: evidence-0cfd414d87c7
    exact: Transform passes all mutate the program in some way.
  targets:
  - evidence_id: evidence-0cfd414d87c7
    source_id: web-computer-science-compilation-and-runtime-optimization
id: compilation-principle
kind: knowledge
publication_scope: public
related: []
schema_version: wiki/v1
sources:
- web-computer-science-compilation-and-runtime-optimization
- working-computer-science-compilation-principle
status: published
tags:
- compiler
- gcc
- llvm
- linker
- assembly
title: 编译原理
updated_at: '2026-09-06'
---
# 编译原理

## 一句话结论

编译原理研究如何把源程序转换为可运行的目标程序：使用编译器（如 gcc）可把源程序经预处理、编译、汇编、链接四步生成目标程序；编译器内部由词法分析、语法分析、语义分析与中间代码生成、代码优化、目标代码生成等多个阶段组成，符号表管理和错误处理贯穿所有阶段，优化可以以 LLVM 的 pass 形式实现。

## 核心概念

- **源程序与目标程序**：源程序是用户书写的代码（如 `hello.c`），目标程序是可执行程序（如 `hello.exe`），由编译器生成。
- **目标文件格式**：主要分为 PE（Portable Executable，Windows 使用，也称 PE/COFF）与 ELF（Executable and Linking Format，取代早期 a.out，Linux/unix/vxWorks 使用）两类。
- **目标文件内容**：Text（代码，一般需要重定位）、Data（全局数据）、BSS（未初始化的全局数据）。
- **编译器与解释器**：编译器输入源文件、输出目标文件，分多阶段执行；解释器不生成目标代码，直接执行源程序指定运算，两者都含词法、语法、语义分析。
- **词法/语法/语义分析**：词法分析产生 Token 序列；语法分析（编译程序核心）把记号序列分解成语法短语并生成语法树；语义分析做静态语义检查并翻译生成中间代码。
- **中间代码**：和目标机器无关，易于生成；表示形式有逆波兰式、三元式、四元式（三地址语句）。
- **代码优化**：对代码做等价变换，使运行结果相同而运行速度加快或占用存储空间减少，遵循等价、有效、合算原则。

## 工作机制

- **gcc 编译四步**：预处理（`gcc -E hello.c > hello.i`）→ 编译（`gcc -S hello.i -o hello.s`）→ 汇编（`gcc -c hello.s -o hello.o`）→ 链接（`gcc hello.o -o hello.exe`）。预处理文件是文本格式 C 代码，汇编文件是汇编，目标文件和目标程序是二进制文件。
- **目标程序运行**：链接器把多个目标文件和库链接在一起生成程序，并修改重定位代码、指定首条指令；OS 启动时 BIOS 引导将 OS 代码加载到指定地址，运行程序时由 OS 加载器分配地址空间、读入代码和数据、填充 BSS、创建堆栈段并跳转到第一条指令。
- **词法分析**：根据词法规格读入字符，产生记号（Token）序列；用正规表达式和有限状态机描述实现，典型工具如 lex；同时滤掉注释、空格、换行符。
- **语法分析**：在词法分析基础上按语法规则将记号序列分解成各类语法短语，判断是否符合语法规则并生成语法树；通常由上下文无关文法（常用 BNF 描述）定义，过程是递归的或使用显式分析栈。
- **语法分析方法**：自顶向下（LL(1)、递归子程序法、预测分析法）与自底向上（LR(1)、LALR(1)，经典工具 yacc 使用 LALR(1)）。
- **语义分析与中间代码**：基于属性文法和语法制导翻译，做类型检查、控制流检查、一致性检查、作用域分析等；中间代码与目标机器无关，使用一种中间代码只需 m+n 个转换关系（否则需 m*n 个）。
- **代码优化**：分为源代码算法优化与编译优化（与机器无关的中间代码优化 + 依赖机器的目标代码优化）；中间代码优化技术有局部优化（删除公共子表达式、删除无用赋值、合并已知量、临时变量改名、交换语句位置、代数变换）、循环优化（代码外提、强度消弱、变换循环控制条件、循环展开、循环合并）、全局优化。

## 示例或代码

生成目标程序：

```bash
gcc hello.c -o hello.exe
```

四步分解：

```bash
gcc -E hello.c > hello.i   # 预处理，得到文本格式 C 代码
gcc -S hello.i -o hello.s  # 编译，得到汇编文件
gcc -c hello.s -o hello.o  # 汇编，得到二进制目标文件
gcc hello.o -o hello.exe   # 链接，得到二进制目标程序
```

中间代码表示形式示例：

- 逆波兰式（后缀表达式）：`a+b` 表示为 `ab+`
- 三元式：形如 `(op, arg1, arg2)`
- 四元式（三地址语句）：形如 `(op, arg1, arg2, result)`

## 常见误区

- **函数/变量名长短会影响编译与运行性能**：名字的解析发生在词法阶段，编译器的开销主要在语法分析和代码优化，名字长短不影响编译速度和程序运行性能。
- **运算符优先级要靠记**：只需记住括号是最高优先级，不确定优先级时请使用括号。
- **编译器优化是全局、自动充分的**：实际上编译器优化是局部优化（针对单个 C 文件、单个函数、基本块），因为编译器知道的信息非常有限，开发人员日常编码时也需主动做优化（减少函数调用、避免不必要的初始化、4 字节对齐、`likely()/unlikely()`、用本地指针替换全局变量等）。

## 证据映射

| claim_id | 来源 | 要点 |
| --- | --- | --- |
| compilation-principle-claim-1 | web-computer-science-compilation-and-runtime-optimization | LLVM 优化以 Pass 形式实现，Pass 遍历程序某一部分来收集信息或变换程序 |
| compilation-principle-claim-2 | web-computer-science-compilation-and-runtime-optimization | LLVM 的 passes 分为 Analysis、Transform、Utility 三类 |
| compilation-principle-claim-3 | web-computer-science-compilation-and-runtime-optimization | Analysis passes 为其他 passes 计算信息，也可用于调试或程序可视化 |
| compilation-principle-claim-4 | web-computer-science-compilation-and-runtime-optimization | Transform passes 都会以某种方式修改程序 |

## 待验证项

无

## 关联知识

- [[compilation-and-runtime-optimization]]：编译与运行优化的整体流程与 LLVM 编译器架构
- [[gcc]]：GCC 编译器的使用、选项与常见错误
- [[loop-optimization]]：循环级优化
- [[statement-optimization]]：语句级优化
- [[compilers-on-linux]]：Linux 下的编译器

## 详细章节

### 编译原理

#### 源程序

* 使用编译器生成目标程序`gcc hello.c -o hello.exe`
*   可分为四个步骤
    * 预处理：`gcc -E hello.c > hello.i`
    * 编译：`gcc -S hello.i -o hello.s`
    * 汇编：` gcc -c hello.s -o hello.o`
    * 链接：` gcc hello.o -o hello.exe`
*   预处理文件（hello.i），文本格式c代码
*   汇编文件（hello.s），汇编
*   目标文件（hello.o），二进制文件
*   目标程序（hello.exe），二进制文件



#### 目标文件

主要格式

* PE（Portable Executable）
    * Windows使用，也称PE/COFF
* ELF (Executable and Linking Format)
    * 取代早期a.out格式
    * Linux, unix, vxWorks使用



主要内容

*   Text 代码，一般需要重定位
*   Data 全局数据
*   BSS 未初始化的全局数据



目标程序

*   目标程序内容和格式与目标文件相同
*   链接器将多个目标文件和库链接在一起生成程序
*   链接器修改重定位代码，指定首条指令



目标程序的运行

* 启动OS
    *  Bios引导
        *  不支持虚拟空间，bios将OS代码加载到某个指定地址，Linux PPC一般是0地址；
        *  修改重定位代码，将bss段填充0，跳转指定地址运行
*   运行程序
    *   将程序和库加载到内存
    *   修改重定位代码，跳转到首条指令执行
    *   OS加载器
        *  支持虚拟空间的操作系统，如Linux/Windows支持多进进程，一般将程序加载到一个固定位置（虚拟地址）开始运行，Linux为128M+，Windows为4
        *  从目标文件中读取头部信息，计算地址空间并分配，包括代码段、数据段等
        *  读入程序的代码和数据，修改重定位代码
        *  将程序末尾的bss段空间填充为0
        *  创建堆栈段，设置参数和环境变量等运行时信息
        *  跳转到程序第一条指令运行



#### 编译器

* 编译器
    *   输入是源文件，输出是目标文件（目标程序）。
    *   分多个阶段执行，其中符号表管理和错误处理贯穿所有阶段。
* 解释器
    *   不生成目标代码，直接执行源程序的指定的运算。
    *   相同点：词法、语法、语义分析
*   举例
    *   C、C++
    *   Perl、python、ruby、lua
    *   Java
    *   Html、xml、js



##### 词法分析器

词法分析

* 根据词法规格，读入字符，产生记号（Token）序列，提交给语法分析使用。
* 词法规则使用正规表达式和有限状态机描述实现，典型工具如lex。
*  词法分析同时滤掉注释、空格、换行符等，并将出错信息与源文件位置关联起来

函数变量名的长短是否影响编译性能？如编译速度、运行性能、生成文件大小
函数名和变量名的解析在词法阶段，编译器的开销主要在语法分析和代码优化，名字长短不影响编译速度和程序运行性能。



##### 语法分析器

语法分析

*  是编译程序的核心，在词法分析的基础上，根据语法规则，将记号序列分解成各类语法短语，判断是否符合语法规则，生成语法树。
*   通常由上下文无关文法规则描述
*   与正则表示式主要区别在于上下文无关文法的规则是递归的，
    *  如while嵌套while，if嵌套if，表达式嵌套等
    *  语法分析的过程也是递归的或使用显式的分析栈
* 通常使用BNF范式描述上下文无关文法。



##### 语法二义性

* 优先权和结合性
    * 重定义上面的表达式消除二义性
    * 运算符的优先级有多少种？
        * 记住括号是最高优先级就可以了，不确定优先级时请使用括号。
*  悬挂else问题，两种方法
    *   使用最近嵌套规则
        * 即else与前面最近的一个if配对
    * 有的语言要求所有的if都有一个配对的关键字如endif
        * BASIC必须if end配对。



##### 语法分析方法

语法分析方法也即构造语法树的算法，分自顶向下和由底向上两种方法。

* 自顶向下分析法就是从文法的开始符号出发，试图推导出与输入的单词串完全匹配的语句。
    * 又分确定性和不确定性两种：后者很强大，但是需要回溯，效率低，很少使用；前者要求满足LL(1)文法，有一定的限制，但实现简单直观，便于手工或自动构造；
    *  LL(1)文法与分析方法：从左L向右扫描输入串，分析过程中采用最左L推导，只需向右看1个符号就可确定如何推导。
    *  手工构造，递归子程序法：文法中每个非终结符编写一个递归过程，每个过程的功能是识别由该非终结符推出的串。
    *  自动构造，预测分析法：判断是否LL(1)文法，根据文法构造预测分析表，按算法入栈出战分析。递归 栈
* 由底向上分析是自顶向下预测分析推导的逆过程
    *  有LR(1)和LALR(1)等分析方法
    *  经典的语法分析器生成工具yacc就是使用LALR(1)方法



##### 语法分析和中间代码

* 语义分析：
    *   基于属性文法和语法制导翻译
    *  语法检查，审查每个语法结构的静态语义，验证语法结构合法性。
        * 类型检查、控制流检查、一致性检查、相关名字检查、名字的作用域分析等。
    * 如果静态语义正确，翻译生成中间代码
        * 也可以生成实际的目标代码，目前大多都生成中间优化后再生成目标代码。
* 中间代码
* 和目标机器无关，易于生成
    * 如gcc可支持多种语言、多种目标机器，使用一种中间代码，只需要各种语言到中间代码的转换，中间代码倒各种机器代码间的转换，有m+n个转换关系；如果不使用中间代码，则有m*n个转换关系。
    *   逻辑结构清楚，利于进行与机器无关的优化
    *  简化编译器设计
    *  表示形式
        * 逆波兰式，后缀表达式，如`a+b`表示为` ab+`
        * 三元式，形如`(op, arg1, arg2)`
        * 四元式，三地址语句，更接近目标代码，形如`(op, arg1, arg2, result)`



##### 代码优化

* 代码优化：
    *   对代码进行等价变换，使得变换后的代码运行结果与变换前代码运行结果相同，而运行速度加快或占用存储空间减少。
        *  等价原则：经过优化后不应改变程序运行的结果；
        *  有效原则：使优化后所产生的目标代码运行时间较短，占用的存储空间较小；
        *  合算原则：应尽可能以较低的代价取得较好的优化效果。
* 优化分类
    * 源代码算法优化
        * 可能数量级的优化提升，一般只优化关键代码，否则代价太大。
    * 编译优化
        *  可能提升xx%或者几倍左右，可对所有代码优化
        *  分为与机器无关的中间代码优化和依赖机器的目标代码优化
* 中间代码优化技术
    *   局部优化：对基本块范围内的优化
        * 删除公共子表达式
        *  删除无用赋值
        * 合并已知量
        *  临时变量改名
        *  交换语句的位置
        *  代数变换
    * 循环优化：对循环中的代码进行优化
        *  代码外提
        *  强度消弱
        * 变换循环控制条件
        * 循环展开
        * 循环合并
    * 全局优化：整个程序范围内的优化
        * 编译器优化较少



##### 帮助编译器优化

* 编译器优化是局部优化
    *   针对单独的c文件、单个函数、基本块的优化
        * 因为编译器知道的信息非常有限，开发人员在日常编写代码时也可以做很多优化
    * 减少函数调用。
        * 函数调用需要参数压栈和退栈，寄存器保存，和指令跳转等。
          * 一是要减少不必要的函数调用
          * 二要减少函数调用层次、避免递归算法、通过宏替换简单函数、使用inline函数等
    *   避免不必要的初始化，特别是memset初始化
    *   消除不必要的存储器引用
    *   尽可能采用4字节对齐的数据结构
    *   利用`likely()`/`unlikely()`告诉编译器哪个分支可能性更大，避免不必要的跳转
    *   用本地指针替换复杂数据结构的全局变量，减少地址重复计算
