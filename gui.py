import tkinter as tk
from card import SUITS
from game import Game, tableauNames, foundationNames

SYMBOLS = {"hearts": "♥", "diamonds": "♦", "spades": "♠", "clubs": "♣"}
FELT = "#1e5a2c"
SHADOW = "#0b2e14"
RED = "#d6232a"
BLACK = "#1a1a1a"

# where the symbols go for ranks 2 to 10, as fractions of the card (0 to 1)
PIPS = {
    2: [(0.5, 0.26), (0.5, 0.74)],
    3: [(0.5, 0.26), (0.5, 0.5), (0.5, 0.74)],
    4: [(0.34, 0.26), (0.66, 0.26), (0.34, 0.74), (0.66, 0.74)],
    5: [(0.34, 0.26), (0.66, 0.26), (0.5, 0.5), (0.34, 0.74), (0.66, 0.74)],
    6: [(0.34, 0.26), (0.66, 0.26), (0.34, 0.5), (0.66, 0.5), (0.34, 0.74), (0.66, 0.74)],
    7: [(0.34, 0.26), (0.66, 0.26), (0.34, 0.5), (0.66, 0.5), (0.34, 0.74), (0.66, 0.74), (0.5, 0.38)],
    8: [(0.34, 0.26), (0.66, 0.26), (0.34, 0.5), (0.66, 0.5), (0.34, 0.74), (0.66, 0.74), (0.5, 0.38), (0.5, 0.62)],
    9: [(0.34, 0.26), (0.66, 0.26), (0.34, 0.42), (0.66, 0.42), (0.34, 0.58), (0.66, 0.58), (0.34, 0.74), (0.66, 0.74), (0.5, 0.5)],
    10: [(0.34, 0.26), (0.66, 0.26), (0.34, 0.42), (0.66, 0.42), (0.34, 0.58), (0.66, 0.58), (0.34, 0.74), (0.66, 0.74), (0.5, 0.34), (0.5, 0.66)],
}


