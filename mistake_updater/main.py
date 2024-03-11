# %%
import cv2
from pathlib import Path
import pickle

import numpy as np


def make_image_grid(images, num_rows=4, num_cols=5):
    """
    Combine a list of images into a grid.

    Parameters:
    images (list): List of image arrays.
    num_rows (int): Number of rows in the grid.
    num_cols (int): Number of columns in the grid.

    Returns:
    ndarray: Image grid.
    """

    # Calculate total number of images and required grid size
    total_images = len(images)
    grid_height = num_rows * images[0].shape[0]
    grid_width = num_cols * images[0].shape[1]

    # Create an empty grid to hold the combined images
    grid = np.zeros((grid_height, grid_width, images[0].shape[2]), dtype=np.uint8)

    # Fill the grid with images
    for i in range(num_rows):
        for j in range(num_cols):
            index = i * num_cols + j
            if index < total_images:
                image = images[index]
                grid[
                    i * image.shape[0] : (i + 1) * image.shape[0],
                    j * image.shape[1] : (j + 1) * image.shape[1],
                    :,
                ] = image
    return grid


model_dir = Path("/data/proposed")
mistake_files = list(model_dir.rglob("*.pkl"))
for mfile in mistake_files:
    with open(mfile, "rb") as f:
        data = pickle.load(f)
    # for mistake in data[0][0]:
    print(data)
    break

#     max_items_for_grid = 20

#     # split data into chunks
#     chunked_data = [
#         data[0][0][i : i + max_items_for_grid]
#         for i in range(0, len(data[0][0]), max_items_for_grid)
#     ]

#     for chunk in chunked_data:
#         print(chunk)
#         images = [x["crop"] for x in chunk]
#         grid = make_image_grid(images)
#         cv2.imshow("imgrid", grid)
#         cv2.waitKey(0)

# cv2.destroyAllWindows()

# Example usage:
# Assuming 'images' is a list of image arrays
# grid = make_image_grid(images)

# Display the grid
# plt.imshow(grid)
# plt.axis('off')
# plt.show()

# %%
