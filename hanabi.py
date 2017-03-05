#!/usr/bin/python
#-*- coding: utf-8 -*-
from deck import *
from table import *
from player import *
from bcolor import *
import colorama


class Hanabi:
    """
    Hanabi is the main class in the project.
    Static Attributes :
        deck (Deck) : the deck of cards in the game
        table (Table) : the table on which the game is played
        players (List<Player>) : the list of players
    """
    deck = Deck()
    deck.shuffle()
    table = Table()
    players = []

    def __init__(self):
        pass

    @classmethod
    def initPlayers(cls):
        playerType = Hanabi.promptPlayerType()
        playersNumber = Hanabi.promptPlayers()
        handSize = Hanabi.promptHandSize()
        if playerType == 1:
            for i in range(playersNumber):
                cls.players.append(Player(handSize))
                cls.players[i].drawFrom(cls.deck)
        elif playerType == 2:
            for i in range(playersNumber):
                cls.players.append(PlayerRandom(handSize))
                cls.players[i].drawFrom(cls.deck)
        elif playerType == 3:
            for i in range(playersNumber):
                cls.players.append(PlayerRandomPlus(handSize))
                cls.players[i].drawFrom(cls.deck)

    @classmethod
    def promptPlayerType(cls):
        print(colorama.Fore.LIGHTBLUE_EX + "Human(1), random(2) or randomPlus(3)? " + Bcolor.END, end='')
        playerType = input()
        return int(playerType)

    @classmethod
    def promptHandSize(cls):
        print(colorama.Fore.LIGHTBLUE_EX + "Hand size : " + Bcolor.END, end='')
        handSize = input()
        return int(handSize)

    @classmethod
    def promptPlayers(cls):
        print(colorama.Fore.LIGHTBLUE_EX + "How many players? " + Bcolor.END, end='')
        playersNumber = input()
        return int(playersNumber)
