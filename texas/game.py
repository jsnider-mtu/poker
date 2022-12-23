#!/usr/bin/python3
"""
Texas Hold'Em
"""
from deck import *
from player import *

class Game:
    """Configures the table and calculates the winner or each hand"""

    def __init__(self, name):
        self.name = name
        self.suits = ['Hearts', 'Clubs', 'Diamonds', 'Spades']
        self.d = Deck(self.suits)
        self.table = Table(self.name, self.d, 8, 1, 2)
        self.dealer = 0
        self.playerturn = 3

    def __repr__(self):
        return f"Table: {self.table.name} has {len(self.table.seats)} seats, {self.table.seatstaken()} of which are taken"

    def calculatewinners(self):
        """Determine a winner"""
        combos = [[1, 2, 3, 4, 6],
                [1, 2, 3, 4, 7],
                [1, 2, 3, 5, 6],
                [1, 2, 3, 5, 7],
                [1, 2, 3, 6, 7],
                [1, 2, 4, 5, 6],
                [1, 2, 4, 5, 7],
                [1, 2, 4, 6, 7],
                [1, 2, 5, 6, 7],
                [1, 3, 4, 5, 6],
                [1, 3, 4, 5, 7],
                [1, 3, 4, 6, 7],
                [1, 3, 5, 6, 7],
                [1, 4, 5, 6, 7],
                [2, 3, 4, 5, 6],
                [2, 3, 4, 5, 7],
                [2, 3, 4, 6, 7],
                [2, 3, 5, 6, 7],
                [2, 4, 5, 6, 7],
                [3, 4, 5, 6, 7]]
        finalists = []
        finalscoredict = {}
        finalhandsdict = {}
        for x in self.table.seats:
            if x.isfilled():
                if !x.justsat and !x.p.folded:
                    finalists.append(x.p)
        communityscore = self.scorehand([x for x in self.table.comm.flopcards]+
                                [self.table.comm.turncard]+[self.table.comm.rivercard])
        for f in finalists:
            pile = set()
            for y in self.table.comm.flopcards:
                pile.append(y)
            pile.append(self.table.comm.turncard)
            pile.append(self.table.comm.rivercard)
            for y in f.hand.cards:
                pile.append(y)
            hand = []
            maxscore = communityscore
            maxhand = [x for x in self.table.comm.flopcards]+[self.table.comm.turncard]+
                    [self.table.comm.rivercard]
            for z in combos:
                for a in z:
                    hand.append(pile[a])
                score = self.scorehand(hand)
                if score > maxscore:
                    maxscore = score
                    maxhand = hand
            finalscoredict[f.name] = maxscore
            finalhandsdict[f.name] = maxhand
        winners = []
        highestscore = 0
        for k, v in finalscoredict.items():
            if v == highestscore:
                winners.append(k)
            elif v > highestscore:
                winners = [k]
                highestscore = v
        return winners, finalhandsdict

    def scorehand(self, cards):
        """Check for each hand type from top to bottom"""
        valuesdict = {}
        for x in cards:
            try:
                valuesdict[x.value] += 1
            except KeyError:
                valuesdict[x.value] = 1
        flush = cards[0].suit == cards[1].suit == cards[2].suit == cards[3].suit == cards[4].suit
        maxval = 2
        minval = 14
        pair = False
        twopair = False
        threeofakind = False
        fourofakind = False
        straight = True
        fullhouse = True
        for k, v in valuesdict.items():
            if k > maxval:
                maxval = k
            if k < minval:
                minval = k
            if v != 1:
                straight = False
            if v != 3 and v != 2:
                fullhouse = False
            if v == 2:
                if pair:
                    twopair = True
                    twopairval = k
                else:
                    pair = True
                    pairval = k
            if v == 3:
                threeofakind = True
                threeofakindval = k
            if v == 4:
                fourofakind = True
                fourofakindval = k
        if straight:
            if maxval - minval != 4:
                straight = False
        if straight and flush:
            score = 8192 + maxval
        elif fourofakind:
            score = 4096 + fourofakindval
            for k in valuesdict.keys():
                if k != fourofakindval:
                    score += k
        elif fullhouse:
            score = 2048
            for k, v in valuesdict.items():
                if v == 3:
                    score += k*2
                else:
                    score += k
        elif flush:
            score = 1024
            for k in valuesdict.keys():
                score += k
        elif straight:
            score = 512 + maxval
        elif threeofakind:
            score = 256 + threeofakindval
            for k in valuesdict.keys():
                score += k
        elif twopair:
            score = 128 + twopairval + pairval
            for k, v in valuesdict.items():
                if v == 1:
                    score += k
        elif pair:
            score = 64 + pairval
            for k, v in valuesdict.items():
                if v == 1:
                    score += k
        else:
            score = 0
            for k in valuesdict.keys():
                score += k
        return score

    def blinds(self):
        msg = ""
        a = self.dealer
        for x in self.table.seats:
            if x.isfilled():
                if !x.justsat:
                    a++
                    if a == self.table.seatstaken():
                        a = 0
                    if a == (self.dealer + 1) % self.table.seatstaken():
                        x.p.blind(self.table.smallblind)
                        self.table.pot.add(self.table.smallblind)
                        msg += f"{x.p.name} puts in the small blind ${self.table.smallblind}\n"
                    elif a == (self.dealer + 2) % self.table.seatstaken():
                        x.p.blind(self.table.bigblind)
                        self.table.pot.add(self.table.bigblind)
                        msg += f"{x.p.name} puts in the big blind ${self.table.bigblind}\n"
        return msg

    def playerjoin(self, player):
        if self.table.seatsopen() > 0:
            self.table.sitdown(player)
            return True
        else:
            print("Table's full")
            return False

    def playerleave(self, player):
        self.table.standup(player)
        return True

class Seat:
    """A seat at the table"""

    def __init__(self):
        self.p = None
        self.justsat = True

    def __repr__(self):
        return f"{self.p.name if self.isfilled() else 'Nobody'} is sitting in this seat"

    def fill(self, player):
        self.p = player
        self.justsat = True

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
        self.comm = Community()
        self.seats = set()
        for x in range(seats):
            self.seats.append(Seat())
        self.smallblind = smallblind
        self.bigblind = bigblind
        self.pot = Pot()

    def isready(self):
        a = self.seatstaken()
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

    def inplay(self):
        a = 0
        for x in self.seats:
            if x.isfilled():
                a++ if !x.justsat
        return a

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

class Pot:
    """The Pot is the total bets this hand"""

    def __init__(self):
        self.pot = 0
        self.lastbet = 0

    def add(self, amount, diff):
        self.pot += diff
        self.lastbet = amount