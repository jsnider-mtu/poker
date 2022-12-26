#!/usr/bin/python3
"""The Deck and Card classes"""

import random

class Card:
    """A card has a face value and a suit."""

    def __init__(self, suit, value):
        assert suit in ['Hearts', 'Clubs', 'Diamonds', 'Spades']
        assert value in range(2,15)
        self.vdict = {14: 'Ace', 11: 'Jack', 12: 'Queen', 13: 'King'}
        self.suit = suit
        self.value = self.vdict.get(value, value)

    def __repr__(self):
        return f"{self.value} of {self.suit}"

class Deck:
    """A deck is a collection of cards"""

    def __init__(self):
        """Create a deck (unshuffled)"""
        self.deck = [Card(s, v) for s in ['Hearts', 'Clubs', 'Diamonds', 'Spades'] for v in range(2, 15)]

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

    def __repr__(self):
        return f"a {self.cards[0]} and a {self.cards[1]}"

    def add(self, card):
        if len(self.cards) >= 2:
            print(f"{self.playername}'s hand is already full")
        else:
            self.cards.append(card)

    def fold(self):
        self.cards = []

class Community:
    """Community cards are the 5 shared cards dealt in 3 phases"""

    def __init__(self):
        self.flopcards = []
        self.turncard = None
        self.rivercard = None

    def flop(self, deck):
        deck.deck.pop(0)
        self.flopcards = []
        for x in range(3):
            self.flopcards.append(deck.deck.pop(0))

    def turn(self, deck):
        deck.deck.pop(0)
        self.turncard = deck.deck.pop(0)

    def river(self, deck):
        deck.deck.pop(0)
        self.rivercard = deck.deck.pop(0)

    def cards(self):
        msg = "On the table:"
        for x in self.flopcards:
            msg += f" {x};"
        if self.turncard:
            msg += f" {self.turncard};"
        if self.rivercard:
            msg += f" {self.rivercard};"
        return msg

    def clean(self):
        self.flopcards = []
        self.turncard = None
        self.rivercard = None
