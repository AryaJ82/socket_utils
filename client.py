

import socket
import sys
import threading

IP = '127.0.0.1'
PORT = 2255

class ServerClient:
    def __init__(self, IP, PORT) -> None:
        """ Creates a <ServerClient> object that will send console
        input to IP, PORT
        """
        self.data = ['']
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.connect((IP, PORT))
    
    def _inp(self):
        """
        Threaded method which takes input from the console
        <index>;<message> to send to <index> of the associated server
        """
        self.data[0] = input("")
    
    def _receive(self):
        """
        Threaded method which recieves data from IP:PORT
        """
        while True:
            rcv_len = 1
            response = ""
            while rcv_len:
                data = self.socket.recv(4096)
                rcv_len = len(data)
                response += data.decode()
                if rcv_len < 4096:
                    break
            if response:
                print(response)

    def handle_connection(self):
        """
        Method which implements communication between self and
        the server
        """
        rcv = threading.Thread(target=self._receive, daemon=True)
        rcv.start()

        try:
            while True:
                snd = threading.Thread(target=self._inp, daemon=True)
                snd.start()
                snd.join()
                # when snd terminates it writes to the mutable attribute
                # self.data; no need to handle a return value
                self.socket.send(self.data[0].encode())

        except:
            print("Connection terminated")
            self.socket.close()
            sys.exit()

def main():
    client = ServerClient(IP, PORT)
    client.handle_connection()

if __name__ == '__main__':
    main()