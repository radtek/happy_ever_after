import socket
import time
import threading


def send_msg(s):
    msg = input("What do you want to send? ")
    ip = input("IP: ")
    port = input("Port: ")

    if len(ip) == 0:
        ip = '127.0.0.1'

    if not port:
        port = 3334

    s.sendto(msg.encode('utf8'), ((ip, int(port))))


def recv_msg(s):
    while True:
        msg, ip_port = s.recvfrom(1024)
        print("Message from %s:%s: %s" % (ip_port[0], ip_port[1], msg.decode('utf-8')))


def print_menu():
    print("**** 1. Send message *******")
    print("**** 2. Receive message ****")
    print("**** 3. Exit ***************")


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("", 3333))

    t = threading.Thread(target = recv_msg, args = (s, ))
    t.setDaemon(True)
    t.start()
    
    while True:
        print_menu()
        opts = input("Please choose: ")
        if opts == "3":
            return
        elif opts == "1":
            send_msg(s)
        elif opts == "2":
            recv_msg(s)
        else:
            print("Error! Please choose one.")
            continue

if __name__ == "__main__":
    main()