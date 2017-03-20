#!/usr/bin/python
#-*- coding: utf-8 -*-
import random
from card import Card
from suit import Suit
import math


class NeuralNetwork:
    """ This class models a Neural Network.
        Attributes:
            - self.layers
            - connexions
    """

    def __init__(self, neuronsPerLayer=[4, 8, 1], learningStep=0.1):
        """ Constructor.
            Args:
                - neuronsPerLayer : an array containing the number of neurons for each layer
                - the learning step, or Nu.
        """

        self.nInputs = neuronsPerLayer[0]  # number of input neurons
        self.layers = []                   # this list contains the layers. Each layer is a list of values
        # this list contains the connexion layers. Each connexion layer is a list of values.
        self.connexions = []               # We can identify the neurons involved by the connexion's index.
        # This list contains the biases for each neuron. it corresponds perfectly self.layers,
        self.biases = []                   # i.e. self.biases[i][j] is the bias for self.layers[i][j]
        self.step = learningStep           # the learning step, or Nu.

        for layer in neuronsPerLayer:  # initializing neuron self.layers with zeroes
            self.layers.append([])
            for x in range(layer):
                self.layers[len(self.layers) - 1].append(0)

        for i in range(len(self.layers) - 1):  # initializing connexions with random real values [-10, 10]
            self.connexions.append([])
            for x in range(len(self.layers[i]) * len(self.layers[i + 1])):
                self.connexions[i].append(random.random() * 20 - 10)
            # the connexion from self.layers[i][j] to self.layers[i-1][k] is self.connexions[i-1][k*len(self.layers[i])+j]
            # the connexion from self.layers[i][j] to self.layers[i+1][k] is self.connexions[i][j*len(self.layers[i+1])+k]
            # the neurons corresponding to self.connexions[i][j] are self.layers[i][j/len(self.layers[i+1])] and self.layers[i+1][j%len(self.layers[i+1])]

        self.biases.append(None)  # self.biases[0] corresponds to self.layers[0] which is the input layer ; however inputs do not have biases.
        for i in range(1, len(neuronsPerLayer)):  # initializing bias layers with random real values [-10, 10]
            self.biases.append([])
            for x in range(neuronsPerLayer[i]):
                self.biases[i].append(random.random() * 20 - 10)

    def compute(self, input):
        """ Output value computation method.
            Args:
                - input : an array of values corresponding to the input values of the network
            Raises ValueError if input is not the same length as the number of input neurons in the network
        """
        if len(input) != self.nInputs:
            raise ValueError("Input list length does not match number of input neurons in network")

        self.layers[0] = input

        for i in range(1, len(self.layers)):  # for each layer except input layer
            for j in range(len(self.layers[i])):   # for each neuron
                netj = 0                      # this is the raw value of the neuron (before it's passed to the sigmoid)
                for k in range(len(self.layers[i - 1])):  # for each connexion of the current neuron to the neurons of the previous layer
                    netj += self.layers[i - 1][k] * self.connexions[i - 1][k * len(self.layers[i]) + j]  # netj += value * connexion
                netj += self.biases[i][j]
                self.layers[i][j] = sigmoid(netj)
        return self.layers[len(self.layers) - 1]

    def backprop(self, targetValues):
        """ Backwards propagation algorithm.
            This method should be called immediately after compute() : It uses the last computed value as the output to correct.
            Args :
                - targetValues : a list of values corresponding to what was expected of the output neurons.
                                Must be the same size as the number of output neurons.
        """
        outputLayer = self.layers[len(self.layers) - 1]
        if len(targetValues) != len(outputLayer):
            raise ValueError("Target list length does not match number of output neurons in network")

        errorSignals = []  # a list of lists that contains the error signal for each neuron
        for layer in self.layers:  # initializing errorSignals to zeroes
            a = [0 for neuron in layer]
            errorSignals.append(a)

        # Backprop on the last layer
        for k in range(len(targetValues)):
            # error signal dk = (Tk-Ok) f'(Netk) = (Tk-Ok) f(Netk) (1-f(Netk)) = (Tk-Ok) Ok (1-Ok)
            dk = (targetValues[k] - outputLayer[k]) * outputLayer[k] * (1 - outputLayer[k])
            errorSignals[len(errorSignals) - 1][k] = dk
            for j in range(len(self.layers[len(self.layers) - 2])):  # for each neuron in the second-to-last layer
                # connexion from current neuron of the second-to-last layer to current output neuron
                WjkOld = self.connexions[len(self.layers) - 2][j * len(self.layers[len(self.layers) - 1]) + k]
                WjkNew = WjkOld + self.step * dk * self.layers[len(self.layers) - 2][j]  # Wjk_old + Nu * Dk * Oj
                self.connexions[len(self.layers) - 2][j * len(self.layers[len(self.layers) - 1]) + k] = WjkNew

        # backprop on the rest of the network
        for i in range(len(self.layers) - 2, -1, -1):  # for each layer from the second-to-last to the first (the last computed index being 0 since -1 is excluded)
            for j in range(len(self.layers[i])):  # for each neuron
                for k in range(len(self.layers[i + 1])):
                    # update connexion
                    WhzOld = self.connexions[i][j * len(self.layers[i + 1]) + k]
                    dk = errorSignals[i + 1][k]
                    WhzNew = WhzOld + self.step * dk * self.layers[i][j]
                    self.connexions[i][j * len(self.layers[i + 1]) + k] = WhzNew

                    # determine error signal for current neuron
                    oh = self.layers[i][j]
                    Whz = self.connexions[i][j * len(self.layers[i + 1]) + k]
                    dh = oh * (1 - oh) * Whz * errorSignals[i + 1][k]
                    errorSignals[i][j] = max(dh, errorSignals[i][j])

    def getOutput(self):
        return self.layers[len(self.layers) - 1]


