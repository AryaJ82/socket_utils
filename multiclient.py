#####################
## Author: Arya Jafari
## Description: A socket programming project based on star topology.
##  <Server> object that acts as relay between <ServerClient> 
##  objects.
#####################

import socket
import sys
import threading
import concurrent.futures

IP = '127.0.0.1'
PORT = 2255


class Server:
    def __init__(self, IP, PORT) -> None:
        self.connections = []
        self.data = []
        self.con_threads = concurrent.futures.ThreadPoolExecutor()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((IP, PORT))
        self.socket.listen(5)
    
    def _listen_loop(self, client):
        """
        Threaded loop that listens to <client> for packets
        """
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
                if(response[0] == "/"):
                    print(f"Command intercept for {client.getsockname()}")
                    com = response[1:]
                    # Imagine not having switch/cases. I certainly can't.
                    if(com == "con"):
                        s = ""
                        for con in self.connections:
                            s += f"\t {con[1][0]}:{con[1][1]} \n"
                        client.send(s.encode())
                else:
                    self.data.append(response)
    
    def _connect(self) -> None:
        """
        Threaded method that listens for new connections on self.IP
        """
        while True:
            self.connections.append(self.socket.accept())
            print((f"[SERVER]: Connected to {self.connections[-1][1][0]}:"
                   f"{self.connections[-1][1][1]}"))
            self.con_threads.submit(self._listen_loop, self.connections[-1][0])

    
    def handle_clients(self):
        make_connection = threading.Thread(target=self._connect, daemon=True)
        make_connection.start()

        try:
            while True:
                while self.data:
                    r = self.data.pop()
                    s = r.find(";")
                    dest = r[:s]
                    dat = r[(s+1):]
                    try:
                        print((f"Sending '{dat}' to {self.connections[int(dest)][1][0]}:"
                               f"{self.connections[int(dest)][1][1]}"))
                        self.connections[int(dest)][0].send(dat.encode())
                        
                    except:
                        print(f"Sending '{dat}' to all clients")
                        dat = dat.encode()
                        for con in self.connections:
                            con[0].send(dat)

        except KeyboardInterrupt:
            print("connection terminated")
            self.socket.close()
            sys.exit()

def main():
    server = Server(IP, PORT)
    server.handle_clients()

if __name__ == '__main__':
    main()