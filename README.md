# Klondike Solitaire

A GUI Solitaire game with Klondike rules, made in Python with Tkinter for DSA mid term project.

## How to run

Python 3.10 or newer is needed. Tkinter comes with Python, so nothing needs to be installed.

    python main.py

## Rules

- The 52 cards are shuffled and dealt into 7 tableau piles with 1, 2, 3 ... 7 cards. Only the last card of each pile is face up.
- The other 24 cards form the stock. Clicking it moves 1 or 3 cards to the waste pile. When the stock is empty, clicking it flips the waste back into the stock.
- Cards move between tableau piles in descending rank and alternating colors, for example a red 6 on a black 7. Several face up cards in a sequence can be moved together.
- Only a King can be placed on an empty tableau pile.
- When a card leaves a tableau pile, the face down card under it turns face up.
- The four foundation piles are built from Ace to King, one suit each.
- The game is won when all 52 cards are on the foundations.

## Controls

- Click a face up card to select it, then click the pile it should go to.
- Double click a card to send it to its foundation.
- Click the stock to draw.
- New Game, Undo, Redo and Hint buttons are in the top bar.
- Turn 1 or Turn 3 chooses how many cards are drawn at a time. Changing it starts a new game.
- The timer and the score are shown on the right of the top bar.

## Scoring

- Card to a foundation: +10
- Waste card to a tableau pile: +5
- Foundation card back to a tableau pile: -15
- Undo takes back the points of the move it reverses.

## Data structures used

| Structure | Where it is used |
|---|---|
| Stack | Foundation piles, waste pile, undo history and redo history |
| Queue | Stock pile. Cards are drawn in first in, first out order. It keeps a head index so dequeue takes O(1). |
| Linked list | Tableau piles. Moving a group of cards means cutting the list at a node with splitFrom. |
| List | The deck of 52 cards, shuffled with Fisher-Yates in O(n) |
| Dictionary | piles maps a pile name to the pile object. cardLocation maps a card id to the name of its pile. |

All the stack, queue and linked list classes are written by hand, without using Python's built in deque or queue modules.

## Design notes

- Undo and redo use the command pattern. Every draw, recycle and move is saved as a Move object that stores the source, destination, card count and whether a card was flipped.
- One move() function handles every kind of move, and canMove() holds all the rules in one place.
- The game logic (game.py, pile.py) does not depend on the GUI (gui.py).

## Files

- structures/ : Stack, Queue and LinkedList
- card.py, deck.py : card class, deck and shuffle
- pile.py : foundation, waste, tableau and stock piles
- move.py : the Move object for undo and redo
- game.py : setup, rules, moves, undo, redo, hint and win check
- gui.py : the Tkinter window and drawing
- main.py : starts the game