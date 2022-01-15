# httpd

## 一, httpd 服务

### 1. 特性

* DSO (Dynamic Shared Object, 动态共享对象)
* MPM (Multipath Procession Modules, 多路处理模块)
    * 可以通过修改MPM来修改并发响应模型
    * 2.4支持MPM模块动态切换, 2.2不支持

### 2. 并发响应模型

* prefork
    
    两级进程模型, 父进程管理子进程, 每个进程响应一个请求

    ```conf
    # 工作模型
        一个主进程: 
            负责生成子进程及回收子进程
            负责创建套接字, 接受请求, 并将其派发给某子进程进行处理
        n个子进程: 
            每个子进程处理一个请求

    # 注意: 
        会预先生成几个空闲进程, 随时等待用于响应用户请求
        最大空闲和最小空闲
    ```

* worker
    
    三级进程模型, 父进程管理子进程, 子进程通过线程响应用户请求, 每个线程处理一个用户请求

    ```conf
    # 工作模型
        一个主进程: 
            负责生成子进程, 创建套接字, 接受请求, 并将其派发给某子进程进行处理
        多个子进程: 
            每个子进程负责生成多个线程
        每个线程: 
            负责响应用户请求

    # 并发响应数量: 
        子进程数 * 每个子进程能创建的最大线程数
        ```
* event
    
    两级模型, 父进程管理子进程, 子进程通过事件驱动 `event-driven` 机制直接响应n个请求

    ```conf
    # 工作模型: 
        一个主进程: 
            负责生成子进程, 创建套接字, 接受请求, 并将其派发给某子进程进行处理
        子进程: 
            基于事件驱动机制直接响应多个请求

    # httpd-2.4中的event机制可以在生产环境中使用
    ```

### 3. 程序结构

* httpd-2.2(CentOS 6.x)

    ```dircolors
    httpd-2.2
    │
    ├── 主程序文件
    │   ├── /usr/sbin/httpd
    │   ├── /usr/sbin/httpd.event
    │   └── /usr/sbin/httpd.worker
    ├── 服务脚本
    │   └── /etc/rc.d/init.d/httpd
    │       └── /etc/sysconfig/httpd
    ├── 配置文件
    │   ├── /etc/httpd/conf/httpd.conf
    │   └── /etc/httpd/conf.d/*.conf
    ├── 日志文件
    │   └── /var/log/httpd/
    │       ├── access_log
    │       └── error_log
    ├── 站点文件
    │   └── /var/www/html
    └── 模块文件路径
        └── /usr/lib64/httpd/modules
    ```

* httpd-2.4(CentOS 7.x)

    ```dircolors
    httpd-2.4
    │
    ├── 主程序文件
    │   ├── /usr/sbin/httpd
    │   └── httpd-2.4支持MPM的动态切换
    ├── unit file(systemd)
    │   └── /usr/lib/systemd/system/httpd.service
    ├── 配置文件
    │   ├── /etc/httpd/conf/httpd.conf
    │   └── /etc/httpd/conf.d/*.conf
    ├── 日志文件
    │   └── /var/log/httpd/
    │       ├── access_log
    │       └── error_log
    ├── 站点文件
    │   └── /var/www/html
    └── 模块文件路径
        ├── /usr/lib64/httpd/modules
        └── 模块相关的配置文件
            ├── /etc/httpd/conf.modules.d/*.conf
            └── 分别配置每个模块的特性
    ```

## 二, httpd的主配置文件

### 1. 配置文件结构和格式

* (1) 整体结构

    * 全局环境配置(Global Environment): 对进程自己的工作特点, 对所有虚拟主机都通用的设定

    * 主服务器配置段("Main" server configuration): *在 2.2 上如果要使用主服务器, 则要将虚拟主机关掉*

    * 虚拟主机(Virtual Hosts) 

* (2) 配置格式: `directive value`

    * `directive`: 不区分字符大小写

    * `value`: 为路径时, 是否区分字符大小写, 取决于文件系统


