# RPM macros

> https://docs.fedoraproject.org/en-US/packaging-guidelines/RPMMacros/

RPM provides a rich set of macros to make package maintenance simpler and consistent across packages. For example, it includes *a list of default path definitions* which are used by the build system macros, and definitions for RPM package build specific directories. They usually should be used instead of hard-coded directories. It also provides the default set of compiler flags as macros, which should be used when compiling manually and not relying on a build system.

```sh
~]$ rpm --eval "some text printed on %{_arch}"
some text printed on x86_64

~]$ rpm --define 'test Hello, World!' --eval "%{test}"
Hello, World!
```

宏定义相关的文件(共两类): 

* 1.直接定义类

    ```sh
    # 优先级顺序如下
    1. 当前文件中定义: 如spec文件中 %define dist .centos
    2. 命令中定义: rpm --define "_arch my_arch" --eval "%{_arch}"
    3. 用户自定义相关:  ~/.rpmmacros
    4. 系统相关的配置:  /etc/rpm/
    5. 全局扩展配置:   /usr/lib/rpm/macros.d/*
    6. 全局的配置:     /usr/lib/rpm/macros, /usr/lib/rpm/redhat/macros
    ```

* 2.通过macrofiles引用类

    ```sh
    /usr/lib/rpm/rpmrc
    /usr/lib/rpm/redhat/rpmrc
    /etc/rpmrc
    ~/.rpmrc

    # rpmrc主要是用来定义一些跟平台特型相关的一些选项: 如optflags引用的是"i686" ，则optflags的值就是: "-O2 -g -march=i686"
    optflags: i386 -O2 -g -march=i386 -mtune=i686
    optflags: i686 -O2 -g -march=i686
    ```

定义macrofiles:

> 注: 需要在编译阶段定义 `MACROFILES`，否则会加载默认的路径

```sh
macrofiles: /usr/lib/rpm/macros:/etc/rpm/macros
```


## Macros for paths set and used by build systems

The macros for build system invocations (for example, `%configure`, `%cmake`, or `%meson`) use the values defined by RPM to set installation paths for packages. So, it’s usually preferable to not hard-code these paths in spec files either, but use the same macros for consistency.

> The values for these macros can be inspected by looking at `/usr/lib/rpm/platform/*/macros` for the respective platform.

The following table lists macros which are widely used in fedora `.spec` files.

| macro | definition | comment |
| -- | -- | -- |
| `%{_sysconfdir}` | `/etc` |  |
| `%{_prefix}` | `/usr` | can be defined to /app for flatpak builds |
| `%{_exec_prefix}` | `%{_prefix}` | default: `/usr` |
| `%{_includedir}` | `%{_prefix}/include` | default: `/usr/include` |
| `%{_bindir}` | `%{_exec_prefix}/bin` | default: `/usr/bin` |
| `%{_libdir}` | `%{_exec_prefix}/%{_lib}` | default: `/usr/%{_lib}` |
| `%{_libexecdir}` | `%{_exec_prefix}/libexec` | default: `/usr/libexec` |
| `%{_sbindir}` | `%{_exec_prefix}/sbin` | default: `/usr/sbin` |
| `%{_datadir}` | `%{_datarootdir}` | default: `/usr/share` |
| `%{_infodir}` | `%{_datarootdir}/info` | default: `/usr/share/info` |
| `%{_mandir}` | `%{_datarootdir}/man` | default: `/usr/share/man` |
| `%{_docdir}` | `%{_datadir}/doc` | default: `/usr/share/doc` |
| `%{_rundir}` | `/run` |  |
| `%{_localstatedir}` | `/var` |  |
| `%{_sharedstatedir}` | `/var/lib` |  |
| `%{_lib}` | `lib64` | lib on *32bit* platforms |

Some seldomly used macros are listed below for completeness. Old `.spec` files might still use them, and there might be cases where they are still needed.

