import tkinter as tk
from PIL import Image, ImageTk

# def overlap_images(canvas, image1, image2, overlap_x, overlap_y):
#     # Get the size of the images
#     width1, height1 = image1.width(), image1.height()
#     width2, height2 = image2.width(), image2.height()

#     # Calculate the total size of the canvas
#     canvas_width = max(width1, width2 + overlap_x)
#     canvas_height = max(height1, height2 + overlap_y)

#     # Create a Canvas widget with the calculated size
#     canvas.config(width=canvas_width, height=canvas_height)

#     # Draw the first image onto the canvas
#     canvas.create_image(0, 0, anchor=tk.NW, image=image1)
#     # canvas.create_image(0, 0, image=image1)

#     # Draw the second image with overlap
#     canvas.create_image(overlap_x, overlap_y, anchor=tk.NW, image=image2)

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

# Create a Tkinter window
root = tk.Tk()
root.title("Image Overlap")

# Load your images (replace 'image1.png' and 'image2.png' with your image filenames)
image1 = Image.open("card_imgs/2c.png")
image1 = image1.resize((100, 130))
image1 = ImageTk.PhotoImage(image1)

image2 = Image.open("card_imgs/3c.png")
image2 = image2.resize((100, 130))
image2 = ImageTk.PhotoImage(image2)

# image1 = tk.PhotoImage(file='card_imgs/2c.png')
# image2 = tk.PhotoImage(file='card_imgs/3c.png')

# Create a Canvas widget
canvas = tk.Canvas(root, width=max(image1.width(), image2.width()), height=max(image1.height(), image2.height()))
canvas2 = tk.Canvas(root, width=max(image1.width(), image2.width()), height=max(image1.height(), image2.height()))
canvas.grid(row = 0, column = 0, padx = 10)
canvas2.grid(row = 0, column = 1, padx = 10)


# Set the overlap distance (adjust as needed)
overlap_x = 0
overlap_y = 30

# Call the function to overlap and display images
for i in range(12):
    overlap_images(canvas, image1, i, overlap_x, overlap_y)

overlap_images(canvas2, image2, 1, overlap_x, overlap_y)

# Start the Tkinter event loop
root.mainloop()
