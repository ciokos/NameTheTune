#!/usr/bin/python3           # This is client.py file

import socket
from getkey import getkey, keys
# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
host = socket.gethostname()                           

port = 9998

# connection to hostname on the port.
s.connect((host, port))                               

# Receive no more than 1024 bytes
msg = 'ready'
s.send(msg.encode('ascii'))

s.close()
