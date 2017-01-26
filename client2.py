import socket
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QListWidget, QTextEdit, QListView
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import argparse as prsr
import _thread
import os
buf_size=1024
port=2061
server='localhost'
import time
app = QApplication(sys.argv)



class mainData(object):
    _instance = None

    def __new__(class_):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_)
        return class_._instance
    def setSocket(self,sock):
        self.a=[]
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
    def setName(self,name):
        self.name=name
    def setID(self,id):
        self.id=id
    def getName(self):
        return self.name
    def getID(self):
        return self.id
    def setUNames(self,unames):
        self.userNames=unames
    def getUNames(self):
        return self.userNames
    def addtocollection(self,x):
        self.a.append(x)
    def setModel(self,model):
        self.model=model
    def getModel(self):
        return self.model
data = mainData()

class textMsg(QWidget):
    def __init__(self,author,receivers,message):
        super(textMsg, self).__init__()
        self.author=author
        self.receivers=receivers
        self.message=message
        self.start()
    def start(self):
        self.aut = QLineEdit(self)
        self.rec = QLineEdit(self)
        self.msg = QTextEdit(self)
        self.resize(300,400)
        self.aut.move(0,0)
        self.aut.resize(300,self.aut.height())
        self.rec.move(0,self.aut.height())
        self.rec.resize(300,self.rec.height())
        self.msg.resize(300,400 - self.rec.height() * 2)
        self.msg.move(0,self.rec.height()*2)
        self.aut.setText("Sender: "+self.author)
        self.rec.setText("Receivers: "+self.receivers)
        self.msg.setText(self.message)
        self.aut.setReadOnly(True)
        self.rec.setReadOnly(True)
        self.msg.setReadOnly(True)
        mainData().addtocollection(self)
        self.aut.show()
        self.rec.show()
        self.msg.show()




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
        if event.key() == Qt.Key_Enter:
            logIn()
        self.keyPressed.emit(Qt.Key(event.key()))


def receiveMessage(message):
    data = mainData()
    if message == '':
        print('no connection this time')
        data.getSocket().close()
    temp_message = message.split(' ')
    m_id = temp_message[0]
    print(m_id[0])
    if m_id[0] == "1":
        nUsers=int(m_id[1])
        users = list(zip(*[iter(temp_message[1:])]*2))
        uss = []
        usersList.clear()
        for (desc,username) in users:
            if username == data.getName():
                data.setID(desc)
            else:
                usersList.addItem(username)
                uss.append(desc)
            print("ID: {} Username: {}".format(desc,username))

        data.setUsers(uss)
        usersList.show()
    if m_id[0] == "2":
        nUsers=int(m_id[1])
        sender = temp_message[1]
        recvrs = temp_message[2:2+nUsers]
        temp = ""
        for usr in recvrs:
            temp+=usr+" "
        msg = temp_message[2+nUsers:]
        tmp_m = ""
        for m in msg:
            tmp_m+=m+" "
        #show message
        msg = textMsg(sender,temp,tmp_m)
        msg.show()






def connectionThread(socket):
    print("new thread")
    while True:
        msg_received = socket.recv(buf_size)
        msg_received=msg_received[:msg_received.find(b'\x00')].decode()
        receiveMessage(msg_received)
    print("OLA")





#init everyting

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
msgButton.setText('Messages creator')
msg.show()
msgButton.show()

login=QLineEdit(helloWin) #line edit for user's nickname
login.move(helloWin.width()/2-login.width()/2,0)
loginButton = QPushButton(helloWin) #after pushing that button, user will connect to server
loginButton.setText('Login')
loginButton.move(helloWin.width()/2-loginButton.width()/2,login.height())


server_address = (server,port)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
data.setSocket(sock)

def sendMsg():
    sock = data.getSocket()
    uss = data.getUsers()
    message = msg.toPlainText()
    n = len(uss)
    msg_type = "1"
    mg = msg_type + str(n) + " "
    mg+=data.getID()+" "
    for x in uss:
        mg+=x+" "
    mg += str(sys.getsizeof(message.encode()))+" "
    print(mg)
    sock.sendall(mg.encode())
    try:
        sock.sendall(message.encode())
    finally:
        print("msg sent")


def checkConnection(sock):
    d=mainData()
    sock=d.getSocket()
    while 1:
        time.sleep(5)
        temp = sock.recv(0).decode()
        if temp == None:
            print("Disconnected from server")
            d.getSocket().close()
            os._exit(0)
            _thread.exit()


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
    server_address = (server,port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data.setSocket(sock)
    data.setName(login.text())
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
    _thread.start_new_thread(checkConnection, (sock,))
    print("Connection established")

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