import socket
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QListWidget, QTextEdit, QListView
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import _thread
import os

buf_size = 1024
# port = 2068
# server = 'localhost'
import time

app = QApplication(sys.argv)


class mainData(object):
    _instance = None

    def __new__(class_):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_)
        return class_._instance

    def setSocket(self, sock):
        self.a = []
        self.socket = sock

    def setUsers(self, users):
        self.users = users

    def clear(self):
        self.users = []
        self.socket = None

    def getSocket(self):
        return self.socket

    def getUsers(self):
        return self.users

    def setName(self, name):
        self.name = name

    def setID(self, id):
        self.id = id

    def getName(self):
        return self.name

    def getID(self):
        return self.id

    def setUNames(self, unames):
        self.userNames = unames

    def getUNames(self):
        return self.userNames

    def addtocollection(self, x):
        self.a.append(x)

    def setModel(self, model):
        self.model = model

    def getModel(self):
        return self.model

    def setPort(self,port):
        self.port=port

    def getPort(self):
        return int(self.port.text())
    def setIP(self,ip):
        self.ip=ip
    def getIP(self):
        return self.ip.text()


data = mainData()


class textMsg(QWidget):
    def __init__(self, author, receivers, message):
        super(textMsg, self).__init__()
        self.author = author
        self.receivers = receivers
        self.message = message
        print(self.message)
        self.start()

    def start(self):
        self.aut = QLineEdit(self)
        self.rec = QLineEdit(self)
        self.msg = QTextEdit(self)
        self.resize(300, 400)
        self.aut.move(0, 0)
        self.aut.resize(300, self.aut.height())
        self.rec.move(0, self.aut.height())
        self.rec.resize(300, self.rec.height())
        self.msg.resize(300, 400 - self.rec.height() * 2)
        self.msg.move(0, self.rec.height() * 2)
        self.aut.setText("Sender: " + self.author)
        self.rec.setText("Receivers: " + self.receivers)
        self.msg.setText(self.message)
        self.aut.setReadOnly(True)
        self.rec.setReadOnly(True)
        self.msg.setReadOnly(True)
        mainData().addtocollection(self)
        self.aut.show()
        self.rec.show()
        self.msg.show()

class msgSender(QWidget):
    def __init__(self):
        super(msgSender, self).__init__()
        self.start()
    def start(self):
        data = mainData()
        self.users=[[],[]]
        self.resize(300, 300)
        self.users[0] = data.getUsers()
        self.users[1] = data.getUNames()
        self.list = QListView(self)
        self.list.resize(300,100)
        self.text = QTextEdit(self)
        self.button = QPushButton(self)
        self.button.setText("Send Message!")
        self.model = QStandardItemModel()
        for i in range(len(self.users[0])):
            item = QStandardItem(self.users[1][i])
            item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            item.setData(QVariant(Qt.Unchecked), Qt.CheckStateRole)
            self.model.appendRow(item)
        self.list.setModel(self.model)
        self.text.resize(300, 100)
        self.text.move(0, 200 - self.button.height())
        self.button.move(0, 300 - self.button.height())
        self.text.show()
        self.button.show()
        self.list.show()
        data.addtocollection(self)
        self.button.clicked.connect(self.sendmessage)
        self.setWindowTitle(data.getName()+"received message")
        self.show()

    def sendmessage(self):
        self.rcvs = []
        for i in range(self.model.rowCount()):
            temp = self.model.item(i).checkState()
            if temp > 0:
                for j in range(len(self.users[1])):
                    if self.model.data(self.model.index(i, 0)) == self.users[1][j]:
                        self.rcvs.append(self.users[0][j])

        if self.rcvs == []:
            print("lista odbiorców pusta")
            return
        data = mainData()
        id = data.getID()
        self.message2send=""
        msg_type = "1"
        message = ''
        message = self.text.toPlainText()
        if message == '':
            print("pusta wiadomość")
            return
        self.message2send = msg_type+str(len(self.rcvs)) +" "+ id + " "
        for ide in self.rcvs:
            self.message2send+=ide + " "
        sock = data.getSocket()
        self.message2send+=str(sys.getsizeof(message))+" "
        sock.sendall(self.message2send.encode())
        try:
            sock.sendall(message.encode())
        finally:
            print("Message sent successfully!!!")


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
    print('recieved: '+message)
    data = mainData()
    if message == '':
        print('no connection this time')
        data.getSocket().close()
    temp_message = message.split(' ')
    print('msg: ')
    m_id = temp_message[0]
    if m_id[0] == "1":
        nUsers = int(m_id[1])
        users = list(zip(*[iter(temp_message[1:])] * 2))
        uss = []
        uss_n = []
        usersList.clear()
        for (desc, username) in users:
            if username == data.getName():
                data.setID(desc)
            else:
                uss.append(desc)
                uss_n.append(username)
                usersList.addItem(username)
            print("ID: {} Username: {}".format(desc, username))
        data.setUNames(uss_n)
        data.setUsers(uss)
        usersList.show()
    if m_id[0] == "2":
        nUsers = int(m_id[1])
        sender = temp_message[1]
        recvrs = temp_message[2:3 + nUsers]
        temp = ""
        for usr in recvrs:
            temp += usr + " "
        msg = temp_message[3 + nUsers:]
        tmp_m = ""
        mg=decodeusers(temp)
        if sender == data.getID():
            return
        for m in msg:
            tmp_m += m + " "
        # show message
        msg = textMsg(sender, mg, tmp_m)
        print(sender)
        print(mg)
        msg.show()