### 2. 监听的 IP 和 PORT

```apacheconf
Listen  [IP:]Port  [protocol]
    # 若省略IP则表示0.0.0.0
    # Listen指令可以重复出现多次
        Listen 80
        Listen 8080        
```

注意:

* 修改监听的套接字, 重启服务进程才能生效

* 限制其必须通过ssl通信时, protocol需要定义为https


### 3. 用户和用户组

```apacheconf
# 作用: 
指定以哪个用户的身份运行httpd服务器进程
    
# 格式: 
User apache
Group apache
    
# 对主控进程是root用户的说明: 
主控进程是root, 因为80端口是特权端口(小于1024的端口), 只有管理员才能使用
所以主控进程是root, 而其他的进程使用普通用户权限
        
SUexec 在某些指令执行时可以切换到另外一个用户(默认没有装载)
```


### 4. 默认字符集

```apacheconf
# 设置默认字符集
# 格式
AddDefaultCharset UTF-8

# 中文字符集: 
GBK, GB2312, GB18030
```

```apacheconf
ServerRoot "/etc/httpd"
Listen 192.168.161.1:8800
Include conf.modules.d/*.conf
User apache
Group apache
ServerAdmin root@localhost
ServerName 192.168.161.1:8800
<Directory />
    AllowOverride none
    Require all denied
</Directory>
DocumentRoot "/var/www/html"
<Directory "/var/www">
    AllowOverride None
    Require all granted
</Directory>
<Directory "/var/www/html">
    Options FollowSymLinks Indexes
    AllowOverride None
    Order Deny,Allow
    Deny From all
    Allow From 192.168.161.0/24
</Directory>
<IfModule dir_module>
    DirectoryIndex index.html
</IfModule>
<Files ".ht*">
    Require all denied
</Files>
ErrorLog "logs/error_log"
LogLevel warn
<IfModule log_config_module>
    LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"" combined
    LogFormat "%h %l %u %t \"%r\" %>s %b" common
    <IfModule logio_module>
      LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\" %I %O" combinedio
    </IfModule>
    CustomLog "logs/access_log" combined
</IfModule>
<IfModule alias_module>
    ScriptAlias /cgi-bin/ "/var/www/cgi-bin/"
</IfModule>
<Directory "/var/www/cgi-bin">
    AllowOverride None
    Options None
    Require all granted
</Directory>
<IfModule mime_module>
    TypesConfig /etc/mime.types
    AddType application/x-compress .Z
    AddType application/x-gzip .gz .tgz
    AddType text/html .shtml
    AddOutputFilter INCLUDES .shtml
</IfModule>
AddDefaultCharset UTF-8
<IfModule mime_magic_module>
    MIMEMagicFile conf/magic
</IfModule>
EnableSendfile on
IncludeOptional conf.d/*.conf
```


### 5. 站点主页面

```apacheconf
# 格式: 
DirectoryIndex index.html index.html.var
```

### 6. 持久连接

* 持久连接/保持连接/长连接(持久连接)

    TCP 连接建立后, 每个资源获取完成后不断开连接, 而是继续等待其他资源请求的进行

* 断开条件

    * 数量限制

    * 时间限制

* 副作用

    对并发访问量较大的服务器, 长连接机制会使得后续某些请求无法得到正常响应

* 折中方案
    
    * 使用较短的持久连接时长
    
    * 限制较少的请求数量
    
* 配置

    ```apacheconf
    KeepAlive On|Off          # 是否启用长连接
    KeepAliveTimeout 15       # 超时时长, 单位为 "秒"; httpd-2.4可设置毫秒级, 在数值后面加上 "ms"
    MaxKeepAliveRequests 100  # 保持连接上面所能获取的最大请求数量(每个连接上面的最大请求数量)
    ```

