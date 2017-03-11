#!/usr/bin/python
#-*- coding: utf-8 -*-
from random import random
import math


class NeuralNetwork:
    """ This class models a Neural Network.
        Attributes:
            - self.layers
            - connexions
    """

    def __init__(self, neuronsPerLayer):
        """ Constructor.
            Args:
                - neuronsPerLayer : an array containing the number of neurons for each layer
        """
        self.nInputs = neuronsPerLayer[0]  # number of input neurons
        self.layers = []                   # this list contains the layers. Each layer is a list of values
        # this list contains the connexion layers. Each connexion layer is a list of values.
        self.connexions = []               # We can identify the neurons involved by the connexion's index.
        # This list contains the biases for each neuron. it corresponds perfectly self.layers,
        self.biases = []                   # i.e. self.biases[i][j] is the bias for self.layers[i][j]

        i = 0
        for layer in neuronsPerLayer:  # initializing neuron self.layers with zeroes
            self.layers[i] = [0 for x in range(layer)]
            i += 1

        for i in range(self.layers - 1):  # initializing connexions with random real values [-10, 10]
            self.connexions[i] = [((random() * 20) - 10) for x in range(len(self.layers[i]) * len(self.layers[i + 1]))]
            # the connexion from self.layers[i][j] to self.layers[i-1][k] is self.connexions[i-1][k*len(self.layers[i])+j]
            # the neurons corresponding to self.connexions[i][j] are self.layers[i][j/len(self.layers[i+1])] and self.layers[i+1][j%len(self.layers[i+1])]

        self.biases[0] = None  # self.biases[0] corresponds to self.layers[0] which is the input layer ; however inputs do not have biases.
        for i in range(1, len(neuronsPerLayer)):  # initializing bias layers with random real values [-10, 10]
            self.biases[i] = [((random() * 20) - 10) for x in range(neuronsPerLayer[i])]

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
            for j in range(self.layers[i]):   # for each neuron
                netj = 0                      # this is the raw value of the neuron
                for k in range(len(self.layers[i - 1])):  # for each connexion of the current neuron to the neurons of the previous layer
                    netj += self.layers[i - 1][k] * self.connexions[i - 1][k * len(self.layers[i]) + j]  # netj += value + connexion
                netj += self.biases[i][j]
                self.layers[i][j] = sigmoid(netj)
        return self.layers[len(self.layers) - 1]


def sigmoid(x):
    return 1 / (1 + math.exp(-x))
