# content/working 全量清单（161 文件 = 153 唯一内容）

生成：2026-09-02 · 数据源 `var/reports/working-inventory.json`（口径与 upgrade-worklist-a.json 一致，A 档零漂移）

## 摘要

| 档 | 目录 | 文件数 | 唯一内容 | 有可快照文本出处 | 仅视频 | 零外链 | 补充来源所需操作 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A 档 | `a-external` | 62 | 57 | 59 | 3 | 0 | `source --url` 快照 + 锚定引文即可升级（llvm 实测一次通过） |
| B 档 | `b-final` | 45 | 44 | 0 | 0 | 45 | 需 owner 逐篇识别出处（融合改写，无 URL 可抓）；判不了走 personal 通道（待决） |
| C 档 | `c-intermediate` | 54 | 52 | 0 | 0 | 54 | 多为碎片，先按"是否服务内容重构"决定删留，再补来源 |

## A 档 `a-external`（62）

_有外链 → 可快照文本出处即可升级；**先处理 5 组重复对**_

| # | source_id | title | 正文 | 链(文本+视频) | 域名 | 备注 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `a-guide-of-compiler-vectorization` | 编译器向量化指南 | 21629 | 15+0 | gnu.org, llvm.org | 有重复副本: `compiler-vectorization-guide`; 大页21629字 |
| 2 | `activity-diagram` | 活动图 | 567 | 3+0 | plantuml.com, uah.edu… | - |
| 3 | `adb` | ADB | 8293 | 5+0 | android.com, google.com… | 大页8293字 |
| 4 | `android-camera-architecture` | android camera 架构 | 5006 | 5+0 | csdn.net, github.com… | - |
| 5 | `architecture-and-organization` | ARM体系结构与现代处理器设计 | 16926 | 1+0 | androidauthority.com | 大页16926字 |
| 6 | `arm-neon` | Neon | 2756 | 3+0 | arm.com | 有重复副本: `neon` |
| 7 | `arm-software-optimization` | arm软件性能优化 | 9438 | 2+0 | kernel.org, zhihu.com | 大页9438字 |
| 8 | `auto-exposure` | 自动曝光 | 1142 | 1+0 | wikipedia.org | - |
| 9 | `black-level-correction` | 黑电平与线性化 | 3130 | 3+0 | csdn.net, deepinout.com… | - |
| 10 | `circular-linked-list` | 循环链表 | 8621 | 4+0 | geeksforgeeks.org | 大页8621字 |
| 11 | `cl-mem` | cl_mem | 2366 | 2+0 | khronos.org | - |
| 12 | `class-and-structure` | 类和结构 | 8047 | 4+0 | microsoft.com | 大页8047字 |
| 13 | `class-diagram` | 类图 | 3133 | 4+0 | github.io, uah.edu… | - |
| 14 | `code-server` | code-server | 784 | 3+0 | code-server.dev, github.com… | - |
| 15 | `collaboration-diagram` | 协作图 | 351 | 2+0 | uah.edu, tutorialspoint.com | - |
| 16 | `compiler-vectorization-guide` | 编译器向量化指南 | 21629 | 15+0 | gnu.org, llvm.org | dup of `a-guide-of-compiler-vectorization`; 大页21629字 |
| 17 | `compilers-on-linux` | Linux的编译器 | 5076 | 9+0 | arm.com, gnu.org | 有重复副本: `linux-compilers` |
| 18 | `compilers-on-windows` | Windows的编译器 | 590 | 3+0 | github.com, microsoft.com | - |
| 19 | `component-diagram` | 组件图 | 479 | 3+0 | plantuml.com, uah.edu… | - |
| 20 | `cpp-key-words` | 关键字 | 6543 | 94+0 | cppreference.com | 有重复副本: `key-words` |
| 21 | `cpp-overview` | C++概述 | 1841 | 1+0 | github.io | - |
| 22 | `cpu-history` | CPU 发展历史 | 561 | 3+0 | wikipedia.org, mit.edu | 有重复副本: `history` |
| 23 | `davinci` | 华为达芬奇（DaVinci）架构 | 4401 | 2+0 | csdn.net, cmc.ca | - |
| 24 | `defective-pixel-correction` | 坏点矫正 | 3434 | 5+0 | huaweicloud.com, 51cto.com… | - |
| 25 | `demosaic` | 去马赛克 | 1693 | 2+0 | google.com, ipol.im | - |
| 26 | `deployment-diagram` | 部署图 | 451 | 3+0 | plantuml.com, uah.edu… | - |
| 27 | `doubly-circular-linked-list` | doubly-circular-linked-list | 1640 | 1+0 | geeksforgeeks.org | - |
| 28 | `doubly-linked-list` | 双链表 | 2634 | 2+0 | geeksforgeeks.org | - |
| 29 | `dumpsys` | dumpsys | 394 | 1+0 | android.com | - |
| 30 | `fastboot` | fastboot | 1979 | 3+0 | csdn.net | - |
| 31 | `gcc` | GCC | 19470 | 3+0 | gnu.org, gnu.org下载 | 大页19470字 |
| 32 | `gdb` | gdb | 249 | 1+0 | gitbooks.io | - |
| 33 | `gpu-overview` | GPU | 9121 | 2+0 | zhaokangkang.com, zhihu.com | 大页9121字 |
| 34 | `harvard-architecture` | 哈佛结构 | 463 | 1+0 | wikipedia.org | - |
| 35 | `history` | CPU 发展历史 | 561 | 3+0 | wikipedia.org, mit.edu | dup of `cpu-history` |
| 36 | `image-file-format` | 图像文件格式 | 2184 | 2+0 | ffmpeg.org, github.com | - |
| 37 | `key-words` | 关键字 | 6543 | 94+0 | cppreference.com | dup of `cpp-key-words` |
| 38 | `linux-compilers` | Linux的编译器 | 5076 | 9+0 | arm.com, gnu.org | dup of `compilers-on-linux` |
| 39 | `linux-performance-tools` | linux性能分析工具 | 762 | 1+0 | testerhome.com | - |
| 40 | `loop-optimization` | 循环级优化 | 15346 | 0+10 |  | video-only; 大页15346字 |
| 41 | `mali-gpu-overview` | Mali GPU 概述 | 11871 | 1+0 | wikipedia.org | 大页11871字 |
| 42 | `metrics-and-optimization-processes` | 程序性能的度量指标及优化流程 | 1653 | 0+2 |  | video-only |
| 43 | `neon` | Neon | 2756 | 3+0 | arm.com | dup of `arm-neon` |
| 44 | `object-diagram` | 对象图 | 474 | 3+0 | plantuml.com, uah.edu… | - |
| 45 | `object-oriented` | 面向对象 | 2532 | 2+0 | inria.fr, wikipedia.org | - |
| 46 | `opencl` | OpenCL | 21005 | 1+0 | csdn.net | 大页21005字 |
| 47 | `opencl-optimizations-list` | OpenCL优化列表 | 7388 | 1+0 | arm.com | - |
| 48 | `optimizing-opencl-for-mali-gpus` | Mali GPUs的OpenCL优化 | 3872 | 1+0 | arm.com | - |
| 49 | `queue` | 队列 | 5969 | 5+0 | geeksforgeeks.org | - |
| 50 | `reference` | ai相关资料 | 2891 | 29+5 | github.io, github.com… | - |
| 51 | `sequence-diagram` | 序列图 | 486 | 4+0 | github.io, plantuml.com… | - |
| 52 | `significance` | 软件性能优化的意义 | 2271 | 0+4 |  | video-only |
| 53 | `simpleperf` | Simpleperf | 1930 | 4+0 | googlesource.com, csdn.net… | - |
| 54 | `singly-linked-list` | 单链表 | 2859 | 1+0 | geeksforgeeks.org | - |
| 55 | `soc` | SOC | 381 | 5+0 | wikipedia.org, socpk.com | - |
| 56 | `software-design` | 软件设计 | 3503 | 2+0 | wikipedia.org, runoob.com | - |
| 57 | `start-a-opencl-project-on-visual-studio-using-nvidia-gpu` | Start a OpenCL project on Visual Studio using Nvidia GPU | 445 | 1+0 | nvidia.com | - |
| 58 | `statechart-diagram` | 状态图 | 571 | 4+0 | github.io, plantuml.com… | - |
| 59 | `systrace` | Systrace | 2724 | 2+0 | android.com, perfetto.dev | - |
| 60 | `transformer` | Transformer | 685 | 1+4 | neurips.cc | - |
| 61 | `uml` | UML | 5821 | 6+0 | github.io, mermaid.live… | - |
| 62 | `use-case-diagram` | 用例图 | 3854 | 5+0 | csdn.net, plantuml.com… | - |

