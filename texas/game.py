#!/usr/bin/python3
"""
Texas Hold'Em
"""
from deck import *
from player import *

class Game:
    """
    Handles the dealer logic now
    """

    def __init__(self, host):
        self.suits = ['Hearts', 'Clubs', 'Diamonds', 'Spades']
        self.valueRange = 14
        self.d = Deck(self.suits, self.valueRange)
        self.players = [host]

    def __repr__(self):
        return self.players

    def begin(self):
        """
        Need to figure out the actual game workflow now
        So first we deal, then we have a betting round,
        need to keep track of blind tokens for betting,
        then we'll put cards on the table and go back to
        betting rounds. At the end we'll need to know how
        to determine the winner..
        """
        if len(self.players) == 1:
            raise NotEnoughPlayers
        else:
            self.d.deal()
            # Woah, what am I doin?

#    def bet

    def deal(self):
        """
        Deal the cards according to the game
        """
        for i in range(2):
            for x in self.players:
                x.hand.append(self.d.deck.pop())

    def playerJoin(self, player):
        self.players.append(player)

    def quit(self):
        quit()
