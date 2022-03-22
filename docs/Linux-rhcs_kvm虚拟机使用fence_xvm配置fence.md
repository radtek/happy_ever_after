> ```sh
> 涉及的包:  
>     fence-virtd.x86_64 : Daemon which handles requests from fence-virt
>     fence-virtd-libvirt.x86_64 : Libvirt backend for fence-virtd
>     fence-virtd-multicast.x86_64 : Multicast listener for fence-virtd
>     fence-virtd-serial.x86_64 : Serial VMChannel listener for fence-virtd
>     fence-virt.x86_64 : A pluggable fencing framework for virtual machines
> 
> RHCS使用的stonith类型：
>     fence_xvm
> ```


## 宿主机配置

**1. 安装**

```sh
yum install fence-virtd fence-virtd-libvirt fence-virtd-multicast
```

**2. 生成key**

```sh
mkdir /etc/cluster
dd if=/dev/urandom of=/etc/cluster/fence_xvm.key bs=4K count=1
```

**3. 使用配置引导, 按需修改**

> `Interface [br0]: ` 注意这里要填kvm虚拟机使用的网络

```sh
[root@striver ~]# fence_virtd -c
Module search path [/usr/lib64/fence-virt/]: 

Available backends:
    libvirt 0.3
Available listeners:
    vsock 0.1
    multicast 1.2

Listener modules are responsible for accepting requests
from fencing clients.

Listener module [multicast]: 

The multicast listener module is designed for use environments
where the guests and hosts may communicate over a network using
multicast.

The multicast address is the address that a client will use to
send fencing requests to fence_virtd.

Multicast IP Address [225.0.0.12]: 

Using ipv4 as family.

Multicast IP Port [1229]: 

Setting a preferred interface causes fence_virtd to listen only
on that interface.  Normally, it listens on all interfaces.
In environments where the virtual machines are using the host
machine as a gateway, this *must* be set (typically to virbr0).
Set to 'none' for no interface.

Interface [br0]: 

The key file is the shared key information which is used to
authenticate fencing requests.  The contents of this file must
be distributed to each physical host and virtual machine within
a cluster.

Key File [/etc/cluster/fence_xvm.key]: 

Backend modules are responsible for routing requests to
the appropriate hypervisor or management layer.

Backend module [libvirt]: 

The libvirt backend module is designed for single desktops or
servers.  Do not use in environments where virtual machines
may be migrated between hosts.

Libvirt URI [qemu:///system]: 

Configuration complete.

=== Begin Configuration ===
backends {
	libvirt {
		uri = "qemu:///system";
	}

}

listeners {
	multicast {
		port = "1229";
		family = "ipv4";
		interface = "br0";
		address = "225.0.0.12";
		key_file = "/etc/cluster/fence_xvm.key";
	}

}

fence_virtd {
	module_path = "/usr/lib64/fence-virt/";
	backend = "libvirt";
	listener = "multicast";
}

=== End Configuration ===
Replace /etc/fence_virt.conf with the above [y/N]? Y
```

**4. 启动`fence_virtd`服务**

```sh
systemctl restart fence_virtd.service 
```


## 虚拟机配置

**1. 安装**

```sh
yum install fence-virt fence-virtd-multicast
```

**2. 复制宿主机的key**

> 每个集群节点都要执行

```sh
mkdir /etc/cluster
scp root@rhel79:/etc/cluster/fence_xvm.key /etc/cluster/
```

**3. 添加fence设备**


