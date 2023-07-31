#!/usr/bin/python3

from player import *
from game import *


def test_game():
    p = Player("josh")
    q = Player("joey")
    g = Game(p)
    g.playerJoin(q)
    g.deal()
    assert len(g.players[0].hand) == 2
    assert len(g.players[1].hand) == 2
