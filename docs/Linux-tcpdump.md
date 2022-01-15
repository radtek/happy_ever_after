EXAMPLE:

* To print all packets arriving at or departing from sundown:

```sh
tcpdump host sundown
```

* To print traffic between helios and either hot or ace:

```sh
tcpdump host helios and \( hot or ace \)
```

* To print all IP packets between ace and any host except helios:

```sh
tcpdump ip host ace and not helios
```

* To print all traffic between local hosts and hosts at Berkeley:

```sh
tcpdump net ucb-ether
```

* To  print  all ftp traffic through internet gateway snup: (note that the expression is quoted to prevent the shell from (mis-)interpreting the parentheses):

```sh
tcpdump 'gateway snup and (port ftp or ftp-data)'
```

* To print traffic neither sourced from nor destined for local hosts (if you gateway to one other net, this stuff should never make it onto your local net).

```sh
tcpdump ip and not net localnet
```

* To print the start and end packets (the SYN and FIN packets) of each TCP conversation that involves a non-local host.

```sh
tcpdump 'tcp[tcpflags] & (tcp-syn|tcp-fin) != 0 and not src and dst net localnet'
```

* To  print  all  IPv4  HTTP packets to and from port 80, i.e. print only packets that contain data, not, for example, SYN and FIN packets and ACK-only packets.  (IPv6 is left as an exercise for the reader.)

```sh
tcpdump 'tcp port 80 and (((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0)'
```

* To print IP packets longer than 576 bytes sent through gateway snup:

```sh
tcpdump 'gateway snup and ip[2:2] > 576'
```

* To print IP broadcast or multicast packets that were not sent via Ethernet broadcast or multicast:

```sh
tcpdump 'ether[0] & 1 = 0 and ip[16] >= 224'
```

* To print all ICMP packets that are not echo requests/replies (i.e., not ping packets):

```sh
tcpdump 'icmp[icmptype] != icmp-echo and icmp[icmptype] != icmp-echoreply'
```

* 抓取指定主机的ICMP包

```sh
tcpdump 'src host 192.168.161.1 and icmp'
```

* 抓取HTTP包

```sh
tcpdump  -XvvennSs 0 -i eth0 tcp[20:2]=0x4745 or tcp[20:2]=0x4854
```

0x4745 为"GET"前两个字母"GE",0x4854 为"HTTP"前两个字母"HT"。

> tcpdump 对截获的数据并没有进行彻底解码，数据包内的大部分内容是使用十六进制的形式直接打印输出的。显然这不利于分析网络故障，通常的解决办法是先使用带-w参数的tcpdump 截获数据并保存到文件中，然后再使用其他程序(如Wireshark)进行解码分析。当然也应该定义过滤规则，以避免捕获的数据包填满整个硬盘。

* tcpdump 与wireshark

Wireshark(以前是ethereal)是Windows下非常简单易用的抓包工具。但在Linux下很难找到一个好用的图形化抓包工具。我们可以用 `Tcpdump + Wireshark` 的完美组合实现：**在 Linux 里抓包，然后在Windows 里分析包。**

```sh
tcpdump tcp -i eth1 -t -s 0 -c 100 and dst port ! 22 and src net 192.168.1.0/24 -w ./target.cap

# (1) tcp       ip icmp arp rarp 和 tcp、udp、icmp这些选项等都要放到第一个参数的位置，用来过滤数据报的类型
# (2) -i eth1   只抓经过接口eth1的包
# (3) -t        不显示时间戳
# (4) -s 0      抓取数据包时默认抓取长度为68字节。加上 -s 0 后可以抓到完整的数据包
# (5) -c 100    只抓取100个数据包
# (6) dst port ! 22     不抓取目标端口是22的数据包
# (7) src net 192.168.1.0/24   数据包的源网络地址为192.168.1.0/24
```


## 1 选项

