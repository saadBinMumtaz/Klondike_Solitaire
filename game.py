from deck import Deck
from card import SUITS
from pile import StackPile, TableauPile, Stock

tableauNames = ["T1", "T2", "T3", "T4", "T5", "T6", "T7"]
foundationNames = ["Fhearts", "Fdiamonds", "Fspades", "Fclubs"]


class Game:
    def __init__(self, drawCount=1):
        self.drawCount = drawCount    
        self.piles = {}               
        self.cardLocation = {}        
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

        # deal in triangular only 1 face up

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
        # adds cards to pile & update location dictionary
        self.piles[name].addCards(cards)
        for card in cards:
            self.cardLocation[card.id] = name

    def draw(self):
        stock = self.piles["stock"]
        waste = self.piles["waste"]
        if stock.size() == 0:
            if waste.size() == 0:
                return False
        
        # remaining cards in stock
        
            cards = waste.removeLast(waste.size())
            self.put("stock", cards)
            return True
        cards = stock.draw(self.drawCount)
        self.put("waste", cards)
        return True