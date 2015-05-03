#!/usr/bin/python
"""Pitch is the name I'm giving to the table structure
desired in server.py
"""
import random
from collections import deque
import player

class Pitch:
    def __init__(self):
        self.watchers = []
        self.players = deque()
        self.deck = ['AH','2H','3H','4H','5H','6H','7H','8H','9H','TH','JH','QH','KH','AD','2D','3D','4D','5D','6D','7D','8D','9D','TD','JD','QD','KD','AC','2C','3C','4C','5C','6C','7C','8C','9C','TC','JC','QC','KC','AS','2S','3S','4S','5S','6S','7S','8S','9S','TS','JS','QS','KS']
        self.table = []
        self.pot = 0
        self.lastRaise = 0

    def bettingRound(self):
        if self.lastRaise == 10:
            turn = 2
        else:
            turn = 0
        while self.players[turn].dec == False or (self.players[turn].ante < self.lastRaise or (self.lastRaise == 0 and self.players[turn].check == False)):
            if self.players[turn].fold == True:
                if turn < len(self.players)-1:
                    turn += 1
                else:
                    turn = 0
                continue
            self.players[turn].decide()
            self.players[turn].dec = True
            if turn < len(self.players)-1:
                turn += 1
            else:
                turn = 0
        for play in self.players:
            self.pot += play.ante
            play.ante = 0
            play.check = play.dec = False
        self.lastRaise = 0
        return 'pot is at $'+str(pot)

    def deal(self):
        for i in range(2):
            for play in self.players:
                play.hand.append(deck.pop())

    def finishHand(self):
        winner = 0
        for play in self.players:
            play.showHand()
            play.fold = False
        self.players[winner].purse += pot
        pot = 0
        return 'Hand done'

    def flop(self):
        deck.pop()
        for i in range(3):
            self.table.append(deck.pop())

    def showPitch(self):
        print '\nCurrently Playing:'
        for play in self.players:
            print ' '+play+' ',
        print '\n\nCurrently Watching:'
        for watch in self.watchers:
            print ' '+watch.name+' ',
        print '\n# of Cards Remaining in Deck: '+str(len(self.deck)),
        print ' | Current Pot: $'+str(self.pot)+' | Last Raise: $'+str(self.lastRaise)

    def showTable(self):
        return 'On the table: '+' '.join(self.table)

    def shuffleDeck(self):
        for i in range(random.randint(1,6)):
            random.shuffle(deck)

    def turnRiver(self):
        self.deck.pop()
        self.table.append(deck.pop())
