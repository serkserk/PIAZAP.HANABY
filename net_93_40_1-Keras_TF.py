#!/usr/bin/python
#-*- coding: utf-8 -*-

from main import neuralNetAutoMain

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


def trainOnGame(model):
    log = neuralNetAutoMain(model=model)
    score = log[-1].getScore()
    for state in log:
        kb = np.array(state.toInputs()).reshape(1, 93)
        model.fit(kb, np.array(score).reshape(1, -1), epochs=1, verbose=0)
    print(score)
    return score


if __name__ == '__main__':

    for j in range(10):

        seed = 1
        np.random.seed(seed)

        model = Sequential()
        model.add(Dense(input_dim=93, units=40, activation="sigmoid"))
        model.add(Dense(units=1, activation="linear"))
        sgd = optimizers.SGD(lr=0.01, clipvalue=0.5)
        model.compile(loss="mse", optimizer=sgd, learning_rate=0.01)

        scores = [0 for _ in range(5000)]
        i = 0
        while mean(scores) < 20:
            scores[i % 5000] = trainOnGame(model=model)
            if i % 5000 == 0:
                with open("scores" + str(j) + ".csv", mode='a') as file:
                    file.write(str(mean(scores)) + ";")
            i += 1
            print(i, end="\t")
        file.close()
