import tkinter as tk


class SolitaireApp:
    def __init__(self, root):
        self.root = root
        root.title("Solitaire")
        self.canvas = tk.Canvas(root, width=650, height=640, bg="darkgreen")
        self.canvas.pack()