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
        self.compute(inputs)
        expectedValue = 0
        if table.cardPlayable(card):
            expectedValue = 1
        self.backprop([expectedValue])


def testOnGame(self, player, table):
    for card in player.hand:
        inputs = []
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


def generateGoodSample():
    inputs = []
    inputs.append(Suit.randomColor())
    inputs.append("")
    inputs.append("cardcol")
    inputs.append("cardvalue")
    inputs[0] = Suit.randomColor()
    inputs[1] = random.randint(1, 5)
    c = Card(suit=Suit.randomColor(), value=random.randint(1, 5))
    inputs[2] = Suit.toInt(c.getSuit())
    inputs[3] = c.getValue()
    while not ((inputs[0] == c.getSuit()) and (inputs[1] == (c.getValue() - 1))):
        inputs[0] = Suit.randomColor()
        inputs[1] = random.randint(1, 5)
        c = Card(suit=Suit.randomColor(), value=random.randint(1, 5))
        inputs[2] = Suit.toInt(c.getSuit())
        inputs[3] = c.getValue()
    # print("good: ", inputs, "card: ", c.getSuit(), c .getValue())
    return [Suit.toInt(inputs[0]), inputs[1], inputs[2], inputs[3]]


def generateBadSample():
    inputs = []
    inputs.append("white")
    inputs.append("")
    inputs.append("cardcol")
    inputs.append("cardvalue")
    inputs[0] = Suit.randomColor()
    inputs[1] = random.randint(1, 5)
    c = Card(suit=Suit.randomColor(), value=random.randint(1, 5))
    inputs[2] = Suit.toInt(c.getSuit())
    inputs[3] = c.getValue()
    while ((inputs[0] == c.getSuit()) and (inputs[1] == (c.getValue() - 1))):
        inputs[0] = Suit.randomColor()
        inputs[1] = random.randint(1, 5)
        c = Card(suit=Suit.randomColor(), value=random.randint(1, 5))
        inputs[2] = Suit.toInt(c.getSuit())
        inputs[3] = c.getValue()
    # print("bad: ", inputs, "card: ", c.getSuit(), c .getValue())
    return [Suit.toInt(inputs[0]), inputs[1], inputs[2], inputs[3]]


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


def test2(net, iterations=100000,):
    from statistics import mean
    errors = []
    for i in range(iterations):
        net.compute(generateGoodSample())
        errors.append(abs(1 - net.getOutput()[0]))
        # print("layers: ", nn.layers[0], "\n", nn.layers[1], "\n", nn.layers[2])
        # print("biases: ", nn.biases[0], "\n", nn.biases[1], "\n", nn.biases[2])
        # print("connexions: ", nn.connexions[0], "\n", nn.connexions[1])
        net.compute(generateBadSample())
        errors.append(abs(0 - net.getOutput()[0]))
        # print("layers: ", nn.layers[0], "\n", nn.layers[1], "\n", nn.layers[2])
        # print("biases: ", nn.biases[0], "\n", nn.biases[1], "\n", nn.biases[2])
        # print("connexions: ", nn.connexions[0], "\n", nn.connexions[1])
    return mean(errors)


if __name__ == '__main__':
    # import main

    # for i in range(10):
    #     main.blockPrint()

    #     weightSeed = random.randint(-65536, 65535)
    #     random.seed(weightSeed)
    #     nn = NeuralNetwork(neuronsPerLayer=[7, 20, 5, 1])
    #     nn.train = train

    #     trainSeed = random.randint(-65536, 65535)
    #     random.seed(trainSeed)
    #     iterations = 16  # base d'apprentissage ~ 10 000 exemples
    #     try:
    #         for i in range(iterations):
    #             main.main(nn, "trainfile.txt")
    #     except Exception as e:
    #         main.enablePrint()
    #         raise e

    #     random.seed(trainSeed)
    #     nn.train = testOnGame
    #     nn.learnError = []
    #     main.main(nn, "trainfile.txt")
    #     main.enablePrint()
    #     print("learn Error :", sum(nn.learnError) / len(nn.learnError))

    #     testError = test(nn)
    #     print("Test Error :", testError)

    #     print(weightSeed, " ", trainSeed)

    # learning
    nn = NeuralNetwork(neuronsPerLayer=[4, 4, 1])
    # print("layers: ", nn.layers[0], "\n", nn.layers[1], "\n", nn.layers[2])
    # print("biases: ", nn.biases[0], "\n", nn.biases[1], "\n", nn.biases[2])
    # print("connexions: ", nn.connexions[0], "\n", nn.connexions[1])
    print("start learning_______")
    for i in range(100000):
        # print(i, end="")
        inputs = generateGoodSample()
        c = Card(inputs[2], inputs[3])
        nn.compute(inputs)
        expectedValue = 1
        nn.backprop([expectedValue])
        # print("layers: ", nn.layers[0], "\n", nn.layers[1], "\n", nn.layers[2])
        # print("biases: ", nn.biases[0], "\n", nn.biases[1], "\n", nn.biases[2])
        # print("connexions: ", nn.connexions[0], "\n", nn.connexions[1])
        # print(i, end="")
        inputs = generateBadSample()
        c = Card(inputs[2], inputs[3])
        nn.compute(inputs)
        expectedValue = 0
        nn.backprop([expectedValue])
        # print("layers: ", nn.layers[0], "\n", nn.layers[1], "\n", nn.layers[2])
        # print("biases: ", nn.biases[0], "\n", nn.biases[1], "\n", nn.biases[2])
        # print("connexions: ", nn.connexions[0], "\n", nn.connexions[1])
    print("end learning_______")
    # test learning
    print("start test learning_______")
    nn.learnError = []
    for i in range(100000):
        inputs = generateGoodSample()
        c = Card(inputs[2], inputs[3])
        nn.compute(inputs)
        expectedValue = 1
        output = nn.getOutput()[0]
        if output > 0.5:
            output = 1
        else:
            output = 0
        nn.learnError.append(abs(expectedValue - output))

        inputs = generateBadSample()
        c = Card(inputs[2], inputs[3])
        nn.compute(inputs)
        expectedValue = 1
        output = nn.getOutput()[0]
        if output > 0.5:
            output = 1
        else:
            output = 0
        nn.learnError.append(abs(expectedValue - output))
    # print(nn.learnError)
    print()
    print("________Learn error :", sum(nn.learnError) / len(nn.learnError))
    print("end test learning_______")

    # test
    testError = test2(nn)
    print("_______Test error :", testError)
