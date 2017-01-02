README.TXT

VISION OF FINAL VERSION:
*fully based on PyQT client interface made for sending images and messages to other clients connected to server
*server written in c/cpp
*every client will connect to server by one, chosen port; client can write his own nickname
*server will send back new port, where stable connection will be established (every client will have his unique port)
*server will send forward message of new user in system
*client interface will automaticaly update 'users_list'
*server will have list (ports_list): user_id, port
*client will have list (users_list): user_name, user_id
*message will consist of: sender_id,receiver(s)_id(s),message,image,height_of_image,width_of_image
*main page of client api will consist of list of other users and option to send message
*any new received message will be shown in pop up window
*server will read header of message and sending it forward after checking 'ports_list'
*probably port(s) will be used as id(s)
*port(s)/id(s) will be hidden on client side

############################################################################

version 0.0.1

STRUCTURE OF PROJECT:
-main_dir:
---client:
-----image1.jpg
-----image2.jpg
---server:
-----new.jpg
---file.py
---client.py

DESCRIPTION OF .py FILES:
a) file.py:
*code of tcp server
*waiting for connection on localhost:1000
*after connection receiving message from client
*displays message and saves image in 'main_dir/server/' as 'new.jpg'
b) client.py
*written in PyQT 
*window application, where user can send image and message to server
*image have to be in 'main_dir/client/' directory and be '.jpg'
*user is choosing photo by writing name of image, in this case he can type 'image1' or 'image2'
*in current situation, client can send photo only once per application
*in message, user CANNOT type '|||' symbol

DESCRIPTION OF MESSAGE PATTERN:
*function for send message starts at 49. line of 'client.py' file
*function for receiv message starts at 12. line of 'file.py' and is called
*symbol to divide parts of message is '|||'
*message pattern: image + ||| + message + ||| + height_of_image + ||| + width_of_image
*image is encoding in 'imgToString()' function in 41. line of client.py file
*function 'strToImage()' in 6. line of file.py file is using to decode received image

####################################################################################3

#TODO for 0.0.2 version:
*server.cpp (cpp)
*own signal/slot system for receiving messages on client site (py)
*better interface for sending/receiving messages (py)
