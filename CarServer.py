import socket, threading, DB, SocketUtils as SU
from time import sleep

PORT = 10000
MSGSIZE = 2048
HOST = '0.0.0.0'

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
        self.dc = False
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        logchoose = SU.receiveInt(self.csocket, self)
        if self.dc:
            return
        print(logchoose)
        if(logchoose==2):
            self.player = DB.sLogin(self.csocket, self)
        elif(logchoose==1):
            self.player = DB.signup(self.csocket, self)
        if self.dc:
            return
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
        if self.dc:
            return
        print("new Connection")
        SU.sendArr(self.csocket, self.player)
        _ = SU.receiveInt(self.csocket)
        sleep(1)
        
        #sending to waiting for players
        while True:
            room = DB.getRoom(self.player[2])[2]
            countplayers = len(ClientThread.rooms[self.player[2]])
            print("PLAYER_NUM",self.player[3])
            print("NUMBER OF PLAYERS", room)
            while countplayers < room:
                countplayers = len(ClientThread.rooms[self.player[2]])
                
                sleep(1)
            sleep(1)
            SU.send(self.csocket, "start")
            break
        x=0
        while True:
            try:
                rec = SU.receiveArr(self.csocket, self)
                if not rec:
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
                    # if rec == 2:
                    #     DB.updatePlayer(ClientThread.
                    #                     rooms[self.player[2]]
                    #                     [self.player[0]])
                    #     self.csocket.send(pickle.dumps('Updated'))
                    #     print("updated")
                    #     continue
                    rec[0] = int(rec[0])
                    rec[2] = int(rec[2])
                    rec[3] = int(rec[3])
                    rec[4] = int(rec[4])
                    rec[5] = int(rec[5])
                    rec[6] = int(rec[6])
                    rec[7] = int(rec[7])
                    ClientThread.rooms[self.player[2]][self.player[0]] = rec
                    
                    reply = get_elements_except_key(ClientThread.rooms[self.player[2]], rec[0])
                    reply = list(reply.values())
                    x+=1
                    if x%100==0:
                        DB.updatePlayer(rec, 0)
                SU.send(self.csocket, len(reply))
                for i in reply:
                    _ = SU.receiveInt(self.csocket)
                    SU.sendArr(self.csocket, i)
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
