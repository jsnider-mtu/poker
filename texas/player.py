#!/usr/bin/python
"""
The player has a purse, an ante, and a hand

(Plus a name, UID, and some state flags)
"""

import deck

class Player:
  playerCnt = 0

  def __init__(self, name, purse=100):
    self.allIn = False
    self.name = name
    self.hand = deck.Hand()
    self.purse = purse
    self.ante = 0
    self.check = False
    self.fold = False
    self.uniq = Player.playerCnt
    Player.playerCnt += 1

  def showHand(self):
    print('\n'+self.name+' is holding '+' '.join(self.hand))
    print('\nTheir purse is currently: $'+str(self.purse))
    print('Their ante is currently: $'+str(self.ante)+'\n')
