import cv2
import numpy as np


def scale_image_with_padding(image, target_resolution):
    """
    Scales an image represented as a NumPy array to a given resolution with changing the aspect ratio.
    Adds black bars for padding if necessary.

    Parameters:
        image (numpy.ndarray): Input image represented as a NumPy array.
        target_resolution (tuple): Target resolution (width, height).

    Returns:
        numpy.ndarray: Scaled image.
    """
    # Get dimensions of the input image
    height, width = image.shape[:2]

    # Calculate the aspect ratio of the input image
    aspect_ratio = width / height

    # Unpack target resolution
    target_width, target_height = target_resolution

    # Calculate target aspect ratio
    target_aspect_ratio = target_width / target_height

    # Calculate scaling factors for width and height
    if aspect_ratio > target_aspect_ratio:
        # Fit width, pad height
        new_width = target_width
        new_height = int(target_width / aspect_ratio)
        padding_top = (target_height - new_height) // 2
        padding_bottom = target_height - new_height - padding_top
    else:
        # Fit height, pad width
        new_height = target_height
        new_width = int(target_height * aspect_ratio)
        padding_left = (target_width - new_width) // 2
        padding_right = target_width - new_width - padding_left

    # Resize the image
    resized_image = cv2.resize(image, (new_width, new_height))

    # Add padding if necessary
    if aspect_ratio > target_aspect_ratio:
        padding = [(0, padding_top), (0, padding_bottom), (0, 0)]
    else:
        padding = [(0, 0), (padding_left, padding_right), (0, 0)]

    padded_image = np.pad(resized_image, padding, mode="constant", constant_values=0)

    return padded_image


# Example usage:
# Load an image using OpenCV
image = np.ones((1000, 700, 3), dtype=np.uint8) * 255

# Target resolution
target_resolution = (1080, 1920)

# Scale the image
scaled_image = scale_image_with_padding(image, target_resolution)

# Display or save the scaled image
cv2.imshow("Scaled Image", scaled_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
