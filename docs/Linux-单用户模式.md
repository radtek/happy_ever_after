## RHEL/Centos 6.x

```
select "kernel…"

s或者single

passwd root

reboot
```
 
## RHEL/Centos 7.x/8.x

* 使用 `runlevel1.target` 或 `rescue.target` 来实现。
* 在此模式下，系统会**挂载所有的本地文件系统**，但不开启网络接口。
* 系统仅启动特定的几个服务和修复系统必要的尽可能少的功能
* 常用场景：
  * 修复损坏的文件系统
  * 重置root密码
  * 修复系统上的一个挂载点问题

**`CentOS/RHEL 7/8` 系统有三种方式进单用户：**

* 方法 1：通过向内核添加 `rd.break` 参数
* 方法 2：通过用 `init=/bin/bash` 或 `init=/bin/sh` 替换内核中的 `rhgb quiet` 语句
* 方法 3：通过用 `rw init=/sysroot/bin/sh` 替换内核中的 `ro` 语句

```
# (1) linux16 这一行添加:
rd.break

# (2) ctrl+x 引导后, 执行以下命令修改/sysroot为读写(rw)
mount -o remount,rw /sysroot/

# (3) 切换环境
chroot /sysroot/

# (4) 7/8版本系统默认使用 SELinux，因此创建下面的隐藏文件，这个文件会在下一次启动时重新标记所有文件。
touch /.autorelabel
reboot
```

```
# (1) init=/bin/bash 或 init=/bin/sh 替换内核中的 rhgb quiet 语句

# (2) 重新挂载/
mount -o remount,rw /

# (3) 标记, 重启
touch /.autorelabel
exec /sbin/init 6
```

```
# (1) rw init=/sysroot/bin/sh 替换内核中的 ro 单词

# (2) 切换环境
chroot /sysroot

# (3) 标记, 重启
touch /.autorelabel
reboot -f
```

## SuSE 12

```sh
init=/bin/bash

mount -o remount,rw /
echo 'root:password' | /usr/sbin/chpasswd
mount -o remount,ro /
```

## Ubuntu

高级选项 => recovery模式 => 

```
ro recovery nomode set ==> rw single init=/bin/bash
```

## Kylin V10

```
# grub: root/Kylin123123

rd.break
mount -o remount,rw /sysroot
chroot /sysroot
reboot
```

arm: 华为泰山

```
# grub: root/Kylin123123

init=/bin/bash console=tty1
mount -o remount,rw /sysroot
chroot /sysroot
reboot
```