import socket
from getkey import getkey, keys
# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
#host = socket.gethostname()
host = "10.0.0.36"                        

port = 9999

# connection to hostname on the port.
s.connect((host, port))                               

# Receive no more than 1024 bytes
msg = 'ready'
key = ''
while key != ' ':
	key = getkey()

s.send(msg.encode('ascii'))

s.close()
