import socket
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QListWidget
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import _thread

buf_size=1024

class WindowWithKeys(QWidget):
    keyPressed = pyqtSignal(int)
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            if sock != None:
                sock.close()
            print("Escape key pressed. Goodbye!")
            sys.exit(app.exec_())
        self.keyPressed.emit(Qt.Key(event.key()))

def receiveMessage(message):
    # message=message.decode()
    temp_message = message.split(' ')
    m_id = temp_message[0]
    if m_id[0] == 1:
        nUsers=m_id[1]
        #arange list of users+ids
        users = zip(*[iter(temp_message[2:])]*2)
        for (desc,username) in users:
            print("ID: {} Username: {}".format(desc,username))
            # usersList.addItem(username)
        #usersList.show()


def connectionThread(socket):
    msg_received = ''
    print("new thread")
    msg_received = socket.recv(buf_size).decode()
    print(msg_received)
    receiveMessage(msg_received)
    print("OLA")


#init everyting
app = QApplication(sys.argv)
helloWin = WindowWithKeys() #login window
helloWin.setWindowTitle('First window')
helloWin.resize(300,100)
mainWin = WindowWithKeys() #main window for user
mainWin.setWindowTitle('Main board')
infoWin = WindowWithKeys()
infoWin.setWindowTitle('Warning!')
infoWin.resize(200,100)
warn = QLabel(infoWin)
warn.setText('You need nick name, to login')
exitWarn = QPushButton(infoWin)
exitWarn.move(0,warn.height())
exitWarn.setText('Go back!')
usersList = QListWidget(mainWin)

login=QLineEdit(helloWin) #line edit for user's nickname
login.move(helloWin.width()/2-login.width()/2,0)
loginButton = QPushButton(helloWin) #after pushing that button, user will connect to server
loginButton.setText('Login')
loginButton.move(helloWin.width()/2-loginButton.width()/2,login.height())


server_address = ("localhost", 2057)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def closeWarn():
    infoWin.hide()
    warn.hide()
    exitWarn.hide()

def logIn(): #function for connection
    #check for nickname
    if login.text() == '':
        infoWin.show()
        warn.show()
        exitWarn.show()
        #show 'u need name'
        return
    #if nickname was entered, establish connection
    server_address = ("localhost", 2057)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(sock)
    print("Connecting to server...")
    while 1:
        try:
            sock.connect(server_address)
            break
        except Exception:
            continue
    print("Connected")
    buf = "1 " + login.text()
    _thread.start_new_thread(connectionThread, (sock,))
    try:
        sock.sendall(buf.encode())
    finally:
        print("Nickname sent")

    print("Connection established"),

    mainWin.show()
    helloWin.hide()


#main part
loginButton.clicked.connect(logIn)
exitWarn.clicked.connect(closeWarn)
loginButton.show()
helloWin.show()

sock.close()
sys.exit(app.exec_())