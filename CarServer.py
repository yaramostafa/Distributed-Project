import socket, threading, pickle
from cargame import *





class ClientThread(threading.Thread):
    #players_number = 0
    #players = [Player(1), Player(2), Player(3), Player(4)]
    games = []
    scores = [0,0,0,0]

    startflag = 0

    def __init__(self,ip,port,clientsocket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.csocket = clientsocket
        self.number_of_players = pickle.loads(self.csocket.recv(2048))
        print(self.number_of_players)
        self.game = 0
        for game in ClientThread.games:
            if (game.number_of_players == self.number_of_players) and game.start==0: #and game.start==0
                self.game = game
                print("Game exists")
        if isinstance(self.game, int):
            self.game = Game(self.number_of_players)
            ClientThread.games.append(self.game)
        self.player = self.game.create_player()

        print("[+] New thread started for ",ip,":",str(port))

    def run(self):
        print("Connection from : ",self.ip,":",str(self.port))
        self.csocket.send(pickle.dumps(self.player))

        self.csocket.send(pickle.dumps("Welcome to the multi-threaded server"))

        while True:
            print("PLAYER_NUM",self.game.player_counter)
            print("NUMBER OF PLAYERS", self.game.number_of_players)
            if self.game.player_counter < self.game.number_of_players:
                while self.game.player_counter < self.game.number_of_players:
                    self.csocket.send(pickle.dumps(self.game.player_counter))
                    sleep(1)
            else:
                sleep(1)
            self.csocket.send(pickle.dumps("start"))
            self.game.start = 1
            break

        reply = ""
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