import socket
import pickle


def get_data():
    a = ['avi', 'noam', 'Yosef']
    data = pickle.dumps(a)
    return data


server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 5005))
server_socket.listen(1)
sock, address = server_socket.accept()
sock.send(b'hello\n' + get_data())
server_socket.close()