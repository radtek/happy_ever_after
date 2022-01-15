# Install Oracle Database 11g on Linux (CentOS 6.9)

##  Single-instance database

### Overview

On a single-instance database, the Oracle Grid Infrastructure home includes *Oracle Restart* and *Oracle Automatic Storage Management* (*Oracle ASM*) software.

*Oracle Cluster Synchronization Services* (CSS), is a daemon process that is configured by the **root.sh** script.

* The CSS service is required to enable synchronization between an Oracle ASM instance and the database instances that rely on it for database file storage.

* Because the service must be running before an Oracle ASM instance or database instance starts, it is configured to start automatically by *Oracle Restart* before the *Oracle ASM* instance is started. It must be running if an Oracle database is using Oracle ASM for database file storage.

* For single-instance installations, the CSS daemon is installed-in and runs from the Oracle Grid Infrastructure home which is the same home that runs Oracle ASM.


Storage Options: 

* File system
    * A file system on disk that *phycially* attached to the system.
    * A file system on logical volume manager (*LVM*) volume or *RAID* device.
        * Oracle recommends that you use the stripe and mirror everything (SAME) methodology to increase performance and reliability
    * A network file system (*NFS*) from a certified network-attached storage (NAS) device.
* Oracle Automatic Storage Management
    * disk groups
    * oracle ASM instance
        * a special oracle instance that manage the Oracle ASM disk groups
        * User: ASMSNMP, *open* status and *SYSDBA* privilege

Oracle Enterprise Manager:

* a web-based management tool to simplify database administration
* deploy
    * centrally
        * You must install at least one *Oracle Management Repository* and one *Oracle Management Service* within the environment, then install an *Oracle Enterprise Management Agent* on every computer to manage.
    * localy
*  *Oracle Enterprise Manager Database Control* provides a web-based user interface that enables you to monitor, administer, and maintain an Oracle database. You can use it to perform all database administration tasks. You can also use it to determine information about the database.
* Backup
    * automated backups
        * use Oracle Rocovery Manager (RMAN): full backup (first time) + incremental backup (subsequent jobs) 
    * location 
        * Default fast recovery area: *$ORACLE_BASE/recovery_area*
        * Default data file location: *$ORACLE_BASE/oradata*
    * user
        * system user
        * group: *ORA_DBA*
        * privilege: *Logon As A Batch Job*
    * The backup job is scheduled to run every morning at *2.00 a.m*.
    * The disk quota for the fast recovery area is *2 GB*.

Upgrade consideration

* Upgrading Your Operating System Before a Database Upgrade
    * Upgrade the operating system. Then, upgrade the database either manually or by using Oracle Database Upgrade Assistant.
    * Migrating to a New Computer. 
        * steps: 1.Copy the database files; 2.Re-create the control files; 3.Manually upgrade the database
        * or using the Export/Import utilities method

### Preinstallion tasks

About Installing the Linux Operating System
Logging In to the System as root
Checking the Hardware Requirements
Checking the Software Requirements
Reviewing Operating System Security Common Practices
Installation Fixup Scripts
Verifying UDP and TCP Kernel Parameters
Installing the cvuqdisk Package for Linux
Confirming Host Name Resolution
Disabling Transparent HugePages
Checking the Network Setup
Creating Required Operating System Groups and Users
Checking Resource Limits for the Oracle Software Installation Users
Configuring Kernel Parameters for Linux
Reviewing Operating System Security Common Practices
Identifying Required Software Directories
Identifying or Creating an Oracle Base Directory
Choosing a Storage Option for Oracle Database and Recovery Files
Creating Directories for Oracle Database or Recovery Files
Configuring Storage for Oracle Database Files Using Block Devices
Configuring Disk Devices for Oracle Database
Stopping Existing Oracle Processes
Configuring Oracle Software Owner Environment


#### Hardware Requirements

* Memory

```
Minimun: 1GB
Recommanded: 2GB or more
```

* Swap


**RAM** | **Swap Space**
 -- | --
Between 1 GB and 2 GB | 1.5 times the size of the RAM
Between 2 GB and 16 GB | Equal to the size of the RAM
More than 16 GB | 16 GB

