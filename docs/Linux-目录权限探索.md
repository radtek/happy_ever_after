# Linux文件权限

## 目录

* 重点理解: 目录主要的内容是**记录文件名列表和子目录列表**, 而不是实际存放数据的地方
* `r`: 具有读取目录结构列表的权限, 可以查看目录下的文件名和子目录名
* `w`: 具有更改目录结构列表的权限, 包括
    * 在该目录下**新建**文件和目录
    * **删除**该目录下已经存在的文件或子目录, **无论文件和子目录权限如何**, 即:用户能否删除一个文件或目录, 由该用户是否具有该文件或目录所在的上级目录的w权限
    * 将该目录下已经文件或子目录进行**重命名**
    * **转移**该目录内的文件或子目录的位置
* `x`: 具有进入该目录成为工作目录的权限, 如果用户对于目录不具有x权限, 则无法切换到该目录下, 也就无法执行该目录下的任何命令, 即使具有该目录的r权限和w权限


### 探索一

* dir01, dir02, dir03 三个目录分别授权 r, w, x权限, 属主和属组分别为 user01, user02, user03

    ```sh
    ~] ls -l 

    dr--------. 2 user01 user01     20 Feb 23 09:17 dir01
    d-w-------. 2 user02 user02     20 Feb 23 09:17 dir02
    d--x------. 2 user03 user03     20 Feb 23 09:17 dir03

    dir01/
    -rw-r--r--. 1 user01 user01 4 Feb 23 09:17 file01
    dir02/
    -rw-r--r--. 1 user02 user02 4 Feb 23 09:17 file02
    dir03/
    -rw-r--r--. 1 user03 user03 4 Feb 23 09:17 file03
    ```

* user01 用户对 dir01 目录及目录下的文件访问权限情况

    ```sh
    ~] su - user01

    ~]$ cd dir01
    -bash: cd: dir01: Permission denied

    ~]$ ls -l dir01
    ls: cannot access dir01/file01: Permission denied
    total 0
    -????????? ? ? ? ?            ? file01

    ~]$ cat dir01/file01 
    cat: dir01/file01: Permission denied

    ~]$ mkdir /tmp/dir01/test_dir
    mkdir: cannot create directory ‘/tmp/dir01/test_dir’: Permission denied

    ~]$ touch dir01/file02
    touch: cannot touch ‘dir01/file02’: Permission denied

    ~]$ rm dir01/file01 
    rm: cannot remove ‘dir01/file01’: Permission denied
    ```

* user02 用户对 dir02 目录及目录下的文件访问权限情况:

    ```sh
    ~] su - user02

    ~]$ cd dir02
    -bash: cd: dir02: Permission denied

    ~]$ ls -l dir02
    ls: cannot open directory dir02: Permission denied

    ~]$ cat dir02/file02
    cat: dir02/file02: Permission denied

    ~]$ mkdir dir02/test_dir
    mkdir: cannot create directory ‘dir02/test_dir’: Permission denied

    ~]$ touch dir02/test_file
    touch: cannot touch ‘dir02/test_file’: Permission denied

    ~]$ rm dir02/file02
    rm: cannot remove ‘dir02/file02’: Permission denied
    ```

* user03 用户对 dir03 目录及目录下的文件访问权限情况

    ```sh
    ~] su - user03

    ~]$ cd dir03

    dir03]$ ls .
    ls: cannot open directory .: Permission denied

    dir03]$ cat ./file03
    333

    dir03]$ touch test_file
    touch: cannot touch ‘test_file’: Permission denied

    dir03]$ mkdir test_dir
    mkdir: cannot create directory ‘test_dir’: Permission denied

    dir03]$ rm file03
    rm: cannot remove ‘file03’: Permission denied
    ```

* 结论1:

    * 对目录仅有 r 权限时: 仅对目录下文件和目录**列表**有访问权限, 且列出该目录下的文件和目录时, 仅能获取到**名字**, 获取不到其他信息
    * 对目录仅有 w 权限时: 实际上无法完成对目录的任何操作
    * 对目录仅有 x 权限时: 可正常切换工作目录, 以及访问文件内容(该权限由文件本身r权限控制)


### 探索二

* dir01, dir02, dir03 三个目录分别授权 rw-, r-x, -wx权限, 属主和属组分别为 user01, user02, user03

    ```sh
    drw-------. 2 user01 user01     20 Feb 23 09:17 dir01
    dr-x------. 2 user02 user02     20 Feb 23 09:17 dir02
    d-wx------. 2 user03 user03     20 Feb 23 09:17 dir03

    dir01/
    -rw-r--r--. 1 user01 user01 4 Feb 23 09:17 file01
    dir02/
    -rw-r--r--. 1 user02 user02 4 Feb 23 09:17 file02
    dir03/
    -rw-r--r--. 1 user03 user03 4 Feb 23 09:17 file03
    ```

* user01 用户对 dir01 目录及目录下的文件访问权限情况

    ```sh
    ~] su - user01

    ~]$ cd dir01
    -bash: cd: dir01: Permission denied

    ~]$ ls -l dir01
    ls: cannot access dir01/file01: Permission denied
    total 0
    -????????? ? ? ? ?            ? file01

    ~]$ touch dir01/test_file
    touch: cannot touch ‘dir01/test_file’: Permission denied

    ~]$ mkdir dir01/test_dir
    mkdir: cannot create directory ‘dir01/test_dir’: Permission denied

    ~]$ cat dir01/file01
    cat: dir01/file01: Permission denied

    ~]$ rm dir01/file01
    rm: cannot remove ‘dir01/file01’: Permission denied
    ```

* user02 用户对 dir02 目录及目录下的文件访问权限情况

    ```sh
    ~]$ su - user02

    ~]$ cd dir02

    dir02]$ ls -l .
    total 4
    -rw-r--r--. 1 user02 user02 4 Feb 23 09:17 file02

    dir02]$ cat file02 
    222

    dir02]$ touch test_file
    touch: cannot touch ‘test_file’: Permission denied

    dir02]$ mkdir test_dir
    mkdir: cannot create directory ‘test_dir’: Permission denied

    dir02]$ rm file02
    rm: cannot remove ‘file02’: Permission denied
    ```


* user03 用户对 dir03 目录及目录下的文件访问权限情况

    ```sh
    ~] su - user03

    dir03]$ cd dir03

    dir03]$ ls -l .
    ls: cannot open directory .: Permission denied

    dir03]$ cat file03
    333

    dir03]$ touch test_file
    (0)dir03]$ mkdir test_dir
    (0)dir03]$ rm test_file
    (0)dir03]$ rmdir test_dir
    ```

* 结论2:

    * 对目录有 rw- 权限时: 仅对目录下文件和目录**列表**有访问权限, 且列出该目录下的文件和目录时, 仅能获取到**名字**, 获取不到其他信息; (**该情况下,可认为 w 未生效**)
    * 对目录有 r-x 权限时: 除"无法完成目录下的**修改**动作(创建或删除文件/目录)"外, 其他操作正常
    * 对目录有 -wx 权限时: 除"无法列出文件/目录列表"外, 其他操作正常
