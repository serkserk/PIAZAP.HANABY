#!/usr/bin/python
#-*- coding: utf-8 -*-
from hanabi import Hanabi
from bcolor import Bcolor
import colorama
import sys
import os


def main(net=None, inputFile=None):
    """ main function. contains the game loop.
        Args :
            - net : a neural network to train on the game that is about to be played (optional)
    """
    colorama.init()
    #print(Bcolor.CLEAR)    # clear the screen
    if inputFile is not None:
        inputFile = open(inputFile)
        sys.stdin = inputFile

    nbPlayer = Hanabi.promptPlayers()
    nbHand = Hanabi.promptHandSize()
    playerTypeArray = []
    for i in range(nbPlayer):
        playerTypeArray.append(Hanabi.promptPlayerType())

    Hanabi.initPlayers(nbPlayer, nbHand, playerTypeArray)
    print()
    print()
    turn = 0
    Hanabi.deck.sort()  # we may want the deck to be shuffled with a specific seed. Since the deck
    Hanabi.deck.shuffle()  # is already shuffled when the Hanabi class is loaded, we need to sort it first.
    while(Hanabi.table.strikesLeft() and (not Hanabi.deck.empty() or turn % len(Hanabi.players) != 0) and Hanabi.table.getScore() < 25):
        currentPlayer = Hanabi.players[turn % len(Hanabi.players)]
        Hanabi.table.display(Hanabi.players, turn % len(Hanabi.players))
        currentPlayer.promptAction(Hanabi.players, net)
        turn += 1
        print("Current score: ", Hanabi.table.getScore())
        print()

    print(Bcolor.BOLD + colorama.Fore.CYAN + "Final score: ", Hanabi.table.getScore(), " in ", turn, " turns !" + Bcolor.END)
    print()

    if inputFile is not None:
        sys.stdin = sys.__stdin__
        inputFile.close()


# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')


# Restore
def enablePrint():
    sys.stdout = sys.__stdout__
    colorama.init()


if __name__ == '__main__':
    # inputs can be set to be read from a file with a command line argument containing the name of the file
    if len(sys.argv) == 2:
        sys.stdin = open(sys.argv[1])
    main()
