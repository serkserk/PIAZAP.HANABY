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
        playersNumber = Hanabi.promptPlayers()
        handSize = Hanabi.promptHandSize()
        for i in range(playersNumber):
            playerType = Hanabi.promptPlayerType()
            if playerType == 1:
                cls.players.append(Player(handSize))
            elif playerType == 2:
                cls.players.append(PlayerRandom(handSize))
            elif playerType == 3:
                cls.players.append(PlayerRandomPlus(handSize))
            elif playerType == 4:
                cls.players.append(PlayerRandomPlusPlus(handSize))
            cls.players[i].drawFrom(cls.deck)

    @classmethod
    def promptPlayerType(cls):
        print(colorama.Fore.LIGHTBLUE_EX + "Human(1), random(2), random+(3) or random++(4)? " + Bcolor.END, end='')
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
