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
        return '{} of {}'.format(self.value, self.suit)

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
