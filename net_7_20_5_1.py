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

    import main
    nn = NeuralNetwork(neuronsPerLayer=[7, 20, 5, 1])
    kb = []
    testKB = []

    for i in range(1000):
        inputs = generatePlayableCard()
        testKB.append((inputs, [1]))
        inputs = generateUnplayableCard()
        testKB.append((inputs, [0]))

    main.blockPrint()
    for i in range(32):
        main.main(knowledgeBase=kb, inputFile="trainfile.txt")
    main.enablePrint()

    print("testing knowledgeBase on untrained network :")
    print(nn.test(knowledgeBase=kb))
    print("Testing untrained on random Knowledge Base :")
    print(nn.test(knowledgeBase=testKB))
    print("testing knowledgeBase on trained network :")
    print(nn.train(knowledgeBase=kb))
    print("Testing trained on random Knowledge Base :")
    print(nn.test(knowledgeBase=testKB))
