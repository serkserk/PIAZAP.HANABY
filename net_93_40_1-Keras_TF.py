#!/usr/bin/python
#-*- coding: utf-8 -*-

from main import neuralNetAutoMain

from neuralnet import NeuralNetwork
from statistics import mean

from keras.models import Sequential
from keras.layers import Dense
from keras import optimizers
import numpy as np


def log2kb(log, score):
    kb = []
    for state in log:
        kb.append((state.toInputs(), [score]))
    return kb


def trainOnGame(net, model):
    log = neuralNetAutoMain(net, model)
    score = log[-1].getScore()
    # fit() method feeds states and target_f information to the model, which I explain below. You can ignore the rest parameters.
    # This training process makes the neural net to predict the reward value (target_f) from a certain state.
    for state in log:
        kb = state.toInputs()
        model.fit(kb, score, epochs=1, verbose=0)
    print(score)
    return score


if __name__ == '__main__':

    for j in range(10):
        # seed = random.randint(-65536, 65535)  # -13920 good seed
        # random.seed(seed)
        # print("seed : ", seed)
        nn = NeuralNetwork(neuronsPerLayer=[93, 40, 1])  # structure is not [93, 40, 1] because we're omitting the number of turns left on 3 bits for now

        seed = 1
        np.random.seed(seed)

        # Sequential() creates the foundation of the layers.
        model = Sequential()
        model.add(Dense(input_dim=93, units=40, activation="sigmoid"))
        model.add(Dense(units=1, activation="linear"))
        # model.summary()
        # sgd = optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        sgd = optimizers.SGD(lr=0.01, clipvalue=0.5)
        # model.compile(loss='mean_squared_error', optimizer=sgd)
        model.compile(loss="mse", optimizer=sgd, learning_rate=0.01)

        scores = [0 for _ in range(5000)]
        i = 0
        while mean(scores) < 20:
            scores[i % 5000] = trainOnGame(nn, model)
            if i % 5000 == 0:
                with open("scores" + str(j) + ".csv", mode='a') as file:
                    file.write(str(mean(scores)) + ";")
            i += 1
            print(i, end="\t")
        file.close()
