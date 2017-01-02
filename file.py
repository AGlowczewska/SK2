import sys
import socket as s
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage

app = QApplication(sys.argv)
window = QWidget()

def BGR2RGB(image):
    h,w,c=image.shape
    for x in range(h):
        for y in range(w):
            image[x][y][2],image[x][y][0]=image[x][y][0],image[x][y][2]
    return image

class Emitter(QObject):
    emitting = pyqtSignal()

class ImageDisplayer(QObject):
    def __init__(self):
        self.sig=Emitter()
        QObject.__init__(self)
        self.sig.emitting.connect(self.showImg)
        print('succeded')
    def letsdothis(self):
        print('letsdothis')
        self.sig.emitting.emit()
    @pyqtSlot()
    def showImg(self):
        print('showimg')
        window.show()

def stringToImg(string):
    string = string.split("_")
    string = [x.split("+") for x in string]
    string = [[y.split(",") for y in x] for x in string]
    return [[[np.float32(z) for z in y] for y in x] for x in string]

def loadMessage(buffer):
    print('1 post')
    img, message, h, w = buffer.split(b'|||')
    h = int(h.decode())
    w = int(w.decode())
    img = stringToImg(img.decode())
    temp_image = np.zeros(shape=(h, w, 3), dtype=np.uint8)
    for row in range(h):
        for value in range(w):
            for channel in range(3):
                temp_image[row][value][channel] = img[row][value][channel]
    print('2 post')
    img = BGR2RGB(temp_image)
    pic = QPixmap(QImage(img, w, h, 3*w, QImage.Format_RGB888))
    if int(w) > 500: pic = pic.scaledToWidth(500)
    lbl = QLabel(window)
    lbl.setPixmap(pic)
    window.resize(pic.width(), 100)
    author = QLineEdit(window)
    author.setText('Nadawca')
    rcvs = QLineEdit(window)
    rcvs.setText('Odbiorca')
    rcvs.move(window.width() - rcvs.width(), 0)
    lbl.move(0, author.height())
    msg = QLineEdit(window)
    msg.setText(message.decode())
    msg.move(0, author.height() + pic.height())
    window.resize(pic.width(), pic.height() + (author.height() * 2))
    win = ImageDisplayer()
    win.letsdothis()
    print('3 post')
#init connection
ip = 'localhost' # string
port = 1000 # integer
BUF_SIZE = 256
sock = s.socket(s.AF_INET, s.SOCK_STREAM)
server_address=(ip, port)

print ('starting connection')
sock.bind(server_address)

sock.listen(1)

while True:
    print ('waiting')
    connection, client = sock.accept()
    try:
        print ('connection established')
        buf=b''
        while True:
            data = connection.recv(BUF_SIZE)
            if data:
                buf+=data
                #save to memory
            else: break
    finally:
        print('transmision ended \n showing message')
        loadMessage(buf)

        connection.close()
        sys.exit(app.exec_())