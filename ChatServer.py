import socket, threading


class Client:
    def __init__(self):
        (clientsockSend, (ipS, portS)) = serverSocket.accept()
        self.Tsend = ClientThread(ipS,portS,clientsockSend,'send')
        self.Tsend.start()
        (clientsockRcv, (ipR, portR)) = serverSocket.accept()
        self.Trcv = ClientThread(ipR,portR,clientsockRcv,'rcv')
        self.Trcv.start()


class ClientThread(threading.Thread):
    clientSocketSend = []
    clientSocketRcv = []
    clientTRcv = []
    clientTSend = []
    i = 0

    def __init__(self,ip,port,clientsocket,type):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.csocket = clientsocket
        self.type = type
        self.id = ClientThread.i
        print(self.i)
        if self.type == 'rcv':
            self.clientTRcv.append(self)
            self.clientSocketRcv.append(clientsocket)
            ClientThread.i +=1
        else:
            self.clientTSend.append(self)
            self.clientSocketSend.append(clientsocket)

        print("[+] New thread started for ",ip,":",str(port))

    def run(self):
        print("Connection from : ",self.ip,":",str(self.port))
        if self.type == 'send':
            self.csocket.send("Welcome to the multi-threaded server".encode())

        else:
            name = self.csocket.recv(2048).decode()
            welcomeMsg = name.replace(" ", "") + " just joined the chat!"
            print(welcomeMsg)
            self.clientTSend[self.id].newmember(welcomeMsg)

            data = "dummydata"
            while len(data):
                data = self.csocket.recv(2048)
                print("Client(%s:%s) sent : %s"%(self.ip, str(self.port), data.decode()))
                if data.decode().split(":")[1].replace(" ","") == "quit":
                    data = ''
                    print("QUIT")
                else:
                    self.sendtoall(data)

            disconnectMsg = name + " disconnected from chat"
            self.sendtoall(disconnectMsg.encode())
            self.clientSocketSend[self.id].close()
            ClientThread.clientSocketSend[self.id] = 0
            self.csocket.close()
            print("Client at ",self.ip," disconnected...")

    def newmember(self,name):
        for client in ClientThread.clientSocketSend:
            if not isinstance(client, int):
                client.send(name.encode())

    def sendtoall(self,data):
        for client in ClientThread.clientSocketSend:
            if not isinstance(client, int):
                client.send(data)
                print("Sent ", data, " to ", client)

host = "0.0.0.0"
port = 10001

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind((host, port))
while True:
    serverSocket.listen(4)
    print("Listening for incoming connections...")
    newClient = Client()