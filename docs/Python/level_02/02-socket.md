套接字，就是对网络中不同主机上的应用进程之间进行双向通信的端点的抽象。一个套接字就是网络上进程通信的一端，提供了应用层进程利用网络协议交换数据的机制。

* 1.导入模块

```python
import socket
```

* 2.创建socket对象

```python
socket_obj = socket.socket(AddressFamily, Type)

# AddressFamily:
#     socket.AF_INET
#     socket.AF_INET6
#     socket.AF_UNIX
# 
# Type:
#     socket.SOCK_STREAM -- 流式 TCP
#     socket.SOCK_DGRAM  -- 数据报式 UDP
```

* 3.udp数据传输

```python
# 发
socket_obj.sendto("hello".encode(), ("172.18.0.2", 333))

# 收 (b'hello girl\n', ('172.18.0.3', 333))
recv_data = socket_obj.recvfrom(1024)
recv_data_message = recv_data[0].decode(encoding="UTF-8", errors="strict")  #error: ignore/strict

# 绑定固定端口发送数据
ip_info = ("172.18.0.2", 3333)  #可省略IP
socket_obj.bind(ip_info)

# 广播
socket_obj.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)
socket_obj.sendto("Hello World".encode("UTF-8"), ("172.18.0.255", 3333))
socket_obj.sendto("Hello World".encode("UTF-8"), ("255.255.255.255", 3333))
```

* 4.tcp数据传输

```python
# （1）客户端
## 连接
socket_obj.connect(("IP", PORT))

## 发
socket_obj.send("".encode())

## 收
recv_data = socket_obj.recv(1024) # b'hello girl\n'
recv_data_message = recv_data.decode()

# （2）服务端
## 绑定端口
socket_obj.bind(("IP", PORT))

## 监听，并设置被动模式
socket_obj.listen(128) # 允许128个连接

## 接受连接
return_socket, src_ip_port = socket_obj.accept()
print("Accept a new connection from %s:%d" % (src_ip_port[0], src_ip_port[1]))

## 收
recv_data = return_socket.recv(1024)

## 发
return_socket.send("good".encode())

## 关闭
return_socket.close()

```

* 5.关闭socket

```python
socket_obj.close()
```

* TCP三次握手

![TCP三次握手](../pictures/TCP-三次握手.png)


* 四次挥手

![四次挥手](../pictures/TCP-四次挥手.png)