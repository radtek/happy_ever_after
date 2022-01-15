> 环境

| 系统  |主机名  |系统IP              |心跳IP         |存储IP(iSCSI)    |服务            |共享盘               |
|  --   | --     |      --            |       --      |     --          |        --      |    --               |
|       |        |                    |               | team2           | -              | -                   |
|Centos7| Host   | 192.168.163.240/24 |       -       | 20.20.20.240/24 | iscsi目标、ntp | /dev/sdb<br>/dev/sdc|


| 系统  |主机名  |系统IP              |心跳IP           |存储IP(iSCSI)    |服务                  |共享盘    |ftp服务ip|
|  --   | --     |      --            |       --        |     --          |        --            |    --    | --      |
|       |        |                    | team1           | team2           | -                    | -        |team1    |
|Centos7| node01 | 192.168.163.241/24 | 10.10.10.241/24 | 20.20.20.241/24 | pcsd,corosync,vsftpd | /dev/sdb |1.1.1.1.241/24|
|Centos7| node02 | 192.168.163.242/24 | 10.10.10.242/24 | 20.20.20.241/24 | pcsd,corosync,vsftpd | /dev/sdb |1.1.1.1.242/24|


| 系统  |主机名  |系统IP              |心跳IP           |存储IP(iSCSI)    |服务               |共享盘    |ftp服务ip|
|  --   | --     |      --            |       --        |     --          |        --         |    --    | --      |
|       |        |                    | bond0           | bond1           | -                 | -        |bond0    |
| REHL6 | node03 | 192.168.163.243/24 | 10.10.10.243/24 | 20.20.20.243/24 | ricci,luci,vsftpd | /dev/sdc |10.10.10.3/24|
| REHL6 | node04 | 192.168.163.244/24 | 10.10.10.244/24 | 20.20.20.243/24 | ricci,vsftpd      | /dev/sdc |10.10.10.4/24|



## 1. 搭建ISCSI目标(提供共享盘)、NTP服务器(提供时间同步)


### 1.1 网络配置

| 系统  |主机名  |系统IP              |心跳IP         |存储IP(iSCSI)    |服务            |共享盘               |
|  --   | --     |      --            |       --      |     --          |        --      |    --               |
|       |        | -                  | -             | team2           | -              | -                   |
|Centos7| Host   | 192.168.163.240/24 |       -       | 20.20.20.240/24 | iscsi目标、ntp | /dev/sdb<br>/dev/sdc|

创建网络组提供冗余：

```sh
nmcli connection add type team con-name team2 ifname team2 config '{"runner":{"name":"activebackup"}}'

nmcli connection modify team2 ipv4.method manual ipv4.addresses 20.20.20.241/24

nmcli connection add type team-slave con-name team2-ens193 ifname ens193 master team2
nmcli connection add type team-slave con-name team2-ens161 ifname ens161 master team2
```

### 1.2 搭建NTP Server



- 安装

```
yum -y install ntp
```

- 防火墙配置

```
firewall-cmd --add-service=ntp --permanent
firewall-cmd --reload
```

- 配置

> 配置以本机时间为准。

注释掉所有已有的server配置行，添加以下配置：


```x
$ vim /etc/ntp.conf

#server 0.centos.pool.ntp.org iburst
#server 1.centos.pool.ntp.org iburst
#server 2.centos.pool.ntp.org iburst
#server 3.centos.pool.ntp.org iburst

restrict 192.168.163.0 mask 255.255.255.0 nomodify notrap
server 127.127.1.0
fudge 127.127.1.0 stratum 0
```

- 启停

```sh
# 如果有chronyd，关闭chronyd，避免冲突
systemctl stop chronyd
systemctl disable chtronyd 

systemctl start ntpd
systemctl enable ntpd
```

以下结果表明ntp服务正常

```x
$ ps -ef | grep ntpd
ntp       12571      1  0 15:15 ?        00:00:00 /usr/sbin/ntpd -u ntp:ntp -g
root      12669  11832  0 15:19 pts/0    00:00:00 grep --color=auto ntpd

$ ntpq -p 
     remote           refid      st t when poll reach   delay   offset  jitter
==============================================================================
*LOCAL(0)        .LOCL.           0 l   23   64   17    0.000    0.000   0.000
```


### 1.3 搭建iSCSI Target



> 通过targetcli提供iSCSI共享盘

