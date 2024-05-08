# %%
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def add_text_to_image(image_array, text, font_path, font_size, position, color):
    # Convert the NumPy array to a Pillow image
    image = Image.fromarray(image_array)

    # Create a drawing object
    draw = ImageDraw.Draw(image)

    # Define the font style and size
    font = ImageFont.truetype(font_path, size=font_size)

    # Write the text on the image
    draw.text(position, text, font=font, fill=color)

    # Convert the Pillow image back to a NumPy array
    modified_image_array = np.array(image)

    return modified_image_array


# Example usage
image_array = np.zeros((1080, 1920, 3), dtype=np.uint8)
text = "Hello, World!\nThis is a test message."
font_path = "./basic_sans_serif_7.ttf"
font_size = 30
position = (10, 10)
color = (255, 0, 0)  # red color

modified_image_array = add_text_to_image(
    image_array, text, font_path, font_size, position, color
)
plt.figure()
plt.imshow(modified_image_array)
