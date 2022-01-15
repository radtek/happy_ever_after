# 1. 导入模块
# 2. 创建套接字
# 3. 建立连接
# 4. 拼接请求协议
# 5. 发送请求协议
# 6. 接受服务器响应内容
# 7. 保存内容
# 8. 关闭连接

import socket


tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_client_socket.connect(("192.168.161.201", 80))

request_line = "GET / HTTP/1.1\r\n"
request_head = "Host: 192.168.161.201\r\n"
request_blank = "\r\n"
request_msg = request_line + request_head + request_blank

tcp_client_socket.send(request_msg.encode())
recv_data = tcp_client_socket.recv(4096)
recv_msg = recv_data.decode()

loc = recv_msg.find("\r\n\r\n")

print(recv_msg[loc+4:])

tcp_client_socket.close()