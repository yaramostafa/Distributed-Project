def send(csocket, data):
    csocket.send(str(data).encode())
    
def sendArr(csocket, arr):
    msg = str(
        arr).replace(
            '[', '').replace(
                ']', '').replace(
                    ' ', '')
    csocket.send(msg.encode())

def receiveInt(csocket, thread = None):
    try:
        return int(csocket.recv(2048).decode())
    except:
        if not thread:
            return [-1]
        csocket.close()
        thread.dc = True
        return [-1]

def receiveString(csocket, thread=None):
    try:
        return str(csocket.recv(2048).decode())
    except:
        if not thread:
            return [-1]
        csocket.close()
        thread.dc = True
        return [-1]

def receiveArr(csocket, thread=None):
    #first element is always int
    try:
        msg = receiveString(csocket)
        arr = msg.replace(
            '"', '').replace(
                '\'''', '').split(
                    ',')
        arr[0] = int(arr[0])
        return arr
    except:
        if not thread:
            return [-1]
        csocket.close()
        thread.dc = True
        return [-1]