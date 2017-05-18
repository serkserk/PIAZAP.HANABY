#!/usr/bin/python
#-*- coding: utf-8 -*-
import colorama
import copy
import hanabi
import numpy as np

from bcolor import *
from card import *
from random import randint


class Player(object):
    """
    The basic human player.
    """

    def __init__(self, handSize):
        self.handCapacity = handSize
        self.hand = []
        self.knownHand = []

    def drawFrom(self, deck):
        missingCards = self.handCapacity - len(self.hand)
        while (missingCards > 0 and not deck.empty()):
            self.hand.append(deck.draw())
            self.knownHand.append(Card())
            missingCards -= 1

    def giveSuitHint(self, s):
        for card in self.hand:
            if card.getSuit() == s:
                self.knownHand[self.hand.index(card)].setSuit(s)

    def giveValueHint(self, value):
        for card in self.hand:
            if card.getValue() == value:
                self.knownHand[self.hand.index(card)].setValue(value)

    def play(self, c):
        self.knownHand.remove(self.knownHand[self.hand.index(c)])
        self.hand.remove(c)
        hanabi.Hanabi.table.place(c)

    def discard(self, c):
        self.knownHand.remove(self.knownHand[self.hand.index(c)])
        self.hand.remove(c)
        hanabi.Hanabi.table.discard(c)
        hanabi.Hanabi.table.rechargeHint()

    def promptAction(self, knowledgeBase=None, nTurnsLeft=0, players=None):
        """ This method prompts the player for action and carries said action out
        """
        # validAction is a boolean that loops on
        # the menu while the action is invalid
        validAction = False

        while not validAction:
            validAction = True
            print("--------------")
            print("What do you want to do? ", end='')
            answer = input()
            if answer == "play":
                print("which card? ", end='')
                answerCardId = input()  # the index of the card answered by the player
                answerCard = self.hand[int(answerCardId)]
                self.play(answerCard)
                self.drawFrom(hanabi.Hanabi.deck)
            elif answer == "hint":
                print("which player? ", end='')
                answerPlayer = input()
                target = players[int(answerPlayer)]
                if hanabi.Hanabi.table.hintsLeft() and target != self:
                    hanabi.Hanabi.table.useHint()
                    print("what type? (suit/value) ", end='')
                    answerHintType = input()
                    if answerHintType == "suit":
                        print("Which suit? ", end='')
                        answerSuit = input()
                        target.giveSuitHint(Suit.valueOf(answerSuit))
                    elif answerHintType == "value":
                        print("Which value? ", end='')
                        answerValue = input()
                        target.giveValueHint(int(answerValue))
                else:
                    validAction = False
            elif answer == "discard":
                print("Which card? ", end='')
                answerCard = input()
                self.discard(self.hand[int(answerCard)])
                self.drawFrom(hanabi.Hanabi.deck)
            else:
                validAction = False

    def displayHand(self):
        for card in self.hand:
            print(card.toString(), end='  ')
        print()

    def displayKnownHand(self):
        print("> ", end='')
        self.displayHand()  # playing with complete information at the moment
        # for card in self.knownHand:
        #     print(card.toString(), end='  ')
        # print()

    def getHandCapacity(self):
        return self.handCapacity


class PlayerRandom(Player):
    """
    Player that play randomly.
    """

    def __init__(self, handSize):
        Player.__init__(self, handSize)

    def promptAction(self, knowledgeBase=None, nTurnsLeft=0, players=None):
        # validAction is a boolean that loops on
        # the menu while the action is invalid
        validAction = False
        randAction = randint(0, 1)

        while not validAction:
            validAction = True
            print("--------------")
            print("Choosing random play ")
            if randAction == 0:
                print(colorama.Fore.CYAN + "Playing..." + Bcolor.END)
                randCard = randint(0, self.handCapacity - 1)
                self.play(self.hand[randCard])
                self.drawFrom(hanabi.Hanabi.deck)
            elif randAction == 1:
                print(colorama.Fore.LIGHTMAGENTA_EX + "Discarding... " + Bcolor.END)
                randDiscard = randint(0, self.handCapacity - 1)
                self.discard(self.hand[randDiscard])
                self.drawFrom(hanabi.Hanabi.deck)
            else:
                validAction = False


