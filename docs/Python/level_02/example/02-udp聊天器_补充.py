import socket 


def send_msg(udp_socket):
    ip = input("IP: ")
    port = input("Port: ")
    content = input("Messages: ")

    if len(ip) == 0:
        ip = "172.18.0.2"

    if len(port) == 0:
        port = "333"
    
    udp_socket.sendto(content.encode(), (ip, int(port)))


def recv_msg(udp_socket):
    recv_data, recv_ip = udp_socket.recvfrom(1024)
    recv_msg = recv_data.decode()

    print("Messages from [%s:%s]: %s" % (recv_ip[0], recv_ip[1], recv_msg))


def print_menu():
    print("**** 1. Send message *******")
    print("**** 2. Receive message ****")
    print("**** 3. Exit ***************")


def main():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("", 333))

    while True:
        print_menu()
        opts = input("Please choose an option: ")
        if opts == "3":
            break
        elif opts == "1":
            send_msg(udp_socket)
        elif opts == "2":
            recv_msg(udp_socket)
        else:
            print("Error! Only one of 1|2|3 !")
            continue

    udp_socket.close()


if __name__ == "__main__":
    main()
