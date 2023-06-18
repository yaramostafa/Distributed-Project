from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5 import uic
import socket, threading


class ClientSocket(threading.Thread):
    def __init__(self,type):
        threading.Thread.__init__(self)
        host = 'localhost'
        port = 10001
        self.size = 2048

        self.csocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.csocket.connect((host, port))
        self.type = type
        if self.type == 'recv':
            data = self.csocket.recv(self.size)
            if len(data):
                print('Received:', data.decode('utf-8'))
    def run(self):
        if self.type == 'recv':
            data = self.csocket.recv(2048)
            self.item.append(str(data.decode()))
            while len(data):
                data = self.csocket.recv(2048)
                print("Data: ", data.decode())

                if self.name+" disconnected from chat" == data.decode():
                    self.item.append(str(data.decode()))
                    data = ''
                    print(self.name+" disconnected from chat")
                    print("QUIT")
                else:
                    self.item.append(str(data.decode()))
            data = self.csocket.recv(2048)
            self.item.append(str(data.decode()))
            self.csocket.close()


    def sendToServer(self,text):
        self.csocket.send(text.encode())

class MyGUI(QMainWindow):
    def __init__(self, cName):
        self.ClientSocketRec = ClientSocket('recv')
        self.ClientSocketSend = ClientSocket('send')
        self.ClientSocketSend.start()
        super(MyGUI,self).__init__()
        uic.loadUi("chatgui.ui",self)
        self.show()
        self.Name.setFont(QFont('Arial', 14))
        self.msgBox.setFont(QFont('Arial', 13))
        self.pushButton.clicked.connect(lambda: self.send(self.msg.toPlainText()))
        name = cName
        self.pushButton.setEnabled(True)
        self.msg.setEnabled(True)
        self.name = name
        self.ClientSocketRec.item = self.msgBox
        self.ClientSocketRec.name = self.name
        self.ClientSocketRec.start()
        self.ClientSocketSend.sendToServer(name)
        self.Name.setText(name)


    def closeEvent(self, *args, **kwargs):
        super(QMainWindow, self).closeEvent(*args, **kwargs)
        self.ClientSocketSend.sendToServer(self.name+": quit")
        self.ClientSocketSend.csocket.close()
        print("Just closed the window!")

    def send(self, msg):
        if len(msg) > 0:
            print("Sent!")
            Name = self.Name.text()
            msgToSend = Name+": "+msg
            print(msgToSend)
            self.ClientSocketSend.sendToServer(msgToSend)
            # if msgToSend.split(":")[1].replace(" ","") == "quit":
            #     self.ClientSocketSend.csocket.close()
            self.msg.setText('')
        else:
            print("Write a Msg!")
            message = QMessageBox()
            message.setText("Write a msg!")
            message.exec_()


def initChat(clientName):
    app = QApplication([])
    cName = clientName
    _ = MyGUI(cName)
    app.exec_()