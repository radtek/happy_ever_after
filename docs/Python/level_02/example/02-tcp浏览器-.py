import socket


tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.connect(("127.0.0.1", 80))

request_line = "GET / HTTP/1.1\r\n"
request_head = "Host: 127.0.0.1\r\n"
request_blank = "\r\n"

request_msg = request_line + request_head + request_blank
tcp_socket.send(request_msg.encode())
recv_data = tcp_socket.recv(4096)
recv_text = recv_data.decode()

# with open("index.html", "w") as file:
#     file.write(recv_text)

tcp_socket.close()