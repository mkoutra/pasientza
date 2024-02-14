# The window of the pasientza game using tkinter.
import os
import tkinter as tk
from PIL import Image, ImageTk

from Cards import Card, Deck, SuitDeck
import random

class GameWindow:
    def __init__(self):
        # Window configuration
        self._win_dimensions = (1024, 800)
        self._background = "darkgreen"
        self._title = "Pasientza"

        self._card_img_folder = os.path.join("imgs", "card_imgs")
        self._card_dimensions = (100, 130)  # Card configuration
        self._card_images:dict = {}         # Card id, i.e. "10s" to card image

        # Testing Deck
        random.seed(100)
        self.__deck = Deck()
        print(self.__deck)

        self._all_SuitDeck_canvas:list = [] # SuitDeck canvas

        # Create root window
        self._root = tk.Tk()
        self._root.title(self._title)
        self._root.configure(background = self._background)
        self._root.geometry(str(self._win_dimensions[0])
                            + "x" + str(self._win_dimensions[1]))

        # Create Frames
        self._suitDecks_frame = tk.Frame(master = self._root, bg = self._background)
        self._deck_frame = tk.Frame(master = self._root, bg = self._background)
        self._soros_cards_frame = tk.Frame(master = self._root, bg = self._background)

        # Place frames on the root window
        self._suitDecks_frame.place(relx = 0, rely = 0.02, anchor = tk.NW)
        self._deck_frame.place(relx = 0, rely = .75, anchor = tk.NW)
        self._soros_cards_frame.place(relx = .2, rely = .75, anchor = tk.NW)

        self._load_cards(dim = self._card_dimensions) # Load Playing Cards

        # Create the 8 SuitDecks with Blank Images and place them on frame.
        for i in range(8):
            canv = tk.Canvas(master = self._suitDecks_frame,
                             width = self._card_dimensions[0],
                             height = self._card_dimensions[1])
            canv.grid(row = 0, column = i, padx = 10, sticky=tk.NW)
            canv.create_image(0, 0, anchor = tk.NW, 
                              image = self._card_images["Blank"])
            
            self._all_SuitDeck_canvas.append(canv)
        
        # Draw deck
        deck_canvas = tk.Canvas(master = self._deck_frame,
                                width = self._card_dimensions[0],
                                height = self._card_dimensions[1])
        deck_canvas.pack(padx = 10)
        deck_canvas.create_image(0, 0, anchor = tk.NW,
                                 image = self._card_images["Blue"])

        # Create three cards Canvas
        self._soros_cards_canvas = tk.Canvas(master = self._soros_cards_frame,
                                width = self._card_dimensions[0],
                                height = self._card_dimensions[1])
        self._soros_cards_canvas.pack()

        # Create Buttons
        self._shuffle_button = tk.Button(master = self._deck_frame,
                                         text = "Shuffle", width = 8, height = 1,
                                         command = self._test_button)
        
        self._shuffle_button.pack()


    def _draw_first_cards(self, deck:Deck, n:int = 3):
        """Given a deck, it draws the first n cards.
        n: int, default value is 3 """
        x_overlap = 20
        y_overlap = 0

        top_cards = deck.first_cards(n)    # First n cards

        for i, card in enumerate(top_cards):
            card_img = self._card_images[card.id()]
            overlap_images(self._soros_cards_canvas, card_img,
                           x_overlap, y_overlap, i)

    def _test_button(self):
        # print("Button Pressed")
        for _ in range(3): self.__deck.pop()
        self._draw_first_cards(self.__deck)


    def _load_cards(self, dim):
        """ Load the cards and resize them with the given dimensions dim"""
        # Load Deck
        for fname in os.listdir(self._card_img_folder):
            img = Image.open(os.path.join(self._card_img_folder ,fname))
            img = img.resize(dim)

            card_name = fname.strip(".png")
            self._card_images[card_name] = ImageTk.PhotoImage(img)
        
        # Load the Blank card
        img = Image.open(os.path.join("imgs" ,"Blank_img.jpg"))
        img = img.resize(dim)
        self._card_images["Blank"] = ImageTk.PhotoImage(img)

        # Load the Blue playing card
        img = Image.open(os.path.join("imgs" ,"Blue_playing_card.jpg"))
        img = img.resize(dim)
        self._card_images["Blue"] = ImageTk.PhotoImage(img)

    def draw_suitDeck_card(self, deck_id:int, card:Card, i:int):
        card_img = self._card_images[card.id()]        
        overlap_images(self._all_SuitDeck_canvas[deck_id], card_img, 0, 35, i)

    def draw(self):
        """Draw window"""
        self._root.mainloop()


# Helper functions
def find_card(cardname:str):
    """
    Finds the card with the cardname given and returns
    the image object for Tkinter frame, otherwise returns None.
    """
    try:
        img = Image.open(cardname)
        img = img.resize((100, 130))
    except:
        print("Error")
        return None

    return ImageTk.PhotoImage(img)

def overlap_images(canvas, img, overlap_x, overlap_y, n:int):
    """Insert the n-th image (counting starts from 0) on a canvas.
    Images overlap by overlap_x on x axis and by overlap_y on y axis.
    All images are assumed to have the same size."""

    # Modify canvas' size
    canvas.config(width = img.width() + n * overlap_x,
                  height = img.height() + n * overlap_y)

    # Draw image starting at position (n * overlap_x, n * overlap_y)
    # Anchor point is the axis origin
    canvas.create_image(n * overlap_x, n * overlap_y, anchor = tk.NW, image = img)

if __name__ == "__main__":
    c1 = Card('10', 's')
    c2 = Card('8', 'd')
    c3 = Card('A', 's')

    # random.seed(100)
    # d = Deck()
    win = GameWindow()

    # # win.draw_suitDeck_card(0, c1, 0)
    # # win.draw_suitDeck_card(0, c2, 1)
    # # win.draw_suitDeck_card(0, c3, 2)
    # for i in range(13):
    #     win.draw_suitDeck_card(0, c3, i)

    # print("Full ", d)
    # # win._draw_three(d)

    # print("Remove three ", d)
    # for _ in range(3):
    #     d.pop()
    # win._draw_first_cards(d)
    # win.draw_suitDeck_card(1, c3, 0)
    # win.draw_suitDeck_card(3, c2, 0)
    # win.draw_suitDeck_card(3, c1, 1)

    # win.draw_deck()
    # k = 0
    # while (True):
        # xarti = input("xarti: ")
        # win.draw_card(xarti + ".png", k, k)
        # k += 1
    win.draw()