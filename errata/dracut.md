问题:

```text
...
[  192.205351] dracut-initqueue[259]: Warning: dracut-initqueue timeout

         Starting Dracut Emergency Shell...
Warning: /dev/centos/root does not exist
Warning: /dev/centos/swap does not exist
Warning: /dev/mapper/centos-root does not exist

Generating "/run/initramfs/rdsosreport.txt"

Entering emergency mode. Exit the shell to continue.
Type "journalctl" to view system logs.
You might want to save "/run/initramfs/rdsosreport.txt" to a USB stick or /boot
after mounting them and attach it to a bug report.

dracut:/#
```

解决:

* 开机内核选择界面, 选择: 

```text
CentOS Linux (3.10.0-957.el7.x86_64) 7 (Core)
CentOS Linux (0-rescue-93c544f64f10461fb312def8eef16f41) 7 (Core)   <= 选择这个
```

* 使用 root 登录

* 执行 `dracut -f`

* 重启后恢复正常