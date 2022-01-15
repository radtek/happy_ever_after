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


## 3. Cman+rgmanager+vsftpd



| 系统  |主机名  |系统IP              |心跳IP           |存储IP(iSCSI)    |服务               |共享盘    |ftp服务ip|
|  --   | --     |      --            |       --        |     --          |        --         |    --    | --      |
|       |        |                    | bond0           | bond1           | -                 | -        |bond0    |
| REHL6 | node03 | 192.168.163.243/24 | 10.10.10.243/24 | 20.20.20.243/24 | ricci,luci,vsftpd | /dev/sdc |10.10.10.3/24|
| REHL6 | node04 | 192.168.163.244/24 | 10.10.10.244/24 | 20.20.20.243/24 | ricci,vsftpd      | /dev/sdc |10.10.10.4/24|

> 测试了很多次，添加ip时，只能添加与系统已有网卡相同网段的ip，其余网段的ip会添加失败。而且，虽然有prefer_interface配置，即指定网卡，但是实验测试，这项配置无法生效。
> rgmanager会根据给定的ip，自动在相应的网卡上启动，无法自定义



### 3.1 网络配置



bond master配置文件`ifcfg-bond0`：

```
DEVICE=bond0
BOOTPROTO=static
ONBOOT=yes
BONDING_OPTS="mode=1 miimon=100"
IPADDR=10.10.10.244
PREFIX=24
USERCTL=no
TYPE=Ethernet
```

slave配置文件`ifcfg-eth3`:

```
DEVICE=eth3
BOOTPROTO=none
ONBOOT=yes
TYPE=Ethernet
USERCTL=no
MASTER=bond0
SLAVE=yes
```

slave配置文件`ifcfg-eth4`:

```
DEVICE=eth4
BOOTPROTO=none
ONBOOT=yes
TYPE=Ethernet
USERCTL=no
MASTER=bond0
SLAVE=yes
```

### 3.2 系统准备工作 (每个节点均需要执行)



#### 配置NTP Client

注释掉所有已有的server配置行，添加以下配置

```x
$ vim /etc/ntp.conf

#server 0.rhel.pool.ntp.org iburst
#server 1.rhel.pool.ntp.org iburst
#server 2.rhel.pool.ntp.org iburst
#server 3.rhel.pool.ntp.org iburst
service 192.168.163.240 iburst
fudge 127.127.1.0 stratum 1
```

```sh
service ntpd restart 
chkconfig ntpd on
```

```
$ ntpq -p 
     remote           refid      st t when poll reach   delay   offset  jitter
==============================================================================
*192.168.163.240 .LOCL.           1 u  194 1024  377    0.425   -0.010   0.019
```

#### 配置解析记录

```sh
$ vi /etc/hosts

10.10.10.243 node03
10.10.10.244 node04
```

#### 配置iSCSI Inititor

- 安装

```
yum install iscsi-initiator-utils.x86_64 -y
```

- 修改InititorName (`/etc/iscsi/initiatorname.iscsi`)，与Target端配置一致:

&emsp;&emsp;node03: `InitiatorName=iqn.2019-12.com.test:targer02node03`  
&emsp;&emsp;node04: `InitiatorName=iqn.2019-12.com.test:targer02node04`  

- 发现iSCSI目标

```
$ iscsiadm --mode discoverydb --type sendtargets --portal 20.20.20.240 --discover

20.20.20.240:3260,1 iqn.2019-12.com.test:targer01
20.20.20.240:3260,1 iqn.2019-12.com.test:targer02
```

- 登录

```
$ iscsiadm --mode node --targetname iqn.2019-12.com.test:targer02 --portal 20.20.20.240:3260 --login

Logging in to [iface: default, target: iqn.2019-12.com.test:targer02, portal: 20.20.20.240,3260] (multiple)
Login to [iface: default, target: iqn.2019-12.com.test:targer02, portal: 20.20.20.240,3260] successful.
```

> 以上三步可参考 `iscsiadm man`文档的 `EXAMPLE` 部分获取帮助

- 各个节点均发现磁盘(sdb)，表明配置正常：

```
$ lsblk
NAME                          MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
loop0                           7:0    0  3.6G  0 loop /root/yum_mount
sr0                            11:0    1 1024M  0 rom  
sda                             8:0    0   16G  0 disk 
├─sda1                          8:1    0  500M  0 part /boot
└─sda2                          8:2    0 15.5G  0 part 
  ├─vg_temp610-lv_root (dm-0) 253:0    0 13.9G  0 lvm  /
  └─vg_temp610-lv_swap (dm-1) 253:1    0  1.6G  0 lvm  [SWAP]
sdb                             8:16   0   10G  0 disk
```

#### 配置共享磁盘

通过lvm命令创建ext4文件系统，不做赘述


#### HA-LVM



CLVM和HA-LVM：  

- 集群中一个以上的节点要求访问在活动节点间共享的存储，就必须使用 CLVM  
- 如果应用程序以最佳的 active/passive（故障切换）配置运行，那么一次只有一个访问该存储的单一节点是活动的，就可以使用高可用逻辑卷管理代理（HA-LVM）  

HA-LVM设置：  

