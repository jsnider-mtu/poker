#!/usr/bin/python3
"""
This is originally from "Programming Python" 4th Ed. by Mark Lutz,
published by O'Reilly

So how do I want the server<->client conversation to look?

Client talks first, server responds with HTTP 200 and new state
(actually all clients need new state after an action taken by any
player), or HTTP 500 in the case of an illegal move (shouldn't
happen if using the client in this repo, I hope anyways), or HTTP 400
in the case of gobbledy-gook. You know what, fuck it, let's define as
many as possible:

200 - OK (data is new state of the pitch)
201 - Created (new player created, new table created, etc)
302 - If HTTP move them to HTTPS (This will come later)
400 - Bad Request (Gobbledy-gook as far as I am concerned)
401 - Unauthorized (Not yet signed-in/registered)
403 - Forbidden (Because Fuck You!, that's why)
404 - Not Found
405 - Method Not Allowed (Will have to include an Allow header)
406 - Not Acceptable (Response entity characteristics mismatch)
408 - Request Timeout (Don't think I'll need this one)          <-#
409 - Conflict (Hopefully won't need to use this one either)
410 - Gone (Table was destroyed somehow)
505 - HTTP Version Not Supported (Let's only allow HTTP/1.1)
"""
import socket
import threading

bind_ip = "0.0.0.0"
bind_port = 9999

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind((bind_ip,bind_port))

server.listen(100)

print("[*] Listening on %s:%d" % (bind_ip,bind_port))

# this is our client-handling thread
def handle_client(client_socket):
  
  # print out what the client sends
  request = client_socket.recv(1024)
  
  print("[*] Received: %s" % request)

  # Parse the request
  
  
  # send back a packet
  client_socket.send("ACK!")
  
  client_socket.close()
  
while True:
  
  client,addr = server.accept()
  
  print("[*] Accepted connection from: %s:%d" % (addr[0],addr[1]))
  
  # spin up our client thread to handle incoming data
  client_handler = threading.Thread(target=handle_client,args=(client,))
  client_handler.start()