* 测试

    可以用 `telnet` 命令来对持久连接进行测试

    ```sh
    ~] telnet 10.0.0.110 80
    GET / HTTP/1.1
    Host: 10.0.0.110

    HTTP/1.1 200 OK
    Date: Mon, 10 Jan 2022 05:43:39 GMT
    Server: Apache/2.4.37 (rocky)
    Content-Length: 1750
    ...                    # <= 输出完以后立刻就退出, 即表明未配置长连接
    ```

3.7 配置MPM
1)说明

在2.2中(CentOS6的rpm包)专门提供了三个应用程序文件；因为httpd2.2不支持通过编译多个MPM模块, 所以只能编译选定要使用的那个；

这三个应用程序文件分别用于实现对不同的MPM机制的支持, 默认是使用prefork机制

httpd(prefork)默认就是使用prefork机制
httpd.worker
httpd.event
2)查看httpd程序的模块列表

# 查看httpd程序的模块列表

# 查看静态编译的模块
httpd -l

# 查看静态编译及动态编译的模块, 查看所有模块
httpd -M
3)切换MPM机制

### 2.2中
# 1.更换使用的httpd程序, 以支持其他MPM机制
vim  /etc/sysconfig/httpd
    HTTPD=/usr/sbin/httpd.{worker,event}
# 2.然后启用的时候要使用/usr/sbin/httpd.worker
/usr/sbin/httpd.worker -k start

### 2.4中
# 直接在这个文件中将对应的模块取消注释就ok
vim  /etc/httpd/conf.modules.d/00-mpm.conf
        
# 查看当前的工作模式
httpd -V
    
# 注意: 重启服务方可生效
4)MPM的配置

# prefork的配置: 
        <IfModule prefork.c>
                StartServers      8   # httpd服务进程启用以后自动创建出空闲的子进程数量
                MinSpareServers   5   # 最少空闲进程数, 无论如何都需要有5个空闲进程来对待新请求
                MaxSpareServers  20   # 最大空闲进程数, 要大于StartServers的数量
                ServerLimit      256  # 同时在生命周期内处于活跃状态的服务器进程数(跟MaxClients应该是相同的)
                MaxClients       256  # 最大允许启动的服务器子进程的数量
                MaxRequestsPerChild  4000  
                    # 一个子进程最多能处理的请求, 若超过这个值, 就将这个进程kill掉而创建新的进程
                   # 设置为0则表示永不过期
        </IfModule>
        
# worker的配置: 
        <IfModule worker.c>
                StartServers     4      # httpd服务进程启动以后自动创建出空闲的子进程数量
                MinSpareThreads  25     # 最少空闲的线程数
                MaxSpareThreads  75     # 最大空闲的线程数
        MaxClients       300    # 最大的允许在线的线程数
                ThreadsPerChild  25     # 每个子进程生成多少个线程
                MaxRequestsPerChild  0  # 单个进程最大允许响应多少个请求
        <IfModule>
3.8 模块加载
# DSO动态共享对象
    
# 模块位置
/etc/httpd/conf.modules.d/ 
在这个目录下的模块对应的配置文件中修改
    
# 加载模块
LoadModule   <mod_name>  <mod_path>
模块文件路径可使用相对路径, 相对于ServerRoot, 默认是 /etc/httpd
3.9 定义Main Server
# 定义Main Server
ServerName  FQDN

