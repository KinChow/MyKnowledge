# OpenCL

OpenCL文档学习：
OpenCL架构可参考：
https://blog.csdn.net/leonwei/article/details/8880012

OpenCL是为混合CPU、GPU及其他计算设备统一到单个平台编程的开放T业标准。是一个并行编程的框架，包含了语言、API、库和runtime系统。OpenCL的目标是编写可移植且高效的代码。

层次：
* Framework：把主机和设备当作整体，区分为平台层、Runtime和编译器
* 平台模型：区分主机和设备，以及设备上的运行单元：计算单元和处理单元
* 执行模型：区分主机程序和设备上运行的核程序，主要讲了核程序上的调度单元work-group,work-item以及行为。
* 内存模型：区分了主机和核中用到的内存结构、内容和行为。定义了执行顺序关系和同步需要用到的规则。

阅读了OpenCL api文档里的架构这一章，这章把OpenCL分成了四个层次的抽象模型。
层次：

平台模型
平台模型由一个host链接一个或多个OpenCL devices组成。OpenCL devices被划分成一个或多个compute units （CUs），CU被划分为一个或多个processing elements（PEs）。计算在PE中进行。

一个OpenCL应用由host code和device kernel code两部分实现。一个OpenCL应用的Host code在host processor上根据host平台的本机模型运行。OpenCL应用的host code把kernel code当做command从host提交到OpenCL devices。OpenCL device在PE中执行命令计算。

控制流属性：
* converged、一个CU中的PE都在以相同的顺序执行指令。针对跨PE执行单个指令流的硬件优化适合converged控制流
* diverged: PE之间控制流不同。

Kernel通常以converged控制流开始执行，两种控制流都会在一个核里发生。这种机制为能在OpenCL上实现的算法提供了很大的灵活性。

可使用OpenCLC源程序，SPIR-V中间语言或者二进制obj文件提供程序。OpenCI的编译器将这些形式的程序翻译为可执行objDevice code compiler分类
* online：在host program执行期间使用标准AP调用。
* offline：使用平台特定的方法，在host program控制之外调用。

OpenCL runtime允许开发者执行之前编译好的device program，能够加载、执行之前编译好的device program。Custom device只支持built-in kernel，不能使用kernel语言编程。

平台profile分类：
* full profile： 为所有设备提供online compiler
* Embedded profile：不是必须提供online compiler

用于特殊用途的device可作为built-in kernel。平台提供API，用于枚举和调用built-in kernel。

执行模型
* kernel：在一个或多个OpenCL设备上运行。定义在program中，在OpenCL device上执行。是真正执行的部分。计算由在work-group中执行的work-item进行。kernel在由host管理的context下执行。
* Host program：在host上运行。使用OpenCLAPI与上下文进行交互，对OpenCL进行初始化，创建context以及命令通道，提交命令，copy效据到device上等功能。（host应CPU,device 应GPU
* context: context定义了kernel执行的环境。包含了以下资源：。Host program用OpenCLAPI来创建、管理上下文。
* device: OpenCL平台的一个或多个设备
* Kernel obj：在OpenCL devices上运行的OpenCL函数
* Program obj：实现kernel的源程序
* Memory obj：变量对host和OpenCL devices可见。kernel实例在memory obj上运行。

OpenCL API的功能允许主机通过命令队列（command-queue）与device交互。一个命令队列与单个device关联。命令队列中的队列分为以下三种：
* Kernel-enqueue commands：入队一个在device上执行的kernel
* Memory commands： 在hosnt和device memory之间、memory obj之间、map和honst地址空间中的unmap memeroy obj之间传输数据
* Synchronization commands：指明命令之间的执行顺序。

在device上运行的kernel可以入队命令到device侧的命令队列，即child kernel。无论是子核还是父核，每个命令经过六个状态；
1. Queue：这条指令已入队。指令会一直在队列中，直到被显示冲掉或被其他指令隐式冲掉。
2. Submitted：名列从命令队列中被冲掉，提交至device上运行。从命令队列出队后，命令会在前置条件都满足的情况下执行。
3. Ready：所有命令需要的前置条件都满足。这条命令，或者与kernel-enqueue命令相关的work-group集合，会进入设备资源池等待调度执行。
4. running：命令执行开始。在核入队列命令的情况下，一个或多个相关的work-group开始执行。
5. Ended：命令执行结束。Kernel-enqueue命令结束，所有相关的work-groups都结束执行。
6. complete：命令和子命令都结束执行，事件obj的状态过移到CL_COMPLETE
以上状态和设备的工作池都是执行模型的概念性元素。在实现中比较自由。

命令间通过event obj通信。把命令相关联的状态设为CL_COMPLETE即为成功执行指令。把事件状态设为负值即为执行指令失败，异常终止。在这种情况下，与异常终止指令相关的指令和在同一个上下文中的所有其他指令可能都无法再获取，它们的行为由实现定义。

