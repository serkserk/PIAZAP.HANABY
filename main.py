from hanabi import Hanabi
from bcolor import Bcolor
import colorama
import sys


def main():
        colorama.init()
        print(Bcolor.CLEAR)    # clear the screen

        Hanabi.initPlayers()
        print()
        print()

        turn = 0
        while(Hanabi.table.strikesLeft() and (not Hanabi.deck.empty() or turn % len(Hanabi.players) != 0)):
            currentPlayer = Hanabi.players[turn % len(Hanabi.players)]
            Hanabi.table.display(Hanabi.players, turn % len(Hanabi.players))
            currentPlayer.promptAction(Hanabi.players)
            turn += 1
            print("Score after play: ", Hanabi.table.getScore())
            print()

        print("Final score: ", Hanabi.table.getScore())


if __name__ == '__main__':
    if len(sys.argv) == 2:
        sys.stdin = open(sys.argv[1])
    main()