# 语法格式
ServerName [scheme://]fully-qualified-domain-name[:port]
# 此处的名字是用来表示当前主机认为主机主要是服务于谁的
# 如果这条指令没有定义, 那么httpd启动时会试图反解本地的IP地址(把IP解析为主机名), 如果解析不成功, 则会警告
    
DocumentRoot   "/var/www/html"
# 作用: 指明网站的站点的url映射到本地的哪个文件系统路径下
# 文档路径映射: 
    # DocumentRoot指向的路径为URL路径的起始位置, 其相当于站点URL的根路径
    # URL PATH与FileSystem PATH不是等同的, 而是存在一种映射关系
3.10 路径别名
# 格式: 
Alias  /URL/   "/PATH/TO/SOMEDIR" 
# 把URL跟另外的其他的目录建立映射关系

# 注意: 在httpd2.4中要对那个目录进行显示授权(在Directory中定义那个目录的权限)
Alias和DocumentRoot的区别: 
DocumentRoot "/www/htdocs"
        http://www.hgzero.com/download/xxx.txt 
                             /www/htdocs/download/xxx.txt
                
Alias  /download/  "/doc/pub/"
        http://www.hgzero.com/download/xxx.txt
                             /doc/pub/xxx.txt
3.11 站点访问控制
# 文件系统路径: 
        <Directory  "">        # 对目录下的所有资源进行控制
          ...
        </Directory>
        
        <File  "">             # 针对某个文件进行控制
          ...
        </File>
        
        <FileMatch  "PATTERN"> # 针对符合正则匹配的所有文件进行控制
          ...
        </FileMatch>

# URL路径: 
        <Location  "">         # 针对URL路径进行控制
          ...
        </Location>
        
        <LocationMatch  "">
          ...
        </LocationMatch>
3.12 status页面
在2.4上面要装载的模块: LoadModule status_module modules/mod_status.so

# 在httpd2.2中: 
        <Location  /server-status>
                SetHandler server-status
                Order allow,deny
                Allow  from  172.16
        </Location>
        
# 在httpd2.4中: 
        <Location  /server-status>
                SetHandler server-status
                <RequireAll>
                        Require ip 172.16
                </RequireAll>
        </Location>
3.13 页面压缩deflate
1)作用

使用mod_deflate模块压缩页面优化传输速度(压缩文本文件, 图片文件不需要压缩)
2)适用场景

节约带宽, 额外消耗CPU；同时, 可能有些较老浏览器不支持
压缩适于压缩的资源, 例如文件文件
3)设置示例

SetOutputFilter DEFLATE    # 设置一个叫DEFLATE的过滤器

# mod_deflate configuration

 
# Restrict compression to these MIME types  # 指定对哪些内容做压缩
AddOutputFilterByType DEFLATE text/plain 
AddOutputFilterByType DEFLATE text/html
AddOutputFilterByType DEFLATE application/xhtml+xml
AddOutputFilterByType DEFLATE text/xml
AddOutputFilterByType DEFLATE application/xml
AddOutputFilterByType DEFLATE application/x-javascript
AddOutputFilterByType DEFLATE text/javascript
AddOutputFilterByType DEFLATE text/css
 
# Level of compression (Highest 9 - Lowest 1) # 指定压缩比
DeflateCompressionLevel 9
 
# Netscape 4.x has some problems.  # 匹配特定的浏览器, 再对其做特定的压缩, 因为可能有些浏览器的特性不一样, 如IE
BrowserMatch ^Mozilla/4  gzip-only-text/html
 
# Netscape 4.06-4.08 have some more problems
BrowserMatch  ^Mozilla/4\.0[678]  no-gzip
 
# MSIE masquerades as Netscape, but it is fine
BrowserMatch \bMSI[E]  !no-gzip !gzip-only-text/html
4. 虚拟主机
4.1 虚拟主机概述
1)站点标识(IP, PORT, FQDN)

IP相同, 端口不同
IP不同, 端口均为默认端口
FQDN不同: http请求报文首部中 Host: www.hgzero.com
2)虚拟主机种类

基于IP地址: 为每个虚拟主机准备至少一个ip地址, 默认是匹配自上而下的第一个符合条件的
基于端口PORT: 为每个虚拟主机使用至少一个独立的port
基于FQDN: 为每个虚拟主机使用至少一个FQDN
基于FQDN时, 要将所有的FQDN都解析到同一个IP地址上
可以在本地hosts文件中定义或者在DNS服务器上指定
基于FQDN时, 是根据http请求报文中的host值来判断的, 这个host值是不会被解析的
4.2 匹配规则&匹配格式
1)匹配规则

