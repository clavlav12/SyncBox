import socket, cv2, pickle, struct
import os
# Socket Create
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = '0.0.0.0'
print('HOST IP:', host_ip)
port = 9999
socket_address = (host_ip, port)

# Socket Bind
server_socket.bind(socket_address)

# Socket Listen
server_socket.listen(5)
print("LISTENING AT:", socket_address)

every_frame = 10
current_frame = 0
# Socket Accept
while True:
    client_socket, addr = server_socket.accept()
    print('GOT CONNECTION FROM:', addr)
    if client_socket:
        vid = cv2.VideoCapture('the-100.S1E1_1080P.mp4')

        while vid.isOpened():
            print("frame")
            img, frame = vid.read()

            scale_percent = 50  # percent of original size
            width = int(frame.shape[1] * scale_percent / 100)
            height = int(frame.shape[0] * scale_percent / 100)
            dim = (width, height)
            # resize image
            frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

            current_frame += 1
            if not current_frame % every_frame:
                a = pickle.dumps(frame)
                message = struct.pack("Q", len(a)) + a
                client_socket.sendall(message)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow('TRANSMITTING VIDEO', gray)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                client_socket.close()
