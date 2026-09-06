---
archive_policy: text-only
attachments:
- filename: web-computer-science-linux-performance-tools.html
  kind: document
  media_type: text/html
  role: original
  sha256: sha256:9aaed79234b5058ff42ff8e936153b5870641ca9ffc73123a65cc802c266836e
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-15ffe98b6e3c
  position:
    end: 257
    start: 0
    type: TextPositionSelector
  quote_sha256: sha256:221d180c612011b787d21bdf48d64750a146f46261f33aa676c157ddc84741fe
  selector:
    exact: 'linux 自身有很多性能分析工具。并且提供了详细的输出格式。熟练掌握这些工具可以帮助我们更快的发现性能瓶颈，为性能调优提供思路。

      load average：平均负载

      PID：进程号

      USER：进程所有者的名字。

      PRI：进程优先级

      NI nice：级别

      SIZE：进程使用的内存（代码、数据和栈），kb 单位

      RSS：物理 RAM 使用量，kb 单位

      SHARE：和其它进程共享的内存，kb 单位

      STAT 进程状态 S 睡眠，R=运行，T=停止或跟踪，D=不可中断的睡眠，Z=僵尸。

      %CPU CPU 使用量。'
    prefix: ''
    suffix: '

      %MEM 物理内存用量

      TIME进程使用的总 CPU 时间（从'
    type: TextQuoteSelector
  selector_sha256: sha256:6f6abb6d9107fcc8a0334b9d51a7b6659dfb3d973a7b3f3d15a4c28710ed35d3
  snapshot_sha256: sha256:c9d8d88e9b01c2576a70cf7146220cec02627023c153451c587b5748de5d767d
extractor: trafilatura/2.2.0
id: web-computer-science-linux-performance-tools
media_type: text/html
origin: external
raw_ref:
  path: archive/raw/9aaed79234b5058ff42ff8e936153b5870641ca9ffc73123a65cc802c266836e.html
  sha256: sha256:9aaed79234b5058ff42ff8e936153b5870641ca9ffc73123a65cc802c266836e
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: https://testerhome.com/topics/21513/show_wechat
  url: https://testerhome.com/topics/21513/show_wechat
schema_version: source/v1
snapshot_sha256: sha256:c9d8d88e9b01c2576a70cf7146220cec02627023c153451c587b5748de5d767d
source_type: doc
vault_id: public
---
linux 自身有很多性能分析工具。并且提供了详细的输出格式。熟练掌握这些工具可以帮助我们更快的发现性能瓶颈，为性能调优提供思路。
load average：平均负载
PID：进程号
USER：进程所有者的名字。
PRI：进程优先级
NI nice：级别
SIZE：进程使用的内存（代码、数据和栈），kb 单位
RSS：物理 RAM 使用量，kb 单位
SHARE：和其它进程共享的内存，kb 单位
STAT 进程状态 S 睡眠，R=运行，T=停止或跟踪，D=不可中断的睡眠，Z=僵尸。
%CPU CPU 使用量。
%MEM 物理内存用量
TIME进程使用的总 CPU 时间（从启动开始算）
COMMAND 进程的命令行启动命令（包括参数）
各列含义如下
进程
r:等待执行时间的进程数
b:在不可中断睡眠中的进程数
内存
swpd：已使用的虚拟内存量
free：空闲内存量
buff：作为缓冲的内存
cache：作缓存的内存
Swap
si：从交换分区写到内存的量
so：从内存写到交换分区的大小
IO
bi：磁盘读速率 (blocks/s)
bo：磁盘写速率 (blocks/s)
System
in：每秒钟的中断次数
cs：每秒的上下文切换次数
CPU（总 CPU 时间的百分比）：
us：用户空间运行的时间百分比
sy：系统空间运行的时间百分比
id：空闲时间
wa：等待 IO 的时间
vmstat -a  显示活跃和非活跃内存
    vmstat -f 显示从系统启动至今的 fork(系统调用)
    vmstat -s 显示内存相关统计信息及多种系统活动数量
    vmstat -d【查看磁盘的读写】
    vmstat -p /dev/sda1
    vmstat -m 查看系统的 slab 信息
