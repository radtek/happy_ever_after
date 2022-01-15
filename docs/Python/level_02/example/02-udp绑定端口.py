import socket

# Create object
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind port
# udp_socket.bind("172.18.0.2", 3333)
ip_info = ("172.18.0.2", 3333)
udp_socket.bind(ip_info)

# Send message
udp_socket.sendto("helloworld\n".encode(), ("172.18.0.3", 333))

# Receive and print message
recv_data = udp_socket.recvfrom(1024)
print(recv_data)
print(recv_data[0].decode(encoding="UTF-8"))

# Close object
udp_socket.close()

