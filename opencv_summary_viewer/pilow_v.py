import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Example of using Pillow to write text on an image
# Create a NumPy array as the image source
image_array = np.zeros((1080, 1920, 3), dtype=np.uint8)

# Convert the NumPy array to a Pillow image
image = Image.fromarray(image_array)

# Create a drawing object
draw = ImageDraw.Draw(image)

# Define the text to be written
text = "Hello, World!"

# Define the font style and size
font = ImageFont.truetype("path/to/font.ttf", size=30)

# Define the position where the text should be written
position = (10, 10)

# Define the color of the text
color = (255, 0, 0)  # red color

# Write the text on the image
draw.text(position, text, font=font, fill=color)

# Save the modified image
image.save("result.jpg")
