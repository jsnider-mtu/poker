#!/usr/bin/python
"""Server hosting Texas Hold 'Em games

Eventually I want to be able to host more than one table

First, implement a table structure for players to join, watch, and leave
"""
import threading
import socket
import pitch

connections=[]
s=socket.socket()
host=socket.gethostname()
port=11037
s.bind((host,port))
s.listen(10)
print '[INFO] Server listening on port '+str(port)

tab = pitch.Pitch()
print '[INFO] Table created'

threads = []

class Player:
  playerCnt = 0

  def __init__(self, name):
    self.name = name
    self.hand = []
    self.purse = 100
    self.ante = 0
    self.check = False
    self.fold = False
    self.dec = False
    Player.playerCnt += 1

  def showHand(self):
    data = '\n'+self.name+' is holding '+' '.join(self.hand)
    return data

  def decide(self):
    dif = lastRaise - self.ante
    if self.fold == True:
      return 0
    if dif == 0:
      while k not in ('c', 'r', 'f'):
        k = raw_input("[c] to check, [r] to raise, or [f] to fold: ")
      if k == 'c':
        print self.name+' checks'
        self.check = True
      elif k == 'r':
        j = int(raw_input("How much? "))
        print self.name+' raises $'+str(j)
        self.rais(j)
      elif k == 'f':
        print self.name+' folds'
        for i in range(2):
          self.hand.pop()
        self.fold = True
    else:
      while k not in ('c', 'r', 'f'):
        k = raw_input("[c] to call $"+str(dif)+", [r] to raise, or [f] to fold: ")
      if k == 'c':
        print self.name+' calls $'+str(dif)
        self.rais(dif)
      elif k == 'r':
        j = int(raw_input("How much? "))
        print self.name+' raises $'+str(j)
        self.rais(j)
      elif k == 'f':
        print self.name+' folds'
        for i in range(2):
          self.hand.pop()
          self.fold = True

def worker(c, addr):
    print 'Got connection from', addr
    c.send('Thank you for connecting')
    uname = c.recv(50)
    user = Player(uname)
    print uname+' has walked in, everyone stare!'
    c.send('Welcome to the table '+uname+'!')
    sit = c.recv(1)
    if sit == 'w':
        print uname+' is watching the table'
        c.send('You\'re watching the table.\t\tpervert..')
        tab.watchers.append(user)
    elif sit == 'p':
        print uname+' is playing'
        c.send('You\'re really playing? Good luck.')
        tab.players.append(user)
    else:
        del user
        connections.remove(addr)
        print 'Users still here:'
        for x in connections:
            print str(addr)
        c.send('Goodbye.')
        print uname+' left this realm'
        c.close
    # Here is where I leave off for now

while True:
    c, addr=s.accept()
    connections.append(addr)
    t = threading.Thread(target=worker, args=(c, addr))
    threads.append(t)
    t.start()
