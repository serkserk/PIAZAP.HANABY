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


if __name__ == '__main__':
    nn = NeuralNetwork(neuronsPerLayer=[4, 4, 1])
    print(nn.connexions)
    trainKB = []
    testKB = []
    for i in range(2000):
        trainKB.append((generateGoodCombo(), [1]))
        trainKB.append((generateBadCombo(), [0]))
        testKB.append((generateGoodCombo(), [1]))
        testKB.append((generateBadCombo(), [0]))

    untrainedErrorOnKB = nn.test(knowledgeBase=trainKB)
    untrainedErrorOnTest = nn.test(knowledgeBase=testKB)
    trainedErrorOnKB1 = nn.train(knowledgeBase=trainKB)
    for _ in range(100):
        nn.train(knowledgeBase=trainKB, doTests=False)
    print()
    trainedErrorOnKB1000 = nn.test(knowledgeBase=trainKB)
    trainedErrorOnTest = nn.test(knowledgeBase=testKB)

    print("untrainedErrorOnKB : ", untrainedErrorOnKB)
    print("untrainedErrorOnTest : ", untrainedErrorOnTest)
    print("trainedErrorOnKB1 : ", trainedErrorOnKB1)
    print("trainedErrorOnKB1000 : ", trainedErrorOnKB1000)
    print("trainedErrorOnTest : ", trainedErrorOnTest)
    print(nn.connexions)
    print()
