# 查看文件创建时间

## ext4

* 获取到文件所在磁盘

    ```sh
    ~] df -hT
    Filesystem    Type    Size  Used Avail Use% Mounted on
    /dev/mapper/vg_01-Log01        # <= 
                ext4     35G   13G   21G  39% /
    tmpfs        tmpfs    939M  491M  449M  53% /dev/shm
    /dev/vda1     ext4    485M   32M  428M   7% /boot
    ```

* 获取到文件的inode号, 使用 `ls -i` 也可查询

    ```sh
    ~] stat /etc/hosts
    File: '/etc/hosts'
    Size: 186             Blocks: 8          IO Block: 4096   regular file
    Device: fd00h/64768d    Inode: 1576689     Links: 1      # <= 
    Access: (0644/-rw-r--r--)  Uid: (    0/    root)   Gid: (    0/    root)
    Access: 2022-02-10 00:45:20.769000091 +0800
    Modify: 2022-02-10 00:45:19.983000112 +0800
    Change: 2022-02-10 00:45:19.983000112 +0800
    ```

* 查询文件创建时间

    ```sh
    ~] debugfs -R 'stat <1576689>' /dev/mapper/vg_01-Log01    # <= 
    debugfs 1.41.12 (17-May-2010)
    Inode: 1576689   Type: regular    Mode:  0644   Flags: 0x80000
    Generation: 1875514122    Version: 0x00000000:00000001
    User:     0   Group:     0   Size: 186
    File ACL: 0    Directory ACL: 0
    Links: 1   Blockcount: 8
    Fragment:  Address: 0    Number: 0    Size: 0
    ctime: 0x6203ef9f:ea5d90c0 -- Thu Feb 10 00:45:19 2022
    atime: 0x6203efa0:b7580a6c -- Thu Feb 10 00:45:20 2022
    mtime: 0x6203ef9f:ea5d90c0 -- Thu Feb 10 00:45:19 2022
    crtime: 0x61ef1178:80821818 -- Tue Jan 25 04:52:08 2022   # <= 获取到文件创建时间 crtime
    Size of extra inode fields: 28
    Extended attributes stored in inode body: 
    selinux = "system_u:object_r:net_conf_t:s0\000" (32)
    EXTENTS:
    (0): 4756475
    ```

## ext2,ext3,xfs等不支持

