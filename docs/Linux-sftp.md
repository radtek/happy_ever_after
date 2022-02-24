# 用户限制

> 用户在指定目录, 同时该用户也不能登录该机器。

## 1 修改`/etc/ssh/sshd_config`配置

```
vi /etc/ssh/sshd_config
	#Subsystem      sftp   /usr/libexec/openssh/sftp-server  <===注释这一行
	
	Subsystem	sftp	internal-sftp
	Match User sftpuser01
			ChrootDirectory /data03
			ForceCommand internal-sftp
			X11Forwarding no
			AllowTcpForwarding no
```

- `Match Group sftp` 这一行是指定以下的子行配置是匹配 sftp 用户组的。`Match user userA,userB` 则是匹配用户。

- `ChrootDirectory /data/sftp/%u` 设定属于用户组 sftp 的用户访问的根文件夹。`%h` 代表用户 home 目录, `%u` 代表用户名。

- `ForceCommand internal-sftp` 该行强制执行内部 sftp, 并忽略任何 ~/.ssh/rc 文件中的命令。

- `AllowTcpForwarding no` 是否允许 TCP 转发, 默认值为 "yes",  禁止 TCP 转发并不能增强安全性, 除非禁止了用户对 shell 的访问, 因为用户可以安装他们自己的转发器。

- `X11Forwarding no` 是否允许进行 X11 转发。默认值是 "no", 设为 "yes" 表示允许。如果允许 X11 转发并且 sshd(8)代理的显示区被配置为在含有通配符的地址(`X11UseLocalhost`)上监听。那么将可能有额外的信息被泄漏。由于使用 X11 转发的可能带来的风险, 此指令默认值为"no"。需要注意的是, 禁止X11转发并不能禁止用户转发 X11 通信, 因为用户可以安装他们自己的转发器。


## 2 配置目录的权限

```
ll /data03 -d
drwxr-x---    10 root root    118784  12月 31 17:17 /data03
```

目录权限设置上要遵循2点：
- `ChrootDirectory` 设置的根目录权限及其所有的上级文件夹权限, 属主和属组必须是 root (经测试, 配置属主为root即可)
- `ChrootDirectory` 设置的根目录权限及其所有的上级文件夹权限, 只有属主能拥有写权限, 权限最大设置只能是 755。

## 3 其他

* 多个用户/组受到同一约束时, 可以将多个用户/组写在一起(Match 的写法可参考 ssh_config(5))

    ```sh
    Subsystem	sftp	internal-sftp
    Match User sftpuser01, sftpuser02
            ChrootDirectory /data03
            ForceCommand internal-sftp
            X11Forwarding no
            AllowTcpForwarding no
    ```

* Match

The arguments to Match are one or more criteria-pattern pairs or the single token All which matches all criteria.  The available criteria are User, Group, Host, LocalAddress, LocalPort, and Address.  The match patterns may consist of single entries or comma-separated lists and may use the wildcard and negation operators described in the PATTERNS section of ssh_config(5).

Available keywords are: 
AcceptEnv, AllowAgentForwarding, AllowGroups, AllowStreamLocalForwarding, AllowTcpForwarding, AllowUsers, AuthenticationMethods, AuthorizedKeysCommand, AuthorizedKeysCommandUser, AuthorizedKeysFile, AuthorizedPrincipalsCommand, AuthorizedPrincipalsCommandUser, AuthorizedPrincipalsFile, Banner, ChrootDirectory, ClientAliveCountMax, ClientAliveInterval, DenyGroups, DenyUsers, ForceCommand, GatewayPorts, GSSAPIAuthentication, HostbasedAcceptedKeyTypes, HostbasedAuthentication, HostbasedUsesNameFromPacketOnly, IPQoS, KbdInteractiveAuthentication, KerberosAuthentication, KerberosUseKuserok, MaxAuthTries, MaxSessions, PasswordAuthentication, PermitEmptyPasswords, PermitOpen, PermitRootLogin, PermitTTY, PermitTunnel, PermitUserRC, PubkeyAcceptedKeyTypes, PubkeyAuthentication, RekeyLimit, RevokedKeys, StreamLocalBindMask, StreamLocalBindUnlink, TrustedUserCAKeys, X11DisplayOffset, X11MaxDisplays, X11Forwarding and X11UseLocalHost.

## 4. 案例

实现：

> 1. 指定专用目录作为sftp目录, 读写只在该目录中完成；
> 2. 用户权限分离, 对于允许的用户：部分用户可读写, 部分用户只读；对于不允许的用户, 不允许读写；
> 3. 针对后续新增的文件和文件夹, 满足条件1


* 创建案例中使用用户组

    ```sh
    groupadd -g 1000 sftp_group_rw    # sftp用户组, 该组用户拥有读写权限
    groupadd -g 2000 sftp_group_read  # sftp用户组, 该组用户拥有只读权限
    ```

* 创建目录

    例如使用如下目录结构时:

    ```text
    /data/
    ├── dir01/
    │   ├── file01
    │   ├── file02
    │   ├── sub_dir/
    │   │   ├── file03
    │   │   └── file04
    │   └── test_dir/
    ├── dir02/
    │   ├── file05
    │   └── file06
    ├── file07
    └── file08
    ```


    ```sh
    mkdir -p /data

    mkdir -p /data/dir01/sub_dir
    touch /data/dir01/file{01,02}
    touch /data/dir01/sub_dir/file{03,04}

    mkdir -p /data/dir02
    touch /data/dir02/file{05,06}

    touch /data/file{07,08}
    ```

* 修改目录权限:
  
    * /data 目录: 属主: `root`, 属组: `sftp_group_rw`, 权限: `750`
    * /data 下
        * 目录: 属主: `<USERNAME>`, 属组: `sftp_group_rw`, 权限: `775`
        * 文件: 属主: `<USERNAME>`, 属组: `sftp_group_rw`, 权限: `664`

    ```sh
    chown root:sftp_group_rw /data
    chmod 750 /data

    chown -R <USERNAME>:sftp_group_rw /data/*
    find /data/* -type 'd' | xargs chmod 775 
    find /data/* -type 'f' | xargs chmod 664 
    ```

* 修改 sshd_config

    ```sh
    ~] vim /etc/ssh/sshd_config
    # Subsystem     sftp    /usr/libexec/openssh/sftp-server
    Subsystem       sftp    internal-sftp
    Match Group sftp_group_rw
            ChrootDirectory /data
            ForceCommand internal-sftp -u 0002 -m 664
            X11Forwarding no                         
            AllowTcpForwarding no
    Match Group sftp_group_read
            ChrootDirectory /data
            ForceCommand internal-sftp -R
            X11Forwarding no
            AllowTcpForwarding no
    ```

    注:

    * `-u 0002 -m 664`: 指定用户的umask和新创建文件的权限, 可以保证新创建目录权限775, 新创建文件权限664
    * `-R`: 开启只读模式
    * 经测试, 通过put -r递归上传的目录, 权限与源目录一致, 不受 "`-u`" 配置影响; 文件却会受 "`-m`" 影响

* 修改目录 acl 及 SGID

    ```sh
    ~] setfacl -m g:sftp_group_read:r-x /data
    ~] chmod g+s /data

    ~] ls -ld /data
    drwxr-x---+ 4 root sftp_group_rw 60 Feb 22 21:54 /data

    ~] getfacl /data
    getfacl: Removing leading '/' from absolute path names
    # file: data
    # owner: root
    # group: sftp_group_rw
    # flags: -s-
    user::rwx
    group::r-x
    group:sftp_group_read:r-x
    mask::r-x
    other::---
    ```


=== END ===