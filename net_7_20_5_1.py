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
    inputs.append("white")
    inputs.append("")
    inputs.append("red")
    inputs.append("")
    inputs.append("blue")
    inputs.append("")
    inputs.append("green")
    inputs.append("")
    inputs.append("yellow")
    inputs.append("")
    inputs.append("cardcol")
    inputs.append("cardvalue")
    for i in [1, 3, 5, 7, 9]:
            inputs[i] = random.randint(1, 5)
    c = Card(suit=Suit.randomColor(), value=random.randint(1, 5))
    inputs[10] = Suit.toInt(c.getSuit())
    inputs[11] = c.getValue()
    while not ((inputs[0] == c.getSuit()) and (inputs[1] == (c.getValue() - 1))) or ((inputs[2] == c.getSuit()) and (inputs[3] == (c.getValue() - 1))) or ((inputs[4] == c.getSuit()) and (inputs[5] == (c.getValue() - 1))) or ((inputs[6] == c.getSuit()) and (inputs[7] == (c.getValue() - 1))) or ((inputs[8] == c.getSuit()) and (inputs[9] == (c.getValue() - 1))):
        for i in [1, 3, 5, 7, 9]:
            inputs[i] = random.randint(1, 5)
        c = Card(suit=Suit.randomColor(), value=random.randint(1, 5))
        inputs[10] = Suit.toInt(c.getSuit())
        inputs[11] = c.getValue()
    print("good: ", inputs, "card: ", c.getSuit(), c .getValue())
    return [inputs[1], inputs[3], inputs[5], inputs[7], inputs[9], inputs[10], inputs[11]]


def generateBadSample():
    inputs = []
    inputs.append("white")
    inputs.append("")
    inputs.append("red")
    inputs.append("")
    inputs.append("blue")
    inputs.append("")
    inputs.append("green")
    inputs.append("")
    inputs.append("yellow")
    inputs.append("")
    inputs.append("cardcol")
    inputs.append("cardvalue")
    for i in [1, 3, 5, 7, 9]:
            inputs[i] = random.randint(1, 5)
    c = Card(suit=Suit.randomColor(), value=random.randint(1, 5))
    inputs[10] = Suit.toInt(c.getSuit())
    inputs[11] = c.getValue()
    while ((inputs[0] == c.getSuit()) and (inputs[1] == (c.getValue() - 1))) or ((inputs[2] == c.getSuit()) and (inputs[3] == (c.getValue() - 1))) or ((inputs[4] == c.getSuit()) and (inputs[5] == (c.getValue() - 1))) or ((inputs[6] == c.getSuit()) and (inputs[7] == (c.getValue() - 1))) or ((inputs[8] == c.getSuit()) and (inputs[9] == (c.getValue() - 1))):
        for i in [1, 3, 5, 7, 9]:
            inputs[i] = random.randint(1, 5)
        c = Card(suit=Suit.randomColor(), value=random.randint(1, 5))
        inputs[10] = Suit.toInt(c.getSuit())
        inputs[11] = c.getValue()
    print("bad: ", inputs, "card: ", c.getSuit(), c .getValue())
    return [inputs[1], inputs[3], inputs[5], inputs[7], inputs[9], inputs[10], inputs[11]]


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


def test2(net, iterations=10,):
    from statistics import mean
    errors = []
    for i in range(iterations):
        net.compute(generateGoodSample())
        errors.append(abs(1 - net.getOutput()[0]))
        print("layers: ", nn.layers[0], "\n", nn.layers[1], "\n", nn.layers[2], nn.layers[3])
        print("biases: ", nn.biases[0], "\n", nn.biases[1], "\n", nn.biases[2], "\n", nn.biases[3])
        print("connexions: ", nn.connexions[0], "\n", nn.connexions[1], "\n", nn.connexions[2])
        net.compute(generateBadSample())
        errors.append(abs(0 - net.getOutput()[0]))
        print("layers: ", nn.layers[0], "\n", nn.layers[1], "\n", nn.layers[2], nn.layers[3])
        print("biases: ", nn.biases[0], "\n", nn.biases[1], "\n", nn.biases[2], "\n", nn.biases[3])
        print("connexions: ", nn.connexions[0], "\n", nn.connexions[1], "\n", nn.connexions[2])
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
    nn = NeuralNetwork(neuronsPerLayer=[7, 20, 5, 1])
    print("layers: ", nn.layers[0], "\n", nn.layers[1], "\n", nn.layers[2], nn.layers[3])
    print("biases: ", nn.biases[0], "\n", nn.biases[1], "\n", nn.biases[2], "\n", nn.biases[3])
    print("connexions: ", nn.connexions[0], "\n", nn.connexions[1], "\n", nn.connexions[2])
    print("start learning_______")
    for i in range(10):
        print(i, end="")
        inputs = generateGoodSample()
        c = Card(inputs[5], inputs[6])
        nn.compute(inputs)
        expectedValue = 1
        nn.backprop([expectedValue])
        print("layers: ", nn.layers[0], "\n", nn.layers[1], "\n", nn.layers[2], nn.layers[3])
        print("biases: ", nn.biases[0], "\n", nn.biases[1], "\n", nn.biases[2], "\n", nn.biases[3])
        print("connexions: ", nn.connexions[0], "\n", nn.connexions[1], "\n", nn.connexions[2])
        print(i, end="")
        inputs = generateBadSample()
        c = Card(inputs[5], inputs[6])
        nn.compute(inputs)
        expectedValue = 0
        nn.backprop([expectedValue])
        print("layers: ", nn.layers[0], "\n", nn.layers[1], "\n", nn.layers[2], nn.layers[3])
        print("biases: ", nn.biases[0], "\n", nn.biases[1], "\n", nn.biases[2], "\n", nn.biases[3])
        print("connexions: ", nn.connexions[0], "\n", nn.connexions[1], "\n", nn.connexions[2])
        print("end learning_______")
    # # test learning
    # print("start test learning_______")
    # nn.learnError = []
    # for i in range(20):
    #     inputs = generateGoodSample(ColValseed)
    #     c = Card(inputs[5], inputs[6])
    #     nn.compute(inputs)
    #     expectedValue = 1
    #     output = nn.getOutput()[0]
    #     if output > 0.5:
    #         output = 1
    #     else:
    #         output = 0
    #     nn.learnError.append(abs(expectedValue - output))

    #     inputs = generateBadSample(ColValseed)
    #     c = Card(inputs[5], inputs[6])
    #     nn.compute(inputs)
    #     expectedValue = 1
    #     output = nn.getOutput()[0]
    #     if output > 0.5:
    #         output = 1
    #     else:
    #         output = 0
    #     nn.learnError.append(abs(expectedValue - output))
    # print(nn.learnError)
    # print()
    # print("________Learn error :", sum(nn.learnError) / len(nn.learnError))
    # print("end test learning_______")

    # test
    testError = test2(nn)
    print("_______Test error :", testError)
