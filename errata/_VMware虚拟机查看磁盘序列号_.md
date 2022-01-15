> 默认情况下，VMware创建的虚拟机，无法查询到虚拟磁盘的序列号。如果是因为需要应用系统要求或者其他原因，需要系统内显示磁盘序列号，按以下步骤操作。

* 1 关闭虚拟机
* 2 编辑虚拟机vmx文件，添加以下内容：

```
disk.EnableUUID="TRUE"
```

* 3 重启即可查询。

```
smartctl -a /dev/sda
lsblk -d -n -o serial /dev/sda
```