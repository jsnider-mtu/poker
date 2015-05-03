#!/usr/bin/python
import socket

sit = 'a'
s=socket.socket()
host=socket.gethostname()
port=11037

s.connect((host,port))
print '[INFO] Client started'
print s.recv(50) # Thank you
uname = raw_input('Login name: ')
s.send(uname)
print s.recv(50) # Welcome
while sit not in ['w', 'p', 'l']:
    sit = raw_input('"p" to play, "w" to watch, "l" to leave: ')[:1]
s.send(sit)
print s.recv(50)
if sit == 'l':
    s.close
    exit(0)
nex = s.recv(1)

