#!/usr/bin/python
#-*- coding: utf-8 -*-

from enum import Enum
import colorama
import random


class Suit(Enum):
    white = 1
    red = 2
    blue = 3
    green = 4
    yellow = 5
    unknown = 6

    def randomColor():
        col = random.randint(1, 5)
        if col == 1:
            return "white"
        elif col == 2:
            return "red"
        elif col == 3:
            return "blue"
        elif col == 4:
            return "green"
        elif col == 5:
            return "yellow"
        else:
            return "unknown"

    def toColor(suit):
        if suit == Suit.white:
            return colorama.Fore.WHITE
        elif suit == Suit.red:
            return colorama.Fore.RED
        elif suit == Suit.blue:
            return colorama.Fore.BLUE
        elif suit == Suit.green:
            return colorama.Fore.GREEN
        elif suit == Suit.yellow:
            return colorama.Fore.YELLOW
        else:
            return colorama.Fore.WHITE

    @classmethod
    def valueOf(cls, string):
        if string == "white":
            return cls.white
        elif string == "red":
            return cls.red
        elif string == "blue":
            return cls.blue
        elif string == "green":
            return cls.green
        elif string == "yellow":
            return cls.yellow
        else:
            return cls.unknown

    @classmethod
    def toString(cls, suit):
        if suit == Suit.white:
            return "white"
        elif suit == Suit.red:
            return "red"
        elif suit == Suit.blue:
            return "blue"
        elif suit == Suit.green:
            return "green"
        elif suit == Suit.yellow:
            return "yellow"
        else:
            return "unknown"

    @classmethod
    def trueValues(cls):
        return [cls.white, cls.red, cls.blue, cls.green, cls.yellow]

    @classmethod
    def toInt(cls, suit):
        if suit == Suit.white or suit == "white":
            return 1
        elif suit == Suit.red or suit == "red":
            return 2
        elif suit == Suit.blue or suit == "blue":
            return 3
        elif suit == Suit.green or suit == "green":
            return 4
        elif suit == Suit.yellow or suit == "yellow":
            return 5
        else:
            return 6

    def __int__(self):
        Suit.toInt(self)

    def __str__(self):
        if self == Suit.white:
            return "white"
        elif self == Suit.red:
            return "red"
        elif self == Suit.blue:
            return "blue"
        elif self == Suit.green:
            return "green"
        elif self == Suit.yellow:
            return "yellow"
        else:
            return "unknown"
