import socket
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cv2
import numpy as np
t_image = np.ndarray(0)
t_x=0
t_y=0
buffer=''
path=''
recvs=''
image=''

app = QApplication(sys.argv)
win = QWidget() #win - main  windows
win2 = QWidget()  # win2 - message sender
img = QLineEdit(win2)
msg = QLineEdit(win2)
button = QPushButton(win2)
# msgPreview = QPushButton(win2)
#win3 = QWidget() #review of message: list form header[textbox + list], image [qpixelmap], message [textbox]
#add = QLabel(win3)
#send = QPushButton(win3)
#imma = QPixmap(win3)

#####################################################################################
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 2056)  ## can't be lower that 1024 for unprivilaged users (AG)
#function for connectring to serwer
# IT WORKS
print("Connecting to server...")
while 1:
    try:
        sock.connect(server_address)
        ##### wysyłanie nAZWY - TO DO
        break
    except Exception:
        continue
print("Connection established")
###################################################################################

#handling preview and another sending option
# def review():
#     if img.text() != '': t_image = cv2.imread('client/' + img.text() + '.jpg');  t_x = image.shape[0]; t_y = image.shape[1]
#     win3.show()

#foo to handle recieved msg
def rcv():
    pass

def imgToString(img):
    img = [[[str(z) for z in y] for y in x] for x in img]
    img = [[",".join(y) for y in x] for x in img]
    img = [ "+".join(x) for x in img]
    return  "_".join(img)

def msg_creator(): win2.show()

def sendMsg():
    print('test')
    if img.text() != '': print(img.text()); image = cv2.imread('client/'+img.text()+'.jpg');  x = str(image.shape[0]); y = str(image.shape[1])
    else:   print('wchodze'); x = ''; y = ''
    #show(recvs,image,msg)
    print('test2')
    buffer = (imgToString(image)+'|||'+msg.text()+'|||'+x+'|||'+y).encode()
    #sock.connect(server_address)
    print('sending')
    try:
        #sock.sendall(header)
        sock.sendall(buffer)
    finally:
        print ('closing socket')
    sock.close()

def initialize_msg_creator():
    win2.resize(300, 300)
    msg.move(50, 50)
    button.setText('Send message')
    button.move(50, 100)
    img.move(50, 75)
    msg.show()
    button.show()
    img.show()
    # msgPreview.move(50,125)
    # msgPreview.show()
    # msgPreview.clicked.connect(review)
    button.clicked.connect(sendMsg)

#main
win.resize(200, 200)
win.move(300, 300)
win.setWindowTitle('client')
win.show()
button_message = QPushButton(win)
button_message.setText('messages creator')
button_message.move(50,100)
button_message.clicked.connect(msg_creator)
button_message.show()
print ('connecting')
initialize_msg_creator()


sys.exit(app.exec_())

