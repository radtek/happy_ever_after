```
# /usr/lib/systemd/system/docker.service
[Unit]
Description=Docker Application Container Engine
Documentation=https://docs.docker.com
After=network-online.target firewalld.service
Wants=network-online.target

[Service]
Type=notify
EnvironmentFile=-/etc/sysconfig/docker
EnvironmentFile=-/etc/sysconfig/docker-storage
EnvironmentFile=-/etc/sysconfig/docker-network
Environment=GOTRACEBACK=crash

ExecStart=/usr/bin/dockerd $OPTIONS \
                           $DOCKER_STORAGE_OPTIONS \
                           $DOCKER_NETWORK_OPTIONS \
                           $INSECURE_REGISTRY
ExecReload=/bin/kill -s HUP $MAINPID
LimitNOFILE=1048576
LimitNPROC=1048576
LimitCORE=infinity
# set delegate yes so that systemd does not reset the cgroups of docker containers
Delegate=yes
# kill only the docker process, not all processes in the cgroup
KillMode=process

[Install]
WantedBy=multi-user.target
```



EnvironmentFile：许多软件都有自己的环境参数文件，该字段指定文件路径
> 注意：/etc/profile 或者 /etc/profile.d/ 这些文件中配置的环境变量仅对通过 pam 登录的用户生效，而 systemd 是不读这些配置的。
systemd 是所有进程的父进程或祖先进程，它的环境变量会被所有的子进程所继承，如果需要给 systemd 配置默认参数可以在 /etc/systemd/system.conf  和 /etc/systemd/user.conf 中设置。
加载优先级 system.conf 最低，可能会被其他的覆盖。


Type：定义启动类型。可设置：simple，exec，forking，oneshot，dbus，notify，idle
simple(设置了 ExecStart= 但未设置 BusName= 时的默认值)：ExecStart 字段启动的进程为该服务的主进程
forking：ExecStart 字段的命令将以 fork() 方式启动，此时父进程将会退出，子进程将成为主进程


ExecStart：定义启动进程时执行的命令
上面的例子中，启动 sshd 执行的命令是 /usr/sbin/sshd -D $OPTIONS，其中的变量 $OPTIONS 就来自 EnvironmentFile 字段指定的环境参数文件。类似的，还有如下字段：
ExecReload：重启服务时执行的命令
ExecStop：停止服务时执行的命令
ExecStartPre：启动服务之前执行的命令
ExecStartPost：启动服务之后执行的命令
ExecStopPost：停止服务之后执行的命令


RemainAfterExit：设为yes，表示进程退出以后，服务仍然保持执行


KillMode：定义 Systemd 如何停止服务，可以设置的值如下：
control-group（默认值）：当前控制组里面的所有子进程，都会被杀掉
process：只杀主进程
mixed：主进程将收到 SIGTERM 信号，子进程收到 SIGKILL 信号
none：没有进程会被杀掉，只是执行服务的 stop 命令


Restart：定义了退出后，Systemd 的重启方式。可以设置的值如下：
no（默认值）：退出后不会重启
on-success：只有正常退出时（退出状态码为0），才会重启
on-failure：非正常退出时（退出状态码非0），包括被信号终止和超时，才会重启
on-abnormal：只有被信号终止和超时，才会重启
on-abort：只有在收到没有捕捉到的信号终止时，才会重启
on-watchdog：超时退出，才会重启
always：不管是什么退出原因，总是重启


RestartSec：表示 Systemd 重启服务之前，需要等待的秒数









# systemd.service

systemd.service — 服务单元配置



## 描述

以 "`.service`" 为后缀的单元文件， 封装了一个被 systemd 监视与控制的进程。

本手册列出了所有专用于此类单元的 配置选项(亦称"配置指令"或"单元属性")。 [systemd.unit(5)](http://www.jinbuguo.com/systemd/systemd.unit.html#) 中描述了通用于所有单元类型的配置选项， 它们位于 "`[Unit]`" 与 "`[Install]`" 小节。 此类单元专用的配置选项 位于 "`[Service]`" 小节。

其他可用的选项参见 [systemd.exec(5)](http://www.jinbuguo.com/systemd/systemd.exec.html#) 手册(定义了命令的执行环境)， 以及 [systemd.kill(5)](http://www.jinbuguo.com/systemd/systemd.kill.html#) 手册(定义了如何结束进程)， 以及 [systemd.resource-control(5)](http://www.jinbuguo.com/systemd/systemd.resource-control.html#) 手册(定义了进程的 资源控制)。

如果要求启动或停止的某个单元文件 不存在， systemd 将会寻找同名的SysV初始化脚本(去掉 `.service` 后缀)， 并根据那个同名脚本， 动态的创建一个 service 单元。 这主要用于与传统的SysV兼容(不能保证100%兼容)。 更多与SysV的兼容性可参见 [Incompatibilities with SysV](https://www.freedesktop.org/wiki/Software/systemd/Incompatibilities) 文档。