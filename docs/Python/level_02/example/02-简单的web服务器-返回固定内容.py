# 1. 导入模块
# 2. 创建套接字
# 3. 设置地址重用
# 4. 绑定端口
# 5. 修改为被动模式(监听)
# 6. 客户端连接
# 7. 接受客户端发送的请求协议
# 8. 判断协议是否为空
# 9. 拼接响应报文
# 10. 发送响应报文
# 11. 执行关闭操作

import socket
import time


def request_handler(client_socket, ip_port):
    
    request_data = client_socket.recv(4096)

    if not request_data:
        print("Client connection closed!")
        client_socket.close()
        return
    
    response_line = "HTTP/1.1 200 OK\r\n"
    response_head = "Server: Python 3.9 Web Server\r\n"
    response_blank = "\r\n"
    response_body = "Hello World! Time is " + time.asctime()

    response_msg = response_line + response_head + response_blank + response_body
    client_socket.send(response_msg.encode())

    client_socket.close()


def main():

    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    tcp_server_socket.bind(("192.168.161.101", 333))
    tcp_server_socket.listen(128)
    
    while True:
        new_client_socket, client_ip_port = tcp_server_socket.accept()
        request_handler(new_client_socket, client_ip_port)

    # tcp_server_socket.close()


if __name__ == "__main__":

    main()