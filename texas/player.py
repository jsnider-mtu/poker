#!/usr/bin/python
"""
The player has a purse, an ante, and a hand

(Plus a name, UID, and some state flags)
"""

class Player:

    def __init__(self, name, purse=100):
        self.allIn = False
        self.name = name
        self.hand = Hand()
        self.purse = purse
        self.check = False
        self.fold = False
        self.lastbet = 0
        self.hasbet = False

    def __repr__(self):
        return f"Player {self.name} is holding {self.hand}\nTheir purse "\
                "is at ${self.purse} and their last bet this round was "\
                "{self.lastbet}"

    def blind(self, amount):
        if amount <= self.purse:
            self.purse -= amount
            self.lastbet += amount
            return True
        return False

    def bet(self, amount):
        if amount <= self.purse:
            self.purse -= amount
            self.lastbet += amount
            self.hasbet = True
            return True
        return False

    def check(self):
        pass

    def rais(self):
        pass

    def fold(self):
        pass
