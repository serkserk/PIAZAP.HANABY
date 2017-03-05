#!/usr/bin/python
#-*- coding: utf-8 -*-
from card import *
import hanabi
from random import randint
from bcolor import *
import colorama


class Player(object):
    def __init__(self, handSize):
        self.handCapacity = handSize
        self.hand = []
        self.knownHand = []

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
        hanabi.Hanabi.table.place(c)

    def discard(self, c):
        self.knownHand.remove(self.knownHand[self.hand.index(c)])
        self.hand.remove(c)
        hanabi.Hanabi.table.placeDiscard(c)
        hanabi.Hanabi.table.rechargeHint()

    def promptAction(self, players):
        # validAction is a boolean that loops on
        # the menu while the action is invalid
        validAction = False

        while not validAction:
            validAction = True
            print("--------------")
            print("What do you want to do? ", end='')
            answer = input()
            if answer == "play":
                print("which card? ", end='')
                answerCard = input()
                self.play(self.hand[int(answerCard)])
                self.drawFrom(hanabi.Hanabi.deck)
            elif answer == "hint":
                print("which player? ", end='')
                answerPlayer = input()
                target = players[int(answerPlayer)]
                if hanabi.Hanabi.table.hintsLeft() and target != self:
                    hanabi.Hanabi.table.useHint()
                    print("what type? (suit/value) ", end='')
                    answerHintType = input()
                    if answerHintType == "suit":
                        print("Which suit? ", end='')
                        answerSuit = input()
                        target.giveSuitHint(Suit.valueOf(answerSuit))
                    elif answerHintType == "value":
                        print("Which value? ", end='')
                        answerValue = input()
                        target.giveValueHint(int(answerValue))
                else:
                    validAction = False
            elif answer == "discard":
                print("Which card? ", end='')
                answerCard = input()
                self.discard(self.hand[int(answerCard)])
                self.drawFrom(hanabi.Hanabi.deck)
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


class PlayerRandom(Player):
    def __init__(self, handSize):
        Player.__init__(self, handSize)

    def promptAction(self, players):
        # validAction is a boolean that loops on
        # the menu while the action is invalid
        validAction = False
        randAction = randint(0, 1)

        while not validAction:
            validAction = True
            print("--------------")
            print("Choosing random play ")
            if randAction == 0:
                print(colorama.Fore.CYAN + "Playing..." + Bcolor.END)
                randCard = randint(0, self.handCapacity - 1)
                self.play(self.hand[randCard])
                self.drawFrom(hanabi.Hanabi.deck)
            elif randAction == 1:
                print(colorama.Fore.LIGHTMAGENTA_EX + "Discarding... " + Bcolor.END)
                randDiscard = randint(0, self.handCapacity - 1)
                self.discard(self.hand[randDiscard])
                self.drawFrom(hanabi.Hanabi.deck)
            else:
                validAction = False


class PlayerRandomPlus(Player):
    def __init__(self, handSize):
        Player.__init__(self, handSize)

    def promptAction(self, players):
        # validAction is a boolean that loops on
        # the menu while the action is invalid
        validAction = False

        while not validAction:
            randAction = randint(0, 1)
            validAction = True
            print("--------------")
            print("Choosing random play ")
            if randAction == 0:
                randCard = randint(0, self.handCapacity - 1)
                if not hanabi.Hanabi.table.cardPlayable(self.hand[randCard]):
                    validAction = False
                    print(colorama.Fore.CYAN + "Can't play..." + Bcolor.END)
                else:
                    print(colorama.Fore.CYAN + "Playing..." + Bcolor.END)
                    self.play(self.hand[randCard])
                    self.drawFrom(hanabi.Hanabi.deck)
            elif randAction == 1:
                print(colorama.Fore.LIGHTMAGENTA_EX + "Discarding... " + Bcolor.END)
                randDiscard = randint(0, self.handCapacity - 1)
                self.discard(self.hand[randDiscard])
                self.drawFrom(hanabi.Hanabi.deck)
            else:
                validAction = False


class PlayerRandomPlusPlus(Player):
    def __init__(self, handSize):
        Player.__init__(self, handSize)

    def promptAction(self, players):
        # validAction is a boolean that loops on
        # the menu while the action is invalid
        validAction = False

        while not validAction:
            randAction = randint(0, 1)
            validAction = True
            print("--------------")
            print("Choosing random play ")
            if randAction == 0:
                randCard = randint(0, self.handCapacity - 1)
                if not hanabi.Hanabi.table.cardPlayable(self.hand[randCard]):
                    validAction = False
                    print(colorama.Fore.CYAN + "Can't play..." + Bcolor.END)
                else:
                    print(colorama.Fore.CYAN + "Playing..." + Bcolor.END)
                    self.play(self.hand[randCard])
                    self.drawFrom(hanabi.Hanabi.deck)
            elif randAction == 1:
                randCard = randint(0, self.handCapacity - 1)
                if not hanabi.Hanabi.table.cardDiscardable(self.hand[randCard]):
                    pass
                randDiscard = randint(0, self.handCapacity - 1)
                print(colorama.Fore.LIGHTMAGENTA_EX + "Discarding... " + Bcolor.END)
                self.discard(self.hand[randDiscard])
                self.drawFrom(hanabi.Hanabi.deck)
            else:
                validAction = False
