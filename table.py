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
            print(colorama.Fore.LIGHTRED_EX + "You got 1 strike! " + Bcolor.END)

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
        print()

    def getScore(self):
        return sum(self.field.values())

    def cardPlayable(self, card):
        return self.field[card.getSuit()] == card.getValue() + 1

    def cardDiscardable(self, card):
        for dCard in self.discarded:
            if card.getValue() == 1:
                compt1 = 0
                for dCard in self.discarded:
                    if card.getSuit() == dCard.getSuit():
                        if compt1 == 2:
                            return False
                    else:
                        compt1 += 1
            elif card.getValue() == 2 or card.getValue() == 3 or card.getValue() == 4:
                compt234 = 0
                for dCard in self.discarded:
                    if card.getSuit() == dCard.getSuit():
                        if compt234 == 2:
                            return False
                        else:
                            compt234 += 1
            elif card.getValue() == 5:
                compt5 = 0
                for dCard in self.discarded:
                    if card.getSuit() == dCard.getSuit():
                        if compt5 == 1:
                            return False
                        else:
                            compt5 += 1
        return True
