#!/usr/bin/python
"""To Do:
Work on decide() (it doesn't look functional at all)

"""
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
