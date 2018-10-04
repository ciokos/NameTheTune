import socket
import threading
import sys
import spotipy
import spotipy.util as util
import os
import random
import time
import webbrowser

readycount = 0
round_play = True


def play(client):
    msg = client.recv(1024)
    global readycount
    readycount = readycount + 1
    print(msg.decode('ascii'))


# client.close()

def wait_for_first(client1, client2):
    msg = client1.recv(1024)
    global round_play
    if round_play:
        send(client1, client2, "you were faster!", "another player plays\npress space to continue...")
        print(client1, " were faster")
        round_play = False


def send(client1, client2, text1, text2):
    client1.send(text1.encode('ascii'))
    client2.send(text2.encode('ascii'))


def wait_for_players():
    global readycount
    while True:
        if readycount >= 2:
            readycount = 0
            break


username = "ender5224"
scope = 'user-library-read'
try:
    token = util.prompt_for_user_token(username, scope)

except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username)

if token:
    sp = spotipy.Spotify(auth=token)
    plID = '7D6jsVCme6OKgQO1R1xSId'

    game_playlist = sp.user_playlist(username, plID, fields="tracks,next")

    tracks = game_playlist['tracks']
    tracks = tracks['items']

    # create a socket object
    serversocket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)

    # get local machine name
    host = "0.0.0.0"

    port = 9999

    # bind to the port
    serversocket.bind((host, port))
    print(socket.gethostbyname((socket.getfqdn())))

    print("server is waiting for players...")

    # queue up to 5 requests
    serversocket.listen(2)
    player1, addr1 = serversocket.accept()
    print("Got a connection from %s" % str(addr1))
    player2, addr2 = serversocket.accept()
    print("Got a connection from %s" % str(addr1))

    ##### GAME #####

    while len(tracks)>0:
        print('songs:')
        print(len(tracks))
        thread1 = threading.Thread(target=play, args=(player1,))
        thread2 = threading.Thread(target=play, args=(player2,))
        thread1.start()
        thread2.start()
        send(player1, player2, "Are you ready?", "Are you ready?")
        print("Are you ready?")
        wait_for_players()
        thread1.join()
        thread2.join()
        idx = random.randint(0, len(tracks)-1)
        print("index:")
        print(idx)
        while(not isinstance(tracks[idx]['track']['preview_url'], str)):
            idx = random.randint(0, len(tracks)-1)
        webbrowser.open_new_tab(tracks[idx]['track']['preview_url'])
        send(player1, player2, "Round start!", "Round start!")
        thread3 = threading.Thread(target=wait_for_first, args=(player1, player2,))
        thread4 = threading.Thread(target=wait_for_first, args=(player2, player1,))
        thread3.start()
        thread4.start()
        thread3.join()
        thread4.join()
        tracks.remove(tracks[idx])
        os.system("TASKKILL /F /IM chrome.exe")
        round_play = True

else:
    print("Can't get token for", username)