通配的越少的虚拟主机, 匹配优先级越高
如果基于名称的虚拟主机无法匹配上, 则采用虚拟主机列表中的第一个虚拟主机作为响应主机
如果所有的虚拟主机都无法匹配上, 则采用主配置段中的主机, 如果主配置段中注释了DocumentRoot, 则返回对应的错误
注意: 

一般虚拟主机不要与中心主机混用, 如果要使用虚拟主机, 得先禁用main主机；2.4则可以不禁Main Server
禁用中心主机: 注释DocumentRoot即可
2)虚拟主机配置格式

<VirtualHost  IP:PORT>
        ServerName  FQDN
        DocumentRoot  ""
    ...
    ServerAlias: 虚拟主机的别名, 可多次使用
</VirtualHost>
4.3 虚拟主机配置示例
1)基于IP的虚拟主机(基于端口)

# 基于IP的虚拟主机(基于端口的虚拟主机无非就是IP地址相同, 而端口不同而已): 
<VirtualHost 10.0.0.201:81>
        ServerName www.hgzero.com
        DocumentRoot "/data/html/www"
        <Directory "/data/html/www">
                Options None
                AllowOverride None
                Require all granted
        </Directory>
        CustomLog "/data/html/www/log/access_log" combined
</VirtualHost>

<VirtualHost *:82>   # 这里的*表示监听本地所有地址
        ServerName bbs.hgzero.com
        DocumentRoot "/data/html/bbs"
        <Directory "/data/html/bbs">
                Options None
                AllowOverride None
                Require all granted
        </Directory>
        CustomLog "/data/html/bbs/log/access_log" combined
</VirtualHost>
2)基于FQDN的虚拟主机

# 基于主机名(FQDN)
<VirtualHost *:80>
        ServerName web.hgzero.com
        DocumentRoot "/data/html/www"
        <Directory "/data/html/www">
                Options None
                AllowOverride None
                Require all granted
        </Directory>
        CustomLog "/data/html/www/log/access_log" combined
</VirtualHost>

<VirtualHost *:80>
        ServerName bbs.hgzero.com
        DocumentRoot "/data/html/bbs"
        <Directory "/data/html/bbs">
                Options None
                AllowOverride None
                Require all granted 
        </Directory>
        CustomLog "/data/html/bbs/log/access_log" combined
</VirtualHost>

# 注意: 如果是在http2.2上, 则使用基于FQDN的虚拟主机时, 要事先使用如下指令
        NameVirtualHost  172.16.100.6:80
        # 意为在这个IP和端口上, 开放基于主机名的虚拟主机
3)注意

基于名称的虚拟主机必须指定ServerName指令, 否则它将会继承操作系统的FQDN

对于基于名称的虚拟主机, 如果使用IP地址请求无法匹配到任何虚拟主机时, 将采用第一个虚拟主机作为默认虚拟主机

5. 访问控制
5.1 基于源地址的访问控制
1)httpd2.2和httpd2.4中的访问控制

### httpd-2.2 ###
AllowOverride   # 表示是否允许覆盖这里的配置；与访问控制相关的指令可以放在.htaccess文件中
    All
    None
        
order           # 定义生效次序, 写在后面的表示默认法则
    allow
    deny
        
Allow from      # 允许哪些地址的访问
Deny from       #拒绝哪些地址的访问
    

### httpd-2.4 ###
# 基于IP控制
Require  ip  IP_ADDR
Require  not  ip  IP_ADDR
        
# 基于主机名控制
Require  host  主机名或域名
Require  not  host  主机名或域名
        
### 注意: 
# 以上的这些控制信息需要定义在<RequireAll>...</RequireAll>中或<RequireAny>配置块中
# 2.4中的源地址的访问控制需要显示指定
2)Options选项

Indexes        # 指明的URL路径下不存在与定义的主页面资源相等的资源文件时, 返回索引列表给用户
FollowSymLinks # 允许跟踪符号链接文件所指向的源文件(在配置别名时很有用)
None
All
3)httpd2.4中的配置示例

