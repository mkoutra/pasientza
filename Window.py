# The window of the pasientza game using tkinter.
import os
import tkinter as tk
from PIL import Image, ImageTk

from Cards import Card

class GameWindow:
    def __init__(self):
        # Window configuration
        self._win_dimensions = (1024, 800)
        self._background = "darkgreen"
        self._title = "Pasientza"
        self._card_img_folder = os.path.join("imgs", "card_imgs")

        # Card configuration
        self._card_dimensions = (100, 130)

        # Maps card id (e.g. "10s") to card image
        self._card_images:dict = {}

        # Collection of 8 canvas used to draw the SuitDecks
        self._all_SuitDeck_canvas:list = []

        # Create root window
        self._root = tk.Tk()
        self._root.title(self._title)
        self._root.configure(background = self._background)
        self._root.geometry(str(self._win_dimensions[0]) + "x"
                            + str(self._win_dimensions[1]))

        # Frame containing the eight SuitDecks
        self._suitDecks_frame = tk.Frame(master = self._root,
                                         bg = self._background)
        self._suitDecks_frame.place(relx = 0, rely = 0.02, anchor = tk.NW)

        # Load Playing Cards
        for fname in os.listdir(self._card_img_folder):
            img = Image.open(os.path.join(self._card_img_folder ,fname))
            img = img.resize(self._card_dimensions)

            card_name = fname.strip(".png")
            self._card_images[card_name] = ImageTk.PhotoImage(img)
        
        # Load the Blank card
        img = Image.open(os.path.join("imgs" ,"Blank_img.jpg"))
        img = img.resize(self._card_dimensions)
        self._card_images["Blank"] = ImageTk.PhotoImage(img)

        # Load the Blue playing card
        img = Image.open(os.path.join("imgs" ,"Blue_playing_card.jpg"))
        img = img.resize(self._card_dimensions)
        self._card_images["Blue"] = ImageTk.PhotoImage(img)

        # Create the eight SuitDecks with Blank Image on front.
        for i in range(8):
            canv = tk.Canvas(master = self._suitDecks_frame,
                             width = self._card_dimensions[0],
                             height = self._card_dimensions[1])

            canv.grid(row = 0, column = i, padx = 10, sticky=tk.NW)
            
            canv.create_image(0, 0, anchor = tk.NW, 
                              image = self._card_images["Blue"])

            self._all_SuitDeck_canvas.append(canv)

    def draw_card(self, card_id:str, row, col):
        img = find_card(os.path.join(self._card_img_folder, card_id))
        lbl = tk.Label(master = self._root, image = img)
        lbl.image = img
        lbl.grid(row = row, column = col, padx = 5, pady = 5)

    def draw_card_in_suitDeck(self, deck_id:int, card:Card, i:int):
        card_img = self._card_images[card.id()]        
        overlap_images(self._all_SuitDeck_canvas[deck_id], card_img, i, 0, 35)

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

def overlap_images(canvas, image, i:int, overlap_x, overlap_y):
    width, height = image.width(), image.height()

    # Calculate the total size of the canvas
    canvas_width = max(width, width + overlap_x)
    canvas_height = max(height, (height + i*overlap_y))

    # Create a Canvas widget with the calculated size
    canvas.config(width = canvas_width, height = canvas_height)

    # Draw an image at position (overlap_x, i*overlap_y) measured from anchor point
    canvas.create_image(overlap_x, i * overlap_y, anchor=tk.NW, image=image)

if __name__ == "__main__":
    c1 = Card('10', 's')
    c2 = Card('8', 'd')
    c3 = Card('A', 's')
    win = GameWindow()

    # win.draw_card_in_suitDeck(0, c1, 0)
    # win.draw_card_in_suitDeck(0, c2, 1)
    # win.draw_card_in_suitDeck(0, c3, 2)
    for i in range(13):
        win.draw_card_in_suitDeck(0, c3, i)

    # win.draw_card_in_suitDeck(1, c3, 0)
    # win.draw_card_in_suitDeck(3, c2, 0)
    # win.draw_card_in_suitDeck(3, c1, 1)

    # win.draw_deck()
    # k = 0
    # while (True):
        # xarti = input("xarti: ")
        # win.draw_card(xarti + ".png", k, k)
        # k += 1
    win.draw()