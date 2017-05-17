#!/usr/bin/python
#-*- coding: utf-8 -*-

from main import neuralNetAutoMain

from neuralnet import NeuralNetwork
from statistics import mean


def log2kb(log, score):
    """
    Transform the log from previous game to an array understandable by the neural network.
    Arg:
        -log : array containing the states a game has been in.
        -score : score of the game associated with the log.
    """
    kb = []
    for state in log:
        kb.append((state.toInputs(), [score]))
    return kb


def trainOnGame(net):
    """
    Play a game to save the best computed moves and feed the neural network .
    Arg:
        -model : our neural network.
    """
    log = neuralNetAutoMain(neuralNet=net)
    score = log[-1].getScore()
    net.train(log2kb(log, score), doTests=False)
    print(score)
    return score


if __name__ == '__main__':

    for j in range(10):

        nn = NeuralNetwork(neuronsPerLayer=[93, 40, 1])  # 93 inputs with a hidden layer of 40 nodes and 1 output

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
