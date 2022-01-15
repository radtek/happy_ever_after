- 查看版本号
- 启动
- 关闭
- 重新加载
- 日志分割

```sh
shell> NGX_PATH='/usr/local/nginx-1.20.0'
```

```x
Usage: nginx [-?hvVtTq] [-s signal] [-p prefix]
             [-e filename] [-c filename] [-g directives]

Options:
  -?,-h         : this help
  -v            : show version and exit
  -V            : show version and configure options then exit
  -t            : test configuration and exit
  -T            : test configuration, dump it and exit
  -q            : suppress non-error messages during configuration testing
  -s signal     : send signal to a master process: stop, quit, reopen, reload
  -p prefix     : set prefix path (default: /usr/local/nginx-1.20.0/)
  -e filename   : set error log file (default: logs/error.log)
  -c filename   : set configuration file (default: conf/nginx.conf)
  -g directives : set global directives out of configuration file
```

## 查看版本号

- `-v`

```sh
shell> ${NGX_PATH}/sbin/nginx -v

nginx version: nginx/1.20.0
```

- `-V`

```sh
shell> ${NGX_PATH}/sbin/nginx -V

nginx version: nginx/1.20.0
built by gcc 4.8.5 20150623 (Red Hat 4.8.5-44) (GCC) 
built with OpenSSL 1.0.2k-fips  26 Jan 2017
TLS SNI support enabled
configure arguments: --prefix=/usr/local/nginx-1.20.0 --with-http_ssl_module --with-http_stub_status_module --with-http_gzip_static_module
```

## 启动

```sh
shell> ${NGX_PATH}/sbin/nginx
shell> ps -ef | grep nginx 
root      3881     1  0 10:55 ?        00:00:00 nginx: master process /usr/local/nginx-1.20.0/sbin/nginx
nobody    3882  3881  0 10:55 ?        00:00:00 nginx: worker process
```

## 关闭

```sh
shell> ${NGX_PATH}/sbin/nginx -s quit  # quit 是一个优雅的关闭方式，Nginx在退出前完成已经接受的连接请求。
shell> ${NGX_PATH}/sbin/nginx -s stop  # stop 是快速关闭，不管有没有正在处理的请求。
```

## 重新加载

```sh
shell> ${NGX_PATH}/sbin/nginx -s reload   # 平滑的重启，配置重载；适用于修改配置文件生效
```

> nginx工作中，包括一个master进程，多个worker进程。worker进程负责具体的http等相关工作，master进程主要是进行控制等控制。 
> 
> nginx -s  reload 命令加载修改后的配置文件, 命令下达后发生如下事件：
> 
> 1. Nginx的master进程检查配置文件的正确性，若是错误则返回错误信息，nginx继续采用原配置文件进行工作（因为worker未受到影响）
> 
> 2. Nginx启动新的worker进程，采用新的配置文件
> 
> 3. Nginx将新的请求分配新的worker进程
> 
> 4. Nginx等待以前的worker进程的全部请求已经都返回后，关闭相关worker进程
> 
> 5. 重复上面过程，直到全部旧的worker进程都被关闭掉。
> 
> 所以，重启之后，master的进程号不变，worker的进程号会改变。


## 日志分割

```sh
shell> ${NGX_PATH}/sbin/nginx -s reopen   # 重新打开日志文件：适用于日志文件太大了，切换日志文件使用
```

> 建议过程如下
> 
> 1. `mv` 原文件到新文件目录中，这个时候 nginx 还写这个文件（写入新位置文件中：因为进程拥有文件的inode信息）
> 
> 2. 调用 `nginx -s  reopen` 用来打开日志文件，这样 nginx 会把新日志信息写入这个新的文件中

这样完成了日志的切割工作， 同时切割过程中没有日志的丢失。