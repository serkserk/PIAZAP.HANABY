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
        return Suit.toColor(self.suit) + " " + Suit.toString(self.suit) + " " + str(self.value) + Bcolor.END

    def __int__(self):
        """ overload of int() for easy value comparisons
            1 <= Suit.toInt(self.suit) <= 6
            0 <= (Suit.toInt(self.suit) - 1) <= 5
            0 <= (Suit.toInt(self.suit) - 1) * 5 <= 25
            1 <= (Suit.toInt(self.suit) - 1) * 5 + self.value <= 30
            this stretches our nColors*nValues = 6*5 = 30 different types
            of cards over 30 different values, which allows us to order them
        """
        return (Suit.toInt(self.suit) - 1) * 5 + self.value

    def __lt__(self, other):
        """ Overload of the < operator for sorting
        """
        return int(self) < int(other)

    def __le__(self, other):
        """ Overload of the <= operator
        """
        return int(self) <= int(other)

    def __gt__(self, other):
        """ Overload of the > operator
        """
        return int(self) > int(other)

    def __ge__(self, other):
        """ Overload of the >= operator
        """
        return int(self) >= int(other)

    def __eq__(self, other):
        """ Overload of the == operator
        """
        return int(self) == int(other)

    def __ne__(self, other):
        """ Overload of the != operator
        """
        return int(self) != int(other)
