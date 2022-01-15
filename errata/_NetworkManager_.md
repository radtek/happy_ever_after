NetworkManager

1. 配置了team：

当前level 3:         => 切换level 5
disabled  running   网络中断, team0网卡丢失, NetworkManager服务状态=dead
disabled  dead      网络中断, team0网卡丢失, NetworkManager服务状态=dead

enabled running     网络正常, NetworkManager服务状态=running
enabled dead        网络正常, NetworkManager服务状态=running

当前level 5:         => 切换level 3
disabled  running   网络中断, team0网卡丢失, NetworkManager服务状态=dead
disabled  dead      网络中断, team0网卡丢失, NetworkManager服务状态=dead

enabled running     网络正常, NetworkManager服务状态=running
enabled dead        网络正常, NetworkManager服务状态=

2. 配置了bond：
当前level 3:         => 切换level 5
disabled  dead      网络正常
disabled  running   网络正常

3. 无team或bond下
当前level 3:         => 切换level 5
单网卡：网络正常
双网卡：网络正常