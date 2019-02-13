# coding:utf-8


class Poker(object):

    VALUES = ['A', '2', '3', '4', '5', '6', '7', '8',
              '9', 'T', 'J', 'Q', 'K', 'joker', 'Joker']
    SUITS = ['♥', '♠', '♣', '♦', 'JOKER']
    JOKER = 'JOKER'

    def __init__(self, value='Joker', suit=SUITS[-1]):
        if isinstance(value, int) and 0 <= value < len(Poker.VALUES):
            self.value = value
        elif value in Poker.VALUES:
            self.value = Poker.VALUES.index(value)
        else:
            raise Exception(f'Invalid poker value {type(value)}: {value}')

        if isinstance(suit, int) and 0 <= suit < len(Poker.SUITS):
            self.suit = suit
        elif suit in Poker.SUITS:
            self.suit = Poker.SUITS.index(suit)
        else:
            raise Exception(f'Invalid poker suit {type(suit)}: {suit}')

        if not self.is_joker() and self.get_suit() == Poker.JOKER:
            raise Exception(
                f'Invalid poker. Value [{self.get_value()}]. Suit [{self.get_suit()}]')

    def __str__(self):
        if self.suit < len(Poker.SUITS) - 1:
            return f'{Poker.SUITS[self.suit]}{Poker.VALUES[self.value]}'
        return Poker.VALUES[self.value]

    def __lt__(self, poker):
        return self.value < poker.value

    def __le__(self, poker):
        return self.value <= poker.value

    def __gt__(self, poker):
        return self.value > poker.value

    def __ge__(self, poker):
        return self.value >= poker.value

    def __eq__(self, poker):
        return self.value == poker.value

    def __ne__(self, poker):
        return self.value != poker.value

    def get_value(self):
        return Poker.VALUES[self.value]

    def get_suit(self):
        return Poker.SUITS[self.suit]

    def is_joker(self):
        return len(Poker.VALUES) - 3 < self.value < len(Poker.VALUES)