- 安装

```sh
yum -y install targetcli
```

```x
$ targetcli ls 

Warning: Could not load preferences file /root/.targetcli/prefs.bin.
o- / ......................................................................................................................... [...]
  o- backstores .............................................................................................................. [...]
  | o- block .................................................................................................. [Storage Objects: 0]
  | o- fileio ................................................................................................. [Storage Objects: 0]
  | o- pscsi .................................................................................................. [Storage Objects: 0]
  | o- ramdisk ................................................................................................ [Storage Objects: 0]
  o- iscsi ............................................................................................................ [Targets: 0]
  o- loopback ......................................................................................................... [Targets: 0]
```

- 配置

	* 创建两个block
	
	```
	targetcli /backstores/block create SharedDisk01 /dev/sdb
	targetcli /backstores/block create SharedDisk02 /dev/sdc
	```
	
	* 创建两个target，分别分配给inititor
	
	```
	targetcli /iscsi create iqn.2019-12.com.test:targer01
	targetcli /iscsi/iqn.2019-12.com.test:targer01/tpg1/acls create iqn.2019-12.com.test:targer01node01
	targetcli /iscsi/iqn.2019-12.com.test:targer01/tpg1/acls create iqn.2019-12.com.test:targer01node01
	
	targetcli /iscsi create iqn.2019-12.com.test:targer02
	targetcli /iscsi/iqn.2019-12.com.test:targer02/tpg1/acls create iqn.2019-12.com.test:targer02node03
	targetcli /iscsi/iqn.2019-12.com.test:targer02/tpg1/acls create iqn.2019-12.com.test:targer02node04
	```
	
	* 将之前创建的两个block(`ShareDisk01`,`ShareDisk02`)分配给两个target
	
	```
	targetcli /iscsi/iqn.2019-12.com.test:targer01/tpg1/luns create /backstores/block/SharedDisk01
	targetcli /iscsi/iqn.2019-12.com.test:targer02/tpg1/luns create /backstores/block/SharedDisk02
	```

	* 配置监听: 取消默认的`0.0.0.0:3260`，设置`20.20.20.240:3260`
	
	```sh
	targetcli /iscsi/iqn.2019-12.com.test:targer01/tpg1/portals delete 0.0.0.0 3260
	targetcli /iscsi/iqn.2019-12.com.test:targer02/tpg1/portals delete 0.0.0.0 3260
	
	targetcli /iscsi/iqn.2019-12.com.test:targer01/tpg1/portals create 20.20.20.240 3260
	targetcli /iscsi/iqn.2019-12.com.test:targer02/tpg1/portals create 20.20.20.240 3260
	```
	
- 防火墙配置
	
```sh
firewall-cmd --add-service=iscsi-target --permanent
firewall-cmd --reload
```

- 配置完成结果如下

