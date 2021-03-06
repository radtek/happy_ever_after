```
top - 10:09:07 up 8 days, 19:02,  4 users,  load average: 0.04, 0.04, 0.00
Tasks: 123 total,   1 running, 122 sleeping,   0 stopped,   0 zombie
%Cpu(s):  0.0 us,  1.6 sy,  0.0 ni, 98.4 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
KiB Mem:   3981096 total,  3779424 used,   201672 free,  1607320 buffers
KiB Swap:  6289404 total,   706320 used,  5583084 free.  1308880 cached Mem

   PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
159907 mongod    20   0 1544228  18500      0 S 6.667 0.465  20:56.98 mongod
     1 root      20   0   44208   4784   3520 S 0.000 0.120   0:13.07 systemd
     2 root      20   0       0      0      0 S 0.000 0.000   0:00.13 kthreadd
     4 root       0 -20       0      0      0 S 0.000 0.000   0:00.00 kworker/0:0H
     6 root       0 -20       0      0      0 S 0.000 0.000   0:00.00 mm_percpu_wq
    ...
```

### 第一行

```
top - 10:09:07 up 8 days, 19:02,  4 users,  load average: 0.04, 0.04, 0.00
```

| 值 | 含义 |
| -- | -- |
| 10:09:07                        | 当前时间 |
| up 8 days, 19:02                | 系统运行时间 |
| 4 users                            | 当前登录用户数 |
| load average: 0.04, 0.04, 0.00  | 系统负载, 即任务队列的平均长度(1min, 5mins, 15mins均值) |

### 第二行

```
Tasks: 123 total,   1 running, 122 sleeping,   0 stopped,   0 zombie
```

| 值 | 含义 |
| -- | --  |
| Tasks: 123 total | 进程总数        |
| 1 running       | 正在运行的进程数 |
| 122 sleeping     | 睡眠的进程数     |
| 0 stopped       | 停止的进程数     |
| 0 zombie        | 僵尸进程数       |

### 第三行

```
%Cpu(s):  0.0 us,  1.6 sy,  0.0 ni, 98.4 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
```

| 值 | 含义 |
| -- | --  |
| 0.0 us  | 用户空间占用CPU时间百分比 |
| 1.6 sy  | 内核空间占用CPU时间百分比 |
| 0.0 ni  | 用户进程空间内改变过优先级的进程占用CPU时间百分比 |
| 98.4 id | 空闲CPU百分比 |
| 0.0 wa  | 等待输入输出的CPU时间百分比 |
| 0.0 hi  | 硬中断时间百分比 |
| 0.0 si  | 硬中断时间百分比 |
| 0.0 st  | steal时间百分比 |

**关于ni的计算, 通过读取`/proc/stat`实现** :

```sh
$ cat /proc/stat
cpu  2939047 5858 1005425 300207263 622133 0 18329 4181 0 0
cpu0 736660 163 257532 75044952 168635 0 4031 364 0 0
cpu1 736841 266 250684 75071701 134149 0 4578 956 0 0
cpu2 752014 2257 244280 75057257 155210 0 3742 1713 0 0
cpu3 713530 3169 252928 75033351 164138 0 5977 1147 0 0
intr 205563381 16 1394 0 0 0 0 2569 0 0 1 0 34 261 0 787287 0 0 0 0 0 0 0 0 0 0 ...
ctxt 343737681
btime 1624432134
processes 4691045
procs_running 1
procs_blocked 0
softirq 310195783 3 81201514 673818 35254918 6660668 0 1407 77526953 0 108876502
```

输出中, 含**CPU指标**和**其他指标**: 

* CPU指标--度量尺度`USER_HZ`(1/100s, `sysconf(_SC_CLK_TCK)`)

| 值 | 含义 |
| -- | --  |
| user (2939047)   | 用户态时间 |
| nice (5858)      | 用户态时间(低优先级, nice>0) |
| system (1005425) | 内核态时间 |
| idle (300207263) | 空闲时间(除磁盘IO等待时间以外的等待时间) |
| iowait (622133)  | 磁盘IO等待时间 |
| irq (0)          | 硬中断时间 |
| softirq  (18329) | 软中断时间 |
| steal  (4181)    | 其他系统花费的时间(个人理解为虚拟化层面CPU调度产生的时间) |
| guest (0)        | 内核控制下vCPU损耗时间(如本机上的KVM虚拟机) |
| guest_nice (0)   | 内核控制下vCPU损耗时间(低优先级, nice>0) |

> 注： `iowait`有单独说明, `iowait`时间是不可靠值的,具体原因如下: 
> 
> (1) CPU不会等待I/O执行完成, 而`iowait`是等待I/O完成的时间。当CPU进入idle状态, 很可能会调度另一个task执行, 所以`iowait`计算时间偏小;   
> (2) 多核CPU中, `iowait`的计算并非某一个核, 因此计算每一个cpu的`iowait`非常困难;   
> (3) 这个值在某些情况下会减少。  


* 其他指标

| 值 | 含义 |
| -- | --  |
| intr          | 系统中断数(since boot) |
| ctxt          | 系统经历的上下文切换次数since boot |
| btime         | 系统启动时间点(时间戳) |
| processes     | 系统fork的进程数(since boot) |
| procs_running | 处于Runnable状态的进程个数 |
| procs_blocked | 处于I/O等待状态的进程个数 |