1.Cpu64 位
2.Cpu 6 核
3.NUMA 点个节点
4.Cpu 的核心频率
5.说明此服务器为虚拟机
        sar -p（查看全天 cpu 数据）
        sar -u 1 10（1：每隔一秒，10：写入 10 次）
        sar -r（查看全天内存数据）
        sar -r 1 10
        sar -d 查看全天磁盘数据
        sar -d 1 2（1：每隔一秒，2：写入 2 次）
        sar -n DEV（查看全天网络流量数据）
        sar -n DEV 1 2
        sar -b 5 10 内存及交换空间 I/O 和传送速率监控
        sar -q 1 12 监控进程队列长度和平均负载状态
        sar -W 5 10 内存交换监控
        sar -d 1 2 -p 磁盘监控
        sar -B
mpstat -P ALL 1 每秒中采集一次 cpu  各个核心的使用资源情况
        mpstat -P 0 1 5 采集第一颗 cpu 的信息
iostat -x -k -d 1 采集 IO 数据
        iotop -botq -p【pid】输出进程的 io 信息
        iotop  -d 2 -n 5 间隔 2 秒，输出 5 次 监控时间段内的 IO
        iotop  -o  显示产生 IO 的进程 
        iostat -dxm 3
pidstat -u -p ALL 查看所有进程的 cpu 使用
        pidstat -r 查看进程的内存使用
        pidstat -d 查看进程 IO
        pidstat -w -p【pid】统计进程的上下文切换
 cswch/s：进程每秒主动切换次数
nvcswch/s：进程每秒被动切换次数
ps aux | sort -k3nr |head -n 10 按照按照消耗 CPU 前 10 排序的进程
    ps aux | sort -k4nr |head -n 10 按照按照消耗内存前 10 排序的进程
    ps -A -o stat,ppid,pid,cmd |grep -e '[Zz]' 定位僵尸进程
          kill -HUP 僵尸进程父 ID 杀死僵尸进程
    ps -eLo pid,stat | grep 3598 | grep running | wc -l  根据进程状态筛选线程
    pstree -p | wc -l  查询当前整个系统已用的线程或进程数
    pstree -p pid | wc -l 统计进程的线程数
    ps -o nlwp pid 查看进程下的线程数
1：netstat -nat|grep ESTABLISHED|wc -l  查看系统的总连接数
    2：netstat  -anp|grep pid|wc -l  统计进程的总连接数
    1 和 2 组合使用
    netstat -n | awk '/tcp/ {++S[$NF]} END {for(a in S) print a, S[a]}'   查看连接状态
进程模拟工具
    apt install sysbench sysstat 安装 sysbench
    sysbench --threads=10 --max-time=300 threads run  10 个线程运行 5 分钟的基准测试，模拟多线程切换
stress-ng -c 2 -t 30 -c 指定进程数 -t 指定时间
    stress-ng -c 2 --cpu-method pi 产生 2 个进程做圆周率算法压力
    stress-ng -c 16 --cpu-method all 生成 16 个进程使用多种不同的算法竞争 cpu
    stress-ng --sock 2 产生 2 个进程调用 socket 相关函数产生压力
    taskset -c 16 stress-ng --timeout 30 --cpu 1  生成 16 个进程对索引为 0 的逻辑 cpu 施加压力, 持续 30 秒
    stress-ng -c 0 -l 40 stress-ng -c 0 -l 40
    stress-ng -c 16 --timeout 300 模拟 16 个进程争夺 cpu 持续 300 秒
iozone 安装：
wget http://www.iozone.org/src/current/iozone3_482.tar
tar -xvf iozone3_429.tar
cd iozone3_429/src/current
apt-get install gcc
make
make linux-ia64
iozone 使用：
iozone -a -n 512k -g 4m -i 0 -i 1 -i 5 -f /mnt/iozone -Rb ./iozone.xls   从 512k 写到 4 兆的文件
time dd if=/dev/zero of=test bs=1M count=4096 测试 IO 读写速度
    sync;time -p bash -c "(dd if=/dev/zero of=test bs=1M count=200)" 当前目录下创建一个 test 文件，写入 200 个 1M 的数据。测试写瓶颈
    hdparm -tT --direct /dev/sda 测试读瓶颈
dstat -y  查看系统中断和上下文切换
    grep ctxt /proc/$pid/status 统计上下文切换数
    watch -d cat /proc/interrupts 统计进程中断的方式
    watch -d -n 1 'cat /proc/softirqs'查看中断种类。NET_TX 或 NET _RX 如果变化很快就是网络中断引起，否则 s1 系统其他原因造成的中断