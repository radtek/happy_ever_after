import socket 


tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server_socket.bind(("", 3333))
tcp_server_socket.listen(127)

new_socket, src_ip_info = tcp_server_socket.accept()
print("Accept a new connection from %s:%d" % (src_ip_info[0], src_ip_info[1]))

new_socket.send("Welcome!".encode())
while True:

    recv_data = new_socket.recv(1024)
    # if len(recv_data) == 0:
    if recv_data:
        print("Messages from [%s]: %s" % (src_ip_info, recv_data.decode()))
    else:
        print("Client closed...")
        break

new_socket.close()

tcp_server_socket.close()