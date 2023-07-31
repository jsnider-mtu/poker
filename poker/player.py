#!/usr/bin/python
"""
The player has a purse, an ante, and a hand

(Plus a name, UID, and some state flags)
"""
from . import deck


class Player:
    def __init__(self, name, purse=100):
        self.name = name
        self.turn = False
        self.hand = deck.Hand(self.name)
        self.purse = purse
        self.folded = False
        self.lastbet = 0
        self.hasbet = False
        self.minbet = 0

    def __repr__(self):
        return (
            f"Player {self.name} is holding {self.hand}\nTheir purse "
            f"is at ${self.purse} and their last bet this round was "
            f"{self.lastbet}"
        )

    def blind(self, amount):
        if amount <= self.purse:
            self.purse -= amount
            self.lastbet = amount
            return True
        return False

    def bet(self, amount, diff):
        if amount < self.minbet:
            return False
        if amount <= self.purse:
            self.purse -= diff
            self.lastbet = amount
            self.hasbet = True
            self.turn = False
            return True
        print(f"{amount} is greater than the purse: {self.purse}")
        return False

    def check(self):
        if self.minbet == 0:
            self.hasbet = True
            self.Turn = False
            return True
        return False

    def fold(self):
        self.hand.fold()
        self.folded = True
        self.Turn = False
        return True
