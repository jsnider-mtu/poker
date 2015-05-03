#!/usr/bin/python
import socket
import texas

s=socket.socket()
host=socket.gethostname()
port=11037
s.bind((host,port))

s.listen(10)
while True:
    c, addr=s.accept()
    print 'Got connection from', addr
    c.send('Thank you for connecting')
    data = c.recv(1024)
    uname, epass = data.split(' ', 1)
    user = texas.player.Player(uname)
    texas.players.append(user)
    texas.deal()
    data = user.showHand()
    data = data.rstrip('\n')
    c.send(data)
