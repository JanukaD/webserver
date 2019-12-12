import socket

def headers(response_code, file_type):
    print("Requested File Type : " + file_type)

    header = ''
    if response_code == 200:
        header += 'HTTP/1.1 200 OK\r\n'
    elif response_code == 404:
        header += 'HTTP/1.1 404 Not Found\r\n'
    elif response_code == 400:
        header += 'HTTP/1.1 400 Bad Request\r\n'

    if file_type == 'html':
        header += 'Content-Type: text/html\r\n'
    elif file_type == 'png':
        header += 'Content-Type: image/png\r\n'
    elif file_type == 'jpeg':
        header += 'Content-Type: image/jpeg\r\n'
    elif file_type == 'mp4':
        header += 'Content-Type: video/mp4\r\n'
    elif file_type == 'css':
        header += 'Content-Type: text/css\r\n'
    elif file_type == 'pdf':
        header += 'Content-type: application/pdf\r\n'

    header += 'Connection: close\r\n\n'
    return header.encode()

def process(request):
    print(request)


    requestlines = request.splitlines()                          #Break the request in to lines for read it.
    firstline = requestlines[0]                                  #Only nedded the first line. Usually it is something like: GET /test.html HTTP/1.1]\r\n
    divided_parts_of_the_first_line = firstline.split(' ')       #Divide the first line in to 3 parts(using above example)-> GET,/test.html,/HTTP/1.1 .
    requestedfilename = divided_parts_of_the_first_line[1]       # Only want the 2nd part of the line(the file requested).
    requestedfilename = requestedfilename.strip('/')             #Filename contains a '/' in it. Need to remove it.
    fileType = requestedfilename.split('.')[1]
    try:                                                         #Try to open the requested file and set the response.
        fileObject = open(requestedfilename, 'br')               #file should be opened in br mode. Otherwise images won't be served.
        requested_file = fileObject.read()                       # We read the contents of the file. 
        fileObject.close()
        print("Requested File : " + requestedfilename)
        response_header = headers(200, fileType )   
        response = requested_file



    except FileNotFoundError:                                    #Catch the exception, If the file is not found we send the 404 response to client.
        response_header = headers(404, '')
        response  = b"<h1>Error 404 - File Not Found</h1>"

    except IndexError:  
        response_header = headers(400, '')                       #Catch the exception, If the malformed request we send the 400 response to client.
        response  = b"<h1>Malformed request</h1>"

    finally:   
        response_header +=  response
        recvSock.send(response_header)                           #Send the response to the client.
        recvSock.close()                                         #close the client socket.

host = "127.0.0.1"   
port =  3000

Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       #Get socket object from the socket class.
Socket.bind((host, port))
Socket.listen(4)

while( True):   
    receivedData = ''  
    recvSock,address = Socket.accept()
    while( True):
        receivedData += recvSock.recv(1024).decode("utf-8")     #Read 1024 bytes at a time from the socket and decode it to utf-8.
        if(receivedData.endswith("\r\n\r\n")):
            print("Header sent for processing")
            process(receivedData) 
            break




