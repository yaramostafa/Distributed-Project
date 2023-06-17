import socket, threading, pickle
from cargame import *
import DB

PORT = 10000
MSGSIZE = 2048
HOST = 'localhost'



class ClientThread(threading.Thread):
    
    
    def __init__(self, clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        logchoose = pickle.loads(self.csocket.recv(MSGSIZE))
        print(logchoose)
        if(logchoose==2):
            self.player = list(DB.loginToGame(self.csocket))
        elif(logchoose==1):
            self.player = list(DB.signup(self.csocket))
        print(self.player)
        
        

        print("[+] New thread started")

    def run(self):
        print("new Connection")
        self.csocket.send(pickle.dumps(self.player))
        self.csocket.send(pickle.dumps("Welcome to the multi-threaded server"))
        
        #sending to waiting for players
        while True:
            room = DB.getRoom(self.player[2])[2]
            countplayers = DB.getCountPlayers(self.player[2])
            print("PLAYER_NUM",self.player[3])
            print("NUMBER OF PLAYERS", room)
            while countplayers < room:
                countplayers = DB.getCountPlayers(self.player[2])
                self.csocket.send(pickle.dumps(0))
                sleep(1)
            sleep(1)
            self.csocket.send(pickle.dumps("start"))
            break

        while True:
            try:
                data = pickle.loads(self.csocket.recv(2048))

                if not data:
                    print("Player"+str(self.player[3])+" Disconnected")
                    #self.player.disconnect = 1
                    self.player[-2] = 1
                    break
                else:
                    self.player = data
                    reply = DB.getOpponents(self.player[0])
                    print("Received: ", data)
                    print("Sending : ", reply)

                self.csocket.sendall(pickle.dumps(reply))
            except:
                break


serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind((HOST, PORT))

while True:
    serverSocket.listen(4)
    print("Listening for incoming connections...")
    (clientsock, _) = serverSocket.accept()
    clientThread = ClientThread(clientsock)
    clientThread.start()