class SolitaireApp:
    def __init__(self, root):
        self.root = root
        root.title("Solitaire")
        root.geometry("1000x700")
        root.state("zoomed")      # start maximized (Windows and Mac only, delete on Linux)

        self.canvas = tk.Canvas(root, width=100, height=100, bg=FELT, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self.onResize)
        self.canvas.bind("<Button-1>", self.onClick)

        self.updateSize(1000, 700)
        self.hits = []          # clickable areas, filled by redraw
        self.selected = None    # used in a later commit
        self.newGame()

    def updateSize(self, width, height):
        # works out every size from the window size
        self.height = height
        self.top = 12
        widthLimit = width * 0.96 / 8.2                 # 7 columns need about 8.2 card widths
        self.cardH = min(widthLimit * 1.4, (height - self.top) / 4.8)
        self.cardW = self.cardH / 1.4
        self.gap = self.cardW * 1.2                     # distance between columns
        self.left = (width - (6 * self.gap + self.cardW)) / 2    # centers the layout
        self.downGap = self.cardH * 0.10                # vertical gap for a face down card in a pile
        self.upGap = self.cardH * 0.22                  # vertical gap for a face up card in a pile
        self.tableauY = self.top + self.cardH * 1.15    # where the 7 piles start
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
        if hit is None:
            self.selected = None
        elif hit[0] == "stock":
            self.selected = None
            self.game.draw()
        elif self.selected is not None and self.game.move(self.selected[0], hit[0], self.selected[1]):
            self.selected = None
        else:
            self.select(hit[0], hit[1])
        self.redraw()

    def isSelected(self, name, index):
        if self.selected is None:
            return False
        selectedName, selectedCount = self.selected
        if name != selectedName:
            return False
        return index >= self.game.piles[name].size() - selectedCount

    def select(self, name, index):
        pile = self.game.piles[name]
        if index == -1:
            self.selected = None
            return
        count = pile.size() - index
        card = pile.cardFromTop(count)
        if not card.faceUp or self.selected == (name, count):
            self.selected = None       # face down card, or clicked the same card again
        else:
            self.selected = (name, count)

    def roundedRect(self, x1, y1, x2, y2, r, **options):
        # a rectangle with rounded corners, drawn as a smooth polygon
        points = [x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r, x2, y2 - r, x2, y2,
                  x2 - r, y2, x1 + r, y2, x1, y2, x1, y2 - r, x1, y1 + r, x1, y1]
        return self.canvas.create_polygon(points, smooth=True, **options)

    def drawSlot(self, x, y, label=""):
        self.roundedRect(x, y, x + self.cardW, y + self.cardH, self.cardW * 0.08, fill="", outline="#4f9a60", width=2)
        self.canvas.create_text(x + self.cardW / 2, y + self.cardH / 2, text=label, fill="#4f9a60", font=("Arial", self.fontSize * 2))

    def drawTopCard(self, name, x, y, label=""):
        # draws only the top card of a pile (waste and foundations)
        pile = self.game.piles[name]
        self.drawSlot(x, y, label)
        self.addHit(x, y, name, -1)
        card = pile.topCard()
        if card is not None:
            self.drawCard(x, y, card, self.isSelected(name, pile.size() - 1))
            self.addHit(x, y, name, pile.size() - 1)

    def pileShrink(self, cards):
        # makes the gaps smaller when a pile is too tall for the window
        total = 0
        for card in cards[:-1]:
            if card.faceUp:
                total = total + self.upGap
            else:
                total = total + self.downGap
        available = self.height - self.tableauY - self.cardH - 8
        if total > available and total > 0:
            return available / total
        return 1

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
            self.canvas.create_text(self.left + self.cardW / 2, self.top + self.cardH / 2, text=str(stock.size()), fill="#7a1219", font=("Arial", -int(self.cardW * 0.22), "bold"))

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
            shrink = self.pileShrink(cards)
            for index in range(len(cards)):
                card = cards[index]
                self.drawCard(x, y, card, self.isSelected(name, index))
                self.addHit(x, y, name, index)
                if card.faceUp:
                    y = y + self.upGap * shrink
                else:
                    y = y + self.downGap * shrink

    def drawBack(self, x, y):
        w = self.cardW
        h = self.cardH
        radius = w * 0.08
        self.roundedRect(x + 2, y + 2, x + w + 2, y + h + 2, radius, fill=SHADOW, outline="")
        self.roundedRect(x, y, x + w, y + h, radius, fill="white", outline="#555555")
        self.roundedRect(x + w * 0.07, y + h * 0.05, x + w * 0.93, y + h * 0.95, radius, fill="#b3262e", outline="")
        cx = x + w / 2
        cy = y + h / 2
        self.canvas.create_polygon(cx, cy - h * 0.17, cx + w * 0.22, cy, cx, cy + h * 0.17, cx - w * 0.22, cy, fill="white", outline="")

    def drawCard(self, x, y, card, selected=False):
        if not card.faceUp:
            self.drawBack(x, y)
            return
        w = self.cardW
        h = self.cardH
        radius = w * 0.08
        symbol = SYMBOLS[card.suit]
        if card.getColor() == "red":
            color = RED
        else:
            color = BLACK
        if selected:
            outline = "#ffd400"
            width = 4
        else:
            outline = "#555555"
            width = 1

        # shadow, then the card itself
        self.roundedRect(x + 2, y + 2, x + w + 2, y + h + 2, radius, fill=SHADOW, outline="")
        self.roundedRect(x, y, x + w, y + h, radius, fill="white", outline=outline, width=width)

        # rank and suit in the top left corner, and upside down in the bottom right corner
        cornerFont = ("Arial", -int(max(8, w * 0.22)), "bold")
        text = card.getRankName() + symbol
        self.canvas.create_text(x + w * 0.24, y + h * 0.09, text=text, fill=color, font=cornerFont)
        self.canvas.create_text(x + w * 0.76, y + h * 0.91, text=text, fill=color, font=cornerFont, angle=180)

        # the middle of the card
        rank = card.rank
        if rank == 1:
            self.canvas.create_text(x + w / 2, y + h / 2, text=symbol, fill=color, font=("Arial", -int(w * 0.6)))
        elif rank >= 11:
            self.canvas.create_rectangle(x + w * 0.2, y + h * 0.2, x + w * 0.8, y + h * 0.8, outline=color)
            self.canvas.create_text(x + w / 2, y + h * 0.42, text=card.getRankName(), fill=color, font=("Arial", -int(w * 0.42), "bold"))
            self.canvas.create_text(x + w / 2, y + h * 0.66, text=symbol, fill=color, font=("Arial", -int(w * 0.28)))
        else:
            pipFont = ("Arial", -int(w * 0.25))
            for px, py in PIPS[rank]:
                angle = 0
                if py > 0.5:
                    angle = 180        # symbols in the bottom half are upside down, like a real card
                self.canvas.create_text(x + w * px, y + h * py, text=symbol, fill=color, font=pipFont, angle=angle)