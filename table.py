#!/usr/bin/python
#-*- coding: utf-8 -*-
from suit import *
import hanabi
import colorama
from bcolor import *


class Table:
    def __init__(self):
        self.field = [0 for i in range(5)]
        self.discarded = []
        self.hints = 8
        self.strikes = 3
        self.discardedDict = {'w1': 0, 'w2': 0, 'w3': 0, 'w4': 0, 'w5': 0,
                              'b1': 0, 'b2': 0, 'b3': 0, 'b4': 0, 'b5': 0,
                              'r1': 0, 'r2': 0, 'r3': 0, 'r4': 0, 'r5': 0,
                              'g1': 0, 'g2': 0, 'g3': 0, 'g4': 0, 'g5': 0,
                              'y1': 0, 'y2': 0, 'y3': 0, 'y4': 0, 'y5': 0, }

    def place(self, c):
        if self.field[Suit.toInt(c.getSuit()) - 1] == c.getValue() - 1:
            self.field[Suit.toInt(c.getSuit()) - 1] += 1
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
        print("Cards left in deck : ", hanabi.Hanabi.deck.cardsLeft())
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
        for i in range(len(self.field)):
            currentSuit = Suit(i + 1)
            print(Bcolor.BOLD + Suit.toColor(currentSuit) + "\t" + str(currentSuit), self.field[i], end="\t" + Bcolor.END)
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
        return sum(self.field)

    def cardPlayable(self, card):
        return self.field[Suit.toInt(card.getSuit()) - 1] == card.getValue() - 1

    def cardDiscardable(self, card):
        if card.getValue() <= self.field[Suit.toInt(card.getSuit()) - 1]:
            print("Dead card")
            return True

        cardAttr = ""
        if Suit.toString(card.getSuit()) == "white":
            cardAttr = "w"
        elif Suit.toString(card.getSuit()) == "blue":
            cardAttr = "b"
        elif Suit.toString(card.getSuit()) == "red":
            cardAttr = "r"
        elif Suit.toString(card.getSuit()) == "green":
            cardAttr = "g"
        elif Suit.toString(card.getSuit()) == "yellow":
            cardAttr = "y"

        if card.getValue() == 1:
            cardAttr += "1"
        elif card.getValue() == 2:
            cardAttr += "2"
        elif card.getValue() == 3:
            cardAttr += "3"
        elif card.getValue() == 4:
            cardAttr += "4"
        elif card.getValue() == 5:
            cardAttr += "5"

        if card.getValue() == 1:
            if self.discardedDict[cardAttr] < 2:
                self.discardedDict[cardAttr] += 1
                print(3 - self.discardedDict[cardAttr], "card remaining for ", cardAttr)
                return True
        elif card.getValue() == 2 or card.getValue() == 3 or card.getValue() == 4:
            if self.discardedDict[cardAttr] < 1:
                self.discardedDict[cardAttr] += 1
                print(2 - self.discardedDict[cardAttr], "card remaining for ", cardAttr)
                return True
        elif card.getValue() == 5:
            if self.discardedDict[cardAttr] < 0:
                self.discardedDict[cardAttr] += 1
                print(1 - self.discardedDict[cardAttr], "card remaining for ", cardAttr)
                return True
        print("Useful card")
        return False
