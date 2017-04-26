#!/usr/bin/python
#-*- coding: utf-8 -*-
from card import *
import hanabi
from random import randint
from bcolor import *
import colorama


class Player(object):
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
        hanabi.Hanabi.table.placeDiscard(c)
        hanabi.Hanabi.table.rechargeHint()

    def promptAction(self, players):
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
    def __init__(self, handSize):
        Player.__init__(self, handSize)

    def promptAction(self):
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
    def __init__(self, handSize):
        Player.__init__(self, handSize)

    def promptAction(self):
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
    def __init__(self, handSize):
        Player.__init__(self, handSize)

    def promptAction(self, knowledgeBase=None):
        nbcard = 0  # index of current card
        print("--------------")
        print("Trying to play... ")
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
                print(colorama.Fore.CYAN + "Playing card: " + str(nbcard + 1) + Bcolor.END)
                return  # finish if played a  card
            else:
                if knowledgeBase is not None:
                    knowledgeBase.append((example, [0]))
            print(colorama.Fore.CYAN + "Could not play card: " + str(nbcard + 1) + Bcolor.END)
            nbcard += 1
        nbcard = 0
        for card in self.hand:
            if hanabi.Hanabi.table.cardDiscardable(self.hand[nbcard]):
                print(colorama.Fore.LIGHTMAGENTA_EX + "Discarding card: " + str(nbcard + 1) + Bcolor.END)
                self.discard(self.hand[nbcard])
                self.drawFrom(hanabi.Hanabi.deck)
                return  # finish if discarded a  card
            print(colorama.Fore.LIGHTMAGENTA_EX + "Could not discard card: " + str(nbcard + 1) + Bcolor.END)
            nbcard += 1
        else:  # discard a random card if cant find a discardable card
            randDiscard = randint(0, self.handCapacity - 1)
            print(colorama.Fore.LIGHTMAGENTA_EX + "Could not find discardable card, random card: " + str(randDiscard) + Bcolor.END)
            self.discard(self.hand[randDiscard])
            self.drawFrom(hanabi.Hanabi.deck)


class PlayerNet(Player):
    def __init__(self, handSize, neuralNet):
        Player.__init__(self, handSize)
        self.net = neuralNet

    def promptAction():
        states = []
        for _ in range(len(self.hand)):
            
            states.append(State(hanabi.Hanabi.table.field, hanabi.Hanabi.table.discarded, len(hanabi.Hanabi.deck, hanabi.Hanabi.table.strikesLeft(), self.hand)))

        bestState = states[0]
        bestStateValue = getStateValue
        for i in range(1, states):
            if self.getStateValue(states[i]) > bestStateValue:
                bestState = states[i]

    def getStateValue(self, state):
        inputs = []
        for card in state.field:  # adding the field cards in binary to inputs
            inputs += pad([int(i) for i in str(bin(card.getValue()))[2:]], 3)

        # adding a logical value for each card in the game saying whether it is discardable or not
        discarded = []
        for card in state.graveyard:
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
        inputs += pad([int(i) for i in str(bin(hanabi.Hanabi.deck.cardsLeft()))[2:]], 6)

        # here there should be 3 bits for the number of turns left if the deck is empty

        # current score in binary
        inputs += pad([int(i) for i in str(bin(hanabi.Hanabi.table.getScore()))[2:]], 6)

        # number of strikes in binary
        inputs += pad([int(i) for i in str(bin(hanabi.Hanabi.table.strikes))[2:]], 2)

        # cards in hand
        for card in state.hand:
            currentCardInfoBinary = card.toBinary()
            currentCardInfoBinary.append(int(hanabi.Hanabi.table.cardPlayable(card)))
            currentCardInfoBinary.append(int(hanabi.Hanabi.table.cardDead(card)))
            currentCardInfoBinary.append(int(hanabi.Hanabi.table.cardDiscardable(card)))

        return self.net.compute(inputs)


class State():
    def __init__(self, field, graveyard, cardsLeft, strikes, hand):
        self.field = field
        self.graveyard = graveyard
        self.cardsLeft = cardsLeft
        self.strikes = strikes
        self.hand = hand
