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

window = tk.Tk()
window.title("Testing Tkinter")

def on_closing(event): window.destroy()

window.configure(background = "green")
# window.geometry("720x1080")

# ------ Close window with Ctrl + W -------
# window.bind("<Control-w>", lambda event: on_closing())

window.bind("<Control-w>", on_closing) #Key Binding


card_fnames = os.listdir("./card_imgs")

# ----------------------------------------------
# ------------ Print the whole deck ------------
# ----------------------------------------------

# r = -1 # row
# c = 0 # column
# for k, i in enumerate(card_fnames):
#     if (k % 13 == 0): r += 1; c = 0
#     else: c += 1
#     frame = tk.Frame(master = window)
#     frame.grid(row = r, column = c, padx = 5, pady = 5)
#     img = find_card("card_imgs/" + i)
#     label_img = tk.Label(master = frame, image = img)
#     # ------- Avoid garbage collection ------
#     label_img.image = img
#     # ---------------------------------------
#     label_img.pack()

# ----------------------------------------------
# ------------ Add button for next card --------
# ----------------------------------------------

frame_single_card = tk.Frame(master = window)
frame_single_card.pack(padx = 10, pady = 10)

img_single_card = find_card("./card_imgs/2c.png")
label_single_card = tk.Label(master = frame_single_card, image = img_single_card)
label_single_card.pack()

# Pick a random card from card_imgs directory
def foo():
    print("Button pressed.")
    iimg = find_card("./card_imgs/" + random.choice(card_fnames))
    label_single_card.config(image = iimg)
    # ----- Avoid garbage collection -----
    label_single_card.image = iimg

# Add button
button_single_card = tk.Button(master = window,
                               width=10,
                               height = 1,
                               pady = 10,
                               text= "Next Card",
                               command = foo)
button_single_card.pack()
window.mainloop()