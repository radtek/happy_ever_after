import socket


udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)

send_content = "Hello World"
send_data = send_content.encode("UTF-8")

udp_socket.sendto(send_data, ("255.255.255.255", 3333))

udp_socket.close()