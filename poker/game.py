#!/usr/bin/python3
"""
Poker
"""
from . import deck, player


class Game:
    """Configures the table and calculates the winner or each hand"""

    def __init__(self, name, seats=8, small_blind=1, big_blind=2):
        self.name = name
        self.d = deck.Deck()
        self.table = Table(self.name, self.d, seats, small_blind, big_blind)
        self.dealer = 0
        self.player_turn = 3
        self.running = False
        self.last_turn = 0.0

    def __repr__(self):
        return f"Table: {self.table.name} has {len(self.table.seats)} seats, {self.table.seats_taken()} of which are taken"

    def calculatewinners(self):
        """Determine a winner"""
        combos = [
            [1, 2, 3, 4, 6],
            [1, 2, 3, 4, 7],
            [1, 2, 3, 5, 6],
            [1, 2, 3, 5, 7],
            [1, 2, 3, 6, 7],
            [1, 2, 4, 5, 6],
            [1, 2, 4, 5, 7],
            [1, 2, 4, 6, 7],
            [1, 2, 5, 6, 7],
            [1, 3, 4, 5, 6],
            [1, 3, 4, 5, 7],
            [1, 3, 4, 6, 7],
            [1, 3, 5, 6, 7],
            [1, 4, 5, 6, 7],
            [2, 3, 4, 5, 6],
            [2, 3, 4, 5, 7],
            [2, 3, 4, 6, 7],
            [2, 3, 5, 6, 7],
            [2, 4, 5, 6, 7],
            [3, 4, 5, 6, 7],
        ]
        finalists = []
        final_scores = {}
        final_hands = {}
        for x in self.table.seats:
            if x.is_filled():
                if x.just_sat == False and x.p.folded == False:
                    finalists.append(x.p)
        if len(finalists) == 1:
            return [x.name for x in finalists], {}
        community_score = self.score_hand(
            [x for x in self.table.comm.flop_cards]
            + [self.table.comm.turn_card]
            + [self.table.comm.river_card]
        )
        for f in finalists:
            pile = []
            for y in self.table.comm.flop_cards:
                pile.append(y)
            pile.append(self.table.comm.turn_card)
            pile.append(self.table.comm.river_card)
            for y in f.hand.cards:
                pile.append(y)
            max_score = community_score
            max_hand = (
                [x for x in self.table.comm.flop_cards]
                + [self.table.comm.turn_card]
                + [self.table.comm.river_card]
            )
            for z in combos:
                hand = []
                for a in z:
                    hand.append(pile[a - 1])
                score = self.score_hand(hand)
                if score > max_score:
                    max_score = score
                    max_hand = hand
            final_scores[f.name] = max_score
            final_hands[f.name] = max_hand
        winners = []
        highest_score = 0
        for k, v in final_scores.items():
            if v == highest_score:
                winners.append(k)
            elif v > highest_score:
                winners = [k]
                highest_score = v
        return winners, final_hands

    def score_hand(self, cards):
        """Check for each hand type from top to bottom"""
        if None in cards:
            return 0
        vdict = {"Ace": 14, "Jack": 11, "Queen": 12, "King": 13}
        values = {}
        for x in cards:
            real_value = vdict.get(x.value, x.value)
            try:
                values[real_value] += 1
            except KeyError:
                values[real_value] = 1
        flush = (
            cards[0].suit
            == cards[1].suit
            == cards[2].suit
            == cards[3].suit
            == cards[4].suit
        )
        max_value = 2
        min_value = 14
        pair = False
        two_pair = False
        three_of_a_kind = False
        four_of_a_kind = False
        straight = True
        full_house = True
        for k, v in values.items():
            if int(k) > max_value:
                max_value = int(k)
            if int(k) < min_value:
                min_value = int(k)
            if v != 1:
                straight = False
            if v != 3 and v != 2:
                full_house = False
            if v == 2:
                if pair:
                    two_pair = True
                    two_pair_value = int(k)
                else:
                    pair = True
                    pair_value = int(k)
            if v == 3:
                three_of_a_kind = True
                three_of_a_kind_value = int(k)
            if v == 4:
                four_of_a_kind = True
                four_of_a_kind_value = int(k)
        if straight:
            if max_value - min_value != 4:
                if max_value == 14:
                    for x in ["2", "3", "4", "5"]:
                        if x not in values.keys():
                            straight = False
                else:
                    straight = False
        if straight and flush:
            score = 8192 + max_value
        elif four_of_a_kind:
            score = 4096 + four_of_a_kind_value
            for k in values.keys():
                if k != four_of_a_kind_value:
                    score += int(k)
        elif full_house:
            score = 2048
            for k, v in values.items():
                if v == 3:
                    score += int(k) * 2
                else:
                    score += int(k)
        elif flush:
            score = 1024
            for k in values.keys():
                score += int(k)
        elif straight:
            score = 512 + max_value
        elif three_of_a_kind:
            score = 256 + three_of_a_kind_value
            for k in values.keys():
                score += int(k)
        elif two_pair:
            score = 128 + two_pair_value + pair_value
            for k, v in values.items():
                if v == 1:
                    score += int(k)
        elif pair:
            score = 64 + pair_value
            for k, v in values.items():
                if v == 1:
                    score += int(k)
        else:
            score = 0
            for k in values.keys():
                score += int(k)
        return score

    def blinds(self):
        msg = ""
        small = ((self.dealer % self.table.in_play()) + 1) % self.table.in_play()
        big = ((self.dealer % self.table.in_play()) + 2) % self.table.in_play()
        c = -1
        for x in self.table.seats:
            if x.is_filled():
                if x.just_sat == False:
                    c += 1
                    if c == small:
                        x.p.blind(self.table.small_blind)
                        self.table.pot.add(self.table.small_blind, self.table.small_blind)
                        msg += f"{x.p.name} puts in the small blind ${self.table.small_blind}\n"
                    elif c == big:
                        x.p.blind(self.table.big_blind)
                        self.table.pot.add(self.table.big_blind, self.table.big_blind)
                        msg += (
                            f"{x.p.name} puts in the big blind ${self.table.big_blind}\n"
                        )
        return msg

    def player_join(self, player):
        if self.table.seats_open() > 0:
            self.table.sit_down(player)
            return True
        else:
            print("Table's full")
            return False

    def player_leave(self, player):
        self.table.stand_up(player)
        return True


