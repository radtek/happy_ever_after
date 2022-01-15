import socket
# import time


def request_handler(client_socket, ip_port):
    
    request_data = client_socket.recv(4096)

    if not request_data:
        print("Client connection closed!")
        client_socket.close()
        return
    
    response_line = "HTTP/1.1 200 OK\r\n"
    response_head = "Server: Python 3.9 Web Server\r\n"
    response_blank = "\r\n"
    # response_body = "Hello World! Time is " + time.asctime()
    with open("index.html", "rb") as file:
        response_body = file.read()

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