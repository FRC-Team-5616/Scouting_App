import socket

ServerSocket = socket.socket()
host = '192.168.0.11'
port = 2048
ServerSocket.connect((host, port))
while True:
    ServerSocket.send(input("Send: ").encode("utf-8"))
    print(ServerSocket.recv(2000).decode("utf-8"))
