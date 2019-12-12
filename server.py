import socket
'''
1.) Start reading from the second part of the program.
2.) This just serves any html pages in the same folder as the script. Image or any other resource type will break the script.
3.) No error handling or exception handling is done.
4.) start reading fromt the second part(marked below))

'''
def process(request):
    print("###############################")
    print(request)


    requestlines = request.splitlines()                             #Break the request in to lines so we can read it.
    firstline = requestlines[0]                                     #We are only interested in the first line. Usually it is something like: GET /test.html HTTP/1.1]\r\n
    divided_parts_of_the_first_line = firstline.split(' ')          #Now we divide the first line in to 3 parts(using above example)-> GET,/test.html,/HTTP/1.1 .
    requestedfilename = divided_parts_of_the_first_line[1]          # We only want the 2nd part of the line(the file requested). 2nd part of the filename is in the 1 element of the list.
    requestedfilename = requestedfilename.strip('/')                #Our filename contains a '/' in it. we need to remove it.
    try:                                                                        #Try to open the requested file and set the response.
        fileObject = open(requestedfilename,'r')                                #Now we open the requested file. the file has to be in the same location as this script.
        requested_file = fileObject.read().encode()                             # We read the contents of the file and encode it to a byte stream. This is because socket only accepts a byte stream.
        response = "HTTP/1.0 200 OK\r\n".encode()                               # This is the first line of the HTTP response. This should not be changed.
        if (requestedfilename.endswith("html")):                                # we check whether the requested file is an html file or not.Currently we only serve html files.
            response = response + "Content-Type : text/html\r\n\n".encode()     # we set the Content-Type field of the header to html because we are sending html.
            response = response + requested_file                                # Finally we add the requested file to the response. This order has to be followed.

    except FileNotFoundError:                                                   #Catch the exception, If the file is not found we send the 404 response to client.
        response = "HTTP/1.0 404 Not Found\r\n"
        response += "Content-Type :text/html\r\n\n"
        response += " <h1>File Not found error<h1>\r\n"
        response  = response.encode()
    finally:
        recvSock.send(response)                                                 #We send the response to the client.

        print("###############################")
        recvSock.close()                                                        #close the client socket.


'''
****************************************************
****************************************************
start reading from here. Execution starts from here.
***************************************************
****************************************************
'''
'''
To check the functionality: type in your browser: 127.0.0.1:2500/test.html.
If after first time you get the Adress already in use error, change port and run again.
'''


host = "127.0.0.1"   #This is the IP address of the localhost. We are listening to this.
port =  2501       #This is the port we are listening. you can change these two values.

Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)            #We get socket object from the socket class.
Socket.bind((host, port))                                             #We instruct the socket to listen above defined ip and port. socket doesn't start listening immediately.
Socket.listen(10)                                                       #Now we ask the socket to start listening.

while( True):                                                         #This loop will run forever until we break out of it.
    receivedData = ''                                                 #This is the variable we use to store data we get from the socket.
    recvSock,address = Socket.accept()                                #we insruct the socket to accept a connection. This gives us a socket and the adress of the client that made the connection. We use the received socket to communicate with the client.
    while( True):
        receivedData += recvSock.recv(1024).decode("utf-8")           #We read 1024 bytes at a time from the socket and decode it to utf-8.
        if(receivedData.endswith("\r\n\r\n")):                        #check whether the received data has "\r\n\r\n" in the end. This is the marker used by http to mark the end of the request.
            process(receivedData)                                     #If we have received the full http request we send it for processing by calling the process() method. Defined above.
            break

