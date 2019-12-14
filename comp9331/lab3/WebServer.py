#define python 3.7
import sys
import re
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', int(sys.argv[1])))
s.listen(5)
file = open('index.html' , 'rb')
index_content = b'''
HTTP/1.1 200 ok
Content-Type: text/html

'''
index_content += file.read()
file.close()

while 1:
    connection, addr = s.accept()
    sentence = connection.recv(1024)
    sentence = sentence.decode('utf-8')
    temp = sentence.split(' ')
    if (temp == ['']):
        content = b'''
HTTP/1.1 404 Not Found
Content-Type: image/png

'''
    else:
        method = temp[0]
        scr = temp[1]
        if (method == 'GET'):
            if (scr == '/index.html'):
                content = index_content
            elif ('myimage' in scr):
                content = b'''
HTTP/1.1 200 ok
Content-Type: image/png

'''
                try:
                    f = open(scr[1:] , 'rb')
                    content += f.read()
                    f.close()
                except:
                    content = b'''
HTTP/1.1 404 Not Found
Content-Type: image/png

'''
            else:
                content = b'''
HTTP/1.1 404 Not Found
Content-Type: text/html

'''
    connection.sendall(content)
    connection.close()
