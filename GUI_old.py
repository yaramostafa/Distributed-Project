from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5 import uic

class MyGUI(QMainWindow):
    def __init__(self):
        super(MyGUI,self).__init__()
        uic.loadUi("chatgui.ui",self)
        self.show()
        self.Name.setFont(QFont('Arial', 14))
        self.msgBox.setFont(QFont('Arial', 13))
        self.pushButton.clicked.connect(lambda: self.send(self.msg.toPlainText()))
        self.Name.setText(input("Enter your Name: "))

    def send(self, msg):
        if len(msg) > 0:
            print("Sent!")
            Name = self.Name.text()
            #print(Name)
            #msgToSend = self.msgBox.toPlaintext+"\n"+Name+": "+msg
            msgToSend = Name+": "+msg
            print(msgToSend)

            self.msgBox.append(msgToSend)
            self.msg.setText('')
        else:
            print("Write a Msg!")
            message = QMessageBox()
            message.setText("Write a msg!")
            message.exec_()


def main():
    app = QApplication([])
    window =MyGUI()
    app.exec_()


if  __name__ == '__main__':
    main()