## B 档 `b-final`（45）

_零外链、内容最厚（融合改写）→ 逐篇识别出处，判不了走 personal_

| # | source_id | title | 正文 | 链(文本+视频) | 域名 | 备注 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `a-day-of-a-programmer` | 程序员的一天 | 1651 | 0+0 |  | 零外链 |
| 2 | `analysis-and-measurement-of-program-performance` | 程序性能的分析和测量 | 2337 | 0+0 |  | 零外链 |
| 3 | `arrays` | 数组 | 7091 | 0+0 |  | 零外链 |
| 4 | `auto-focus` | 自动对焦 | 1776 | 0+0 |  | 零外链 |
| 5 | `bad-smells-in-code` | 代码坏味道 | 4037 | 0+0 |  | 零外链 |
| 6 | `binary-tree` | AVL 树 | 7377 | 0+0 |  | 零外链 |
| 7 | `c-class-and-raii` | C++对象生命周期及RAII | 7319 | 0+0 |  | 零外链 |
| 8 | `c-concurrent-programming-and-cuda` | C++并发编程及CUDA | 7499 | 0+0 |  | 零外链 |
| 9 | `c-vs-java` | C++ VS JAVA | 2587 | 0+0 |  | 零外链 |
| 10 | `c-vs-python` | C++ vs Python | 4195 | 0+0 |  | 零外链 |
| 11 | `common-performance-design-patterns` | 常用性能设计模式 | 3105 | 0+0 |  | 零外链 |
| 12 | `compilation-principle` | 编译原理 | 3918 | 0+0 |  | 零外链 |
| 13 | `cpp` | cpp | 45109 | 0+0 |  | 零外链; 大页45109字 |
| 14 | `cpu-and-memory` | CPU和内存 | 8198 | 0+0 |  | 零外链; 大页8198字 |
| 15 | `device-frequency` | 设备频率 | 2590 | 0+0 |  | 零外链 |
| 16 | `example` | 图书馆管理系统建模例子 | 2982 | 0+0 |  | 零外链 |
| 17 | `git-commands` | Git命令 | 6252 | 0+0 |  | 有重复副本: `git-commands`(tools); 零外链 |
| 18 | `git-commands` | Git命令 | 6252 | 0+0 |  | dup（同id双路径 tools/computer-science）; 零外链 |
| 19 | `hdr` | HDR | 1989 | 0+0 |  | 零外链 |
| 20 | `image-quality-assessment` | 图像视频质量评价 | 4976 | 0+0 |  | 零外链 |
| 21 | `insight` | 洞察基础知识 | 4918 | 0+0 |  | 零外链 |
| 22 | `instructions` | 指令 | 3006 | 0+0 |  | 零外链 |
| 23 | `ipd` | IPD | 2189 | 0+0 |  | 零外链 |
| 24 | `kirin-9000s` | Kirin 9000S | 3912 | 0+0 |  | 零外链 |
| 25 | `mali-bifrost-gpu-compute` | Mali Bifrost GPU计算 | 4479 | 0+0 |  | 零外链 |
| 26 | `model` | 模型 | 12279 | 0+0 |  | 零外链; 大页12279字 |
| 27 | `multi-core-software-design` | 多核软件设计 | 7641 | 0+0 |  | 零外链 |
| 28 | `neon-intrinsics-checklist` | Neon Intrinsics清单 | 44714 | 0+0 |  | 零外链; 大页44714字 |
| 29 | `noise-evaluation` | 图像噪声评价 | 2654 | 0+0 |  | 零外链 |
| 30 | `opencl-optimization-guideline` | OpenCL优化指导 | 1806 | 0+0 |  | 零外链 |
| 31 | `optical-fundamentals` | 光学基础 | 2210 | 0+0 |  | 零外链 |
| 32 | `optimizing-opencl-for-maleoon-gpus` | Maleoon Gpu的OpenCL优化 | 2732 | 0+0 |  | 零外链 |
| 33 | `overview-of-opencl` | OpenCL | 17038 | 0+0 |  | 零外链; 大页17038字 |
| 34 | `performance-indicator` | 关键指标 | 2414 | 0+0 |  | 零外链 |
| 35 | `process-optimization` | 过程级优化 | 2780 | 0+0 |  | 零外链 |
| 36 | `refactoring-concepts-and-principles` | 重构的概念与原则 | 2614 | 0+0 |  | 零外链 |
| 37 | `report` | 如何E2E写一份高质量洞察报告 | 7981 | 0+0 |  | 零外链 |
| 38 | `requirements-analysis` | 需求分析 | 2413 | 0+0 |  | 零外链 |
| 39 | `sensor` | 图像传感器 | 1791 | 0+0 |  | 零外链 |
| 40 | `snapdragon-8gen1` | Snapdragon 8gen1+ | 4322 | 0+0 |  | 零外链 |
| 41 | `space-domain-noise-reduction` | 空域降噪 | 1689 | 0+0 |  | 零外链 |
| 42 | `stack` | 栈 | 5569 | 0+0 |  | 零外链 |
| 43 | `statement-optimization` | 语句级优化 | 4161 | 0+0 |  | 零外链 |
| 44 | `tonemapping` | 色调映射 | 1693 | 0+0 |  | 零外链 |
| 45 | `types` | 指令集类型 | 5059 | 0+0 |  | 零外链 |

