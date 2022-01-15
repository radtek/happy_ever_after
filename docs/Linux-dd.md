# dd

<br>

### 参数

```
if=文件名：输入文件名，缺省为标准输入。即指定源文件。<if=inputfile>
of=文件名：输出文件名，缺省为标准输出。即指定目的文件。< of=output file >
ibs=bytes：一次读入bytes个字节，即指定一个块大小为bytes个字节。
obs=bytes：一次输出bytes个字节，即指定一个块大小为bytes个字节。
bs=bytes：同时设置读入/输出的块大小为bytes个字节。
cbs=bytes：一次转换bytes个字节，即指定转换缓冲区大小。
skip=blocks：从输入文件开头跳过blocks个块后再开始复制。
seek=blocks：从输出文件开头跳过blocks个块后再开始复制。
	注意：通常只用当输出文件是磁盘或磁带时才有效，即备份到磁盘或磁带时才有效。
count=blocks：仅拷贝blocks个块，块大小等于ibs指定的字节数。
```

```sh
conv=conversion：用指定的参数转换文件。
	ascii：转换ebcdic为ascii
	ebcdic：转换ascii为ebcdic
	ibm：转换ascii为alternateebcdic
	block：把每一行转换为长度为cbs，不足部分用空格填充
	unblock：使每一行的长度都为cbs，不足部分用空格填充
	lcase：把大写字符转换为小写字符
	ucase：把小写字符转换为大写字符
	swab：交换输入的每对字节
	noerror：出错时不停止
	notrunc：不截断输出文件
	nocreate：不创建输出文件
	sync：将每个输入块填充到ibs个字节，不足部分用空（NUL）字符补齐。
```

```sh
iflag/oflag=FLAGS  指定读/写的方式标签
	append：追加的方式(只对output产生影响)，建议和conv=notrunc搭配使用
	direct：读写数据采用I/O
	directory：非directory就会读写失败
	dsync：书写数据采用synchronized I/O
	sync：同上，但包括metadata
	fullblock：占满block (iflag only)
	nonblack：使用non-blocking I/O
	noatime：不更新access time
	nocache：discard cached data
	nofollow：do not follow symlinks
	skip_bytes/counts_bytes (iflag only)：相应的skip=N/count=N变为N bytes 
	seek_bytes (oflay only)：相应的seek=N变为N bytes
```

```sh
status=LEVEL：控制dd程序的输出信息
	none：除error外，不输出任何信息
	noxfer：不输出最后的统计信息
	progress：输出所有信息
```

> dd做读写测试时，要加两个参数`iflag=nocache`, `oflag=direct`，否则dd有时会显示从内存中传输数据	

<br>

### 1.将本地的/dev/hdb整盘备份到/dev/hdd

```
dd if=/dev/hdb of=/dev/hdd
```

### 2.将/dev/hdb全盘数据备份到指定路径的image文件

```
dd if=/dev/hdb of=/root/image
```

### 3.将备份文件恢复到指定盘

```
dd if=/root/image of=/dev/hdb
```

### 4.备份/dev/hdb全盘数据，并利用gzip工具进行压缩，保存到指定路径

```
dd if=/dev/hdb | gzip > /root/image.gz
```

### 5.将压缩的备份文件恢复到指定盘

```
gzip -dc /root/image.gz | dd of=/dev/hdb
```

### 6.备份磁盘开始的512个字节大小的MBR信息到指定文件

```
dd if=/dev/hda of=/root/image count=1 bs=512
```
count=1指仅拷贝一个块  
bs=512指块大小为512个字节  



恢复：

```
dd if=/root/image of=/dev/hda
```

### 7.备份软盘

```
dd if=/dev/fd0 of=disk.img count=1 bs=1440k
```
bs=1440k 即块大小为1.44M

### 8.拷贝内存内容到硬盘

```
dd if=/dev/mem of=/root/mem.bin bs=1024
```

### 9.拷贝光盘内容到指定文件夹，并保存为cd.iso文件

```
dd if=/dev/cdrom(hdc) of=/root/cd.iso
```

### 10.增加swap分区文件大小

第一步：创建一个大小为256M的文件：

```
dd if=/dev/zero of=/swapfile bs=1024 count=262144
```

第二步：把这个文件变成swap文件：

```
mkswap /swapfile
```

第三步：启用这个swap文件：

```
swapon /swapfile
```

第四步：编辑/etc/fstab文件，使在每次开机时自动加载swap文件：

```
/swapfile swap swap defaults 0 0
```


若出现`swapon: /xxx/swapfile: swapon failed: Cannot allocate memory`


- Increase `vm.min_free_kbytes` value, for example to a higher value than a single allocation request. 
- Change `vm.zone_reclaim_mode` to 1 if it's set to zero, so the system can reclaim back memory from cached memory.  


### 11.销毁磁盘数据

```
dd if=/dev/urandom of=/dev/hda1
```

注意：利用随机的数据填充硬盘，在某些必要的场合可以用来销毁数据。

### 12.测试硬盘的读写速度

```
dd if=/dev/zero bs=1024 count=1000000 of=/root/1Gb.file
dd if=/root/1Gb.file bs=64k | dd of=/dev/null
```

通过以上两个命令输出的命令执行时间，可以计算出硬盘的读、写速度。

### 13.确定硬盘的最佳块大小：

```
dd if=/dev/zero bs=1024 count=1000000 of=/root/1Gb.file
dd if=/dev/zero bs=2048 count=500000 of=/root/1Gb.file
dd if=/dev/zero bs=4096 count=250000 of=/root/1Gb.file
dd if=/dev/zero bs=8192 count=125000 of=/root/1Gb.file
```

通过比较以上命令输出中所显示的命令执行时间，即可确定系统最佳的块大小。

### 14.修复硬盘

```
dd if=/dev/sda of=/dev/sda
```

当硬盘较长时间（比如1，2年）放置不使用后，磁盘上会产生magnetic fluxpoint。当磁头读到这些区域时会遇到困难，并可能导致I/O错误。当这种情况影响到硬盘的第一个扇区时，可能导致硬盘报废。上边的命令有可能使这些数据起死回生。且这个过程是安全，高效的。

### 15.dd命令做usb启动盘

```
dd if=xxx.iso of=/dev/sdb bs=1M
```

- root用户或者sudo  
- 用以上命令前必须卸载u盘, sdb是你的u盘,bs=1M是块的大小,后面的数值大,写的速度相对快一点,但也不是无限的,我一般选2M,注意,执行命令后很快完成,但u盘还在闪,等不闪了,安全移除。

### 16.

### 1)生成文件大小和实际占空间大小一样的文件

```
dd if=/dev/zero of=name.file bs=1M count=1
```

bs=1M表示每一次读写1M数据，count=50表示读写 50次，这样就指定了生成文件的大小为50M。

### 2)生成文件大小固定，但实际不占空间命令

```
dd if=/dev/zero of=1G.img bs=1M seek=1000 count=0
```

seek=1000表示略过1000个Block不写(这里Block按照bs的定义是1M)，count=0表示写入0个Block。

用ls(查看文件大小)命令看新生成的文件，大小可以看出是1000M。但是再用du(查看文件占用空间)一看，实际占用硬盘大小只有0M。


### 17. 占用内存

```sh
#!/bin/bash
mkdir /tmp/memory  
mount -t tmpfs -o size=1024M tmpfs /tmp/memory
dd if=/dev/zero of=/tmp/memory/block

sleep 3600
rm /tmp/memory/block
umount /tmp/memory
rmdir /tmp/memory
```
