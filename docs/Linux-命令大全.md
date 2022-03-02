# Linux-命令大全

<span id = "Jump1" ></span>

<sup><p align="right">[`END↓`](#Jump2)</p></sup>


# 目录

<!-- content -->

* [pwd cd](#pwd-cd)
* [touch](#touch)
* [tree](#tree)
* [ls](#ls)
* [expr](#expr)
* [bc](#bc)
* [rm](#rm)
* [tr](#tr)
* [find](#find)
* [xargs](#xargs)
* [tar](#tar)
* [seq](#seq)
* [xfs_info dumpe2fs](#xfs_info-dumpe2fs)
* [basename dirname readlink](#basename-dirname-readlink)
    * [basename](#basename)
    * [dirname](#dirname)
    * [readlink](#readlink)
* [cp mv install namei](#cp-mv-install-namei)
    * [cp](#cp)
    * [mv](#mv)
    * [install](#install)
    * [namei](#namei)
* [cat](#cat)
* [cut](#cut)
* [sort](#sort)
* [wc](#wc)
* [e2label xfs_admin](#e2label-xfs_admin)
    * [e2label](#e2label)
    * [xfs_admin](#xfs_admin)
* [losetup](#losetup)
* [rpm](#rpm)
* [top](#top)
* [ps](#ps)
* [nice renice](#nice-renice)
* [kill](#kill)
* [lsattr chattr](#lsattr-chattr)
* [getfacl setfacl](#getfacl-setfacl)
* [User and Password](#user-and-password)
    * [/etc/passwd](#passwdJump)
    * [/etc/shadow](#shadowJump)
    * [/etc/group](#groupJump)
    * [/etc/default/useradd](#useraddJump)
    * [useradd](#useradd)
    * [usermod](#usermod)
    * [chsh](#chsh)
    * [chfn](#chfn)
    * [passwd](#passwd)
    * [pwconv](#pwconv)
    * [pwunconv](#pwunconv)
* [test](#test)
* [typeset,declare](#typeset)
* [fdisk,parted](#fdisk)

<br>

## pwd cd

<sup><p align="right">[`TOP`](#Jump1)</p></sup>


`-L`, `--logical`  
`-P`, `--physical`   

<br>

## touch

<sup><p align="right">[`TOP`](#Jump1)</p></sup>

| 参数            | 解释 |
| --------------- | ---------- |
| `-a`,-m            | touch会刷新文件的access、modify、change时间，使用`-a`,`-m`只修改access或modify时间(change时间一定会改变) |
| `-c`, --no-create  | touch默认创建不存在的文件，使用该参数不创建(注：此时命令的状态返回值依然是0) |
| `-d`,--date=STRING | `-d`和`-t`都是可以指定时间替换当前文件的时间，其中`-d`可以用的格式比较随意，而-t的格式要求为 |
| `-t` STAMP         | [[CC]YY]MMDDhhmm[.ss] |
| `-h`               | touch动作默认只影响符号链接的源文件，指定-h则只影响链接本身 |
| `-r` FILE          | 引用FILE的时间属性(只是access、modify时间，change时间依旧是当前) |

<br>

## tree

<sup><p align="right">[`TOP`](#Jump1)</p></sup>

| 参数      |解释 |
| --------- |------ |
| `-a`      |显示所有文件 all |
| `-d`      |只显示目录 directory |
| `-f`      |显示全路径 full path |
| `-i`      |不显示树枝，与 -f 搭配使用比较合适 |
| `-L` N    |往下遍历显示的最大层数N |
| `-F`      |给各类型文件的结尾加上特定的标识符( ls -F ) |
| `-X`      |XML格式输出 |

<br>

## ls

<sup><p align="right">[`TOP`](#Jump1)</p></sup>

| 参数      |解释 |
| --------- |------ |
| `-a`      |显示所有文件 |
| `-l`      |长格式显示文件信息 |
| `-h`      |  |
| `-R`      |递归列出 |
| `-i`      |显示inode |
| `-s`      |size print the allocated size of each file, in blocks |
| `-d`      |显示目录本身而不是目录下的文件 |
| `-p`, `-F`  |指定`-p`，目录后面会加上 "/"" ; 指定`-F`，可执行的普通文件"*"，目录"/"，符号链接"@"，命令管道FIFO "|" ，sockets套接字 "=" |
| `-Z`        |`-Z`，显示context |
| `-c`,`-u`   |都是排序：`-ltc`根据ctime排序并显示ctime，`-lc`显示ctime但按名称排序，其他，按ctime排序；`-u`同理，atime |
| `-t`,`-X`,`-r`    |`-t`根据mtime，-X根据扩展名，-r逆序  (默认排序：按文件名递增)  eg. ls -lt --time-style=long-iso   |
| `--color={}`      |`never` 不显示；`always` 总是显示；`auto` 自动显示 |
| `--full-time`     |显示完整时间 |
| `--time-style={}` |设置显示的时间格式，`full-iso`，`long-iso`，`iso`，`locale` |
| `--time={}`       |显示时间修改为atime或ctime |



查看最近修改的文件(在最下方显示):

```sh
ls -lirt 
```

修改显示格式，排序规则:

```sh
ls -lt --time-style=long-iso 
```

<br>

## expr

<sup><p align="right">[`TOP`](#Jump1)</p></sup>

```sh
expr 3 + 4
```

```sh
expr length "this is a test"
```

```sh
expr substr "this is a test" 3 5
```

```sh
expr index "this is a test" "a"
```

<br>

## bc

<sup><p align="right">[`TOP`](#Jump1)</p></sup>

```sh
echo "4 * 0.56" | bc
```

```sh
no=54
result=`echo "$no * 1.5"| bc`
```

```sh
echo "scale=2;3/8" | bc
```

进制转换：

```sh
no1=100
echo "obase=2;$no1" | bc
no2=01100100
echo "obase=10;ibase=2;$n2" | bc
```

平方及平方根：

```sh
echo "sqrt(100)" | bc
echo "10^10" | bc
```

<br>

## rm

<sup><p align="right">[`TOP`](#Jump1)</p></sup>

> 删除一个目录下所有文件，但保留一个指定文件

    ```sh
    for i in {1..10};do touch file$i;done
    ```

- 方法1

    ```sh
    find /xxdir -type f ! -name "file10" -exec rm -f {} \;
    ```

- 方法2

    ```sh
    find /xxdir -type f ! -name "file10" | xargs rm -f
    ```

- 方法3

    ```sh
    rsync -az --delete --exclude "file10" /null /xxdir
    ```

- 方法4

    ```sh
    #开启bash的extglob功能(此功能的作用就是用rm !(*jpg)这样的方式来删除不包括号内文件的文件)
    shopt -s extglob;  
    rm -f !(file10)
    ```

- 方法5

    ```sh
    find . -type f | grep -v 'file10' |xargs rm -f 
    ```

- 方法6

    ```sh
    rm -f `ls | grep -v 'file10'`
    ```

<br>

## tr 

<sup><p align="right">[`TOP`](#Jump1)</p></sup>

将SET1中的字符一一对应替换成SET2

```sh
tr [OPTION] … SET1 [SET2]
```

| 参数      |解释 |
| --------- |------ |
| `-C`, `-c`, `--complement`      |use the complement of SET1 ：取代所有不属于第一字符集的字符 注：使用此参数时，换行符也会被替换 |
| `-d`, `--delete`             |删除所有属于第一字符集的字符 |
| `-s`, `--squeeze-repeats`    |把连续重复的字符以单独一个字符表示 |
| `-t`, `--truncate-set1`      |先删除第一字符集较第二字符集多出的字符，然后两个字符集匹配替换 |

`CHAR1-CHAR2` ：all characters from CHAR1 to CHAR2 in ascending order

`[CHAR*]` ：in SET2, copies of CHAR until length of SET1 (CHAR只能是单个字符)

`[CHAR*REPEAT]`  ：**REPEAT** copies of **CHAR**, **REPEAT** octal if starting with 0 (CHAR只能是单个字符)


可使用的字符类:  

- `[:alnum:]` 
- `[:alpha:]` 
- `[:digit:]` 
- `[:lower:]` 
- `[:upper:]` 
- `[:space:]`
- `[:cntrl:]` 控制（非打印）字符
- `[:graph:]` 图形字符
- `[:print:]` 可打印字符
- `[:punct:]` 标点符号
- `[:xdigit:]` 十六进制字符

<br>

## find

<sup><p align="right">[`TOP`](#Jump1)</p></sup>

```sh
find [查找路径] [查找标准] [查找到以后的处理动作]
```

### (1) 查找路径

默认为当前目录

### (2) 查找标准

默认指定路径下的所有文件


参数                    |解释
---------               |------
`-name, -iname FILENAME`  |支持文件名通配
`-regex PATTERN`          |基于正则表达式进行文件名匹配
`-user USERNAME`          |
`-group GROUPNAME`        |
`-uid UID`                |
`-gid GID`                |
`-nouser`                 |
`-nogroup`                |
`-size [+|-]`            |#KMG
`-o|-a|-not(!)`         |多个条件的连接方式：or/and/not
`-mtime,-ctime,-atime [+|-]NUMBER`    |默认:天
`-mmin,-cmin,-amin [+|-]NUMBER`       |分钟
`-type  f|d|c|b|l|p|s`                |`c`     字符设备：串行端口的接口设备，如鼠标、键盘<br>`b` 块设备文件：存储数据以供系统存取的接口设备，如硬盘
`-perm MODE`            |査找文件权限刚好等于"权限模式"的文件
`-perm -MODE`            |査找文件权限全部包含"权限模式"的文件
`-perm +MODE`            |査找文件权限包含"权限模式"的任意一个权限的文件


### (3) 查找操作

默认为显示

参数     | 解释
------   | ------
`-print` | 
`-print0`| 行结束符不再是\n，而是一个不可见的字符，可搭配`xargs -0`使用
`-ls` | 
`-ok COMMAND {} \;`   | 执行操作需要确认
`-exec COMMAND {} \;` | 执行操作不需要确认<br>**注**：`{}` 指代前面 find 命令查找到的文件或目录

<br>

## xargs

<sup><p align="right">[`TOP`](#Jump1)</p></sup>

**将标准输入转换成命令行参数**


参数  |解释
----- |------
`-a file` | 从文件中读取，而不是从标准输出
`-d`      | 自定义分隔符，默认为空格
`-n N`    | 指定每行最大参数量，可以将标准输出的文本划分为多行，每行N个参数。默认分隔符为空格
`-i`      | 以 `{}` 指代前面的结果（从标准输入）:  `# find . -name "*.log" | xargs -i mv {} dir1/`
`-I`      | 指定一个符号用以指代前面的结果，而不是用`{}` :  `# find . -name "file*" | xargs -I [] cp [] dir2`
`-0`      | 参考以下示例

示例：  

```sh
$ touch 'a b.txt'
$ find . -name "*b.txt" | xargs /bin/rm 
/bin/rm: cannot remove ‘./a’: No such file or directory
/bin/rm: cannot remove ‘b.txt’: No such file or directory

$ find . -name "*b.txt" -print0 |xargs -0 /bin/rm 
```

<br>

## tar

<sup><p align="right">[`TOP`](#Jump1)</p></sup>

### (1) 独立命令

参数  |解释
----- |------
`-c` | 建立归档
`-x` | 解压
`-t` | 查看归档内容
`-r` | 向归档的末尾追加文件 `tar -rvf bbbb.tar.gz ./tmp2`
`-u` | 更新归档中的文件     `tar -uvf a.tar ./txt1` **注**：若txt1文件有变化，则a.tar中会有两份txt1，原txt1也会保留在a.tar中，但解压时默认解压最新的
`--delete` | 从归档中删除文件  `tar -f a.tar  --delete ./txt1`

### (2) 压缩

参数  | 解释
----- |------
`-z` | 有gzip属性
`-j` | 有bzip2属性
`-J` | 有xz属性
`-Z` | 有compress属性

### (3) overwrite control

参数  | 解释
----- |------
`--keep-old-files`        | don't replace existing files when extracting, treat them as errors
`--keep-newer-files`     | don't replace existing files that are newer than their archive copies
`--overwrite`             | overwrite existing files when extracting
`--remove-files`          | remove files after adding them to the archive
`--skip-old-files`        | don't replace existing files when extracting, silently skip over them

### (4) 其他

参数  | 解释
----- |------
`-p`, `--preserve`              |   保留权限
`-C`                             |   change to directory DIR
`--exclude=PATTERN`              |   exclude files, given as a PATTERN (不能用正则表达式匹配，只能用通配符)
`-T`, `--files-from=FILE`       |   get names to extract or create from FILE
`-h`, `--dereference`           |   follow symlinks; archive and dump the files they point to
`--hard-dereference`              |   follow hard links
`-N` 日期                         | 仅打包比指定日期新的文件，可用于增量备份
`-X`, `--exclude-from=FILE`         |  exclude patterns listed in FILE


### (5) 对tar包加密/解密

```sh
# 加密
tar -zcvf - ./tmp1 | openssl des3 -salt -k 123qweQ | dd of=tmp.tgz.des3

# 解密
dd if=tmp.tgz.des3 | openssl des3 -d -k 123qweQ | tar zxf - 
```

<br>

## seq

<sup><p align="right">[`TOP`](#Jump1)</p></sup>

**产生整数**

```sh
seq [选项]... [首数 [增量]] 尾数
```

参数  |解释
----- |------
`-f`, `--format=`    | 设置显示格式 `seq -f str%03g 1` => str001<br>`%`:表示格式设定开始,默认是`%g`; `03`:不足3位时, 用0补全显示3位; `%-3g`: -表示左对齐
`-s`, `--separator=` | 使用指定字符串分隔数字（默认使用：\n）
`-w`, `--equal-width` | 在列前添加0使得宽度相同 (**注**不能和-f一起用)

```sh
$ seq -f"%03g" 9 11
009
010
011

$ seq -f"str%03g" 9 11
str009
str010
str011
```

```sh
$ seq -s" " -f"str%03g" 9 11
str009 str010 str011

#要指定\t做为分隔符号
$ seq -s"`echo -e "\t"`" 9 11
9	10	11
```

<br>

## xfs_info dumpe2fs

<sup><p align="right">[`TOP`](#Jump1)</p></sup>

`xfs_info`针对xfs系统  
`dumpe2fs`针对ext3,ext4

![Picture][Picture1]

- `isize` : inode的容量，这里为512bytes。
- `agcount`：储存区群组的个数，这里有4个。
- `agsize` : 每个储存区群组里的block个数，这里为1113856个。
- `sectsz`：逻辑扇区（sector）的容量，这里为512bytes。连续八个 sector组成一个 block
- `bsize`：每个block的容量为4 kb。
- `blocks`：共有4455424个block在这个文件系统内。
- `sunit`,`swidth`：与磁盘阵列的stripe相关性较高
- `internal`，指这个登录区的位置在文件系统内，而不是外部系统的意思，占用了4K * 2560空间。
- 第9行：`realtime`区域，extent容量为4k，none=>不过目前没有使用。

<br>

## basename dirname readlink

<sup><p align="right">[`TOP`](#Jump1)</p></sup>

### basename 

**取文件名**

```sh
basename NAME [SUFFIX]
```

参数  |解释
----- |------
`-a` | 同时取多个路径的文件名
`-s` | 指定文件后缀（获取时自动去掉）
`-z` | 取多个文件名时，不换行也没有空格(默认是换行) *separate output with NUL rather than newline*

示例:  

```sh
$ basename -a /root/a /root/b
a
b
```


### dirname

**取路径**

- `-z` 取多个路径时，不换行也没有空格(默认是换行) separate output with NUL rather than newline


### readlink

**后面接符号链接，以获取该符号链接的文件或目录**  

```sh
$ readlink /usr/bin/ypdomainname 
hostname

$ ll /usr/bin/ypdomainname 
lrwxrwxrwx. 1 root root 8 May 20 23:55 /usr/bin/ypdomainname -> hostname
```

<br>

## cp mv install namei

<sup><p align="right">[`TOP`](#Jump1)</p></sup>

### cp

- `-i`: interactive overwrite前提示
- `-r`, `-R`: 递归复制文件夹
- `-p`, `--preserve=`: 保留特殊属性(default: mode,ownership,timestamps) additional attributes: context, links, xattr, all
- `-a`, `-dR --preserve=ALL`
- `-d`, `--no-dereference --preserve=links`:

### mv 

```sh
mv DEST SRC
mv -f # force直接覆盖，不提示
mv -t DEST SRC
```

### install

install ::copy file and set attributes, 复制后默认有执行权限：`rwxr-xr-x`

```sh
install -d: 类似于mkdir -p  
install -t DEST SRC  
install -m --mode=Mode  
install -o -owner=OWNER  
```

### namei

显示目录信息

- `-m` : 显示权限
- `-o` : 显示属组和属主
- `-v` : vertical垂直对齐模式
- `-l` : =-mov
- `-n` : 不跟随符号链接
- `-x` : 以D显示挂载点

<br>

## cat

<sup><p align="right">[`TOP`](#Jump1)</p></sup>

- `-n` : 显示行号
- `-E` : 显示行结束符 $ （windows结束符是$\n）
- `-T` : TAB显示为^T
- `-A` : =`-vET`

<br>

## cut

<sup><p align="right">[`TOP`](#Jump1)</p></sup>

- `-d` : 定义字段的分割符，默认是TAB (delimeter)
- `-f` : 输出指定的字段 (field): "-f1，-f1-3，-f1,3"
- `-b` : 输出指定位置的字节(byte)
- `-c` : 输出指定位置的字符(character)，与`-b` 的区别表现在处理非英文字符时 "-c 3-5", "-c 8-"

<br>

## sort

<sup><p align="right">[`TOP`](#Jump1)</p></sup>

- `-u` : 去除重复的行
- `-n`,`-h` : 按照数值排序，从小到大
- `-t`,`--field-separator` : 指定分割符 
- `-k` : 指定排序的字段
- `-r` : 逆序

```sh
$ ls -lh /etc/ | tail -n 4 | sort -k5,5n  #指定按第5列排序，且只按第5列，k5表示按5-最后列的值排序
drwxr-xr-x.  2 root root 4.0K Mar 27 15:15 yum.repos.d
drwxr-xr-x.  5 root root 4.0K Mar 12 04:07 yum
-rw-r--r--.  1 root root  585 Mar 10  2016 yp.conf
-rw-r--r--.  1 root root  813 Dec  7  2016 yum.conf

$ ls -lh /etc/ | tail -n 4 | sort -k5,5h	#-n 参数没法处理K, M, G等单位字符，这个时候可以使用-h 参数
-rw-r--r--.  1 root root  585 Mar 10  2016 yp.conf
-rw-r--r--.  1 root root  813 Dec  7  2016 yum.conf
drwxr-xr-x.  2 root root 4.0K Mar 27 15:15 yum.repos.d
drwxr-xr-x.  5 root root 4.0K Mar 12 04:07 yum

$ head -4 /etc/passwd | sort -t: -k7,7				#指定分隔符
root:x:0:0:root:/root:/bin/bash
adm:x:3:4:adm:/var/adm:/sbin/nologin
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin

$ head -4 /etc/passwd | sort -t: -k7,7 -k3,3n		#按第七列排序后，相同的值再按第三列数值排序
root:x:0:0:root:/root:/bin/bash
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
adm:x:3:4:adm:/var/adm:/sbin/nologin

$ head -4 /etc/passwd | sort -t: -k7,7 -k3,3nr			#只在第3列颠倒排序
root:x:0:0:root:/root:/bin/bash
adm:x:3:4:adm:/var/adm:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
bin:x:1:1:bin:/bin:/sbin/nologin

$ head -4 /etc/passwd | sort -t: -k7,7r -k3,3nr			#同时颠倒
adm:x:3:4:adm:/var/adm:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
bin:x:1:1:bin:/bin:/sbin/nologin
root:x:0:0:root:/root:/bin/bash
```

<br>

## wc

print newline, word, and byte counts for each file

- `-c` `--bytes`
- `-l` `--lines`
- `-L` `--max-line-length`
- `-m` `--chars`
- `-w` `--words`

<br>

## e2label xfs_admin

<sup><p align="right">[`TOP`](#Jump1)</p></sup>

### e2label

`ext2`/`ext3`/`ext4`文件系统

```x
e2label device [ new-label ]
```

### xfs_admin

> change parameters of an XFS filesystem

`xfs`文件系统

- `-L` LABEL : 设置文件系统的label  
- `-l` : 查看当前文件系统的label  
- `–U` UUID : 设置文件系统的UUID 
- `-u` : 查看当前文件系统的UUID  


```sh
$ xfs_admin -L sdb1 /dev/sdb1
writing all SBs
new label = "sdb1"
```

```sh
$ xfs_admin -l /dev/sdb1
label = "sdb1"
```

```sh
$ xfs_admin -u /dev/sdb1
UUID = 4c5f9591-53ff-48cb-8e8c-372dc92171eb
```

<br>

## losetup

<sup><p align="right">[`TOP`](#Jump1)</p></sup>

- Get info:

    ```sh
    losetup loopdev
    losetup -l [-a]
    losetup -j file [-o offset]
    ```

- Delete loop:

    ```sh
    losetup -d loopdev...
    ```

- Delete all used loop devices:

    ```sh
    losetup -D
    ```

- Print name of first unused loop device:

    ```sh
    losetup -f
    ```

- Setup loop device:

    ```sh
    losetup [-o offset] [--sizelimit size]
            [-p pfd] [-rP] {-f[--show]|loopdev} file
    ```

- Resize loop device:

    ```sh
    losetup -c loopdev
    ```

创建空白的二进制文件，并把它和一个loop设备建立映射关系

```sh
head -c 300m /dev/zero > /tmp/diskfile.bin
losetup /dev/loop1 /tmp/diskfile.bin        #映射
losetup /dev/loop1                          #查看
mount /dev/loop1 /mnt                       #挂载
umount /mnt 
losetup -d /dev/loop1                       #删除
```

<br>

## rpm  

<sup><p align="right">[`TOP`](#Jump1)</p></sup>

```x
rpm -ivh xxx.rpm                             #install verbose hash
rpm -ivh --force xxx.rpm                     #强制安装
rpm -e xxx                                   #erase，删除
rpm -e -nodeps xxx                           #Don’t do a dependency check before installing or upgrading a package
rpm -U                                       #--upgrade，无论是否安装过某rpm包或其旧版本，直接安装指定rpm包
rpm -F                                       #--freshen，仅在安装某rpm包的旧版本时，更新rpm包
```

```x
rpm -q --scripts 包名                        #安装/卸载过程中的脚本
rpm -qf [绝对路径命令]                       #显示命令属于哪个包，-f --file, Query package owing file
	$ rpm -qf /bin/vi
	vim-minimal-7.4.629-5.el6_8.1.x86_64
rpm -qfi 命令                                #命令所属包的基本信息
rpm -qa |grep httpd                          #查询是否安装httpd
rpm -q 包名                                  #查包的版本信息
rpm -ql 包名                                 #包中全部文件
rpm -qc 包名                                 #包中配置文件
rpm -qd 包名                                 #包中文档
rpm -qi 包名                                 #查询包的基本信息
	rpm -pqi 包名                            #未安装的包的信息
	rpm -pql 包名                            #未安装的包的全部文件
```

```x
rpm --import key_file                        #导入公钥用于检查rpm文件的签名
rpm -qa | grep pubkey                        #列出rpm导入的所有公钥
rpm --checksig package.rpm                   #检查rpm文件的签名
	如果提示 MISSING KEYS，就说明缺少公钥。
		rpm --import <key file>              #导入公钥
	$ rpm --checksig screen.rpm 
	screen.rpm: rsa sha1 (md5) pgp md5 OK    #签名完好
	$ rpm --checksig screen.rpm
	screen.rpm: RSA SHA1 (MD5) PGP MD5 NOT OK   #签名损坏
```

```x
rpm -V  包                                  #查看已安装的包有什么变化
rpm -Vf 包
	rpm -V httpd
	rpm -Vf /usr/sbin/httpd
rpm -Va                                     #全部
```

<br>

## top

<sup><p align="right">[`TOP`](#Jump1)</p></sup>

- `h`：显示帮助画面，给出一些简短的命令总结说明；  
- `k`：终止一个进程；  
- `i`：忽略闲置和僵死进程，这是一个开关式命令；  
- `q`：退出程序；  
- `r`：重新安排一个进程的优先级别；  
- `S`：切换到累计模式；  
- `s`：改变两次刷新之间的延迟时间（单位为s），如果有小数，就换算成ms。输入0值则系统将不断刷新，默认值是5s；  
- `f`或者`F`：从当前显示中添加或者删除项目  
- `o`或者`O`：改变显示项目的顺序  
- `l`：切换显示平均负载和启动时间信息  
- `m`：切换显示内存信息  
- `t`：切换显示进程和CPU状态信息  
- `c`：切换显示命令名称和完整命令行  
- `M`：根据驻留内存大小进行排序  
- `P`：根据CPU使用百分比大小进行排序  
- `T`：根据时间/累计时间进行排序  
- `w`：将当前设置写入~/.toprc文件中  

```
top -d 1				        #1秒刷新一次 （默认是3秒）  
top -n 10				        #刷新10次就退出  
top -b					        #以批处理的方式运行，适合把输出重定向（管道，或者文件）  
top -b -d 0.5 | grep -E 'sshd'	#持续监视某个进程的信息变化  

top -b -n 2 > /tmp/aa           
```

<br>

## ps

<sup><p align="right">[`TOP`](#Jump1)</p></sup>

- 常用  
    * `ps`   : 当前登录的用户打开的程序  
    * `ps a` : 控制台进程  
    * `ps au` : 比`ps a`显示更多信息，控制台进程  
    * `ps aux` : 控制台进程+后台进程  
    * `ps auxf` : 进程显示父子关系，init为所有经常的父进程  
    * `ps -ef` : 和`ps aux`显示的列不同  
    * `ps -ef f` : `ps -ef`格式下，显示进程父子关系  

- To see every process with a user-defined format:

    ```sh
    ps -eo pid,tid,class,rtprio,ni,pri,psr,pcpu,stat,wchan:14,comm
    ```
    
    ```sh
    ps axo stat,euid,ruid,tty,tpgid,sess,pgrp,ppid,pid,pcpu,comm
    ```
    
    ```sh
    ps -eo pid,tt,user,fname,tmout,f,wchan
    ```
    
    ```sh
    ps -eo user,group,pid,ppid,nice,command --sort user
    ```


- 相对于进程而言  
    * **real user ID** (uid,ruid): 实际用户ID,指的是进程执行者是谁
    * **effective user ID** (euid): 有效用户ID,指进程执行时对文件的访问权限
    * **saved set-user-ID** (saved uid): 保存设置用户ID。是进程刚开始执行时，euid的副本。在执行exec调用之后能重新恢复原来的effectiv user ID.

- 系统做读写权限检查的流程  
    * (1) 检查进程的`euid`是否为0，是则放行，否则检查下一步  
    * (2) 检查进程的`euid`是否等于文件的`uid`，如果相等，则检查该文件权限位的左边三位是否有相应的权限，有则放行，否则拒绝  
    * (3) 检查进程的`egid`或者其中一个supplementary group id 是否等于文件的`gid`，如果相等，则检查该文件权限位的中间三位是否有相应的权限，有则放行，否则拒绝  
    * (4) 检查该文件权限位的右边三位是否有相应的权限，有则放行，否则拒绝  

### `ps aux`输出结果的参数解释：

```
$ ps aux | head -n 3
USER        PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root          1  0.0  0.3 128044  6680 ?        Ss   10:30   0:01 /usr/lib/systemd/systemd --switched-root --system --deserialize 21
root          2  0.0  0.0      0     0 ?        S    10:30   0:00 [kthreadd]
```
- `VSZ` : 虚拟内存使用量
- `RSS` : alias rss, rsz, resident set size: the non-swapped physical memory that a task has used(in kiloBytes)
- `STAT` : PROCESS STATE CODES 

Here are the different values that the s, stat and state output specifiers (header "STAT" or "S") will display to describe the state of a process.

CODE | meaning
--   |  --
`D`  |  Uninterruptible sleep (usually IO)
`R`  |  Running or runnable (on run queue)
`S`  |  Interruptible sleep (waiting for an event to complete)
`T`  |  Stopped, either by a job control signal or because it is being traced.
`W`  |  paging (not valid since the 2.6.xx kernel)
`X`  |  dead (should never be seen)
`Z`  |  Defunct ("zombie") process, terminated but not reaped by its parent.

For BSD formats and when the stat keyword is used, additional characters may be displayed:

CODE | meaning
--   |  --
`<`  |  high-priority (not nice to other users)
`N`  |  low-priority (nice to other users)
`L`  |  has pages locked into memory (for real-time and custom IO)
`s`  |  is a session leader
`l`  |  is multi-threaded (using CLONE_THREAD, like NPTL pthreads do)
`+`  | is in the foreground process group

<br>

## nice renice

<sup><p align="right">[`TOP`](#Jump1)</p></sup>

以指定优先级19运行程序gedit

```sh
nice -n 19 gedit
```

把正在运行的id为1234的进程的优先级调为19 

```sh
renice -n 19 1234
```

把正在运行的id为1234的进程的优先级调为-20

```sh
renice -n -20 1234
```

**优先级对进程的执行有什么影响**

优先级高的进程可以获得更多的系统资源，这个在系统处于高负荷的状态时比较明显。

```sh
time nice -n 19 head -c 1m /dev/urandom > /dev/null   <-- 用最低优先级运行
time nice -n -20 head -c 1m /dev/urandom > /dev/null  <-- 用最高优先级运行
```

<br>

## kill

<sup><p align="right">[`TOP`](#Jump1)</p></sup>

```
kill PID
kill -9 PID
```

```x
$ kill -l
 1) SIGHUP	     2) SIGINT	     3) SIGQUIT	     4) SIGILL	     5) SIGTRAP
 6) SIGABRT	     7) SIGBUS	     8) SIGFPE	     9) SIGKILL	    10) SIGUSR1
11) SIGSEGV	    12) SIGUSR2	    13) SIGPIPE	    14) SIGALRM	    15) SIGTERM
16) SIGSTKFLT	17) SIGCHLD	    18) SIGCONT	    19) SIGSTOP	    20) SIGTSTP
21) SIGTTIN	    22) SIGTTOU	    23) SIGURG	    24) SIGXCPU	    25) SIGXFSZ
26) SIGVTALRM	27) SIGPROF	    28) SIGWINCH	29) SIGIO	    30) SIGPWR
31) SIGSYS	    34) SIGRTMIN	35) SIGRTMIN+1	36) SIGRTMIN+2	37) SIGRTMIN+3
38) SIGRTMIN+4	39) SIGRTMIN+5	40) SIGRTMIN+6	41) SIGRTMIN+7	42) SIGRTMIN+8
43) SIGRTMIN+9	44) SIGRTMIN+10	45) SIGRTMIN+11	46) SIGRTMIN+12	47) SIGRTMIN+13
48) SIGRTMIN+14	49) SIGRTMIN+15	50) SIGRTMAX-14	51) SIGRTMAX-13	52) SIGRTMAX-12
53) SIGRTMAX-11	54) SIGRTMAX-10	55) SIGRTMAX-9	56) SIGRTMAX-8	57) SIGRTMAX-7
58) SIGRTMAX-6	59) SIGRTMAX-5	60) SIGRTMAX-4	61) SIGRTMAX-3	62) SIGRTMAX-2
63) SIGRTMAX-1	64) SIGRTMAX	
```

### killall

```
killall httpd		#按进程名杀死进程
killall -9 httpd
```

### skill

```
skill qwer		#按用户名杀死进程
skill -9 qwer
```

### pkill

```
pkill -9 bash		#杀死名字包含字符串'bash'的进程
pkill -9 -x bash	#杀死名字为bash的进程
pkill -9 -u qwer	#杀死属于用户qwer的所有进程
```

<br>

## lsattr chattr

<sup><p align="right">[`TOP`](#Jump1)</p></sup>

- `-R` : 递归处理，将指定目录下的所有文件及子目录一并处理。
- `-v` <版本编号> : 设置文件或目录版本。
- `-V` : 显示指令执行过程。
- `+` <属性> : 开启文件或目录的该项属性。
- `-` <属性> : 关闭文件或目录的该项属性。
- `=` <属性> : 指定文件或目录的该项属性。

### xfs的chattr选项

```sh
$ man xfs | tail -n21
FILE ATTRIBUTES
       The XFS filesystem supports setting the following file attributes on Linux systems using the chattr(1) utility:
       a - append only
       A - no atime updates
       d - no dump
       i - immutable  #一成不变的
       S - synchronous updates
       For descriptions of these attribute flags, please refer to the chattr(1) man page.
SEE ALSO
       chattr(1), xfsctl(3), mount(8), mkfs.xfs(8), xfs_info(8), xfs_admin(8), xfsdump(8), xfsrestore(8).
```

### ext4的chattr选项

```
$ man ext4 | tail -n35
FILE ATTRIBUTES
       The ext2, ext3, and ext4 filesystems support setting the following file attributes on Linux systems using the chattr(1) utility:
       a - append only
       A - no atime updates
       d - no dump
       D - synchronous directory updates
       i - immutable
       S - synchronous updates
       u - undeletable
       
       In addition, the ext3 and ext4 filesystems support the following flag:
       j - data journaling
       
       Finally, the ext4 filesystem also supports the following flag:
       e - extents format
       For descriptions of these attribute flags, please refer to the chattr(1) man page.
SEE ALSO
       mke2fs(8), mke2fs.conf(5), e2fsck(8), dumpe2fs(8), tune2fs(8), debugfs(8), mount(8), chattr(1)
```

<br>

## getfacl setfacl

<sup><p align="right">[`TOP`](#Jump1)</p></sup>

访问控制列表

### setfacl参数

```x
-b,--remove-all      删除所有扩展的acl规则，基本的acl规则(所有者，群组，其他）将被保留。  
-k,--remove-default  删除缺省的acl规则。如果没有缺省规则，将不提示。  
-n，--no-mask        不要重新计算有效权限。setfacl默认会重新计算ACL mask，除非mask被明确的制定。  
--mask               重新计算有效权限，即使ACL mask被明确指定。  
-d，--default        设定默认的acl规则。  
--restore=file       从文件恢复备份的acl规则（这些文件可由getfacl   -R产生）。通过这种机制可以恢复整个目录树的acl规则。此参数不能和除--test以外的任何参数一同执行。  
--test               测试模式，不会改变任何文件的acl规则，操作后的acl规格将被列出。  
-R，--recursive      递归的对所有文件及目录进行操作。  
-L，--logical        跟踪符号链接，默认情况下只跟踪符号链接文件，跳过符号链接目录。  
-P，--physical       跳过所有符号链接，包括符号链接文件。  
--                   标识命令行参数结束，其后的所有参数都将被认为是文件名  
-                    如果文件名是-，则setfacl将从标准输入读取文件名。

-m,--modify=ACL          更改文件的访问控制列表
-M,--modify-file=file    从文件读取访问控制列表条目更改
-x,--remove=ACL          根据文件中访问控制列表移除条目
-X,--remove-file=file    从文件读取访问控制列表条目并删除
--set,--set-file         用来设置文件或目录的acl规则，先前的设定将被覆盖
```

### 谁有权限设置ACL？

文件的所有者以及有`CAP_FOWNER`的用户进程可以设置一个文件的ACL。（在目前的Linux系统上，root用户是唯一有`CAP_FOWNER`能力的用户）

### ACL规则

setfacl命令可以识别以下的规则格式：

```x
[d[efault]:] [u[ser]:]uid[:perms]  指定用户的权限，文件所有者的权限（如果uid没有指定）
[d[efault]:] g[roup]:gid[:perms]   指定群组的权限，文件所有群组的权限（如果gid未指定）
[d[efault]:] m[ask][:][:perms]     有效权限掩码
[d[efault]:] o[ther][:perms]       其他的权限
```

- 恰当的acl规则被用在修改和设定的操作中，对于uid和gid，可以指定一个数字，也可指定一个名字。  
- perms域是一个代表各种权限的字母的组合：读-r写-w执行-x，执行只适合目录和一些可执行的文件。pers域也可设置为八进制格式。  

### ACL名词

ACL是由一系列的`Access Entry`所组成的，每一条`Access Entry`定义了特定的类别可以对文件拥有的操作权限。

`Access Entry`有三个组成部分：`Entry tag type`, `qualifier`(optional)和`permission`。

#### Entry tag type

- `ACL_USER_OBJ`：相当于Linux里file_owner的permission
- `ACL_USER`：定义了额外的用户可以对此文件拥有的permission
- `ACL_GROUP_OBJ`：相当于Linux里group的permission
- `ACL_GROUP`：定义了额外的组可以对此文件拥有的permission
- `ACL_MASK`：定义了`ACL_USER`, `ACL_GROUP`和`ACL_GROUP_OBJ`的最大权限 (这个我下面还会专门讨论)
- `ACL_OTHER`：相当于Linux里other的permission

```sh
$ getfacl test.txt
# file: test.txt
# owner: root
# group: admin
user::rw-
user:john:rw-
group::rw-
group:dev:r--
mask::rw- 
other::r--

$ getfacl --omit-header test.txt     # 开头三行的输出结果指定了文件名、属主和属组，--omit-header则不显示这三行
user::rw-
user:john:rw-
group::rw-
group:dev:r--
mask::rw- 
other::r--
```

针对输出结果的说明：

```x
user::rw-       定义了ACL_USER_OBJ, 说明file owner拥有read and write permission
user:john:rw-   定义了ACL_USER, 这样用户john就拥有了对文件的读写权限,实现了我们一开始要达到的目的
group::rw-      定义了ACL_GROUP_OBJ, 说明文件的group拥有read and write permission
group:dev:r--   定义了ACL_GROUP, 使得dev组拥有了对文件的read permission
mask::rw-       定义了ACL_MASK的权限为read and write
other::r--      定义了ACL_OTHER的权限为read
```


### 设置文件的ACL

#### `ACL_USER`和`ACL_GROUP`

新建文件，未设置acl规则： 

```
$ ls -l a.test 
-rw-r--r--. 1 root root 0 Sep 17 13:26 a.test

$ getfacl --omit-header a.test
user::rw-
group::r--
other::r--
```

用户qwer拥有对a.test文件的读写权限

```sh
setfacl -m u:qwer:rw- a.test
```

```x
$ getfacl --omit-header a.test
user::rw-
user:qwer:rw-
group::r--
mask::rw-
other::r--
```

设置dev组拥有read permission

```sh
setfacl -m g:dev:r--
```

```x
$ getfacl --omit-header a.test
user::rw-
user:qwer:rw-
group::r--
group:dev:r--
mask::rw-
other::r--
```

#### ACL_MASK和Effective permission

看假如现在我们设置test.sh的mask为read only，那么admin组的用户还会有write permission吗？

```x
$ setfacl -m mask::r-- test.sh
$ getfacl --omit-header test.sh
user::rwx
user:john:rwx   #effective:r--
group::rw-      #effective:r--
mask::r--
other::r--
```


### Default ACL

之前的讨论都是Access ACL，也就是对被设置的文件有效。

而Default ACL是指对于一个目录进行Default ACL设置，并且在此目录下建立的文件都将继承此目录的ACL。

```x
$ mkdir testdir
$ getfacl --omit-header testdir
user::rwx
group::r-x
other::r-x
```

现在，希望所有在此目录下建立的文件都可以被qwer用户所访问，那么应该对testdir目录设置Default ACL。

```x
$ setfacl -d -m u:qwer:rwx testdir
$ getfacl --omit-header testdir
user::rwx
group::r-x
other::r-x
default:user::rwx
default:user:qwer:rwx
default:group::r-x
default:mask::rwx
default:other::r-x
```

除了default:user:qwer:rwx，其余default项均是从file permission里copy过来的。

分别在testdir下创建文件和目录：

```x
$ touch ./testdir/a.file
$ mkdir ./testdir/b.dir
$ ls -l ./testdir/
total 0
-rw-rw-r--+ 1 root root 0 Sep 17 13:53 a.file
drwxrwxr-x+ 2 root root 6 Sep 17 13:54 b.dir
```

```x
$ getfacl --omit-header ./testdir/a.file
user::rw-
user:qwer:rwx		#effective:rw-
group::r-x			#effective:r--
mask::rw-
other::r--

$ getfacl --omit-header ./testdir/b.dir
user::rwx
user:qwer:rwx
group::r-x
mask::rwx
other::r-x
default:user::rwx
default:user:qwer:rwx
default:group::r-x
default:mask::rwx
default:other::r-x
```

可以看到，权限得到了继承。

### 其他

`setfacl -x`可以删除文件所拥有的ACL属性，但是那个+号还是会出现在文件的末尾。正确的删除方法应该是用`chacl -B`

用cp来复制文件的时候我们现在可以加上`-p`选项，这样在拷贝文件的时候也将拷贝文件的ACL属性，对于不能拷贝的ACL属性将给出警告。

<br>

## User and Password

<sup><p align="right">[`TOP`](#Jump1)</p></sup>


```	
r--: 100(2), 4(10)
-w-: 010(2), 2(10)
--x: 001(2), 1(10)
```

用户信息"数据库"：`/etc/passwd`, `/etc/group`; 分别对应的影子口令文件夹为: `/etc/shadow`、`/etc/gshadow`


文件 | 内容
---  | ---
/etc/passwd	| User account information.
/etc/shadow	| Secure user account information.
/etc/group	| Group account information.
/etc/gshadow | Secure group account information.
/etc/default/useradd | Default values for account creation.
/etc/skel/	|  Directory containing default files.
/etc/login.defs	| Shadow password suite configuration.

<span id='passwdJump'></span>

### /etc/passwd

<sup><p align="right">[`TOP`](#Jump1)</p></sup>

```x
用户登录名:密码位:UID:GID:GECOS:HOMEDIR:默认shell

qwer:x:1000:1000:qwer:/home/qwer:/bin/bash
```

其中，`GECOS`为全部注释信息

<span id='shadowJump'></span>

### /etc/shadow

存储的信息对应`/etc/passwd`**密码位**

```
用户登录名:Encrypted Passwd:上次修改密码时间:最少使用期限:最长使用期限:过期前告警:锁定前时间:指定过期时间:保留位(无意义)

qwer:$6$y3vt6oS1SjmkgoL7$1ydk5CtRX7yX2DKmAs92mZ1FWg2COLY6DRYktIS37jVR25RhE5sAbQ6RTkOJKRRJis68MYZ3qjyBz3WofrVjJ0::1:90:28:::
```

其中：

- **Encrypted Passwd**格式为： 

```
$1$杂质$校验码
```
若**Encrypted Passwd**位上出现的是`!!`或`*`，表示用户未设置密码，或者目前无法登录。

由此可知，若要暂时让用户密码失败，可在**Encrypted Passwd**位前加`!`或者`*`或者`x`

加密算法=$1:MD5、$5:SHA-256、$6:SHA-512

- **上次修改密码时间**=距1970-1-1过去的天数  
- **最少使用期限**=0表示不限制  
- **最长使用期限**=99999表示不限制  

<span id='groupJump'></span>

### /etc/group

<sup><p align="right">[`TOP`](#Jump1)</p></sup>

```x
组名:组密码:gid:属于该组的用户列表(逗号隔开)

root:x:0:qwer,q         #x表示未设置组密码
```

<span id='useraddJump'></span>

### /etc/default/useradd

<sup><p align="right">[`TOP`](#Jump1)</p></sup>

```sh
$ cat /etc/default/useradd

# useradd defaults file
GROUP=100	            用户默认组
HOME=/home	            用户家目录所在地址
INACTIVE=-1	            是否启用过期停权，-1表示不启用；宽限天数，0及以下数皆为无效数字
EXPIRE=	                帐号终止日期，不设置表示不启用；帐号失效日期(如：20081212)
SHELL=/bin/bash	        默认shell
SKEL=/etc/skel	        用户家目录中的环境文件，默认添加用户的目录默认文件存放位置；也就是说，当我们用adduser添加用户时，用户家目录下的文件，都是从这个目录中复制过去的
CREATE_MAIL_SPOOL=yes	是否创建用户邮件缓冲，yes表示创建
```

### useradd

<sup><p align="right">[`TOP`](#Jump1)</p></sup>

- `-r` : 添加系统用户  
- `-u` : 指定UID  
- `-g` : 指定基本组  
- `-G` : 指定附加组，多个可用逗号分开  
- `-c` : 指定附加信息，GECOS  
    ```
	$ useradd -c 'wenger' test2
	$ finger test2
	Login: test2                            Name: wenger
	Directory: /home/test2                  Shell: /bin/bash
	Never logged in.
	No mail.
	No Plan.
    ```
- `-d` : 指定家目录  
- `-s` : 指定登录shell  
- `-m` : 创建家目录，-k, --skel SKEL_DIR  
- `-M` : 不创建家目录  

### usermod

<sup><p align="right">[`TOP`](#Jump1)</p></sup>

- `-u` : 修改UID
- `-G` : 修改附加组（会覆盖之前的设定）
- `-g` : 修改基本组
- `-a` : -G 不覆盖，追加
- `-c` : 修改注释信息
- `-d` : HOMEDIR，-m 原目录一同移动至新目录
- `-s` : 修改登录shell
- `-l` : 修改用户帐号名称
- `-e` : 设置过期时间，格式YYYY-MM-DD，空表示不设置账户过期
    ```
	$ usermod -e 2019-09-03 qwer
	$ cat /etc/shadow | grep qwer
	qwer:$6$puunzxEl$.xII0RCqxEIvbr64x83ircJ1KmeTjfiLU1hb6fgurPAKSsGj/6816ZA4xhCGCUSYLbDL1R84nib8ndxulo8eL0:18120:0:99999:7::18142:
	
	$ usermod -e '' qwer
	$ cat /etc/shadow | grep qwer
	qwer:$6$puunzxEl$.xII0RCqxEIvbr64x83ircJ1KmeTjfiLU1hb6fgurPAKSsGj/6816ZA4xhCGCUSYLbDL1R84nib8ndxulo8eL0:18120:0:99999:7:::
	```
- `-L` : Lock
- `-U` : Unlock

### chsh

<sup><p align="right">[`TOP`](#Jump1)</p></sup>

changer shell，修改shell

- `-l` : 列出所有shell
- `-s` : 修改shell
	
### chfn

<sup><p align="right">[`TOP`](#Jump1)</p></sup>

changer finger，修改注释信息

- `-f`, `--full-name` <full-name>  real name
- `-o`, `--office` <office>        office number
- `-p`, `--office-phone` <phone>   office phone number
- `-h`, `--home-phone` <phone>     home phone number
    ```
	$ chfn -f qwerqwer -o 1234 -p 12345678 -h 1234567800 qwer
	Changing finger information for qwer.
	Finger information changed.
	$ finger qwer
	Login: qwer                             Name: qwerqwer
	Directory: /home/qwer                   Shell: /sbin/nologin
	Office: 1234, 12345678                  Home Phone: 123-456-7800
	Last login Mon Aug 12 12:10 (EDT) on pts/0
	No mail.
	No Plan.
	```

### passwd

<sup><p align="right">[`TOP`](#Jump1)</p></sup>

- `--stdin`
- `-d` : 删除密码
- `-l` : 锁定密码
- `-u` : 解锁
- `-n` : 密码最小生存期，in days
- `-x` : 密码最大生存期，in days

### pwconv

根据/etc/passwd文件生成/etc/shadow。它把所有口令从/etc/passwd移到/etc/shadow中。

### pwunconv

将/etc/shadow中的信息尽可能地恢复到/etc/passwd。


## test

<sup><p align="right">[`TOP`](#Jump1)</p></sup>

和if后接的判断符号`[ ]`类似 

```sh
       test - check file types and compare values

DESCRIPTION
       Exit with the status determined by EXPRESSION.
       --help display this help and exit
       --version
              output version information and exit
       An omitted EXPRESSION defaults to false.  Otherwise, EXPRESSION is true or false and sets exit status.  It is one of:
       ( EXPRESSION )
              EXPRESSION is true
       ! EXPRESSION
              EXPRESSION is false
       EXPRESSION1 -a EXPRESSION2
              both EXPRESSION1 and EXPRESSION2 are true
       EXPRESSION1 -o EXPRESSION2
              either EXPRESSION1 or EXPRESSION2 is true
       -n STRING
              the length of STRING is nonzero
       STRING equivalent to -n STRING
       -z STRING
              the length of STRING is zero
       STRING1 = STRING2
              the strings are equal
       STRING1 != STRING2
              the strings are not equal
       INTEGER1 -eq INTEGER2
              INTEGER1 is equal to INTEGER2
       INTEGER1 -ge INTEGER2
              INTEGER1 is greater than or equal to INTEGER2
       INTEGER1 -gt INTEGER2
              INTEGER1 is greater than INTEGER2
       INTEGER1 -le INTEGER2
              INTEGER1 is less than or equal to INTEGER2
       INTEGER1 -lt INTEGER2
              INTEGER1 is less than INTEGER2
       INTEGER1 -ne INTEGER2
              INTEGER1 is not equal to INTEGER2
       FILE1 -ef FILE2
              FILE1 and FILE2 have the same device and inode numbers
       FILE1 -nt FILE2
              FILE1 is newer (modification date) than FILE2
       FILE1 -ot FILE2
              FILE1 is older than FILE2
       -b FILE
              FILE exists and is block special
       -c FILE
              FILE exists and is character special
       -d FILE
              FILE exists and is a directory
       -e FILE
              FILE exists
       -f FILE
              FILE exists and is a regular file
       -g FILE
              FILE exists and is set-group-ID
       -G FILE
              FILE exists and is owned by the effective group ID
       -h FILE
              FILE exists and is a symbolic link (same as -L)
       -k FILE
              FILE exists and has its sticky bit set
       -L FILE
              FILE exists and is a symbolic link (same as -h)
       -O FILE
              FILE exists and is owned by the effective user ID
       -p FILE
              FILE exists and is a named pipe
       -r FILE
              FILE exists and read permission is granted
       -s FILE
              FILE exists and has a size greater than zero
       -S FILE
              FILE exists and is a socket
       -t FD  file descriptor FD is opened on a terminal
       -u FILE
              FILE exists and its set-user-ID bit is set
       -w FILE
              FILE exists and write permission is granted
       -x FILE
              FILE exists and execute (or search) permission is granted
```

## typeset 

typeset和declare相同

<sup><p align="right">[`TOP`](#Jump1)</p></sup>

```
declare [-aAfFgilrtux] [-p] [name[=value] ...]
typeset [-aAfFgilrtux] [-p] [name[=value] ...]

       Declare variables and/or give them attributes.  If no names are given then display the values of variables.  The -p option will display the attributes and values of each name.  When -p is used with name arguments,
       additional  options  are  ignored.   When  -p  is supplied without name arguments, it will display the attributes and values of all variables having the attributes specified by the additional options.  If no other
       options are supplied with -p, declare will display the attributes and values of all shell variables.  The -f option will restrict the display to shell functions.  The -F option inhibits  the  display  of  function
       definitions;  only the function name and attributes are printed.  If the extdebug shell option is enabled using shopt, the source file name and line number where the function is defined are displayed as well.  The
       -F option implies -f.  The -g option forces variables to be created or modified at the global scope, even when declare is executed in a shell function.  It is ignored in all other cases.  The following options can
       be used to restrict output to variables with the specified attribute or to give variables attributes:
       -a     Each name is an indexed array variable (see Arrays above).
       -A     Each name is an associative array variable (see Arrays above).
       -f     Use function names only.
       -i     The variable is treated as an integer; arithmetic evaluation (see ARITHMETIC EVALUATION above) is performed when the variable is assigned a value.
       -l     When the variable is assigned a value, all upper-case characters are converted to lower-case.  The upper-case attribute is disabled.
       -r     Make names readonly.  These names cannot then be assigned values by subsequent assignment statements or unset.
       -t     Give each name the trace attribute.  Traced functions inherit the DEBUG and RETURN traps from the calling shell.  The trace attribute has no special meaning for variables.
       -u     When the variable is assigned a value, all lower-case characters are converted to upper-case.  The lower-case attribute is disabled.
       -x     Mark names for export to subsequent commands via the environment.

       Using  `+'  instead  of  `-' turns off the attribute instead, with the exceptions that +a may not be used to destroy an array variable and +r will not remove the readonly attribute.  When used in a function, makes
       each name local, as with the local command, unless the -g option is supplied, If a variable name is followed by =value, the value of the variable is set to value.  The return value is 0 unless an invalid option is
       encountered,  an  attempt is made to define a function using ``-f foo=bar'', an attempt is made to assign a value to a readonly variable, an attempt is made to assign a value to an array variable without using the
       compound assignment syntax (see Arrays above), one of the names is not a valid shell variable name, an attempt is made to turn off readonly status for a readonly variable, an attempt is made to turn off array sta‐
       tus for an array variable, or an attempt is made to display a non-existent function with -f.
```

选项	            |含义
--                  |--
-f [name]	        |列出之前由用户在脚本中定义的函数名称和函数体。
-F [name]	        |仅列出自定义函数名称。
-g name	            |在 Shell 函数内部创建全局变量。
-p [name]	        |显示指定变量的属性和值。
-a name	            |声明变量为普通数组。
-A name	            |声明变量为关联数组（支持索引下标为字符串）。
-i name 	        |将变量定义为整数型。
-r name[=value] 	|将变量定义为只读（不可修改和删除），等价于 readonly name。
-x name[=value]	    |将变量设置为环境变量，等价于 export name[=value]。
-                   |表示设置属性
+                   |表示取消属性
<br>

## fdisk

<sup><p align="right">[`TOP`](#Jump1)</p></sup>

Linux系统中有两个分区工具: 

- fdisk  
- parted  

二者都可以对linux的硬盘进行分区，但是二者从细节上来说，又有很大的区别.

### MBR

大小512字节，分为三部分:  
- 主引导程序：446字节  
- 硬盘分区表：64字节  
- 分区结束标记（硬盘有效位）：2字节  

MBR分区类型中有三种类型的分区: 主分区、扩展分区和逻辑分区

![Picture][Picture2]

![Picture][Picture3]

`DPT`的大小是64字节，每个主分区要占用16字节，扩展分区也要占用16个字节的主分区空间，所以每个磁盘上最多只能建立四个主分区

### GPT

![Picture][Picture4]

这张图，简明扼要的显示除了GPT分区方案的硬盘结构:  

- 1>GPT使用`LBA 0`、`LBA 1`表明硬盘上的地址. `LBA 0`指的是物理序号为0的第一个扇区，`LBA 1`指的是物理序号为1的第二个扇区，依次类推。 以前一般都是用chs方式对硬盘寻址的，现在一般都用LBA方式对硬盘寻址  
- 2> `LBA0` :保留MBR, 主要是出于软件兼容性的考虑，对GPT分区方案本身来讲，其实没有啥意义

- 3> `LBA1` :GPT表头记录,             记录分区本身位置与大小，同时记录了备份用的GPT分区放置位置以及分区表的检验机制码（CRC32）

- 4> `LBA2-33` : 实际记录分区信息 
从`LBA2`区块开时，每个LBA都可以记录4笔分区记录，所以默认情况下可以有4×32=128笔分区记录，因为每个LBA有512bytes，因此每个记录用到128bytes的空间，除了每个记录所需要的标识符和相关记录外，GPT在每个记录中分别提供64bits来记录开始/结束的扇区号码，因此，GPT分区表对于单一分区来说，他的最大容量限制就是8ZB。

![Picture][Picture5]

```
# fdisk
Command (m for help): m
Command action
   d   delete a partition
   g   create a new empty GPT partition table
   G   create an IRIX (SGI) partition table
   l   list known partition types
   m   print this menu
   n   add a new partition
   o   create a new empty DOS partition table
   q   quit without saving changes
   s   create a new empty Sun disklabel
   w   write table to disk and exit
```

```
# parted
(parted) help                                                             
  align-check TYPE N                        check partition N for TYPE(min|opt) alignment
  help [COMMAND]                           print general help, or help on COMMAND
  mklabel,mktable LABEL-TYPE               create a new disklabel (partition table)
  mkpart PART-TYPE [FS-TYPE] START END     make a partition
  name NUMBER NAME                         name partition NUMBER as NAME
  print [devices|free|list,all|NUMBER]     display the partition table, available devices, free space, all found partitions, or a particular partition
  quit                                     exit program
  rescue START END                         rescue a lost partition near START and END
  rm NUMBER                                delete partition NUMBER
  select DEVICE                            choose the device to edit
  disk_set FLAG STATE                      change the FLAG on selected device
  disk_toggle [FLAG]                       toggle the state of FLAG on selected device
  set NUMBER FLAG STATE                    change the FLAG on partition NUMBER
  toggle [NUMBER [FLAG]]                   toggle the state of FLAG on partition NUMBER
  unit UNIT                                set the default unit to UNIT
  version                                  display the version number and copyright information of GNU Parted
```



<span id = "Jump2" ></span>

<sup><p align="right">[`TOP`](#Jump1)</p></sup>