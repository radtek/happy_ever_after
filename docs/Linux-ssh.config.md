> 本文主要介绍`ssh config`配置文件中各参数的含义, 这些文件存在的位置: `/etc/ssh/ssh_conf`, `~/.ssh/config`

# ssh配置信息

## 1 配置文件

### 1.1 优先程度

* 1.command-line options
* 2.user's configuration file (`~/.ssh/config`)
* 3.system-wide configuration file (`/etc/ssh/ssh_config`)

### 1.2 配置文件的格式

* **写法**, 以下两种都可以
```sh
config value
config value1 value2
```

```sh
config=value
config=value1 value2
```

* 空行和以`#`开头的行会被忽略；

* 所有的**值区分大小写**，但**参数名不区分**


## 2 `PATTERNs` 和 `TOKENs`

### 2.1 `PATTERNs`

部分配置项中可能会用到pattern, 其规则如下:

* 一个模式由零个或多个非空白字符组成; 

* **`*`**: 匹配任意个任意字符;

    `Host *.co.uk`

* **`?`**: 匹配任意一个字符

    `Host 192.168.0.?`

* **`!`**: 否定运算符

* 一个模式列表由逗号分隔的多个模式组成

    `from="!*.dialup.example.com,*.example.com"`


### 2.2 `TOKENs`

Arguments to some keywords can make use of tokens, which are expanded at runtime:

| Arguments | Meanings |
|  --  | :-- |
| `%%` | A literal '`%`'. |
| `%C` | Shorthand for `%l%h%p%r`. |
| `%d` | Local user's home directory. |
| `%h` | The remote hostname. |
| `%i` | The local user ID. |
| `%L` | The local hostname. |
| `%l` | The local hostname, including the domain name. |
| `%n` | The original remote hostname, as given on the command line. |
| `%p` | The remote port. |
| `%r` | The remote username. |
| `%u` | The local username. |

* **`Match exec`** accepts the tokens `%%`, `%h`, `%L`, `%l`, `%n`, `%p`, `%r`, and `%u`.
* **`CertificateFile`** accepts the tokens `%%`, `%d`, `%h`, `%l`, `%r`, and `%u`.
* **`ControlPath`** accepts the tokens `%%`, `%C`, `%h`, %i, `%L`, `%l`, `%n`, `%p`, `%r`, and` %u`.
* **`HostName`** accepts the tokens `%%` and `%h`.


## 3 标识: `Host`, `Match`

### 3.1 `Host`: 标识一个组

* 标识符, 作为整个组的标识(直到下个`Host`/`Match`出现); 可以理解为名字; 

* 标识符可以有多个, 用空格隔开;

    * 配置两个名字, 分别为`rhel79`和`rhel7`:

    ```sh
    Host rhel-79 rhel-7
        HostName 192.168.1.201
        User root
        Port 22
    ```

    * 可以结合`PATTERN`的运算符号, 写出多种配置; 以下示例表示: **标识符会匹配任何`-79`结尾的字符, 但是不能是`rhel-79`**

    ```sh
    Host *-79 !rhel-79
        HostName 192.168.1.201
        User root
        Port 22
    ```

### 3.2 `Match`: 引入匹配块

> 不常用, 只做介绍

* 支持的关键字:
  * criteria(条件、准则)类: `canonical`, `exec`, `host`, `originalhost`, `user`, and `localuser`
  * `all`

* `exec`: 执行命令返回值为0
* `user`: 匹配到用户
* `host`: 匹配到主机

例1: 如果是来自qwer用户的ssh, 将其由192.168.1.202代理连接: 

```sh
Match User qwer
    ProxyCommand ssh root@192.168.1.202 -W %h:%p
```

```sh
[test@200 ~]$ ssh qwer@192.168.1.201
Last login: Sat May 29 21:39:51 2021 from 192.168.1.202
[qwer@201 ~]$ w
 21:39:51 up  3:53,  1 users,  load average: 0.00, 0.01, 0.05
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
qwer     pts/1    192.168.1.202    21:34    1.00s  0.06s  0.04s w      # <= 此处登陆来自192.168.1.202
```

例2: 如果是来自qwer用户的ssh, 并且IP是192.168.1.开头的, 将其由192.168.1.202代理连接: 

```sh
Match User qwer, Exec "echo %h | grep 192.168.1."
    ProxyCommand ssh root@192.168.1.202 -W %h:%p
```


## 4 常见参数

