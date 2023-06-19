import MySQLdb
import pickle

def send(csocket, data):
    csocket.send(pickle.dumps(data))

def receive(csocket, thread):
    try:
        return pickle.loads(csocket.recv(2048))
    except:
        csocket.close()
        thread.dc = True
        return [-1]

def set(exp: str):
    try:
        cur.execute(exp)
        db.commit()
        return 1
    except:
        return -1

def get(exp: str):
    try:
        cur.execute(exp)
        x = cur.fetchone()
        if not x: return [-1]
        return list(x)
    except:
        return [-1]
    
def getall(exp: str):
    try:
        cur.execute(exp)
        x = cur.fetchall()
        if not x: return [-1]
        return list(x)
    except:
        return [-1]
db = MySQLdb.connect(host='localhost',  # your host, usually localhost
                     user='root',       # your username
                     passwd='',         # your password
                     db='race-chat')

cur = db.cursor()

def signup(csocket, thread):
    ack = [-1]
    while ack[0]==-1:
        username = receive(csocket, thread)
        if thread.dc:
            return [-1]
        ack = set("INSERT INTO player"+
                     " (username, xCoord, yCoord) VALUES"
                     +" ('"+username+"', 0, 0)")
        ack = [ack]
        send(csocket, ack)
    return sLogin(csocket, thread)
    
def loginToGame(csocket, thread):
    #returns    account in case of success
    #           [-1]    in case of failure
    try:
        username, roomname, numplayers = receive(csocket, thread)
    except:
        thread.dc = True
    if thread.dc:
        return [-1]
    account = get("SELECT * FROM player WHERE username= '"+username+"'")
    if account[0]==-1: return [-1]
    elif account[2]>0:
        _ = set("UPDATE player SET dc = '0' WHERE pID = '"+str(account[0])+"'")
        account[7] = 0
        return account
    
    if numplayers == -1:
        room = get("SELECT * FROM room WHERE rName = '"+roomname+"'")
        if room[0]==-1: return [-1]
        
        currplayers = get("SELECT COUNT(*) FROM player WHERE rID = '"
                          +str(room[0])+"'")
        if not currplayers[0]<room[2]: return [-1]
        
        
        status = set("UPDATE player SET rID = '"
                     +str(room[0])+"', dc = '0', xCoord = '"
                     +str(1300 * (0.1+0.2*(currplayers[0])))+"', "
                     +"yCoord = '480', filepath = '.\\\img\\\car"
                     +str(currplayers[0]+1)+".png', counter ='"
                     +str(currplayers[0]+1)+"' WHERE pID = '"
                     +str(account[0])+"'")
        if status==-1: return [-1]
        
    else:
        status = set("INSERT INTO room (rName, numPlayers) VALUES ('"+roomname+"', '"+str(numplayers)+"')")
        if status==-1: return [-1]
        rID = get("SELECT rID FROM room WHERE rName='"+roomname+"'")
        if rID[0]==-1: return [-1]
        status = set("UPDATE player SET rID = '"
                     +str(rID[0])+"', dc = '0',"
                     +" xCoord = '130', yCoord = '480',"
                     +" filepath = '.\\\img\\\car1.png',"
                     +" counter ='1' WHERE pID = '"
                     +str(account[0])+"'")
        if status==-1: return [-1]
        
    account = get("SELECT * FROM player WHERE pID = '"
                  +str(account[0])+"'")
    return account

def sLogin(csocket, thread):
    ack = [-1]
    while ack[0]==-1:
        ack = list(loginToGame(csocket, thread))
        if thread.dc:
            return
        send(csocket, ack)
    return ack

def getRoom(rID):
    cur.execute("SELECT * FROM room WHERE rID = '"+str(rID)+"'")
    return cur.fetchone()
            
    
def getOpponents(pID):
    cur.execute("SELECT * FROM player WHERE"+
                " rID = (SELECT rID FROM player WHERE pID = '"
                +str(pID)+"') AND NOT pID = '"+str(pID)+"'")
    x = []
    for i in cur.fetchall():
        i = list(i)
        x+=[i]
    return x

def updatePlayer(player, dc):
    _ = set("UPDATE player SET xCoord = '"+str(player[4])+"',"+
                " yCoord = '"+str(player[5])+"', score = '"+str(player[6])+"',"+
                " dc = '"+str(dc)+"' WHERE pID = '"+str(player[0])+"'")
    
def deleteRoom(rID):
    _ = set("DELETE FROM player WHERE rID = '"+str(rID)+"'")
    _ = set("DELETE FROM room WHERE rID = '"+str(rID)+"'")
    
