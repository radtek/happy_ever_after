## 创建

### 推荐做法1：用`mktemp`创建只有脚本作者能访问的临时目录

```sh
function func()
{
    : ${TMPDIR:=/tmp}
    local temp_dir=""
    local save_mask=$(umask)
    umask 077
    temp_dir=$(mktemp -d "${TMPDIR}/XXXXXXXXXXXXXXXXXX") 
    if [ $? -ne 0 ]
    then
        #出错处理
        umask "${save_mask}"
        return 1
    fi
    umask "${save_mask}"

    #业务逻辑
}
```

### 推荐做法2：如果不支持命令`mktemp`，则用`mkdir`创建只有脚本作者能访问的临时目录

```sh
function func()
{
    local temp_dir="/tmp/tmp_${RANDOM}_$$"
    mkdir -m 700 "${temp_dir}"
    if [ $? -ne 0 ]
    then
        #出错处理"
        return 1
    fi

    #业务逻辑
}
```

## 删除

### 推荐做法：使用`mktemp`创建只有脚本作者能访问的临时目录，并用`trap`命令在脚本退出时删除整个临时目录

```sh
#!/bin/bash
 
: ${TMPDIR:=/tmp}
trap '[ -n "${temp_dir}" ] && rm -rf "${temp_dir}"' EXIT
 
save_mask=$(umask)
umask 077
temp_dir=$(mktemp -d "${TMPDIR}/XXXXXXXXXXXXXXXXXX") 
if [ $? -ne 0 ]
then
    #出错处理
    umask "${save_mask}"
    exit 1
fi    
umask "${save_mask}"

#业务逻辑
```

### `trap` 扩展

**1. 命令格式**

```sh
# 1. 当脚本收到signal-list清单内列出的信号时, trap命令执行双引号中的命令
trap "commands" signal-list

# 2. trap指定为"-", 接受信号的默认操作
trap - signal-list

# 3. trap命令指定空命令串("")，允许忽视信号
trap "" signal-list
trap " " signal-list #类似于不执行
trap ":" signal-list
```

**2. 信号说明**

如常见的`Ctrl+C`组合键会产生`SIGINT`信号，`Ctrl+Z`会产生`SIGTSTP`信号。

名称|默认动作|说明
 -- | -- | --
`SIGHUP`|终止进程|终端线路挂断
`SIGINT`|终止进程|中断进程
`SIGQUIT`|建立CORE文件|终止进程，并且生成core文件
`SIGILL`|建立CORE文件|非法指令
`SIGTRAP`|建立CORE文件|跟踪自陷
`SIGBUS`|建立CORE文件|总线错误
`SIGSEGV`|建立CORE文件|段非法错误
`SIGFPE`|建立CORE文件|浮点异常
`SIGIOT`|建立CORE文件|执行I/O自陷
`SIGKILL`|终止进程|杀死进程
`SIGPIPE`|终止进程|向一个没有读进程的管道写数据
`SIGALARM`|终止进程|计时器到时
`SIGTERM`|终止进程|软件终止信号
`SIGSTOP`|停止进程|非终端来的停止信号
`SIGTSTP`|停止进程|终端来的停止信号
`SIGCONT`|忽略信号|继续执行一个停止的进程
`SIGURG`|忽略信号|I/O紧急信号
`SIGIO`|忽略信号|描述符上可以进行I/O
`SIGCHLD`|忽略信号|当子进程停止或退出时通知父进程
`SIGTTOU`|停止进程|后台进程写终端
`SIGTTIN`|停止进程|后台进程读终端
`SIGXGPU`|终止进程|CPU时限超时
`SIGXFSZ`|终止进程|文件长度过长
`SIGWINCH`|忽略信号|窗口大小发生变化
`SIGPROF`|终止进程|统计分布图用计时器到时
`SIGUSR1`|终止进程|用户定义信号1
`SIGUSR2`|终止进程|用户定义信号2
`SIGVTALRM`|终止进程|虚拟计时器到时

也可以用数字指定信号, 对应关系:

| Signal Number | Signal Name |
|       --      |    --       |
| 0             | EXIT        |
| 1             | SIGHUP      |
| 2             | SIGINT      |
| 3             | SIGQUIT     |
| 6             | SIGABRT     |
| 9             | SIGKILL     |
| 14            | SIGALRM     |
| 15            | SIGTERM     |


扩展: `kill`命令支持的信号: 

