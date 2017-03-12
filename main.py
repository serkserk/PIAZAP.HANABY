#!/usr/bin/python
#-*- coding: utf-8 -*-
from hanabi import Hanabi
from bcolor import Bcolor
import colorama
import sys
from statistics import median, mean


def main():
    """ main function. contains the game loop.
    """
    colorama.init()
    print(Bcolor.CLEAR)    # clear the screen

    print(colorama.Fore.LIGHTBLUE_EX + "How many iteration? " + Bcolor.END, end='')
    iteration = int(input())
    nbite = iteration

    nbPlayer = Hanabi.promptPlayers()
    nbHand = Hanabi.promptHandSize()
    playerTypeArray = []
    for i in range(nbPlayer):
        playerTypeArray.append(Hanabi.promptPlayerType())
    scoreArray = []

    while not iteration == 0:
        Hanabi.initPlayers(nbPlayer, nbHand, playerTypeArray)
        print()
        print()
        turn = 0
        while(Hanabi.table.strikesLeft() and (not Hanabi.deck.empty() or turn % len(Hanabi.players) != 0) and Hanabi.table.getScore() < 25):
            currentPlayer = Hanabi.players[turn % len(Hanabi.players)]
            Hanabi.table.display(Hanabi.players, turn % len(Hanabi.players))
            currentPlayer.promptAction(Hanabi.players)
            turn += 1
            print("Score after play: ", Hanabi.table.getScore())
            print()
        print("Final score: ", Hanabi.table.getScore(), " in ", turn, " turn !")
        print()

        scoreArray.append(Hanabi.table.getScore())
        print("Score from ", nbite, " iteration: ", scoreArray)
        iteration -= 1

    print("mean: ", mean(scoreArray))
    print("median:", median(scoreArray))


if __name__ == '__main__':
    # inputs can be set to be read from a file with a command line argument containing the name of the file
    if len(sys.argv) == 2:
        sys.stdin = open(sys.argv[1])
    main()
