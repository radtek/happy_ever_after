## 报错

```
...
dracut-initqueue timeout: dracut-initqueue timeout
...
/dev/rootvg/lvswap1 does not exist
/dev/rootvg/lvswap2 does not exist
/dev/rootvg/lvswap3 does not exist
/dev/rootvg/lvswap4 does not exist

dracut>
```

## 原因

`/dev/rootvg/lvswap1`被人为删除


## 解决

1. 手动挂载`/`、`/boot`、`/boot/efi`(如果有efi，可以结合blkid和/etc/fstab判断)
2. 修改 `/<MOUNT_POINT>/etc/fstab`, 注释掉swap相关的配置行
3. 修改 `/<MOUNT_POINT>/boot/efi/EFI/redhat/grub.cfg`, 将`linux16`(efi为`linuxefi`)行中的`rd.lvm.lv=rootvg/swap`字样的都注释(先备份后再修改)
4. `reboot`