- 首选方法是使用 CLVM，但它只能激活唯一的逻辑卷。好处是可轻松设置并有效防止管理失误 （比如删除正在使用的逻辑卷）。要使用 CLVM，则必须运行高可用性附加组件软件和弹性存储附加组件软件，包括 clvmd。  
- 第二种方法使用本地机器锁定和 LVM“标签”。这个方法的优点是不需要任何 LVM 集群软件包， 但设置步骤比较复杂，且无法防止管理员意外从不活动的集群中删除逻辑卷。  



##### CONFIGURING HA-LVM FAILOVER WITH CLVM (PREFERRED)

- 将`locking_type`值修改为3  
- 添加集群资源，如`<lvm name="lvm" vg_name="shared_vg" lv_name="ha-lv"/>`

##### CONFIGURING HA-LVM FAILOVER WITH TAGGING

- 将`locking_type`值修改为：**1**  
- 将`use_lvmetad`值修改为：**0**  
- 将`volume_list`值修改为：`volume_list = [ "VolGroup00" ]`，只将本机的卷组加进中括号，集群管理的卷组不添加进去。  
- Update the initramfs device:  
    * `cp /boot/initramfs-$(uname -r).img /boot/initramfs-$(uname -r).img.$(date +%m-%d-%H%M%S).bak`
    * `dracut -H -f /boot/initramfs-$(uname -r).img $(uname -r)`


#### 配置vsftpd服务


```sh
mkdir /data03
mkdir /data04
yum -y install vsftpd
useradd -s /sbin/nologin vsftpd
```

> ftp03禁用主动模式，启动被动模式，端口限制在2222-2225


```sh
$ vim /etc/vsftpd/vsftpd_ftp03.conf

anonymous_enable=NO
guest_enable=NO
local_enable=YES
write_enable=YES
local_umask=022
port_enable=NO
pasv_enable=YES
pasv_min_port=2222
pasv_max_port=2225
dirmessage_enable=YES
ftpd_banner=Welcome to blah FTP service
xferlog_enable=YES
xferlog_std_format=YES
xferlog_file=/var/log/ftp03_xferlog
dual_log_enable=YES
vsftpd_log_file=/var/log/ftp03_vsftpd.log
nopriv_user=vsftpd
connect_from_port_20=YES
chroot_local_user=NO
chroot_list_enable=YES
chroot_list_file=/etc/vsftpd/chroot_list03
listen=YES
listen_ipv6=NO
listen_address=10.10.10.4
pam_service_name=vsftpd
userlist_enable=YES
userlist_deny=NO
tcp_wrappers=YES
local_root=/data03
use_localtime=YES
#allow_writeable_chroot=YES
```

```
-A INPUT -p tcp -m state --state NEW -m tcp --dport 21 -j ACCEPT
-A INPUT -p tcp --dport 2222:2225 -j ACCEPT
```


> ftp04禁用主动模式，启动被动模式，端口限制在2226-2229

```sh
$ vim /etc/vsftpd/vsftpd_ftp04.conf

anonymous_enable=NO
guest_enable=NO
local_enable=YES
write_enable=YES
local_umask=022
port_enable=NO
pasv_enable=YES
pasv_min_port=2226
pasv_max_port=2229
dirmessage_enable=YES
ftpd_banner=Welcome to blah FTP service
xferlog_enable=YES
xferlog_std_format=YES
xferlog_file=/var/log/ftp04_xferlog
dual_log_enable=YES
vsftpd_log_file=/var/log/ftp04_vsftpd.log
nopriv_user=vsftpd
connect_from_port_20=YES
chroot_local_user=NO
chroot_list_enable=YES
chroot_list_file=/etc/vsftpd/chroot_list04
listen=YES
listen_ipv6=NO
listen_address=10.10.10.4
pam_service_name=vsftpd
userlist_enable=YES
userlist_deny=NO
tcp_wrappers=YES
local_root=/data04
use_localtime=YES
#allow_writeable_chroot=YES
```

```
-A INPUT -p tcp -m state --state NEW -m tcp --dport 21 -j ACCEPT
-A INPUT -p tcp --dport 2226:2229 -j ACCEPT
```



### 3.3 HA配置



#### 3.3.1 安装

```sh
yum groupinstall -y 'High Availability'
yum install -y luci				# 若要使用luci(conga用户界面)，需要安装此包(按需安装，不要求每个节点都安装)
yum install -y lvm2-cluster		# 若使用clvm，则需要安装此包(每个节点都需要)
```

#### 3.3.2 配置防火墙

- 附加组件的端口

|IP端口号|协议|组件|
|--|--|--|
|`5404`,`5405`| UDP | corosync/cman(集群管理器)|
|`11111`| TCP |	ricci|
|`21064`| TCP |	dlm|
|`16851`| TCP |	modclusterd|

- 客户端访问luci(conga用户界面)的端口：

|IP端口号|协议|组件|
|--|--|--|
|`8084`|TCP|luci(conga用户接口服务器)|

若要修改luci的端口，可按以下方法：

```
$ vi /etc/sysconfig/luci
port = 8084

$ service luci restart 
```

防火墙配置如下：

