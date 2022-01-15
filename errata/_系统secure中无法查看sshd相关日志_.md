> sshd相关的日志在 `/var/log/secure` 中不显示，但是在 `/var/log/messages` 有相关

- 检查 `sshd` 当前的配置

```sh
shell> sshd -T | grep -i syslogfacility
syslogfacility AUTH     <= 此处日志设备为 AUTH
```

- 检查 `rsyslog` 配置

```sh
shell> grep -Ev '^$|^#' /etc/rsyslog.conf 
...
*.info;mail.none;authpriv.none;cron.none                /var/log/messages   <= rsyslog默认配置：auth日志会写入messages
authpriv.*                                              /var/log/secure     <= authpriv日志会写入secure
...
```

- 查看 `sshd` 配置文件 `/etc/ssh/sshd_config`

```x
shell> less /etc/ssh/sshd_config
#SyslogFacility AUTH  <= 只有注释的行
```

新增一行配置，重启sshd服务， 

```x
shell> vi /etc/ssh/sshd_config
#SyslogFacility AUTH
SyslogFacility AUTHPRIV

shell> systemctl restart sshd
shell> sshd -T | grep -i syslogfacility
syslogfacility AUTHPRIV     <= 此处日志设备为 AUTH
```