提交至设备的命令只有在所有限制命令顺序的前置条件都满足时才会launch。这些前置条件有以下三种资源：
* 执行顺序的限制。e.g. barrier
* 依赖关系。
* 全局变量的Non-trivial C初始化器或cpp构造函数。此时OpenCL的C/C++编译器需要生成program初始化kernel来进行C的初始化或者CPP的构造。这些kernel必须在同一程序在同—device上的其他核之前执行。程序初始化核的ND range是（1,1,1）。多个程序连接在一起时，未定义程序初始化核的执行顺序。

命令执行分为阻塞或非阻塞。
* 阻塞式命令：在命令完成之前OpenCL API接口不会返回。
* 非阻塞式命令：立即返回，需要程序员保证入队命令的执行顺序，入队命令需要在必要资源可用之后执行。
实际的命令执行可能是异步的。

在同一个命令队列中的命令相对于其他的命令执行有以下两种模式：
* In-order execution：指令和指令的副作用只在他们按照同一顺序执行时入队时出现
* Out-of-order execution：显式同步指定或对事件的显式依赖决定命令执行的顺序。

同一上下文中可以多个命令队列，独立执行。对host program可见的事件对象可被用于定义不同命令队列中各命令之间的同步点。

执行模型的核心是根据kernel是怎么执行来定义的。kernel入队列命令提交一个kernel来执行时，此时就出现了索引空间。kernel实例由kernel、kernel的参数值和索引空间里的参数定义。设备上执行kernel时，kernel function在定义好的索引空间上各个点上执行。这些在执行的kernel function叫做work-item。关联给定的kernel实例Work-tiem受work-group管理。Work-group定义了一个对于家引空间的粗粒度划分。Work-group又划分了sub group，提供额外层次的执行控制。

Work-item有一个N元组全局ID，基于它们在索引空间的坐标。也可以在work group中定义。

Work-item至ND range的映射
OpenCL支持的索引空间叫做NDRange，是N维索引空间，N=1or 2or 3。NDRange被分解为工作组，形成覆盖索引空间的块。
NDrange由三个长度为N的整数数列定义：
* 每维度index space的范围/每个维度的全局大小偏移
* 索引，表示每个维度的初始索引
* 每个维度的work-group大小/local大小
Work-item的全局ID是个N维三元组。每个维度的大小范围从F到F加上这个维度的元素个数-1。

在同一个NDRange中的work-group大小不能都一样，除非kernel不允许。在这种情况下，每个全局大小不能被局部大小整除的维度，都会被划分成两个区域。其中一个区域的work-group包含了由程序员指定该维度的局部大小的work-items。另一个区域的work-group包含的work-item数量比前一个区域少，称作the remainder work-group。Work-group的大小在每个维度可以不均匀，2D range中至多4种，3D至多8种。

Work-item在work-group中有一个N元组local id，表示在work-group中的位置。这个N元组的范围是0到这个维度的work-group size - 1

没有对每个维度里的work-group有直接定义，可以在kernel实例入队时从局部和全局的ND ranges中推导。

Work-group的ID是以一个N元组，范围从0到这个维度的全局大小/局部大小取上整。Work-group的ID和work-item在group中的局部ID唯一定义了一个work-item。

二维索引空间示例：
* Work-items（Gx,Gy）：全局索引使用Gy定义Gx,Gx*Gy = work items总数
* work-group（Sx,Sy）：局部索引使用Sy定义Sx,Sx *Sy =一个work-group中的work-items总数
* 已知以上数据可以计算出work-group的数量（Wx, Wy） =（ceil（Gx / Sx）， ceil（Gy / Sy））
* global ID offset(Fx, Fy)
* Work-item 全局ID和local ID转换
    * (gx, gy) = (wx × Sx + sx + Fx, wy × Sy + sy + Fy) 
        * wx, wy是work-group ID
        * Sx, Sy work-group size
        * sx sy work-group里的local id

Work-group中的work-item会被划分成sub-group，映射需要实现来定义，在运行时可能被调用

kerne 实例运行
OpenCL程序执行的工作是通过执行Device上的内核实例进行的。
本节讲了kernel obj怎样从kernel入队列指令移动到命令队列中，在设备上执行并完成执行。
Kernel obj定义为一个函数在program obj中，是连接kernel和参效值得参数集合。Host program把kernel obj和ND Range、work-group划分一起入队到命令队列，这即为一个kernel实例。同时，事件的可选集合可以在kernel入队时被定义。与特定核实例相关的事件用于限制kernel实例相对于队列中基他命令lauch时或者其他队列里在同一上下文中的命令。

