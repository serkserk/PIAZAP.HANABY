#!/usr/bin/python
#-*- coding: utf-8 -*-

from main import neuralNetAutoMain

from neuralnet import NeuralNetwork
from statistics import mean


def log2kb(log, score):
    kb = []
    for state in log:
        kb.append((state.toInputs(), [score]))
    return kb


def trainOnGame(net):
    log = neuralNetAutoMain(net)
    score = log[-1].getScore()
    net.train(log2kb(log, score), doTests=False)
    return score


if __name__ == '__main__':

    for j in range(10):
        # seed = random.randint(-65536, 65535)  # -13920 good seed
        # random.seed(seed)
        # print("seed : ", seed)
        nn = NeuralNetwork(neuronsPerLayer=[84, 40, 1])  # structure is not [93, 40, 1] because we're omitting the number of turns left on 3 bits for now

        file = open("scores" + str(j) + ".csv", mode='a')

        scores = [0 for _ in range(10)]
        i = 0
        while mean(scores) < 20:
            scores[i % 10] = trainOnGame(nn)
            if i % 100 == 0:
                file.write(str(mean(scores)) + "; ")
            i += 1
        file.close()
