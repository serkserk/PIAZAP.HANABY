#!/usr/bin/python
#-*- coding: utf-8 -*-
from deck import *
from table import *
from player import *


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
        Hanabi.initPlayers()

        turn = 0
        while(cls.table.strikesLeft() and (not cls.deck.empty() or turn % len(cls.players) != 0)):
            currentPlayer = cls.players[turn % len(cls.players)]
            cls.table.display(cls.players, turn % len(cls.players))
            currentPlayer.promptAction(cls.players)
            turn += 1
            print("Current score : ", cls.table.getScore())
            print()

        print("Final score : ", cls.table.getScore())

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
        print("Human(1) or random(2)? ", end='')
        playerType = input()
        return int(playerType)

    @classmethod
    def promptHandSize(cls):
        print("Hand size : ", end='')
        handSize = input()
        return int(handSize)

    @classmethod
    def promptPlayers(cls):
        print("How many players? ", end='')
        playersNumber = input()
        return int(playersNumber)


if __name__ == '__main__':
    Hanabi.main()
