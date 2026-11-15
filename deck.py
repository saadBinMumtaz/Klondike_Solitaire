import random
from card import Card, SUITS


class Deck:
    def __init__(self):
        self.cards = []
        for suit in SUITS:
            for rank in range(1, 14):
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        # Fisher-Yates shuffle
        for i in range(len(self.cards) - 1, 0, -1):
            j = random.randint(0, i)
            temp = self.cards[i]
            self.cards[i] = self.cards[j]
            self.cards[j] = temp