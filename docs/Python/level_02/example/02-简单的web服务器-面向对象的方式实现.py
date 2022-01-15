import socket
import time


class HttpServer:
    
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.sock.bind((self.ip, self.port))
        self.sock.listen(128)

        while True:
            self.client_socket, self.client_ip_port = self.sock.accept()
            self.request_handler()

    def request_handler(self):
            request_data = self.client_socket.recv(4096)

            if not request_data:
                print("Client connection closed!")
                self.client_socket.close()
                return
            
            request_msg = request_data.decode()

            # # 方法一
            # loc1 = request_msg.find("/")
            # loc2 = request_msg.find(" ", loc1)
            # if loc1 + 1 == loc2:
            #     file_name = "index.html"
            # else:
            #     file_name = request_msg[loc1+1:loc2]

            # 方法二
            loc = request_msg.find("\r\n")
            request_line = request_msg[:loc]
            request_line_list = request_line.split(" ")
            file_name = request_line_list[1]
            if file_name == "/":
                file_name = "/index.html"
            # else:
            #     file_name = file_name[1:] 

            response_line = "HTTP/1.1 200 OK\r\n"
            response_head = "Server: Python 3.9 Web Server\r\n"
            response_blank = "\r\n"

            try:
                with open("source"+file_name, "rb") as file:
                    response_body = file.read()
            except Exception as e:
                response_line = "HTTP/1.1 404 Not Found\r\n"
                error_msg = "Error!" + str(e)
                response_body = error_msg.encode()

            response_msg = (response_line + response_head + response_blank).encode() + response_body
            self.client_socket.send(response_msg)

            self.client_socket.close()
    
    # def response_msg(self):
    #     pass

    def close(self):

        self.sock.close()


def main():
    hs = HttpServer("192.168.161.101", 3333)
    hs.start()
    hs.stop()


if __name__ == "__main__":
    main()



