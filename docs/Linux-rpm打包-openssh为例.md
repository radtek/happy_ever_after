```spec
Name:
Version:
Release:        1%{?dist}
Summary:

Group:
License:
URL:
Source0:

BuildRequires:
Requires:

%description


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
%make_install


%files
%doc



%changelog
```

```sh
Name:      软件包的名称, 在后面的变量中即可使用%{name}的方式引用
Summary:   软件包的内容
Version:   软件的实际版本号, 例如：1.12.1, 后面可使用%{version}引用
Release:   发布序列号, 例如：1%{?dist}, 标明第几次打包, 后面可使用%{release}引用
Group:     软件分组, 建议使用：Applications/System
License:   软件授权方式GPLv2
Source:    源码包, 可以带多个用Source1、Source2等源, 后面也可以用%{source1}、%{source2}引用
BuildRoot: 这个是安装或编译时使用的临时目录, 即模拟安装完以后生成的文件目录：%_topdir/BUILDROOT 后面可使用$RPM_BUILD_ROOT 方式引用。
URL:       软件的URI
Vendor:    打包组织或者人员
Patch:     补丁源码, 可使用Patch1、Patch2等标识多个补丁, 使用 %patch0 或 %{patch0}引用
Prefix: %{_prefix}  这个主要是为了解决今后安装rpm包时, 并不一定把软件安装到rpm中打包的目录的情况。这样, 必须在这里定义该标识, 并在编写%install脚本的时候引用, 才能实现rpm安装时重新指定位置的功能
Prefix: %{_sysconfdir} 这个原因和上面的一样, 但由于%{_prefix}指/usr, 而对于其他的文件, 例如/etc下的配置文件, 则需要用%{_sysconfdir}标识
Requires:  该rpm包所依赖的软件包名称, 可以用 ">=" 或 "<=" 表示大于或小于某一特定版本, 例如："libxxx-devel >= 1.1.1" 。 注意：">="号两边需用空格隔开, 而不同软件名称也用空格分开

%description: 软件的详细说明
%define:      预定义的变量, 例如定义日志路径: _logpath /var/log/weblog
%prep:        预备参数, 通常为 %setup -q
%build:       编译参数 ./configure --user=nginx --group=nginx --prefix=/usr/local/nginx/……
%install:     安装步骤,此时需要指定安装路径, 创建编译时自动生成目录, 复制配置文件至所对应的目录中（这一步比较重要！）
%pre:         安装前需要做的任务, 如：创建用户
%post:        安装后需要做的任务 如：自动启动的任务
%preun:       卸载前需要做的任务 如：停止任务
%postun:      卸载后需要做的任务 如：删除用户, 删除/备份业务数据
%clean:       清除上次编译生成的临时文件, 就是上文提到的虚拟目录
%files:       设置文件属性, 包含编译文件需要生成的目录、文件以及分配所对应的权限
%changelog:   修改历史
```




需要注意的几点:


* 1. `${SOURCE_PATH}/contrib/redhat/sshd.pam` 中的内容不完整, 替换系统的 `/etc/pam.d/sshd` 后会引起 sshd 不可用, 需要在制作rpm包修改

    ```sh
    install -m644 contrib/redhat/sshd.pam     $RPM_BUILD_ROOT/etc/pam.d/sshd  # <= 注释此行
    # 
    SourceN: sshd.pam        # <= "简介节点" 处添加配置此行配置; N 为具体的数字, 根据实际情况配置
    install -m644 $RPM_SOURCE_DIR/sshd.pam    $RPM_BUILD_ROOT/etc/pam.d/sshd  # 将准备好的sshd pam配置文件放到 "rpmbuild/SOURCES/"
    ```

    ```sh
    CentOS 7.6 ~] cat /etc/pam.d/sshd
    #%PAM-1.0
    auth       required     pam_sepermit.so
    auth       substack     password-auth
    auth       include      postlogin
    # Used with polkit to reauthorize users in remote sessions
    -auth      optional     pam_reauthorize.so prepare
    account    required     pam_nologin.so
    account    include      password-auth
    password   include      password-auth
    # pam_selinux.so close should be the first session rule
    session    required     pam_selinux.so close
    session    required     pam_loginuid.so
    # pam_selinux.so open should only be followed by sessions to be executed in the user context
    session    required     pam_selinux.so open env_params
    session    required     pam_namespace.so
    session    optional     pam_keyinit.so force revoke
    session    include      password-auth
    session    include      postlogin
    # Used with polkit to reauthorize users in remote sessions
    -session   optional     pam_reauthorize.so prepare
    ```

chmod 600 /etc/ssh/ssh_host_*_key
sed -i -e 's/#PasswordAuthentication yes/PasswordAuthentication yes/g' /etc/ssh/sshd_config
sed -i -e 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/g' /etc/ssh/sshd_config
sed -i -e 's/#PermitEmptyPasswords no/PermitEmptyPasswords no/g'       /etc/ssh/sshd_config
sed -i -e 's/#UsePAM no/UsePAM yes/g'                                  /etc/ssh/sshd_config
# sed -i -e 's/#X11Forwarding no/X11Forwarding yes/g'                    /etc/ssh/sshd_config
sed -i -e '/KexAlgorithms/d'                                           /etc/ssh/sshd_config
sed -i -e '$a \KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org,diffie-hellman-group1-sha1,diffie-hellman-group14-sha1,diffie-hellman-group14-sha256,diffie-hellman-group16-sha512,diffie-hellman-group18-sha512,diffie-hellman-group-exchange-sha1,diffie-hellman-group-exchange-sha256,ecdh-sha2-nistp256,ecdh-sha2-nistp384,ecdh-sha2-nistp521,sntrup761x25519-sha512@openssh.com'                 /etc/ssh/sshd_config