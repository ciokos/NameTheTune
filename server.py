#!/usr/bin/python3
import socket
import threading

readycount = 0

def play(client):
   	msg = client.recv(1024)
   	global readycount
   	readycount = readycount + 1
   	print(msg.decode('ascii'))
   	client.close()                   

# create a socket object
serversocket = socket.socket(
	        socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
host = "0.0.0.0"                        

port = 9998                                           

# bind to the port
serversocket.bind((host, port))                      
#print(socket.gethostbyname((socket.getfqdn())))    

print("server is waiting for players...")
# queue up to 5 requests
serversocket.listen(2)
player1,addr1 = serversocket.accept()
print("Got a connection from %s" % str(addr1))
player2,addr2 = serversocket.accept()
print("Got a connection from %s" % str(addr1))
print("Are you ready?")


thread1 = threading.Thread(target=play, args=(player1, ))
thread2 = threading.Thread(target=play, args=(player2, ))

thread1.start()
thread2.start()

while True:
	if readycount >= 2:
		break

print('great')
thread1.join()
thread2.join()