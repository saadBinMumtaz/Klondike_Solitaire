import tkinter as tk
from card import Card

SYMBOLS = {"hearts": "♥", "diamonds": "♦", "spades": "♠", "clubs": "♣"}


class SolitaireApp:
    def __init__(self, root):
        self.root = root
        root.title("Solitaire")
        root.geometry("1000x700")
        root.state("zoomed")      

        self.canvas = tk.Canvas(root, width=100, height=100, bg="darkgreen")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self.onResize)

        self.updateSize(1000, 700)

    def updateSize(self, width, height):
        # works out every size 
        self.top = 15
        widthLimit = width * 0.94 / 8.5                             # 7 columns need about 8.5 card widths
        self.cardH = min(widthLimit * 1.4, (height - self.top) / 6)
        self.cardW = self.cardH / 1.4
        self.gap = self.cardW * 1.25                                # distance b/w columns
        self.left = (width - (6 * self.gap + self.cardW)) / 2       # center layout
        self.downGap = self.cardH * 0.12                            # vert gap for a face down
        self.upGap = self.cardH * 0.25                              # vert gap for a face up
        self.tableauY = self.top + self.cardH * 1.2                 # starting of 7 pile
        self.fontSize = max(8, int(self.cardW * 0.22))

    def onResize(self, event):
        self.updateSize(event.width, event.height)
        self.redraw()

    def redraw(self):
        self.canvas.delete("all")
        # temporary test card
        test = Card("hearts", 5)
        test.faceUp = True
        self.drawCard(self.left, self.top, test)
        self.drawCard(self.left + self.gap, self.top, Card("spades", 13))

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