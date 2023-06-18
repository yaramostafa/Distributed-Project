import MySQLdb
import pickle

def send(csocket, data):
    csocket.send(pickle.dumps(data))

def receive(csocket):
    return pickle.loads(csocket.recv(2048))

db = MySQLdb.connect(host='localhost',  # your host, usually localhost
                     user='root',       # your username
                     passwd='',         # your password
                     db='race-chat')

cur = db.cursor()

def signup(csocket):
    send(csocket, 'Signing Up: ')
    username = receive(csocket)
    while True:
        try:
            cur.execute("INSERT INTO player (username, xCoord, yCoord) VALUES ('"
                        +username+"', 0, 0)")
            send(csocket, 1)
            send(csocket, 'Signed Up: ')
            print(receive(csocket))
            break
        except:
            send(csocket, 0)
            username = receive(csocket)
            continue
    db.commit()
    return loginToGame(csocket)
    
def loginToGame(csocket):
    send(csocket, 'Logging in: ')
    user = receive(csocket)
    while True:
        cur.execute("SELECT * FROM player WHERE username= '"
                    +user+"'")
        account = cur.fetchone()
        if not account:
            send(csocket, 0)
            send(csocket, 'User not found\n')
            user = receive(csocket)
            continue
        else:
            send(csocket, 1)
            if not account[2]>0:
                send(csocket, 2)
                send(csocket,'Press 1 to Create a room')
                send(csocket,'Press 2 to join an exisiting room')
                createorjoin = receive(csocket)
                if createorjoin==1:
                    createRoom(csocket, account)
                elif createorjoin==2:
                    roomname=receive(csocket)
                    cur.execute("SELECT * FROM room WHERE rName = '"
                                +roomname+"'")
                    room = cur.fetchone()
                    cur.execute("SELECT COUNT(*) FROM player "
                                +"WHERE rID = '"+str(room[0])+"'")
                    currplayers = cur.fetchone()[0]
                    while not (currplayers<room[2] or room):
                        send(csocket, 1)
                        roomname = receive(csocket)
                        cur.execute("SELECT * FROM room WHERE rName = '"
                                    +roomname+"'")
                        room = cur.fetchone()
                        cur.execute("SELECT COUNT(*) FROM player "+
                                    "WHERE rID = '"+str(room[0])+"'")
                        currplayers = cur.fetchone()[0]
                    
                    send(csocket, 0)
                    finalizePlayer(room[0], account)
                    print(receive(csocket))
            else:
                updatePlayer(account, 0)
                send(csocket, 3)
            break
    cur.execute("SELECT * FROM player WHERE username= '"
                +user+"'")
    account = cur.fetchone()
    return account

def getRoom(rID):
    cur.execute("SELECT * FROM room WHERE rID = '"
                +str(rID)+"'")
    return cur.fetchone()

def createRoom(csocket, account):
    roomname = receive(csocket)
    numPlayers = receive(csocket)
    while True:
        try:
            cur.execute("INSERT INTO room (rName, numPlayers) VALUES ('"
                        +roomname+"', '"+numPlayers+"')")
            db.commit()
            cur.execute("SELECT rID FROM room WHERE rName='"
                        +roomname+"'")
            rID = cur.fetchone()[0]
            finalizePlayer(rID, account)
            send(csocket, 4)
            print(receive(csocket))
            break
        except:
            send(csocket, 5)
            send(csocket, 'Error! enter correct details')
            roomname = receive(csocket)
            numPlayers = receive(csocket)
            
            
def finalizePlayer(rID, account):
    cur.execute("UPDATE player SET rID = '"
                +str(rID)+"', dc = '0' "+
                " WHERE pID = '"
                +str(account[0])+"'")
    db.commit()
    cur.execute(
        "SELECT COUNT(*) FROM player WHERE rID= "+
        "(SELECT rID FROM player WHERE pID = '"
        +str(account[0])+"')")
    counter = cur.fetchone()
    cur.execute("UPDATE player SET xCoord = '"
                +str(1300 * (0.1+0.2*(counter[0]-1)))+
                "', yCoord = '"
                +str(600 * 0.8)+"', filepath = '.\\\img\\\car"
                +str(counter[0])+".png', counter ='"
                +str(counter[0])+"' WHERE pID = '"
                +str(account[0])+"'")
    db.commit()
    
def getOpponents(pID):
    cur.execute("SELECT * FROM player WHERE"+
                " rID = (SELECT rID FROM player WHERE pID = '"
                +str(pID)+"') AND NOT pID = '"+str(pID)+"'")
    x = []
    for i in cur.fetchall():
        i = list(i)
        x+=[i]
    return x

def getCountPlayers(rID):
    cur.execute("SELECT COUNT(*) FROM player WHERE"+
                " rID = '"+str(rID)+"'")
    return cur.fetchone()[0]

def updatePlayer(player, dc):
    cur.execute("UPDATE player SET xCoord = '"+str(player[4])+"',"+
                " yCoord = '"+str(player[5])+"', score = '"+str(player[6])+"',"+
                " dc = '"+str(dc)+"' WHERE pID = '"+str(player[0])+"'")
    db.commit()
    
def deleteRoom(rID):
    cur.execute("DELETE FROM player WHERE rID = '"+str(rID)+"'")
    cur.execute("DELETE FROM room WHERE rID = '"+str(rID)+"'")
    db.commit()
    