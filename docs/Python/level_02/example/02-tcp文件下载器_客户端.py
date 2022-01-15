import socket 


tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 172.18.0.3:333(C) --> 172.18.0.2:3333(S)
tcp_client_socket.bind(("172.18.0.3", 333))
tcp_client_socket.connect(("172.18.0.2", 3333))

file_name = input("Please enter the name of file you want to download: ")
tcp_client_socket.send(file_name.encode())

with open("/tmp/recv.txt", "wb") as file:

    while True:
        file_data = tcp_client_socket.recv(1024)
        if file_data:
            file.write(file_data)
        else:
            break

tcp_client_socket.close()