class Seat:
    """A seat at the table"""

    def __init__(self):
        self.p = None
        self.just_sat = True

    def __repr__(self):
        return f"{self.p.name if self.is_filled() else 'Nobody'} is sitting in this seat"

    def fill(self, player):
        self.p = player
        self.just_sat = True

    def is_filled(self):
        if self.p != None:
            return True
        return False

    def empty(self):
        self.p = None


class Table:
    """A table consisting of seats and a deck"""

    def __init__(self, name, deckk, seats, small_blind, big_blind):
        self.name = name
        self.deck = deckk
        self.comm = deck.Community()
        self.seats = []
        for x in range(seats):
            self.seats.append(Seat())
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.pot = Pot()

    def is_ready(self):
        a = self.seats_taken()
        if a > 1:
            return True
        return False

    def seats_taken(self):
        a = 0
        for x in self.seats:
            if x.is_filled():
                a += 1
        return a

    def seats_open(self):
        a = 0
        for x in self.seats:
            if x.is_filled():
                a += 1
        return len(self.seats) - a

    def in_play(self):
        a = 0
        for x in self.seats:
            if x.is_filled():
                if x.just_sat == False and x.p.folded == False:
                    a += 1
        return a

    def sit_down(self, player):
        if self.seats_open() > 0:
            for x in self.seats:
                if x.is_filled() == False:
                    x.fill(player)
                    break

    def stand_up(self, player):
        for x in self.seats:
            if x.p == player:
                x.empty()
                break

    def clean(self):
        self.pot.clean()
        for x in self.seats:
            if x.is_filled():
                x.p.turn = False
                x.p.last_bet = 0
                x.p.has_bet = False
                x.p.min_bet = 0

    def deep_clean(self):
        self.pot.deep_clean()
        self.comm.clean()
        for x in self.seats:
            if x.is_filled():
                x.p.hand.fold()
                x.p.folded = False
                x.p.turn = False
                x.p.last_bet = 0
                x.p.has_bet = False
                x.p.min_bet = 0


class Pot:
    """The Pot is the total bets this hand"""

    def __init__(self):
        self.pot = 0
        self.last_bet = 0

    def add(self, amount, diff):
        self.pot += diff
        if amount > self.last_bet:
            self.last_bet = amount

    def clean(self):
        self.last_bet = 0

    def deep_clean(self):
        self.last_bet = 0
        self.pot = 0
