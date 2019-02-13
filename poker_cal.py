# coding:utf-8


from poker import *
from poker_utils import *
import random

pack = create_pack()

random.shuffle(pack)

hand = []
for i in range(15):
    hand.append(pack.pop())

hand = sorted(hand, key=lambda poker: poker.value)
display_adv(hand)
display(hand)