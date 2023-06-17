import pickle


def send(csocket, data):
    csocket.send(pickle.dumps(data))

def receive(csocket):
    return pickle.loads(csocket.recv(2048))

def cLogin(csocket):
    print(receive(csocket))
    user = str(input('Enter your username: '))
    send(csocket,user)
    ack = receive(csocket)
    while True:
        if ack==0:
            print(receive(csocket))
            user = str(input(
                'Please enter a correct username: '))
            send(csocket,user)
            continue
        else:
            ack = receive(csocket)
            if ack==2:
                print(receive(csocket))
                print(receive(csocket))
                createorjoin = int(input('Your Choice: '))
                send(csocket, createorjoin)
                while createorjoin != 1 and createorjoin !=2:
                    createorjoin = int(
                        input('Enter a correct choice: '))
                if createorjoin==1:
                    cCreateRoom(csocket)
                else:
                    roomname = input("Enter room name: ")
                    send(csocket, roomname)
                    ack = receive(csocket)
                    while ack==1:
                        roomname = input("Enter a correct"+
                                         "/avaliable room name: ")
                        send(csocket, roomname)
                        ack = receive(csocket)
                    send(csocket, 'ok')
            break
    
    
    
def cSignup(csocket):
    print(receive(csocket))
    username = str(input('Enter a username: '))
    send(csocket,username)
    while True:
        ack = receive(csocket)
        if ack==1:
            print(receive(csocket))
            send(csocket,'Ok')
            break
        else:
            username = str(input(
                'Please Re-enter a correct username: '))
            send(csocket,username)
            continue
    cLogin(csocket)
    
def cCreateRoom(csocket):
    roomname = str(input(
        'Enter room name: '))
    send(csocket,roomname)
    numPlayers = str(int(
    input('Enter number of players: ')))
    send(csocket,numPlayers)
    while True:
        ack = receive(csocket)
        if ack == 5:
            print(receive(csocket))
            roomname = str(
                input('Enter room name: '))
            numPlayers = str(int(input(
                'Enter number of players: ')))
            send(csocket, roomname)
            send(csocket, numPlayers)
        else:
            send(csocket, 'ok')
            break