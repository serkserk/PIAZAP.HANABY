#!/usr/bin/python
#-*- coding: utf-8 -*-
import random
from suit import *
from card import *


class Deck:
    N_SHUFFLES = 100

    def __init__(self, seed=None):
        self.deck = []
        self._seed = seed
        suits = [Suit.white, Suit.red, Suit.blue, Suit.green, Suit.yellow]

        # creating the deck with 3 ones, 2 2s, 3s & 4s and 1 5 for each suit
        for s in suits:
            for i in range(3):
                self.deck.append(Card(s, 1))
            for i in range(2, 5):
                for j in range(2):
                    self.deck.append(Card(s, i))
            self.deck.append(Card(s, 5))

    def shuffle(self, seed=None):
        if seed is None:
            # I would love for self._seed to be the default value of seed,
            # calling self in a default value isn't syntactically correct in Python
            seed = self._seed
        random.seed(seed)
        random.shuffle(self.deck)

    def sort(self):
        self.deck.sort()

    def draw(self):
        if not self.empty():
            return self.deck.pop()

    def display(self):
        for i in self.deck:
            print(i.toString())

    def empty(self):
        return len(self.deck) <= 0

    def cardsLeft(self):
        return len(self.deck)