```x
$ targetcli ls 

o- / ......................................................................................................................... [...]
  o- backstores .............................................................................................................. [...]
  | o- block .................................................................................................. [Storage Objects: 2]
  | | o- SharedDisk01 .................................................................... [/dev/sdb (10.0GiB) write-thru activated]
  | | | o- alua ................................................................................................... [ALUA Groups: 1]
  | | |   o- default_tg_pt_gp ....................................................................... [ALUA state: Active/optimized]
  | | o- SharedDisk02 .................................................................... [/dev/sdc (10.0GiB) write-thru activated]
  | |   o- alua ................................................................................................... [ALUA Groups: 1]
  | |     o- default_tg_pt_gp ....................................................................... [ALUA state: Active/optimized]
  | o- fileio ................................................................................................. [Storage Objects: 0]
  | o- pscsi .................................................................................................. [Storage Objects: 0]
  | o- ramdisk ................................................................................................ [Storage Objects: 0]
  o- iscsi ............................................................................................................ [Targets: 2]
  | o- iqn.2019-12.com.test:targer01 ..................................................................................... [TPGs: 1]
  | | o- tpg1 ............................................................................................... [no-gen-acls, no-auth]
  | |   o- acls .......................................................................................................... [ACLs: 2]
  | |   | o- iqn.2019-12.com.test:targer01node01 .................................................................. [Mapped LUNs: 1]
  | |   | | o- mapped_lun0 .......................................................................... [lun0 block/SharedDisk01 (rw)]
  | |   | o- iqn.2019-12.com.test:targer01node02 .................................................................. [Mapped LUNs: 1]
  | |   |   o- mapped_lun0 .......................................................................... [lun0 block/SharedDisk01 (rw)]
  | |   o- luns .......................................................................................................... [LUNs: 1]
  | |   | o- lun0 ............................................................... [block/SharedDisk01 (/dev/sdb) (default_tg_pt_gp)]
  | |   o- portals .................................................................................................... [Portals: 1]
  | |     o- 20.20.20.240:3260 ................................................................................................ [OK]
  | o- iqn.2019-12.com.test:targer02 ..................................................................................... [TPGs: 1]
  |   o- tpg1 ............................................................................................... [no-gen-acls, no-auth]
  |     o- acls .......................................................................................................... [ACLs: 2]
  |     | o- iqn.2019-12.com.test:targer02node03 .................................................................. [Mapped LUNs: 1]
  |     | | o- mapped_lun0 .......................................................................... [lun0 block/SharedDisk02 (rw)]
  |     | o- iqn.2019-12.com.test:targer02node04 .................................................................. [Mapped LUNs: 1]
  |     |   o- mapped_lun0 .......................................................................... [lun0 block/SharedDisk02 (rw)]
  |     o- luns .......................................................................................................... [LUNs: 1]
  |     | o- lun0 ............................................................... [block/SharedDisk02 (/dev/sdc) (default_tg_pt_gp)]
  |     o- portals .................................................................................................... [Portals: 1]
  |       o- 20.20.20.240:3260 ................................................................................................ [OK]
  o- loopback ......................................................................................................... [Targets: 0]
```

```
$ netstat -an | grep 3260
tcp        0      0 20.20.20.240:3260       0.0.0.0:*               LISTEN 
```

- 客户端对服务端target共享出去的磁盘做了lvm，当服务端重启，可能会失去对block。
    * 原因：服务端的`lvm2-lvmetad.service`将客户端的lvm识别并纳管，导致target绑定的/dev/sdb,/dev/sdc无法被识别。
    * 解决：修改`/etc/lvm/lvm.conf`中`volume_list = [ "rhel_host0"]`，即只将主机上的卷组添加进去，其他的不添加。关闭target，重启lvm2-lvmetad.server。最好重启服务器。


## 2. Pacemaker+Corosync+vsFTPd



| 系统  |主机名  |系统IP              |心跳IP           |存储IP(iSCSI)    |服务                  |共享盘    |
|  --   | --     |      --            |       --        |     --          |        --            |    --    |
|       |        |                    | team1           | team2           | -                    | -        |
|Centos7| node01 | 192.168.163.241/24 | 10.10.10.241/24 | 20.20.20.241/24 | pcsd,corosync,vsftpd | /dev/sdc |
|Centos7| node02 | 192.168.163.242/24 | 10.10.10.242/24 | 20.20.20.241/24 | pcsd,corosync,vsftpd | /dev/sdc |




### 2.1 网络配置



- node01

```
nmcli connection add type team con-name team1 ifname team1 config '{"runner":{"name":"activebackup"}}'
nmcli connection add type team con-name team2 ifname team2 config '{"runner":{"name":"activebackup"}}'

nmcli connection modify team1 ipv4.method manual ipv4.addresses 10.10.10.241/24
nmcli connection modify team2 ipv4.method manual ipv4.addresses 20.20.20.241/24

nmcli connection add type team-slave con-name team1-ens224 ifname ens224 master team1
nmcli connection add type team-slave con-name team1-ens256 ifname ens256 master team1

nmcli connection add type team-slave con-name team2-ens193 ifname ens193 master team2
nmcli connection add type team-slave con-name team2-ens161 ifname ens161 master team2
```

- node02

```
nmcli connection add type team con-name team1 ifname team1 config '{"runner":{"name":"activebackup"}}'
nmcli connection add type team con-name team2 ifname team2 config '{"runner":{"name":"activebackup"}}'

nmcli connection modify team1 ipv4.method manual ipv4.addresses 10.10.10.242/24
nmcli connection modify team2 ipv4.method manual ipv4.addresses 20.20.20.242/24

nmcli connection add type team-slave con-name team1-ens224 ifname ens224 master team1
nmcli connection add type team-slave con-name team1-ens256 ifname ens256 master team1

nmcli connection add type team-slave con-name team2-ens193 ifname ens193 master team2
nmcli connection add type team-slave con-name team2-ens161 ifname ens161 master team2
```

