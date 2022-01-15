## 问题

CentOS/RHEL 8 中, 执行dnf repolist或者其他dnf/yum命令时，出现以下报错：

```sh
shell> dnf repolist
Failed to set locale, defaulting to C.UTF-8            <=报错
Updating Subscription Management repositories.
Unable to read consumer identity

This system is not registered to Red Hat Subscription Management. You can use subscription-manager to register.
```

## 原因

缺少包，导致设置的 `/etc/locale.conf` 中的设置*(如 `LANG=en_US.UTF-8`)*无法被 `dnf`/`yum` 读取

## 解决

yum