import numpy as np
import cv2


def make_image_grid(images, num_rows=2, num_cols=6, selected_idx=-1, active_idx=[]):
    """
    Combine a list of images into a grid.

    Parameters:
    images (list): List of image arrays.
    num_rows (int): Number of rows in the grid.
    num_cols (int): Number of columns in the grid.
    selected_idx (int): Index of the selected image.
    active_idx (list): List of indices of active images.

    Returns:
    ndarray: Image grid.
    """

    # Calculate total number of images and required grid size
    total_images = len(images)
    grid_height = num_rows * (images[0].shape[0] + 6)
    grid_width = num_cols * (images[0].shape[1] + 6)

    # Create an empty grid to hold the combined images
    grid = np.zeros((grid_height, grid_width, images[0].shape[2]), dtype=np.uint8)

    # Fill the grid with images
    for i in range(num_rows):
        for j in range(num_cols):
            index = i * num_cols + j
            if index < total_images:
                image = images[index]

                border_color = (255, 255, 255)

                if index == selected_idx:
                    border_color = (0, 0, 0)
                elif index in active_idx:
                    border_color = (0, 255, 0)

                image = cv2.copyMakeBorder(
                    image, 3, 3, 3, 3, cv2.BORDER_CONSTANT, value=border_color
                )

                # Check if the current index is equal to selected_idx

                grid[
                    i * image.shape[0] : (i + 1) * image.shape[0],
                    j * image.shape[1] : (j + 1) * image.shape[1],
                    :,
                ] = image
    return grid