### 2.2 系统准备工作 (每个节点均需要执行)



#### 2.2.1 配置NTP Client



注释掉所有已有的server配置行，添加以下配置

```x
$ vim /etc/chrony.conf

#server 0.centos.pool.ntp.org iburst
#server 1.centos.pool.ntp.org iburst
#server 2.centos.pool.ntp.org iburst
#server 3.centos.pool.ntp.org iburst
server 192.168.163.240 iburst
```

```sh
systemctl restart chronyd
systemctl enable chronyd
```

```x
$ chronyc sources -v 

210 Number of sources = 1

  .-- Source mode  '^' = server, '=' = peer, '#' = local clock.
 / .- Source state '*' = current synced, '+' = combined , '-' = not combined,
| /   '?' = unreachable, 'x' = time may be in error, '~' = time too variable.
||                                                 .- xxxx [ yyyy ] +/- zzzz
||      Reachability register (octal) -.           |  xxxx = adjusted offset,
||      Log2(Polling interval) --.      |          |  yyyy = measured offset,
||                                \     |          |  zzzz = estimated error.
||                                 |    |           \
MS Name/IP address         Stratum Poll Reach LastRx Last sample               
===============================================================================
^* 192.168.163.240               1   6    17     3    -27us[  -35us] +/-   12ms
```

#### 2.2.2 配置解析记录



```
$ vim /etc/hosts

10.10.10.241 node01
10.10.10.242 node02
```

#### 2.2.3 配置iSCSI Inititor



- 安装

```sh
yum -y install iscsi-initiator-utils
```

- 修改InititorName (`/etc/iscsi/initiatorname.iscsi`)，与Target端配置一致: 

&emsp;&emsp;node01 : `InitiatorName=iqn.2019-12.com.test:targer01node01`  
&emsp;&emsp;node02 : `InitiatorName=iqn.2019-12.com.test:targer01node02`  


- 启动iscsi和iscsid服务, 并设置自启

```sh
systemctl restart iscsi
systemctl restart iscsid

systemctl enable iscsi
systemctl enable iscsid
```

- 发现iSCSI目标

```
$ iscsiadm --mode discoverydb --type sendtargets --portal 20.20.20.240 --discover

20.20.20.240:3260,1 iqn.2019-12.com.test:targer01
20.20.20.240:3260,1 iqn.2019-12.com.test:targer02
```

- 登录

```sh
$ iscsiadm --mode node --targetname iqn.2019-12.com.test:targer01 --portal 20.20.20.240:3260 --login

Logging in to [iface: default, target: iqn.2019-12.com.test:targer01, portal: 20.20.20.240,3260] (multiple)
Login to [iface: default, target: iqn.2019-12.com.test:targer01, portal: 20.20.20.240,3260] successful.
```

- 若要登出，先取消所有磁盘占用，然后执行以下命令：

```sh
iscsiadm --mode node --targetname iqn.2019-12.com.test:targer01 --portal 120.20.20.240,3260 --logout
```

> 以上三步可参考 `iscsiadm` man文档的 `EXAMPLE` 部分获取帮助

- 各个节点均发现磁盘，表明配置正常：

```x
$ lsblk

NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda      8:0 0   16G  0 disk 
├─sda1   8:1 0    1G  0 part /boot
├─sda2   8:2 0  1.6G  0 part [SWAP]
└─sda3   8:3 0 13.4G  0 part /
sdb      8:160   10G  0 disk 
sr0     11:0 1  4.3G  0 rom  
loop0    7:0 0  4.3G  0 loop /root/centos7.yum
```

#### 配置共享磁盘



> 通过lvm方式创建xfs格式的磁盘

- 创建逻辑卷  

```sh
pvcreate /dev/sdb
vgcreate vg_data01 /dev/sdb
lvcreate -n lv_data01 -l 50%FREE vg_data01
lvcreate -n lv_data01 -l 50%FREE vg_data02
```

- 创建文件系统

```
mkfs.xfs /dev/mapper/vg_data01-lv_data01
mkfs.xfs /dev/mapper/vg_data01-lv_data02
```


#### 配置vsftpd服务

```sh
mkdir /data01
mkdir /data02
yum install -y vsftpd
useradd vsftpd
```

添加配置文件：

