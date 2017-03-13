#!/usr/bin/python
#-*- coding: utf-8 -*-

from enum import Enum
import colorama


class Suit(Enum):
    white = 1
    red = 2
    blue = 3
    green = 4
    yellow = 5
    unknown = 6

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
        if suit == Suit.white:
            return 1
        elif suit == Suit.red:
            return 2
        elif suit == Suit.blue:
            return 3
        elif suit == Suit.green:
            return 4
        elif suit == Suit.yellow:
            return 5
        else:
            return 6
