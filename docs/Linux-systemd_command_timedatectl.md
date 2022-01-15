# `timedatectl` — 控制系统的时间与日期

```sh
timedatectl [OPTIONS...] {COMMAND}
```

## 选项(RHEL8)

```
--no-ask-password
    在执行特权操作时 不向用户索要密码。

--adjust-system-clock
    当使用 set-local-rtc 命令时， 若使用了此选项， 则表示根据RTC时间来更新系统时钟。 若未使用此选项， 则表示根据系统时钟来更新RTC时间。

--monitor
    与 timesync-status 命令一起使用， 表示监视 systemd-timesyncd.service(8) 的状态并不断刷新输出。可以使用 Ctrl+C 终止监视。

-a, --all
    显示全部的 systemd-timesyncd.service(8) 属性，无论这些属性是否已设置。

-p, --property=
    仅显示指定的 systemd-timesyncd.service(8) 属性。若未指定任何属性则显示全部已设置的属性。 参数必须是一个例如 "ServerName" 这样的属性名称。 可以多次使用此选项，以显示多个属性。

--value
    当使用 show-timesync 命令显示属性时， 仅显示属性的值(不显示"="与属性名称)。

-H, --host=
    操作指定的远程主机。可以仅指定一个主机名(hostname)， 也可以使用 "username@hostname" 格式。 hostname 后面还可以加上 SSH监听端口(以冒号":"分隔)与容器名(以正斜线"/"分隔)， 也就是形如 "hostname:port/container" 的格式， 以表示直接连接到指定主机的指定容器内。 操作将通过SSH协议进行，以确保安全。 可以通过 machinectl -H HOST 命令列出远程主机上的所有容器名称。IPv6地址必须放在方括号([])内。

-M, --machine=
    在本地容器内执行操作。 必须明确指定容器的名称。

-h, --help
    显示简短的帮助信息并退出。

--version
    显示简短的版本信息并退出。

--no-pager
    不将程序的输出内容管道(pipe)给分页程序。
```

## 命令

```
status
    显示系统时钟与RTC的当前状态， 包括时区设置以及网络时间同步服务(也就是 systemd-timesyncd.service)的状态。 注意，此命令并不检查是否存在其他时间同步服务。 如果没有使用任何命令，那么这是默认命令。

show
    以机器可读格式显示与 status 一样的信息。 此命令的输出主要供程序使用， 而 status 命令的输出则是人类易读的格式。

    默认不输出空属性，但可以使用 --all 选项强制输出所有属性。 可以使用 --property= 选项仅输出特定的属性。

set-time [TIME]
    将系统时钟设为指定的时间， 并同时更新RTC时间。 [TIME] 是一个形如 "2012-10-30 18:17:16"的时间字符串。

set-timezone [TIMEZONE]
    设置系统时区， 也就是更新 /etc/localtime 软连接的指向。 可以用下面的 list-timezones 命令列出所有可用时区。 如果RTC被设为本地时间， 此命令还会同时更新RTC时间。 详见 localtime(5) 手册。

list-timezones
    列出所有可用时区，每行一个。 列出的值可以用作前述 set-timezone 命令的参数。

set-local-rtc [BOOL]
    设为 "no" 表示在RTC中存储UTC时间； 设为 "yes" 表示在RTC中存储本地时间。 应该尽一切可能在RTC中存储UTC时间。 尽量不要在RTC中存储本地时间， 因为这会造成一系列麻烦， 尤其是在切换时区以及调整夏令时或冬令时的时候。 注意， 除非明确使用了 --adjust-system-clock 选项， 否则此命令还会同时用系统时钟更新RTC时间。 此命令还会改变 /etc/adjtime 文件第三行的内容，详见 hwclock(8) 手册。

set-ntp [BOOL]
    接受一个布尔值，表示是否开启网络时间同步(若可用)。 设为 yes 表示启用并启动 systemd-timedated.service 中的环境变量 $SYSTEMD_TIMEDATED_NTP_SERVICES 中的第一个存在的服务。 设为 no 表示禁用并停止环境变量 $SYSTEMD_TIMEDATED_NTP_SERVICES 中的所有服务。
```