```
$ vim /etc/vsftpd/vsftpd_ftp01.conf

anonymous_enable=NO
guest_enable=NO
local_enable=YES
write_enable=YES
local_umask=022
port_enable=YES
pasv_enable=NO
dirmessage_enable=YES
ftpd_banner=Welcome to blah FTP service
xferlog_enable=YES
xferlog_std_format=YES
xferlog_file=/var/log/ftp01_xferlog
dual_log_enable=YES
vsftpd_log_file=/var/log/ftp01_vsftpd.log
nopriv_user=vsftpd
connect_from_port_20=YES
chroot_local_user=NO
chroot_list_enable=YES
chroot_list_file=/etc/vsftpd/chroot_list01
listen=YES
listen_ipv6=NO
listen_address=1.1.1.241
pam_service_name=vsftpd
userlist_enable=YES
userlist_deny=NO
tcp_wrappers=YES
local_root=/data01
use_localtime=YES
allow_writeable_chroot=YES
```

```
$ vim /etc/vsftpd/vsftpd_ftp02.conf

anonymous_enable=NO
guest_enable=NO
local_enable=YES
write_enable=YES
local_umask=022
port_enable=YES
pasv_enable=NO
dirmessage_enable=YES
ftpd_banner=Welcome to blah FTP service
xferlog_enable=YES
xferlog_std_format=YES
xferlog_file=/var/log/ftp02_xferlog
dual_log_enable=YES
vsftpd_log_file=/var/log/ftp02_vsftpd.log
nopriv_user=vsftpd
connect_from_port_20=YES
chroot_local_user=NO
chroot_list_enable=YES
chroot_list_file=/etc/vsftpd/chroot_list02
listen=YES
listen_ipv6=NO
listen_address=1.1.1.242
pam_service_name=vsftpd
userlist_enable=YES
userlist_deny=NO
tcp_wrappers=YES
local_root=/data02
use_localtime=YES
allow_writeable_chroot=YES
```

防火墙配置：

```
firewall-cmd --add-service=ftp --pernament
firewall-cmd --reload
```

### 2.3 HA配置



#### (1) 安装

```sh
yum -y groupinstall 'High Availability'
```

注:未安装相应的fence设备


#### (2) 配置防火墙

**TCP** : 2224、3121、21064  
**UDP** : 5405  
**DLM** : 21064 (如果使用add-on clvm/GFS2 的 DLM 锁管理器)  

```sh
firewall-cmd --add-service=high-availability --permanent
firewall-cmd --reload
```

#### (3) 启动服务&修改集群用户密码

- 启动pcsd.service(pcs01, pcs02)

```sh
systemctl start pcsd.service
systemctl enable pcsd.service
```

- 为集群用户hacluster修改密码(pcs01, pcs02)

```sh
echo '123qweQ' | passwd hacluster  --stdin
```

#### (4) 配置corosync&新建集群(任一节点)

##### 在集群节点中为 pcs 守护进程认证：

```sh
pcs cluster auth [node] [...] [-u username] [-p password]
```
- 每个节点中的 pcs 管理员的用户名必须为 hacluster  
- 如果未指定用户名或密码，系统会在执行该命令时提示您为每个节点指定那些参数  
- 如果未指定任何节点，且之前运行过该命令，则这个命令会在所有所有使用 pcs cluster setup 命令指定的节点中认证 pcs  
- 授权令牌保存在 ~/.pcs/tokens 或/ var/lib/pcsd/tokens  

```sh
$ pcs cluster auth node01 node02

Username: hacluster
Password: 
node02: Authorized
node01: Authorized
```

##### 创建集群

```sh
$ pcs cluster setup --name FTPCluster7 node01 node02 

Destroying cluster on nodes: node01, node02...
node01: Stopping Cluster (pacemaker)...
node02: Stopping Cluster (pacemaker)...
node02: Successfully destroyed cluster
node01: Successfully destroyed cluster

Sending 'pacemaker_remote authkey' to 'node01', 'node02'
node01: successful distribution of the file 'pacemaker_remote authkey'
node02: successful distribution of the file 'pacemaker_remote authkey'
Sending cluster config files to the nodes...
node01: Succeeded
node02: Succeeded

Synchronizing pcsd certificates on nodes node01, node02...
node02: Success
node01: Success
Restarting pcsd on the nodes in order to reload the certificates...
node02: Success
node01: Success
```

