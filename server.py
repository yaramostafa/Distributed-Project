import socket

HOST = "0.0.0.0"
PORT = 10001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

while True:
    conn, addr = s.accept()
    print("Connected by", addr)

    while True:
        data = conn.recv(1024)
        if not data:
            break
        print("Received from client:", data.decode())
        conn.sendall("Hello".encode())

    conn.close()

