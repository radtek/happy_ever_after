## lvm命令

命令|释义
--|--
`lvchange` | Change the attributes of logical volume(s)
`lvconvert` | Change logical volume layout
`lvcreate` | Create a logical volume
`lvdisplay` | Display information about a logical volume
`lvextend` | Add space to a logical volume
`lvmchange` | With the device mapper, this is obsolete and does nothing.
`lvmconfig` | Display and manipulate configuration information
`lvmdiskscan` | List devices that may be used as physical volumes
`lvmsadc` | Collect activity data
`lvmsar` | Create activity report
`lvreduce` | Reduce the size of a logical volume
`lvremove` | Remove logical volume(s) from the system
`lvrename` | Rename a logical volume
`lvresize` | Resize a logical volume
`lvs` | Display information about logical volumes
`lvscan` | List all logical volumes in all volume groups
`pvchange` | Change attributes of physical volume(s)
`pvresize` | Resize physical volume(s)
`pvck` | Check the consistency of physical volume(s)
`pvcreate` | Initialize physical volume(s) for use by LVM
`pvdata` | Display the on-disk metadata for physical volume(s)
`pvdisplay` | Display various attributes of physical volume(s)
`pvmove` | Move extents from one physical volume to another
`lvpoll` | Continue already initiated poll operation on a logical volume
`pvremove` | Remove LVM label(s) from physical volume(s)
`pvs` | Display information about physical volumes
`pvscan` | List all physical volumes
`segtypes` | List available segment types
`systemid` | Display the system ID, if any, currently set on this host
`tags` | List tags defined on this host
`vgcfgbackup` | Backup volume group configuration(s)
`vgcfgrestore` | Restore volume group configuration
`vgchange` | Change volume group attributes
`vgck` | Check the consistency of volume group(s)
`vgconvert` | Change volume group metadata format
`vgcreate` | Create a volume group
`vgdisplay` | Display volume group information
`vgexport` | Unregister volume group(s) from the system
`vgextend` | Add physical volumes to a volume group
`vgimport` | Register exported volume group with system
`vgimportclone` | Import a VG from cloned PVs
`vgmerge` | Merge volume groups
`vgmknodes` | Create the special files for volume group devices in /dev
`vgreduce` | Remove physical volume(s) from a volume group
`vgremove` | Remove volume group(s)
`vgrename` | Rename a volume group
`vgs` | Display information about volume groups
`vgscan` | Search for all volume groups
`vgsplit` | Move physical volumes into a new or existing volume group


## pvmove

可将某一个物理卷中的数据转移到同卷组的其他物理卷中。多用于更换卷组中的硬盘。

该命令执行，被移动的pv上的lv处于被挂载和使用的情况下也能够正常移动到另一个pv上。

> **注意，该操作要求对整个硬盘建立pv而不是仅仅针对一个分区创建pv**

### 实操  

> 例如，在卷组vg_data中有两个1g的pv分别是`/dev/sdb`与`/dev/sdc`。现在需要将这两个pv上的数据完整移动到一个新的pv（/dev/sdd）上（该pv很可能是一块4g的硬盘），那么可以使用pemove。

#### 操作步骤如下（操作之前备份数据）:


- (1) 把新磁盘/dev/sdd添加到lvm卷组中

```bash
pvcreate /dev/sdd;
vgextend vg_data /dev/sdd
```

- (2) 将旧分区数据移动到新磁盘/dev/sdd中(该过程完成时间和数据量大小有关)

```bash
pvmove –v /dev/sdb /dev/sdd
```

等同于

```bash
pvmove /dev/sdb /dev/sdd
pvmove /dev/sdc /dev/sdd
```

- (3) 将旧磁盘从vg中删除

```bash
vgreduce vg_data /dev/sdb
vgreduce vg_data /dev/sdc
```

- (4) 删除pv

```bash
pvremove /dev/sdb
pvremove /dev/sdc
```

## lvm在线扩容

#### 扫盘

```bash
# (1)
echo "- - -" > /sys/class/scsi_host/host0/scan

# (2)
for file in $(ls /sys/class/scsi_host);do echo "- - -" > /sys/class/scsi_host/${file}/scan; done

# (3)
/usr/bin/rescan-scsi-bus.sh
```

#### 

```bash
pvcreate /dev/sd?

vgextend vg? /dev/sd?

lvextend -L +100M /path/lv?
lvextend -l +100%FREE /path/lv?

resize2fs /path/lv?
xfs_growfs /path/lv?
```
