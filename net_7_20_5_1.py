#!/usr/bin/python
#-*- coding: utf-8 -*-
import random
from card import Card
from suit import Suit
from neuralnet import NeuralNetwork


def train(self, player, table):
    for card in player.hand:
        inputs = []
        for suit, value in table.field.items():
            inputs.append(value)
        inputs.append(Suit.toInt(card.getSuit()))
        inputs.append(card.getValue())
        print(inputs)
        self.compute(inputs)
        expectedValue = 0
        if table.cardPlayable(card):
            expectedValue = 1
        self.backprop([expectedValue])


def testOnGame(self, player, table):
    inputs = []
    for card in player.hand:
        for suit, value in table.field.items():
            inputs.append(value)
        inputs.append(Suit.toInt(card.getSuit()))
        inputs.append(card.getValue())
        self.compute(inputs)
        expectedValue = 0
        if table.cardPlayable(card):
            expectedValue = 1
        output = self.getOutput()[0]
        if output > 0.5:
            output = 1
        else:
            output = 0
        self.learnError.append(abs(expectedValue - output))


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
    fireWorks.append(Suit.toInt(card.getSuit()))
    fireWorks.append(card.getValue())
    return fireWorks


def test(net, iterations=10000, seed=None):
    from statistics import mean
    errors = []
    for i in range(iterations):
        net.compute(generatePlayableCard(seed))
        errors.append(abs(1 - net.getOutput()[0]))
        net.compute(generateUnplayableCard(seed))
        errors.append(abs(0 - net.getOutput()[0]))
    return mean(errors)


if __name__ == '__main__':
    import main
    import sys

    main.blockPrint()

    weightSeed = "placeholder"
    random.seed(weightSeed)
    nn = NeuralNetwork(neuronsPerLayer=[7, 20, 5, 1])
    nn.train = train

    stdinbkp = sys.stdin

    trainSeed = "placeholder"
    random.seed(trainSeed)
    iterations = 16  # base d'apprentissage ~ 10 000 exemples
    for i in range(iterations):
        main.main(nn, "trainfile.txt")

    random.seed(trainSeed)
    nn.train = testOnGame
    main.main(nn)
    nn.learnError = []
    main.enablePrint()
    print("learn Error :", nn.learnError)
    testError = test(nn)

    sys.stdin = stdinbkp