```
$ vim /etc/sysconfig/iptables


-A INPUT -m state --state NEW -p udp -s 10.10.10.244 -d 10.10.10.243 -m multiport --dports 5404,5405 -j ACCEPT
-A INPUT -m addrtype --dst-type MULTICAST -m state --state NEW -p udp -m multiport -s 10.10.10.0/24 --dports 5404,5405 -j ACCEPT
-A INPUT -m state --state NEW -p tcp -s 10.10.10.244 -d 10.10.10.243 -m multiport --dports 11111,21064,16851 -j ACCEPT
-A INPUT -m state --state NEW -p tcp -s 192.168.2.0/24 -d 192.168.163.243 --dport 8084 -j ACCEPT
-A INPUT -p igmp -j ACCEPT  # For igmp (Internet Group Management Protocol)

-A INPUT -m state --state NEW -p udp -s 10.10.10.243 -d 10.10.10.244 -m multiport --dports 5404,5405 -j ACCEPT
-A INPUT -m addrtype --dst-type MULTICAST -m state --state NEW -p udp -m multiport -s 10.10.10.0/24 --dports 5404,5405 -j ACCEPT
-A INPUT -m state --state NEW -p tcp -s 10.10.10.243 -d 10.10.10.244 -m multiport --dports 11111,21064,16851 -j ACCEPT
-A INPUT -m state --state NEW -p tcp -s 192.168.2.0/24 -d 192.168.163.244 --dport 8084 -j ACCEPT
-A INPUT -p igmp -j ACCEPT  # For igmp (Internet Group Management Protocol)
```

#### 3.3.3 禁用ACPI



> If your cluster uses integrated fence devices, you must configure ACPI (Advanced Configuration and Power Interface) to ensure immediate and complete fencing.

为了fence正常使用，需要关闭ACPI，共有以下三种方法实现

- 使用 chkconfig 管理禁用 ACPI 软关闭


```
chkconfig --del acpid  				#删除acpid
chkconfig --level 2345 acpid off 	#关闭
```

- 使用 BIOS 禁用 ACPI 软关闭


若chkconfig关闭无效，可以在BIOS中设置：

BIOS CMOS Setup Utility：将`Soft-Off by PWR-BTTN`设定为`Instant-Off`

- 在 grub.conf (`/boot/grub/grub.conf`)文件中完全禁用 ACPI

```
kernel /vmlinuz-2.6.32-358.el6.x86_64 ro root=/dev/…………rhgb quiet  acpi=off
```

#### 3.3.4 准备仲裁盘



> 使用qdisk的集群，fence设备推荐配置power fencing：  
>> To ensure reliable fencing when using qdiskd, use power fencing. While other types of fencing can be reliable for clusters not configured with qdiskd, they are not reliable for a cluster configured with qdiskd.  

- 创建100M盘

```sh
dd if=/dev/zero of=/root/qdisk_100M.img bs=1M count=100
```

- 通过 target 共享给node03、node04

```sh
targetcli /backstores/fileio create qdisk_for_0304 /root/qdisk_100M.img
targetcli /iscsi/iqn.2019-12.com.test:targer02/tpg1/luns create /backstores/fileio/qdisk_for_0304
```

- 创建仲裁盘

```x
$ mkqdisk -c /dev/sdc -l cluster_qdisk
mkqdisk v3.0.12.1

Writing new quorum disk label 'cluster_qdisk' to /dev/sdc.
WARNING: About to destroy all data on /dev/sdc; proceed [N/y] ? y
Initializing status block for node 1...
Initializing status block for node 2...
Initializing status block for node 3...
Initializing status block for node 4...
Initializing status block for node 5...
Initializing status block for node 6...
Initializing status block for node 7...
Initializing status block for node 8...
Initializing status block for node 9...
Initializing status block for node 10...
Initializing status block for node 11...
Initializing status block for node 12...
Initializing status block for node 13...
Initializing status block for node 14...
Initializing status block for node 15...
Initializing status block for node 16...
```

```x
$ mkqdisk -L
mkqdisk v3.0.12.1

/dev/block/8:32:
/dev/disk/by-id/scsi-3600140527992a8ab38e4fbfa2fffc8d8:
/dev/disk/by-id/wwn-0x600140527992a8ab38e4fbfa2fffc8d8:
/dev/disk/by-path/ip-20.20.20.240:3260-iscsi-iqn.2019-12.com.test:targer02-lun-1:
/dev/sdc:
	Magic:                eb7a62c2
	Label:                cluster_qdisk
	Created:              Sat Sep 19 21:38:48 2020
	Host:                 node03
	Kernel Sector Size:   512
	Recorded Sector Size: 512
```


#### 3.3.5 启动服务&修改集群用户密码



- 设置ricci密码

```sh
chkconfig ricci on
service ricci start
echo '123qweQ' | passwd --stdin ricci
```

#### 3.3.6 创建集群



实际上是创建一个配置文件`/etc/cluster/cluster.conf`

```sh
ccs -h node03 --createcluster FTPCluster6
```

若要编辑/查看配置文件`/etc/cluster/cluster.conf`, 或者手动指定文件：

```x
ccs -h host [options]
ccs -f file [options]
ccs -h host -f file --setconf   # 将主机上配置文件改名cluster.conf，并发送至集群的其他host上(/etc/cluster/下)
ccs -h host --getconf           # 查看指定主机上的配置文件
```


#### 3.3.7 添加节点



```x
ccs -h node03 --addnode node03
ccs -h node03 --addnode node04

# 可以指定节点的nodeid和投票权(the number of votes)
## ccs -h host --addnode host --nodeid nodeid
## ccs -h host --addnode host --votes votes

# 若要删除节点
## ccs -h host --rmnode node
```

