#!/usr/bin/python3
"""The Deck and Card classes"""

import random

class Card:
    """A card has a face value and a suit."""

    def __init__(self, suit, value):
        assert suit in ['Hearts', 'Clubs', 'Diamonds', 'Spades']
        assert value in range(1,14)
        self.vdict = {1: 'Ace', 11: 'Jack', 12: 'Queen', 13: 'King'}
        self.suit = suit
        self.value = self.vdict.get(value, value)

    def __repr__(self):
        return f"{self.value} of {self.suit}"

class Deck:
    """A deck is a collection of cards"""

    def __init__(self, suits=[], valueRange=14):
        """Create a deck (unshuffled)"""
        self.deck = [Card(s, v) for s in suits for v in range(1,
                                                        valueRange)]

    def shuffle(self):
        """Shuffle the deck some number of times between 1 and 6"""
        for i in range(random.randint(1,6)):
            random.shuffle(self.deck)

    def deal(self, player):
        """Deal one card from the top of the deck"""
        player.hand.add(self.deck.pop(0))

class Hand:
    """A hand is two cards dealt from the Deck"""

    def __init__(self, playername):
        self.cards = []
        self.playername = playername

    def add(self, card):
        if len(self.cards) >= 2:
            print(f"{playername}'s hand is already full")
        else:
            self.cards.append(card)

    def fold(self):
        self.cards = []

class Community:
    """Community cards are the 5 shared cards dealt in 3 phases"""

    def __init__(self):
        self.flop = None
        self.turn = None
        self.river = None

    def flop(self, deck):
        deck.pop(0)
        self.flop = []
        for x in range(3):
            self.flop.append(deck.pop(0))

    def turn(self, deck):
        deck.pop(0)
        self.turn = deck.pop(0)

    def river(self, deck):
        deck.pop(0)
        self.river = deck.pop(0)