Kerne实例提交到device。
* in-order命令队列：kernel实例以相同顺序launch、执行。
* Out of order命令队列：kernel实例需等待：在kernel实例之前入队的同步指令满足后、在kernel实例事件入队时，可选集合中定义的各事件设置为CL_COMPLETE。这两个条件满足后，kernel实例launch，与这个kernel实例相关的work-group被放入一个用于执行work-group的池中。这个池叫做work-pool，work-pool可以以任意方式实现，只要能确保放入池中的work-group能执行。device从work-pool中调度work-group，在device的CU上执行。kernel入队命令会在所有与kernel实例相关的work-group结束执行后完成，与命令关联的全局内存更新在全局可见，通过设置与kernel入队列命令相关的事件为CL_COMPLETE, device信号成功完成。

命令队列只能和一台设备关联，一台设备可以与同一个work-pool里的多个命令队列关联。一台设备也可以与同一平台的不同上下文里的命令队列关联，这些命令队列都同同一个work-pool中。设备会从work-pool中拉取work-groups，在一个或多个CU上以任意顺序执行它们，可能会交错执行不同命令里的work-groups。符合规范的实现可能会顺序化work-group，正确的算法就不可以假设work-groups并行执行。在work-pool中，没有安全并可移植的方式来在work-groups的独立执行之间同步，work-groups可以以任意顺序执行。

在同一个sub-group中的work-items同时执行，但不必要并行执行（比如他们不能保证独立执行）。因此，只有用在一个sub-group上所有的work-items的高层次的同步构造（比如sub-group的barrier）才会在OpenCL中定义和包含。

在一个给定的work-group中，sub-groups在合适的device支撑下同步执行，相对其他sub-groups可能会独立执行，相对于hosntthreads和其他运行在OpenCL device上的、OpenCL系统外的实体，甚至不需要work-groupsbarrier操作。在这种情况下，sub-groups会在内部使用barrier操作，不需要互相之间同步，并且可能使用依赖其他sub-groups操作的runtime依赖的操作。

在同一work-group中的work-items同时执行，但只能保证在sub-groups和device支持下能独立执行。在这种能力缺失时，只有用在一个work-group上所有的work-items的高层次的同步构造（比如work-group的barrier）才会在OpenCL中定义和包含。

在同步函数（berrier）的缺失下，在一个sub-group 下的work-item可能会被序列化。在sub-group函数存在的前提下，一个sub-group中的work-item会在任意给定sub-group函数之前被序列化，在动态遇到的sub-group函数对之间和在work-group和kernel结束之间。
在各成分的sub-groups不是独立运作的情况下，一个work-group中的work-item可能会在work-group同步函数之前或者之后或者之间被序列化。

device侧的入队
算法在执行时可能需要生成额外的工作。在很多情况下，这个额外的工作不会被静态确定下来，所以与kernel关联的工作只会在kernel实例运行时的runtime出现。这种能力可以在host program上用龙脊运行实现，但是host的参与可能会带来巨大的开销和应用控制流的复杂度。更有效的方法是从其他核的内部嵌套kernel入队列命令。这种嵌套式并行可以通过在device上支持kernel的入队来实现，不需要hostprogram的直接参与。所以叫做device侧的入队。
device侧的kernel入队在命令和host例的kernel入队命令类似。在device上运行的kernel（parent kernel）入队一个kernel实例（chilekernel）至device侧的命令队列。这是个乱序命令队列，并且和host program上的乱序队列有一样的行为。入队至device侧命令队列的命令生成并使用事件来强制执行顺序限制，和host上的命令队列一样。然而这些事件只对device上运行的parent kernel可见。这些前置条件事件设置为CL_COMPLETE时，与child-kernel相关的work-groups被放入device工作池中。child和parent kernel异步执行。然而，parent kernel并不会再把它的事件设为CL_COMPLETE时完成，它完成需要等到所有的child kernel执行结束并且设置所有相关事件为CL_COMPLETE的信号发出后。任意child kernel会在事件状态设置为负值时结束，parent kernel也会异常退出，并且将负的事件值传递给childs。如果有多个child有设为负值的事件，对负值的选择由实现定义。

同步
同步指的是限制两个或多个执行单元之间的执行顺序。存在以下三种OpenCL的同步域：
* work-group同步：在同一个work-group中对work-items的执行顺序有限制。
* sub-gorup同步：在同一个sub-group中对work-items的执行顺序有限制。
* 命令同步：对执行的命令顺序有限制。

在同一个work-group中对所有work-items的限制使用work-group function实现。这些函数集中操作在一个work-group中的work-items。可用的集中操作有：barrier，reduction，广播，前缀和，对predicate的评估。Work-group function必须在converged控制流中出现（举例：在同一个work-item中的work-group必须精准地用到相同的work-group function）。比如说，如果一个work-group function在循环里出现，在同一个循环迭代中的work-items必须用到相同的work-group function。同一work-group中的work-items必须执行work-group function并且完成内存的读写访问，在任意操作被允许在work-group function外执行之前。OpenCL未定义和提供应用在work-group之间的Work-group funcitons，因为OpenCL没有定义前向过程（forward-progress）或work-gorups之间的顺序关系

