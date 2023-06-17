import socket

HOST = "54.160.162.228"
PORT = 10001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    message = input("Enter message: ")
    s.sendall(message.encode())
    data = s.recv(1024)
    print("Received from server:", data.decode())

