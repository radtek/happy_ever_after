## 负载均衡常见策略

**1. 轮询（默认）**

每个请求按时间顺序逐一分配到不同的后端服务器，如果后端服务器down掉，能自动剔除

**2. weight**

weight代表权重, 默认为1。权重越高被分配的客户端越多指定轮询几率，weight和访问比率成正比，用于后端服务器性能不均的情况。例如：

```sh
upstream ServerPool {
    server 192.168.5.21 weight=10;  <=添加 weight=N 项
    server 192.168.5.22 weight=10;  <=添加 weight=N 项
}
```

**3. ip_hash**

每个请求按访问ip的hash结果分配，这样每个访客固定访问一个后端服务器，可以解决session的问题。例如

```sh
upstream ServerPool {
    ip_hash;                        <=添加 ip_hash; 配置行
    server 192.168.5.21;
    server 192.168.5.22;
}
```

**4. fair**

按后端服务器的响应时间来分配请求，响应时间短的优先分配。

```sh
upstream ServerPool {
    server 192.168.5.21;
    server 192.168.5.22;
    fair;                           <=添加 fair; 配置行
}
```

## 负载均衡实例

**1. 实现效果**

客户端访问 `www.test.com/edu/hello.html`, 实现负载均衡, 请求分发到不同的tomcat: `127.0.0.1:8080`, `127.0.0.1:8081`

**2. 准备工作**

- 本地tomcat搭建

> 为了简单配置，直接解压两个apache tomcat，修改端口后启动服务

```sh
# /usr/local:
# apache-tomcat-8080  # 使用默认配置
# apache-tomcat-8081  # 修改端口号

shell> vim /usr/local/apache-tomcat-8081/conf/server.xml

<Server port="8015" shutdown="SHUTDOWN">          #<=修改: 8005=>8015
  ...
    <Connector port="8081" protocol="HTTP/1.1"    #<=修改: 8080=>8081
               connectionTimeout="20000"
               redirectPort="8443" />
```

准备测试页面(`webapp/edu`):

```html
# /usr/local/apache-tomcat-8080/webapps/edu/hello.html 
<h1>This is Apache Tomcat 8080 !</h1>

# /usr/local/apache-tomcat-8081/webapps/edu/hello.html 
<h1>This is Apache Tomcat 8081 !</h1>
```

启动:

```sh
/usr/local/apache-tomcat-8080/bin/startup.sh
/usr/local/apache-tomcat-8081/bin/startup.sh
```

- host修改

```sh
192.168.1.201 www.test.com
```

Linux: `/etc/hosts`

Windows: `C:\WINDOWS\system32\drivers\etc`

**3. Nginx配置**

- 修改 `nginx.conf`

```sh
http {
    ...
    upstream tomcatserver {                    #<=插入, 注tomcatserver, 名称不能带下划线
        server 127.0.0.1:8080;                 #<=插入
        server 127.0.0.1:8081;                 #<=插入
    }                                          #<=插入

    server {
        listen       80;
        server_name  www.test.com;             #<=修改
        location ~ /edu/ {
            proxy_pass http://tomcatserver;    #<=插入
            root   html;
            index  index.html index.htm;
        }
...
```