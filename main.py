#!/usr/bin/python
#-*- coding: utf-8 -*-
from hanabi import Hanabi
from bcolor import Bcolor
import colorama
import os
import sys


def main(knowledgeBase=None, inputFile=None):
    """ main function. contains the game loop.
        Args :
            - knowledgeBase : a Knowledge Base to fill with examples (optional)
    """

    def numberOfTurnsLeft(player, lastTurn):
        return nPlayers - Hanabi.players.index(player)  # if lastTurn else nPlayers + 1

    colorama.init()
    print(Bcolor.CLEAR)    # clear the screen
    if inputFile is not None:
        inputFile = open(inputFile)
        sys.stdin = inputFile

    nPlayers = Hanabi.promptPlayers()
    nbHand = Hanabi.promptHandSize()
    playerTypeArray = []
    for i in range(nPlayers):
        playerTypeArray.append(Hanabi.promptPlayerType())

    Hanabi.initPlayers(nPlayers, nbHand, playerTypeArray)
    print()
    print()
    turn = 0
    Hanabi.deck.sort()  # we may want the deck to be shuffled with a specific seed. Since the deck
    Hanabi.deck.shuffle()  # is already shuffled when the Hanabi class is loaded, we need to sort it first.
    while(Hanabi.table.strikesLeft() and (not Hanabi.deck.empty()) and Hanabi.table.getScore() < 25):
        currentPlayer = Hanabi.players[turn % len(Hanabi.players)]
        Hanabi.table.display(Hanabi.players, turn % len(Hanabi.players))
        currentPlayer.promptAction(nTurnsLeft=numberOfTurnsLeft(currentPlayer, Hanabi.deck.empty()))
        turn += 1
        print("Current score: ", Hanabi.table.getScore())
        print()

    print(Bcolor.BOLD + colorama.Fore.CYAN + "Final score: ", Hanabi.table.getScore(), " in ", turn, " turns !" + Bcolor.END)
    print()

    if inputFile is not None:
        sys.stdin = sys.__stdin__
        inputFile.close()


def neuralNetAutoMain(neuralNet=None, model=None, nPlayers=3):
    """ This method is analogous to main() but is designed for training NeuralNet players.
        It could be fused with main(), but that would imply harmonizing many behaviours arbitrarily.
    """
    from player import PlayerNet
    Hanabi.newGame()
    Hanabi.deck.sort()
    Hanabi.deck.shuffle()
    if model is None:
        players = [PlayerNet(4, neuralNet=neuralNet) for _ in range(nPlayers)]
    else:
        players = [PlayerNet(4, model=model) for _ in range(nPlayers)]
    turn = 0

    def numberOfTurnsLeft(player, lastTurn):
        return nPlayers - players.index(player)  # if lastTurn else nPlayers + 1

    while(Hanabi.table.strikesLeft() and (not Hanabi.deck.empty()) and Hanabi.table.getScore() < 25):
        currentPlayer = players[turn % nPlayers]
        currentPlayer.promptAction(numberOfTurnsLeft(currentPlayer, Hanabi.deck.empty()))
        turn += 1

    log = []
    for player in players:
        log += player.log
    return log


def blockPrint():
    """ Redirect the output so we don't see printing.
    """
    sys.stdout = open(os.devnull, 'w')


def enablePrint():
    """ Restrore the output so we can see the printing.
    """
    sys.stdout = sys.__stdout__
    colorama.init()


if __name__ == '__main__':
    # inputs can be set to be read from a file with a command line argument containing the name of the file
    if len(sys.argv) == 2:
        sys.stdin = open(sys.argv[1])
    main()
