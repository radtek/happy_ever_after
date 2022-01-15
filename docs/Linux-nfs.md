
### 1. 安装所需要的安装包 (服务端和客户端都需要)

```sh
yum install nfs-utils rpcbind(安装nfs-utils时会依赖安装rpcbind)
```

### 2. 确认export的目录

```sh
vim /etc/exports
```

```sh
[共享目录] [第一台主机(权限)] [主机可用主机名、通配符表示]
```

|权限|解释|
| --------- | ------- |
|`rw`,`ro`      | 指定客户端对共享目录的权限：可读或读写（最终能不能读写，还是需要检查文件系统的rwx及身份有关）
|`sync`,`async` | `sync`代表数据会同步写入到内存与硬盘中，`async`则代表数据会暂存于内存当中，而非直接写入硬盘
|`root_squash`,`no_root_squash` | 客户端使用NFS文件系统的账号为root时，系统该如何判断这个账号的身份？<br>	默认的情况下，客户端root的身份会由`root_squash`的设置`nfsnobody`，如此对服务器系统会较有保障。如果想开放客户端使用root身份来操作服务器的文件系统，设置`no_root_squash`
|`all_squash`      | 不论NFS的用户为何，他的身份都会被压缩成为匿名用户，通常也就是nobody(nfsnobody)
|`anonuid`,`anongid` | 对匿名用户设置uid和gid(必须是`/etc/passwd`存在的uid和gid)
|`hide`,`no_hide` | `hide` : NFS共享目录下的子目录不可见<br>`no_hide` : 可见
|`secure`,`insecure` | `secure` : 限制客户端只能从小于1024的tcp/ip端口连接nfs服务器（默认设置）<br>`insecure` : 允许
|`subtree`,`no_subtree`|`subtree` ：若输出目录是一个子目录，则nfs服务器将检查其父目录的权限(默认设置)；<br>`no_subtree`：即使输出目录是一个子目录，nfs服务器也不检查其父目录的权限，这样可以提高效率；

#### Sample

```sh
/           master(rw) trusty(rw,no_root_squash)`
```

```sh
/projects   proj*.local.domain(rw)`
```

```sh
/usr        *.local.domain(ro) @trusted(rw)
```

```sh
/home/joe   pc001(rw,all_squash,anonuid=150,anongid=100)
```

```sh
/pub        *(ro,insecure,all_squash)
```

```sh
/srv/www    -sync,rw server @trusted @external(ro)
```

```sh
/foo        2001:db8:9:e54::/64(rw) 192.0.2.0/24(rw)
```

```sh
/build      buildhost[0-9].local.domain(rw)
```

```sh
/           192.168.163.241(rw)
```
- The first line exports the entire filesystem to machines master and trusty.  In addition to write access, all uid squashing is turned off for host trusty.   
- The second and third entry show examples  for  wildcard  hostnames and  netgroups  (this  is  the entry `@trusted').   
- The fourth line shows the entry for the PC/NFS client discussed above.   
- Line 5 exports the public FTP directory to every host in the world, executing all requests under the nobody account. The insecure option in this entry also allows clients with NFS implementations that don't use a reserved port for NFS.    
- The sixth line exports a directory read-write to the machine 'server' as well as  the `@trusted'  netgroup, and read-only to netgroup `@external', all three mounts with the `sync' option enabled.   
- The seventh line exports a directory to both an IPv6 and an IPv4 subnet.   
- The eighth line demonstrates a character class wildcard match.  
- The ninth line exports a directory to static ip (this is 192.168.163.241)  


### 3. 服务设置

为rpcbind和nfs-server设置开机自启

```sh	
systemctl enable rpcbind
systemctl enable nfs-server
```

启动服务

```
systemctl start rpcbind
systemctl start nfs-server
```


### 4. 客户端设置

安装服务包 

```sh
yum install rpcbind nfs-utils 
```

服务设置

```sh
systemctl enable rpcbind
systemctl start rpcbind
```

获取服务器共享出来的目录

```sh
showmount -e ServerHost
```

### 5. showmount -e 漏洞

`showmount -e` 通过 `mountd` 守护进程去显示信息，因此可以限制 `mountd` 的访问达到限制

```sh
~] vi /etc/hosts.deny
mountd:all

~] vi /etc/hosts.allow
mountd:192.168.55.20
```

```sh
~] rpcinfo -p 192.168.1.71
   program vers proto   port  service
    100000    4   tcp    111  portmapper
    100000    3   tcp    111  portmapper
    100000    2   tcp    111  portmapper
    100000    4   udp    111  portmapper
    100000    3   udp    111  portmapper
    100000    2   udp    111  portmapper
    100024    1   udp  53579  status
    100024    1   tcp  40254  status
    100005    1   udp  20048  mountd
    100005    1   tcp  20048  mountd
    100005    2   udp  20048  mountd
    100005    2   tcp  20048  mountd
    100005    3   udp  20048  mountd
    100005    3   tcp  20048  mountd
    100003    3   tcp   2049  nfs
    100003    4   tcp   2049  nfs
    100227    3   tcp   2049  nfs_acl
    100003    3   udp   2049  nfs
    100003    4   udp   2049  nfs
    100227    3   udp   2049  nfs_acl
    100021    1   udp  48485  nlockmgr
    100021    3   udp  48485  nlockmgr
    100021    4   udp  48485  nlockmgr
    100021    1   tcp  45860  nlockmgr
    100021    3   tcp  45860  nlockmgr
    100021    4   tcp  45860  nlockmgr
```