此时集群服务未启动，手动启动，加入开机自启

```sh
$ pcs status 
Error: cluster is not currently running on this node
```

```sh
$ pcs cluster start --all 
node01: Starting Cluster (corosync)...
node02: Starting Cluster (corosync)...
node02: Starting Cluster (pacemaker)...
node01: Starting Cluster (pacemaker)...

#上面的命令会触发:
# systemctl start corosync.service
# systemctl start pacemaker.service

$ systemctl enable corosync.service
$ systemctl enable pacemaker.servic
```

##### 验证corosync配置

检查corosync通信状态: 

```
$ corosync-cfgtool -s
Printing ring status.
Local node ID 2
RING ID 0
	id	= 10.10.10.242
	status	= ring 0 active with no faults
```

检查成员关系与quorum: 

```
$ corosync-cmapctl  | grep members 
runtime.totem.pg.mrp.srp.members.1.config_version (u64) = 0
runtime.totem.pg.mrp.srp.members.1.ip (str) = r(0) ip(10.10.10.241) 
runtime.totem.pg.mrp.srp.members.1.join_count (u32) = 1
runtime.totem.pg.mrp.srp.members.1.status (str) = joined
runtime.totem.pg.mrp.srp.members.2.config_version (u64) = 0
runtime.totem.pg.mrp.srp.members.2.ip (str) = r(0) ip(10.10.10.242) 
runtime.totem.pg.mrp.srp.members.2.join_count (u32) = 1
runtime.totem.pg.mrp.srp.members.2.status (str) = joined
```

```
$ pcs status corosync

Membership information
----------------------
    Nodeid      Votes Name
         1          1 node01
         2          1 node02 (local)
```

检查pacemaker配置

* pacemaker服务

```
$ ps axf |grep pacemaker
 10172 pts/0    S+     0:00          \_ grep --color=auto pacemaker
  9993 ?        Ss     0:00 /usr/sbin/pacemakerd -f
  9994 ?        Ss     0:00  \_ /usr/libexec/pacemaker/cib
  9995 ?        Ss     0:00  \_ /usr/libexec/pacemaker/stonithd
  9996 ?        Ss     0:00  \_ /usr/libexec/pacemaker/lrmd
  9997 ?        Ss     0:00  \_ /usr/libexec/pacemaker/attrd
  9998 ?        Ss     0:00  \_ /usr/libexec/pacemaker/pengine
  9999 ?        Ss     0:00  \_ /usr/libexec/pacemaker/crmd

$ pcs status
$ pcs cluster cib
```

* 集群基础配置信息检测

```
$ crm_verify -L -V
   error: unpack_resources:	Resource start-up disabled since no STONITH resources have been defined
   error: unpack_resources:	Either configure some or disable STONITH with the stonith-enabled option
   error: unpack_resources:	NOTE: Clusters with shared data need STONITH to ensure data integrity
Errors found during check: config not valid
```

注: STONITH/Fencing默认开启，可以先暂时关闭: 

> By default pacemaker enables STONITH (Shoot The Other Node In The Head ) / Fencing in an order to protect the data. Fencing is mandatory when you use the shared storage to avoid the data corruptions.)

```
$ pcs property set stonith-enabled=false

$ pcs property show stonith-enabled
Cluster Properties:
 stonith-enabled: false
```

#### (5) 集群资源配置

```
$ pcs resource standards
ocf                         # Open cluster Framework
lsb                         # Linux standard base (legacy init scripts)
service                     #  Based on Linux "service" command
systemd                     # systemd based service Management
stonith                     # Fencing Resource standard (本机测试没有改选项，不知道是不是VM的原因)
		
$ pcs resource providers
heartbeat
openstack
pacemaker

# 如查看ocf标准，heartbeat提供的内建类型
# pcs resource agents ocf:heartbeat 
```

##### 添加IP

```sh
pcs resource create ftp02_ip ocf:heartbeat:IPaddr2 ip=1.1.1.242 cidr_netmask=24 nic=team1 op monitor interval=30s
pcs resource create ftp01_ip ocf:heartbeat:IPaddr2 ip=1.1.1.241 cidr_netmask=24 nic=team1 op monitor interval=30s

$ pcs resource show ftp01_ip
 Resource: ftp01_ip (class=ocf provider=heartbeat type=IPaddr2)
  Attributes: cidr_netmask=24 ip=1.1.1.241 nic=team1
  Operations: monitor interval=30s (ftp01_ip-monitor-interval-30s)
              start interval=0s timeout=20s (ftp01_ip-start-interval-0s)
              stop interval=0s timeout=20s (ftp01_ip-stop-interval-0s)
```