* Automatic Memory Management

Starting with Oracle Database 11g, the *Automatic Memory Management* feature requires more shared memory (*`/dev/shm`*)and file descriptors. The size of the shared memory must be at least the greater of the `MEMORY_MAX_TARGET` and `MEMORY_TARGET` parameters for each Oracle instance on the computer

If the `MEMORY_MAX_TARGET` parameter or the `MEMORY_TARGET` parameter is set to a nonzero value, and an incorrect size is assigned to the shared memory, it results in an `ORA-00845` error at startup. On Linux systems, if the operating system `/dev/shm` mount size is too small for the Oracle system global area (SGA) and program global area (PGA), it results in an `ORA-00845` error.

for ORA-00845:

```sh
# temporary
~] mount -t tmpfs shmfs -o size=7g /dev/shm

# presistent
~] vi /etc/fstab
shmfs /dev/shm tmpfs size=7g 0
```


* File descriptors

    * The number of file descriptors for each Oracle instance must be at least `512*PROCESSES`

    * `ORA-27123` error from various Oracle processes and potentially Linux Error EMFILE (*Too many open files*)in non-Oracle processes.


* Disk

    * 1 GB of space in the `/tmp` directory

    * Data file and software file (x86_64)

    | **Installation Type** | **Requirement for Software Files (GB)** |
    |  -- | -- |
    | Enterprise Edition | 4.5 |
    | Standard Edition | 4.4 |

    | **Installation Type** | **Disk Space for Data Files (GB)** |
    |  -- | -- |
    | Enterprise Edition | 1.7 |
    | Standard Edition | 1.5 |


#### Software Requirements

RPM (x86_64)

```
binutils-2.20.51.0.2-5.11.el6 (x86_64)
compat-libcap1-1.10-1 (x86_64)
compat-libstdc++-33-3.2.3-69.el6 (x86_64)
compat-libstdc++-33-3.2.3-69.el6.i686
gcc-4.4.4-13.el6 (x86_64)
gcc-c++-4.4.4-13.el6 (x86_64)
glibc-2.12-1.7.el6 (i686)
glibc-2.12-1.7.el6 (x86_64)
glibc-devel-2.12-1.7.el6 (x86_64)
glibc-devel-2.12-1.7.el6.i686
ksh
libgcc-4.4.4-13.el6 (i686)
libgcc-4.4.4-13.el6 (x86_64)
libstdc++-4.4.4-13.el6 (x86_64)
libstdc++-4.4.4-13.el6.i686
libstdc++-devel-4.4.4-13.el6 (x86_64)
libstdc++-devel-4.4.4-13.el6.i686
libaio-0.3.107-10.el6 (x86_64)
libaio-0.3.107-10.el6.i686
libaio-devel-0.3.107-10.el6 (x86_64)
libaio-devel-0.3.107-10.el6.i686
make-3.81-19.el6
sysstat-9.0.4-11.el6 (x86_64)
unixODBC
unixODBC-devel
unixODBC.i686
unixODBC-devel.i686
```

```sh
~] yum install binutils compat-libcap1 compat-libstdc++-33 compat-libstdc++-33.i686 gcc gcc-c++ glibc glibc.i686 glibc-devel glibc-devel.i686 ksh libgcc libgcc.i686 libstdc++ libstdc++.i686 libstdc++-devel libstdc++-devel.i686 libaio libaio.i686 libaio-devel libaio-devel.i686 make sysstat unixODBC unixDOBC-devel unixODBC.i686 unixODBC-devel.i686
```

#### TCP and UDP port

```sh
# temporary
~] echo 9000 65500 > /proc/sys/net/ipv4/ip_local_port_range

# presistent
~] vi /etc/sysctl.conf
net.ipv4.ip_local_port_range = 9000 65500
~] sysctl -p
~] service network restart
```

#### `cvuqdisk` Package

```sh
# Remove installed cvuqdisk
rpm -qi cvuqdisk
rpm -e cvuqdisk

# Set the environment variable CVUQDISK_GRP to point to the group that owns cvuqdisk, typically oinstall
CVUQDISK_GRP=oinstall; export CVUQDISK_GRP

rpm -iv cvuqdisk-1.0.9-1.rpm
```