```
$ ccs -h node03 --getconf

<cluster config_version="3" name="FTPCluster6">  
  <fence_daemon/>  
  <clusternodes>    
    <clusternode name="node03" nodeid="1"/>    
    <clusternode name="node04" nodeid="2"/>    
  </clusternodes>  
  <cman/>  
  <fencedevices/>  
  <rm>    
    <failoverdomains/>    
    <resources/>    
  </rm>  
</cluster>
```

#### 3.3.8 添加fence设备



> When using SELinux with the High Availability Add-On in a VM environment, you should ensure that the SELinux boolean `fenced_can_network_connect` is persistently set to on. This allows the `fence_xvm` fencing agent to work properly, enabling the system to fence virtual machines.

##### 关于`post_fail_delay`,`post_join_delay`两个参数

- `post_fail_delay`:the number of seconds the fence daemon ( fenced) waits before fencing a node (a member of the fence domain) after the node has failed(default 0)  
- `post_join_delay`: the number of seconds the fence daemon ( fenced) waits before fencing a node after the node joins the fence domain. The post_join_delay default value is 6. A typical setting for post_join_delay is between 20 and 30 seconds, but can vary according to cluster and network performance.

这两个参数需要同时设置，如果只单独设置一个，另一个会重置为默认值  

```
ccs -h node03 --setfencedaemon post_fail_delay=5 post_join_delay=25
```

##### 查找虚拟机UUID

如果是利用vc配置fence，需要找到虚拟机的UUID：

```sh
$ fence_vmware_soap -a 192.168.163.252 -z -l administrator@vsphere.local -p 1qaz@WSX4rfv -o list
...
node03,422ad512-3ce5-c046-0046-9516094be718
node04,422ac3f0-e2f9-31a7-1816-7980e4757b80
...
```

##### 查找支持的fence agent

```x
ccs -h host --lsfenceopts                   # 列出所有支持的fence agent
ccs -h host --lsfenceopts fence_vmware_soap # 具体某一项fence agent的参数
```

##### 使用vCenter作为fence设备

设备名： `fence_vmware_soap`

```
$ ccs -h node03 --addfencedev VC_Fence agent=fence_vmware_soap ipaddr=192.168.163.252 login=administrator@vsphere.local passwd=1qaz@WSX4rfv
```

##### 添加fence method和instance

```x
ccs -h node03 --addmethod APC node03
ccs -h node03 --addmethod APC node04

ccs -h node03 --addfenceinst VC_Fence node03 APC port=node03 ssl=on uuid=422ad512-3ce5-c046-0046-9516094be718
ccs -h node03 --addfenceinst VC_Fence node04 APC port=node04 ssl=on uuid=422ac3f0-e2f9-31a7-1816-7980e4757b80
```

若要删除method或instance

```x
ccs -h <host> --rmmethod <method> <node>
ccs -h <host> --rmfenceinst --rmfenceinst <fence device name> <node> <method>
```

##### 检查

fence设备配置并启动以后，可用一下命令测试：

```
$ fence_check

fence_check run at Wed Oct 14 14:49:47 CST 2020 pid: 19117
Testing node03 method 1: success
Testing node04 method 1: success

$ fence_node node01
$ fence_node -vv node01
$ ipmitool -I lanplus -H x.x.x.x -U root -P 'Yth@canway2019' -v chassis power status
```

#### 3.3.9 failover domain

以下参数，若不指定，默认值为**加粗**的那个：

- **unrestricted**/restricted  
    Services can run only on nodes specified  
- **unordered**/ordered  
    Order the nodes to which services failover.   
- **failback**/nofailback  
    Do not send service back to first priority node when it becomes available again.   

命令格式：  

```
ccs -h host --addfailoverdomain name [restricted] [ordered] [nofailback]
```

```
ccs -h node03 --addfailoverdomain ftp03_fd ordered 
ccs -h node03 --addfailoverdomain ftp04_fd ordered 

ccs -h node03 --addfailoverdomainnode ftp03_fd node03 1 
ccs -h node03 --addfailoverdomainnode ftp03_fd node04 2 
ccs -h node03 --addfailoverdomainnode ftp04_fd node04 1
ccs -h node03 --addfailoverdomainnode ftp04_fd node03 2
```

```
$ ccs -h node03 --lsfailoverdomain 

ftp03_fd: restricted=0, ordered=1, nofailback=0
  node03: priority=1
  node04: priority=2
ftp04_fd: restricted=0, ordered=1, nofailback=0
  node04: priority=1
  node03: priority=2
```

#### 3.3.10 添加quorum

```
ccs -h node03 --setquorumd label=cluster_qdisk
ccs -h node03 --addheuristic program="/bin/ping -c1 -t2 192.168.163.1" interval=2 score=1 tko=2

$ ccs -h node03 --lsquorum 
Quorumd: label=cluster_qdisk
  heuristic: program=/bin/ping -c1 -t2 192.168.163.1, interval=2, score=1, tko=2
```

- quorum disk options

