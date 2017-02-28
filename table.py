#!/usr/bin/python
#-*- coding: utf-8 -*-
from suit import *


class Table:
    def __init__(self):
        self.field = {}
        for s in Suit.trueValues():
            self.field[s] = 0
        self.hints = 8
        self.strikes = 3

    def place(self, c):
        if self.field[c.getSuit()] == c.getValue() - 1:
            self.field[c.getSuit()] = self.field[c.getSuit()] + 1
        else:
            self.strikes -= 1

    def useHint(self):
        self.hints = self.hints - 1

    def rechargeHint(self):
        if self.hints < 8:
            self.hints = self.hints + 1

    def hintsLeft(self):
        return self.hints > 0

    def strikesLeft(self):
        return self.strikes > 0

    def display(self, players, currentPlayerIndex):
        print("Hints :\t", self.hints)
        print("Strikes :\t", self.strikes)
        self.displayField()
        for player in players:
            if player == players[currentPlayerIndex]:
                player.displayKnownHand()
            else:
                player.displayHand()

    def displayField(self):
        print("Field :")
        for s, v in self.field.items():
            print(s, v, end="\t")
        print()

    def getScore(self):
        return sum(self.field.values())