### 第四、五行

和`free`输出保持一致

```
KiB Mem:   3981096 total,  3779424 used,   201672 free,  1607320 buffers
KiB Swap:  6289404 total,   706320 used,  5583084 free.  1308880 cached Mem
```

### 进程信息区

| 列名 | 含义 |
| --- | --- |
| PID | 进程id |
| PPID | 父进程id |
| RUSER | Real user name |
| UID | 进程所有者的用户id |
| USER | 进程所有者的用户名 |
| GROUP | 进程所有者的组名 |
| TTY | 启动进程的终端名。不是从终端启动的进程则显示为 ? |
| PR | 优先级 |
| NI | nice值。负值表示高优先级, 正值表示低优先级 |
| P | 最后使用的CPU, 仅在多CPU环境下有意义 |
| TIME | 进程使用的CPU时间总计, 单位秒(`00:00:13`, 表示13s) |
| TIME+ | 进程使用的CPU时间总计, 单位1/100秒(`0:13.16`, 表示13.16s, 最后一位为1/100s) |
| %CPU | 上次更新到现在的CPU时间占用百分比 |
| %MEM | 进程使用的物理内存百分比(RES占比) |
| CODE | 可执行代码占用的物理内存大小, 单位kb |
| DATA | 可执行代码以外的部分(数据段+栈)占用的物理内存大小(数据驻留集或者DRS), 单位kb |
| RES | 进程使用的、未被换出的物理内存大小, 单位kb(驻留内存空间)。(man文档: `RES=CODE+DATA`) |
| SWAP | 进程使用的虚拟内存中, 被换出的大小, 单位kb(**已经申请但没有使用的空间**, 包括(栈、堆))。 |
| VIRT | 进程使用的虚拟内存总量, 单位kb。(man文档:`VIRT=SWAP+RES`, 实际测试为**所有已申请的内存空间** |
| SHR | 进程使用的共享内存大小, 单位kb |
| nFLT | 页面错误次数 |
| nDRT | 最后一次写入到现在, 被修改过的页面数。 |
| S | D=不可中断的睡眠状态<br>R=运行<br>S=睡眠<br>T=跟踪/停止<br>Z=僵尸进程 |
| COMMAND | 命令名/命令行 |
| WCHAN | 若该进程在睡眠, 则显示睡眠中的系统函数名 |
| Flags | 任务标志, 参考 sched.h |


### 更改显示内容

### top命令参数(常用选项)

| 选项 | 含义 |
| ---- | ---- |
| `-b` | 批出模式(不覆盖之前的输出结果) |
| `-c` | 显示整个命令行而不只是显示命令名 |
| `-d` | 指定每两次屏幕信息刷新之间的时间间隔。当然用户可以使用s交互命令来改变之 |
| `-i` | 使top不显示任何闲置(idle)或者僵死(zombie)进程 |
| `-n` | 更新的次数, 完成后将会退出top |
| `-o` | 指定按某列排序<br>`-o +PID`: 按PID排序, high->low<br>`-o -PID`: 按PID排序, low->high|
| `-O` | 显示top所有列标题 |
| `-p` | 通过指定监控进程ID来仅仅监控某个进程的状态 |
| `-q` | 该选项将使top没有任何延迟的进行刷新。如果调用程序有超级用户权限, 那么top将以尽可能高的优先级运行 |
| `-S` | 指定累计模式(包含己完成或消失的子进程CPU时间) |
| `-s` | 使top命令在安全模式中运行。这将去除交互命令所带来的潜在危险(不能利用交谈式指令对进程下命令) |
| `-u` | 指定显示哪个用户的进程信息(uid/username) |
| `-w` | 指定显示宽度(一般与`-b`一起使用) |

### top交互命令

h或者? 显示帮助画面, 给出一些简短的命令总结说明。 
k  | 终止一个进程。系统将提示用户输入需要终止的进程PID, 以及需要发送给该进程什么样的信号。一般的终止进程可以使用15信号；如果不能正常结束那就使用信号9强制结束该进程。默认值是信号15。在安全模式中此命令被屏蔽。 
i | 忽略闲置和僵死进程。这是一个开关式命令。 
q | 退出程序。 
r | 重新安排一个进程的优先级别。系统提示用户输入需要改变的进程PID以及需要设置的进程优先级值。输入一个正值将使优先级降低, 反之则可以使该进程拥有更高的优先权。默认值是10。 
S | 切换到累计模式。 
s | 改变两次刷新之间的延迟时间。系统将提示用户输入新的时间, 单位为s。如果有小数, 就换算成m s。输入0值则系统将不断刷新, 默认值是5 s。需要注意的是如果设置太小的时间, 很可能会引起不断刷新, 从而根本来不及看清显示的情况, 而且系统负载也会大大增加。 
f/F | 从当前显示中添加或者删除项目。 
o/O | 改变显示项目的顺序。 
u/U | 改变显示哪个用户的进程
l 切换显示平均负载和启动时间信息。 
m 切换显示内存信息。 
t 切换显示进程和CPU状态信息。 
c 切换显示命令名称和完整命令行。 
M 根据驻留内存大小进行排序。 
P 根据CPU使用百分比大小进行排序。 
T 根据时间/累计时间进行排序。 
W 将当前设置写入~/.toprc文件中。这是写top配置文件的推荐方法。
