
import socket
import threading

target_host = '127.0.0.1'
target_port = 9998

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((target_host, target_port))

x = "ABCDEF"
client.send(x.encode())

response = client.recv(4096)

print(response.decode())
client.close()

