# The window of the Pasientza game using tkinter.
import copy
import os

import tkinter as tk
from PIL import Image, ImageTk

from Cards import Card, Deck, SuitDeck

class GameWindow:
    """The Window for the Pasientza game."""

    def __init__(self, deck):
        # Create decks variables needed to play the game
        self.__deck = deck
        self.__soros = Deck(full = False)   # Cards removed from deck
        self.__suit_decks:list = [SuitDeck() for _ in range(8)]
        self._n_cards_removed_last_round = 0
        self._n_suitdecks = 8

        # Window configuration
        self._win_dimensions = (980, 800)
        self._background = "seagreen4"
        self._title = "Pasientza"

        # Images info
        self._img_folder = "imgs"
        self._card_img_folder = "card_imgs"
        self._card_dimensions = (100, 130)
        self._card_images:dict = {} # Mapping card id, e.g. "10s" to image

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
                            + "x"
                            + str(self._win_dimensions[1]))

        # Create Frames
        frames_configurations = {"master": self._root,
                                 "bg": self._background}

        self._suitDecks_frame = tk.Frame(**frames_configurations)
        self._deck_frame = tk.Frame(**frames_configurations)
        self._soros_frame = tk.Frame(**frames_configurations)
        self._undo_frame = tk.Frame(**frames_configurations)
        self._replay_frame = tk.Frame(**frames_configurations)

        # Place frames on the root window
        self._suitDecks_frame.place(relx = 0.0, rely = 0.02, anchor = tk.NW)
        self._deck_frame.place(relx = 0.4, rely = .75, anchor = tk.NW)
        self._soros_frame.place(relx = 0.55, rely = .75, anchor = tk.NW)
        self._undo_frame.place(relx = .85, rely = .9, anchor = tk.NW)
        self._replay_frame.place(relx = .85, rely = .8, anchor = tk.NW)

        # Load Playing Cards
        self._load_images(dim = self._card_dimensions)

        # Create SuitDeck frames, canvas and buttons
        self._all_SuitDeck_canvas:list = []
        self._all_SuitDecks_buttons:list = []

        for i in range(self._n_suitdecks):
            # Create frame to store canvas and button
            suitDeck_frame = tk.Frame(master = self._suitDecks_frame,
                                      bg = self._background)

            suitdeck_canv = tk.Canvas(master = suitDeck_frame)

            suitDeck_but = tk.Button(
                master = suitDeck_frame,
                text = "Deck " + str(i + 1),
                width = 8, height = 1,
                **button_configuration,
                command = lambda x = i : self._pick_suitDeck_callback(x))

            self._all_SuitDecks_buttons.append(suitDeck_but)
            self._all_SuitDeck_canvas.append(suitdeck_canv)

            suitDeck_frame.grid(row = 0, column = i, padx = 10, sticky=tk.NW)

        self._soros_canvas = tk.Canvas(master = self._soros_frame,
                                       width = self._card_dimensions[0],
                                       height = self._card_dimensions[1])

        # ------------------------------- Buttons ------------------------------
        self._deck_button = tk.Button(master = self._deck_frame,
                                      image = self._card_images["Blue"],
                                      activebackground = "steelblue3",
                                      relief = tk.RAISED,
                                      command = self._deck_button_callback)

        self._undo_button = tk.Button(master = self._undo_frame,
                                      text = "Undo",
                                      width = 4, height = 1,
                                      state = tk.DISABLED,
                                      **button_configuration,
                                      command = self._undo_callback)

        self._replay_button = tk.Button(master = self._replay_frame,
                                        text = "New game",
                                        width = 7, height = 1,
                                        **button_configuration,
                                        command = self._replay_callback)

        # ------------------------- Widget placement --------------------------
        self._soros_canvas.pack()
        self._deck_button.pack(padx = 10)
        self._undo_button.pack(pady = 5)
        self._replay_button.pack(pady = 5)
        for i in range(self._n_suitdecks):
            self._all_SuitDecks_buttons[i].pack(pady = 5)
            self._all_SuitDeck_canvas[i].pack(pady = 5)
        
        # ------------------------------ Drawing ------------------------------
        self._draw_initial_state()

    # ---------------------------- Button Callbacks ---------------------------

    def _deck_button_callback(self):
        # Modify undo button
        self._undo_button.configure(
            state = tk.NORMAL,
            command = self._undo_callback)

        self._n_cards_removed_last_round = 0    # Required for undo button

        # If deck is empty make soros the new deck and redraw Blue card.
        if self.__deck.is_empty():
            self.__soros.inverse()
            del self.__deck
            self.__deck = copy.deepcopy(self.__soros)
            self.__soros.make_empty()

            self._deck_button.configure(image = self._card_images["Blue"])

        # Place cards in soros
        for _ in range(3):
            card = self.__deck.pop()

            if not isinstance(card, Card):
                self._deck_button.configure(image = self._card_images["Blank"])
                break

            self.__soros.push(card)
            self._n_cards_removed_last_round += 1

        self._draw_soros()

    def _pick_suitDeck_callback(self, deck_id:int):
        moving_card = self.__soros.pop()

        if not isinstance(moving_card, Card):
            return

        try:
            self.__suit_decks[deck_id].push(moving_card)
            self._undo_button.configure(state = tk.DISABLED)
            self.draw_card_in_suitDeck(deck_id, moving_card)
            self._draw_soros()
        except:
            # Move card back to soros
            self.__soros.push(moving_card)

    def _undo_callback(self):
        """Puts the cards last picked, back to deck.
        Can be used only once per round."""
        if self.__soros.is_empty():
            return

        # Redraw deck's card
        if self.__deck.is_empty():
            self._deck_button.configure(image = self._card_images["Blue"])

        for _ in range(self._n_cards_removed_last_round):
            # Remove from soros and place to deck
            go_back_card = self.__soros.pop()
            self.__deck.push(go_back_card)

        # Makes undo button callable only once
        self._n_cards_removed_last_round = 0
        self._undo_button.configure(state = tk.DISABLED)

        self._draw_soros()

    def _replay_callback(self):
        # Remove cards from suitDecks
        for i in range(self._n_suitdecks):
            self.__suit_decks[i].make_empty()

        # Remove all elements from deck and soros
        del self.__deck
        del self.__soros
        self.__deck = Deck(full = True)
        self.__soros = Deck(full = False)

        self._n_cards_removed_last_round = 0

        # Draw decks in initial state
        self._draw_initial_state()

    # ------------------------------ LOAD IMAGES ------------------------------

    def _load_images(self, dim):
        """ Load cards, blank image and blue card and
        resize them with the dimensions given."""
        # Load playing cards
        for fname in os.listdir(
            os.path.join(self._img_folder, self._card_img_folder)):
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
        img = Image.open(
            os.path.join(self._img_folder, "Blue_playing_card.jpg"))
        img = img.resize(dim)
        self._card_images["Blue"] = ImageTk.PhotoImage(img)

    # ------------------------------- DRAWING ---------------------------------

    def _draw_initial_state(self):
        """Draw the decks when the game starts."""

        blank_image = self._card_images["Blank"]

        # Draw the top of the deck button
        self._deck_button.configure(image = self._card_images["Blue"])

        # Draw soros
        self._draw_soros()

        # Draw the blank card on every suitDeck
        for i in range(self._n_suitdecks):
            self._all_SuitDeck_canvas[i].delete("all")

            self._all_SuitDeck_canvas[i].configure(
                width = self._card_dimensions[0],
                height = self._card_dimensions[1])

            self._all_SuitDeck_canvas[i].create_image(0, 0, anchor = tk.NW,
                                                      image = blank_image)

    def _draw_soros(self):
        if self.__soros.is_empty():
            self._soros_canvas.delete('all')

            self._soros_canvas.configure(
                width = self._card_dimensions[0],
                height = self._card_dimensions[1])

            self._soros_canvas.create_image(
                0, 0, anchor = tk.NW,
                image = self._card_images["Blank"])
        else:
            # Draw soros top three with the third card on top
            self._soros_canvas.delete('all')
            self._draw_top_cards(deck = self.__soros, inv = True)

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
        if deck.is_empty():
            self._soros_canvas.delete("all")
            self._soros_canvas.create_image(
                0, 0, anchor = tk.NW,
                image = self._card_images["Blank"])

        if inv:
            top_cards.reverse()

        for i, card in enumerate(top_cards):
            card_img = self._card_images[card.id()]
            overlap_images(self._soros_canvas, card_img,
                           x_overlap, y_overlap, i)

    def draw_card_in_suitDeck(self, deck_id:int, card:Card):
        """Add a card on the SuitDeck Canvas vertically."""
        card_img = self._card_images[card.id()]

        overlap_images(self._all_SuitDeck_canvas[deck_id], card_img, 0, 35,
                       self.__suit_decks[deck_id].number_of_cards() - 1)

    def draw(self):
        """Draw window"""
        self._root.mainloop()


def overlap_images(canvas, img, overlap_x, overlap_y, n:int):
    """Insert the n-th image (counting starts from 0) on a canvas.
    Images overlap by overlap_x on x axis and by overlap_y on y axis.
    All images are assumed to have the same size."""

    # Draw image starting at position (n * overlap_x, n * overlap_y)
    canvas.create_image(n*overlap_x, n*overlap_y, anchor = tk.NW, image = img)

    # Modify canvas' size
    canvas.config(width = img.width() + n * overlap_x,
                  height = img.height() + n * overlap_y)

if __name__ == "__main__":
    d = Deck()

    win = GameWindow(d)

    win.draw()
