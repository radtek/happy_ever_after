## 网络安装Linux

### 安装

```
yum install dhcp xinetd syslinux httpd tftp-server

# dhcpd          动态分配IP
# xinetd         对服务访问进行控制，这里主要是控制tftp
# tftp           从服务器端下载pxelinux.0、default文件
# syslinux       用于网络引导
# httpd          在网络上提供安装源，也就是镜像文件中的内容
```

### xinetd配置

```
vi /etc/xinetd.d/tftp

service tftp
{
        socket_type             = dgram
        protocol                = udp
        wait                    = yes
        user                    = root
        server                  = /usr/sbin/in.tftpd
        server_args             = -s /var/lib/tftpboot
        disable                 = no
        per_source              = 11
        cps                     = 100 2
        flags                   = IPv4
}
```

### DHCP配置

```
vi /etc/dhcp/dhcpd.conf

# 1. 整体的环境设定 (其中192.168.1.100是本机IP地址)
ddns-update-style none;
ignore client-updates;
default-lease-time 259200;
max-lease-time 518400;
option domain-name-servers 192.168.1.100;

# 2. 关于动态分配的 IP 
# 192.168.1.0 netmask 255.255.255.0     服务器所在的内网网段及子网掩码  
# range 192.168.1.101 192.168.1.120     可用的DHCP地址池范围
subnet 192.168.1.0 netmask 255.255.255.0 {
       range 192.168.1.101 192.168.1.120;
       option routers 192.168.1.100;
       option subnet-mask 255.255.255.0;
       next-server 192.168.1.100;
       # the configuration  file for pxe boot
       filename "pxelinux.0";
}
```

### 设置镜像文件、安装配置文件

创建挂载点

```
mkdir /rhel511
mkdir /rhel64
mkdir /rhel79
mkdir /rhel83
ln -s /rhel511 /var/www/html/rhel511
ln -s /rhel64 /var/www/html/rhel64
ln -s /rhel79 /var/www/html/rhel79
ln -s /rhel83 /var/www/html/rhel83
```

编辑fstab文件, 便于开机自动挂载

```
vi /etc/fstab    # /dev/sr0-3分别对应4个版本的镜像

/dev/sr0                /rhel511                iso9660 defaults        0 0
/dev/sr1                /rhel64                 iso9660 defaults        0 0
/dev/sr2                /rhel79                 iso9660 defaults        0 0
/dev/sr3                /rhel83                 iso9660 defaults        0 0
```

执行挂载

```
mount -a
```

安装配置文件 配置

```
mkdir /var/lib/tftpboot/{rhel511,rhel64,rhel79,rhel83}

cp /usr/share/syslinux/{pxelinux.0,menu.c32} /var/lib/tftpboot/
cp -a /rhel511/images/pxeboot/{vmlinuz,initrd.img} /var/lib/tftpboot/rhel511/
cp -a /rhel64/images/pxeboot/{vmlinuz,initrd.img} /var/lib/tftpboot/rhel64/
cp -a /rhel79/images/pxeboot/{vmlinuz,initrd.img} /var/lib/tftpboot/rhel79/
cp -a /rhel83/images/pxeboot/{vmlinuz,initrd.img} /var/lib/tftpboot/rhel83/
```

```
mkdir /var/lib/tftpboot/pxelinux.cfg
vi /var/lib/tftpboot/pxelinux.cfg/default

default menu.c32
prompt 0
timeout 300
ONTIMEOUT local

menu title ########## PXE Boot Menu ##########

label 1
menu label ^1) Install RHEL 5.11 x84_64 with HTTP
kernel rhel511/vmlinuz
append initrd=rhel511/initrd.img method=http://192.168.1.100/rhel511 devfs=nomount

label 2
menu label ^2) Install RHEL 6.4 x84_64 with HTTP
kernel rhel64/vmlinuz
append initrd=rhel64/initrd.img method=http://192.168.1.100/rhel64 devfs=nomount

label 3
menu label ^3) Install RHEL 7.9 x84_64 with HTTP
kernel rhel79/vmlinuz
append initrd=rhel79/initrd.img method=http://192.168.1.100/rhel79 devfs=nomount

label 4
menu label ^4) Install RHEL 8.3 x84_64 with HTTP
kernel rhel83/vmlinuz
append initrd=rhel83/initrd.img method=http://192.168.1.100/rhel83 devfs=nomount
```

### 启动服务

```
systemctl enable dhcpd
systemctl enable xinetd
systemctl enable tftp
systemctl enable httpd

systemctl restart dhcpd
systemctl restart xinetd
systemctl restart tftp
systemctl restart httpd
```

### 注 1

```
报错：/sbin/dmsquash-live-root: line 273: printf: write error: No space left on device
解决：安装时将内存选择为2G以上
```

### 注 2

```
# suse 12sp5

mount /dev/sr5 /sle12sp5
ln -s /sle12sp5 /var/www/html/sle12sp5
cp /sle12sp5/boot/x86_64/loader/{linux,initrd} /var/lib/tftpboot/sle12sp5/

label 5
menu label ^5) Install SUSE Linux Enterprise 12SP5 x84_64 with HTTP
kernel sle12sp5/linux
append initrd=sle12sp5/initrd install=http://192.168.1.100/sle12sp5 splash=silent showopts
```