import pickle
from time import sleep


def send(csocket, data):
    csocket.send(pickle.dumps(data))

def receive(csocket):
    return pickle.loads(csocket.recv(2048))

def cLogin(csocket):
    ack = [-1]
    while ack[0] ==-1:
        print('Logging in: ')
        username = str(input('Enter your username: '))
        print('Press 0 to create a room: ')
        print('Press 1 to join a room: ')
        create_join = int(input('Your Choice: '))
        while not (create_join==1 or create_join==0):
            create_join = int(input('Error! Press 1 or 0: '))
            sleep(1)
        roomname = str(input('Enter Room name: '))
        if create_join==0:
            numplayers = -1
            while numplayers < 1:
                try:
                    numplayers = int(input('Enter Number of players: '))
                except:
                    numplayers = input('Error! Enter a correct number: ')
                sleep(1)
        else:
            numplayers = -1 # dummy number
        send(csocket, [username, roomname, numplayers])
        ack = receive(csocket)
        if ack[0]==-1:
            print("Error! Enter Correct data\n\n")
    
def cSignup(csocket):
    ack = [-1]
    while ack[0]==-1:
        username = str(input('Enter a username: '))
        send(csocket,username)
        ack = receive(csocket)
        if ack[0]==-1:
            print("Error! Enter another username ")
    cLogin(csocket)