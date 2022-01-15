## 一、从备份文件中恢复

> 适用于主引导分区被破坏,无法通过手动输入引导命令解决

### 1. 备份

MBR位于第一块硬盘(`/dev/sda)` 的第一个物理扇区处，总共512字节，前446字节是主引导记录，分区表保存在MBR扇区中的第447-510字节中

```sh
dd if=/dev/vda of=/root/grub.bak bs=446 count=1
```

### 2. 模拟主引导记录丢失

```sh
dd if=/dev/zero of=/dev/vda bs=446 count=1
```

此时重启, 服务器卡在 `boot from hard disk`

### 3. 修复

- 挂iso进入救援模式
- `chroot`进入`/mnt/image`
- 修复:
    ```sh
    dd if=/root/grub.bak of=/dev/vda bs=446 count=1
    ```
- 执行重启

## 二、手动输入引导命令

> 适用于主引导分区未被破坏, grub文件配置错误或者丢失
> 此时重启系统会提示 `grub>`

### RHEL/CentOS 6

> 6系的`grub>`命令有限， 如`ls`等命令都没有，因此只能使用tab补全

- 模拟`grub.cfg`文件丢失, 重启后系统进入 `grub >` 提示符界面
    ```sh
    $ mv /boot/grub/grub.conf /tmp
    $ reboot
    ```
- 选择磁盘
    ```sh
    grub> root (hd0,0)
    ```
- 选择内核文件, 同时指定内核参数
    ```sh
    grub> kernel /vmlinuz-2.6.32-358.el6.x86_64 ro root=/dev/vda2 selinux=1 # 只指定了有限的参数: "根目录挂载", "SELinux状态设置"
    ```
- 选择`initrd`(初始化时的根文件系统)
    ```sh
    grub> initrd /initramfs-2.6.32-358.el6.x86_64.img
    ```
- 启动
    ```sh
    grub> boot
    ```
- 进入系统以后需要还原`grub.conf`配置文件
    * 1.手动编辑一份
    * 2.从同版本的系统复制一份, 修改参数

> RHEL 6.4 /boot/grub/grub.conf
>   ```conf
>   default=0
>   timeout=5
>   splashimage=(hd0,0)/grub/splash.xpm.gz
>   hiddenmenu
>   title Red Hat Enterprise Linux (2.6.32-358.el6.x86_64)
>       root (hd0,0)
>       kernel /vmlinuz-2.6.32-358.el6.x86_64 ro root=UUID=1b0a442f-e911-4c61-8558-bb1f167affde rd_NO_LUKS rd_NO_LVM LANG=en_US.UTF-8 rd_NO_MD SYSFONT=latarcyrheb-sun16 crashkernel=128M  KEYBOARDTYPE=pc KEYTABLE=us rd_NO_DM rhgb quiet console=ttyS0
>	    initrd /initramfs-2.6.32-358.el6.x86_64.img
>    ```


### RHEL/CentOS 7

- 模拟`grub.cfg`文件丢失, 重启后系统进入 `grub >` 提示符界面
    ```sh
    $ mv /boot/grub2/grub.cfg /tmp/
    $ reboot
    ```
- 查看
    ```sh
    grub> ls
    (hd0) (hd0,msdos3) (hd0,msdos2) (hd0,msdos1)

    grub> ls (hd0,msdos1)
        Partition hd0,msdos1: Filesystem type xfs, UUID xxxxxxxxxxxxxxxxxxx - Partition start at 1024KiB - Total size 1048576Kib <= 这个约1024Mb的就是分配给/boot的分区, 指定这个
    
    grub> cat (hd0,msdos1)/grub2/device.map
    (hd0)   /dev/vda                                   <=hd0 磁盘在系统中名称为vda
    ...
    
    grub> ls (hd0,msdos3)
        Partition hd0,msdos3: Filesystem type xfs, UUID xxxxxxxxxxxxxxxxxxx - Partition start at 2098176KiB - Total size 8387584Kib <= 这个约8G的就是分配给/的分区, linux16中需要root指定(root=/dev/vda3)
    ```
- 选择磁盘
    ```sh
    grub > set root=(hd0,msdos1)
    ```
- 选择内核文件, 同时指定内核参数
    ```sh
    grub > linux16 /vmlinuz-3.10.0-1160.el7.x86_64 ro root=/dev/vda3
    # grub > linux16 /vmlinuz-3.10.0-1160.el7.x86_64 ro root=/dev/mapper/rhel-root rd.lvm.lv=rhel/root 如果使用的是lvm系统，要指定root的lv路径
    ```
- 选择`initrd`(初始化时的根文件系统)
    ```sh
    grub > initrd16 /initramfs-3.10.0-1160.el7.x86_64.img
    ```
- 启动
    ```sh
    grub > boot
    ```
- 进入系统以后需要还原`grub.cfg`配置文件
    ```sh
    grub2-mkconfig -o /boot/grub2/grub.cfg
    ```


## 三、救援模式重新生成

> 此方法需要使用 `grub2-install`/`grub-install` 命令

**RHEL/CentOS 6**

```x
sh-4.1# grub-install /dev/vda
sh-4.1# vi /boot/grub/grub.conf

default=0
timeout=5
title RHEL 6.4
kernel /vmlinuz-2.6.32-358.el6.x86_64 ro root=/dev/vda2 selinux=1
initrd /initramfs-2.6.32-358.el6.x86_64.img
```

**RHEL/CentOS 7**

```x
sh-4.2# grub2-install /dev/vda
sh-4.2# grub2-mkconfig -o /boot/grub2/grub.cfg
```