```sh
$ trap -l
 1) SIGHUP       2) SIGINT       3) SIGQUIT      4) SIGILL       5) SIGTRAP
 6) SIGABRT      7) SIGBUS       8) SIGFPE       9) SIGKILL     10) SIGUSR1
11) SIGSEGV     12) SIGUSR2     13) SIGPIPE     14) SIGALRM     15) SIGTERM
16) SIGSTKFLT   17) SIGCHLD     18) SIGCONT     19) SIGSTOP     20) SIGTSTP
21) SIGTTIN     22) SIGTTOU     23) SIGURG      24) SIGXCPU     25) SIGXFSZ
26) SIGVTALRM   27) SIGPROF     28) SIGWINCH    29) SIGIO       30) SIGPWR
31) SIGSYS      34) SIGRTMIN    35) SIGRTMIN+1  36) SIGRTMIN+2  37) SIGRTMIN+3
38) SIGRTMIN+4  39) SIGRTMIN+5  40) SIGRTMIN+6  41) SIGRTMIN+7  42) SIGRTMIN+8
43) SIGRTMIN+9  44) SIGRTMIN+10 45) SIGRTMIN+11 46) SIGRTMIN+12 47) SIGRTMIN+13
48) SIGRTMIN+14 49) SIGRTMIN+15 50) SIGRTMAX-14 51) SIGRTMAX-13 52) SIGRTMAX-12
53) SIGRTMAX-11 54) SIGRTMAX-10 55) SIGRTMAX-9  56) SIGRTMAX-8  57) SIGRTMAX-7
58) SIGRTMAX-6  59) SIGRTMAX-5  60) SIGRTMAX-4  61) SIGRTMAX-3  62) SIGRTMAX-2
63) SIGRTMAX-1  64) SIGRTMAX
```

**3. 示例**

* 示例一: 捕获`Ctrl-C`

```sh
#!/bin/bash
trap "echo 'Sorry! I have trapped Ctrl-C'" SIGINT

echo This is a test script

count=1
while [ $count -le 10 ]
do
  echo "Loop $count"
  sleep 1
  count=$[ $count + 1 ]
done

echo The end.
```

运行结果：

```
This is a test script
Loop 1
Loop 2
^CSorry! I have trapped Ctrl-C
Loop 3
Loop 4
^CSorry! I have trapped Ctrl-C
Loop 5
Loop 6
Loop 7
Loop 8
^CSorry! I have trapped Ctrl-C
Loop 9
Loop 10
The end.
```

* 示例二: 捕获脚本退出信号

```sh
#!/bin/bash
trap "echo Goodbye." EXIT

echo This is a test script

count=1
while [ $count -le 10 ]
do
  echo "Loop $count"
  sleep 1
  count=$[ $count + 1 ]
done

echo The end.
```

运行结果：

```
This is a test script
Loop 1
Loop 2
Loop 3
Loop 4
Loop 5
Loop 6
Loop 7
Loop 8
Loop 9
Loop 10
The end.
Goodbye.
```

* 示例三: 脚本中途可以修改`trap`设置

```sh
#!/bin/bash
trap "echo 'Sorry! I have trapped Ctrl-C'" SIGINT

count=1
while [ $count -le 5 ]
do
  echo "Loop $count"
  sleep 1
  count=$[ $count + 1 ]
done


trap "echo 'Sorry! The trap has been modified.'" SIGINT

count=1
while [ $count -le 5 ]
do
  echo "Loop $count"
  sleep 1
  count=$[ $count + 1 ]
done

echo The end.
```

运行结果：

```
Loop 1
Loop 2
Loop 3
^CSorry! I have trapped Ctrl-C
Loop 4
Loop 5
Loop 1
Loop 2
Loop 3
^CSorry! The trap has been modified.
Loop 4
Loop 5
The end.
```

```sh
$ stty -a # 显示触发某些信号的键位
speed 38400 baud; rows 61; columns 236; line = 0;
intr = ^C; quit = ^\; erase = ^?; kill = ^U; eof = ^D; eol = <undef>; eol2 = <undef>; swtch = <undef>; start = ^Q; stop = ^S; susp = ^Z; rprnt = ^R; werase = ^W; lnext = ^V; discard = ^O; min = 1; time = 0;
-parenb -parodd -cmspar cs8 -hupcl -cstopb cread -clocal -crtscts
-ignbrk -brkint -ignpar -parmrk -inpck -istrip -inlcr -igncr icrnl ixon -ixoff -iuclc -ixany -imaxbel -iutf8
opost -olcuc -ocrnl onlcr -onocr -onlret -ofill -ofdel nl0 cr0 tab0 bs0 vt0 ff0
isig icanon iexten echo echoe echok -echonl -noflsh -xcase -tostop -echoprt echoctl echoke -flusho -extproc
```