## C 档 `c-intermediate`（54）

_零外链、多为碎片 → 先删留再补来源_

| # | source_id | title | 正文 | 链(文本+视频) | 域名 | 备注 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `algorithm-optimization` | 算法优化 | 529 | 0+0 |  | 零外链 |
| 2 | `auto-white-balance` | 自动白平衡 | 192 | 0+0 |  | 零外链; 碎片≤200字 |
| 3 | `avl-tree` | AVL 树 | 41 | 0+0 |  | 有重复副本: `b-tree`, `binary-search-tree`; 零外链; 碎片≤200字 |
| 4 | `b-tree` | AVL 树 | 41 | 0+0 |  | dup of `avl-tree`; 零外链; 碎片≤200字 |
| 5 | `basic-of-color` | 颜色基础 | 289 | 0+0 |  | 零外链 |
| 6 | `binary-search-tree` | AVL 树 | 41 | 0+0 |  | dup of `avl-tree`; 零外链; 碎片≤200字 |
| 7 | `c-vs-c` | C++ VS C | 1442 | 0+0 |  | 零外链 |
| 8 | `calculate-mode` | 计算模式 | 878 | 0+0 |  | 零外链 |
| 9 | `color-aberration-correction` | 色差校正 | 932 | 0+0 |  | 零外链 |
| 10 | `color-correction-and-3d-lut` | 色彩矫正与3D LUT | 68 | 0+0 |  | 零外链; 碎片≤200字 |
| 11 | `color-enhancement` | 颜色增强 | 371 | 0+0 |  | 零外链 |
| 12 | `compilation-and-runtime-optimization` | 编译与运行优化 | 476 | 0+0 |  | 零外链 |
| 13 | `computer-performance-and-power-consumption` | 计算机性能和功耗 | 841 | 0+0 |  | 零外链 |
| 14 | `configuration` | Git配置 | 1454 | 0+0 |  | 零外链 |
| 15 | `conversion` | 转换 | 336 | 0+0 |  | 零外链 |
| 16 | `cpu-cache-optimization` | cache优化 | 1171 | 0+0 |  | 零外链 |
| 17 | `data-structure-optimization` | 数据结构优化 | 526 | 0+0 |  | 零外链 |
| 18 | `developer-test` | 开发者测试 | 1348 | 0+0 |  | 零外链 |
| 19 | `dynamic-range-compression` | 动态范围压缩 | 1383 | 0+0 |  | 零外链 |
| 20 | `feature` | feature | 1340 | 0+0 |  | 零外链 |
| 21 | `flash` | 闪光灯 | 1317 | 0+0 |  | 零外链 |
| 22 | `four-rules-of-simple-desgin` | 简单设计四原则 | 242 | 0+0 |  | 零外链 |
| 23 | `frequency-domain-noise-reduction` | 频域降噪 | 1460 | 0+0 |  | 零外链 |
| 24 | `gamma` | gamma | 225 | 0+0 |  | 零外链 |
| 25 | `general-principles` | 总体原则 | 419 | 0+0 |  | 零外链 |
| 26 | `generic-tree` | AVL 树 | 434 | 0+0 |  | 零外链 |
| 27 | `green-balance-correction` | 绿平衡校正 | 290 | 0+0 |  | 零外链 |
| 28 | `highgui` | highgui | 143 | 0+0 |  | 零外链; 碎片≤200字 |
| 29 | `huawei-camera` | 华为相机 | 807 | 0+0 |  | 零外链 |
| 30 | `ifconfig` | ifconfig | 1008 | 0+0 |  | 零外链 |
| 31 | `image-scaling` | 图像缩放 | 172 | 0+0 |  | 零外链; 碎片≤200字 |
| 32 | `image-sharpening` | 锐化 | 890 | 0+0 |  | 零外链 |
| 33 | `image-stabilization` | 图像防抖 | 974 | 0+0 |  | 零外链 |
| 34 | `ips` | IPS | 1416 | 0+0 |  | 零外链 |
| 35 | `isp-system` | ISP系统 | 1435 | 0+0 |  | 零外链 |
| 36 | `lens-vignetting-correction` | 镜头暗角校正 | 881 | 0+0 |  | 零外链 |
| 37 | `limitations-of-local-work-size-and-global-work-size` | Limitations of local work size and global work size | 617 | 0+0 |  | 零外链 |
| 38 | `linux-commands` | Linux常用命令 | 1310 | 0+0 |  | 零外链 |
| 39 | `lod` | LOD原则 | 931 | 0+0 |  | 零外链 |
| 40 | `matrix` | 矩阵 | 417 | 0+0 |  | 零外链 |
| 41 | `opencv` | OpenCV | 158 | 0+0 |  | 零外链; 碎片≤200字 |
| 42 | `operations` | 运行 | 101 | 0+0 |  | 零外链; 碎片≤200字 |
| 43 | `overview-of-3a` | 3A统计概述 | 1297 | 0+0 |  | 零外链 |
| 44 | `process-and-thread` | 进程和线程 | 700 | 0+0 |  | 零外链 |
| 45 | `random` | 随机数 | 625 | 0+0 |  | 零外链 |
| 46 | `reading-notes` | 读书笔记模版 | 1706 | 0+0 |  | 零外链 |
| 47 | `red-black-tree` | AVL 树 | 54 | 0+0 |  | 零外链; 碎片≤200字 |
| 48 | `refactoring-techniques` | 重构手法 | 622 | 0+0 |  | 零外链 |
| 49 | `software-modeling` | 软件建模 | 791 | 0+0 |  | 零外链 |
| 50 | `solid` | SOLID原则 | 655 | 0+0 |  | 零外链 |
| 51 | `source-4ed827b8730d` | 正交四原则 | 292 | 0+0 |  | 零外链 |
| 52 | `terminology` | 术语 | 2653 | 0+0 |  | 零外链 |
| 53 | `time-domain-noise-reduction` | 时域降噪 | 1471 | 0+0 |  | 零外链 |
| 54 | `von-neumann-architecture` | 冯诺依曼结构 | 536 | 0+0 |  | 零外链 |