class PlayerRandomPlus(Player):
    """
    Player that try to play playable card.
    """

    def __init__(self, handSize):
        Player.__init__(self, handSize)

    def promptAction(self, knowledgeBase=None, nTurnsLeft=0, players=None):
        nbcard = 0  # index of current card
        print("--------------")
        print("Trying to play... ")
        for card in self.hand:
            if hanabi.Hanabi.table.cardPlayable(self.hand[nbcard]):
                self.play(self.hand[nbcard])
                self.drawFrom(hanabi.Hanabi.deck)
                print(colorama.Fore.CYAN + "Playing card: " + str(nbcard + 1) + Bcolor.END)
                return  # finish if played a  card
            print(colorama.Fore.CYAN + "Could not play card: " + str(nbcard + 1) + Bcolor.END)
            nbcard += 1
        randDiscard = randint(0, self.handCapacity - 1)
        print(colorama.Fore.LIGHTMAGENTA_EX + "Discarding random card: " + str(randDiscard + 1) + Bcolor.END)
        self.discard(self.hand[randDiscard])
        self.drawFrom(hanabi.Hanabi.deck)


class PlayerRandomPlusPlus(Player):
    """
    Player that try to play playable card and dicard correctly.
    """

    def __init__(self, handSize):
        Player.__init__(self, handSize)

    def promptAction(self, knowledgeBase=None, nTurnsLeft=0, players=None):
        nbcard = 0  # index of current card
        # print("--------------")
        # print("Trying to play... ")
        for card in self.hand:
            if knowledgeBase is not None:
                    example = list(hanabi.Hanabi.table.field)
                    example.append(Suit.toInt(self.hand[nbcard].getSuit()))
                    example.append(self.hand[nbcard].getValue())

            if hanabi.Hanabi.table.cardPlayable(self.hand[nbcard]):
                if knowledgeBase is not None:
                    knowledgeBase.append((example, [1]))
                self.play(self.hand[nbcard])
                self.drawFrom(hanabi.Hanabi.deck)
                # print(colorama.Fore.CYAN + "Playing card: " + str(nbcard + 1) + Bcolor.END)
                return  # finish if played a  card
            else:
                if knowledgeBase is not None:
                    knowledgeBase.append((example, [0]))
            # print(colorama.Fore.CYAN + "Could not play card: " + str(nbcard + 1) + Bcolor.END)
            nbcard += 1
        nbcard = 0
        for card in self.hand:
            if hanabi.Hanabi.table.cardDiscardable(self.hand[nbcard]):
                # print(colorama.Fore.LIGHTMAGENTA_EX + "Discarding card: " + str(nbcard + 1) + Bcolor.END)
                self.discard(self.hand[nbcard])
                self.drawFrom(hanabi.Hanabi.deck)
                return  # finish if discarded a  card
            # print(colorama.Fore.LIGHTMAGENTA_EX + "Could not discard card: " + str(nbcard + 1) + Bcolor.END)
            nbcard += 1
        else:  # discard a random card if cant find a discardable card
            randDiscard = randint(0, self.handCapacity - 1)
            # print(colorama.Fore.LIGHTMAGENTA_EX + "Could not find discardable card, random card: " + str(randDiscard) + Bcolor.END)
            self.discard(self.hand[randDiscard])
            self.drawFrom(hanabi.Hanabi.deck)


