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
            self.player = DB.loginToGame(self.csocket)
        elif(logchoose==1):
            self.player = DB.signup(self.csocket)
        
        print(self.player)
        # print(self.number_of_players)
        
        # Check if game exists
        
        # self.game = 0
        # for game in ClientThread.games:
        #     if (game.number_of_players == self.number_of_players) and game.start==0: #and game.start==0
        #         self.game = game
        #         print("Game exists")
        # if isinstance(self.game, int):
        #     self.game = Game(self.number_of_players)
        #     ClientThread.games.append(self.game)
        

        print("[+] New thread started")

    def run(self):
        print("new Connection")
        self.csocket.send(pickle.dumps(self.player))

        self.csocket.send(pickle.dumps("Welcome to the multi-threaded server"))
        #sending to waiting for players
        while True:
            print("PLAYER_NUM",self.game.player_counter)
            print("NUMBER OF PLAYERS", self.game.number_of_players)
            while self.game.player_counter < self.game.number_of_players:
                self.csocket.send(pickle.dumps('asd'))
                sleep(1)
            sleep(1)
            self.csocket.send(pickle.dumps("start"))
            self.game.start = 1
            break

        while True:
            try:
                data = pickle.loads(self.csocket.recv(2048))

                if not data:
                    print("Player"+str(self.player.Player_num)+" Disconnected")
                    #self.player.disconnect = 1
                    self.game.players[self.player.Player_num-1].disconnect = 1
                    break
                else:
                    self.game.players[self.player.Player_num - 1] = data
                    reply = [self.game.players[i] for i in range(len(self.game.players)) if i !=self.player.Player_num-1]

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