| macro | definition | comment |
| -- | -- | -- |
| `%{_datarootdir}` | `%{_prefix}/share` | default: `/usr/share` |
| `%{_var}` | `/var` |  |
| `%{_tmppath}` | `%{_var}/tmp` | default: `/var/tmp` |
| `%{_usr}` | `/usr` |  |
| `%{_usrsrc}` | `%{_usr}/src` | default: `/usr/src` |
| `%{_initddir}` | `%{_sysconfdir}/rc.d/init.d` | default: `/etc/rc.d/init.d` |
| `%{_initrddir}` | `%{_initddir}` | old misspelling, provided for compatiblity |

## Macros set for the RPM (and SRPM) build process

RPM also exposes the locations of several directories that are relevant to the package build process via macros.

The only macro that’s widely used in `.spec` files is `%{buildroot}`, which points to the root of the installation target directory. It is used for setting `DESTDIR` in the package’s `%install` step.

The other macros are usually only used outside `.spec` files. For example, they are set by `fedpkg` to override the default directories.


| macro | definition | comment |
| -- | -- | -- |
| `%{buildroot}` | `%{_buildrootdir}/%{name}-%{version}-%{release}.%{_arch}` | same as `$BUILDROOT` |
| `%{_topdir}` | `%{getenv:HOME}/rpmbuild` |  |
| `%{_builddir}` | `%{_topdir}/BUILD` |  |
| `%{_rpmdir}` | `%{_topdir}/RPMS` |  |
| `%{_sourcedir}` | `%{_topdir}/SOURCES` |  |
| `%{_specdir}` | `%{_topdir}/SPECS` |  |
| `%{_srcrpmdir}` | `%{_topdir}/SRPMS` |  |
| `%{_buildrootdir}` | `%{_topdir}/BUILDROOT` |  |

## Macros providing compiler and linker flags

The default build flags for binaries on fedora are also available via macros. They are used by the build system macros to setup the build environment, so it is usually not necessary to use them directly — except, for example, when doing bare bones compilation with `gcc` directly.

The set of flags listed below reflects the current state of fedora 28 on a `x86_64` machine, as defined in the file `/usr/lib/rpm/redhat/macros`.

The `%{optflags}` macro contains flags that determine `CFLAGS`, `CXXFLAGS`, `FFLAGS`, etc. — the `%{__global_cflags}` macro evaluates to the same string.

