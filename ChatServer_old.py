import socket, threading


class ClientThread(threading.Thread):
    clientSockets = []

    def __init__(self,ip,port,clientsocket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.csocket = clientsocket
        self.clientSockets.append(clientsocket)
        print("[+] New thread started for ",ip,":",str(port))

    def run(self):
        print("Connection from : ",self.ip,":",str(self.port))

        self.csocket.send("Welcome to the multi-threaded server".encode())

        name = self.csocket.recv(2048).decode()
        data = name.replace(" ", "") + " just joined the chat!"
        for client in self.clientSockets[::2]:
            client.send(data.encode())
        print(name.replace(" ", ""), "just joined the chat!")
        data = "dummydata"

        while len(data):
            data = self.csocket.recv(2048)
            print("Client(%s:%s) sent : %s"%(self.ip, str(self.port), data.decode()))
            if data.decode().split(":")[1].replace(" ","") == "quit":
                data = ''
                print("QUIT")
            else:
                for client in self.clientSockets[::2]:
                    client.send(data)
                    print("Sent ",data," to ",client)


        self.csocket.send(str.encode("Ok Bye Bye"))

        index = self.clientSockets.index(self.csocket)
        self.clientSockets[index-1].close()
        del self.clientSockets[index]
        del self.clientSockets[index-1]
        print("New ClientSocketList: ",self.clientSockets)
        self.csocket.close()
        data = name.replace(" ", "") + " just left the chat.."
        for client in self.clientSockets[::2]:
            client.send(data.encode())
        print ("Client at ",self.ip," disconnected...")
host = "0.0.0.0"
port = 10000

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind((host, port))
while True:
    serverSocket.listen(4)
    print("Listening for incoming connections...")
    (clientsock, (ip, port)) = serverSocket.accept()
    clientThread = ClientThread(ip, port, clientsock)
    clientThread.start()