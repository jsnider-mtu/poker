#!/usr/bin/python
"""Pitch is the name I'm giving to the table structure
desired in server.py

TODO:
* call and rais need to ensure purse doesn't go negative
* finishHand requires a way of determining a winner
"""
import random
from collections import deque

class Pitch:
    def __init__(self):
        self.watchers = []
        self.players = deque()
        self.deck = ['AH','2H','3H','4H','5H','6H','7H','8H','9H','TH','JH',\
                     'QH','KH','AD','2D','3D','4D','5D','6D','7D','8D','9D',\
                     'TD','JD','QD','KD','AC','2C','3C','4C','5C','6C','7C',\
                     '8C','9C','TC','JC','QC','KC','AS','2S','3S','4S','5S',\
                     '6S','7S','8S','9S','TS','JS','QS','KS']
        self.table = []
        self.pot = 0
        self.lastRaise = 0

    def bettingRound(self):
        if self.lastRaise == 10:
            turn = 2
        else:
            turn = 0
        while self.players[turn].dec == False or (self.players[turn].ante < \
              self.lastRaise or (self.lastRaise == 0 and \
              self.players[turn].check == False)):
            if self.players[turn].fold == True:
                if turn < len(self.players)-1:
                    turn += 1
                else:
                    turn = 0
                continue
            print(self.players[turn].name+'\'s turn')
            self.showPitch()
            self.decide(self.players[turn])
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
        return 'pot is at $'+str(self.pot)

    def call(self, amount, player):
        player.purse -= amount
        player.ante += amount

    def deal(self):
        for i in range(2):
            for play in self.players:
                play.hand.append(self.deck.pop())

    def decide(self,player):
        try:
            player.showHand()
            if player.fold == True or player.allIn == True:
                return 0
            dif = self.lastRaise - player.ante
            if dif >= player.purse:
                player.allIn = True
            k = 'a'
            if dif == 0:
                while k not in ('c', 'r', 'f'):
                    k = input("[c] to check, [r] to raise, or [f] to fold: ")
                if k == 'c':
                    print(player.name+' checks')
                    player.check = True
                elif k == 'r':
                    j = int(input("How much? "))
                    self.rais(j,player)
                    print(player.name+' raises $'+str(j))
                elif k == 'f':
                    print(player.name+' folds')
                    for i in range(2):
                        player.hand.pop()
                    player.fold = True
            else:
                while k not in ('c', 'r', 'f'):
                    if player.allIn:
                        k = input("[c] to go ALL IN with $"+str(player.purse)+", or [f] to fold: ")
                        while k not in ('c', 'f'):
                            k = input("[c] to go ALL IN with $"+str(player.purse)+", or [f] to fold: ")
                    else:
                        k = input("[c] to call $"+str(dif)+", [r] to raise, or [f] to fold: ")
                if k == 'c':
                    self.call(dif,player)
                    print(player.name+' calls $'+str(dif))
                elif k == 'r':
                    j = int(input("How much? "))
                    self.call(dif,player)
                    self.rais(j,player)
                    print(player.name+' raises $'+str(j))
                elif k == 'f':
                    print(player.name+' folds')
                    for i in range(2):
                        player.hand.pop()
                    player.fold = True
        except NoFundsError:
            self.decide(player)

    def finishHand(self):
        winner = 0
        self.players[winner].purse += self.pot
        self.pot = 0
        for play in self.players:
            play.showHand()
            play.fold = False
            play.hand = []
        return 'Hand done'

    def flop(self):
        self.deck.pop()
        for i in range(3):
            self.table.append(self.deck.pop())

    def rais(self, amount, player):
        if player.purse - amount < 0:
            print("You don't have the funds\n")
            raise NoFundsError("You don't have the funds")
        else:
            player.purse -= amount
            player.ante += amount
            self.lastRaise = player.ante

    def showPitch(self):
        print('\nCurrently Playing:')
        for play in self.players:
            print(' '+play.name+' ',end='')
        print('\n\nCurrently Watching:')
        for watch in self.watchers:
            print(' '+watch.name+' ',end='')
        print('\n# of Cards Remaining in Deck: '+str(len(self.deck)),end='')
        print(' | Current Pot: $'+str(self.pot)+' | Last Raise: $'+\
              str(self.lastRaise))

    def showTable(self):
        print('\nOn the table: '+' '.join(self.table))
        for i in self.players:
            i.showHand()

    def shuffleDeck(self):
        for i in range(random.randint(1,6)):
            random.shuffle(self.deck)

    def turnRiver(self):
        self.deck.pop()
        self.table.append(self.deck.pop())

class NoFundsError(Exception):
    pass
