#!/usr/bin/python
#-*- coding: utf-8 -*-

from main import neuralNetAutoMain

from statistics import mean

from keras.models import Sequential
from keras.layers import Dense
from keras import optimizers
import numpy as np


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


def trainOnGame(model):
    """
    Play a game to save the best computed moves and feed the neural network .
    Arg:
        -model : the keras neural network model.
    """
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

        model = Sequential()  # Creates the foundation of the layers.
        model.add(Dense(input_dim=93, units=40, activation="sigmoid"))  # Dense is the basic form of a neural network layer, with input Layer of 93 and hidden Layer with 40 nodes
        model.add(Dense(units=1, activation="linear"))  # Output layer with 1 nodes (score)
        sgd = optimizers.SGD(lr=0.01, clipvalue=0.5)  # Stochastic gradient descent optimizer
        model.compile(loss="mse", optimizer=sgd, learning_rate=0.01)  # Create the model based on the information above

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
