#!/usr/bin/python
#-*- coding: utf-8 -*-
from random import random


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
        self.layers = []
        self.connexions = []
        i = 0
        for layer in neuronsPerLayer:  # initializing neuron self.layers
            self.layers[i] = [0 for x in range(layer)]
            i += 1

        for i in range(self.layers - 1):
            self.connexions[i] = [((random() * 20) - 10) for x in range(len(self.layers[i]) * len(self.layers[i + 1]))]
