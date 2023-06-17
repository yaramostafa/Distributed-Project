import pickle
MSGSIZE = 2048



def cLogin(csocket):
    print(pickle.loads(csocket.recv(MSGSIZE)))
    user = str(input('Enter your username: '))
    csocket.send(pickle.dumps(user))
    ack = pickle.loads(csocket.recv(MSGSIZE))
    while True:
        if ack==0:
            print(pickle.loads(csocket.recv(MSGSIZE)))
            user = str(input(
                'Please enter a correct username: '))
            csocket.send(pickle.dumps(user))
            continue
        else:
            ack = pickle.loads(csocket.recv(MSGSIZE))
            if ack==2:
                roomname = str(input(
                    'Enter room name: '))
                csocket.send(pickle.dumps(roomname))
                numPlayers = str(int(
                    input('Enter number of players: ')))
                csocket.send(pickle.dumps(numPlayers))
                while True:
                    ack = pickle.loads(
                        csocket.recv(MSGSIZE))
                    if ack == 5:
                        print(pickle.loads(
                            csocket.recv(MSGSIZE)))
                        roomname = str(
                            input('Enter room name: '))
                        numPlayers = str(int(input(
                            'Enter number of players: ')))
                        csocket.send(
                            pickle.dumps(roomname))
                        csocket.send(
                            pickle.dumps(numPlayers))
                    else:
                        csocket.send(
                            pickle.dumps('ok'))
                        break
            break
    
    
    
def cSignup(csocket):
    print(pickle.loads(csocket.recv(MSGSIZE)))
    username = str(input('Enter a username: '))
    csocket.send(pickle.dumps(username))
    while True:
        ack = pickle.loads(csocket.recv(MSGSIZE))
        if ack==1:
            print(pickle.loads(csocket.recv(MSGSIZE)))
            csocket.send(pickle.dumps('Ok'))
            break
        else:
            username = str(input(
                'Please Re-enter a correct username: '))
            csocket.send(pickle.dumps(username))
            continue
    cLogin(csocket)