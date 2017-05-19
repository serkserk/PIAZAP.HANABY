#!/usr/bin/python
#-*- coding: utf-8 -*-

from main import neuralNetAutoMain

import numpy as np

from keras import optimizers
from keras.layers import Dense
from keras.models import Sequential


def log2kb(log, score):
    kb = []
    for state in log:
        kb.append((state.toInputs(), [score]))
    return kb


def trainOnGame(model):
    log = neuralNetAutoMain(model=model)
    score = log[-1].getScore()
    # fit() method feeds states and target_f information to the model, which I explain below. You can ignore the rest parameters.
    # This training process makes the neural net to predict the reward value (target_f) from a certain state.
    for state in log:
        kb = np.array(state.toInputs()).reshape(1, 93)
        model.fit(kb, np.array(score).reshape(1, -1), epochs=1, verbose=0)
    print(score)
    return score


if __name__ == '__main__':

    model = Sequential()
    model.add(Dense(input_dim=93, units=40, activation="sigmoid"))
    model.add(Dense(units=1, activation="linear"))
    # model.summary()
    # sgd = optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    sgd = optimizers.SGD(lr=0.01, clipvalue=0.5)
    # model.compile(loss='mean_squared_error', optimizer=sgd)
    model.compile(loss="mse", optimizer=sgd, learning_rate=0.01)

    for _ in range(25000):
        trainOnGame(model)
    model.save("NeuralNetPlayer.pkl")
