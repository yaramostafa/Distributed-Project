import socket, threading, pickle, DB
from time import sleep

PORT = 10000
MSGSIZE = 2048
HOST = 'localhost'

def get_elements_except_key(dict, key):
    x = dict.copy()
    try:
        x.pop(key)
    except KeyError:
        pass
    return x

class ClientThread(threading.Thread):
    rooms = {}
    
    def __init__(self, clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        logchoose = pickle.loads(self.csocket.recv(MSGSIZE))
        print(logchoose)
        if(logchoose==2):
            self.player = list(DB.loginToGame(self.csocket))
        elif(logchoose==1):
            self.player = list(DB.signup(self.csocket))
        print("user: '"+ str(self.player[0])+"' Started")
        
        try:
            ClientThread.rooms[
                self.player[2]].update(
                    {self.player[0]: self.player})
        except:
            ClientThread.rooms[self.player[2]] = {}
        
        ClientThread.rooms[
            self.player[2]][
                self.player[0]] = self.player
        print(ClientThread.rooms)
        print(self.player)
        print("[+] New thread started")

    def run(self):
        print("new Connection")
        self.csocket.send(pickle.dumps(self.player))
        self.csocket.send(pickle.dumps("Welcome to the multi-threaded server"))
        
        #sending to waiting for players
        while True:
            room = DB.getRoom(self.player[2])[2]
            countplayers = len(ClientThread.rooms[self.player[2]])
            print("PLAYER_NUM",self.player[3])
            print("NUMBER OF PLAYERS", room)
            while countplayers < room:
                countplayers = len(ClientThread.rooms[self.player[2]])
                self.csocket.send(pickle.dumps(0))
                sleep(1)
            sleep(1)
            self.csocket.send(pickle.dumps("start"))
            break

        while True:
            
            try:
                data = pickle.loads(self.csocket.recv(2048))
                if not data:
                    print("Player"+str(self.player[3])
                          +" Disconnected")
                    #self.player.disconnect = 1
                    ClientThread.rooms[
                        self.player[2]][
                            self.player[0]][-2] = 1
                    DB.updatePlayer(ClientThread.
                                        rooms[self.player[2]]
                                        [self.player[0]], 1)
                    ClientThread.rooms[
                        self.player[2]].pop(self.player[0])
                    if not ClientThread.rooms[self.player[2]]:
                        ClientThread.rooms.pop(self.player[2])
                        DB.deleteRoom(self.player[2])
                    print("updated")
                    break
                else:
                    # if data == 2:
                    #     DB.updatePlayer(ClientThread.
                    #                     rooms[self.player[2]]
                    #                     [self.player[0]])
                    #     self.csocket.send(pickle.dumps('Updated'))
                    #     print("updated")
                    #     continue
                    ClientThread.rooms[self.player[2]][self.player[0]] = data
                    
                    reply = get_elements_except_key(ClientThread.rooms[self.player[2]], data[0])
                    reply = list(reply.values())
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