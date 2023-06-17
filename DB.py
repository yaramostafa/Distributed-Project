import MySQLdb
import pickle
MSGSIZE = 2048

db = MySQLdb.connect(host='localhost',  # your host, usually localhost
                     user='root',       # your username
                     passwd='',         # your password
                     db='race-chat')

cur = db.cursor()

def signup(csocket):
    csocket.send(pickle.dumps('Signing Up: '))
    username = pickle.loads(csocket.recv(MSGSIZE))
    while True:
        try:
            cur.execute("INSERT INTO player (username, xCoord, yCoord) VALUES ('"
                        +username+"', 0, 0)")
            csocket.send(pickle.dumps(1))
            csocket.send(pickle.dumps('Signed Up: '))
            print(pickle.loads(csocket.recv(MSGSIZE)))
            break
        except:
            csocket.send(pickle.dumps(0))
            username = pickle.loads(csocket.recv(MSGSIZE))
            continue
    db.commit()
    return loginToGame(csocket)
    
def loginToGame(csocket):
    csocket.send(pickle.dumps('Logging in: '))
    user = pickle.loads(csocket.recv(MSGSIZE))
    while True:
        cur.execute("SELECT * FROM player WHERE username= '"+user+"'")
        account = cur.fetchone()
        if not account:
            csocket.send(pickle.dumps(0))
            csocket.send(pickle.dumps('User not found\n'))
            user = pickle.loads(csocket.recv(MSGSIZE))
            continue
        else:
            csocket.send(pickle.dumps(1))
            if not account[2]>0:
                csocket.send(pickle.dumps(2))
                roomname = pickle.loads(csocket.recv(MSGSIZE))
                numPlayers = pickle.loads(csocket.recv(MSGSIZE))
                while True:
                    try:
                        cur.execute("INSERT INTO room (rName, numPlayers) VALUES ('"
                                    +roomname+"', '"+numPlayers+"')")
                        db.commit()
                        cur.execute("SELECT rID FROM room WHERE rName='"
                                    +roomname+"'")
                        rID = cur.fetchone()[0]
                        cur.execute("UPDATE player SET rID = '"
                                    +str(rID)+"' WHERE pID = '"
                                    +str(account[0])+"'")
                        db.commit()
                        cur.execute(
                            "SELECT COUNT(*) FROM player WHERE rID= "+
                            "(SELECT rID FROM player WHERE pID = '"
                            +str(account[0])+"')")
                        counter = cur.fetchone()
                        cur.execute("UPDATE player SET counter ='"
                                    +str(counter[0])+"' WHERE pID = '"
                                    +str(account[0])+"'")
                        db.commit()
                        csocket.send(pickle.dumps(4))
                        print(pickle.loads(csocket.recv(MSGSIZE)))
                        break
                    except:
                        csocket.send(pickle.dumps(5))
                        csocket.send(pickle.dumps(
                            'Error! enter correct details'))
                        roomname = pickle.loads(csocket.recv(MSGSIZE))
                        numPlayers = pickle.loads(csocket.recv(MSGSIZE))
            else:
                csocket.send(pickle.dumps(3))
            break
    cur.execute("SELECT * FROM player WHERE username= '"+user+"'")
    account = cur.fetchone()
    return account

def getRoom(rID):
    cur.execute("SELECT * FROM room WHERE rID = '"+str(rID)+"'")
    return cur.fetchone()