##### 添加HA-LVM(通过lvm标签配置)【可选】

若指定群集管理卷组, 需要执行这一步骤: 

```sh
pcs resource create ftp_LVM LVM volgrpname=vg_data01 exclusive=yes
```

上面命令表示: **由集群管理`vg_data01`这个卷组**


配置卷组由集群管理, 可参考以下步骤：

> * 修改配置文件
> 
> ```sh
> $ vim /etc/lvm/lvm.conf
> 
> locking_type = 1
> use_lvmetad = 0
> volume_list = [ "rhel-root" ]  # 除了集群管理的卷组，其他均写进去
> ```
> 
> * 关闭服务
> 
> ```
> systemctl stop lvm2-lvmetad
> systemctl disable lvm2-lvmetad
> 
> #以下命令能达到上面两条命令的作用
> lvmconf --enable-halvm --services --startstopservices
> ```
> 
> * 重建initramfs
> 
> ```
> cp /boot/initramfs-$(uname -r).img /boot/initramfs-$(uname -r).img.$(date +%m-%d-%H%M%S).bak
> dracut -H -f /boot/initramfs-$(uname -r).img $(uname -r)
> ```
> 
> * 重启系统


##### 添加Filesystem

```sh
pcs resource create ftp01_FS Filesystem device='/dev/vg_data01/lv_data01' directory='/data01' fstype='xfs'
pcs resource create ftp02_FS Filesystem device='/dev/vg_data01/lv_data02' directory='/data02' fstype='xfs'
```

##### 添加vsftpd

- 使用vsftpd默认文件，即 `/etc/vsftpd/vsftpd.conf`

```sh
# pcs resource create vsftpd_ftp01 systemd:vsftpd
```

- 使用自定义文件： `/etc/vsftpd/vsftpd_ftp01.conf`, `/etc/vsftpd/vsftpd_ftp02.conf`

```sh
pcs resource create vsftpd_ftp01 systemd:vsftpd@vsftpd_ftp01
pcs resource create vsftpd_ftp02 systemd:vsftpd@vsftpd_ftp02
```

##### 创建资源组

```sh
pcs resource group add GROUP_FTP01 ftp01_ip ftp01_FS vsftpd_ftp01
pcs resource group add GROUP_FTP02 ftp02_ip ftp02_FS vsftpd_ftp02
```

如果要删除其中一个，使用以下命令：

```sh
pcs resource group remove GROUP_FTP01 ftp01_ip
```

##### 添加约束条件

- 列出指定资源的约束条件

```
pcs constraint ref ftp01_ip
```

- 列出当前所有约束条件

```x
pcs constraint list
pcs constraint show
                        --full      # If '--full' is specified also list the constraint ids
```

- 添加`order`类约束

```
order [action] <resource id> then [action] <resource id> [options]
```

例如:

```sh
pcs constraint order start ftp02_ip then vsftpd_ftp02
pcs constraint order start ftp02_FS then vsftpd_ftp02

$ pcs constraint list --full
Location Constraints:
Ordering Constraints:
  start ftp01_ip then start vsftpd_ftp01 (kind:Mandatory) (id:order-ftp01_ip-vsftpd_ftp01-mandatory)
  start ftp01_FS then start vsftpd_ftp01 (kind:Mandatory) (id:order-ftp01_FS-vsftpd_ftp01-mandatory)
  start ftp02_ip then start vsftpd_ftp02 (kind:Mandatory) (id:order-ftp02_ip-vsftpd_ftp02-mandatory)
  start ftp02_FS then start vsftpd_ftp02 (kind:Mandatory) (id:order-ftp02_FS-vsftpd_ftp02-mandatory)
Colocation Constraints:
Ticket Constraints:
```

- 添加`colocation`类约束

```
colocation add [master|slave] <source resource id> with [master|slave] <target resource id> [score] [options] [id=constraint-id]

# Request <source resource> to run on the same node where pacemaker has determined <target resource> should run.
```

例如:

