#!/usr/bin/python
"""Pitch is the name I'm giving to the table structure
desired in server.py
"""
from deck import *
import player
from collections import deque

class Dealer(Pitch):
    def __init__(self, deck, game="Texas Hold'Em", name='dealer'):
        assert len(deck) == 52
        assert game in ["Texas Hold'Em"]
        self.deck = deck
        self.game = game
        self.name = name

    def __repr__(self):
        return 'A Dealer for {} named {}'.format(self.game, self.name)

    def deal(self)
        if game == "Texas Hold'Em":
            for i in range(2):              # Deal two cards to each player
                for x in self.players:      # in order
                    x.hand.append(self.deck.pop())
        else:
            raise 'The fuck are we even playing?'

class Pitch:
    """This is the "playing field" where the Deck and Dealer are
    instantiated."""
    def __init__(self, owner):
        self.deck = Deck()
        self.dealer = Dealer(self.deck)
        self.players = [owner]
        self.table = []
        self.watchers = []
        self.pot = 0

    def showTable(self):
        print('\nOn the table: '+' '.join(self.table))
        for i in self.players:
            i.showHand()
