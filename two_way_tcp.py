########################
# Author: Arya Jafari
# Description: A two way TCP connection/communication
#########################

import socket
import sys
import threading

IP = '127.0.0.1'
PORT = 2255


class Server:
    def __init__(self, mode="server"):
        print(f"initializing in {mode} mode")
        self.data = ['', '']
        # [0] = input()
        # [1] may equal the received data
        self.mode = mode
        # mode defines whether the object is in server mode or client mode
        # default is server mode
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def _inp_loop(self):
        self.data[0] = input()

    def _listen_loop(self, client):
        # self.socket.bind((self.target["ip"], self.target["port"]))
        # self.socket.listen(5)
        while True:
            rcv_len = 1
            response = ""
            while rcv_len:
                data = client.recv(4096)
                rcv_len = len(data)
                response += data.decode()
                if rcv_len < 4096:
                    break
            if response:
                print(response)

    def _send(self, client):
        client.send(self.data[0].encode())
        self.data[0] = ""

    def handle_client(self):
        if self.mode == "server":
            self.socket.bind((IP, PORT))
            self.socket.listen(5)
            client, address = self.socket.accept()
        else: # in client mode
            self.socket.connect((IP, PORT))
            client = self.socket

        rcv_data = threading.Thread(target=self._listen_loop, args=(client,), daemon=True)
        rcv_data.start()

        try:
            while True:
                snd = threading.Thread(target=self._inp_loop, daemon=True)
                snd.start()
                snd.join()
                # when snd terminates it writes to the mutable attribute
                # self.data; no need to handle a return value
                self._send(client)

        except KeyboardInterrupt:
            print("connection terminated")
            self.socket.close()
            sys.exit()


def main():
    server = Server(sys.argv[1])
    server.handle_client()

#
# def main():
#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server.bind((IP, PORT))
#     server.listen(5)
#     print(f'[*] Listening on {IP}:{PORT}')
#
#     while True:
#         client, address = server.accept()
#         print(f'[*] Listening on {address[0]}:{address[1]}')
#         client_handler = threading.Thread(target=handle_client, args=(client,))
#         client_handler.start()
#
#
# def handle_client(client_socket):
#     with client_socket as sock:
#         request = sock.recv(1024)
#         print(f'[*] Listening on {request.decode("utf-8")}')
#         sock.send(b'ACK')


if __name__ == '__main__':
    main()