Parameter | Description 
-- | --
`interval` | The frequency of read/write cycles, in seconds. 
`votes` | The number of votes the quorum daemon advertises to cman when it has a high enough score. 
`tko` | The number of cycles a node must miss to be declared dead. 
`min_score` | The minimum score for a node to be considered "alive". <br>If omitted or set to 0, the default function, ***floor((n+1)/2)***, is used, where *n* is the sum of the heuristics scores. <br>The **Minimum Score** value must never exceed the sum of the heuristic scores; otherwise, the quorum disk cannot be available. 
`device` | The storage device the quorum daemon uses. The device must be the same on all nodes. 
`label` | Specifies the quorum disk label created by the mkqdisk utility. <br>If this field contains an entry, the label overrides the Device field. <br>If this field is used, the quorum daemon reads `/proc/partitions` and checks for qdisk signatures on every block device found, comparing the label against the specified label. <br>This is useful in configurations where the quorum device name differs among nodes.

- quorum disk heuristic

Parameter | Description 
--|--
`program` | The path to the program used to determine if this heuristic is available. <br>This can be anything that can be executed by /bin/sh -c. A return value of 0 indicates success; anything else indicates failure. <br>This parameter is required to use a quorum disk.   
`interval` | The frequency (in seconds) at which the heuristic is polled. The default interval for every heuristic is 2 seconds.   
`score` | The weight of this heuristic. Be careful when determining scores for heuristics. The default score for each heuristic is 1.   
`tko` | The number of consecutive failures required before this heuristic is declared unavailable.  

#### 3.3.11 添加resource



```
ccs -h node03 --lsservices          # 列出所有已经配置的resource和service
ccs -h node03 --lsresourceopt       # 列出所有支持的resource
ccs -h node03 --lsresourceopt ip    # 列出指定resource的配置选项

ccs -h host --addresource resourcetype [resource options]   # 添加
ccs -h host --rmresource resourcetype [resource options]    # 删除
```

##### IP

```
ccs -h node03 --addresource ip address="10.10.10.3/24" family=ipv4 monitor_link=1 sleeptime=10 prefer_interface=bond0
ccs -h node03 --addresource ip address="10.10.10.4/24" family=ipv4 monitor_link=1 sleeptime=10 prefer_interface=bond0
```

##### Filesystem

```
mkfs.ext4 /etc/mapper/vg_data02-lv_data03
mkfs.ext4 /etc/mapper/vg_data02-lv_data04
```

```
ccs -h node03 --addresource fs name=fs_ftp03 mountpoint="/data03" device="/dev/mapper/vg_data02-lv_data03" fstype="ext4"
ccs -h node03 --addresource fs name=fs_ftp04 mountpoint="/data04" device="/dev/mapper/vg_data02-lv_data04" fstype="ext4"
```

##### vsftpd

```
cp /etc/init.d/vsftpd /etc/init.d/vsftpd_ftp03
cp /etc/init.d/vsftpd /etc/init.d/vsftpd_ftp04
```

将`/etc/init.d/vsftpd_ftp03`和`/etc/init.d/vsftpd_ftp04`中的

