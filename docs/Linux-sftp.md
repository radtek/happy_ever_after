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

- `ChrootDirectory /data/sftp/%u` 设定属于用户组 sftp 的用户访问的根文件夹。`%h` 代表用户 home 目录，`%u` 代表用户名。

- `ForceCommand internal-sftp` 该行强制执行内部 sftp，并忽略任何 ~/.ssh/rc 文件中的命令。

- `AllowTcpForwarding no` 是否允许 TCP 转发，默认值为 "yes"， 禁止 TCP 转发并不能增强安全性，除非禁止了用户对 shell 的访问，因为用户可以安装他们自己的转发器。

- `X11Forwarding no` 是否允许进行 X11 转发。默认值是 "no"，设为 "yes" 表示允许。如果允许 X11 转发并且 sshd(8)代理的显示区被配置为在含有通配符的地址(`X11UseLocalhost`)上监听。那么将可能有额外的信息被泄漏。由于使用 X11 转发的可能带来的风险，此指令默认值为"no"。需要注意的是，禁止X11转发并不能禁止用户转发 X11 通信，因为用户可以安装他们自己的转发器。


## 2 配置目录的权限

```
ll /data03 -d
drwxr-x---    10 root root    118784  12月 31 17:17 /data03
```

目录权限设置上要遵循2点：
- `ChrootDirectory` 设置的根目录权限及其所有的上级文件夹权限，属主和属组必须是 root (经测试，配置属主为root即可)
- `ChrootDirectory` 设置的根目录权限及其所有的上级文件夹权限，只有属主能拥有写权限，权限最大设置只能是 755。

## 3 其他

* 多个用户/组受到同一约束时，可以将多个用户/组写在一起(Match 的写法可参考 ssh_config(5))

  ```sh
  Subsystem	sftp	internal-sftp
  Match User sftpuser01, sftpuser02
  		ChrootDirectory /data03
  		ForceCommand internal-sftp
  		X11Forwarding no
  		AllowTcpForwarding no
  ```

  

* 