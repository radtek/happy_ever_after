# RPM打包 -- openssh为例

## 1. RPM打包工作目录

* 方式一: 安装 rpmdevtools 后执行 `rpmdev-setuptree` 后生成

    ```sh
    ~] yum install rpmdevtools

    ~] useradd rpmbuilder  # 非root用户下进行rpm打包
    ~] su - rpmbuilder

    ~]$ rpmdev-setuptree
    ~]$ tree rpmbuild/
    rpmbuild/
    ├── BUILD
    ├── RPMS
    ├── SOURCES
    ├── SPECS
    └── SRPMS
    ```

* 方式二: 手动创建

    ```sh
    mkdir -p rpmbuild/{BUILD,RPMS,SRPMS,SOURCES,SPECS}
    ```

**注: 工作目录介绍**

| Directory | Purpose |
| -- | -- |
| BUILD | When packages are built, various `%buildroot` directories are created here. This is useful for investigating a failed build if the logs output do not provide enough information. |
| RPMS  | Binary RPMs are created here, in subdirectories for different architectures, for example in subdirectories x86_64 and noarch. |
| SOURCES | Here, the packager puts compressed source code archives and patches. The `rpmbuild` command looks for them here. |
| SPECS   | The packager puts SPEC files here. |
| SRPMS   | When `rpmbuild` is used to build an SRPM instead of a binary RPM, the resulting SRPM is created here. |

## 2. 准备工作

### 2.1 SPEC文件

SPEC文件主体由两部分组成: + Body
*  Preamble(前言): The *Preamble* part contains a series of **metadata items** that are used in the Body part.
*  Body: The *Body* part represents the main part of the instructions.

#### Preamble Items

| SPEC Directive | Definition |
| -- | :-- |
| `Name` | The base name of the package, **which should match the SPEC file name**.  |
| `Version` | The upstream version number of the software.  |
| `Release` | The number of times this version of the software was released. <br>Normally, set the initial value to 1%{?dist}, and increment it with each new release of the package.  Reset to 1 when a new Version of the software is built. |
| `Summary` | A brief, one-line summary of the package. |
| `License` | The license of the software being packaged. GPLv2, GPLv3, BSD... |
| `URL`     | The full URL for more information about the program. Most often this is the upstream project website for the software being packaged. |
| `Source0` | Path or URL to the compressed archive of the upstream source code (unpatched, patches are handled elsewhere). <br>This should point to an accessible and reliable storage of the archive, for example, the upstream page and not the packager’s local storage. <br>If needed, more SourceX directives can be added, incrementing the number each time, for example: Source1, Source2, Source3, and so on. |
| `Patch` | The name of the first patch to apply to the source code if necessary. <br><br>The directive can be applied in two ways: with or without numbers at the end of Patch. <br><br>If no number is given, one is assigned to the entry internally. It is also possible to give the numbers explicitly using Patch0, Patch1, Patch2, Patch3, and so on. <br><br>These patches can be applied one by one using the `%patch0`, `%patch1`, `%patch2` macro and so on. <br>The macros are applied within the `%prep` directive in the *Body* section of the RPM SPEC file. <br>Alternatively, you can use the `%autopatch` macro which automatically applies all patches in the order they are given in the SPEC file. |
| `BuildArch` | If the package is not architecture dependent, for example, if written entirely in an interpreted programming language, set this to `BuildArch: noarch`. <br>If not set, the package automatically inherits(继承) the Architecture of the machine on which it is built, for example `x86_64`.
| `BuildRequires` | A comma(,) or whitespace-separated list of packages required for building the program written in a compiled language. <br>There can be multiple entries of `BuildRequires`, **each on its own line** in the SPEC file. |
| `Requires` | A comma-(,) or whitespace-separated list of packages required by the software to run once installed. <br>There can be multiple entries of `Requires`, **each on its own line** in the SPEC file. <br> Use "<=" and ">=", e.g.: `libxxx-devel >= 1.1.1`  |
| `ExcludeArch` | If a piece of software can not operate on a specific processor architecture, you can exclude that architecture here. |
| `Conflicts` | `Conflicts` are inverse to `Requires`. <br>If there is a package matching Conflicts, the package cannot be installed independently on whether the `Conflict` tag is on the package that has <u>already been installed</u> or on a package that is <u>going to be installed</u>. |
| `Obsoletes` | This directive alters the way updates work depending on whether the rpm command is used directly on the command line or the update is performed by an updates or dependency solver. <br>- When used on a command line, RPM removes all packages matching obsoletes of packages being installed. <br>- When using an update or dependency resolver, packages containing matching Obsoletes: are added as updates and replace the matching packages. |
| `Provides` | If `Provides` is added to a package, the package can be referred to by dependencies other than its name. |
|   |    |
| `Vendor` | 打包组织或者人员 |
| `Group` | 软件分组, 如`Applications/System`, `Applications/Internet`等 |
| `BuildRoot` | 这个是安装或编译时使用的临时目录, 即模拟安装完以后生成的文件目录：`BuildRoot: %_topdir/BUILDROOT`; 后面可使用 `$RPM_BUILD_ROOT`, `${buildroot}` 方式引用。 |
| `Prefix: %{_prefix}` | 这个主要是为了解决今后安装rpm包时, 并不一定把软件安装到rpm中打包的目录的情况。这样, 必须在这里定义该标识, 并在编写 `%install` 脚本的时候引用, 才能实现rpm安装时重新指定位置的功能 |
| `Prefix: %{_sysconfdir}` | 这个原因和上面的一样, 但由于 `%{_prefix}` 指 `/usr`, 而对于其他的文件, 例如 /etc 下的配置文件, 则需要用 `%{_sysconfdir}` 标识 |


