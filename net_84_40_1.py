#!/usr/bin/python
#-*- coding: utf-8 -*-

import random

from neuralnet import NeuralNetwork
from statistics import mean


def log2kb(log, score):
    kb = []
    for state in log:
        kb.append((state.toInputs(), [score]))


def trainOnGame(net):
    pass


if __name__ == '__main__':

    for j in range(10):
        seed = random.randint(-65536, 65535)  # -13920 good seed
        random.seed(seed)
        print("seed : ", seed)
        nn = NeuralNetwork(neuronsPerLayer=[84, 40, 1])  # structure is not [93, 40, 1] because we're omitting the number of turns left on 3 bits for now

        file = open("scores" + j + ".csv", mode='a')

        scores = [0 for _ in range(10)]
        i = 0
        while mean(scores) < 20:
            scores[i % 10] = trainOnGame(nn)
            if i % 100 == 0:
                file.write(mean(scores))
            i += 1
