# coding:utf-8

import random
from poker import *
from prettytable import PrettyTable


def is_joker(value):
    if isinstance(value, Poker):
        return value.is_joker()
    if isinstance(value, int):
        return len(Poker.VALUES) - 2 < value < len(Poker.VALUES) - 1
    return value.upper() == Poker.JOKER


def multi_poker(value_list, suit_list):
    result = []
    for (value, suit) in zip(value_list, suit_list):
        result.append(Poker(value, suit))
    return result


def create_pack(with_joker=True):
    pack = []
    for value in Poker.VALUES:
        if is_joker(value):
            if with_joker:
                pack.append(Poker(value))
            continue
        for suit in Poker.SUITS[:-1]:
            pack.append(Poker(value, suit))
    random.shuffle(pack)
    return pack


def display(poker_list, sep=' '):
    result = sep.join(str(poker) for poker in poker_list)
    return result


def init_stat_table():
    stat_table = {}
    for suit in Poker.SUITS:
        stat_table[suit] = {}
        for value in Poker.VALUES:
            stat_table[suit][value] = 0
    return stat_table


def update_stat_table(stat_table, poker_list):
    for poker in poker_list:
        stat_table[poker.get_suit()][poker.get_value()] += 1


def display_adv(poker_list):
    stat_table = init_stat_table()
    update_stat_table(stat_table, poker_list)

    fields = ['Values']
    fields.extend(Poker.SUITS)
    table = PrettyTable(fields)
    for value in Poker.VALUES:
        line = [value]
        for suit in Poker.SUITS:
            line.append(str(stat_table[suit][value]))
        table.add_row(line)
    return table