`Name`, `Version`, 和 `Release`组成rpm软件包版本信息, 称为`NAME-VERSION-RELEASE`, `NVR` 或 `N-V-R`

```sh
~]$ rpm -qa bash 
bash-4.2.46-31.el7.x86_64
```

#### Body Items

| SPEC Directive | Definition |
| -- | :-- |
| `%description` | A full description of the software packaged in the RPM. This description can span multiple lines and can be broken into paragraphs. |
| `%prep` | Command or series of commands to prepare the software to be built, for example, unpacking the archive in `Source0`. <br>This directive can contain a **shell script**. |
| `%build` | Command or series of commands for building the software into **machine code** (for compiled languages) or **byte code** (for some interpreted languages). <br>configure, make |
| `%install` | Command or series of commands for copying the desired build artifacts from the `%builddir` (*where the build happens*) to the `%buildroot` directory (*which contains the directory structure with the files to be packaged*). <br>This usually means copying files from `~/rpmbuild/BUILD` to `~/rpmbuild/BUILDROOT` and creating the necessary directories in `~/rpmbuild/BUILDROOT`. <br>This is only run when creating a package, not when the end-user installs the package. <br>make install |
| `%check` | Command or series of commands to test the software. This normally includes things such as unit tests. |
| `%files` | The list of files that will be installed in the end user’s system. |
| `%changelog` | A record of changes that have happened to the package between different `Version` or `Release` builds. |


* Scriptlet

| Directive | Definition |
| -- | :-- |
| `%pre` | Scriptlet that is executed just before installing the package on the target system. |
| `%post` | Scriptlet that is executed just after the package was installed on the target system. |
| `%preun` | Scriptlet that is executed just before uninstalling the package from the target system. |
| `%postun` | Scriptlet that is executed just after the package was uninstalled from the target system. |
| `%pretrans` | Scriptlet that is executed just before installing or removing *any package*. |
| `%posttrans` | Scriptlet that is executed at the end of the transaction. |

* macros

> Refer to: [RPM-macros](./Linux-rpm-macros.md)

* `e.g.` An example SPEC file for the bello program written in bash

    ```spec
    Name:           bello
    Version:        0.1
    Release:        1%{?dist}
    Summary:        Hello World example implemented in bash script

    License:        GPLv3+
    URL:            https://www.example.com/%{name}
    Source0:        https://www.example.com/%{name}/releases/%{name}-%{version}.tar.gz

    Requires:       bash

    BuildArch:      noarch

    %description
    The long-tail description for our Hello World Example implemented in
    bash script.

    %prep
    %setup -q

    %build

    %install

    mkdir -p %{buildroot}/%{_bindir}

    install -m 0755 %{name} %{buildroot}/%{_bindir}/%{name}

    %files
    %license LICENSE
    %{_bindir}/%{name}

    %changelog
    * Tue May 31 2016 Adam Miller <maxamillion@fedoraproject.org> - 0.1-1
    - First bello package
    - Example second item in the changelog for version-release 0.1-1
    ```

* `e.g.` An example SPEC file for the pello program written in Python

    ```spec
    Name:           pello
    Version:        0.1.1
    Release:        1%{?dist}
    Summary:        Hello World example implemented in Python

    License:        GPLv3+
    URL:            https://www.example.com/%{name}
    Source0:        https://www.example.com/%{name}/releases/%{name}-%{version}.tar.gz

    BuildRequires:  python
    Requires:       python
    Requires:       bash

    BuildArch:      noarch

    %description
    The long-tail description for our Hello World Example implemented in Python.

    %prep
    %setup -q

    %build

    python -m compileall %{name}.py

    %install

    mkdir -p %{buildroot}/%{_bindir}
    mkdir -p %{buildroot}/usr/lib/%{name}

    cat > %{buildroot}/%{_bindir}/%{name} <←EOF
    #!/bin/bash
    /usr/bin/python /usr/lib/%{name}/%{name}.pyc
    EOF

    chmod 0755 %{buildroot}/%{_bindir}/%{name}

    install -m 0644 %{name}.py* %{buildroot}/usr/lib/%{name}/

    %files
    %license LICENSE
    %dir /usr/lib/%{name}/
    %{_bindir}/%{name}
    /usr/lib/%{name}/%{name}.py*

    %changelog
    * Tue May 31 2016 Adam Miller <maxamillion@fedoraproject.org> - 0.1.1-1
    - First pello package
    ```

* `e.g.` An example SPEC file for the cello program written in C

    ```spec
    Name:           cello
    Version:        1.0
    Release:        1%{?dist}
    Summary:        Hello World example implemented in C

    License:        GPLv3+
    URL:            https://www.example.com/%{name}
    Source0:        https://www.example.com/%{name}/releases/%{name}-%{version}.tar.gz

    Patch0:         cello-output-first-patch.patch

    BuildRequires:  gcc
    BuildRequires:  make

    %description
    The long-tail description for our Hello World Example implemented in
    C.

    %prep
    %setup -q

    %patch0

    %build
    make %{?_smp_mflags}

    %install
    %make_install

    %files
    %license LICENSE
    %{_bindir}/%{name}

    %changelog
    * Tue May 31 2016 Adam Miller <maxamillion@fedoraproject.org> - 1.0-1
    - First cello package
    ```



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