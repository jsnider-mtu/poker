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
import player
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

  while len(deck) > (len(players)*2+8):
    hand(you)
    players.rotate(-1)
