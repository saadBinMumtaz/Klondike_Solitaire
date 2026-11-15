import tkinter as tk
from card import SUITS
from game import Game, tableauNames, foundationNames

SYMBOLS = {"hearts": "♥", "diamonds": "♦", "spades": "♠", "clubs": "♣"}


class SolitaireApp:
    def __init__(self, root):
        self.root = root
        root.title("Solitaire")
        root.geometry("1000x700")
        root.state("zoomed")      # start maximized (Windows and Mac only, delete on Linux)

        self.canvas = tk.Canvas(root, width=100, height=100, bg="darkgreen")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self.onResize)
        self.canvas.bind("<Button-1>", self.onClick)

        self.updateSize(1000, 700)
        self.hits = []          # clickable areas, filled by redraw
        self.selected = None    # used in a later commit
        self.newGame()

    def updateSize(self, width, height):
        # works out every size from the window size
        self.top = 15
        widthLimit = width * 0.94 / 8.5                 # 7 columns need about 8.5 card widths
        self.cardH = min(widthLimit * 1.4, (height - self.top) / 6)
        self.cardW = self.cardH / 1.4
        self.gap = self.cardW * 1.25                    # distance between columns
        self.left = (width - (6 * self.gap + self.cardW)) / 2    # centers the layout
        self.downGap = self.cardH * 0.12                # vertical gap for a face down card in a pile
        self.upGap = self.cardH * 0.25                  # vertical gap for a face up card in a pile
        self.tableauY = self.top + self.cardH * 1.2     # where the 7 piles start
        self.fontSize = max(8, int(self.cardW * 0.22))

    def onResize(self, event):
        self.updateSize(event.width, event.height)
        self.redraw()

    def newGame(self):
        self.game = Game()
        self.selected = None
        self.redraw()

    def addHit(self, x, y, name, index):
        self.hits.append((x, y, x + self.cardW, y + self.cardH, name, index))

    def findHit(self, x, y):
        # check from the last drawn (top most) to the first
        for i in range(len(self.hits) - 1, -1, -1):
            x1, y1, x2, y2, name, index = self.hits[i]
            if x1 <= x <= x2 and y1 <= y <= y2:
                return (name, index)
        return None

    def onClick(self, event):
        hit = self.findHit(event.x, event.y)
        if hit is not None and hit[0] == "stock":
            self.game.draw()
            self.redraw()

    def isSelected(self, name, index):
        if self.selected is None:
            return False
        selectedName, selectedCount = self.selected
        if name != selectedName:
            return False
        return index >= self.game.piles[name].size() - selectedCount

    def drawSlot(self, x, y, label=""):
        self.canvas.create_rectangle(x, y, x + self.cardW, y + self.cardH, outline="white")
        self.canvas.create_text(x + self.cardW / 2, y + self.cardH / 2, text=label, fill="white", font=("Arial", self.fontSize))

    def drawTopCard(self, name, x, y, label=""):
        # draws only the top card of a pile (waste and foundations)
        pile = self.game.piles[name]
        self.drawSlot(x, y, label)
        self.addHit(x, y, name, -1)
        card = pile.topCard()
        if card is not None:
            self.drawCard(x, y, card, self.isSelected(name, pile.size() - 1))
            self.addHit(x, y, name, pile.size() - 1)

    def redraw(self):
        self.canvas.delete("all")
        self.hits = []
        game = self.game

        # stock
        stock = game.piles["stock"]
        self.drawSlot(self.left, self.top, "↻")
        self.addHit(self.left, self.top, "stock", -1)
        if stock.size() > 0:
            self.drawBack(self.left, self.top)
            self.canvas.create_text(self.left + self.cardW / 2, self.top + self.cardH / 2, text=str(stock.size()), fill="white", font=("Arial", self.fontSize))

        # waste
        self.drawTopCard("waste", self.left + self.gap, self.top)

        # foundations
        for i in range(4):
            self.drawTopCard(foundationNames[i], self.left + (3 + i) * self.gap, self.top, SYMBOLS[SUITS[i]])

        # tableau
        for i in range(7):
            name = tableauNames[i]
            x = self.left + i * self.gap
            y = self.tableauY
            self.drawSlot(x, y)
            self.addHit(x, y, name, -1)
            cards = game.piles[name].toList()
            for index in range(len(cards)):
                card = cards[index]
                self.drawCard(x, y, card, self.isSelected(name, index))
                self.addHit(x, y, name, index)
                if card.faceUp:
                    y = y + self.upGap
                else:
                    y = y + self.downGap

    def drawBack(self, x, y):
        self.canvas.create_rectangle(x, y, x + self.cardW, y + self.cardH, fill="navy", outline="white")

    def drawCard(self, x, y, card, selected=False):
        if not card.faceUp:
            self.drawBack(x, y)
            return
        outline = "yellow" if selected else "black"
        width = 4 if selected else 1
        self.canvas.create_rectangle(x, y, x + self.cardW, y + self.cardH, fill="white", outline=outline, width=width)
        text = card.getRankName() + SYMBOLS[card.suit]
        offset = self.cardW * 0.08
        self.canvas.create_text(x + offset, y + offset, text=text, fill=card.getColor(), anchor="nw", font=("Arial", self.fontSize, "bold"))