#### Host Name Resolution

```sh
~] vi /etc/hosts
x.x.x.x  your_hostname
```

#### Disabling Transparent HugePages

* Check

> If Transparent HugePages are removed from the kernel then the `/sys/kernel/mm/transparent_hugepage` or `/sys/kernel/mm/redhat_transparent_hugepage` files do not exist.

```sh
~] cat /sys/kernel/mm/redhat_transparent_hugepage/enabled
~] cat /sys/kernel/mm/transparent_hugepage/enabled

[always] madvise never   # [always]: Transparent HugePages are being used
```

* Set

    * the kernel boot line in `/etc/grub.conf`. Add:
    
    ```
    transparent_hugepage=never
    ```

    * reboot

#### Setting the ORACLE_HOSTNAME Environment Variable

```sh
ORACLE_HOSTNAME=somehost.example.com
export ORACLE_HOSTNAME
```

#### Creating users and groups

```sh
groupadd oinstall
groupadd dba
groupadd oper
useradd -g oinstall -G dba,oper oracle

# usermod -g oinstall -G dba,oper oracle
```

#### Checking Resource Limits for the Oracle Software Installation Users

```sh
~] vi /etc/security/limit.conf
oracle        soft    nofile          1024
oracle        hard    nofile          65536
oracle        soft    nproc           1024
oracle        hard    nproc           65536
oracle        soft    stack           10240
oracle        hard    stack           32768
```

#### Configuring Kernel Parameters for Linux

```sh
# minimum values only
fs.aio-max-nr = 1048576
fs.file-max = 6815744
kernel.shmall = 2097152
kernel.shmmax = 4294967295
kernel.shmmni = 4096
kernel.sem = 250 32000 100 128
net.ipv4.ip_local_port_range = 9000 65500
net.core.rmem_default = 262144
net.core.rmem_max = 4194304
net.core.wmem_default = 262144
net.core.wmem_max = 1048576
```

#### Identifying Required Software Directories

You must identify or create the following directories for the Oracle software:

* Oracle Base Directory: `/mount_point/app/software_owner`
    * `mount_point` is the mount point directory for the file system that contains the Oracle software (`/u01`)
    * `software_owner` is the operating system user name of the software owner installing the Oracle software, for example `oracle `or `grid`.

* Oracle Inventory Directory
    * `/u01/app/oraInventory`
    * `/home/oracle/oraInventory`

* Oracle Home Directory
    * `oracle_base/product/11.1.0/dbhome_1`
    * `oracle_base/product/11.2.0/dbhome_1`
    * `oracle_base/product/11.2.0/grid`

```sh
~] mkdir -p /u01/app/oracle
~] chown -R oracle:oinstall /u01/app/oracle  # chown -R oracle:oinstall /u01
~] chmod -R 775 /u01/app/oracle

~] vi /home/oracle/.bash_profile
ORACLE_BASE='/u01/app/oracle'
export ORACLE_BASE
```

* Creating Required Directories

    * database file directory: `$ORACLE_BASE/oradata`
    * Recovery file directory (fast recovery area): `$ORACLE_BASE/fast_recovery_area`

* .bash_profile (`/home/oracle/.bash_profile`)

```sh
ORACLE_HOSTNAME='ora11g-test-n01'
ORACLE_BASE='/u01/app/oracle'
ORACLE_HOME="$ORACLE_BASE/product/11.2.0/dbhome_1"
ORACLE_SID=orcl
PATH=$PATH:$ORACLE_HOME/bin

export ORACLE_HOSTNAME ORACLE_BASE ORACLE_HOME ORACLE_SID PATH
```




#### 启动和关闭数据库

* 监听操作

```sh
lsnrctl status
lsnrctl start
lsnrctl stop
```

* 启动/关闭实例

```sh
# 用sys账号登录到Oracle
sqlplus /nolog
conn /as sysdba

# 启动实例
startup

# 关闭实例
shutdown immediate
```
