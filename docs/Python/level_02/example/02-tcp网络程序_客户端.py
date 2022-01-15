import socket 


tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_client_socket.connect(("172.18.0.3", 3333))

tcp_client_socket.send("Hello, this is 172.18.0.2.".encode())

recv_data = tcp_client_socket.recv(1024)
print(recv_data.decode())

tcp_client_socket.close()