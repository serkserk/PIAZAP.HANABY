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
    def main(cls):

        colorama.init()
        print(bcolor.CLEAR)    # clear the screen

        Hanabi.initPlayers()
        print()
        print()

        turn = 0
        while(cls.table.strikesLeft() and (not cls.deck.empty() or turn % len(cls.players) != 0)):
            currentPlayer = cls.players[turn % len(cls.players)]
            cls.table.display(cls.players, turn % len(cls.players))
            currentPlayer.promptAction(cls.players)
            turn += 1
            print("Score after play: ", cls.table.getScore())
            print()

        print("Final score: ", cls.table.getScore())

    @classmethod
    def initPlayers(cls):
        playerType = Hanabi.promptPlayerType()
        playersNumber = Hanabi.promptPlayers()
        handSize = Hanabi.promptHandSize()
        if playerType == 1:
            for i in range(playersNumber):
                cls.players.append(Player(handSize, cls.table))
                cls.players[i].drawFrom(cls.deck)
        elif playerType == 2:
            for i in range(playersNumber):
                cls.players.append(PlayerRandom(handSize, cls.table))
                cls.players[i].drawFrom(cls.deck)

    @classmethod
    def promptPlayerType(cls):
        print(colorama.Fore.LIGHTBLUE_EX + "Human(1) or random(2)? " + bcolor.END, end='')
        playerType = input()
        return int(playerType)

    @classmethod
    def promptHandSize(cls):
        print(colorama.Fore.LIGHTBLUE_EX + "Hand size : " + bcolor.END, end='')
        handSize = input()
        return int(handSize)

    @classmethod
    def promptPlayers(cls):
        print(colorama.Fore.LIGHTBLUE_EX + "How many players? " + bcolor.END, end='')
        playersNumber = input()
        return int(playersNumber)


if __name__ == '__main__':
    Hanabi.main()
