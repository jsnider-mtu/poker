#!/usr/bin/python
"""
The player has a purse, an ante, and a hand

(Plus a name, UID, and some state flags)
"""
class Player:
  playerCnt = 0

  def __init__(self, name):
    self.allIn = False
    self.name = name
    self.hand = []
    self.purse = 100
    self.ante = 0
    self.check = False
    self.fold = False
    self.dec = False
    self.uniq = Player.playerCnt
    Player.playerCnt += 1

  def showHand(self):
    print('\n'+self.name+' is holding '+' '.join(self.hand))
    print('\nTheir purse is currently: $'+str(self.purse))
    print('Their ante is currently: $'+str(self.ante)+'\n')