使用sub-group function来实现在一个sub-group中所有work-items的同步。这些函数集中操作在一个sub-group中的work-items。可用的集中操作有：barrier，reduction，广播，前缀和，对predicate的评估。关于控制流的定义、内存读写和上一段相同。Sub-groups之间的同步要么用work-groups function实现，或者通过内存操作实现。需要小心使用sub-group同步的内存操作，因为sub-group之间的forward progress只在OpenCL的一些实现里可选文持。

命令同步用于区分同步点（synchronization points）。同步点在host命令队列中的命令之间、device侧的命令队列的命令之间发生。
OpenCL中定义的同步点包括：
* launching a command：在kernel等待的事件被设置为CL_COMPLETE后kernel实例被launch到device。
* Ending a command: child kernel可以入队，以等待parent kerne！在它们可以被lauch之前到达end状态。
* Completion of a command：kernel实例会在核以及它的child-kernel内所有work-group完成后完成。在命令队列中的parent kernel或者其他kernel通过kerne/相关的事件值设置，来向host发送信号。
* Blocking commands：定义了调用blocking API function和到达完成状态的入队队列的执行单元之间的同步点。
* Command-queue barrier：保证所有之前入队的命令在之后的命令可以launch之前都完成。
* clFinish：这个函数屏蔽直到所有之前入队的命令在clFinish定义的同步点之后且clFinish函效返回后完成。

一对命令A和B之间的同步点确保了命令A的结果会在命令B launch之前发生。这需要命令A的任意内存更新完成，并且在其他同步点完成前，这块内存可以被其他命令使用。同样，这需要命令B在从全局内存加载值之前等待同步点。同步点的概念同样可以用在命令上，比如在两个命令集之间使用的barrier。在barrier之前的所有命令都必须完成，并且他们的结果对后续命令都可用。此外，在barrier之后的命令在加载值、继续执行之前都需要等待barrier之前的命令。

这些Happens-before的关系事OpenCL 2×内存模型的基本组成部分。在应用在命令这个层级时，这些关系直接地在语言层次定义了指定不同命令间的顺序关系。指定不同操作的内存操作顺序，需要比同步点这种高层次概念更复杂的规则。由memory ordering rules来定义。

kernel分类
OpenCL执行模型支持三种类型的kernel：
* OpenCL kernels：受OepnCL API管理为与kernel function相关的、在program obj中的kernel obj。OpenCL program obj使用OpenCLAPl来创建。OpenCL API包括查询内核语言和中间语言的函数，这些语言可用于为设备创建OpenCL程序对象。
* Native kernels：通过host函数指针访问。Native kernel和device上的OpenCL kerne|一起排队等待执行，切和OpenCL kernel一起共享内存obj。举个例子，native kernels可以是应用代码里定义的函数，或者从库里导入的函数。执行native kernel的能力在OpenCL中可选，并且native kernel的语义由实现定义。OpenCL AP/包括了能够查询一台设备的能力，以决定能力是否支持。
* Built-in kernels：与特定设备绑定，不能在program obj的源代码运行时build。Buit-in kernel的用途是示固定功能的硬件或固件，这些硬件和固件与特定OpenCL设备或用户自定义设备关联。Built-in kernel的寓意可能在OpenCL以外有别的定义，因此由实现定义。
以上三种类型的核都通过OpenCL命令队列操纵，必须符合在执行模型中定义的同步点。





内存模型
OpenCL的内存模型描述了在一个OpenCL程序运行期间的OpenCL平台用到的内存结构、内容和行为。模型允许程序员推理host程序和多kernel实例运行时的内存值。
OpenCL程序定义了包含一个host，一个或多个设备、命令队列和上下文中的内存。Host program在host上运行一个或多个受操作系统管理的host线程。可能在同一个上下文中有多个设备，这个上下文有权访问OpenCL定义的memory obj。在单个设备上，多个并行执行的work-group可能会潜在更新重叠的内存。最终，在单个work-group中，多个work-items同时执行，也潜在会对重叠内存进行更新。
内存模型必须精确定义从各执行单元中能被看到的内存里的值交互的方式，以便程序员可以推测OpenCL程序的正确性。

从四个部分定义内存模型：
* 内存区域：不同的对共享同一上下文的host和device可见的内存
* 内存对象：OpenCL API定义的obj，由host和devices管理
* Shared Vrtual memory：在同一上下文里的host和devices都能看到的虚拟地址空间
* Consistency Model：定义从多个执行单元从内存加载的值加上规定内存操作顺序的原子/fence操作、定义同步关系的规则。