```
CONFS=`ls /etc/vsftpd/*.conf 2>/dev/null`
```

分别替换为：

```
CONFS=`ls /etc/vsftpd/vsftpd_ftp03.conf 2>/dev/null`
CONFS=`ls /etc/vsftpd/vsftpd_ftp04.conf 2>/dev/null`
```

添加服务：

```
ccs -h node03 --addresource script name="vsftpd_ftp03" file="/etc/init.d/vsftpd_ftp03"
ccs -h node03 --addresource script name="vsftpd_ftp04" file="/etc/init.d/vsftpd_ftp04"
```

```
$ ccs -h node03 --lsservices

resources: 
  ip: monitor_link=1, sleeptime=10, prefer_interface=bond0, family=ipv4, address=10.10.10.3/24
  ip: monitor_link=1, sleeptime=10, prefer_interface=bond0, family=ipv4, address=10.10.10.4/24
  fs: name=fs_ftp03, device=/dev/mapper/vg_data02-lv_data03, mountpoint=/data03, fstype=ext4
  fs: name=fs_ftp04, device=/dev/mapper/vg_data02-lv_data04, mountpoint=/data04, fstype=ext4
  script: name=vsftpd_ftp03, file=/etc/init.d/vsftpd_ftp03
  script: name=vsftpd_ftp04, file=/etc/init.d/vsftpd_ftp04
```

#### 3.3.12 添加service



```
ccs -h host --addservice servicename [service options]
```

```
ccs -h node03 --addservice "GROUP_FTP03" domain="ftp03_fd" autostart="1" recovery="relocate" 
ccs -h node03 --addservice "GROUP_FTP04" domain="ftp04_fd" autostart="1" recovery="relocate" 

ccs -h node03 --addsubservice "GROUP_FTP03" ip ref="10.10.10.3/24"
ccs -h node03 --addsubservice "GROUP_FTP03" fs ref="fs_ftp03"
ccs -h node03 --addsubservice "GROUP_FTP03" script ref="vsftpd_ftp03"

ccs -h node03 --addsubservice "GROUP_FTP04" ip ref="10.10.10.4/24"
ccs -h node03 --addsubservice "GROUP_FTP04" fs ref="fs_ftp04"
ccs -h node03 --addsubservice "GROUP_FTP04" script ref="vsftpd_ftp04"
```

#### 3.3.13 群集其他配置



```
$ ccs -h node03 --lsmisc

Resource Manager: 
CMAN: 
Fence Daemon: post_join_delay=25, post_fail_delay=5
```

##### Cluster Configuration Version

```
ccs -h host --getversion
ccs -h host --setversion n
ccs -h host --incversion    # 集群配置文件中将当前配置版本值增加1
```

##### Multicast Configuration

```
ccs -h host --setmulticast multicastaddress     # 自定义多播地址
ccs -h host --setmulticast                      # 恢复默认
```

##### Configuring a Two-Node Cluster

如果要配置两节点群集，则可以执行以下命令以允许单节点维护仲裁

```x
ccs -h host --setcman two_node=1 expected_votes=1

# 此命令会将--setcman选项设置的所有其他属性重置为其默认值
# ccs --setcman命令添加、删除或修改two_node选项时，必须重新启动集群才能使此更改生效

ccs -h node03 --stopall
ccs -h node03 --startall [--noenable|--nodisable] # if --noenable or --nodisable is specified cluster services will only be started
```

##### 配置服务先后顺序(父子服务)

The following rules apply to parent/child relationships in a resource tree: 

- Parents are started before children.   
- Children must all stop cleanly before a parent may be stopped.   
- For a resource to be considered in good health, all its children must be in good health.

将之前配置的修改如下：

```
ccs -h node03 --addservice "GROUP_FTP03" domain="ftp03_fd" autostart="1" recovery="relocate" 
ccs -h node03 --addservice "GROUP_FTP04" domain="ftp04_fd" autostart="1" recovery="relocate" 

ccs -h node03 --addsubservice "GROUP_FTP03" ip address="10.10.10.3/24" family=ipv4 monitor_link=1 sleeptime=10 prefer_interface=bond0
ccs -h node03 --addsubservice "GROUP_FTP03" ip:fs name="fs_ftp03" mountpoint="/data03" device="/dev/mapper/vg_data02-lv_data03" fstype="ext4"
ccs -h node03 --addsubservice "GROUP_FTP03" ip:fs:script name="vsftpd_ftp03" file="/etc/init.d/vsftpd_ftp03"

ccs -h node03 --addsubservice "GROUP_FTP04" ip address="10.10.10.4/24" family=ipv4 monitor_link=1 sleeptime=10 prefer_interface=bond0
ccs -h node03 --addsubservice "GROUP_FTP04" ip:fs name="fs_ftp04" mountpoint="/data04" device="/dev/mapper/vg_data02-lv_data04" fstype="ext4"
ccs -h node03 --addsubservice "GROUP_FTP04" ip:fs:script name="vsftpd_ftp04" file="/etc/init.d/vsftpd_ftp04"
```

```html
$ ccs -h node03 --getconf

<cluster config_version="95" name="FTPCluster6">  
  <fence_daemon post_fail_delay="5" post_join_delay="25"/>  
  <clusternodes>    
    <clusternode name="node03" nodeid="1">      
      <fence>        
        <method name="APC">          
          <device name="VC_Fence" port="node03" ssl="on" uuid="422ad512-3ce5-c046-0046-9516094be718"/>          
        </method>        
      </fence>      
    </clusternode>    
    <clusternode name="node04" nodeid="2">      
      <fence>        
        <method name="APC">          
          <device name="VC_Fence" port="node04" ssl="on" uuid="422ac3f0-e2f9-31a7-1816-7980e4757b80"/>          
        </method>        
      </fence>      
    </clusternode>    
  </clusternodes>  
  <cman expected_votes="1" two_node="1"/>  
  <fencedevices>    
    <fencedevice agent="fence_vmware_soap" ipaddr="192.168.163.252" login="administrator@vsphere.local" name="VC_Fence" passwd="1qaz@WSX4rfv"/>    
  </fencedevices>  
  <rm>    
    <failoverdomains>      
      <failoverdomain name="ftp03_fd" nofailback="0" ordered="1" restricted="0">        
        <failoverdomainnode name="node03" priority="1"/>        
        <failoverdomainnode name="node04" priority="2"/>        
      </failoverdomain>      
      <failoverdomain name="ftp04_fd" nofailback="0" ordered="1" restricted="0">        
        <failoverdomainnode name="node04" priority="1"/>        
        <failoverdomainnode name="node03" priority="2"/>        
      </failoverdomain>      
    </failoverdomains>    
    <resources/>    
    <service autostart="1" domain="ftp03_fd" name="GROUP_FTP03" recovery="relocate">      
      <ip address="10.10.10.3/24" family="ipv4" monitor_link="1" prefer_interface="bond0" sleeptime="10">        
        <fs device="/dev/mapper/vg_data02-lv_data03" fstype="ext4" mountpoint="/data03" name="fs_ftp03">          
          <script file="/etc/init.d/vsftpd_ftp03" name="vsftpd_ftp03"/>          
        </fs>        
      </ip>      
    </service>    
    <service autostart="1" domain="ftp04_fd" name="GROUP_FTP04" recovery="relocate">      
      <ip address="10.10.10.4/24" family="ipv4" monitor_link="1" prefer_interface="bond0" sleeptime="10">        
        <fs device="/dev/mapper/vg_data02-lv_data04" fstype="ext4" mountpoint="/data04" name="fs_ftp04">          
          <script file="/etc/init.d/vsftpd_ftp04" name="vsftpd_ftp04"/>          
        </fs>        
      </ip>      
    </service>    
  </rm>  
  <quorumd label="cluster_qdisk">    
    <heuristic interval="2" program="/bin/ping -c1 -t2 192.168.163.1" score="1" tko="2"/>    
  </quorumd>  
</cluster>

```

#### 3.3.14 同步配置到每个节点



此时集群的基本配置已经完成，需要将配置同步到每个节点上，使用一下命令： 

```sh
rg_test test /etc/cluster/cluster.conf  # 检查配置文件
ccs -h node03 --sync
ccs -h node03 --checkconf 
```

ccs_config_dump — Cluster Configuration Dump Tool

#### 3.3.15 启动



```
service cman start
service rgmanager start 

clusvcadm -e GROUP_FTP03
clusvcadm -e GROUP_FTP04
```

```
chkconfig cman on
chkconfig rgmanager on
chkconfig clvmd on  
# 服务器重启以后，会识别不到共享盘上的vg，启动clvmd即可激活卷组
# 也可以通过clvmd配置HA-LVM，参考上文
```




## ccs



```x
Usage: ccs [OPTION]...
Cluster configuration system.

      --help            Display this help and exit
  -h, --host host       Cluster node to perform actions on
      --usealt          If primary node name is unavailable, attempt to
                        connect to ricci on the alt interface (only works from
                        a cluster member)
  -f, --file file       File to perform actions on
  -i, --ignore          Ignore validation errors in cluster.conf file
  -p, --password        Ricci user password for node running ricci
      --getconf         Print current cluster.conf file
      --setconf         Use the file specified by '-f' to send to the host
                        specified with '-h'
      --checkconf       If file is specified, verify that all the nodes in the
                        file have the same cluster.conf as the file.  If a
                        host is specified then verify that all nodes in the
                        host's cluster.conf file have the identical
                        cluster.conf file
                        same cluster.conf
      --getschema       Print current cluster schema file (if using -h use
                        schema from network, if using -f use local schema)
      --sync [--activate]
                        Sync config file to all nodes and optionally activating
                        that configuration on all nodes
  -b, --backup          Backup cluster.conf file before changes in
                        ~/.ccs/backup directory
  -d, --debug           Display debugging information to help troubleshoot
                        connection issues with ricci
      --exp tag [location] [options]
                        Expert mode to add elements not currently defined in
                        ccs (see man page for more information)
      --exprm location
                        Expert mode to remove elements not currently defined in
                        ccs (see man page for more information)

Cluster Operations:
      --createcluster <cluster>
                        Create a new cluster.conf (removing old one if it
                                                   exists)
      --getversion      Get the current cluster.conf version
      --setversion <n>  Set the cluster.conf version
      --incversion      Increment the cluster.conf version by 1
      --startall [--noenable|--nodisable]
                        Start *AND* enable cluster services on reboot
                        for all nodes (if --noenable or --nodisable is
                        specified cluster services will only be started)
      --stopall [--noenable|--nodisable]
                        Stop *AND* disable cluster services on reboot
                        for all nodes (if --noenable or --nodisable is
                        specified cluster services will only be stopped)
      --start [--noenable|--nodisable]
                        Start *AND* enable cluster services on reboot for
                        host specified with -h or localhost if no host is
                        provided (if --noenable or --nodisable is specified
                        cluster services will only be started)
      --stop [--noenable|--nodisable]
                        Stop *AND* disable cluster services on reboot for
                        host specified with -h or localhost if no host is
                        provided (if --noenable or --nodisable is specified
                        cluster services will only be stopped)

Node Operations:
      --lsnodes         List all nodes in the cluster
      --addnode <node>  Add node <node> to the cluster
      --rmnode <node>
                        Remove a node from the cluster
      --nodeid <nodeid> Specify nodeid when adding a node
      --votes <votes>   Specify number of votes when adding a node
      --addalt <node name> <alt name> [alt options]
                        Add an altname to a node for RRP
      --rmalt <node name>
                        Remove an altname from a node for RRP

Fencing Operations:
      --lsfenceopts [fence type]
                        List available fence devices.  If a fence type is
                        specified, then list options for the specified
                        fence type
      --lsfencedev      List all of the fence devices configured
      --lsfenceinst [<node>]
                        List all of the fence methods and instances on the
                        specified node or all nodes if no node is specified
      --addmethod <method> <node>
                        Add a fence method to a specific node
      --rmmethod <method> <node>
                        Remove a fence method from a specific node
      --addfencedev <device name> [fence device options]
                        Add fence device. Fence devices and parameters can be
                        found in online documentation in 'Fence Device
                        Parameters'
      --rmfencedev <fence device name>
                        Remove fence device
      --addfenceinst <fence device name> <node> <method> [options] [--nounfence]
                        Add fence instance. Fence instance parameters can be
                        found in online documentation in 'Fence Device
                        Parameters'. Using --nounfence prevents ccs from automatically
                        including an unfencing section for agents that require
                        unfencing (ie. fence_scsi, fence_sanlock, etc.)
      --rmfenceinst <fence device name> <node> <method>
                        Remove all instances of the fence device listed from
                        the given method and node
      --addunfenceinst <fence device name> <node> [options]
                        Add an unfence instance
      --rmunfenceinst <fence device name> <node>
                        Remove all instances of the fence device listed from
                        the unfence section of the node

Failover Domain Operations:
      --lsfailoverdomain
                        Lists all of the failover domains and failover domain
                        nodes configured in the cluster
      --addfailoverdomain <name> [restricted] [ordered] [nofailback]
                        Add failover domain
      --rmfailoverdomain <name>
                        Remove failover domain
      --addfailoverdomainnode <failover domain> <node> [priority]
                        Add node to given failover domain
      --rmfailoverdomainnode <failover domain> <node>
                        Remove node from failover domain

Service Operations:
      --lsserviceopts [service type]
                        List available services.  If a service type is
                        specified, then list options for the specified
                        service type
      --lsresourceopts [service type]
                        An alias to --lsserviceopts
      --lsservices      List currently configured services and resources in
                        the cluster
      --addresource <resource type> [resource options] ...
                        Add global cluster resources to the cluster
                        Resource types and variables can be found in the
                        online documentation under 'HA Resource Parameters'
      --rmresource <resource type> [resource options]
                        Remove specified resource with resource options
      --addservice <servicename> [service options] ...
                        Add service to cluster
      --rmservice <servicename>
                        Removes a service and all of its subservices
      --addaction <resource/name> <action_name> <action_option=val>
                        Add an action to the specified resource.
      --rmaction <resource name> [<action_name> [action options]]
                        Remove all actions from resource, or actions matching
                        action name and options specified
      --addvm <virtual machine name> [vm options] ...
                        Add a virtual machine to the cluster
      --rmvm <virtual machine name>
                        Removes named virtual machine from the cluster
      --addsubservice <servicename> <subservice> [service options] ...
                        Add individual subservices, if adding child services,
                        use ':' to separate parent and child subservices
                        and brackets to identify subservices of the same type

                        Subservice types and variables can be found in the
                        online documentation in 'HA Resource Parameters'

                        To add a nfsclient subservice as a child of the 2nd
                        nfsclient subservice in the 'service_a' service use
                        the following example: --addsubservice service_a \
                                               nfsclient[1]:nfsclient \
                                               ref=/test
      --rmsubservice <servicename> <subservice>
                        Removes a specific subservice specified by the
                        subservice, using ':' to separate elements and
                        brackets to identify between subservices of the
                        same type.
                        To remove the 1st nfsclient child subservice
                        of the 2nd nfsclient subservice in the 'service_a'
                        service, use the following example:
                                            --rmsubservice service_a \
                                            nfsclient[1]:nfsclient

Quorum Operations:
      --lsquorum        List quorum options and heuristics
      --setquorumd [quorumd options] ...
                        Add quorumd options
      --addheuristic [heuristic options] ...
                        Add heuristics to quorumd
      --rmheuristic [heuristic options] ...
                        Remove heuristic specified by heurstic options

Misc Options
      --lsmisc          List all of the misc options
      --settotem [totem options]
                        Set totem options
      --setuidgid uid=<uid> gid=<gid>
                        Set uidgid options
      --rmuidgid uid=<uid> gid=<gid>
                        Remove uidgid entry matching specified uid/gid
      --setdlm [dlm options]
                        Set dlm options
      --setrm [resource manager options]
                        Set resource manager options
      --setcman [cman options]
                        Set cman options
      --setmulticast [multicast address] [multicast options]
                        Sets the multicast address to use (or removes it
                        if no multicast address is given)
      --setaltmulticast [alt multicast address] [alt multicast options]
                        Sets the alt multicast address to use (or removes it
                        if no alt multicast address is given)
      --setfencedaemon [fence daemon options]
                        Set fence daemon options
      --setlogging [logging options]
                        Set logging options
      --addlogging [logging_daemon options]
                        Add a logging daemon (see cluster.conf for options)
      --rmlogging [logging_daemon options]
                        Remove the logging daemon with specified options
  

```



## clusvcadm

```
usage: clusvcadm [command]

Resource Group Control Commands:
  -v                     Display version and exit
  -d <group>             Disable <group>.  This stops a group
                         until an administrator enables it again,
                         the cluster loses and regains quorum, or
                         an administrator-defined event script
                         explicitly enables it again.
  -e <group>             Enable <group>
  -e <group> -F          Enable <group> according to failover
                         domain rules (deprecated; always the
                         case when using central processing)
  -e <group> -m <member> Enable <group> on <member>
  -r <group> -m <member> Relocate <group> [to <member>]
                         Stops a group and starts it on another
                         cluster member.
  -M <group> -m <member> Migrate <group> to <member>
                         (e.g. for live migration of VMs)
  -q                     Quiet operation
  -R <group>             Restart a group in place.
  -s <group>             Stop <group>.  This temporarily stops
                         a group.  After the next group or
                         or cluster member transition, the group
                         will be restarted (if possible).
  -Z <group>             Freeze resource group.  This prevents
                         transitions and status checks, and is 
                         useful if an administrator needs to 
                         administer part of a service without 
                         stopping the whole service.
  -U <group>             Unfreeze (thaw) resource group.  Restores
                         a group to normal operation.
  -c <group>             Convalesce (repair, fix) resource group.
                         Attempts to start failed, non-critical 
                         resources within a resource group.
Resource Group Locking (for cluster Shutdown / Debugging):
  -l                     Lock local resource group managers.
                         This prevents resource groups from
                         starting.
  -S                     Show lock state
  -u                     Unlock resource group managers.
                         This allows resource groups to start.
```


