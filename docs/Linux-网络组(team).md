## 网络组的基本信息

**网络组**：将多个网卡聚合在一起方法，从而实现冗错和提高吞吐量

不同于旧版中bonding技术，网络组提供更好的性能和扩展性; 网络组由内核驱动和teamd守护进程实现。

### 网络组支持的方式(runner): 

- `broadcast`
- `roundrobin`
- `activebackup`
- `loadbalance`
- `lacp` (implements the 802.3ad Link Aggregation Control Protocol)

### 网络组相关特性

- 启动网络组接口不会自动启动网络组中的port接口  
- 启动网络组接口中的port接口总会自动启动网络组接口  
- 禁用网络组接口会自动禁用网络组中的port接口  
- 没有port接口的网络组接口可以启动静态IP连接  
- 启用DHCP连接时，没有port接口的网络组会等待port接口的加入  

## 网络组的相关配置

### 1. 通过nmctl命令创建team

#### 创建网络接口组

```sh
nmcli connection add type team con-name team0 ifname team0 config '{"runner":{"name":"activebackup"}}'
```

#### 绑定ip

```sh
nmcli connection modify team0 ipv4.method manual ipv4.addresses 192.168.1.20/24 ipv4.gateway 192.168.1.1
```

#### 创建port接口

```sh
nmcli connection add type team-slave con-name team0-ens33 ifname ens33 master team0
nmcli connection add type team-slave con-name team0-ens38 ifname ens38 master team0
```

#### 启动

```
nmcli connection up team0
nmcli connection up team0-ens33
nmcli connection up team0-ens38
```

```
systemctl restart network
```

#### 查看状态

```sh
teamdctl team0 stat
```

#### 修改team参数配置

```sh
nmcli connection modify team0 team.config '{"runner":{"name":"activebackup","hwaddr_policy":"by_active","primary":"ens33"}}'
```

- `"hwaddr_policy":"by_active"`配置是为了解决以下VMware Workstation的报错：  

![Picture](./Pictures/Linux-team-Mac地址报错.png)

- `"primary":"ens33"`用于指定主网卡

- 修改 Team Port 优先级

  - `prio` 越大, 优先级越高

  - 方法一: 手动编辑port配置文件`ifcfg-team0-xxx`, 添加 `TEAM_PORT_CONFIG="{\"prio\": 100}"`, 或者用单引号 `TEAM_PORT_CONFIG='{"prio": 100}'`

  - 方法二: 使用命令添加: `nmcli connection modify team0-eth2 team-port.prio 100`


### 2. 配置文件创建team


- /etc/sysconfig/network-scripts/ifcfg-team0

```cong
DEVICE=team0
DEVICETYPE=Team
TEAM_CONFIG="{\"runner\":{\"name\":\"activebackup\",\"hwaddr_policy\":\"by_active\",\"primary\":\"ens33\"}}"
#TEAM_CONFIG="{\"runner\":{\"name\":\"activebackup\"}}"
BOOTPROTO=none
NAME=team0
ONBOOT=yes
IPADDR=192.168.1.20
PREFIX=24
GATEWAY=192.168.1.1
```

- /etc/sysconfig/network-scripts/ifcfg-team0-ens33

```x
NAME=team0-ens33
DEVICE=ens33
ONBOOT=yes
TEAM_MASTER=team0
DEVICETYPE=TeamPort
```

- /etc/sysconfig/network-scripts/ifcfg-team0-ens38

```x
NAME=team0-ens38
DEVICE=ens38
ONBOOT=yes
TEAM_MASTER=team0
DEVICETYPE=TeamPort
```

优先度配置：
```
TEAM_PORT_CONFIG='{"prio"=110}'
TEAM_PORT_CONFIG='{"prio"=100}'     #越大越优先

nmcli connection modify team0-port1 team-port.config '{"prio":100}'
nmcli connection modify team0-port2 team-port.config '{"prio":110}'
```

<!--Picture: Base64 Encoding-->

