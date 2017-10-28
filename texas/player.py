#!/usr/bin/python
"""
The player has a purse, an ante, and a hand

(Plus a name, UID, and some state flags)
"""

class Player:
    playerCnt = 0

    def __init__(self, name, purse=100):
        self.allIn = False
        self.name = name
        self.hand = []
        self.purse = purse
        self.ante = 0
        self.check = False
        self.fold = False
        self.uniq = Player.playerCnt
        self.seat = None
        Player.playerCnt += 1

    def __repr__(self):
        return 'Player {} is holding {}'.format(self.name, self.hand)

    def showHand(self):
        """
        Return a msg showing the player's state
        """
        msg = '\n'+self.name+' is holding '+' '.join(self.hand)
        msg += '\nTheir purse is currently: $'+str(self.purse)
        msg += '\nTheir ante is currently: $'+str(self.ante)
        return msg

    def blind(self, m):
        pass

    def check(self):
        pass

    def rais(self):
        pass

    def fold(self):
        pass

    def sit(self):
        """
        Take a seat at a table
        """
        pass
