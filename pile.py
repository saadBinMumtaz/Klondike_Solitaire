from structures.stack import Stack


class StackPile:
    # used for foundation and waste
    def __init__(self, suit=None):
        self.suit = suit
        self.stack = Stack()

    def canAccept(self, card):
        if self.suit is None or card.suit != self.suit:
            return False
        if self.stack.isEmpty():
            return card.rank == 1
        return card.rank == self.stack.peek().rank + 1

    def addCards(self, cards):
        for card in cards:
            self.stack.push(card)

    def removeLast(self, count):
        # removes then return in their original order
        cards = []
        for i in range(count):
            cards.insert(0, self.stack.pop())
        return cards

    def topCard(self):
        return self.stack.peek()

    def cardFromTop(self, count):
        return self.stack.items[self.stack.size() - count]

    def size(self):
        return self.stack.size()