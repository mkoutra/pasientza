# The window of the pasientza game using tkinter.
import os
import tkinter as tk
from PIL import Image, ImageTk

class GameWindow:
    def __init__(self):
        #TODO make arguments optional
        self._dimensions = (960, 600)
        self._background = "green"
        self._title = "Pasientza"
        self.img_folder = "card_imgs"

        # Create root window
        self._root = tk.Tk()
        self._root.geometry(str(self._dimensions[0]) + "x"
                            + str(self._dimensions[1]))
        self._root.configure(background = self._background)
        self._root.title(self._title)

        # Add blank image
        # for i in range(8):
            # self.draw_card("blank_img.jpg", 0, i)

    def draw_card(self, card_id:str, row, col):
        img = find_card(os.path.join(self.img_folder, card_id))
        lbl = tk.Label(master = self._root, image = img)
        lbl.image = img
        lbl.grid(row = row, column = col, padx = 5, pady = 5)

    def draw_deck(self):
        image = find_card(os.path.join(self.img_folder, "2c.png"))
        canvas = tk.Canvas(self._root, width = image.width(), height = image.height())
        canvas.grid(row = 0, column = 0, padx = 10)
        canvas.image = image
        # Set the overlap distance (adjust as needed)
        overlap_x = 0
        overlap_y = 40
        
        # Call the function to overlap and display images
        for i in range(12):
            overlap_images(canvas, image, i, overlap_x, overlap_y)

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

def overlap_images(canvas, image, i, overlap_x, overlap_y):
    # Get the size of the images
    width, height = image.width(), image.height()

    # Calculate the total size of the canvas
    canvas_width = max(width, width + overlap_x)
    canvas_height = max(height, (height + i*overlap_y))

    # Create a Canvas widget with the calculated size
    canvas.config(width=canvas_width, height=canvas_height)

    # Draw an image at position (i*overlap_x, i*overlap_y)
    canvas.create_image(i*overlap_x, i*overlap_y, anchor=tk.NW, image=image)

if __name__ == "__main__":
    win = GameWindow()

    win.draw_deck()

    win.draw()