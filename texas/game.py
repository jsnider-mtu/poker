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

    def __init__(self):
        self.suits = ['Hearts', 'Clubs', 'Diamonds', 'Spades']
        self.valueRange = 14
        self.d = Deck(self.suits, self.valueRange)
        self.table = Table("test", self.d, 8, 5, 10)
        self.dealer = 0

    def __repr__(self):
        return f"Table: {self.table.name} has {len(self.table.seats)} seats, {self.table.seatstaken()} of which are taken"

    def begin(self):
        """
        Need to figure out the actual game workflow now
        So first we deal, then we have a betting round,
        need to keep track of blind tokens for betting,
        then we'll put cards on the table and go back to
        betting rounds. At the end we'll need to know how
        to determine the winner..
        """
        self.d.shuffle()
        self.blinds()
        for y in range(2):
            for x in self.table.seats:
                if x.isfilled():
                    self.d.deal(x.p)

    def blinds(self):
        if self.table.seatstaken() == 2:
            dealerblind = False
            for x in self.table.seats:
                if x.isfilled() and !dealerblind:
                    x.p.bet(self.table.bigblind)
                    self.table.pot.add(self.table.bigblind)
                    dealerblind = True
                elif x.isfilled():
                    x.p.bet(self.table.smallblind)
                    self.table.pot.add(self.table.smallblind)
        else:
        a = self.dealer
        for x in self.table.seats:
            if x.isfilled():
                a++
                if a == self.table.seatstaken():
                    a = 0
                if a == (self.dealer + 1) % self.table.seatstaken():
                    x.p.blind(self.table.smallblind)
                    self.table.pot.add(self.table.smallblind)
                elif a == (self.dealer + 2) % self.table.seatstaken():
                    x.p.blind(self.table.bigblind)
                    self.table.pot.add(self.table.bigblind)

    def betting(self):
        a = self.dealer
        for x in self.table.seats:
            if x.isfilled():
                print(f"Player {x.p.name}'s turn")
                a++
                if a == self.table.seatstaken():
                    a = 0
                if !x.p.hasbet:
                    if x.p.lastbet > 0: # Blinds
                        if self.table.pot.lastbet >= x.p.lastbet:
                            # Call, raise, or fold
                        else:
                            print(f"Player {x.p.name}'s last bet was "\
                                "more than the pot's last bet somehow\n"\
                                "Player's last bet: {x.p.lastbet}\n"\
                                "Last bet in pot: {self.table.pot.lastbet}")
                    elif self.table.pot.lastbet >= x.p.purse:
                        # All in or fold
                    elif self.table.pot.lastbet < x.p.purse:
                        # Call, raise, or fold
                        if x.p.bet(self.table.bigblind):
                            self.table.pot.add(self.table.bigblind)
                elif x.p.lastbet < self.table.pot.lastbet:
                    # Call, raise, or fold
                    diff = self.table.pot.lastbet - x.p.lastbet
                    if x.p.bet(diff):
                        self.table.pot.add(diff)
                else:
                    break

    def playerjoin(self, player):
        if self.table.seatsopen() > 0:
            self.table.sitdown(player)

    def playerleave(self, player):
        self.table.standup(player)

    def quit(self):
        quit()

class Seat:
    """A seat at the table"""

    def __init__(self):
        self.p = None

    def fill(self, player):
        self.p = player

    def isfilled(self):
        if self.p != None:
            return True
        return False

    def empty(self):
        self.p = None

class Table:
    """A table consisting of seats and a deck"""

    def __init__(self, name, deck, seats, smallblind, bigblind):
        self.name = name
        self.deck = deck
        self.seats = []
        for x in range(seats):
            self.seats.append(Seat())
        self.smallblind = smallblind
        self.bigblind = bigblind
        self.pot = Pot()

    def isready(self):
        a = 0
        for x in self.seats:
            a++ if x.isfilled()
        if a > 1:
            return True
        return False

    def seatstaken(self):
        a = 0
        for x in self.seats:
            a++ if x.isfilled()
        return a

    def seatsopen(self):
        a = 0
        for x in self.seats:
            a++ if x.isfilled()
        return len(self.seats) - a

    def sitdown(self, player):
        if self.seatsopen() > 0:
            for x in self.seats:
                if !x.isfilled():
                    x.fill(player)
                    break

    def standup(self, player):
        for x in self.seats:
            if x.p == player:
                x.empty()
                break

class Bet:
    """Players create bets"""

    def __init__(self, amount, pot):
        self.amount = amount

class Pot:
    """The Pot is the total bets this hand"""

    def __init__(self):
        self.pot = 0
        self.lastbet = 0

    def add(self, amount):
        self.pot += amount
        self.lastbet = amount
