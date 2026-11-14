SUITS = ["hearts", "diamonds", "spades", "clubs"]


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank          # 1 = Ace, 11 = Jack, 12 = Queen, 13 = King
        self.faceUp = False
        self.id = suit[0].upper() + str(rank)   # eg H5, S13

    def getColor(self):
        if self.suit == "hearts" or self.suit == "diamonds":
            return "red"
        return "black"

    def getRankName(self):
        names = {1: "A", 11: "J", 12: "Q", 13: "K"}
        if self.rank in names:
            return names[self.rank]
        return str(self.rank)