```sh
[root@nginx-01 ~]# pcs stonith describe fence_xvm
fence_xvm - Fence agent for virtual machines

fence_xvm is an I/O Fencing agent which can be used withvirtual machines.

Stonith options:
  debug: Specify (stdin) or increment (command line) debug level
  ip_family: IP Family ([auto], ipv4, ipv6)
  multicast_address: Multicast address (default=225.0.0.12 / ff05::3:1)
  ipport: TCP, Multicast, or VMChannel IP port (default=1229)
  retrans: Multicast retransmit time (in 1/10sec; default=20)
  auth: Authentication (none, sha1, [sha256], sha512)
  hash: Packet hash strength (none, sha1, [sha256], sha512)
  key_file: Shared key file (default=/etc/cluster/fence_xvm.key)
  port: Virtual Machine (domain name) to fence
  use_uuid: Treat [domain] as UUID instead of domain name. This is provided for compatibility with older fence_xvmd installations.
  timeout: Fencing timeout (in seconds; default=30)
  delay: Fencing delay (in seconds; default=0)
  domain: Virtual Machine (domain name) to fence (deprecated; use port)
  pcmk_host_map: A mapping of host names to ports numbers for devices that do not support host names. Eg. node1:1;node2:2,3 would tell the cluster to use port 1 for node1 and ports 2 and 3 for node2
  pcmk_host_list: A list of machines controlled by this device (Optional unless pcmk_host_check=static-list).
  pcmk_host_check: How to determine which machines are controlled by the device. Allowed values: dynamic-list (query the device via the 'list' command), static-list (check the pcmk_host_list attribute), status
                   (query the device via the 'status' command), none (assume every device can fence every machine)
  pcmk_delay_max: Enable a random delay for stonith actions and specify the maximum of random delay. This prevents double fencing when using slow devices such as sbd. Use this to enable a random delay for
                  stonith actions. The overall delay is derived from this random delay value adding a static delay so that the sum is kept below the maximum delay.
  pcmk_delay_base: Enable a base delay for stonith actions and specify base delay value. This prevents double fencing when different delays are configured on the nodes. Use this to enable a static delay for
                   stonith actions. The overall delay is derived from a random delay value adding this static delay so that the sum is kept below the maximum delay.
  pcmk_action_limit: The maximum number of actions can be performed in parallel on this device Pengine property concurrent-fencing=true needs to be configured first. Then use this to specify the maximum number
                     of actions can be performed in parallel on this device. -1 is unlimited.

Default operations:
  monitor: interval=60s
```

参照以上说明, 配置命令如下:

```sh
# pcs stonith create vmfence fence_xvm pcmk_host_map="nginx-01:rhel79-nginx-01;nginx-02:rhel79-nginx-02" op monitor interval=60s
pcs stonith create vmfence fence_xvm pcmk_host_map="nginx-01:rhel79-nginx-01;nginx-02:rhel79-nginx-02" pcmk_host_list="nginx-01,nginx-02" pcmk_host_check=static-list

# vmfence: fence设备名
# fence_xvm: 类型
# pcmk_host_map: Node01:rhel79-01;Node02:rhel79-02
#     Node01和Node02: 主机名, 也是集群中节点的名字
#     rhel79-01和rhel79-02: 虚拟机在kvm中的domain name(即虚拟机名)
```

**4. 其他**

可以在节点上查看可用的fence: 

```sh
 stonith_admin -I
 stonith_admin -M -a fence_xvm # 查看fence_xvm的详细信息
```

宿主机上查看当前虚拟机：

```sh
shell> fence_xvm -o list

rhel79-nginx-01                  fde1e89d-ff52-446c-b771-ec3eb5b1d4b2 on
rhel79-nginx-02                  fcd396e5-799e-4b51-aac7-fd76e8469a33 on
```

宿主机测试：

```sh
# 测试on,off,reboot,status等操作
fence_xvm -o off -H rhel79-nginx-01
fence_xvm -o off -H rhel79-nginx-02
```

节点上验证：

```sh
 fence_xvm -H rhel79-nginx-01 -d -o reboot
```

集群测试fence：	

```sh
pcs stonith fence rhel79-nginx-01
pcs stonith fence rhel79-nginx-02
```

 集群设置fence动作：

```sh
pcs property show --all | grep stonith
pcs property show --all | grep stonith
```









