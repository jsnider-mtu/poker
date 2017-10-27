#!/usr/bin/python3
"""
This file is for the Lobby class. It starts a particular game in
the current lobby.
"""
import game
import threading

class Lobby:
    """
    The lobby where players start after logging into the service.
    """

    def __init__(self, sock, gameType="Texas Hold'Em"):
        self.sock = sock
        self.gameType = gameType
        self.game_handler = threading.Thread(target=self.newGame,
                                            args=(self.gameType,))
        self.game_handler.start()

    def newGame(self, gameType):
        self.game = game.Game(gameType)
        self.game.begin()