Fundamental Memory Regions
OpenCL中的内存分为两块：
*  Host memory：主机可直接访问的内存。具体行为OpenCL不定义。内存obj通过OpenCL API中的函数在host和devicess之间移动，或者通过共享虚拟内存接口。
*  Device memory：在OpenCL devices上执行的kerne/可以直接访问的内存。包含以下四种地址空间/内存区域：
    * Global memory：这段内存区域允许同一个上下文下的任意device上运行的所有work-groups的所有work-items的读写访问。Work-items可以读出或写入一个memory obj的任意元素。xglobal memory的读出和写入可能会根据device的能力被缓存。
    * Constant Memory：global memory中在kerne/实例执行期间保存常量的一块区域。host分配并初始化放入constant memor的memory obj。
    * local memory：work-group的本地内存区域。这块内存区域可以被用来分配这个work-group中所有work-items共享的变量。
    * Private memory：work-item的私有内存区域。在一个work-item的私有内存中定义的变量对其他work-item个可见。
    Local和private内存通常与特定的设备关联，global和constant内存在给定上下文的所有设备间共享。OpenCl device可能会存在一个支持这些共享内存高效访问的cache。

一个设备可以获取的这四个命名的内存区域是不连贯的，不重叠。这是逻辑关系，然而，在实现中可能会让这四个不连贯的命名地址空间共享同一块物理内存。

程序员经常需要kernel能够调用的函数，这些函数控制的指针可指向多个命名地址空间。能让程序员避免错误和浪费创建多个函数的拷贝，为每个命名地址空间创建的函数拷贝。global、local、private地址空间属于单个generic address space。以下特性支持在device内存中指向命名地址空间的指针：
* 指问generic address space的指针可以强转为指向global、local或private地址空间的指针。
* 指向global、local或private的指针可以强转为指向generic address space的指针。
* 指向global、local或private的指针可以隐式强转为指向genericaddress space的指针，但不能反着转。
constant地址空间和generic address space不连续。

与global memory里的内存obj关联的内存地址不会在kernel实例间、device和主机间、device之间保存。在这方面，global memory比起一段地址空间更像memory obj的全局资源池。这个限制在使用shared Virtual memory （SVM）时比较宽松。

SVM让host和在同一上下文中的所有devices之间的地址有意义，因此支持在OpenCL kernel中使用基于数据结构的指针。它逻辑地扩展了global memory的一块区域到给予work-item访问host地址空间的host地址空间。在有文持host和一个或多个devices之间的共享地址空间的硬件的平台上，SVM可能有提供更有效的方法来共享devices和host之间的数据。

Memory object
Memory obj是global memory中的内容。
Memory obj是global memory的参考计数区的句柄。
Memory obj使用OpenCL类型cl_mem并
且分为以下三类：
* Buffer：是以连续内存的block形式存储的memory obj，用作持有OpenCL程序数据的多用途obj。buffer中值的类型可以是任意已有的类型（比如int、float），向最类型或者用户定义的结构体。可以通过指针操作。
* Image：一个image obj持有一维、二维或三维的图像。格式基于在图像应用中使用的标准图像格式。图像是由OpenCLAP/定义的函数管理的不透明数据结构。为了优化很多GPU里存储在文理内存中的图像操作，OpenCL kernel不能读写单幅图像。在OpenCL 2.0中，这条限制比较宽松，通过提供同步和栅栏操作，使得程序员可以合理地同步代码使用kernel读、写一个图片。
*  Pipe：pipe memory obj概念上来说，是一个data item的有序序列。一个pipe有两个结束点：写结束点在插入的data item中，读结束点在移除的data item中。为了文持生产者消费者设计模式，一个kernel 实例连接到写结束点（生产者），另一个kernel实例连接到读结束点（消费者）。

Memory obj由host的API分配。Host program还可以提供runtime，这个runtime有一个指向连续内存的block的指针，block在obj创建时持有memory obj（CL_MEM_USE_HOST_PTR）。或者，物理内存可以用OpenCL runtime来管理，host program不能直接获取。

在不同的内存区域Memory obj的分配和访问在host和在device上运行的work-items之间是不同的。在下表中总结，表里描述了kernel或host能否从内存区域分配内存，分类的种类（编译时静态 vs运行时动态）和访问权限（kernel或host能否读或写内存区域）。

表格说明了OpenCL中不同的内存区域，和内存对象是怎样被host和kernel的执行实例分配和访问的。对于kernel，需要区分parent kernel和child kernel上本地内存的行为。

一旦分配好了内存，memory obj运行在一个或多个devices上的kernel实例可用。除了SVM，有三种基本的方式来管理host和device之间的buffer内容。
* Read/Write/Fill commands：与memory obj关联的数据在host和使用命令入队到OpenCL命令队列的global内存区域之间显式读写。
* Map/Unmap commands：从memory obj里来的数据会通过host能获取到的指针被映射到内存的连续block。Host program会在mapcommand能被host program安全操纵前入队map command到内存对象的block上。在host program结束和内存块的工作时，hostprogram入队unmap command来允许kernel实例安全地读写buffer。
* copy commands： 与memory obj关联的数据在两个buffer之间拷贝，可能会一直留在host或device上。
使用读/写/映射，命令可以是阻塞式或非阻塞式的操作。调用阻塞内存转移的函数会在命令（内存转移）完成后立即返回。此时host上关联的内存资源可以安全地再次使用，转移完成的后序操作可以得到确保。对非阻塞式的内存转移，OpenCL函数在命令入队后立即返回。

