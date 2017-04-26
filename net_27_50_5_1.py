#!/usr/bin/python
#-*- coding: utf-8 -*-
import random

from card import Card
from neuralnet import NeuralNetwork
from suit import Suit


def generateDispensableCard(seed=None):
    if seed is not None:
        random.seed(seed)
    card = Card()
    card.setSuit(Suit(random.randint(1, 5)))
    card.setValue(random.randint(1, 4))  # 5s are indispensable
    graveyard = [random.randint(0, 3) if i % 5 == 0 else (random.randint(0, 1) if i % 5 == 4 else random.randint(0, 2)) for i in range(25)]
    #            0-3 discarded if a 1                          0-1 discarded if a 5                 else 0-2 discarded
    graveyard[int(card) - 1] = 0 if card.getValue() > 1 else random.randint(0, 1)

    graveyard.append(Suit.toInt(card.getSuit()))
    graveyard.append(card.getValue())
    return graveyard


def generateIndispensableCard(seed=None):
    if seed is not None:
        random.seed(seed)
    card = Card()
    card.setSuit(Suit(random.randint(1, 5)))
    card.setValue(random.randint(1, 5))
    graveyard = [random.randint(0, 3) if i % 5 == 0 else (random.randint(0, 1) if i % 5 == 4 else random.randint(0, 2)) for i in range(25)]
    #            0-3 discarded if a 1                          0-1 discarded if a 5                 else 0-2 discarded

    graveyard[(Suit.toInt(card.getSuit()) - 1) * 5] = random.randint(0, 2)
    for i in range((Suit.toInt(card.getSuit()) - 1) * 5 + 1, int(card) - 1):
        graveyard[i] = random.randint(0, 1)
    graveyard[int(card) - 1] = 0 if card.getValue() == 5 else 2 if card.getValue() == 1 else 1
    #                            5 can't be discarded            must be the last 1         must be the last of its kind
    graveyard.append(Suit.toInt(card.getSuit()))
    graveyard.append(card.getValue())
    return graveyard


if __name__ == '__main__':
    for i in range(10):
        seed = random.randint(-65536, 65535)
        random.seed(seed)
        nn = NeuralNetwork(neuronsPerLayer=[27, 50, 5, 1])
        kb = []
        testKB = []
        for i in range(10000):
            kb.append((generateDispensableCard(), [1]))
            kb.append((generateIndispensableCard(), [0]))

        for i in range(1000):
            testKB.append((generateDispensableCard(), [1]))
            testKB.append((generateIndispensableCard(), [0]))

        untrainedErrorOnKB = nn.test(knowledgeBase=kb)
        untrainedErrorOnTest = nn.test(knowledgeBase=testKB)
        trainedErrorOnKB1 = nn.train(knowledgeBase=kb)
        for _ in range(1000):
            nn.train(knowledgeBase=kb, doTests=False)
        trainedErrorOnKB1000 = nn.test(knowledgeBase=kb)
        trainedErrorOnTest = nn.test(knowledgeBase=testKB)

        print("untrainedErrorOnKB : ", untrainedErrorOnKB)
        print("untrainedErrorOnTest : ", untrainedErrorOnTest)
        print("trainedErrorOnKB1 : ", trainedErrorOnKB1)
        print("trainedErrorOnKB1000 : ", trainedErrorOnKB1000)
        print("trainedErrorOnTest : ", trainedErrorOnTest)
        print("seed : ", seed)
        print()
