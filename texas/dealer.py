#!/usr/bin/python
"""
This is a Dealer class. It deals cards from a deck to players
"""
from deck import *
from collections import deque

class Dealer:
    def __init__(self, deck, game, owner, name='dealer'):
        self.deck = deck
        self.game = game
        self.name = name
        self.players = [owner]
        self.table = []
        self.pot = 0

    def __repr__(self):
        return 'A Dealer for {} named {}'.format(self.game, self.name)

    def deal(self):
        """
        Deal the cards according to game
        """
        if game == "Texas Hold'Em":
            for i in range(2):              # Deal two cards to each player
                for x in self.players:      # in order
                    x.hand.append(self.deck.pop())
        else:
            raise 'The fuck are we even playing?'

    def rename(self, name):
        """Rename the dealer"""
        self.name = name

    def showTable(self):
        """
        Return a printout msg of the table and hands
        """
        msg = '\nOn the table: '+' '.join(self.table)
        for i in self.players:
            msg += '\n'+i.showHand()

