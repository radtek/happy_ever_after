## ssh端口转发

```sh
ssh [-46AaCfGgKkMNnqsTtVvXxYy] [-B bind_interface] [-b bind_address] [-c cipher_spec] [-D [bind_address:]port] [-E log_file] [-e escape_char] [-F configfile]
         [-I pkcs11] [-i identity_file] [-J destination] [-L address] [-l login_name] [-m mac_spec] [-O ctl_cmd] [-o option] [-p port] [-Q query_option] [-R address]
         [-S ctl_path] [-W host:port] [-w local_tun[:remote_tun]] destination [command]
# -f ssh在执行命令前退至后台(后台启用)
# -N 不打开远程shell, 处于等待状态, 用于转发端口（不加-N则直接登录进去）
# -g 允许远端主机连接本地的转发端口 (支持多主机访问本地侦听端口)
# -L 将本地主机的地址和端口接收到的数据通过安全通道转发给远程主机的地址和端口
# -R 将远程主机上的地址和端口接收的数据通过安全通道转发给本地主机的地址和端口
# -D 动态转发
```

**1. 本地端口转发**

接收本地端口(Local Port)数据, 转发到远程端口(Remote Port)


```sh
ssh -L [Local IP:]<Local Port>:<Remote IP>:<Remote Port> [User@]<Remote IP>
```

例1: `ServerA:8080 =22=> ServerB:127.0.0.1:80`

* ServerB只允许本地127.0.0.1访问nginx的80端口
* ServerA可以连接ServerB的22端口
* 实现: 将ServerA的8080端口转发到ServerB的127.0.0.1:80端口, 这样外部可以通过访问ServerA-IP:8080访问到ServerB的nginx

```sh
ServerA> ssh -Nf -L 0.0.0.0:8080:127.0.0.1:80 User@ServerB-IP
```

例2: `ServerA:8022 =22=> ServerB:22 =22=> ServerC:22`

* ServerA可以访问ServerB的22端口, 而与ServerC网络隔离;
* ServerB可以访问ServerC的22端口;
* 实现: ServerA可以本地8022端口ssh连接到ServerC

```sh
ServerA> ssh -Nf -L 127.0.0.1:8022:<ServerC-IP>:80 User@ServerB-IP
```


**2. 远程端口转发**

接收远程端口(Remote Port)数据, 转发到服务端口(Server Port)

```sh
ssh -L [Remote IP:]<Remote Port>:<Server IP>:<Server Port> [User@]<Remote IP>
```

例23: `ServerA <=22,6666= ServerB =7777=> ServerC`

* ServerB可以访问ServerA的22和6666端口;
* ServerB可以访问ServerC的7777端口;
* ServerA与ServerC网络隔离
* 实现: ServerA的6666端口与ServerC的7777端口通信

```sh
ServerB> ssh -Nf -R <ServerC-IP>:7777:<ServerA-IP>:6666 <ServerC-IP>

# 1. ServerC可以查询到7777端口监听, 用nc查看7777端口输出
nc -v 127.0.0.1 7777
# 2. ServerA手动配置监听6666端口
nc -l 6666
# 3. ServerA与ServerC互发信息能够相互接收
ServerC> nc -v 127.0.0.1 7777
Ncat: Version 7.50 ( https://nmap.org/ncat )
Ncat: Connected to 127.0.0.1:7777.
hello
this is ServerA

ServerA> nc -l 6666
hello
this is ServerA
```


## 动态端口转发


对于**本地端口转发**和**远程端口转发**，都存在两个一一对应的端口，分别位于SSH的客户端和服务端，而动态端口转发则只是绑定了一个本地端口，而 **`目标地址:目标端口`** 则是不固定的。

**`目标地址:目标端口`**是由发起的请求决定的，比如，请求地址为`192.168.1.100:3000`，则通过SSH转发的请求地址也是`192.168.1.100:3000`。


```sh
ssh -D [Local IP:]<Local port>
```

这时，通过动态端口转发，可以将在本地主机ServerA发起的请求，转发到远程主机ServerB，而由ServerB去真正地发起请求。

```sh
# 在本地主机ServerA登陆远程云主机ServerB，并进行动态端口转发
ServerA> ssh -D localhost:2000 root@<ServerB-IP>
```

而在本地发起的请求，需要由Socket代理(Socket Proxy)转发到SSH绑定的2000端口。以Firefox浏览器为例，配置Socket代理需要找到`首选项>高级>网络>连接->设置`