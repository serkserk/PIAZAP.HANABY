#!/usr/bin/python
#-*- coding: utf-8 -*-
from card import *
from hanabi import Hanabi


class Player:
    def __init__(self, handSize, table):
        self.handCapacity = handSize
        self.hand = []
        self.knownHand = []
        Hanabi.table = table

    def drawFrom(self, deck):
        missingCards = self.handCapacity - len(self.hand)
        while (missingCards > 0):
            self.hand.append(deck.draw())
            self.knownHand.append(Card())
            missingCards -= 1

    def giveSuitHint(self, s):
        for card in self.hand:
            if card.getSuit() == s:
                self.knownHand[self.hand.index(card)].setSuit(s)

    def giveValueHint(self, value):
        for card in self.hand:
            if card.getValue() == value:
                self.knownHand[self.hand.index(card)].setValue(value)

    def play(self, c):
        self.knownHand.remove(self.knownHand[self.hand.index(c)])
        self.hand.remove(c)
        Hanabi.table.place(c)

    def discard(self, c):
        self.knownHand.remove(self.knownHand[self.hand.index(c)])
        self.hand.remove(c)
        Hanabi.table.rechargeHint()

    def promptAction(self, players):
        # validAction is a boolean that loops on
        # the menu while the action is invalid
        validAction = False

        while not validAction:
            validAction = True
            print("--------------")
            answer = input("What do you want to do? ")
            if answer == "play":
                self.play(self.hand[int(input("which card? "))])
                self.drawFrom(Hanabi.deck)
            elif answer == "hint":
                target = players[int(input("which player? "))]
                if Hanabi.table.hintsLeft() and target != self:
                    Hanabi.table.useHint()
                    hintType = input("what type? (suit/value) ")
                    if hintType == "suit":
                        target.giveSuitHint(Suit.valueOf(input("Which suit? ")))
                    elif hintType == "value":
                        target.giveValueHint(int(input("Which value? ")))
                else:
                    validAction = False
            elif answer == "discard":
                self.discard(self.hand[int(input("Which card? "))])
                self.drawFrom(Hanabi.deck)
            else:
                validAction = False

    def displayHand(self):
        for card in self.hand:
            print(card.toString(), end='  ')
        print()

    def displayKnownHand(self):
        print("> ", end='')
        self.displayHand()  # playing with complete information at the moment
        # for card in self.knownHand:
        #     print(card.toString(), end='  ')
        # print()

    def getHandCapacity(self):
        return self.handCapacity
