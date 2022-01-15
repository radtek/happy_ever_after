## 问题

服务器启动过程中报错: `Timed out waiting for device dev-disk-by\x2duuid-XXXXXXX.device`, 自动进入紧急模式(`emergency mode`)

## 原因

`/etc/fstab` 中使用的是`UUID`指定挂载设备, 而此时`UUID`发生改变

## 解决

- 输入root密码, 进入紧急模式
- `blkid`查看对应分区的`UUID`
- 编辑 `/etc/fstab`, 修改`UUID`
- `reboot`
