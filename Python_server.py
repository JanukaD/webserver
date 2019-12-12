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
    elif file_type == 'jpeg'or file_type == 'jpg':
        header += 'Content-Type: image/jpeg\r\n'
    elif file_type == 'mp4':
        header += 'Content-Type: video/mp4\r\n'
    elif file_type == 'css':
        header += 'Content-Type: text/css\r\n'

    header += 'Connection: close\r\n\n'
    return header.encode()

def process(request):
    print(request)


    requestlines = request.splitlines()
    firstline = requestlines[0] 
    divided_parts_of_the_first_line = firstline.split(' ') 
    requestedfilename = divided_parts_of_the_first_line[1]
    requestedfilename = requestedfilename.strip('/')
    fileType = requestedfilename.split('.')[1]
    try:
        fileObject = open(requestedfilename, 'br')             #file should be opened in br mode. Otherwise images won't be served.
        requested_file = fileObject.read()
        fileObject.close()
        print("Requested File : " + requestedfilename)
        response_header = headers(200, fileType )   # you forgot to send the file type to headerd function. I added it. (fileType variable is declared above)
        response = requested_file



    except FileNotFoundError:  
        response_header = headers(404, '')
        response  = b"<h1>Error 404 - File Not Found</h1>"

    except IndexError:  
        response_header = headers(400, '')
        response  = b"<h1>Malformed request</h1>"

    finally:   #you created the response, but forgot to send it. if you dont use finally clause you'll have to add recvSoc.send line to all try,except blocks.
        response_header +=  response
        recvSock.send(response_header)
        recvSock.close()

host = "127.0.0.1"   
port =  3000

Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Socket.bind((host, port))
Socket.listen(4)

while( True):   
    receivedData = ''  
    recvSock,address = Socket.accept()
    while( True):
        receivedData += recvSock.recv(1024).decode("utf-8")
        if(receivedData.endswith("\r\n\r\n")): 
            process(receivedData) 
            break