Memory obj和上下文绑定，可以在多余一个的物理设备上运行的kernel实例中出现。OpenCI平台必须支持大范围的硬件凭条，包括在硬件上不支持单个共享内存空间的系统，因此在kernel实例之间共享memory obj的方式受限。基本原则是允许在时间上重疊的kernel实例中的memory obj上的多个读操作。但是混合重叠的在不同kerne实例上的相同内存obj的读写只在使用SVM时粒度划分较好的同步上允许。

在多个devices上运行的多个kernel实例操作global memory时，OpenCL的运行时系统必须管理和给定device关联的memory obj。在很多情况下，OpenCl会隐式关联device和memory obi。kernel实例自然和提交kernel的命令队列关联。既然一个命令队列只能访问一台设备，队列唯一地定义了哪一个队列参与给定的kernel实例，定义了memory obj、kernel实例和device之间清晰的关联关系。程序员可以在自己的程序中预想这些关联，并显式通过管理memory和device的关系来改善性能。

Shared Virtual Memory
OpenCL扩展了global memory区域到host memory区域，通过SVM机制。
在OpenCL中有三种类型的SVM：
* Coarse-Grained buffer SVM：共享发生在OpenCl buffer memory obj的粗粒度区域。在同步需要强制保证一致性，并且使用map/unmap命令来驱动host和device之间的更新。这种SVM的形式与非SVM的内存使用类似，然而，这种形式使得kernel实例和host program共享基于指针的数据结构（比如链表）。程序作用域的全局变量会被当做每个device上的粗粒度SVM，用来寻址和共享purpose.
*  Fine-Grained buffer SVM： 共享发生在个体加载/存储字节至OpenCL buffer memory object时。加载和存储可能会被缓存。这意味着在同步点可以保证一致性。如果支持可选项OpenCl原子性，可以用来保证细粒度的内存一致性控制。
*  Fine-Grained system SVM：共享发生在host memory中任意地方的个体加载/存储字节。加载/存储可能会被缓存所以同步点可以保证一致性。如果支持可选项OpenCl原子性，可以用来保证细粒度的内存一致性控制。

OpenCL 1.x的内存一致性模型
OpenCL 1.x的内存一致性模型限制较松，比如work-item可见的内存状态不能保证在work-items的集合中总是一致。
在work-item下的内存存在加载/存储一致性。Local memory在work-group barrier 下的单个work-group里的work-items之间保持一致。
Globalmemory同样，但是不能保证在在运行一个核的不同work-groups之间的内存一致性。
Memory obj在入队命令之间的一致性由同步点来保证。

OpenCL 2.x的內存一致性模型
OpenCL 2x模型可以实现哪些内存操作保证以何种顺序发生，每个读取操作将返回哪些内存值，程序员需要关注。编译器的编写者需要在实现编译优化时遵守一些限制：哪些变量可以缓存在寄存器中，什么时候可以在barrier或者原子操作附近移动读操作或写操作。硬件设计者需要关注硬件优化的限制，比如说刷新或者让硬件缓存无效。
OpenCL 2x的内存一致性模型基于ISO C11编程语言模型。为了使得模型更加精准和自包含，我们一字不落地包含了ISO C11国际标准的一些段。
对于程序员来说，最直观的模型是sequencial consistency内存模型。顺序一致性交错了每个UE执行的步骤。每个对内存位置的访问可以看到在这个交错里的最后一次内存分配。然而顺序一致性对于程序员的推导来说相对直接，但实现的代价很高昂。因此，OpenCL2.x现了一个宽松的内存一致性模型，举个例子，它可以在内存加载违法内存一致性时写程序。如果一个程序不包含任何race且如果一个程序只使用利用了顺序一致性内存顺序的原子操作，OpenCL程序会表现出顺序一致性。
程序员可以一定程度控制内存模型的竞松程序，通过选择同步操作的内存顺序。在这里，我们给出一个高层次的描达，描达了这些内存顺序怎样应用在UE之间共享的原子obj上的原子操作中。OpenCL 2×memory-order选项基于ISO C11标准内存模型。在确定的OpenCL functions中，通过以下枚举常量确定内存顺序
* memory.order_relaxed：表示没有顺序限制。这个内存顺序可以安全地用于增加增量的计数，但不保证相对于其他内存位置的任何顺序。
* memory_order_acquire：从同步它的释放操作获取到“acquires”语义的副作用的同步操作（fence或者原子）：如果是释放的获取同步，在获取的UE可以看到所有前面释放的副作用。作为carefully-designed的部分，程序员可以使用“acquire”来安全地观察另一个UE的工作。三=相当于一个具有“获取"含义的同步操作。
* memory_order_release：一个具有“释放“含义的同步操作，对用于同步的获取操作有副作用。所有在release之前的副作用都在release之前包合。作为carefully-designed协议，程序员可以使用release来使得一个UE能看到另一个UE的改变。
* memory_order_acq_rel：具有acquire-release语义的同步操作，具有acquire和release内存顺序的性质。在排序read-modify-write操作时常用。
* memory_order_seq_cst：每个UE中的加载和存储操作以program顺序执行（比如，sequenced-before），不同UE间的加载和存储操作是间断的。

