import numpy as np
import cv2


def make_image_grid(
    images, types, num_rows=2, num_cols=6, selected_idx=-1, active_idx=[], ignore_idx=[]
):
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
                mtype = types[index]

                border_color = (255, 255, 255)
                if mtype == "false_positive":
                    border_color = (0, 0, 255)
                elif mtype == "false_negative":
                    border_color = (255, 0, 0)

                if index == selected_idx:
                    border_color = (0, 0, 0)
                elif index in active_idx:
                    border_color = (0, 255, 0)
                elif index in ignore_idx:
                    border_color = (50, 50, 50)

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


def compute_iou(box1, box2):
    """
    Compute intersection over union (IoU) between two bounding boxes.
    box1 and box2 should be in format [x, y, w, h].
    """
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2

    # Compute coordinates of intersection rectangle
    x_left = max(x1, x2)
    y_top = max(y1, y2)
    x_right = min(x1 + w1, x2 + w2)
    y_bottom = min(y1 + h1, y2 + h2)

    # If boxes do not intersect, return 0
    if x_right < x_left or y_bottom < y_top:
        return 0.0

    # Compute intersection area
    intersection_area = (x_right - x_left) * (y_bottom - y_top)

    # Compute union area
    box1_area = w1 * h1
    box2_area = w2 * h2
    union_area = box1_area + box2_area - intersection_area

    # Compute IoU
    iou = intersection_area / union_area
    return iou
