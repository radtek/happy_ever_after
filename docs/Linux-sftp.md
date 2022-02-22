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

  
## 4. 案例

实现：
1. 指定专用目录作为sftp目录，读写只在该目录中完成；
2. 用户权限分离，对于允许的用户：部分用户可读写，部分用户只读；对于不允许的用户，不允许读写；
3. 针对后续新增的文件和文件夹，满足条件1


### 4.1 Create users

groupadd -g 1000 sftp_group_rw                   # sftp用户组，该组用户拥有读写权限
groupadd -g 2000 sftp_group_read                 # sftp用户组，该组用户拥有只读权限


useradd -g sftp_group_rw -u 1001 user_rw_01      # 普通sftp用户，拥有读写权限
useradd -g sftp_group_rw -u 1002 user_rw_02      # 普通sftp用户，拥有读写权限

useradd -g sftp_group_read -u 2001 user_read_01  # 只读sftp，拥有读权限
useradd -g sftp_group_read -u 2002 user_read_02  # 只读sftp，拥有读权限

echo 111 | passwd --stdin user_rw_01
echo 111 | passwd --stdin user_rw_02
echo 111 | passwd --stdin user_read_01
echo 111 | passwd --stdin user_read_02


(0)[2022-02-22-21:24:07]# id user_rw_01
uid=1001(user_rw_01) gid=1000(sftp_group_rw) groups=1000(sftp_group_rw)

(0)[2022-02-22-21:24:25]# id user_rw_02
uid=1002(user_rw_02) gid=1000(sftp_group_rw) groups=1000(sftp_group_rw)

(0)[2022-02-22-21:24:26]# id user_read_01
uid=2001(user_read_01) gid=2000(sftp_group_read) groups=2000(sftp_group_read)

(0)[2022-02-22-21:24:31]# id user_read_02
uid=2002(user_read_02) gid=2000(sftp_group_read) groups=2000(sftp_group_read)


### 4.2 Create dir


/data
├── dir01/
│   ├── file01
│   ├── file02
│   └── sub_dir/
│       ├── file03
│       └── file04
├── dir02/
│   ├── file05
│   └── file06
├── file07
└── file08

mkdir -p /data

mkdir -p /data/dir01/sub_dir
touch /data/dir01/file{01,02}
touch /data/dir01/sub_dir/file{03,04}

mkdir -p /data/dir02
touch /data/dir02/file{05,06}

touch /data/file{07,08}