忽略指定的memory_order，解决异构平台上的内存操作限制增加的巨大的程序执行开销。OpenCL平台可能可以优化特定的操作，这些操作依赖于通过限制内存操作的作用域的内存一致性模型特性。离散的内存作用域使用一下memory scope枚举常量定义：
* memory_scope_work_item： 只在work-item中应用memory-ordering限制
* memory_scope_sub_group：只在sub-group中应用memory-ordering限制
* memory_scope_work_group： 只在单个work-group里应用memory-ordering限制
* memory_scope_all_svm_devices：对执行在跨设备和使用SVM的host上的work-item应用memory-ordering限制。带着这个选项的、对buffer进行的release操作在没有设置CL_MEM_SVM_ATOMICS标记位时，会至少memory_scope_device可见性，在一个队列同步点得buffer是完全同步的。

这些内存作用域定义了在分析内存操作的顺序限制时的可见性层次。举个例子，如果程序员知道内存操作的顺序仅仅跟单个work-group中的work-items集合关联（因此在同一个设备上运行），实现能避免在同一上下文中跨设备管理内存顺序的开销，可以实质上减少程序的开销。在全局内存或局部内存上使用时所有的内存作用域都有效。对于local memory，所有的可见性都受限于给定的work-group和比沒有某他意义的memory_scope_work_group宽的作用域。

接下米会解释同步构造和需要使用OpenCL 2×宽松内存模型的详细规则。很多程序都没从宽松程序模型中获益，甚至专家程序员使用原子和栅栏来写宽松程序模型的程序都很艰难。很多OpenCL程序可以使用简化的程序模型来写。需要遵循以下规则；
* 通过命令队列定义的同步点来写管理安全global memory obj共享的内存。
* 把在work-groups中的低层次 同步限制为work-group的函数，比如barrier
* 如果想在系统分配或者支持原子的细粒度SVMbuffer时连续一致的行为，在作用域memory_scope_all_svm_devices只使用memory_order_seq_cst操作
* 如果想在不使用系统分配或支持原子的细粒度SVMbuffer时连续一致的行为，在作用域memory_scope_driver或memory_scope_all_svm_device只使用memory_order_seq_cst操作。
* 确保程序没有竟争条件。
如果遵循了以上规则，可以跳过宽松内存模型的详细规则。

原子和fence操作的概览
OpenCL 2.x有大量的同步操作，用于定义程序中的内存顺序限制。这些操作在控制一个UE中的内存操作怎样被另一个UE看到演很重要的角色。
原子操作是不可分割的。要么完全出现，要么完全不出现。这些操作用于指定UE间的内存操作顺序，因此它们使用定义在OpenCL内存一致性模型中的memory order和memory_scope参数来参数化。OpenCL kernel语言中的原子操作和C11标准中的对应操作类似。
OpenCl 2x中的原子操作应用于原子类型包括int, uint, long, ulong, float, double, half, intptr_t, uintptr_t, size_t, and ptrdiff-t types。 然而，一些原子类型的支持依赖于对应常规类型的支持。
对一个或多个内存位置的原子操作要么是获取操作，释放操作，或者获取释放操作。沒有关联的内存位置的原子操作是fence且可以是获取fence，释放fence或者获取释放fence。另外，存在宽松原子操作，没有同步性质，切原子read-modify-write操作有特殊属性。
顺序memory_order_acquire（用于读），memory_order_release（用于写）和memory_order_acq_rel（用于read_modify_write操作）用于使用共享变量的UE间的简单通信。不是正式地，在一个原子对象A上执行memory_order_release会导致后序执行memory_order_acquire的UE都能看到A之前所有的副作用。顺序memory_order_acquire,memory_order_release，memory order_acq_rel都不为没有竞争的程序提供顺序一致性，因为不能确保在原子load后的原子store在这个顺序下对其他thread可见。

fence操作是atomic_work_item_fence，包含了memory_order参数、memory_scope和cl_mem_fence_flags参数。依赖于memory_order參效，fence操作：
* memory_order_relaxed顺序下，没有作用memory_order_acquire顺序下，有获取fence
* memory_order_release顺序下，有释放fence
* memory_order_acq_rel顺序下，有一个获取fence和一个释放fence
* memory_order_seq_cst顺序下，有一个同时具备获取释放语义的顺序一致性fence。
如果指定，clmem fence flags参数必须是CLK_IMAGE_MEM_FENCE, CLK_GLOBAL_MEM_FENCE, CLK_LOCAL_MEM_FENCE, or
CLK _GLOBAL_MEM_FENCE | CLK LOCAL_ MEM_FENCE。

