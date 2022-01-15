# Configrating Nginx

## 1. 默认配置

```sh
worker_processes  1;

events {
    worker_connections  1024;
}

http {
    include       mime.types;
    default_type  application/octet-stream;

    sendfile        on; 

    keepalive_timeout  65;

    server {      
        listen       80;
        server_name  localhost;

        location / {
            root   html;
            index  index.html index.htm;
        }

        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
        
    }   
}
```

## 2. 配置模块分解

- **第一部分: 全局块**

从配置文件开始到 `events` 块之间的内容, 主要会设置一些影响 nginx 服务器整体运行的配置指令, 主要包括**配置运行 Nginx 服务器的用户（组）**、**允许生成的worker process 数**, **进程PID 存放路径**、**日志存放路径和类型**以及**配置文件的引入**等。

如: 

```sh
worker_processes  1;
```

这是 Nginx 服务器并发处理服务的关键配置, `worker_processes` 值越大, 可以支持的并发处理量也越多, 但是会受到硬件、软件等设备的制约


- **第二部分: `events`块**

`events` 块涉及的指令主要**影响 Nginx 服务器与用户的网络连接**, 常用的设置包括**是否开启对多work process 下的网络连接进行序列化**, **是否允许同时接收多个网络连接**, **选取哪种事件驱动模型来处理连接请求**, **每个word process 可以同时支持的最大连接数**等。

如:

```sh
events {
    worker_connections  1024;
}
```

上述例子就表示每个 work process 支持的最大连接数为1024.这部分的配置对Nginx 的性能影响较大, 在实际中应该灵活配置。

- **第三部分: `http`块**

这算是Nginx 服务器配置中最频繁的部分, **代理**、**缓存**和**日志定义**等绝大多数功能和**第三方模块的配置**都在这里。

需要注意的是: `http` 块包括 **http全局块**、**server块**。

```sh
http {
    include       mime.types;
    default_type  application/octet-stream;

    sendfile        on; 

    keepalive_timeout  65;

    server {      
        listen       80;
        server_name  localhost;

        location / {
            root   html;
            index  index.html index.htm;
        }

        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
        
    }   
}
```

**`http` 全局块**

http全局块配置的指令包括**文件引入**、**MIME-TYPE 定义**、**日志自定义**、**连接超时时间**、**单链接请求数上限**等。

**`server` 块**

这块和**虚拟主机**有密切关系, 虚拟主机从用户角度看, 和一台独立的硬件主机是完全一样的, 该技术的产生是为了节省互联网服务器硬件成本。**每个 `http` 块可以包括多个 `server` 块, 而每个`server` 块就相当于一个虚拟主机。**

每个 `server` 块也分为**`server` 全局块**, 以及可以同时包含多个 **`locaton` 块**。

1. `server` 全局块: 最常见的配置是**本虚拟机主机的监听配置**和**本虚拟主机的名称或IP配置**。
2. `location` 块: **一个 `server` 块可以配置多个 `location` 块**。这块的主要作用是**基于Nginx服务器接收到的请求字符串（例如server_name/uri-string）, 对虚拟主机名称（也可以是IP别名）之外的字符串（例如前面的/uri-string）进行匹配, 对特定的请求进行处理。地址定向、数据缓存和应答控制等功能, 还有许多第三方模块的配置也在这里进行**。


## 3. location指令

该指令用于匹配URL

修饰符:

1. 无修饰符: 必须以指定模式开始
2. `=`： 必须与指定的模式精确匹配, 如果匹配成功, 就停止继续向下搜索并立即处理该请求。  
3. `~`： 用于表示 uri 包含正则表达式, 并且**区分大小写**。  
4. `~*`： 用于表示 uri 包含正则表达式, 并且**不区分大小写**。  
5. `^~`： 类似于无修饰符的行为, 也是以指定模式开始
6. `@`: 定义命名location区段, 这些区段客户段不能访问, 只可以由内部产生的请求来访问, 如try_files或error_page等

查找顺序和优先级: 

- 带有 `=` 精确匹配, 成功则立即停止
- 进行前缀匹配: 先查找带有 `^~` 的前缀匹配, 如果带有 `^~` 的前缀匹配是精确匹配, 则立即处理并停止; 否则, 暂存匹配结果, 进行正则匹配和普通前缀匹配(正则优先)
- `=` 和 `^~` 均未匹配成功前提下, 进行带有 `~` 或 `~*` 修饰符的, 如果正则表达式与URI匹配, 命中则立即停止
- 所有正则均为命中, 取最优的暂存的前缀匹配(带`^~`和不带任何修饰符的前缀匹配)


例1: **`location = /abcd`**

```sh
location = /abcd {
    return 701;
}

# 用curl -I http://测试查看返回值
```

- `http://website.com/abcd`: **匹配**  
- `http://website.com/ABCD`: **可能会匹配 , 也可以不匹配**, 取决于操作系统的文件系统是否大小写敏感。**ps**: Mac 默认是大小写不敏感的。  
- `http://website.com/abcd?param1&param2`: **匹配**, 忽略 querystring  
- `http://website.com/abcd/`: **不匹配**, 带有结尾的`/`  
- `http://website.com/abcde`: **不匹配**  

