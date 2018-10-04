import socket
from getkey import getkey, keys
import threading


def thrd_fnc():
    msg = s.recv(1024)
    print(msg.decode('ascii'))


def send(text):
    s.send(text.encode('ascii'))


def recieve():
    msg = s.recv(1024)
    return msg.decode('ascii')


def confirm():
    msg = 'ready'
    key = ''
    while key != ' ':
        key = getkey()
    send(msg)
    print(msg)


# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
#host = socket.gethostname()
host = "10.0.0.36"

port = 9998

# connection to hostname on the port.
s.connect((host, port))
print("connected")

##### GAME #####

while True:
    print(recieve())
    confirm()
    print(recieve())
    t = threading.Thread(target=thrd_fnc, args=())
    t.start()
    confirm()
    t.join()


s.close()