atomic_work_item_fence(CLK_IMAGE_MEM_FENCE, ...)：这个内置函数必须用于确保无采样器的写能够对后序相同work-item的读可见。不用这个函数，不能保证对图像对象的读写连贯性：如果work-item读入的图像是它之前没用这个函数但是写过的区域，不能保证之前的写对work-item可见。

OpenCL 2.x中的同步操作可以被memory_scope参数化。内存作用域控制原子操作或fence相对于内存模型可见的扩展。这些内存作用域可能会在全局内存或局部内存上使用原子操作和fence时使用。在全局内存上使用时，可见性收到内存容量的限制。在细粒度、非原子的SVMbuffer、粗粒度SVMbuffer、非SVMbuffer上使用时，使用memory_scope_all_svm_devices来参数化的操作会表现得与使用memory_scope_device一致。在局部内存上使用时，可见性受work-group的限制，因此比memory _scope.work_group具有更广的作用域都会被缩小为Memory_scope_work_group。

如果两个行为A和B在同一作用域P下，他们会有包含的作用域关系：
* P-memory_scope_sub_group: A和B会被在同—个sub-group里的work-items执行
* P-memory_scope_work_group: A和B会被同一个work-group里的work-items执行
* P-memory_socpe_device:A和B被同一个设备上的work-items执行，前提是A和B使用SVM分配，或者A和B被同一个kerne或者A和B使用cl_mem buffer时的一个子核的work-items上执行。
* P-memory_scope_al_svm_devices:A和B是被主机线程直线，或者被一个或多个互相共享并和host program共享SVM内存设备上的work-items执行。

Memory ordering rules
内存模型的目的是为了理解在内存中对ob修改的事件顺序。修改一个对象或者调用一个更改obj的函数是副作用，比如改变了执行环境的状态。通常评估一个表达式包括值的计算和副作用的启动。对左值表达式的值计算包含确认指定对象的身份。
* 假设OpenCL核语言和host编程语言在单个UE执行的评估之间存在sequenced-before的关系，这个关系是不对称的，传递的，成对出现在这些评估之间，形成了评估之间的部分有序。给定任意两个评估A和B，如果A sequenced-before B，那么A会在B之前执行（B sequenced-after A）。如果A和B之间这两种关系都没有，那么AB是无序的。A和B会在这两种关系某中一种定义后立即顺序华，但可能没指定哪一个。（sequenced-before是在单个UE执行的操作的一种偏序关系。答题对应于这些操作的源程序顺序，是部分的是因为OpenCL C kernel语言未定义参数评估顺序）。
* 在OpenCL核语言中，obj的值在特定的点对work-item W可见时，是这个obj的初始值，或者一个W存储在这个obj里的值，或者其他work-item或host线程存储的值。依赖于host编程语言的细节，对host线程可见的obj值可能也是其他work-item或host线程在这个对象中存储的值。
* 两个表达式的评估存在冲突，如果他们其中一个更改了内存位置切另一个读或更改了相同的内存位置。
* 所有对特定原子对象M的修改都存在特定的顺序，叫做M的修改顺序 （modification order）如果A和B是一个原子对象M的修改，A happens-before B，那么在M的修改顺序中，A在B之前。注意，M的修改顺序与M在local还是global memory中无关。
* 释放顺序以原子对象M上的一个释放操作A开始，且是M的修改顺序中副作用的最大连续子序列，此处第一个操作是A，且每个后继操作做要么由同一个work-item或者执行释放的host线程执行，要么是一个原子的read-modif-write操作。
* OpenCL的本地和全局内存是不连续的。kernels可以访问两种内存但是host线程只能访问全局内存。此外，OpenCL的work_group_barrier函数里的flags参数指明了函数会使哪种内存操作可见：这些内存操作可以是对本地内存的，可以使对全局内存的或是对两者的。既然内存操作的可见性可以被指定为本地内存与全局内存区分开，我们定义两种相关但独立的关系：global-synchronizes-with和local-snchronizes-with。在全局内存上的确定操作可能与在另一个work-item或host线程上的其他操作有global-synchrionize-with的关系。
* 定义对内存的操作之间的顺序关系，global-happens-before 和local-happens-before以及其需要具备的条件。循环不能有这样的关系。
* 对副作用的定义。一个全局obj上的副作用需要满足的条件。
* 数据竞争的条件
以上都是规则性的东西。

原子操作

Fence操作

编程模型
The OpenCL Framework
框架让应用把host和一到多个devices当做单个的异构并行计算机系统来使用，包含以下三个组件：

*  OpenCL平台层：这层允许host program来感知设备及设备能力和创建上下文
*  OpenCL Runtime：允许host program在创建上下文后控制它们
*  OpenCL compiler：创建包含OpenCL kernel的可执行程序。