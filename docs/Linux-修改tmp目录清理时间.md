## 7.x

* 涉及服务

```sh
# systemd-tmpfiles-setup.service         创建
# systemd-tmpfiles-setup-dev.service     创建
# systemd-tmpfiles-clean.service         清理
# systemd-tmpfiles-clean.timer           定时器

systemctl status systemd-tmpfiles-clean.timer
```

```sh
~] vi /usr/lib/tmpfiles.d/tmp.conf 

# Clear tmp directories separately, to make them easier to override
v /tmp 1777 root root 10d          # <=修改此处即可
v /var/tmp 1777 root root 30d      # <=修改此处即可

# Exclude namespace mountpoints created with PrivateTmp=yes
x /tmp/systemd-private-%b-*
X /tmp/systemd-private-%b-*/tmp
x /var/tmp/systemd-private-%b-*
X /var/tmp/systemd-private-%b-*/tmp
```

## 其他

```sh
~] cat /etc/cron.daily/tmpwatch  # 6.9最小化安装没有

#! /bin/sh
flags=-umc
/usr/sbin/tmpwatch "$flags" -x /tmp/.X11-unix -x /tmp/.XIM-unix \
    -x /tmp/.font-unix -x /tmp/.ICE-unix -x /tmp/.Test-unix \
    -X '/tmp/hsperfdata_*' 10d /tmp
/usr/sbin/tmpwatch "$flags" 30d /var/tmp
for d in /var/{cache/man,catman}/{cat?,X11R6/cat?,local/cat?}; do
    if [ -d "$d" ]; then
    /usr/sbin/tmpwatch "$flags" -f 30d "$d"
    fi
done
```