### 配置示例
<Directory "/var/www/html/bbs">
        Options None                     
        AllowOverride None
        <RequireAll>  # 这里定义了基于IP的访问控制(这里也可以缓存域名或主机名)
                Require ip 192.168.0.0/16
                Require not ip 192.168.1.102
        </RequireAll>
</Directory>

### 来源地址的格式: 如果是基于主机名的话, 要写成Requrie host node1.com 
        IP
        NetAddr: 
                172.16
                172.16.0.0/16
                172.16.0.0/255.255.0.0
5.2 控制页面允许or不允许所有主机访问
# 控制页面资源允许所有来源的主机可访问: 
        # http-2.2
                <Directory  "">
                        ...
                        Order  allow,deny
                        Allow from all
                </Directory>
        # http-2.4
                <Directory  "">
                        ...
                        Require all granted
                </Directory>

# 控制页面资源拒绝所有来源的主机可访问: 
        # http-2.2
                <Directory  "">
                        ...
                        Order  allow,deny
                        Deny from all
                </Directory>
        # http-2.4
                <Directory  "">
                        ...
                        Require all denied
                </Directory>
5.3 htpasswd


5.4 基于用户的访问控制
1)认证概述

# 认证质询
WWW-Authenticate, 响应码为401, 拒绝客户端请求, 并说明要求客户端提供账号和密码
客户端用户填入账号和密码后再次发送请求报文, 若认证通过, 则服务器发送响应的资源
    
# 认证方式
basic: 明文
digest: 消息摘要认证
表单认证
    
# 安全域
需要用户认证后方能访问的路径
应该通过名称对其特性标识, 以便告知用户认证的原因
    
# 用户的账号和密码存放的位置
虚拟账号: 仅用于访问某服务时用到的认证标识
存储: 
    文本文件
    SQL数据库
    ldap目录存储
2)basic认证配置示例

基于用户的认证: 
# 定义安全域: 
        <Directory  "">
                Options  None
                AllowOverride None # 是否允许覆盖这里的配置, 一般都是设置为None
                AuthType Basic     # 也可以指明digest认证方式
                AuthName "String"  # 指明提示信息
                AuthUserFile  "/etc/httpd/conf.d/.htpasswd"  # 密码文件,最好将其设置为隐藏文件
                Require user username1 username2 ...         # 允许登录的用户
        Require valid-user  # 允许账号文件中的所有用户登录访问
        </Directory>
基于组账号进行认证: 
# 定义安全域: 
        <Directory  "">
                Options  None
                AllowOverride  None
                AuthType  Basic
                AuthName  "String"
                AuthUserFile  "PATH/TO/HTTPD_USER_PASSWD_FILE"
                AuthGroupFile  "/PATH/TO/HTTPD_GROUP_FILE"   # 这里引用的是组账号的文件
                Require  group  groupname1  grpname2 ...       # 允许登录的组
        </Directory>
        
# 创建用户账号和组账号文件: 
          # 组账号定义格式: 
    组文件: 每一行定义一个组(创建组账号文件)
    GRP_NAME: username1  username2 ...
6. https的配置
6.1 https的工作流程
1)SSL会话过程



 2)SSL会话缓存

SSL会话的时长
若每次通信都经过ssl handshake, 那将是非常浪费资源的, 所以Server端可以吧ssl会话给缓存下来
在一段时间内同一客户端访问时这个ssl handshake过程就不必再做了, 直接利用此前已经建立的会话资源就可以了
但是此会话不能保存太长时间, 一般是五分钟之内都是有效的
SSL会话是基于IP地址创建的, 所以单IP的主机上, 仅可以使用一个https的虚拟主机
6.2 配置httpd支持https


7. 日志相关
7.1 日志的记录


7.2 日志轮替
cronolog
rotatelog


8. 压测工具


9. httpd自带的工具程序
apachectl
apxs
suexec


10. LAMP基本架构


 

 

 