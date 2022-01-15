- 设置时区

```sh
tzselect
```

```bash
cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
```

```bash
timedatectl list-timezones
timedatectl set-timezone Asia/Shanghai
```

- 设置时间

```bash
date -s "2020-04-18 09:09:09"
timedatectl set-time "2020-04-18 09:09:09"
```


## 配置

```sh
$ vim /etc/ntp.conf
server s1a.time.edu.cn prefer
restrict 192.168.20.0 mask 255.255.255.0 nomodify notrap
```

如果是要将本机作为顶层ntp服务器，可按以下配置：

```x
$ vim /etc/ntp.conf

server  127.127.1.0
fudge 127.127.1.0 stratum 0
restrict 192.168.55.0 mask 255.255.255.0 nomodify notrap

# fudge: 设置时间服务器的层级
# 格式：fudge ip [startnum int]
# 例子：fudge 10.225.5.1 startnum 10
# fudge必须和server一块用， 而且是在server的下一行
# startnum 0~15
#     0：表示顶级
#     10：通常用于给局域网主机提供时间服务
```

### restrict 控制相关权限。

语法: 
```
restrict IP地址 mask 子网掩码 参数
```

其中"IP地址"也可以是`default` ，指所有的IP

参数有以下几个：  
- `ignore`：关闭所有的 NTP 联机服务
- `nomodify`：客户端不能更改服务端的时间参数，但是客户端可以通过服务端进行网络校时。
- `notrust`：客户端除非通过认证，否则该客户端来源将被视为不信任子网
- `noquery`：不提供客户端的时间查询：用户端不能使用ntpq，ntpc等命令来查询ntp服务器
- `notrap`：不提供trap远端登陆：拒绝为匹配的主机提供模式 6 控制消息陷阱服务。陷阱服务是 ntpdq 控制消息协议的子系统，用于远程事件日志记录程序。
- `nopeer`：用于阻止主机尝试与服务器对等，并允许欺诈性服务器控制时钟
- `kod`： 访问违规时发送 KoD 包。
- `restrict -6`：表示IPV6地址的权限设置。

### 查询同步结果

```
[root@qwer /]# ntpq -p
     remote           refid      st t when poll reach   delay   offset  jitter
==============================================================================
 10.112.202.in-a .GPS.            1 u   22   64    3   98.888  -21.391  17.237
 ntp1.ams1.nl.le .STEP.          16 u    -   64    0    0.000    0.000   0.000
 stratum2-1.ntp. .STEP.          16 u    -   64    0    0.000    0.000   0.000
 124-108-20-1.st .STEP.          16 u    -   64    0    0.000    0.000   0.000
*electabuzz.feli 185.255.55.20    3 u   49   64    1  295.219  -15.540  20.121
[root@qwer /]# date
Mon Apr 22 15:19:40 CST 2019
```

- `st`：即stratum阶层，值越小表示ntp serve的精准度越高。
- `when`：几秒前曾做过时间同步更新的操作。
- `Poll`表示每隔多少毫秒与ntp server同步一次。
- `reach`：已经向上层NTP服务器要求更新的次数。
- `delay`：网络传输过程钟延迟的时间。
- `offset`：时间补偿的结果。
- `jitter`：Linux系统时间与BIOS硬件时间的差异时间


```
[root@iscsihost ~]# ntpq -c asso

ind assid status  conf reach auth condition  last_event cnt
===========================================================
  1 55829  963a   yes   yes  none  sys.peer    sys_peer  3
```

显示`sys.peer`则已经处于同步状态

### 将同步好的系统时间写入到硬件(BIOS)时间里

```sh
$ vim /etc/sysconfig/ntpd

# Drop root to id 'ntp:ntp' by default.
OPTIONS="-u ntp:ntp -p /var/run/ntpd.pid -g"
SYNC_HWCLOCK=yes    #添加一行SYNC_HWCLOCK=yes
```

### 修改ntp提供服务的ip地址

> 6 版本自带的ntp配置不生效，提示 `configure: keyword "interface" unknown, line ignored`

```sh
interface listen IPv4|IPv6|all 
interface ignore IPv4|IPv6|all 
interface drop IPv4|IPv6|all 
```

```sh
interface ignore wildcard       #忽略所有端口之上的监听
interface listen 172.16.3.1
interface listen 10.105.28.1
```