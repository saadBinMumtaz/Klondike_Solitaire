from deck import Deck
from card import SUITS
from pile import StackPile, TableauPile, Stock
from move import Move
from structures.stack import Stack

tableauNames = ["T1", "T2", "T3", "T4", "T5", "T6", "T7"]
foundationNames = ["Fhearts", "Fdiamonds", "Fspades", "Fclubs"]


class Game:
    def __init__(self, drawCount=1):
        self.drawCount = drawCount    
        self.piles = {}               
        self.cardLocation = {}        
        self.undoStack = Stack()
        self.redoStack = Stack()
        self.setupGame()

    def setupGame(self):
        deck = Deck()
        deck.shuffle()

        for name in tableauNames:
            self.piles[name] = TableauPile()
        for suit in SUITS:
            self.piles["F" + suit] = StackPile(suit)
        self.piles["waste"] = StackPile()
        self.piles["stock"] = Stock()

        # deal 1 card to T1, 2 to T2 ... 7 to T7, only the last card is face up
        index = 0
        for i in range(7):
            for j in range(i + 1):
                card = deck.cards[index]
                index = index + 1
                card.faceUp = (j == i)
                self.put(tableauNames[i], [card])

        # the remaining 24 cards go to the stock
        self.put("stock", deck.cards[index:])

    def put(self, name, cards):
        # adds cards to a pile and updates the location dictionary
        self.piles[name].addCards(cards)
        for card in cards:
            self.cardLocation[card.id] = name

    def record(self, move):
        self.undoStack.push(move)
        self.redoStack = Stack()     # a new move clears the redo history

    def draw(self):
        stock = self.piles["stock"]
        waste = self.piles["waste"]
        if stock.size() == 0:
            if waste.size() == 0:
                return False
            # stock is empty, so flip the waste in the stock
            cards = waste.removeLast(waste.size())
            self.put("stock", cards)
            self.record(Move("recycle", "waste", "stock", len(cards), False))
            return True
        cards = stock.draw(self.drawCount)
        self.put("waste", cards)
        self.record(Move("draw", "stock", "waste", len(cards), False))
        return True

    def canMove(self, sourceName, destName, count):
        if sourceName == destName:
            return False
        source = self.piles[sourceName]
        dest = self.piles[destName]
        if count < 1 or count > source.size():
            return False
        # only tableau piles can move several cards, and never onto a foundation
        if count > 1 and (sourceName[0] != "T" or destName[0] == "F"):
            return False
        firstCard = source.cardFromTop(count)    # bottom card of the moving group
        return firstCard.faceUp and dest.canAccept(firstCard)

    def move(self, sourceName, destName, count):
        if not self.canMove(sourceName, destName, count):
            return False
        cards = self.piles[sourceName].removeLast(count)
        self.put(destName, cards)
        flipped = False
        if sourceName[0] == "T":
            flipped = self.piles[sourceName].flipTop()   # flip the new top card
        self.record(Move("move", sourceName, destName, count, flipped))
        return True

    def undo(self):
        move = self.undoStack.pop()
        if move is None:
            return False
        if move.kind == "draw":
            cards = self.piles["waste"].removeLast(move.count)
            self.piles["stock"].putBackOnFront(cards)
            for card in cards:
                self.cardLocation[card.id] = "stock"
        elif move.kind == "recycle":
            cards = self.piles["stock"].takeAll()
            for card in cards:
                card.faceUp = True
            self.put("waste", cards)
        else:
            cards = self.piles[move.dest].removeLast(move.count)
            if move.flipped:
                self.piles[move.source].topCard().faceUp = False   # turn it back face down
            self.put(move.source, cards)
        self.redoStack.push(move)
        return True        