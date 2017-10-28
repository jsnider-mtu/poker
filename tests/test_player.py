#!/usr/bin/python3

from player import *

def test_player():
    p = Player('josh')
    q = Player('joey')
    assert p.name == 'josh'
    assert q.name == 'joey'
