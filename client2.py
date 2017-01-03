import socket
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class WindowWithKeys(QWidget):
    keyPressed = pyqtSignal(int)
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            if sock != None:
                sock.close()
            print("Escape key pressed. Goodbye!")
            sys.exit(app.exec_())
        self.keyPressed.emit(Qt.Key(event.key()))

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

login=QLineEdit(helloWin) #line edit for user's nickname
login.move(helloWin.width()/2-login.width()/2,0)
loginButton = QPushButton(helloWin) #after pushing that button, user will connect to server
loginButton.setText('Login')
loginButton.move(helloWin.width()/2-loginButton.width()/2,login.height())

#connection vars
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 2056)

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
    print("Connecting to server...")
    while 1:
        try:
            sock.connect(server_address)
            buf = "1 "+login.text()
            try:
                sock.sendall(buf.encode())
            finally:
                print("Nickname sent")
            break
        except Exception:
            continue
    print("Connection established")
    mainWin.show()
    helloWin.hide()


#main part
loginButton.clicked.connect(logIn)
exitWarn.clicked.connect(closeWarn)
loginButton.show()
helloWin.show()

sock.close()
sys.exit(app.exec_())