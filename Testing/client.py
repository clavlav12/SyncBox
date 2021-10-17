import socket
import pickle

client_socket = socket.socket()
client_socket.connect(('127.0.0.1', 5005))
data = client_socket.recv(1024)
lines = data.splitlines()
print(lines)
print(pickle.loads(lines[1]))