> `abcd?param1` 匹配成功, 说明nginx认为 `?` 为是字符串结束的标志  ????

例2: **`location ~ ^/abcd$`**

- `http://website.com/abcd`: **匹配**, 完全匹配  
- `http://website.com/ABCD`: **不匹配**, 大小写敏感  
- `http://website.com/abcd?param1&param2`: **匹配**  
- `http://website.com/abcd/`: **不匹配**, 不能匹配正则表达式
- `http://website.com/abcde`: **不匹配**, 不能匹配正则表达式 
  
例3:

```sh
Location区段匹配示例

location = / {
    # 只匹配 / 的查询.
    [ configuration A ]
}
location / {
    # 匹配任何以 / 开始的查询, 但是正则表达式与一些较长的字符串将被首先匹配。
    [ configuration B ]
}
location ^~ /images/ {
    # 匹配任何以 /images/ 开始的查询并且停止搜索, 不检查正则表达式。
    [ configuration C ]
}
location ~* \.(gif|jpg|jpeg)$ {
    # 匹配任何以gif, jpg, or jpeg结尾的文件, 但是所有 /images/ 目录的请求将在Configuration C中处
    理。
    [ configuration D ]
}

各请求的处理如下：
/                        => configuration A
/documents/document.html => configuration B
/images/1.gif            => configuration C
/documents/1.jpg         => configuration D
```



## 4. 配置语法

1. 配置文件由指令与指令块构成  
2. 每条指令以 `;` 分号结尾，指令与参数间以空格符号分隔  
3. 指令块以 `{}` 大括号将多条指令组织在一起   
4. `include` 语句允许组合多个配置文件以提升可维护性  
5. 使用 `#` 符号添加注释，提高可读性  
6. 使用 `$` 符号使用变量  
7. 部分指令的参数支持正则表达式  
   
## 5. 配置参数

### 时间的单位

|  缩写 | 含义 |
|   -- | --  |
| `ms` | milliseconds |
| `s`  | seconds |
| `m`  | minutes |
| `h`  | hours |
| `d`  | days |
| `w`  | weeks |
| `M`  | months, 30 days |
| `y`  | years, 365 days |

### 空间的单位

|  缩写 | 含义 |
|   -- | --  |
|         | bytes |
| `k`/`K` | kilobytes |
| `m`/`M` | megabytes |
| `g`/`G` | gigabytes |

## 6. 正则表达式

### 元字符

| 代码 | 说明 |
|  --  |  --  |
| `.` | 匹配除换行符以外的任意字符 |
| `\w` | 匹配字母/数字/下划线/汉字 |
| `\s` | 匹配任意空白字符 |
| `\d` | 匹配数字 |
| `\b` | 匹配单词的开始或结束 |
| `^` | 匹配字符串开头 |
| `$` | 匹配字符串结尾 |

### 重复

| 代码 | 说明 |
|  --  |  --  |
| `*` | 重复任意次|
| `+` | 重复1次或以上 |
| `?` | 重复0次或1次 |
| `{n}` | 重复n次 |
| `{m,}` | 重复m次或以上 |
| `{m,n}` | 重复m次到n次 |

### 其他

| 代码 | 说明 |
|  --  |  --  |
| `()` | 分组与取值 |
| `\`  | 转义符号 |


## 7. Listen 指令

- 详情

```sh
Syntax: 

    listen address[:port] [default_server] [ssl] [http2|spdy] [setfib=number] [fastopen=number] [backlog=number] [rcvbuf=size] [sndbuf=size] [accept_filter=filter] [deferred] [bind] [ipv6only=on|off] [reuseport] [so_keepalive=on|off|[keepidle]:[keepintvl]:[keepcnt]; `

    listent port [default_server] [ssl] [http2|spdy] [setfib=number] [fastopen=number] [backlog=number] [rcvbuf=size] [sndbuf=size] [accept_filter=filter] [deferred] [bind] [ipv6only=on|off] [reuseport] [so_keepalive=on|off|[keepidle]:[keepintvl]:[keepcnt]; `

    listen unix:path [default_server] [ssl] [http2|spdy] [proxy_protocol] [backlog=number] [rcvbuf=size] [sndbuf=size] [accept_filter=filter] [deferred] [bind] [so_keepalive=on|off|[keepidle]:[keepintvl]:[keepcnt]; `

Default: listen *:80 | *:8000;
Context: server
```

- 示例：

```sh
listen unix:/var/run/nginx.sock;
listen 127.0.0.1:8000;
listen 127.0.0.1;
listen 8000;
listen *:8000;
listen localhost:8000 bind;
listen [::]:8000 ipv6only=on;
listen [::1];
```

### 过大的请求头部

```sh
Syntax: client_header_buffer_size size;
Default: client_header_buffer_size 1k;
Context: http, server

Syntax: large_client_header_buffers number size;
Default: large_client_header_buffers 4 8k;
Context: http, server
```