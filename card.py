#!/usr/bin/python
#-*- coding: utf-8 -*-
from suit import *


class Card:
    def __init__(self, suit=Suit.unknown, value=0):
        self.value = value
        self.suit = suit

    def getSuit(self):
        return self.suit

    def getValue(self):
        return self.value

    def setSuit(self, suit):
        self.suit = suit

    def setValue(self, value):
        self.value = value

    def toString(self):
        return Suit.toString(self.suit) + " " + str(self.value)
