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
    deck.shuffle()  # deck is shuffled here for code portability. Should be sorted if re-shuffled with a seed.
    table = Table()
    players = []

    @classmethod
    def initPlayers(cls, nbPlayer, nbHand, playerTypeArray):
        Hanabi.newGame()
        playersNumber = nbPlayer
        handSize = nbHand
        playersType = playerTypeArray
        for i in range(playersNumber):
            playerType = playersType[i]
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
    def newGame(cls):
        cls.deck = Deck()
        cls.deck.shuffle()
        cls.table = Table()
        cls.players = []

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