chown root:sftp_group_rw /data
chown -R sftp_admin:sftp_group_rw /data/*

find /data -type 'd' | xargs chmod 770 
find /data -type 'f' | xargs chmod 660 

chmod 750 /data


(0)[2022-02-22-22:07:36]# ls -ld /data
drwxr-x---. 4 root sftp_group_rw 60 Feb 22 21:54 /data
[CENTOS76]root@192.168.161.2:/data
(2)[2022-02-22-22:19:44]# ls -lR /data
.:
total 0
drwxrwx---. 3 sftp_admin sftp_group_rw 49 Feb 22 21:55 dir01
drwxrwx---. 2 sftp_admin sftp_group_rw 34 Feb 22 21:54 dir02
-rw-rw----. 1 sftp_admin sftp_group_rw  0 Feb 22 21:54 file07
-rw-rw----. 1 sftp_admin sftp_group_rw  0 Feb 22 21:54 file08

./dir01:
total 0
-rw-rw----. 1 sftp_admin sftp_group_rw  0 Feb 22 21:55 file01
-rw-rw----. 1 sftp_admin sftp_group_rw  0 Feb 22 21:55 file02
drwxrwx---. 2 sftp_admin sftp_group_rw 34 Feb 22 21:54 sub_dir

./dir01/sub_dir:
total 0
-rw-rw----. 1 sftp_admin sftp_group_rw 0 Feb 22 21:54 file03
-rw-rw----. 1 sftp_admin sftp_group_rw 0 Feb 22 21:54 file04

./dir02:
total 0
-rw-rw----. 1 sftp_admin sftp_group_rw 0 Feb 22 21:54 file05
-rw-rw----. 1 sftp_admin sftp_group_rw 0 Feb 22 21:54 file06


### 4.3 配置

#### 修改sshd_config
[CENTOS76]root@192.168.161.2:~
(0)[2022-02-22-20:55:48]# vim /etc/ssh/sshd_config
# Subsystem     sftp    /usr/libexec/openssh/sftp-server
Subsystem       sftp    internal-sftp
Match Group sftp_group_rw,sftp_group_read
        ChrootDirectory /data
        ForceCommand internal-sftp
        X11Forwarding no
        AllowTcpForwarding no


#### 给 /data 添加acl权限，使 sftp_admin 用户可以修改目录

未修改前，只读用户 user_read_01 正确chroot ，但是无法读取目录下文件，也没有写权限

[CENTOS76]root@192.168.161.2:~
(1)[2022-02-22-22:09:35]# sftp user_read_01@127.0.0.1
user_read_01@127.0.0.1's password: 
Connected to 127.0.0.1.
sftp> pwd
Remote working directory: /
sftp> ls
remote readdir("/"): Permission denied
sftp> mkdir test
Couldn't create directory: Permission denied
sftp> exit

而 读写用户 可以读取文件(注：chroot以后 在 / 下只有读权限，因为系统/data/目录权限为750)，下一级子目录 /dir01 下拥有读写权限(/data/dir01权限770)

[CENTOS76]root@192.168.161.2:/tmp
(0)[2022-02-22-22:27:53]# sftp user_rw_01@127.0.0.1
user_rw_01@127.0.0.1's password: 
Connected to 127.0.0.1.
sftp> ls -l
drwxrwx---    3 1001     1001           49 Feb 22 13:55 dir01
drwxrwx---    2 1001     1001           34 Feb 22 13:54 dir02
-rw-rw----    1 1001     1001            0 Feb 22 13:54 file07
-rw-rw----    1 1001     1001            0 Feb 22 13:54 file08
sftp> mkdir dir03
Couldn't create directory: Permission denied
sftp> cd dir01
sftp> mkdir test_dir
sftp> ls -l
-rw-rw----    1 1001     1001            0 Feb 22 13:55 file01
-rw-rw----    1 1001     1001            0 Feb 22 13:55 file02
drwxrwx---    2 1001     1001           34 Feb 22 13:54 sub_dir
drwxr-xr-x    2 1002     1001            6 Feb 22 14:29 test_dir  # 注意此时创建的文件用户名是1002，组为1001
sftp> exit


#### 给 /data 添加acl权限，使 sftp_group_read 组用户读取/data目录信息


通过 acl 赋予 /data 目录的 r-x 权限给只读用户组 sftp_group_read，保证该组用户正常 chroot，且能看到(list)该目录下文件和目录

修改之前：

[CENTOS76]root@192.168.161.2:~
(0)[2022-02-22-22:07:36]# ls -ld /data
drwxr-x---. 4 root sftp_group_rw 60 Feb 22 21:54 /data

[CENTOS76]root@192.168.161.2:~
(0)[2022-02-22-22:10:05]# getfacl /data
getfacl: Removing leading '/' from absolute path names
# file: data
# owner: root
# group: sftp_group_rw
user::rwx
group::r-x
other::---

修改之后：

[CENTOS76]root@192.168.161.2:~
(0)[2022-02-22-22:10:26]# setfacl -m g:sftp_group_read:r-x /data

[CENTOS76]root@192.168.161.2:~
(0)[2022-02-22-22:13:18]# ls -ld /data
drwxr-x---+ 4 root sftp_group_rw 60 Feb 22 21:54 /data

[CENTOS76]root@192.168.161.2:~
(0)[2022-02-22-22:13:14]# getfacl /data
getfacl: Removing leading '/' from absolute path names
# file: data
# owner: root
# group: sftp_group_rw
user::rwx
group::r-x
group:sftp_group_read:r-x
mask::r-x
other::---

只读用户user_read_01能进入 /data，但无法修改也无法读取任何文件

(0)[2022-02-22-22:21:29]# sftp user_read_01@127.0.0.1
user_read_01@127.0.0.1's password: 
Connected to 127.0.0.1.
sftp> ls -l
drwxrwx---    3 1001     1001           49 Feb 22 13:55 dir01
drwxrwx---    2 1001     1001           34 Feb 22 13:54 dir02
-rw-rw----    1 1001     1001            0 Feb 22 13:54 file07
-rw-rw----    1 1001     1001            0 Feb 22 13:54 file08
sftp> ls -l dir01
remote readdir("/dir01/"): Permission denied
sftp> ls -l dir02
remote readdir("/dir02/"): Permission denied
sftp> get file07
Fetching /file07 to file07
remote open("/file07"): Permission denied
sftp> get file08
Fetching /file08 to file08
remote open("/file08"): Permission denied
sftp> mkdir test
Couldn't create directory: Permission denied

通过 acl 赋予 /data 目录下所有文件 r-- 权限、目录的 r-x 权限给只读用户组 sftp_group_read，保证该组用户正常访问到所有目录及文件，保证可读性

find /data/* -type 'f' | xargs setfacl -m g:sftp_group_read:r--
find /data/* -type 'd' | xargs setfacl -m g:sftp_group_read:r-x

[CENTOS76]root@192.168.161.2:/tmp
(130)[2022-02-22-22:46:29]# sftp user_read_01@127.0.0.1
user_read_01@127.0.0.1's password: 
Connected to 127.0.0.1.
sftp> ls -l
drwxrwx---    4 1001     1001           65 Feb 22 14:29 dir01
drwxrwx---    2 1001     1001           34 Feb 22 13:54 dir02
-rw-rw----    1 1001     1001            0 Feb 22 13:54 file07
-rw-rw----    1 1001     1001            0 Feb 22 13:54 file08
sftp> ls -l dir01
-rw-rw----    1 1001     1001            0 Feb 22 13:55 file01
-rw-rw----    1 1001     1001            0 Feb 22 13:55 file02
drwxrwx---    2 1001     1001           34 Feb 22 13:54 sub_dir
drwxr-xr-x    2 1002     1001            6 Feb 22 14:29 test_dir
sftp> get file07
Fetching /file07 to file07
sftp> get dir01/file01 
Fetching /dir01/file01 to file01
sftp> cd dir01
sftp> mkdir test
Couldn't create directory: Permission denied
sftp> exit

通过 acl 控制只读用户组 sftp_group_read对 /data 目录下新增的文件有r--权限、新增的目录有r-x权限，保证后续可读性

find /data/* -type 'd' | xargs setfacl -d -m g:sftp_group_read:r-x