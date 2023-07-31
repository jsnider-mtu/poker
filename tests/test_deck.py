#!/usr/bin/python3

from deck import *


def test_deck():
    d = Deck(["Hearts", "Diamonds", "Spades", "Clubs"], 14)
    assert len(d.deck) == 52
    assert isinstance(d.deck[0], Card)
