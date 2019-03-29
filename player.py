# coding:utf-8

from poker import *


class Player:
    def __init__(self, name, score=0):
        self.name = name
        self.score = score
        self.hand = []

    def draw(self, pack):
        if not pack:
            print('No card exists in this pack.')
            return False
        card = pack.pop()
        self.hand.append(card)
        self.hand = sorted(
            self.hand, key=lambda poker: poker.value, reverse=True)
        return True

    def reset(self):
        self.hand = []

    def display_hand(self):
        return display(self.hand)
