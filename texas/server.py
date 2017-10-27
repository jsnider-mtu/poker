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
import lobby

class Server:
    """
    The Server class has one lobby with multiple games.
    Games have a one-to-one relationship to a Pitch.
    
    Parameters: bind_ip, bind_port
    Attributes: self.bind_ip, self.bind_port, sock
    Methods: main
    """

    def __init__(self, bind_ip='0.0.0.0', bind_port=9999):
        self.bind_ip = bind_ip
        self.bind_port = bind_port
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        return self

    # this is our client-handling thread
    def handle_client(client_socket):
        """
        This thread's purpose is to authenticate a user before they enter
        the service-land. We're mimicking IRC in that any user can enter
        but only once, at least for now. Once logged in we'll fork a new
        process if they create a new Pitch. The point is to limit how easy
        it is for the service to be DoS'ed by accident.
        """
        request = client_socket.recv(1024)
        print("[*] Received: %s" % request)

        # Parse the request
        # The first thing client sends should be USER name for the player
        if not request.startswith('USER '):
            msg = "{'Error': {'Invalid Syntax': 400}}"
            client_socket.send(msg)
            client_socket.close()

if __name__ == '__main__':
    while True:
        server = Server()
        client,addr = server.sock.accept()
        print("[*] Accepted connection from: %s:%d" % (addr[0],addr[1]))
        # spin up our client thread to handle incoming data
        client_handler = threading.Thread(target=server.handle_client,
                                                args=(client,))
        client_handler.start()
