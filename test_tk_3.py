# Testing TopLevel() and multiple windows.
# Also operations have been placed inside functions
import os
import random
import tkinter as tk
from PIL import Image, ImageTk

def find_card(cardname:str):
    """
    Finds the card with the cardname given and returns
    the image object for Tkinter frame, otherwise returns None.
    """
    try:
        img = Image.open(cardname)
        img = img.resize((100, 100))
    except:
        print("Error")
        return None
    
    return ImageTk.PhotoImage(img)

# ----------------------------------------------
# ------------ Print the whole deck ------------
# ----------------------------------------------
def full_deck(win):
    card_fnames = os.listdir("./card_imgs")
    r = -1 # row
    c = 0 # column
    for k, i in enumerate(card_fnames):
        if (k % 13 == 0): r += 1; c = 0
        else: c += 1
        frame = tk.Frame(master = win)
        frame.grid(row = r, column = c, padx = 5, pady = 5)
        img = find_card("card_imgs/" + i)
        label_img = tk.Label(master = frame, image = img)
        # ------- Avoid garbage collection ------
        label_img.image = img
        # ---------------------------------------
        label_img.pack()

# ---------------------------------------------
# ------------ Add button for next card --------
# ----------------------------------------------
def random_card(win):
    card_fnames = os.listdir("./card_imgs")
    frame_single_card = tk.Frame(master = win)
    frame_single_card.pack(padx = 10, pady = 10)

    img_single_card = find_card("./card_imgs/2c.png")
    label_single_card = tk.Label(master = frame_single_card,
                                 image = img_single_card)
    # ----- Avoid garbage collection -----
    label_single_card.image = img_single_card
    label_single_card.pack()

    # Pick a random card from card_imgs directory
    def foo():
        print("Button pressed.")
        iimg = find_card("./card_imgs/" + random.choice(card_fnames))
        label_single_card.config(image = iimg)
        # ----- Avoid garbage collection -----
        label_single_card.image = iimg

    # Add button
    button_single_card = tk.Button(master = win,
                                width=10,
                                height = 1,
                                pady = 10,
                                text= "Next Card",
                                command = foo)
    button_single_card.pack()

root = tk.Tk()
root.title("Root window")

root.configure(background = "green")

random_card(root)

window2 = tk.Toplevel()
window2.title("Window 2")
window2.configure(bg = "blue")
full_deck(window2)

root.mainloop()