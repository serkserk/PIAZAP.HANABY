#!/usr/bin/python
#-*- coding: utf-8 -*-
from suit import *
import colorama
from bcolor import *


class Table:
    def __init__(self):
        self.field = {}
        self.discarded = []
        for s in Suit.trueValues():
            self.field[s] = 0
        self.hints = 8
        self.strikes = 3

    def place(self, c):
        if self.field[c.getSuit()] == c.getValue() - 1:
            self.field[c.getSuit()] = self.field[c.getSuit()] + 1
        else:
            self.strikes -= 1
            print(colorama.Fore.LIGHTRED_EX + "You got 1 strike! " + bcolor.END)

    def placeDiscard(self, c):
        self.discarded.append(c)

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
        print("Hints : ", self.hints)
        print("Strikes : ", self.strikes)
        self.displayField()
        self.displayDiscarded()
        print("Hands:")
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

    def displayDiscarded(self):
        print("Discarded :")
        if len(self.discarded) == 0:
            print("*no discard yet*")
        else:
            for card in self.discarded:
                print(card.toString(), end="  ")

    def getScore(self):
        return sum(self.field.values())
