import pickle
from time import sleep


def send(csocket, data):
    csocket.send(pickle.dumps(data))

def receive(csocket):
    return pickle.loads(csocket.recv(2048))

def cLogin(csocket):
    
    print('Logging in: ')
    username = str(input('Enter your username: '))
    print('Press 0 to create a room')
    print('Press 1 to join a room')
    create_join = int(input('Your Choice: '))
    while not (create_join==1 or create_join==0):
        create_join = int(input('Error! Press 1 or 0: '))
        sleep(1)
    roomname = str(input('Enter Room name:'))
    if create_join==0:
        numplayers = -1
        while numplayers < 1:
            try:
                numplayers = int(input('Enter Number of player: '))
            except:
                numplayers = input('Error! Enter a correct number:')
            sleep(1)
    else:
        numplayers = -1 # dummy number
    send(csocket, [username, roomname, numplayers])
    ack = receive(csocket)
    if ack == -1:
        sleep(1)
        cLogin(csocket)
    
    
    
    
def cSignup(csocket):
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