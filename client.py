#!/usr/bin/python
import socket
import player

s=socket.socket()
host=socket.gethostname()
port=11037

s.connect((host,port))
print s.recv(1024)
print '[INFO] Client started'
uname = raw_input('Login name: ')
passw = raw_input('Password: ')
epass = passw.encode('rot_13')
del passw
s.send(uname+' '+epass)
print s.recv(1024)
user = player.Player(uname)
user.showHand()
s.close
