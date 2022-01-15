- rpm安装
- 编译安装

## rpm安装

yum的repo配置文件参考如下：

```
[nginx-stable]
name=nginx stable
baseurl=https://nginx.org/packages/rhel/$releasever/$basearch
enabled=1
gpgcheck=0
```

## 编译安装

> 以当前最新版 `nginx-1.20.0.tar.gz` 为例

> gzip模块需要 zlib 库  
> rewrite模块需要pcre 库  
> ssl 功能需要openssl库  

### 01 下载

按需求选择版本, 下载地址: [https://nginx.org/en/download.html](https://nginx.org/en/download.html)

- `stable`: 最新稳定版
- `mainline`: 当前主线开发版
- `legacy`: 历史版本

### 02 编译环境准备

- 安装 make

```sh
yum -y install gcc automake autoconf libtool make
```

- 安装 g++

```sh
yum -y install gcc-c++
```

### 方式一: 手动指定 pcre, zlib 源码路径, nginx 编译过程中编译 pcre 和 zlib (甚至openssl), 可以认为是将 pcre 和 zlib 内置

```bash
shell> ./configure --prefix=/usr/local/nginx-1.20.0 \
            --with-http_ssl_module  \
            --with-http_stub_status_module  \
            --with-http_gzip_static_module  \
            --with-pcre=/root/pcre-8.44 \
            --with-zlib=/root/zlib-1.2.11 \
            --with-openssl=/root/openssl-1.1.1k
```

- 注1： --with-pcre、--with-zlib、--with-openssl 指定的都是源码路径，而不是编译安装后的

- 注2：执行完 ./configure, 可以手动编辑 objs/Makefile 修改 pcre、openssl 的编译参数

```sh
shell> vi objs/Makefile

...
/root/pcre-8.44/pcre.h: /root/pcre-8.44/Makefile

/root/pcre-8.44/Makefile:       objs/Makefile
        cd /root/pcre-8.44 \
        && if [ -f Makefile ]; then $(MAKE) distclean; fi \
        && CC="$(CC)" CFLAGS="-O2 -fomit-frame-pointer -pipe " \
        ./configure --disable-shared  # <= 按需添加, 如 --enable-utf8 --enable-unicode-properties --enable-pcre16 --enable-pcre32

/root/pcre-8.44/.libs/libpcre.a:        /root/pcre-8.44/Makefile
        cd /root/pcre-8.44 \
        && $(MAKE) libpcre.la


/root/openssl-1.1.1k/.openssl/include/openssl/ssl.h:    objs/Makefile
        cd /root/openssl-1.1.1k \
        && if [ -f Makefile ]; then $(MAKE) clean; fi \
        && ./config --prefix=/root/openssl-1.1.1k/.openssl no-shared no-threads  \  # <= 此处路径如果要修改, 改动的地方较大，参考以下附
        && $(MAKE) \
        && $(MAKE) install_sw LIBDIR=lib


/root/zlib-1.2.11/libz.a:       objs/Makefile
        cd /root/zlib-1.2.11 \
        && $(MAKE) distclean \
        && CFLAGS="-O2 -fomit-frame-pointer -pipe " CC="$(CC)" \
                ./configure \
        && $(MAKE) libz.a
...
```

```
shell> make && make install
```

```sh
[root@nginx-02 nginx-1.20.0]# ./sbin/nginx -V
nginx version: nginx/1.20.0
built by gcc 4.8.5 20150623 (Red Hat 4.8.5-44) (GCC) 
built with OpenSSL 1.1.1k  25 Mar 2021
TLS SNI support enabled
configure arguments: --prefix=/usr/local/nginx-1.20.0 --with-http_ssl_module --with-http_stub_status_module --with-http_gzip_static_module --with-pcre=/root/pcre-8.44 --with-zlib=/root/zlib-1.2.11 --with-openssl=/root/openssl-1.1.1k
```

**附**: 修改内置openssl编译路径

```x
...
   8 ALL_INCS = -I src/core \
    ........
  12         -I /root/pcre-8.44 \
  13         -I /root/openssl-1.1.1k/.openssl/include \                                                   <=
  14         -I /root/zlib-1.2.11 \
...
  20 CORE_DEPS = src/core/nginx.h \
    ........
  80         src/core/ngx_regex.h \
  81         /root/pcre-8.44/pcre.h \
  82         /usr/local/nginx-1.20.0/.openssl-1.1.1k/include/openssl/ssl.h \                              <=
  83         objs/ngx_auto_config.h
...
  86 CORE_INCS = -I src/core \
    ........
  90         -I /root/pcre-8.44 \
  91         -I /usr/local/nginx-1.20.0/.openssl-1.1.1k/include \                                         <=
...
 117 objs/nginx:     objs/src/core/nginx.o \
    ........
 370         objs/ngx_modules.o \                                                                         <👇
 371         -ldl -lpthread -lcrypt /root/pcre-8.44/.libs/libpcre.a /usr/local/nginx-1.20.0/.openssl-1.1.1k/lib/libssl.a /usr/local/nginx-1.20.0/.openssl-1.1.1k/lib/libcrypto.a -ldl -lpthread /root/zlib-1.2.11/libz.a \
 372         -Wl,-En
...
1266 /usr/local/nginx-1.20.0/.openssl-1.1.1k/include/openssl/ssl.h:  objs/Makefile                        <=
1267         cd /root/openssl-1.1.1k \
1268         && if [ -f Makefile ]; then $(MAKE) clean; fi \
1269         && ./config --prefix=/usr/local/nginx-1.20.0/.openssl-1.1.1k no-shared no-threads  \         <=
1270         && $(MAKE) \
1271         && $(MAKE) install_sw LIBDIR=lib
```


### 方式二: 单独编译pcre, zlib, openssl, nginx识别调用

pcre, zlib, openssl编译见下文

nginx编译:

```sh
./configure --prefix=/usr/local/nginx-1.20.0 \
            --with-http_ssl_module  \
            --with-http_stub_status_module  \
            --with-http_gzip_static_module

make
make install
```

```
[root@nginx-02 nginx-1.20.0]# ./sbin/nginx -V
nginx version: nginx/1.20.0
built by gcc 4.8.5 20150623 (Red Hat 4.8.5-44) (GCC) 
built with OpenSSL 1.1.1k  25 Mar 2021
TLS SNI support enabled
configure arguments: --prefix=/usr/local/nginx-1.20.0 --with-http_ssl_module --with-http_stub_status_module --with-http_gzip_static_module
```

### 01 安装pcre库

- 方式一: 通过rpm安装

```sh
yum install pcre pcre-devel
```

- 方式二: 通过编译安装

下载地址: [https://ftp.pcre.org/pub/pcre/](https://ftp.pcre.org/pub/pcre/)

```x
# 1. 解压

shell> tar xf pcre-8.44.tar.gz

# 2. configure

shell> cd ./pcre-8.44
shell> ./configure --prefix=/usr/local/pcre-8.44 --enable-utf8 --enable-unicode-properties --enable-pcre16 --enable-pcre32

    # 指定man, doc文档的存放位置, 默认位置在源码包路径下, 一般安装完成以后会清理掉, 建议添加
    # shell> ./configure --prefix=/usr/local/pcre-8.44 --enable-utf8 --enable-unicode-properties --enable-pcre16 --enable-pcre32 --mandir=/usr/local/pcre-8.44/man --docdir=/usr/local/pcre-8.44/doc

# 3. 编译, 安装

shell> make
shell> make check  # 检查编译结果(非必须)
shell> make install

# 4. 加载lib
## 加载pcre主体库

shell> echo '/usr/local/pcre-8.44/lib/' > /etc/ld.so.conf.d/pcre-8.44.conf

## 创建软链到/usr/lib64: 
##     观察rpm版本的pcre-devel的包结构可以发现, 实际pcre-devel并没有安装新的lib，而是新建一些软链到/usr/lib64/
##     为了满足nginx编译时的检查，此处可以手动创建软链

shell> ln -sf /usr/local/pcre-8.44/lib/libpcre.so /usr/lib64/libpcre.so
shell> ln -sf /usr/local/pcre-8.44/lib/libpcrecpp.so /usr/lib64/libpcrecpp.so 
shell> ln -sf /usr/local/pcre-8.44/lib/libpcreposix.so /usr/lib64/libpcreposix.so
shell> ln -sf /usr/local/pcre-8.44/lib/libpcre16.so /usr/lib64/libpcre16.so 
shell> ln -sf /usr/local/pcre-8.44/lib/libpcre32.so /usr/lib64/libpcre32.so 

shell> ldconfig

# 5. 配置头文件
## 头文件均通过软链模式放置到/usr/include

shell> cd /usr/local/pcre-8.44/include/
shell> for item in $(ls);do ln -s /usr/local/pcre-8.44/include/${item} /usr/include/${item};done
```

###  02 安装zlib库

- 方式一: 通过rpm安装

```sh
yum install zlib zlib-devel
```

- 方式二: 通过编译安装

下载地址: [http://zlib.net/zlib-1.2.11.tar.gz](http://zlib.net/zlib-1.2.11.tar.gz)

```sh
./configure --prefix=/usr/local/zlib-1.2.11
make
make check
make install

echo '/usr/local/zlib-1.2.11/lib/' > /etc/ld.so.conf.d/zlib-1.2.11.conf
ln -sf /usr/local/zlib-1.2.11/lib/libz.so /usr/lib64/libz.so   #同pcre-devel, zlib-devel包中的lib64目录下只有一个软链

cd /usr/local/zlib-1.2.11/include
for item in $(ls);do ln -s /usr/local/zlib-1.2.11/include/${item} /usr/include/${item};done

ldconfig
```

###  03 安装ssl库

此处选择openssl

- 方式一: 通过rpm安装

```sh
yum install openssl-libs openssl-devel
```

- 方式二: 通过编译安装

```sh
# 使用的是编译的zlib
./config --prefix=/usr/local/openssl-1.1.1k --openssldir=/usr/local/openssl-1.1.1k zlib shared --with-zlib-include=/usr/local/zlib-1.2.11/include --with-zlib-lib=/usr/local/zlib-1.2.11/lib

# 使用rpm安装的zlib-devel或者按照上面配置了include和lib64软链的，可直接使用以下
./config --prefix=/usr/local/openssl-1.1.1k --openssldir=/usr/local/openssl-1.1.1k zlib shared

make
make install

echo "/usr/local/openssl-1.1.1k/lib" > /etc/ld.so.conf.d/openssl-1.1.1k.conf      # ld.conf
ln -sf /usr/local/openssl-1.1.1k/lib/libcrypto.so /usr/lib64/libcrypto.so         # lib64
ln -sf /usr/local/openssl-1.1.1k/lib/libssl.so /usr/lib64/libssl.so               # lib64

ln -sf /usr/local/openssl-1.1.1k/include/openssl /usr/include/openssl             # include

ldconfig
```

**附1**: nginx源码包结构

```
[root@nginx-01 nginx-1.20.0]# ls -l 
total 784
-rw-r--r--. 1 1001 1001 311102 Apr 20 21:35 CHANGES     <= 版本变化
-rw-r--r--. 1 1001 1001 474697 Apr 20 21:35 CHANGES.ru
-rw-r--r--. 1 1001 1001   1397 Apr 20 21:35 LICENSE
-rw-r--r--. 1 1001 1001     49 Apr 20 21:35 README
drwxr-xr-x. 6 1001 1001   4096 May  9 23:03 auto        <=检测系统模块依赖关系
drwxr-xr-x. 2 1001 1001    168 May  9 23:03 conf        <=存放配置文件
-rwxr-xr-x. 1 1001 1001   2590 Apr 20 21:35 configure
drwxr-xr-x. 4 1001 1001     72 May  9 23:03 contrib     <=提供vim插件配置和两个脚本geo2nginx.pl、unicode2nginx
drwxr-xr-x. 2 1001 1001     40 May  9 23:03 html        <=存放标准的html页面文件
drwxr-xr-x. 2 1001 1001     21 May  9 23:03 man         <=man文档
drwxr-xr-x. 9 1001 1001     91 May  9 23:03 src         <=nginx源码
```

**附2**: nginx编译参数

|              参数                  |              解释                 |
|  :-------------------------------  | :--------------------------------|
|  通用配置选项:                      |                                  |
|  --prefix=PATH                     | set installation prefix          |
|  --sbin-path=PATH                  | set nginx binary pathname        |
|  --modules-path=PATH               | set modules path                 |
|  --conf-path=PATH                  | set nginx.conf pathname          |
|  --error-log-path=PATH             | set error log pathname           |
|  --pid-path=PATH                   | set nginx.pid pathname           |
|  --lock-path=PATH                  | set nginx.lock pathname          |
|  --user=USER                       | set non-privileged user for work |
|  --group=GROUP                     | set non-privileged group for worker processes  |
|  优化编译选项:                      |                             |
|  --with-cc=PATH                    | set C compiler pathname(设置C编译器路径, 默认用PATH中的)  |
|  --with-cpp=PATH                   | set C preprocessor pathname(设置C预处理路径)             |
|  --with-cc-opt=OPTIONS             | set additional C compiler options                       |
|  --with-ld-opt=OPTIONS             | set additional linker options                           |
|  --with-cpu-opt=CPU                | build for the specified CPU, valid values:              |
|                                    | pentium, pentiumpro, pentium3, pentium4, athlon, opteron, sparc32, sparc64, ppc64  |
|  邮件代理配置选项:                  |                                      |
|  --with-mail                       | enable POP3/IMAP4/SMTP proxy module  |
|  --with-mail=dynamic               | enable dynamic POP3/IMAP4/SMTP proxy module              |
|  --with-mail_ssl_module            | enable ngx_mail_ssl_module                               |
|  --without-mail_pop3_module        | disable ngx_mail_pop3_module                             |
|  --without-mail_imap_module        | disable ngx_mail_imap_module   |
|  --without-mail_smtp_module        | disable ngx_mail_smtp_module   |
|  http配置选项:                      |                                 |
|  --without-http                    | disable HTTP server               |
|  --without-http-cache              | disable HTTP cache                 |
|  --with-perl=PATH                  | set perl binary pathname          |
|  --with-perl_modules_path=PATH     | set Perl modules path             |
|  --with-http_perl_module           | enable ngx_http_perl_module       |
|  --with-http_perl_module=dynamic   | enable dynamic ngx_http_perl_module   |
|  --http-log-path=PATH              | set http access log pathname          |
|  --http-client-body-temp-path=PATH | set path to store http client request body temporary files   |
|  --http-proxy-temp-path=PATH       | set path to store http proxy temporary files   |
|  --http-fastcgi-temp-path=PATH     | set path to store http fastcgi temporary files      |
|  --http-uwsgi-temp-path=PATH       | set path to store http uwsgi temporary files        |
|  --http-scgi-temp-path=PATH        | set path to store http scgi temporary files         |
| 适当配置--with-<module-name>_module启动相应模块: | |
|  --with-http_ssl_module                  | enable ngx_http_ssl_module |
|  --with-http_v2_module                   | enable ngx_http_v2_module |
|  --with-http_realip_module               | enable ngx_http_realip_module |
|  --with-http_addition_module             | enable ngx_http_addition_module |
|  --with-http_xslt_module                 | enable ngx_http_xslt_module |
|  --with-http_xslt_module=dynamic         | enable dynamic ngx_http_xslt_module |
|  --with-http_image_filter_module         | enable ngx_http_image_filter_module |
|  --with-http_image_filter_module=dynamic | enable dynamic ngx_http_image_filter_module |
|  --with-http_geoip_module                | enable ngx_http_geoip_module |
|  --with-http_geoip_module=dynamic        | enable dynamic ngx_http_geoip_module |
|  --with-http_sub_module                  | enable ngx_http_sub_module |
|  --with-http_dav_module                  | enable ngx_http_dav_module |
|  --with-http_flv_module                  | enable ngx_http_flv_module |
|  --with-http_mp4_module                  | enable ngx_http_mp4_module |
|  --with-http_gunzip_module               | enable ngx_http_gunzip_module |
|  --with-http_gzip_static_module          | enable ngx_http_gzip_static_module |
|  --with-http_auth_request_module         | enable ngx_http_auth_request_module |
|  --with-http_random_index_module         | enable ngx_http_random_index_module |
|  --with-http_secure_link_module          | enable ngx_http_secure_link_module |
|  --with-http_degradation_module          | enable ngx_http_degradation_module |
|  --with-http_slice_module                | enable ngx_http_slice_module |
|  --with-http_stub_status_module          | enable ngx_http_stub_status_module |
| 适当配置--without-<module-name>_module禁用相应模块:  | |
|  --without-http_charset_module       | disable ngx_http_charset_module |
|  --without-http_gzip_module          | disable ngx_http_gzip_module |
|  --without-http_ssi_module           | disable ngx_http_ssi_module |
|  --without-http_userid_module        | disable ngx_http_userid_module |
|  --without-http_access_module        | disable ngx_http_access_module |
|  --without-http_auth_basic_module    | disable ngx_http_auth_basic_module |
|  --without-http_mirror_module        | disable ngx_http_mirror_module |
|  --without-http_autoindex_module     | disable ngx_http_autoindex_module |
|  --without-http_geo_module           | disable ngx_http_geo_module |
|  --without-http_map_module           | disable ngx_http_map_module |
|  --without-http_split_clients_module | disable ngx_http_split_clients_module |
|  --without-http_referer_module      | disable ngx_http_referer_module |
|  --without-http_rewrite_module      | disable ngx_http_rewrite_module |
|  --without-http_proxy_module        | disable ngx_http_proxy_module |
|  --without-http_fastcgi_module      | disable ngx_http_fastcgi_module |
|  --without-http_uwsgi_module        | disable ngx_http_uwsgi_module |
|  --without-http_scgi_module         | disable ngx_http_scgi_module |
|  --without-http_grpc_module         | disable ngx_http_grpc_module |
|  --without-http_memcached_module    | disable ngx_http_memcached_module |
|  --without-http_limit_conn_module   | disable ngx_http_limit_conn_module |
|  --without-http_limit_req_module    | disable ngx_http_limit_req_module |
|  --without-http_empty_gif_module    | disable ngx_http_empty_gif_module |
|  --without-http_browser_module      | disable ngx_http_browser_module |
|  --without-http_upstream_hash_module    | disable ngx_http_upstream_hash_module |
|  --without-http_upstream_ip_hash_module | disable ngx_http_upstream_ip_hash_module |
|  --without-http_upstream_least_conn_module | disable ngx_http_upstream_least_conn_module |
|  --without-http_upstream_random_module     | disable ngx_http_upstream_random_module |
|  --without-http_upstream_keepalive_module  | disable ngx_http_upstream_keepalive_module |
|  --without-http_upstream_zone_module       | disable ngx_http_upstream_zone_module |
| 其他选项: |             |
|  --build=NAME                            | set build name |
|  --builddir=DIR                          | set build directory |
|  --with-select_module                    | enable select module |
|  --without-select_module                 | disable select module |
|  --with-poll_module                      | enable poll module |
|  --without-poll_module                   | disable poll module |
|  --with-threads                          | enable thread pool support |
|  --with-file-aio                         | enable file AIO support |
|  --with-stream                                | enable TCP/UDP proxy module |
|  --with-stream=dynamic                        | enable dynamic TCP/UDP proxy module |
|  --with-stream_ssl_module                     | enable ngx_stream_ssl_module |
|  --with-stream_realip_module                  | enable ngx_stream_realip_module |
|  --with-stream_geoip_module                   | enable ngx_stream_geoip_module |
|  --with-stream_geoip_module=dynamic           | enable dynamic ngx_stream_geoip_module |
|  --with-stream_ssl_preread_module             | enable ngx_stream_ssl_preread_module |
|  --without-stream_limit_conn_module           | disable ngx_stream_limit_conn_module |
|  --without-stream_access_module               | disable ngx_stream_access_module |
|  --without-stream_geo_module                  | disable ngx_stream_geo_module |
|  --without-stream_map_module                  | disable ngx_stream_map_module |
|  --without-stream_split_clients_module        | disable ngx_stream_split_clients_module |
|  --without-stream_return_module               | disable ngx_stream_return_module |
|  --without-stream_set_module                  | disable ngx_stream_set_module |
|  --without-stream_upstream_hash_module        | disable ngx_stream_upstream_hash_module |
|  --without-stream_upstream_least_conn_module  | disable ngx_stream_upstream_least_conn_module |
|  --without-stream_upstream_random_module      | disable ngx_stream_upstream_random_module |
|  --without-stream_upstream_zone_module        | disable ngx_stream_upstream_zone_module |
|  --with-google_perftools_module               | enable ngx_google_perftools_module |
|  --with-cpp_test_module                       | enable ngx_cpp_test_module |
|  --add-module=PATH                            | enable external module |
|  --add-dynamic-module=PATH                    | enable dynamic external module |
|  --with-compat                                | dynamic modules compatibility |
|  --without-pcre                               | disable PCRE library usage |
|  --with-pcre                                  | force PCRE library usage |
|  --with-pcre=DIR                              | set path to PCRE library sources |
|  --with-pcre-opt=OPTIONS                      | set additional build options for PCRE |
|  --with-pcre-jit                              | build PCRE with JIT compilation support |
|  --with-zlib=DIR                              | set path to zlib library sources |
|  --with-zlib-opt=OPTIONS                      | set additional build options for zlib |
|  --with-zlib-asm=CPU                          | use zlib assembler sources optimized |
|                                               | for the specified CPU, valid values: |
|                                               | pentium, pentiumpro |
|  --with-libatomic                             | force libatomic_ops library usage |
|  --with-libatomic=DIR                         | set path to libatomic_ops library sources |
|  --with-openssl=DIR                           | set path to OpenSSL library sources |
|  --with-openssl-opt=OPTIONS                   | set additional build options for OpenSSL |
|  --with-debug                                 | enable debug logging |

