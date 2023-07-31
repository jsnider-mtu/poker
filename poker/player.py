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
        self.last_bet = 0
        self.has_bet = False
        self.min_bet = 0

    def __repr__(self):
        return (
            f"Player {self.name} is holding {self.hand}\nTheir purse "
            f"is at ${self.purse} and their last bet this round was "
            f"{self.last_bet}"
        )

    def blind(self, amount):
        if amount <= self.purse:
            self.purse -= amount
            self.last_bet = amount
            return True
        return False

    def bet(self, amount, diff):
        if amount < self.min_bet:
            return False
        if amount <= self.purse:
            self.purse -= diff
            self.last_bet = amount
            self.has_bet = True
            self.turn = False
            return True
        print(f"{amount} is greater than the purse: {self.purse}")
        return False

    def check(self):
        if self.min_bet == 0:
            self.has_bet = True
            self.Turn = False
            return True
        return False

    def fold(self):
        self.hand.fold()
        self.folded = True
        self.Turn = False
        return True