The current definitions of these values can be found in the `redhat-rpm-macros package`, in the [build flags documentation](https://src.fedoraproject.org/rpms/redhat-rpm-config//blob/rawhide/f/buildflags.md).

```sh
~]$ rpm --eval "%{optflags}"
-O2 -g -pipe -Wall -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -Wp,-D_GLIBCXX_ASSERTIONS -fexceptions -fstack-protector-strong -grecord-gcc-switches -specs=/usr/lib/rpm/redhat/redhat-hardened-cc1 -specs=/usr/lib/rpm/redhat/redhat-annobin-cc1 -m64 -mtune=generic -fasynchronous-unwind-tables -fstack-clash-protection -fcf-protection
```

The value of the `LDFLAGS` environment variable set by build systems is determined by the `%{build_ldflags}` macro:

```sh
~]$ rpm -E "%{build_ldflags}"
-Wl,-z,relro  -Wl,-z,now -specs=/usr/lib/rpm/redhat/redhat-hardened-ld
```

## 宏定义与修改

* spec文件里面定义:

    ```spec
    %define macro_name value
    %define macro_name %(data)
    ```

* spec文件中使用方法:

    ```spec
    %macro_name
    %macro_name 1 2 3 # 1，2，3为参数传递给宏
    %0                # 宏名字
    %*                # 传递给宏的所有参数
    %#                # 传递给宏的参数个数
    %1                # 参数1
    %2                # 参数2
    ```

* 命令行使用 `--define`
 
    ```sh
    rpm --define "dist my_dist" --eval "%{dist}"
    rpmbuild -bs name.spec --define "dist x86_64"
    ```

## 宏语法

> [https://rpm-software-management.github.io/rpm/manual/macros.html](https://rpm-software-management.github.io/rpm/manual/macros.html)

* Defining a Macro

    ```spec
    %define <name>[(opts)] <body>
    ```

    * All whitespace surrounding `<body>` is removed.
    * Name may be composed of alphanumeric(`0-9,a-z,A-Z`) characters, and the character "`_`" and must be **at least 3 characters** in length.
    * A macro without an (opts) field is "simple" in that only recursive macro expansion is performed. A parameterized macro contains an (opts) field. "–" as opts disables all option processing, otherwise the opts (i.e. string between parentheses) are passed exactly as is to `getopt(3)` for argc/argv processing at the beginning of a macro invocation. 
    * "–" can be used to separate options from arguments. While a parameterized macro is being expanded, the following shell-like macros are available:

        ```spec
        %0       the name of the macro being invoked
        %*       all arguments (unlike shell, not including any processed flags)
        %#       the number of arguments
        %{-f}    if present at invocation, the flag f itself
        %{-f*}   if present at invocation, the argument to flag f
        %1, %2   the arguments themselves (after getopt(3) processing)
        ```

    * Within the body of a macro, there are several constructs that permit testing for the presence of optional parameters. 

        * The simplest construct is "`%{-f}`" which expands (literally) to "`-f`" if `-f` was mentioned when the macro was invoked. 
        * There are also provisions for including text if flag was present using "`%{-f:X}`". This macro expands to (the expansion of) `X` if the flag was present. 
        * The negative form, "`%{!-f:Y}`", expanding to (the expansion of) `Y` if `-f` was not present, is also supported.
        * In addition to the "`%{…}`" form, shell expansion can be performed using "`%(shell command)`".

* Builtin Macros

There are several builtin macros (with reserved names) that are needed to perform useful operations. The current list is:

```sh
    %trace          toggle print of debugging information before/after expansion
    %dump           print the active (i.e. non-covered) macro table
    %getncpus       return the number of CPUs
    %getconfdir     expand to rpm "home" directory (typically /usr/lib/rpm)
    %dnl            discard to next line (without expanding)
    %verbose        expand to 1 if rpm is in verbose mode, 0 if not
    %{verbose:...}  expand to ... if rpm is in verbose mode, the empty string if not

    %{echo:...}    print ... to stdout
    %{warn:...}    print warning: ... to stderr
    %{error:...}    print error: ... to stderr and return an error
 
    %define ...    define a macro
    %undefine ...  undefine a macro
    %global ...    define a macro whose body is available in global context

    %{macrobody:...}    literal body of a macro

    %{basename:...}   basename(1) macro analogue
    %{dirname:...}    dirname(1) macro analogue
    %{exists:...}     test file existence, expands to 1/0
    %{suffix:...}     expand to suffix part of a file name
    %{url2path:...}   convert url to a local path
    %{getenv:...}     getenv(3) macro analogue
    %{uncompress:...} expand ... to <file> and test to see if <file> is compressed. The expansion is
                cat <file>        # if not compressed
                gzip -dc <file>   # if gzip'ed
                bzip2 -dc <file>  # if bzip'ed

                e.g. ~]$ rpm --eval "%{uncompress:pello-0.1.1.tar.gz}"
                     /usr/bin/gzip -dc pello-0.1.1.tar.gz

    %{load:...}      load a macro file
    %{lua:...}       expand using the [embedded Lua interpreter](/rpm/manual/lua.html)
    %{expand:...}    like eval, expand ... to <body> and (re-)expand <body>
    %{expr:...}      evaluate an expression
    %{shescape:...}  single quote with escapes for use in shell
    %{shrink:...}    trim leading and trailing whitespace, reduce intermediate whitespace to a single space
    %{quote:...}     quote a parametric macro argument, needed to pass empty strings or strings with whitespace

    %{S:...}   expand ... to <source> file name
    %{P:...}   expand ... to <patch> file name
```