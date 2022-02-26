
## 1

> [https://www.cnblogs.com/luohaixian/p/9313863.html](https://www.cnblogs.com/luohaixian/p/9313863.html)


## 2 准备工作

* 创建编译用户

    ```sh
    useradd rpmbuilder
    ```

* 构建编译所需环境

    * 安装依赖包

        ```sh
        yum install rpm-build redhat-rpm-config asciidoc hmaccalc perl-ExtUtils-Embed pesign xmlto
        yum install audit-libs-devel binutils-devel elfutils-devel elfutils-libelf-devel java-devel
        yum install ncurses-devel newt-devel numactl-devel pciutils-devel python-devel zlib-devel
        yum install make gcc bc openssl-devel 
        yum groupinstall "Development Tools"
        ```

    * rpm编译目录创建

        ```sh
        su - rpmbuilder
        mkdir -p ~/rpmbuild/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}
        # echo '%_topdir %(echo $HOME)/rpmbuild' > ~/.rpmmacros    # 默认情况下 _topdir 就是 $HOME/rpmbuild
        ```
 
## 3 获取源码

* 使用"红帽系"发行版操作系统提供的 `SRPM`, 即 SRC RPM

* 下载 kernel 源码

## 4 编译

### 4.1 通过SRPM编译

* 获取.src.rpm内核源码包

    ```sh
    ~]$ uname -r 
    3.10.0-957.el7.x86_64

    ~]$ ls -l kernel-3.10.0-957.el7.src.rpm 
    -rw-------. 1 rpmbuilder rpmbuilder 101032927 Feb 26 15:44 kernel-3.10.0-957.el7.src.rpm
    ```

* 安装.src.rpm内核源码包

    ```sh
    ~]$ rpm -i kernel-3.10.0-957.el7.src.rpm 2>/dev/null
    ```

* 检查 BuildRequire 有没有少安装

    ```sh
    ]$ grep BuildRequire ~/rpmbuild/SPEC/kernel.spec

    BuildRequires: module-init-tools, patch >= 2.5.4, bash >= 2.03, sh-utils, tar
    BuildRequires: xz, findutils, gzip, m4, perl, make >= 3.78, diffutils, gawk
    BuildRequires: gcc >= 4.8.5-29, binutils >= 2.25, redhat-rpm-config >= 9.1.0-55
    BuildRequires: hostname, net-tools, bc
    BuildRequires: xmlto, asciidoc
    BuildRequires: openssl
    BuildRequires: hmaccalc
    BuildRequires: python-devel, newt-devel, perl(ExtUtils::Embed)  # perl-ExtUtils-Embed
    BuildRequires: pesign >= 0.109-4
    BuildRequires: elfutils-libelf-devel
    BuildRequires: sparse >= 0.4.1
    BuildRequires: elfutils-devel zlib-devel binutils-devel bison
    BuildRequires: audit-libs-devel
    BuildRequires: java-devel
    BuildRequires: numactl-devel
    BuildRequires: pciutils-devel gettext ncurses-devel
    BuildRequires: python-docutils
    BuildRequires: zlib-devel binutils-devel
    BuildRequires: rpm-build >= 4.9.0-1, elfutils >= 0.153-1
    BuildRequires: bison flex
    BuildRequires: glibc-static

    root ~] yum install module-init-tools patch bash sh-utils tar xz findutils gzip m4 perl make diffutils gawk gcc binutils redhat-rpm-config hostname net-tools bc xmlto asciidoc openssl hmaccalc python-devel newt-devel perl pesign elfutils-libelf-devel sparse elfutils-devel zlib-devel binutils-devel bison audit-libs-devel java-devel numactl-devel pciutils-devel gettext ncurses-devel python-docutils zlib-devel binutils-devel rpm-build elfutils bison flex glibc-static
    ```


* 解压并释放源码包

    ```sh
    ]$ cd ~/rpmbuild/SPECS
    ]$ rpmbuild -bp --target=$(uname -m) kernel.spec
    ```

* 修改配置文件

    ```sh
    # 1. 切换至相应目录, 准备修改".config"
    cd ~/rpmbuild/BUILD/kernel-3.10.0-957.el7/linux-3.10.0-957.el7.x86_64/

    # 2. 自定义编译模块
    make menuconfig

    # 3. .config 文件改名, 拷贝到编译配置文件目录
    cp .config ~/rpmbuild/SOURCES/kernel-3.10.0-`uname -m`.config

    ```

* 编译

    ```sh
    cd ~/rpmbuild/SPECS
    rpmbuild -bb --target=`uname -m` kernel.spec --without debug --without debuginfo
    ```


    * 如果出现以下报错, 则需要修改 ```~/rpmbuild/SOURCES/kernel-3.10.0-`uname -m`.config```, 首行修改为 `# x86_64`

    ```text
    ...
    + rm -f .newoptions
    + make ARCH= oldnoconfig
    Makefile:530: arch//Makefile: No such file or directory
    make: *** No rule to make target 'arch//Makefile'.  Stop.
    error: Bad exit status from /var/tmp/rpm-tmp.AEKmiI (%prep)


    RPM build errors:
        Bad exit status from /var/tmp/rpm-tmp.AEKmiI (%prep)
        ...
    ```
