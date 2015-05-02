#!/usr/bin/python
import socket

s=socket.socket()
host=socket.gethostname()
port=11037
s.bind((host,port))

s.listen(10)
while True:
	c, addr=s.accept()
	print 'Got connection from', addr
	c.send('Thank you for connecting')
