#!/usr/bin/python
"""Server hosting Texas Hold 'Em games

Eventually I want to be able to host more than one table

First, implement a table structure for players to join, watch, and leave
"""
import socket
import player
import pitch

s=socket.socket()
host=socket.gethostname()
port=11037
s.bind((host,port))
s.listen(10)

# Create pitch
tab = pitch.Pitch()

while True:
    c, addr=s.accept()
    print 'Got connection from', addr
    c.send('Thank you for connecting')
    data = c.recv(1024)
    uname, epass = data.split(' ', 1)
    c.send('Welcome to the lobby '+uname+'!')
    user = player.Player()
    tab.players.append(user)