```sh
-A    以ASCII格式打印出所有分组，并将链路层的头最小化。 
-b    在数据-链路层上选择协议，包括ip、arp、rarp、ipx都是这一层的。
-c N  在收到指定的数量的分组后，tcpdump就会停止。 
-C N  在将一个原始分组写入文件之前，检查文件当前的大小是否超过了参数file_size 中指定的大小。如果超过了指定大小，则关闭当前文件，然后在打开一个新的文件。参数 file_size 的单位是兆字节（是1,000,000字节，而不是1,048,576字节）。 
      此选项用于配合-w file 选项使用
-d    将匹配信息包的代码以人们能够理解的汇编格式给出。 
-dd   将匹配信息包的代码以c语言程序段的格式给出。 
-ddd  将匹配信息包的代码以十进制的形式给出。 
-D    打印出系统中所有可以用tcpdump截包的网络接口。 
-e    在输出行打印出数据链路层的头部信息。 
-E    用spi@ipaddr algo:secret解密那些以addr作为地址，并且包含了安全参数索引值spi的IPsec ESP分组。 
-f    将外部的Internet地址以数字的形式打印出来。 
-F file   从指定的文件中读取表达式，忽略命令行中给出的表达式。 
-i interface   指定监听的网络接口。 
-l    使标准输出变为缓冲行形式，可以把数据导出到文件。 
-L    列出网络接口的已知数据链路。 
-m module   从文件module中导入SMI MIB模块定义。该参数可以被使用多次，以导入多个MIB模块。 
-M secret   如果tcp报文中存在TCP-MD5选项，则需要用secret作为共享的验证码用于验证TCP-MD5选选项摘要（详情可参考RFC 2385）。 
-n    不把网络地址转换成名字。
-nn   不进行端口名称的转换。
-N    不输出主机名中的域名部分。例如，'nic.ddn.mil' 只输出 'nic'。 
-O    不运行分组分组匹配（packet-matching）代码优化程序。 
-P    不将网络接口设置成混杂模式。 
-q    快速输出。只输出较少的协议信息。 
-r    从指定的文件中读取包(这些包一般通过-w选项产生)。 
-S    将tcp的序列号以绝对值形式输出，而不是相对值。 
-s    从每个分组中读取最开始的snaplen个字节，而不是默认的68个字节。 
-t    在输出的每一行不打印时间戳。 
-T    将监听到的包直接解释为指定的类型的报文，常见的类型有rpc远程过程调用）和snmp（简单网络管理协议；）。 
-t    不在每一行中输出时间戳。 
-tt   在每一行中输出非格式化的时间戳。 
-ttt  输出本行和前面一行之间的时间差。 
-tttt 在每一行中输出由date处理的默认格式的时间戳。 
-u    输出未解码的NFS句柄。 
-v    输出一个稍微详细的信息，例如在ip包中可以包括ttl和服务类型的信息。 
-vv   输出详细的报文信息。 
-w    直接将分组写入文件中，而不是不分析并打印出来。
```

## 2 表达式

```
dst  目的地址
src  原地址
host 主机名称
port 端口号
icmp icmp协议
tcp  tcp协议
udp  udp协议
```

* **第一种是关于类型的关键字**，主要包括: `host`, `net`, `port` (缺省的类型是host)
  * `host 210.27.48.2`, 指明 210.27.48.2是一台主机
  * `net 202.0.0.0`, 指明202.0.0.0是一个网络地址
  * `port 23`, 指明端口号是23

* **第二种是确定传输方向的关键字**，主要包括 `src`, `dst`, `dst or src`, `dst and src` (缺省是 `src or dst` 关键字)
  * `src 210.27.48.2`, 指明ip包中源地址是 210.27.48.2
  * `dst net 202.0.0.0`, 指明目的网络地址是 202.0.0.0 网段

* **第三种是协议的关键字**，主要包括 `fddi`, `ip`, `arp`, `rarp`, `tcp`, `udp` (缺省是所有协议的信息包)
  * `fddi` 指明是在FDDI (分布式光纤数据接口网络)上的特定的网络协议，实际上它是 `ether` 的别名
  * `fddi` 和 `ether` 具有类似的源地址和目的地址，所以可以将fddi协议包当作ether的包进行处理和分析
  * 其他的几个关键字就是指明了监听的包的协议内容

* **其他**重要的关键字：`gateway`, `broadcast`, `less`, `greater`

* **三种逻辑运算**: 
  * 取非运算是 `not`, `!`
  * 与运算是 `and`, `&&`
  * 或运算是 `or`, `||`

