import socket
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QListWidget, QTextEdit
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import _thread
buf_size=1024

class mainData(object):
    _instance = None
    def __new__(class_):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_)
        return class_._instance
    def setSocket(self,sock):
        self.socket=sock
    def setUsers(self,users):
        self.users=users
    def clear(self):
        self.users=[]
        self.socket=None
    def getSocket(self):
        return self.socket
    def getUsers(self):
        return self.users


data = mainData()



class WindowWithKeys(QWidget):
    keyPressed = pyqtSignal(int)
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            data = mainData()
            sock = data.getSocket()
            if sock != None:
                sock.close()
            print("Escape key pressed. Goodbye!")
            sys.exit(app.exec_())
        self.keyPressed.emit(Qt.Key(event.key()))

def receiveMessage(message):
    temp_message = message.split(' ')
    m_id = temp_message[0]
    print(m_id[0])
    if m_id[0] == "1":
        nUsers=int(m_id[1])
        data = mainData()
        print(nUsers)
        #arange list of users+ids
        users = list(zip(*[iter(temp_message[1:])]*2))
        # print(users)
        uss = []
        usersList.clear()
        for (desc,username) in users:
            print("ID: {} Username: {}".format(desc,username))
            usersList.addItem(username)
            uss.append(desc)

        data.setUsers(uss)
        usersList.show()




def connectionThread(socket):
    msg_received = ''
    print("new thread")
    while True:
        msg_received = socket.recv(buf_size)
        # print(msg_received)

        msg_received=msg_received.split('/x00')[0].decode()
        receiveMessage(msg_received)
    print("OLA")





#init everyting
app = QApplication(sys.argv)
helloWin = WindowWithKeys() #login window
helloWin.setWindowTitle('First window')
helloWin.resize(300,100)
mainWin = WindowWithKeys() #main window for user
mainWin.setWindowTitle('Main board')
mainWin.resize(300,300)
infoWin = WindowWithKeys()
infoWin.setWindowTitle('Warning!')
infoWin.resize(200,100)
warn = QLabel(infoWin)
warn.setText('You need nick name, to login')
exitWarn = QPushButton(infoWin)
exitWarn.move(0,warn.height())
exitWarn.setText('Go back!')
usersList = QListWidget(mainWin)
usersList.resize(usersList.width(),100)
msg = QTextEdit(mainWin)
msgButton = QPushButton(mainWin)
msg.move(0,usersList.width())
msg.resize(200,100)
msgButton.move(0,200)
msg.show()
msgButton.show()

login=QLineEdit(helloWin) #line edit for user's nickname
login.move(helloWin.width()/2-login.width()/2,0)
loginButton = QPushButton(helloWin) #after pushing that button, user will connect to server
loginButton.setText('Login')
loginButton.move(helloWin.width()/2-loginButton.width()/2,login.height())


server_address = ("localhost", 2057)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
data.setSocket(sock)

def sendMsg():
    sock = data.getSocket()
    uss = data.getUsers()
    message = msg.toPlainText()
    n = len(uss)
    msg_type = "1"
    mg = msg_type + str(n) + " "
    for x in uss:
        mg += x + " "
    mg+=message
    print(mg)
    try:
        print(sock)
        print(uss)
        sock.sendall(mg.encode())
    finally:
        print("msg sent")


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
    data.setSocket(sock)
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
msgButton.clicked.connect(sendMsg)
loginButton.show()
helloWin.show()

data.getSocket().close()
sys.exit(app.exec_())