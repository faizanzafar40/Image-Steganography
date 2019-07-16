# import dependencies
import socket
import sys
import re
import os
from Encoder import *

# create and bind a new socket

newSocket = socket.socket()
myHost = 'localhost'
myPort = 55555
newSocket.bind((myHost, myPort))

# read image file and return binary

def load_image_binary(myfile):
    with open(myfile, 'rb') as myfile:
        return myfile.read()

newSocket.listen(10) # accepting 10 max connections

while True:
   client, address = newSocket.accept()
   print('Got connection from', address)

   HTTPRequest = client.recv(4096)
   fileName = re.search(r"file(\d+).txt",HTTPRequest.decode("utf-8")); # extract filename from HTTP request

   if hasattr(fileName,'group'):
      fileCompleteName = fileName.group(0) # match for complete regex above
   else:
      fileCompleteName = ''

   # SEND APPROPRIATE RESPONSE TO CLIENT
   
   if fileCompleteName == '':
      client.send(str.encode('HTTP/1.1 400 Bad request\nContent-type: text/html\n\n<html><head><title>400 Bad request</title></head><body><p>Sorry, your request is invalid.</p></body><html>','utf-8'))
      client.close()

   elif os.path.isfile(fileCompleteName) == False:
      client.send(str.encode('HTTP/1.1 404 Not Found\nContent-type: text/html\n\n<html><head><title>404 Not Found</title></head><body><p>Sorry, the object you requested was not found.</p></body><html>','utf-8'))
      client.close()

   else:
      myEncoder(fileName.group(0),fileName.group(1)) # encode and save encoded file
      imageContents = load_image_binary(fileName.group(1)+'modified.png') #return encoded file
      client.send(str.encode('HTTP/1.1 200 OK\nContent-type: image/png\n\n','utf-8') + imageContents)
      client.close()