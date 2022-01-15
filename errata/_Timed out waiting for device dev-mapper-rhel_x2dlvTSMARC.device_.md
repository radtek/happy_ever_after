## 问题

服务器启动过程中报错: `Timed out waiting for device dev-mapper-rhel\x2dlvTSMARC.device`, 自动进入紧急模式(`emergency mode`)

```sh
...
Job device dev-mapper-rhel\x2dlvTSMARC.device/start timed out
systemd[1]: Timed out waiting for device dev-mapper-rhel\x2dlvTSMARC.device
Dependence failed for /TSMARC.
Denpedence failed for Local File Systems.
Job...
```


## 原因

- 检查 `/etc/fstab`
- 检查 `lsblk`, `lvs`
- 比对上面区别, 检查 `/etc/fstab` 中是否存在配置错误的行

## 解决

- 输入root密码, 进入紧急模式
- 编辑 `/etc/fstab`, 注释相应行
- `reboot`
