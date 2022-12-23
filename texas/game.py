#!/usr/bin/python3
"""
Texas Hold'Em
"""
from . import deck, player

class Game:
    """Configures the table and calculates the winner or each hand"""

    def __init__(self, name):
        self.name = name
        self.suits = ['Hearts', 'Clubs', 'Diamonds', 'Spades']
        self.d = deck.Deck(self.suits)
        self.table = Table(self.name, self.d, 8, 1, 2)
        self.dealer = 0
        self.playerturn = 3
        self.running = False

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
                if x.justsat == False and x.p.folded == False:
                    finalists.append(x.p)
        communityscore = self.scorehand([x for x in self.table.comm.flopcards]+
                                [self.table.comm.turncard]+[self.table.comm.rivercard])
        for f in finalists:
            pile = []
            for y in self.table.comm.flopcards:
                pile.append(y)
            pile.append(self.table.comm.turncard)
            pile.append(self.table.comm.rivercard)
            for y in f.hand.cards:
                pile.append(y)
            maxscore = communityscore
            maxhand = [x for x in self.table.comm.flopcards]+[self.table.comm.turncard]+[self.table.comm.rivercard]
            for z in combos:
                hand = []
                for a in z:
                    hand.append(pile[a - 1])
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
        vdict = {'Ace': 14, 'Jack': 11, 'Queen': 12, 'King': 13}
        valuesdict = {}
        for x in cards:
            realval = vdict.get(x.value, x.value)
            try:
                valuesdict[realval] += 1
            except KeyError:
                valuesdict[realval] = 1
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
            if int(k) > maxval:
                maxval = int(k)
            if int(k) < minval:
                minval = int(k)
            if v != 1:
                straight = False
            if v != 3 and v != 2:
                fullhouse = False
            if v == 2:
                if pair:
                    twopair = True
                    twopairval = int(k)
                else:
                    pair = True
                    pairval = int(k)
            if v == 3:
                threeofakind = True
                threeofakindval = int(k)
            if v == 4:
                fourofakind = True
                fourofakindval = int(k)
        if straight:
            if maxval - minval != 4:
                straight = False
        if straight and flush:
            score = 8192 + maxval
        elif fourofakind:
            score = 4096 + fourofakindval
            for k in valuesdict.keys():
                if k != fourofakindval:
                    score += int(k)
        elif fullhouse:
            score = 2048
            for k, v in valuesdict.items():
                if v == 3:
                    score += int(k)*2
                else:
                    score += int(k)
        elif flush:
            score = 1024
            for k in valuesdict.keys():
                score += int(k)
        elif straight:
            score = 512 + maxval
        elif threeofakind:
            score = 256 + threeofakindval
            for k in valuesdict.keys():
                score += int(k)
        elif twopair:
            score = 128 + twopairval + pairval
            for k, v in valuesdict.items():
                if v == 1:
                    score += int(k)
        elif pair:
            score = 64 + pairval
            for k, v in valuesdict.items():
                if v == 1:
                    score += int(k)
        else:
            score = 0
            for k in valuesdict.keys():
                score += int(k)
        return score

    def blinds(self):
        msg = ""
        small = ((self.dealer % self.table.inplay()) + 1) % self.table.inplay()
        big = ((self.dealer % self.table.inplay()) + 2) % self.table.inplay()
        c = -1
        for x in self.table.seats:
            if x.isfilled():
                if x.justsat == False:
                    c += 1
                    if c == small:
                        x.p.blind(self.table.smallblind)
                        self.table.pot.add(self.table.smallblind, self.table.smallblind)
                        msg += f"{x.p.name} puts in the small blind ${self.table.smallblind}\n"
                    elif c == big:
                        x.p.blind(self.table.bigblind)
                        self.table.pot.add(self.table.bigblind, self.table.bigblind)
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

    def __init__(self, name, deckk, seats, smallblind, bigblind):
        self.name = name
        self.deck = deckk
        self.comm = deck.Community()
        self.seats = []
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
            if x.isfilled():
                a += 1
        return a

    def seatsopen(self):
        a = 0
        for x in self.seats:
            if x.isfilled():
                a += 1
        return len(self.seats) - a

    def inplay(self):
        a = 0
        for x in self.seats:
            if x.isfilled():
                if x.justsat == False and x.p.folded == False:
                    a += 1
        return a

    def sitdown(self, player):
        if self.seatsopen() > 0:
            for x in self.seats:
                if x.isfilled() == False:
                    x.fill(player)
                    break

    def standup(self, player):
        for x in self.seats:
            if x.p == player:
                x.empty()
                break

    def clean(self):
        self.pot.clean()
        for x in self.seats:
            if x.isfilled():
                x.p.turn = False
                x.p.lastbet = 0
                x.p.hasbet = False
                x.p.minbet = 0

    def deepclean(self):
        self.pot.clean()
        for x in self.seats:
            if x.isfilled():
                x.p.hand.fold()
                x.p.turn = False
                x.p.lastbet = 0
                x.p.hasbet = False
                x.p.minbet = 0

class Pot:
    """The Pot is the total bets this hand"""

    def __init__(self):
        self.pot = 0
        self.lastbet = 0

    def add(self, amount, diff):
        self.pot += diff
        if amount > self.lastbet:
            self.lastbet = amount

    def clean(self):
        self.lastbet = 0
