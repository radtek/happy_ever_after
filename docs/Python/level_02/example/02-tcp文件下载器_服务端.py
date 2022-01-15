import socket 


tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

tcp_server_socket.bind(("172.18.0.2", 3333))
tcp_server_socket.listen(128)

connect_socket, client_ip_port = tcp_server_socket.accept()

recv_data = connect_socket.recv(1024)
file_name = recv_data.decode()

print(file_name)

with open(file_name, "rb") as file:
    while True:
        file_data = file.read(1024)
        if file_data:
            connect_socket.send(file_data)
        else:
            break


connect_socket.close()
tcp_server_socket.close()