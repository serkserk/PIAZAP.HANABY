#!/usr/bin/python
#-*- coding: utf-8 -*-
import random
from card import Card
from suit import Suit
from neuralnet import NeuralNetwork


def generateUnplayableCard(seed=None):
    random.seed(seed)
    fireWorks = []
    for i in range(5):
        fireWorks.append(random.randint(0, 5))  # creating random firework values (intentionally normally distributed)
    card = Card()
    card.setSuit(Suit(random.randint(1, 5)))
    forbiddenValue = fireWorks[Suit.toInt(card.getSuit()) - 1] + 1
    card.setValue(random.randint(1, 5))
    while card.getValue() == forbiddenValue:
        card.setValue(random.randint(1, 5))
    fireWorks.append(Suit.toInt(card.getSuit()))
    fireWorks.append(card.getValue())
    return fireWorks


def generatePlayableCard(seed=None):
    random.seed(seed)
    fireWorks = []
    for i in range(5):
        fireWorks.append(random.randint(0, 5))  # creating random firework values (intentionally normally distributed)
    card = Card()
    card.setSuit(Suit(random.randint(1, 5)))
    card.setValue(fireWorks[Suit.toInt(card.getSuit()) - 1] + 1)
    if card.getValue() == 6:
        fireWorks[Suit.toInt(card.getSuit()) - 1] = random.randint(1, 4)
        card.setValue(fireWorks[Suit.toInt(card.getSuit()) - 1] + 1)
    fireWorks.append(Suit.toInt(card.getSuit()))
    fireWorks.append(card.getValue())
    return fireWorks


if __name__ == '__main__':
    for i in range(1000):
        seed = random.randint(-65536, 65535)
        random.seed(seed)
        nn = NeuralNetwork(neuronsPerLayer=[7, 20, 5, 1], learningStep=0.1)
        kb = []
        testKB = []
        for i in range(10000):
            kb.append((generatePlayableCard(), [1]))
            kb.append((generateUnplayableCard(), [0]))

        for i in range(1000):
            testKB.append((generatePlayableCard(), [1]))
            testKB.append((generateUnplayableCard(), [0]))

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