```
pcs constraint colocation add vsftpd_ftp01 ftp01_ip
pcs constraint colocation add vsftpd_ftp01 ftp01_FS

$ pcs constraint colocation show --full
Colocation Constraints:
  vsftpd_ftp01 with ftp01_FS (score:INFINITY) (id:colocation-vsftpd_ftp01-ftp01_FS-INFINITY)
  vsftpd_ftp01 with ftp01_ip (score:INFINITY) (id:colocation-vsftpd_ftp01-ftp01_ip-INFINITY)

```

- 添加`location`类约束

```sh
# Create a location constraint on a resource to prefer the specified node with score (default score: INFINITY).
location <resource> prefers <node>[=<score>] [<node>[=<score>]]...

# Create a location constraint on a resource to avoid the specified node with score (default score: INFINITY).
location <resource> avoids <node>[=<score>] [<node>[=<score>]]...
```

例如:

```sh
pcs constraint location vsftpd_ftp01 prefers node01=200
pcs constraint location vsftpd_ftp01 prefers node02=20

pcs constraint location vsftpd_ftp02 prefers node01=20
pcs constraint location vsftpd_ftp02 prefers node02=200


$ pcs constraint location show --full
Location Constraints:
  Resource: vsftpd_ftp01
    Enabled on: node01 (score:200) (id:location-vsftpd_ftp01-node01-200)
    Enabled on: node02 (score:20) (id:location-vsftpd_ftp01-node02-20)
  Resource: vsftpd_ftp02
    Enabled on: node01 (score:20) (id:location-vsftpd_ftp02-node01-20)
    Enabled on: node02 (score:200) (id:location-vsftpd_ftp02-node02-200)
```

#### (6) fence

> 添加vCenter或Esxi作为fence设备

找到虚拟机信息：  

```
$ fence_vmware_soap -a 192.168.163.252 -z -l administrator@vsphere.local -p 1qaz@WSX4rfv -o list --ssl-insecure

...
node01:422a97b9-5f92-a095-db50-c6a08eccda73
node02:422aa805-fe81-638a-02a5-a1985085f68e
...
```

查看fence_vmware_soap的配置参考：  

```
pcs stonith describe fence_vmware_soap
```

添加fencing：

```sh
pcs stonith create FTP_fence_vmware fence_vmware_soap inet4_only=1 ipport=443 ipaddr="192.168.163.252" login="administrator@vsphere.local" passwd="1qaz@WSX4rfv" ssl_insecure=1 pcmk_host_map="node01:422a97b9-5f92-a095-db50-c6a08eccda73;node02:422aa805-fe81-638a-02a5-a1985085f68e" pcmk_host_list="node01,node02" pcmk_host_check=static-list

# 参考链接:  https://access.redhat.com/solutions/917813
```

ipmi设置fence

```sh
fence_ipmilan -a 10.0.64.115 -P -l USERID -p PASSW0RD –o status    # 输出 Status: ON 表示正常

pcs stonith create ipmi-fence-016 fence_ipmilan pcmk_host_list='cnsz03016' pcmk_host_check='static-list' ipaddr='10.0.64.115' login='USERID' passwd='PASSW0RD' lanplus=1 power_wait=4 pcmk_reboot_action='reboot' op monitor interval=30s
```


可以指定fence的操作，使用`pcmk_reboot_action`，默认指令是reboot，可修改为off（只关机不开机）

上文中将STONITH/Fencing暂时关闭了，需要开启：

```sh
pcs property set stonith-enabled=true
```

```
$ pcs stonith show  --full

 Resource: FTP_fence_vmware (class=stonith type=fence_vmware_soap)
  Attributes: inet4_only=1 ipaddr=192.168.163.252 ipport=443 login=administrator@vsphere.local passwd=1qaz@WSX4rfv pcmk_host_check=static-list pcmk_host_list=node01,node02 pcmk_host_map=node01:422a97b9-5f92-a095-db50-c6a08eccda73;node02:422aa805-fe81-638a-02a5-a1985085f68e ssl_insecure=1
  Operations: monitor interval=60s (FTP_fence_vmware-monitor-interval-60s)


$ pcs property show

Cluster Properties:
 cluster-infrastructure: corosync
 cluster-name: FTPCluster7
 dc-version: 1.1.19-8.el7-c3c624ea3d
 have-watchdog: false
 last-lrm-refresh: 1600345245
 stonith-enabled: true
```


