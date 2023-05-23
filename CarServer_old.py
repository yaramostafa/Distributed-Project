import socket, threading, pickle
from cargame import *





class ClientThread(threading.Thread):
    players_number = 0
    players = [Player(1), Player(2), Player(3), Player(4)]
    scores = [0,0,0,0]
    startflag = 0

    def __init__(self,ip,port,clientsocket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.csocket = clientsocket
        self.player_num = ClientThread.players[ClientThread.players_number].Player_num
        ClientThread.players_number += 1

        print("[+] New thread started for ",ip,":",str(port))

    def run(self):
        print("Connection from : ",self.ip,":",str(self.port))
        self.csocket.send(pickle.dumps(ClientThread.players[self.player_num-1]))

        self.csocket.send(pickle.dumps("Welcome to the multi-threaded server"))

        # while True:
        #     if ClientThread.players_number != 4:
        #         while ClientThread.players_number < 4:
        #             self.csocket.send(pickle.dumps(ClientThread.players_number))
        #             sleep(1)
        #     else:
        #         sleep(1)
        #     self.csocket.send(pickle.dumps("start"))
        #     break

        reply = ""
        while True:
            try:
                data = pickle.loads(self.csocket.recv(2048))

                if not data:
                    print("Player"+str(self.player_num)+" Disconnected")
                    ClientThread.players[self.player_num-1].disconnect = 1
                    break
                else:
                    ClientThread.players[self.player_num - 1] = data
                    reply = [ClientThread.players[i] for i in range(len(ClientThread.players)) if i !=self.player_num-1]

                    print("Received: ", data)
                    print("Sending : ", reply)

                self.csocket.sendall(pickle.dumps(reply))
            except:
                break

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