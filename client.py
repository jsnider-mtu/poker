#!/usr/bin/python
import socket

s=socket.socket()
host=socket.gethostname()
port=11037

s.connect((host,port))
print '[INFO] Client started'
print s.recv(1024) # Thank you
uname = raw_input('Login name: ')
passw = raw_input('Password: ')
epass = passw.encode('rot_13')
del passw
s.send(uname+' '+epass)
print s.recv(1024) # Welcome + first option
des = raw_input()[:1]
s.send(des)
print s.recv(1024)
