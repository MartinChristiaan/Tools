#%%
import os
from PIL import Image

def crop_and_resize(image_path,  size=(256, 256)):
    # Create output folder if it doesn't exist

    # Open the image
    img = Image.open(image_path)

    # Crop the image to make it square
    width, height = img.size
    if width > height:
        left = (width - height) / 2
        right = (width + height) / 2
        top = 0
        bottom = height
    else:
        left = 0
        right = width
        top = (height - width) / 2
        bottom = (height + width) / 2
    img = img.crop((left, top, right, bottom))

    # Resize the image
    img = img.resize(size)

    return img


def create_image_grid(image_folder, output_folder, columns=5, size=(128, 128)):
    # List all image files in the folder
    image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]

    # Calculate dimensions of the final image
    rows = len(image_files) // columns + (1 if len(image_files) % columns != 0 else 0)
    final_width = columns * size[0]
    final_height = rows * size[1]

    # Create a blank canvas to paste images onto
    final_image = Image.new('RGB', (final_width, final_height), color='white')

    # Paste images onto the canvas
    for i, image_file in enumerate(image_files):
        img = crop_and_resize(os.path.join(image_folder, image_file), size=size)
        row = i // columns
        col = i % columns
        x_offset = col * size[0]
        y_offset = row * size[1]
        final_image.paste(img, (x_offset, y_offset))

    # Save the final image
    final_image.save( 'grid_image.png')

if __name__ == "__main__":
    input_folder = "/data/example_detections"
    create_image_grid(input_folder, "")
