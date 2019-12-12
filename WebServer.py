import socket

def process(request):
    lines = request.splitlines()  #get lines of the request
    parts = lines[0].split(' ')   #divide first line in to three parts. If the 1st line is GET /resource HTTP/1.0 , this divided in to GET, /resource and /HTTP/1.0
    if(parts[0] =='GET'):         #take the first part of the above line.(Checking for the method)
        #do the processing for GET here

        wanted_file = parts[1].strip('/')  #this contains thr requested file.
        f = open(wanted_file, 'rb')        #open the file in binary read mode.
        print('file opened')
        file_to_send = f.read()            #read the file.
        print('file read')
        response = b"HTTP/1.0 200 OK\r\n"                   #put the first part of the response
        response += b"content-type : text/html\r\n\n"       #put the content part of the response
        response += file_to_send                            # add the file requested
        rSocket.send(response)                              #send the file
        rSocket.close()                                     # close the socket
    #elif (parts[0] == 'PUT')
    #do the processing for PUT here


host = "127.0.0.1"
port =  2450

Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Socket.bind((host, port))
Socket.listen(10)

input =''
while True:
    rSocket, Address = Socket.accept()
    print("socket accepted")

    limit = 0 # lmit for the header size.

    while(True):
        # Read 1024byte block from the socket  at a time then data from the socket is decoded to utf-8 format
        received = rSocket.recv(1024).decode("utf-8")
        input += received   # put the read data in to input variable
        limit += 1

        # HTTP request end is marked by '\r\n\r\n'. We read from the socket untill we get that string.
        if(received.endswith('\r\n\r\n')):
            print("Header sent for processing")
            process(input)  #send the header for processing
            break
        #We only read 4KB header
        if( limit <= 3):
            print("Send entity too large error")
            break







