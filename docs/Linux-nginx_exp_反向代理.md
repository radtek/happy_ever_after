## 反向代理实例-1

**1. 实现效果**

客户端访问 `www.test.com`, 跳转到 nginx 本地tomcat主页: `127.0.0.1:8080`

**2. 准备工作**

- 本地tomcat搭建

下载: [Apache Tomcat](https://tomcat.apache.org/download-80.cgi)

解压: `tar xf apache-tomcat-8.5.65.tar.gz  -C /usr/local/`

启动: `/usr/local/apache-tomcat-8.5.65/bin/start.sh`

- host修改

```sh
192.168.1.201 www.test.com
```

Linux: `/etc/hosts`

Windows: `C:\WINDOWS\system32\drivers\etc`

**3. Nginx配置**

- 修改 `nginx.conf`

```sh
...
http {
    ...
    server {
        listen       80;
        server_name  www.test.com;             #<= 修改
        location / {
            root   html;
            proxy_pass http://127.0.0.1:8080;  #<= 插入此行
            index  index.html index.htm;
        }
...
```

- 启动或重载nginx

```
$NGX_PATH/sbin/nginx
$NGX_PATH/sbin/nginx -s reload
```


## 反向代理实例-2


**1. 实现效果**

使用nginx反向代理，根据访问的路径跳转到不同端口的服务中: 

- nginx监听端口为 `9001`  
- 访问 `http://www.test.com:9001/edu/` 直接跳转到 `127.0.0.1:8080/edu`  
- 访问 `http://www.test.com:9001/vod/` 直接跳转到 `127.0.0.1:8081/vod`  

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

准备测试页面(`webapp/edu`和`webapp/vod`):

```html
# /usr/local/apache-tomcat-8080/webapps/edu/hello.html 
<h1>This is Apache Tomcat 8080 !</h1>

# /usr/local/apache-tomcat-8081/webapps/vod/hello.html 
<h1>This is Apache Tomcat 8081 !</h1>
```

启动:

```sh
/usr/local/apache-tomcat-8080/bin/startup.sh
/usr/local/apache-tomcat-8081/bin/startup.sh
```

- host修改同实例1


**3. Nginx配置**


- 修改 `nginx.conf`

```sh
...
http {
    ...
    server {
        listen       9001;                           #<=修改: 80=>9001
        server_name  www.test.com;                   #<=修改
        location ~ /edu/ {
            root   html;
            proxy_pass http://127.0.0.1:8080;        #<=插入
            index  index.html index.htm;
        }

        location ~ /vod/ {                           #<=插入
            root   html;                             #<=插入
            proxy_pass http://127.0.0.1:8081;        #<=插入
            index  index.html index.htm;             #<=插入
        }                                            #<=插入
...
```

- 启动或重载nginx

```
$NGX_PATH/sbin/nginx
$NGX_PATH/sbin/nginx -s reload
```

- 验证

![8080](Pictures/Nginx-反向代理-实例-01.png)

![8081](Pictures/Nginx-反向代理-实例-02.png)