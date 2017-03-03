#!/usr/bin/python
#-*- coding: utf-8 -*-
from suit import *
from bcolor import *


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
        return Suit.toColor(self.suit) + " " + Suit.toString(self.suit) + " " + str(self.value) + bcolor.END