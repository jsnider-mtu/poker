#!/usr/bin/python3
"""
Starting with Texas Hold'Em for now
Each game will have a definition for the Deck
"""
from dealer import *
from deck import *
from player import *

class Game:
    def __init__(self, user, name="Texas Hold'Em"):
        self.name = name
        self.user = user
        if self.name == "Texas Hold'Em":
            suits = ['Hearts', 'Clubs', 'Diamonds', 'Spades']
            valueRange = 14
            self.deck = Deck(suits, valueRange)
        elif self.name == "Petals":
            # Add logic for a dice game
            # instead of a card game
            pass
        else:
            print('What the fuck are we playing?')

    def __repr__(self):
        return self.name

    def begin(self):
        pass

    def quit(self):
        pass

if __name__ == '__main__':
    user = input("Username? ")
    g = Game(user)
    g.begin()
