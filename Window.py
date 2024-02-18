# The window of the Pasientza game using tkinter.
import os
import copy
import tkinter as tk
from PIL import Image, ImageTk

from Cards import Card, Deck, SuitDeck

class GameWindow:
    def __init__(self, deck):
        # Create decks needed to play the game
        self.__deck = deck
        print("Initial Deck\n", self.__deck)
        self.__soros = Deck(full = False)   # Cards removed from deck
        self.__suit_decks:list = [SuitDeck() for _ in range(8)]

        # Window configuration
        self._win_dimensions = (980, 650)
        self._background = "seagreen4"
        self._title = "Pasientza"

        # Images info
        self._img_folder = "imgs"
        self._card_img_folder = "card_imgs"
        self._card_dimensions = (100, 130)
        self._card_images:dict = {} # Card id, e.g. "10s" to image

        # Buttons configuration
        button_configuration = {"background": "steelblue3",
                                "activebackground": "steelblue4",
                                "foreground": "white",
                                "activeforeground": "white"}
        
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
        self._undo_frame = tk.Frame(master = self._root, bg = self._background) # Undo button

        # Place frames on the root window
        self._suitDecks_frame.place(relx = 0.0, rely = 0.02, anchor = tk.NW)
        self._deck_frame.place(relx = 0.4, rely = .75, anchor = tk.NW)
        self._soros_cards_frame.place(relx = 0.4 + .15, rely = .75, anchor = tk.NW)
        self._undo_frame.place(relx = .85, rely = .9, anchor = tk.NW)

        self._load_images(dim = self._card_dimensions) # Load Playing Cards

        # Create the 8 SuitDecks with the corresponding buttons.
        self._all_SuitDeck_canvas:list = [] # SuitDeck canvas

        for i in range(8):
            # Create frame to store canvas and button
            suitDeck_frame = tk.Frame(master = self._suitDecks_frame,
                                      bg = self._background)

            # Create suitDeck button
            suitDeck_but = tk.Button(master = suitDeck_frame,
                text = "Deck " + str(i + 1),
                width = 8, height = 1,
                **button_configuration,
                command = lambda x = i : self._pick_suitDeck_callback(x))
            
            # Create Canvas
            canv = tk.Canvas(master = suitDeck_frame,
                             width = self._card_dimensions[0],
                             height = self._card_dimensions[1])
            canv.create_image(0, 0, anchor = tk.NW, 
                              image = self._card_images["Blank"])
            self._all_SuitDeck_canvas.append(canv)

            suitDeck_frame.grid(row = 0, column = i, padx = 10, sticky=tk.NW)       
            suitDeck_but.pack(pady = 5)
            canv.pack(pady = 5)

        # Create Deck Button
        self._deck_button = tk.Button(master = self._deck_frame,
                                      image = self._card_images["Blue"],
                                      activebackground = "steelblue3",
                                      relief = tk.RAISED,
                                      command = self._deck_button_callback)
        self._deck_button.pack(padx = 10)

        # Create Soros (three cards) Canvas
        self._soros_cards_canvas = tk.Canvas(master = self._soros_cards_frame,
                                             width = self._card_dimensions[0],
                                             height = self._card_dimensions[1])
        self._soros_cards_canvas.pack()
        self._soros_cards_canvas.create_image(0, 0, anchor = tk.NW,
                                              image = self._card_images["Blank"])
        
        # Create Undo Button
        self._undo_button = tk.Button(master = self._undo_frame,
                                      text = "Undo",
                                      width = 4, height = 1,
                                      **button_configuration,
                                      command = self._undo_callback)
        self._undo_button.pack()
        self._n_cards_removed_last_round = 0    # Number of cards removed from deck in last draw.

    # ---------------------------- BUTTON CALLBACKS ---------------------------

    def _deck_button_callback(self):
        self._undo_button.configure(command = self._undo_callback)
        # If deck is empty make soros the new deck and redraw Blue card.
        if (self.__deck.isEmpty() == True):
            self.__soros.inverse()
            self.__deck = copy.deepcopy(self.__soros)
            self.__soros.makeEmpty()

            self._deck_button.configure(image = self._card_images["Blue"])
            
        self._n_cards_removed_last_round = 0    # Required for undo button

        # Place cards in soros
        for _ in range(3): 
            card = self.__deck.pop()

            if (not isinstance(card, Card)):
                print("End of deck")
                self._deck_button.configure(image = self._card_images["Blank"])
                break
            else:
                self.__soros.push(card.rank(), card.suit())
                self._n_cards_removed_last_round += 1
        
        # Draw soros top three with the third card on top 
        self._draw_top_cards(deck = self.__soros, inv = True)

    def _pick_suitDeck_callback(self, deck_id:int):
        moving_card = self.__soros.pop()
        
        if (isinstance(moving_card, Card) == False): return
        try:
            self.__suit_decks[deck_id].push(moving_card.rank(), moving_card.suit())
            self._undo_button.configure(command = do_nothing)
        except:
            self.__soros.push(moving_card.rank(), moving_card.suit())
            # print("ERROR: Unable to handle this move")
            return
        
        self.draw_suitDeck_card(deck_id, moving_card)
        
        self._draw_top_cards(deck = self.__soros, inv = True)

    def _undo_callback(self):
        """Puts the cards last picked, back to deck.
        Can be used only once per round."""
        if (self.__soros.isEmpty()): return

        # Redraw deck's card 
        if (self.__deck.isEmpty()):
            self._deck_button.configure(image = self._card_images["Blue"])

        for _ in range(self._n_cards_removed_last_round):
            # Remove from soros and place to deck
            go_back_card = self.__soros.pop()
            self.__deck.push(go_back_card.rank(), go_back_card.suit())
        
        self._n_cards_removed_last_round = 0    # Makes undo button callable only once

        # If after removal soros has no cards left
        if (self.__soros.isEmpty()):
            # Redraw Blank card
            blank_image = self._card_images["Blank"]
            self._soros_cards_canvas.configure(width = blank_image.width(),
                                               height= blank_image.height())
            self._soros_cards_canvas.create_image(0, 0, anchor = tk.NW,
                                                  image = blank_image)
        else:
            # Redraw soros
            self._draw_top_cards(deck = self.__soros, inv = True)
        
    # ------------------------------ LOAD IMAGES ------------------------------

    def _load_images(self, dim):
        """ Load cards, blank image and blue card and
        resize them with the dimensions given."""
        # Load Deck
        for fname in os.listdir(os.path.join(self._img_folder, self._card_img_folder)):
            img = Image.open(os.path.join(self._img_folder, 
                                          self._card_img_folder, fname))
            img = img.resize(dim)

            card_name = fname.strip(".png")
            self._card_images[card_name] = ImageTk.PhotoImage(img)
        
        # Load the Blank card
        img = Image.open(os.path.join(self._img_folder ,"Blank_img.jpg"))
        img = img.resize(dim)
        self._card_images["Blank"] = ImageTk.PhotoImage(img)

        # Load the Blue playing card
        img = Image.open(os.path.join(self._img_folder ,"Blue_playing_card.jpg"))
        img = img.resize(dim)
        self._card_images["Blue"] = ImageTk.PhotoImage(img)

    # ------------------------------- DRAWING ---------------------------------

    # TODO add a method to draw soros

    def _draw_top_cards(self, deck:Deck, n:int = 3, inv:bool = False):
        """Given a deck, it draws the first n cards.
        n: int, default value is 3.
        inv: bool, if true prints the top n cards in reverse order
        (useful for soros) """
        x_overlap = 20
        y_overlap = 0

        # First n cards. (top_cards[0] is the deck's top card)
        top_cards = deck.top_cards(n)
        
        # When deck is Empty draw blank card
        if (deck.isEmpty()):
            self._soros_cards_canvas.create_image(0, 0, anchor = tk.NW,
                                                  image = self._card_images["Blank"])
        
        if (inv == True): top_cards.reverse()

        for i, card in enumerate(top_cards):
            card_img = self._card_images[card.id()]
            overlap_images(self._soros_cards_canvas, card_img,
                           x_overlap, y_overlap, i)

    def draw_suitDeck_card(self, deck_id:int, card:Card):
        """Add a card on the SuitDeck Canvas vertically."""
        card_img = self._card_images[card.id()]        
        overlap_images(self._all_SuitDeck_canvas[deck_id], card_img, 0, 35,
                       self.__suit_decks[deck_id].nCards() - 1)

    def draw(self):
        """Draw window"""
        self._root.mainloop()

def do_nothing(): print("Do nothing")

def overlap_images(canvas, img, overlap_x, overlap_y, n:int):
    """Insert the n-th image (counting starts from 0) on a canvas.
    Images overlap by overlap_x on x axis and by overlap_y on y axis.
    All images are assumed to have the same size."""

    # Modify canvas' size
    canvas.config(width = img.width() + n * overlap_x,
                  height = img.height() + n * overlap_y)

    # Draw image starting at position (n * overlap_x, n * overlap_y)
    # Anchor point is the axis origin
    canvas.create_image(n*overlap_x, n*overlap_y, anchor = tk.NW, image = img)

if __name__ == "__main__":
    # random.seed(100)
    d = Deck()

    win = GameWindow(d)

    win.draw()