### 3 数据包

一般格式：

```sh
timestamp src > dst: flags data-seqno ack window urgent options

# (1) timestamp 时间
# (2) src 和 dst 是源和目的IP地址以及相应的端口. 
# (3) flags 标志由S(SYN), F(FIN), P(PUSH, R(RST), W(ECN CWT), E(ECN-Echo)组成, 单独一个'.'表示没有flags标识. 
# (4) 数据段顺序号(Data-seqno)描述了此包中数据所对应序列号空间中的一个位置(整个数据被分段, 每段有一个顺序号, 所有的顺序号构成一个序列号空间)(可参考以下例子). 
# (5) Ack 描述的是同一个连接, 同一个方向, 下一个本端应该接收的(对方应该发送的)数据片段的顺序号. 
# (6) Window是本端可用的数据接收缓冲区的大小(也是对方发送数据时需根据这个大小来组织数据).
# (7) Urg(urgent) 表示数据包中有紧急的数据. 
# (8) options 描述了tcp的一些选项, 这些选项都用尖括号来表示(如 <mss 1024>).

# src, dst 和 flags 这三个域总是会被显示. 其他域的显示与否依赖于tcp协议头里的信息.
```



```
13:29:07.788802 IP localhost.42333 > localhost.9501: Flags [S], seq 828582357, win 43690, options [mss 65495,sackOK,TS val 2207513 ecr 0,nop,wscale 7], length 0
13:29:07.788815 IP localhost.9501 > localhost.42333: Flags [S.], seq 1242884615, ack 828582358, win 43690, options [mss 65495,sackOK,TS val 2207513 ecr 2207513,nop,wscale 7], length 0
13:29:07.788830 IP localhost.42333 > localhost.9501: Flags [.], ack 1, win 342, options [nop,nop,TS val 2207513 ecr 2207513], length 0
13:29:10.298686 IP localhost.42333 > localhost.9501: Flags [P.], seq 1:5, ack 1, win 342, options [nop,nop,TS val 2208141 ecr 2207513], length 4
13:29:10.298708 IP localhost.9501 > localhost.42333: Flags [.], ack 5, win 342, options [nop,nop,TS val 2208141 ecr 2208141], length 0
13:29:10.298795 IP localhost.9501 > localhost.42333: Flags [P.], seq 1:13, ack 5, win 342, options [nop,nop,TS val 2208141 ecr 2208141], length 12
13:29:10.298803 IP localhost.42333 > localhost.9501: Flags [.], ack 13, win 342, options [nop,nop,TS val 2208141 ecr 2208141], length 0
13:29:11.563361 IP localhost.42333 > localhost.9501: Flags [F.], seq 5, ack 13, win 342, options [nop,nop,TS val 2208457 ecr 2208141], length 0
13:29:11.563450 IP localhost.9501 > localhost.42333: Flags [F.], seq 13, ack 6, win 342, options [nop,nop,TS val 2208457 ecr 2208457], length 0
13:29:11.563473 IP localhost.42333 > localhost.9501: Flags [.], ack 14, win 342, options [nop,nop,TS val 2208457 ecr 2208457], length 0
```

> *Tcpflags are some combination of: `S (SYN), F (FIN), P (PUSH), R (RST), U (URG), W (ECN CWR), E (ECN-Echo) or '.' (ACK), or 'none'` if no flags are set.*


* `13:29:11.563473` 时间带有精确到微妙
* `localhost.42333 > localhost.9501` 表示通信的流向，42333是客户端，9501是服务器端
* `[S]` SYN 表示这是一个SYN请求
* `[.]` ACK 表示这是一个ACK确认包，(client)SYN->(server)SYN->(client)ACK 就是3次握手过程
* `[P]` PUSH 表示这个是一个数据推送，可以是从服务器端向客户端推送，也可以从客户端向服务器端推
* `[F]` FIN 表示这是一个FIN包，是关闭连接操作，client/server都有可能发起
* `[R]` RST 表示这是一个RST包，与F包作用相同，但RST表示连接关闭时，仍然有数据未被处理。可以理解为是强制切断连接
* `win 342` 是指滑动窗口大小
* `length 12` 指数据包的大小