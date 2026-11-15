from structures.stack import Stack
from structures.linkedlist import LinkedList

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

class TableauPile:
    def __init__(self):
        self.cards = LinkedList()    # first = bottom card, last = top card

    def canAccept(self, card):
        top = self.topCard()
        if top is None:
            return card.rank == 13       # only a King on an empty pile
        return top.faceUp and card.getColor() != top.getColor() and card.rank == top.rank - 1

    def addCards(self, cards):
        for card in cards:
            self.cards.append(card)

    def removeLast(self, count):
        # cuts the last count (linked list)
        return self.cards.splitFrom(self.cards.size() - count).toList()

    def topCard(self):
        return self.cards.get(self.cards.size() - 1)

    def cardFromTop(self, count):
        return self.cards.get(self.cards.size() - count)

    def flipTop(self):
        # face up top card, returns True if flip
        card = self.topCard()
        if card is not None and not card.faceUp:
            card.faceUp = True
            return True
        return False

    def size(self):
        return self.cards.size()

    def toList(self):
        return self.cards.toList()