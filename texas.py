#!/usr/bin/python
"""Texas Hold 'Em Game Engine
--------------------------
	Goal:
		Module that is a fully functional game engine to power WSOP rules Texas Hold 'Em

	To Do:
		Restructure hand() to be multiplayer
        Learn pickle to send player objects
		Define structured layout of engine
		Transform this file into a functional module
"""
import random
from collections import deque

deck = ['AH','2H','3H','4H','5H','6H','7H','8H','9H','TH','JH','QH','KH','AD','2D','3D','4D','5D','6D','7D','8D','9D','TD','JD','QD','KD','AC','2C','3C','4C','5C','6C','7C','8C','9C','TC','JC','QC','KC','AS','2S','3S','4S','5S','6S','7S','8S','9S','TS','JS','QS','KS']
players = deque()
table = []
pot = lastRaise = 0

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

#def main():
#  nm = raw_input("What's your name? ")
#  you = Player(nm)
#  players.append(you)
def shuffleDeck():
  for i in range(random.randint(1,6)):
    random.shuffle(deck)

#  while len(deck) > (len(players)*2+8):
#    hand(you)
#    players.rotate(-1)
