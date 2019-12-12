import socket

host = "127.0.0.1"   #This is the IP address of the localhost. We are listening to this.
port =  2501       #This is the port we are listening. you can change these two values.

Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)            #We get socket object from the socket class.
Socket.bind((host, port))                                             #We instruct the socket to listen above defined ip and port. socket doesn't start listening immediately.
Socket.listen(4)                                                     #Now we ask the socket to start listening.
