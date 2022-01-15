## `kvm桥接`

```
                              --vnet0  ==> kvm-host0
宿主机 ==> br0 ==> ens33 ==>  
                              --vnet1  ==> kvm-host1
```

```
# 修改ifcfg-ens33, 注释掉IP信息, 添加 BRIDGE=br0
TYPE=Ethernet
BOOTPROTO=none
DEFROUTE=yes
IPV4_FAILURE_FATAL=no
NAME=ens33
DEVICE=ens33
ONBOOT=yes
#IPADDR=192.168.1.100   <=
#PREFIX=24              <=
BRIDGE=br0              <=
```

```
# 添加ifcfg-br0
DEVICE=br0
ONBOOT=yes
TYPE=Bridge
BOOTPROTO=none
IPADDR=192.168.1.100   <=
NETMASK=255.255.255.0  <=
DELAY=0
```

重启网络即可

```
brctl show 

bridge name     bridge id               STP enabled     interfaces
br0             8000.000c297b41d3       no              ens33        <=
virbr0          8000.525400e4a58b       yes             virbr0-nic
```