| 参数名 |  取值[默认值] | 解释 |
|  ---  | --- | :-- |
| `AddKeysToAgent` | `yes,confirm,ask,[no]` | 添加key到ssh agent |
| `AddressFamily`  | `[any],inet,inet6` | address family |
| `BatchMode`      | `yes,[no]` | yes表示不提示输入密码,而是直接失败,避免批处理卡住 |
| `BindAddress`    | `NULL` | `UsePrivilegedPort=yes`时不生效 |
| `CertificateFile` |  | 证书 |
| `CheckHostIP` | `[yes],no` | 检查目标Host key是否因DNS欺骗(spoof)而改变, 并添加到`~/.ssh/known_hosts` |
| `Cipher` | | Specifies the cipher to use for encrypting the session in protocol version 1. |
| `Ciphers` | | Specifies the ciphers allowed for protocol version 2 in order of preference. |
| `Compression` | `yes,[no]` | Specifies whether to use compression. |
| `CompressionLevel` | `1(fast)~9(slow, best)[6]` | the compression level |
| `ConnectionAttempts` | `<Integer>,[1]` | 每秒尝试连接次数 |
| `ConnectTimeout` | `<TCP-TIMEOUT>` | 连接超时时间, 默认使用TCP超时时间 |
| `EscapeChar` | `~` | 设置ssh的逃逸符号(作用可使用`~?`查看) |
| `ForwardAgent` | `yes,[no]` | 设置连接是否经过"认证代理"(如果存在)转发给远程计算机 |
| `ForwardX11` | `yes,[no]` | 设置X11连接是否被自动重定向到安全的通道和显示集(DISPLAY set) |
| `ForwardX11Timeout` | `[20](min)` | 设置不受信的x11连接的超时时间 |
| `ForwardX11Trusted` | `yes,[no]` | 设置是否将x11连接设置为受信(完全访问权限) |
| `GatewayPorts` | `yes,[no]` | 设置是否允许转发端口 |
| `HostKeyAlgorithms` | | 指定期望目标主机提供的algorithms |
| `HostName` | | 主机名/IP |
| `Include` | | Include the specified configuration file(s) |
| `KexAlgorithms` | | Specifies the available KEX (Key Exchange) algorithms |
| `LocalCommand` | | 设定本地执行的命令, 执行正常才发起连接 |
| `LocalForward` | `[bind_address:]port host:hostport` | 本地转发端口, 需要提供两个参数 |
| `LogLevel` | `[INFO]` | QUIET,FATAL,ERROR,INFO,VERBOSE,DEBUG,DEBUG1,DEBUG2,DEBUG3 |
| `MACs` | | Specifies the MAC algorithms in order of preference. |
| `NumberOfPasswordPrompts` | `3` | 设置允许尝试输入密码的次数 |
| `PasswordAuthentication` | `[yes],no` | 是否使用密码认证 |
| `PermitLocalCommand` | `yes,[no]` | 是否允许`LocalCommand`设置的命令执行 |
| `Port` | `22` | ssh连接端口 |
| `PreferredAuthentications` | | 设置认证顺序 |
| `Protocol` | `[2],1` | 设置protocol:可以单独设置1/2,也可以设置2,1顺序 |
| `ProxyCommand` | | Specifies the command to use to connect to the server |
| `PubkeyAcceptedKeyTypes` | | 设置公钥认证支持的类型(逗号分隔)) |
| `PubkeyAuthentication` | `[yes],no` | 是否使用公钥认证 |
| `RemoteForward` | `[bind_address:]port host:hostport` | 远程转发端口, 需要提供两个参数 |
| `RevokedHostKeys` | | 指定撤销的主机公钥(文件);即该文件中的公钥不能用主机认证 |
| `RequestTTY` | `yes,no,force,auto` | Specifies whether to request a pseudo-tty for the session. |
| `RhostsAuthentication` | `[yes],no` | 设置是否使用基于rhosts的安全验证 |
| `RhostsRSAAuthentication` | `yes,[no]` | 设置是否使用用RSA算法的基于rhosts的安全验证 |
| `RSAAuthentication` | `[yes],no` | 设置是否使用RSA认证(仅Protocol 1) |
| `SendEnv` | | 设置发送的环境变量 |
| `ServerAliveCountMax` | `3` | 设置ssh后台发送server alive messages数量 |
| `ServerAliveInterval` | `0` | 设置ssh后台发送server alive messages间隔, 0表示不发送 |
| `StrictHostKeyChecking` | `yes,no,[ask]` | 优先级低于`CheckHostIP` |
| `TCPKeepAlive` | `[yes],no` | 设置是否发送TCP keepalive messages |
| `UpdateHostKeys` | `yes,[no],ask` | 是否允许更新替换host key |
| `UsePrivilegedPort` | `yes,[no]` | Specifies whether to use a privileged port for outgoing connections.|
| `User` | | 用于登陆的用户 |
| `UserKnownHostsFile` | `~/.ssh/known_hosts{,2}` | 设置known_hosts |
| `VerifyHostKeyDNS` | `yes,[no],ask` | 是否通过DNS确认Host key |
| `XAuthLocation` | `/usr/bin/xauth` | Specifies the full pathname of the `xauth` program |

**EXAMPLE:**

```
PubkeyAcceptedKeyTypes +ssh-rsa
Host rhel511
    HostName 192.168.1.51
    User root
    Port 22
    KexAlgorithms diffie-hellman-group1-sha1

Host <name>
    HostName 192.168.1.202
    User <user>
    Port <port>
    ProxyCommand ssh <cloud-user>@<cloud-host> -W %h:%p

name：是一个方便记得本地登录服务器用的名称，自己决定即可
user：登录服务器使用的用户名
Port：映射端口号，一般22
cloud-user:登录跳板机使用的用户名
cloud-host：跳板机的hostname或ip地址
```
