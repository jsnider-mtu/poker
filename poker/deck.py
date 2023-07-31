#!/usr/bin/python3
"""
The Deck and Card classes
"""
import random


class Card:
    """A card has a face value and a suit."""

    def __init__(self, suit, value):
        assert suit in ["Hearts", "Clubs", "Diamonds", "Spades"]
        assert value in range(2, 15)
        self.vdict = {14: "Ace", 11: "Jack", 12: "Queen", 13: "King"}
        self.suit = suit
        self.value = self.vdict.get(value, value)

    def __repr__(self):
        return f"{self.value} of {self.suit}"


class Deck:
    """A deck is a collection of cards"""

    def __init__(self):
        """Create a deck (unshuffled)"""
        self.deck = [
            Card(suit, value)
            for suit in ["Hearts", "Clubs", "Diamonds", "Spades"]
            for value in range(2, 15)
        ]

    def shuffle(self):
        """Shuffle the deck some number of times between 1 and 6"""
        for _ in range(random.randint(1, 6)):
            random.shuffle(self.deck)

    def deal(self, player):
        """Deal one card from the top of the deck"""
        player.hand.add(self.deck.pop(0))


class Hand:
    """A hand is two cards dealt from the Deck"""

    def __init__(self, player_name):
        self.cards = []
        self.player_name = player_name

    def __repr__(self):
        return f"a {self.cards[0]} and a {self.cards[1]}"

    def add(self, card):
        if len(self.cards) >= 2:
            print(f"{self.player_name}'s hand is already full")
        else:
            self.cards.append(card)

    def fold(self):
        self.cards = []


class Community:
    """Community cards are the 5 shared cards dealt in 3 phases"""

    def __init__(self):
        self.flop_cards = []
        self.turn_card = None
        self.river_card = None

    def flop(self, deck):
        deck.deck.pop(0)
        self.flop_cards = []
        for x in range(3):
            self.flop_cards.append(deck.deck.pop(0))

    def turn(self, deck):
        deck.deck.pop(0)
        self.turn_card = deck.deck.pop(0)

    def river(self, deck):
        deck.deck.pop(0)
        self.river_card = deck.deck.pop(0)

    def cards(self):
        msg = "On the table:"
        for x in self.flop_cards:
            msg += f" {x};"
        if self.turn_card:
            msg += f" {self.turn_card};"
        if self.river_card:
            msg += f" {self.river_card};"
        return msg

    def clean(self):
        self.flop_cards = []
        self.turn_card = None
        self.river_card = None
