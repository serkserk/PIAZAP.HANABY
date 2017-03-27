#!/usr/bin/python
#-*- coding: utf-8 -*-
import random
from card import Card
from suit import Suit
from neuralnet import NeuralNetwork

""" This module is the interface between the NeuralNetwork class and the Hanabi game classes
"""


def trainOnGeneratedCombos(net, nIterations=100):
    """ Trains a network on a number of generated card combos
        Args:
            - net : a network to train
            - nIterations : the number of card combos to train the network on. Defaults to 100.
    """
    n = nIterations
    while n > 0:
        net.compute(generateBadCombo())
        net.backprop([0])
        net.compute(generateGoodCombo())
        net.backprop([1])
        n -= 1


def trainOnPlay(net, card, table):
    fireWork = Card(suit=card.suit, value=table.field[card.suit])
    net.compute((Suit.toInt(fireWork.getSuit()), fireWork.getValue(), Suit.toInt(card.getSuit()), card.getValue()))
    expectedValue = 0
    if card.value == fireWork.value + 1:
        expectedValue = 1
    net.backprop([expectedValue])


"""


def trainOnPlay(net, card, table):
    inputs = []
    for suit, value in table.field.items():
        inputs.append(value)
    inputs.append(Suit.toInt(card.getSuit()))
    inputs.append(card.getValue())
    net.compute(inputs)
    expectedValue = 0
    if table.cardPlayable(card):
        expectedValue = 1
    net.backprop([expectedValue])
"""


def trainOnGame(net, seed=None):
    """ Trains a network on a hanabi game played by an AI
        Args:
            - net : a network to train
    """
    import main
    import sys
    stdinbkp = sys.stdin
    sys.stdin = open("trainfile.txt")
    main.main(net, seed)
    sys.stdin = stdinbkp


def generateBadCombo(seed=None):
    """ Generates two cards which can not be played on top of each other in the hanabi game
    """
    random.seed(seed)
    fireWork = Card()
    card = Card()
    while fireWork.getSuit() == card.getSuit() and fireWork.getValue() == card.getValue() - 1:
        fireWork.setSuit(Suit(random.randint(1, 5)))
        fireWork.setValue(random.randint(1, 5))
        card.setSuit(Suit(random.randint(1, 5)))
        card.setValue(random.randint(1, 5))
    return (Suit.toInt(fireWork.getSuit()), fireWork.getValue(), Suit.toInt(card.getSuit()), card.getValue())


def generateGoodCombo(seed=None):
    """ Generates two cards which can be played on top of each other in the hanabi game
    """
    random.seed(seed)
    fireWork = Card()
    card = Card()
    while not (fireWork.getSuit() == card.getSuit() and fireWork.getValue() == card.getValue() - 1):
        fireWork.setSuit(Suit(random.randint(1, 5)))
        fireWork.setValue(random.randint(1, 5))
        card.setSuit(Suit(random.randint(1, 5)))
        card.setValue(random.randint(1, 5))
    return (Suit.toInt(fireWork.getSuit()), fireWork.getValue(), Suit.toInt(card.getSuit()), card.getValue())


def test(net, testSeed=None):
    from statistics import mean
    errors = []
    for i in range(100):
        net.compute(generateGoodCombo(testSeed))
        errors.append(abs(1 - net.getOutput()[0]))
        net.compute(generateBadCombo(testSeed))
        errors.append(abs(0 - net.getOutput()[0]))
    return mean(errors)


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


def test72051(net, testSeed=None):
    from statistics import mean
    errors = []
    for i in range(100):
        net.compute(generatePlayableCard(testSeed))
        errors.append(abs(1 - net.getOutput()[0]))
        net.compute(generateUnplayableCard(testSeed))
        errors.append(abs(0 - net.getOutput()[0]))
    return mean(errors)


def findSeeds(maxIterations=10):
    error = 1
    bestSeed = (0, 0, 0, error)
    while maxIterations > 0 and error > 0.1:
        maxIterations -= 1
        random.seed(None)  # reset random number generator
        weightSeed = random.randint(-65536, 65535)  # create a random seed
        learnSeed = random.randint(-65536, 65535)  # create a random seed
        testSeed = random.randint(-65536, 65535)  # create a random seed
        nn = NeuralNetwork(weightInitSeed=weightSeed)  # creating a neural network and initializing it with the chosen seed

        trainOnGame(nn, learnSeed)
        error = test(nn, testSeed)

        if error < bestSeed[3]:
            bestSeed = (weightSeed, learnSeed, testSeed, error)

    with open("GoodSeeds.txt", "a") as file:
        file.write(str(bestSeed))
        file.write("\n")
    print(bestSeed)


def mixAndMatchSeeds():
    seedTuples = []
    with open('GoodSeeds.txt') as file:
        for line in file.readlines():
            line = line.strip('\n')
            nextTuple = eval(line)
            if nextTuple[3] < 0.001:
                seedTuples.append(nextTuple[:3])  # appending the tuple of seeds to the list without the error field
    confusionTable = {}
    for i in range(len(seedTuples)):
        for j in range(len(seedTuples)):
            nn = NeuralNetwork(weightInitSeed=seedTuples[i][0])
            trainOnGame(nn, seed=seedTuples[j][1])
            confusionTable[seedTuples[i][0], seedTuples[j][1]] = test(nn, 53701)  # 53701 is a bad test seed

            with open("SeedConfusionTable.txt", "w") as file:
                file.write(str(confusionTable))
                file.write("\n")


if __name__ == '__main__':
    mixAndMatchSeeds()

    """
    results = []
    for nu in [0.01, 0.1, 1, 10]:
        nn = NeuralNetwork(learningStep=nu, weightInitSeed=40478)
        trainOnGame(nn, seed=28315)
        results.append(test(nn))
    print(results)
    """

    """toasts = []
    for i in range(1):
        nn = NeuralNetwork(neuronsPerLayer=[7, 20, 5, 1])
        for i in range(10):
            trainOnGame(nn)
        toasts.append(test72051(nn))
        print(nn.layers)
        print(nn.biases)
        print(nn.connexions)
    print(toasts)
    """