def sigmoid(x):
    """ The sigmoid function
    """
    return 1 / (1 + math.exp(-x))


def generateBadCombo():
    """ Generates two cards which can not be played on top of each other in the hanabi game
    """
    fireWork = Card()
    card = Card()
    while fireWork.getSuit() == card.getSuit() and fireWork.getValue() == card.getValue() - 1:
        fireWork.setSuit(Suit(random.randint(1, 5)))
        fireWork.setValue(random.randint(1, 5))
        card.setSuit(Suit(random.randint(1, 5)))
        card.setValue(random.randint(1, 5))
    return (Suit.toInt(fireWork.getSuit()), fireWork.getValue(), Suit.toInt(card.getSuit()), card.getValue())


def generateGoodCombo():
    """ Generates two cards which can be played on top of each other in the hanabi game
    """
    fireWork = Card()
    card = Card()
    while not (fireWork.getSuit() == card.getSuit() and fireWork.getValue() == card.getValue() - 1):
        fireWork.setSuit(Suit(random.randint(1, 5)))
        fireWork.setValue(random.randint(1, 5))
        card.setSuit(Suit(random.randint(1, 5)))
        card.setValue(random.randint(1, 5))
    return (Suit.toInt(fireWork.getSuit()), fireWork.getValue(), Suit.toInt(card.getSuit()), card.getValue())


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


def trainOnGame(net):
    """ Trains a network on a hanabi game played by an AI
        Args:
            - net : a network to train
    """
    import main
    import sys
    stdinbkp = sys.stdin
    sys.stdin = open("trainfile.txt")
    main.main(net)
    sys.stdin = stdinbkp


if __name__ == '__main__':
    from statistics import mean
    nn = NeuralNetwork()

    random.seed(None)
    random.seed(random.randint(-65536, 65535))
    nn = NeuralNetwork()  # creating a neural network and initializing it with the chosen seed

    nIterations = 0
    error = 100
    while error > 0.001 and nIterations < 100:
        trainOnGame(nn)
        errors = []
        for i in range(100):
            nn.compute(generateGoodCombo())
            errors.append(abs(1 - nn.getOutput()[0]))
        for i in range(100):
            nn.compute(generateBadCombo())
            errors.append(abs(0 - nn.getOutput()[0]))
            error = mean(errors)
        nIterations += 1
    print(error)


"""
if __name__ == '__main__':
    import sys
    bestSeed = (0, 100)  # will be used to store the best seed of the trial run

    nIterations = 50
    if len(sys.argv) == 2:
        nIterations = int(sys.argv[1])

    for i in range(nIterations):  # trying out nIterations seeds
        random.seed(None)
        seed = random.randint(-65536, 65535)  # randomly choosing a random seed
        nn = NeuralNetwork(seed=seed)  # creating a neural network and initializing it with the chosen seed
        trainHanabi(nn)
        errors = []
        for i in range(100):
            nn.compute(generateGoodInstance())
            errors.append(abs(1 - nn.getOutput()[0]))
        for i in range(100):
            nn.compute(generateBadInstance())
            errors.append(abs(0 - nn.getOutput()[0]))
        if mean(errors) < bestSeed[1]:
            bestSeed = (seed, mean(errors))
    with open("GoodSeeds.txt", "a") as file:
        file.write(str(bestSeed))
        file.write("\n")
    print(bestSeed)
"""
