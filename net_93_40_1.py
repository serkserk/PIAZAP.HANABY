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
    log = neuralNetAutoMain(neuralNet=net)
    score = log[-1].getScore()
    net.train(log2kb(log, score), doTests=False)
    print(score)
    return score


if __name__ == '__main__':

    for j in range(10):

        nn = NeuralNetwork(neuronsPerLayer=[93, 40, 1])

        scores = [0 for _ in range(5000)]
        i = 0
        while mean(scores) < 20:
            scores[i % 5000] = trainOnGame(net=nn)
            if i % 5000 == 0:
                with open("scores" + str(j) + ".csv", mode='a') as file:
                    file.write(str(mean(scores)) + ";")
            i += 1
            print(i, end="\t")
        file.close()
