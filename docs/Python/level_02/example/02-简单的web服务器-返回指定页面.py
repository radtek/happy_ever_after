# 根据不同请求返回不同页面
import socket
# import time


def request_handler(client_socket, ip_port):
    
    request_data = client_socket.recv(4096)

    if not request_data:
        print("Client connection closed!")
        client_socket.close()
        return
    
    request_msg = request_data.decode()

    # # 方法一
    # loc1 = request_msg.find("/")
    # loc2 = request_msg.find(" ", loc1)
    # if loc1 + 1 == loc2:
    #     file_name = "index.html"
    # else:
    #     file_name = request_msg[loc1+1:loc2]

    # 方法二
    loc = request_msg.find("\r\n")
    request_line = request_msg[:loc]
    request_line_list = request_line.split(" ")
    file_name = request_line_list[1]
    if file_name == "/":
        file_name = "/index.html"
    # else:
    #     file_name = file_name[1:] 

    response_line = "HTTP/1.1 200 OK\r\n"
    response_head = "Server: Python 3.9 Web Server\r\n"
    response_blank = "\r\n"

    try:
        with open("source"+file_name, "rb") as file:
            response_body = file.read()
    except Exception as e:
        response_line = "HTTP/1.1 404 Not Found\r\n"
        error_msg = "Error!" + str(e)
        response_body = error_msg.encode()

    response_msg = (response_line + response_head + response_blank).encode() + response_body
    client_socket.send(response_msg)

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