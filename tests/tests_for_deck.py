#!/usr/bin/python3
from texas.deck import *

def test_Hand():
    handt = Hand()
    handt = handt + Card(1, 'Hearts')
    handt.append(Card(2, 'Hearts'))
    print(handt)
    try:
        handt.append(list(2, 'Hearts'))
    except:
        assert len(handt) == 2

#def test_Deck():
