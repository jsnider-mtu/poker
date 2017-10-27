#!/usr/bin/python3
"""The Deck class"""

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

class Hand(list):
    def __init__(self):
        """Create a collection of cards."""
        self.hand = []

    def __add__(self, card):
        assert isinstance(card, Card)
        self.hand.append(card)

class Deck(Hand):
    def __init__(self):
        """Create a deck (unshuffled)"""
        self.hand = []
        self.hand.append(Card(s, v) for s in ['Hearts', 'Clubs', 'Diamonds',
                                              'Spades'] for v in range(1,14))

    def shuffle(self):
        """Shuffle the deck some number of times between 1 and 6"""
        for i in range(random.randint(1,6)):
            random.shuffle(self.deck)
