import MySQLdb

db = MySQLdb.connect(host='localhost',  # your host, usually localhost
                     user='root',       # your username
                     passwd='',         # your password
                     db='race-chat')

cur = db.cursor()

def signup():
    username = str(input('Enter a username: '))
    while True:
        try:
            cur.execute("INSERT INTO player (username, xCoord, yCoord) VALUES ('"+username+"', 0, 0)")
            print('Signed up')
            break
        except:
            username = str(input('Please Re-enter a correct username: '))
            continue
    db.commit()
    return loginToGame()
    
def loginToGame():
    user = str(input('Enter your username: '))
    while True:
        cur.execute("SELECT * FROM player WHERE username= '"+user+"'")
        account = cur.fetchone()
        if not account:
            print('User not found\n')
            user = str(input('Please enter a correct username: '))
            continue
        else:
            if not account[2]>0:
                roomname = str(input('Enter room name: '))
                numPlayers = str(int(input('Enter number of players: ')))
                while True:
                    try:
                        cur.execute("INSERT INTO room (rName, numPlayers) VALUES ('"
                                    +roomname+"', '"+numPlayers+"')")
                        db.commit()
                        cur.execute("SELECT rID FROM room WHERE rName='"+roomname+"'")
                        rID = cur.fetchone()[0]
                        cur.execute('UPDATE player SET rID = '
                                    +rID+' WHERE pID = '+account[0])
                        db.commit()
                        break
                    except:
                        print('Error! enter correct details')
                        roomname = str(input('Enter room name: '))
                        numPlayers = str(int(input('Enter number of players: ')))
            break
    cur.execute("SELECT * FROM player WHERE username= '"+user+"'")
    account = cur.fetchone()
    return account
