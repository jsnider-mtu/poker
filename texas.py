#!/usr/bin/python
import random
from collections import deque

deck = ['AH','2H','3H','4H','5H','6H','7H','8H','9H','TH','JH','QH','KH','AD','2D','3D','4D','5D','6D','7D','8D','9D','TD','JD','QD','KD','AC','2C','3C','4C','5C','6C','7C','8C','9C','TC','JC','QC','KC','AS','2S','3S','4S','5S','6S','7S','8S','9S','TS','JS','QS','KS']
players = deque()
table = []
pot = lastRaise = 0

class Player:
  playerCnt = 1

  def __init__(self, name=None, user=False):
    self.name = name
    self.user = user
    if self.name == None:
      self.name = 'player'+str(Player.playerCnt)
      Player.playerCnt += 1
    self.hand = []
    self.purse = 100
    self.ante = 0
    self.check = False
    self.fold = False
    self.dec = False

  def showHand(self):
    print self.name+' '+' '.join(self.hand)+' $'+str(self.purse)

  def decide(self):
    global lastRaise
    dif = lastRaise - self.ante
    if self.fold == True:
      return 0
    if self.user == True:
      k = 'a'
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
    else:
      if dif == 0:
	print self.name+" checks"
	self.check = True
      else:
        print self.name+" calls $"+str(lastRaise)
        self.rais(dif)

  def rais(self, amt):
    global lastRaise
    self.purse -= amt
    self.ante += amt
    lastRaise = self.ante

def bettingRound():
  global lastRaise
  global pot
  if lastRaise == 10:
    turn = 2
  else:
    turn = 0
  while players[turn].dec == False or (players[turn].ante < lastRaise or (lastRaise == 0 and players[turn].check == False)):
    if players[turn].fold == True:
      if turn < len(players)-1:
	turn += 1
      else:
	turn = 0
      continue
    players[turn].decide()
    players[turn].dec = True
    if turn < len(players)-1:
      turn += 1
    else:
      turn = 0
  for player in players:
    pot += player.ante
    player.ante = 0
    player.check = player.dec = False
  lastRaise = 0
  print 'pot is at $'+str(pot)

def deal():
  for i in range(2):
    for player in players:
      player.hand.append(deck.pop())

def finishHand():
  global pot
  winner = 0
  for player in players:
    player.showHand()
    player.fold = False
  players[winner].purse += pot
  pot = 0
  print 'Hand done'

def flop():
  deck.pop() # burn
  for i in range(3):
    table.append(deck.pop())

def hand(you):
  global table
  deal()
  players[0].rais(5)
  players[1].rais(10)
  you.showHand()
  bettingRound()
  flop()
  you.showHand()
  showTable()
  bettingRound()
  turnRiver()
  you.showHand()
  showTable()
  bettingRound()
  turnRiver()
  you.showHand()
  showTable()
  bettingRound()
  finishHand()

def showTable():
  print "On the table: "+' '.join(table)

def turnRiver():
  deck.pop() # burn
  table.append(deck.pop())

def main():
  nm = raw_input("What's your name? ")
  you = Player(nm, True)
  players.append(you)
  for i in range(random.randint(1,6)):
    random.shuffle(deck)
  cnt = raw_input("How many other players? ")
  for x in range(int(cnt)):
    tmp = Player()
    players.append(tmp)
  while len(deck) > (len(players)*2+8):
    hand(you)
    players.rotate(-1)

if __name__=='__main__':
  main()