def decodeusers(id_string):
    data=mainData()
    temp=[[],[]]
    temp[0]=data.getUsers()
    temp[1]=data.getUNames()
    z=id_string.split(' ')
    lista=[]
    for i in range(len(temp[1])):
        for id in z:
            if id == temp[0][i]:
                lista.append(temp[1][i])
    msg=""
    for name in lista:
        msg+=name+" "
    return msg

def decodesender(id):
    data=mainData()
    temp=[[],[]]
    temp[0] = data.getUsers()
    temp[1] = data.getUNames()
    for i in range(len(temp[1])):
        if id == temp[0][i]:
            print("S: "+temp[1][i])
            return temp[1][i]

def connectionThread(socket):
    print("new thread")
    while True:
        msg_received = socket.recv(buf_size)
        msg_received = msg_received[:msg_received.find(b'\x00')].decode()
        if int(msg_received.split(' ')[0][0])>1:
            msg2 = socket.recv(buf_size)
            msg2=msg2[:msg2.find(b'\x00')].decode()
            receiveMessage(msg_received+" "+msg2)
        else:
            receiveMessage(msg_received)
    print("OLA")


# init everyting

helloWin = WindowWithKeys()  # login window
helloWin.setWindowTitle('First window')
helloWin.resize(300, 100)
mainWin = WindowWithKeys()  # main window for user
mainWin.setWindowTitle('Main board')
mainWin.resize(300, 300)
infoWin = WindowWithKeys()
infoWin.setWindowTitle('Warning!')
infoWin.resize(200, 100)
warn = QLabel(infoWin)
warn.setText('You need nick name, to login')
exitWarn = QPushButton(infoWin)
exitWarn.move(0, warn.height())
exitWarn.setText('Go back!')
usersList = QListWidget(mainWin)
usersList.resize(usersList.width(), 100)
msgButton = QPushButton(mainWin)
msgButton.move(0, 150)
msgButton.setText('Messages creator')
msgButton.show()
serv = QLineEdit(helloWin)
port2 = QLineEdit(helloWin)
serv.move(0,0)
port2.move(helloWin.width()-port2.width(),0)
serv.show()
port2.show()
login = QLineEdit(helloWin)  # line edit for user's nickname
login.move(+helloWin.width() / 2 - login.width() / 2, serv.height())
loginButton = QPushButton(helloWin)  # after pushing that button, user will connect to server
loginButton.setText('Login')
loginButton.move(helloWin.width() / 2 - loginButton.width() / 2, login.height()*2)



server_address = ("",0)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
data.setSocket(sock)


def sendMsg():
    print("KLIX1")
    sender = msgSender()
    print("KLIX2")


def checkConnection(sock):
    d = mainData()
    sock = d.getSocket()
    while 1:
        time.sleep(5)
        temp = sock.recv(1).decode()
        if temp == None:
            print("Disconnected from server")
            d.getSocket().close()
            os._exit(0)
            _thread.exit()


def closeWarn():
    infoWin.hide()
    warn.hide()
    exitWarn.hide()


def logIn():  # function for connection
    # check for nickname
    data.setIP(serv)
    data.setPort(port2)
    print(data.getIP())
    print(data.getPort())
    server_address = (data.getIP(), data.getPort())
    print(server_address)
    if login.text() == '':
        infoWin.show()
        warn.show()
        exitWarn.show()
        # show 'u need name'
        return
    # if nickname was entered, establish connection

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data.setSocket(sock)
    data.setName(login.text())
    mainWin.setWindowTitle('Main board '+data.getName())
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
    #_thread.start_new_thread(checkConnection, (sock,))
    print("Connection established")

    mainWin.show()
    helloWin.hide()


# main part
loginButton.clicked.connect(logIn)
exitWarn.clicked.connect(closeWarn)
msgButton.clicked.connect(sendMsg)
loginButton.show()
helloWin.show()

data.getSocket().close()
sys.exit(app.exec_())
