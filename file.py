import sys
import socket as s
import cv2
import numpy as np

def stringToImg(string):
    string = string.split("_")
    string = [x.split("+") for x in string]
    string = [[y.split(",") for y in x] for x in string]
    return [[[np.float32(z) for z in y] for y in x] for x in string]

def loadMessage(buffer):
    img, message, h, w = buffer.split(b'|||')
    h = h.decode()
    w = w.decode()
    print(message.decode())
    img = stringToImg(img.decode())
    temp_image = np.zeros(shape=(int(h), int(w), 3), dtype=np.uint8)
    for row in range(int(h)):
        for value in range(int(w)):
            for channel in range(3):
                temp_image[row][value][channel] = img[row][value][channel]
    cv2.imwrite('server/new.jpg', temp_image)


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
        loadMessage(buf)
        print('Image saved in //server// folder')
        print('transmision finished')
        connection.close()