class PlayerNet(Player):
    """
    Player that play with the help of the neural network.
    """

    def __init__(self, handSize, neuralNet=None, model=None):
        Player.__init__(self, handSize)
        self.net = neuralNet
        self.log = []
        self.drawFrom(hanabi.Hanabi.deck)
        self.model = model

    def promptAction(self, knowledgeBase=None, nTurnsLeft=5):
        states = []
        for i in range(len(self.hand)):
            states.append(State(hanabi.Hanabi.table.field, hanabi.Hanabi.table.discarded, len(hanabi.Hanabi.deck), hanabi.Hanabi.table.strikes, self.hand, nTurnsLeft))
            states[-1].play(i)
            states[-1].hand.append(copy.deepcopy(hanabi.Hanabi.deck[0]))
        for i in range(len(self.hand)):
            states.append(State(hanabi.Hanabi.table.field, hanabi.Hanabi.table.discarded, len(hanabi.Hanabi.deck), hanabi.Hanabi.table.strikes, self.hand, nTurnsLeft))
            states[-1].discard(i)
            states[-1].hand.append(copy.deepcopy(hanabi.Hanabi.deck[0]))

        stateValues = []
        for s in states:
            if self.model is None:
                stateValues.append(self.net.compute(s.toInputs()))
            else:
                v = self.model.predict(np.array(s.toInputs()).reshape(-1, 93))
                stateValues.append(v[0][0])

        if all(x == stateValues[0] for x in stateValues):
            indexOfBestState = stateValues.index(random.choice(stateValues))
        else:
            indexOfBestState = stateValues.index(max(stateValues))
        if int(indexOfBestState / len(self.hand)) == 0:
            self.play(self.hand[indexOfBestState % len(self.hand)])
        else:
            self.discard(self.hand[indexOfBestState % len(self.hand)])
        self.drawFrom(hanabi.Hanabi.deck)

        self.log.append(states[indexOfBestState])  # logging the states to learn later


class State():
    """
    Copy the state of the game to try all the moves so we don't touch the real game.
    """

    def __init__(self, field, graveyard, cardsLeft, strikes, hand, nTurnsLeft):
        self.field = copy.deepcopy(field)
        self.graveyard = copy.deepcopy(graveyard)
        self.cardsLeft = copy.deepcopy(cardsLeft)
        self.strikes = strikes
        self.hand = copy.deepcopy(hand)
        self.nTurns = nTurnsLeft

    def play(self, i):
        c = self.hand[i]
        if self.field[Suit.toInt(c.getSuit()) - 1] == c.getValue() - 1:
            self.field[Suit.toInt(c.getSuit()) - 1] += 1
            del self.hand[i]
        else:
            self.strikes -= 1
            self.discard(i)

    def discard(self, i):
        self.graveyard.append(self.hand[i])
        del self.hand[i]

    def getScore(self):
        return sum(self.field)

    def toInputs(self):
        inputs = []
        for card in self.field:  # adding the field cards in binary to inputs
            inputs += pad([int(i) for i in str(bin(card))[2:]], 3)

        # adding a logical value for each card in the game saying whether it is discardable or not
        discarded = []
        for card in self.graveyard:
            discarded.append(int(card))  # now we have all the discarded cards in int form ([1, 25])
        discardable = [0 for _ in range(25)]
        for card in discarded:
            discardable[card - 1] += 1  # now we have the number of discarded cards of each type  # the -1 is to avoid out of bounds
        # discardable is turned into a boolean array
        # this doesn't take into account dead cards
        for i in range(25):
            if Card.getValueFromInt(i + 1) == 1:
                discardable[i] = 1 if discardable[i] <= 1 else 0
            elif Card.getValueFromInt(i + 1) == 5:
                discardable[i] = 0
            else:
                discardable[i] = 1 if discardable[i] == 0 else 0
        inputs += discardable

        # length of deck (binary)
        inputs += pad([int(i) for i in str(bin(self.cardsLeft))[2:]], 6)

        # number of turns left in binary
        inputs += pad([int(i) for i in str(bin(self.nTurns))[2:]], 3)

        # current score in binary
        inputs += pad([int(i) for i in str(bin(self.getScore()))[2:]], 6)

        # number of strikes in binary
        inputs += pad([int(i) for i in str(bin(self.strikes))[2:]], 2)

        # cards in hand
        for card in self.hand:
            currentCardInfoBinary = card.toBinary()
            currentCardInfoBinary.append(int(hanabi.Hanabi.table.cardPlayable(card)))
            currentCardInfoBinary.append(int(hanabi.Hanabi.table.cardDead(card)))
            currentCardInfoBinary.append(int(hanabi.Hanabi.table.cardDiscardable(card)))
            inputs += currentCardInfoBinary

        return inputs

    def cardListToStr(self, cards):
        s = ''
        for i in cards:
            s += str(i)
            s += '\n'
        return s

    def __str__(self):
        return "field : " + str(self.field) + "\ngraveyard : " + self.cardListToStr(self.graveyard) + "\ncards left : " + str(self.cardsLeft) + "\nstrikes : " + str(self.strikes) + "\nhand : " + self.cardListToStr(self.hand) + "\nturns left : " + str(self.nTurns) + "\n"
