# RPM macros

> https://docs.fedoraproject.org/en-US/packaging-guidelines/RPMMacros/

RPM provides a rich set of macros to make package maintenance simpler and consistent across packages. For example, it includes *a list of default path definitions* which are used by the build system macros, and definitions for RPM package build specific directories. They usually should be used instead of hard-coded directories. It also provides the default set of compiler flags as macros, which should be used when compiling manually and not relying on a build system.

```sh
~]$ rpm --eval "some text printed on %{_arch}"
some text printed on x86_64

~]$ rpm --define "test Hello, World!" --eval "%{test}"
Hello, World!
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